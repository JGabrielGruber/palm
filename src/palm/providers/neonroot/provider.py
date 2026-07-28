"""NeonRoot resource provider — hermetic isolation as a Palm resource (0.53)."""

from __future__ import annotations

from typing import Any

from palm.core.resource import BaseProvider
from palm.core.resource.result import ProviderDescriptor, ProviderHealth, ProviderResult
from palm.providers.neonroot.bindings.resource.descriptor import describe
from palm.providers.neonroot.cli import probe_neonroot
from palm.providers.neonroot.run_script import run_script_job
from palm.providers.neonroot.spawn import resolve_repo_root, run_spawn


class NeonrootProvider(BaseProvider):
    """Invoke NeonRoot from the resource engine (optional host binary)."""

    def connect(self) -> None:
        """No persistent connection — each probe is independent."""

    def disconnect(self) -> None:
        pass

    def fetch(self, resource_id: str, **params: Any) -> Any:
        """NeonRoot has no fetch-by-id; use ``invoke('health')`` / ``spawn``."""
        raise RuntimeError(
            "neonroot provider does not support fetch; use invoke(action='health'|'spawn'|…)"
        )

    def invoke(
        self,
        action: str,
        *,
        params: dict[str, Any] | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> ProviderResult:
        merged = dict(params or {})
        merged.update(kwargs)
        if resource_id is not None:
            merged.setdefault("resource_id", resource_id)

        if action == "health":
            probe = probe_neonroot()
            data = probe.as_dict()
            if probe.available:
                return ProviderResult.ok(data, action=action, provider=self.name)
            # Do not pass data["error"] as kwargs — fail() already takes error=
            meta = {k: v for k, v in data.items() if k != "error" and v is not None}
            return ProviderResult.fail(
                probe.error or "neonroot unavailable",
                action=action,
                provider=self.name,
                **meta,
            )

        if action == "spawn":
            return self._spawn_result(merged, action=action)

        if action == "run_script":
            try:
                payload = run_script_job(merged)
            except (ValueError, RuntimeError) as exc:
                return ProviderResult.fail(str(exc), action=action, provider=self.name)
            except Exception as exc:
                return ProviderResult.fail(
                    f"run_script failed: {exc}",
                    action=action,
                    provider=self.name,
                )
            return self._spawn_result_from_payload(payload, action=action)

        if action in ("list_images", "image.ensure", "image.build"):
            return ProviderResult.fail(
                f"action {action!r} not implemented yet",
                action=action,
                provider=self.name,
            )

        return ProviderResult.fail(
            f"Unsupported action {action!r}",
            action=action,
            provider=self.name,
        )

    def _spawn_result(self, merged: dict[str, Any], *, action: str) -> ProviderResult:
        # 0.56 — prefer WorkloadEngine + neonroot WorkloadRuntime when a Palm
        # runtime is bound (one isolation plane). Else classic CLI spawn.
        from palm.common.workload.neonroot_facade import try_spawn_via_workload

        via_engine = try_spawn_via_workload(merged)
        if via_engine is not None:
            # Preserve action name from invoke (spawn vs run_script path)
            if via_engine.metadata.get("action") != action:
                meta = dict(via_engine.metadata)
                meta["action"] = action
                via_engine = ProviderResult(
                    success=via_engine.success,
                    data=via_engine.data,
                    error=via_engine.error,
                    metadata=meta,
                )
            return via_engine

        try:
            payload = run_spawn(merged, repo_root=resolve_repo_root())
        except (ValueError, RuntimeError) as exc:
            return ProviderResult.fail(str(exc), action=action, provider=self.name)
        except Exception as exc:
            return ProviderResult.fail(
                f"spawn failed: {exc}",
                action=action,
                provider=self.name,
            )
        return self._spawn_result_from_payload(payload, action=action)

    def _spawn_result_from_payload(
        self, payload: dict[str, Any], *, action: str
    ) -> ProviderResult:
        exit_code = payload.get("exit_code")
        if payload.get("timed_out") or exit_code is None:
            return ProviderResult.fail(
                str(payload.get("error") or "spawn timed out or produced no exit code"),
                action=action,
                provider=self.name,
                **{k: v for k, v in payload.items() if k != "error" and v is not None},
            )
        if exit_code != 0:
            stderr = str(payload.get("stderr_tail") or "").strip()
            stdout = str(payload.get("stdout_tail") or "").strip()
            detail = f"spawn command exited {exit_code}"
            # Prefer stderr (runtime errors); fall back to stdout (often neonroot logs).
            tail = stderr or stdout
            if tail:
                # Keep failure lines short for Assist / validation feedback.
                one_line = " | ".join(
                    ln.strip() for ln in tail.splitlines() if ln.strip()
                )[-400:]
                detail = f"{detail}: {one_line}"
            return ProviderResult.fail(
                detail,
                action=action,
                provider=self.name,
                **payload,
            )
        return ProviderResult.ok(payload, action=action, provider=self.name)

    def describe(self) -> ProviderDescriptor:
        return describe(name=self.name)

    def health(self) -> ProviderHealth:
        probe = probe_neonroot()
        if probe.available:
            msg = f"neonroot ready ({probe.version or probe.path})"
            return ProviderHealth(healthy=True, message=msg)
        return ProviderHealth(
            healthy=False,
            message=probe.error or "neonroot not available",
        )


__all__ = ["NeonrootProvider"]
