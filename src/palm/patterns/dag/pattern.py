"""
DAG pattern — execute resource nodes with dependencies (0.54.3 v0).

v0: one ready node per tick (sequential). Nodes invoke ResourceEngine
(resource_ref or provider). State keys under ``dag.*``.
"""

from __future__ import annotations

from typing import Any

from palm.core.behavior_tree import BasePattern, PatternStatus
from palm.core.context import BaseState
from palm.core.resource.engine import ResourceEngine
from palm.core.resource.observability import resource_correlation
from palm.patterns.dag.bindings.definitions.config import DagConfig, DagNodeSpec

_DAG_KEY = "dag"
_STATUS_PENDING = "pending"
_STATUS_SUCCEEDED = "succeeded"
_STATUS_FAILED = "failed"


class DagPattern(BasePattern):
    """Run a DAG of resource invokes; linear or explicit depends_on."""

    def __init__(
        self,
        *,
        name: str = "dag",
        config: DagConfig | None = None,
        resource_engine: ResourceEngine | None = None,
    ) -> None:
        super().__init__(name=name)
        if config is None:
            raise ValueError("DagPattern requires a DagConfig")
        self._config = config
        self._resource_engine = resource_engine
        self._seeded = False

    @property
    def config(self) -> DagConfig:
        return self._config

    def tick(self, state: BaseState) -> PatternStatus:
        self._seed_initial_state(state)
        dag = self._ensure_dag_state(state)

        if dag.get("status") == _STATUS_SUCCEEDED:
            return PatternStatus.SUCCESS
        if dag.get("status") == _STATUS_FAILED:
            return PatternStatus.FAILURE

        # 0.54.8: drain ready-set (and newly unlocked nodes) in one tick when
        # drain_ready; otherwise a single ready node per tick.
        last = PatternStatus.RUNNING
        while True:
            dag = state.get(_DAG_KEY)
            if not isinstance(dag, dict):
                return PatternStatus.FAILURE
            if dag.get("status") == _STATUS_FAILED:
                return PatternStatus.FAILURE
            if dag.get("status") == _STATUS_SUCCEEDED:
                return PatternStatus.SUCCESS

            ready = self._ready_nodes(dag)
            if not ready:
                if self._all_succeeded(dag):
                    dag["status"] = _STATUS_SUCCEEDED
                    state.set(_DAG_KEY, dag)
                    return PatternStatus.SUCCESS
                dag["status"] = _STATUS_FAILED
                dag["error"] = "DAG stuck: no ready nodes and not all succeeded"
                state.set(_DAG_KEY, dag)
                return PatternStatus.FAILURE

            batch = list(ready) if self._config.drain_ready else ready[:1]
            for node in batch:
                dag = state.get(_DAG_KEY)
                if not isinstance(dag, dict) or dag.get("status") == _STATUS_FAILED:
                    return PatternStatus.FAILURE
                st = ((dag.get("nodes") or {}).get(node.id) or {}).get("status")
                if st != _STATUS_PENDING:
                    continue
                node_state = dag.get("nodes") or {}
                deps_ok = all(
                    (node_state.get(d) or {}).get("status") == _STATUS_SUCCEEDED
                    for d in node.depends_on
                )
                if not deps_ok:
                    continue
                last = self._run_node(state, dag, node)
                if last in (PatternStatus.FAILURE, PatternStatus.SUCCESS):
                    return last
            if not self._config.drain_ready:
                break
            # drain_ready: loop to pick up nodes unlocked by this batch (e.g. join)
        return last

    def reset(self) -> None:
        self._seeded = False

    def _seed_initial_state(self, state: BaseState) -> None:
        if self._seeded or not self._config.initial_state:
            return
        for key, value in self._config.initial_state.items():
            if not state.has(key):
                state.set(key, value)
        self._seeded = True

    def _ensure_dag_state(self, state: BaseState) -> dict[str, Any]:
        raw = state.get(_DAG_KEY)
        if isinstance(raw, dict) and raw.get("nodes"):
            return raw
        nodes_state = {
            n.id: {"status": _STATUS_PENDING, "output_key": n.output_key or n.id}
            for n in self._config.nodes
        }
        dag = {
            "status": "running",
            "order": [n.id for n in self._config.nodes],
            "nodes": nodes_state,
        }
        state.set(_DAG_KEY, dag)
        return dag

    def _ready_nodes(self, dag: dict[str, Any]) -> list[DagNodeSpec]:
        node_state = dag.get("nodes") or {}
        ready: list[DagNodeSpec] = []
        for n in self._config.nodes:
            st = (node_state.get(n.id) or {}).get("status")
            if st != _STATUS_PENDING:
                continue
            deps_ok = all(
                (node_state.get(d) or {}).get("status") == _STATUS_SUCCEEDED
                for d in n.depends_on
            )
            if deps_ok:
                ready.append(n)
        return ready

    def _all_succeeded(self, dag: dict[str, Any]) -> bool:
        node_state = dag.get("nodes") or {}
        return all(
            (node_state.get(n.id) or {}).get("status") == _STATUS_SUCCEEDED
            for n in self._config.nodes
        )

    def _run_node(
        self,
        state: BaseState,
        dag: dict[str, Any],
        node: DagNodeSpec,
    ) -> PatternStatus:
        nodes_state: dict[str, Any] = dict(dag.get("nodes") or {})
        entry = dict(nodes_state.get(node.id) or {})
        entry["status"] = "running"
        nodes_state[node.id] = entry
        dag["nodes"] = nodes_state
        dag["current"] = node.id
        state.set(_DAG_KEY, dag)

        if self._resource_engine is None:
            return self._fail_node(state, dag, node, "ResourceEngine is not configured")
        if not self._resource_engine.is_initialized:
            self._resource_engine.initialize()

        result = self._resource_engine.invoke(
            node.resource_ref,
            provider=node.provider,
            action=node.action,
            resource_id=node.resource_id,
            params=dict(node.params),
            state=state,
            correlation=resource_correlation(state, wizard=self.name, step_slug=node.id),
        )

        output_key = node.output_key or node.id
        if result.success:
            state.set(output_key, result.data)
            entry = dict(nodes_state.get(node.id) or {})
            entry["status"] = _STATUS_SUCCEEDED
            entry["output_key"] = output_key
            nodes_state[node.id] = entry
            dag["nodes"] = nodes_state
            if self._all_succeeded(dag):
                dag["status"] = _STATUS_SUCCEEDED
                dag.pop("current", None)
                state.set(_DAG_KEY, dag)
                return PatternStatus.SUCCESS
            state.set(_DAG_KEY, dag)
            return PatternStatus.RUNNING

        err = result.error or "resource invoke failed"
        return self._fail_node(state, dag, node, err)

    def _fail_node(
        self,
        state: BaseState,
        dag: dict[str, Any],
        node: DagNodeSpec,
        error: str,
    ) -> PatternStatus:
        nodes_state = dict(dag.get("nodes") or {})
        entry = dict(nodes_state.get(node.id) or {})
        entry["status"] = _STATUS_FAILED
        entry["error"] = error
        nodes_state[node.id] = entry
        dag["nodes"] = nodes_state
        dag["status"] = _STATUS_FAILED
        dag["error"] = f"node {node.id!r}: {error}"
        dag["current"] = node.id
        state.set(_DAG_KEY, dag)
        state.set(f"dag_error_{node.id}", error)
        return PatternStatus.FAILURE


__all__ = ["DagPattern"]
