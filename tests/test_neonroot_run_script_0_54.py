"""run_script provider action removed (0.56) — use run-python workload dogfood."""

from __future__ import annotations

from examples.definitions.run_python import RUN_PYTHON_FLOW, register_definitions


def test_run_python_replaces_run_script() -> None:
    steps = [s["slug"] for s in RUN_PYTHON_FLOW.options["steps"]]
    assert "run" in steps
    run = next(s for s in RUN_PYTHON_FLOW.options["steps"] if s["slug"] == "run")
    assert run["step_kind"] == "workload"

    class _Repo:
        n = 0

        def save_flow(self, _f):
            self.n += 1

        def save_process(self, _p):
            self.n += 1

    repo = _Repo()
    register_definitions(repo)
    assert repo.n >= 2
