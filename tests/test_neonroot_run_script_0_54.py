"""neonroot.run_script + hermetic-run-code definitions (Assist run-code)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from palm.providers.neonroot.run_script import run_script_job


def test_run_script_allowlist() -> None:
    with pytest.raises(ValueError, match="allowlist"):
        run_script_job(
            {
                "image": "evil-image",
                "code": "print(1)",
            }
        )


def test_run_script_requires_code() -> None:
    with pytest.raises(ValueError, match="code"):
        run_script_job({"image": "palm-ci", "code": "  "})


def test_run_script_stages_and_spawns(tmp_path: Path) -> None:
    captured: dict = {}

    def _fake_spawn(params, **kwargs):
        captured["params"] = dict(params)
        seed = Path(params["seed"])
        assert (seed / "payload" / "main.py").is_file()
        assert "print" in (seed / "payload" / "main.py").read_text(encoding="utf-8")
        return {
            "exit_code": 0,
            "stdout_tail": "hello\n",
            "stderr_tail": "",
            "command": params["command"],
            "image": params["image"],
        }

    with patch("palm.providers.neonroot.run_script.run_spawn", side_effect=_fake_spawn):
        out = run_script_job(
            {
                "image": "palm-ci",
                "code": "print('hello')\n",
                "data_dir": tmp_path,
                "seed_mode": "bind",
            }
        )
    assert out["exit_code"] == 0
    assert out["stdout_tail"] == "hello\n"
    assert captured["params"]["seed_mode"] == "bind"
    assert captured["params"]["command"] == ["python", "payload/main.py"]
    # GC removes run dir by default
    assert list(tmp_path.joinpath("palm/hermetic/runs").glob("*")) == []


def test_provider_run_script_action() -> None:
    import palm.providers  # noqa: F401
    from palm.core.registry import provider_registry

    p = provider_registry.get("neonroot")(name="neonroot")
    with patch(
        "palm.providers.neonroot.provider.run_script_job",
        return_value={
            "exit_code": 0,
            "stdout_tail": "ok\n",
            "stderr_tail": "",
            "image": "palm-ci",
        },
    ):
        result = p.invoke(
            "run_script",
            params={"image": "palm-ci", "code": "print(1)"},
        )
    assert result.success is True
    assert result.data["stdout_tail"] == "ok\n"


def test_hermetic_run_code_definitions() -> None:
    from examples.definitions.hermetic_run_code import (
        HERMETIC_RUN_CODE_FLOW,
        HERMETIC_RUN_SCRIPT,
        register_definitions,
    )

    assert HERMETIC_RUN_SCRIPT.provider == "neonroot"
    assert HERMETIC_RUN_SCRIPT.action == "run_script"
    assert "{{ state.code }}" in str(HERMETIC_RUN_SCRIPT.params.get("code"))
    assert HERMETIC_RUN_CODE_FLOW.pattern == "wizard"
    steps = [s["slug"] for s in HERMETIC_RUN_CODE_FLOW.options["steps"]]
    assert "image" in steps and "code" in steps and "run" in steps

    class _Repo:
        def __init__(self) -> None:
            self.n = 0

        def save_resource(self, _r):
            self.n += 1

        def save_flow(self, _f):
            self.n += 1

        def save_process(self, _p):
            self.n += 1

    repo = _Repo()
    register_definitions(repo)
    assert repo.n == 3
