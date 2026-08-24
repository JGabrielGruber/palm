"""0.68.3 — living POST lies composted."""

from __future__ import annotations

from pathlib import Path

from palm.system.runtime.job_hooks.outbox_drain import OutboxDrainHook
from palm.system.subsystems.supervisor.outbox_loop import OutboxLoopService

ROOT = Path(__file__).resolve().parents[2]
LIE = "POST outbox events to external URLs before mark-published"


def test_living_docs_do_not_promise_outbox_post() -> None:
    for rel in (
        "ARCHITECTURE.md",
        "README.md",
        "docs/llms.txt",
        "src/palm/runtimes/mcp/data/llms.txt",
        "website/llms.txt",
        "website/dist/llms.txt",
        "docs/EVENT-PLANE.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert LIE not in text
        assert "optional webhook dispatch" not in text


def test_production_drain_does_not_pass_on_before_publish() -> None:
    import inspect

    loop_src = inspect.getsource(OutboxLoopService)
    hook_src = inspect.getsource(OutboxDrainHook)
    assert "on_before_publish" not in loop_src
    assert "on_before_publish" not in hook_src
    assert "process_batch" in loop_src
    assert "process_batch" in hook_src
