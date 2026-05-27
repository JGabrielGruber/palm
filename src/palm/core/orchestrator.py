"""
Orchestrator - the top-level coordinator of the Palm engine.

It wires together:
- WizardEngine (interactive sessions)
- ProcessManager (background workers)
- EventBus (observability)
- Persistence

This is the primary object a daemon, TUI, or API server would hold.
"""

from __future__ import annotations

from typing import Any

from palm.core.events import EventBus
from palm.core.process_manager import ProcessManager
from palm.core.wizard.engine import WizardEngine
from palm.core.workflow.registry import WorkflowRegistry
from palm.persistence.sqlite import SQLiteSessionStore


class Orchestrator:
    """
    Central facade for the Palm engine.

    In production this would be instantiated once per process (or per node).
    """

    def __init__(
        self,
        store: SQLiteSessionStore | None = None,
        event_bus: EventBus | None = None,
        process_manager: ProcessManager | None = None,
    ) -> None:
        self.store = store or SQLiteSessionStore()
        self.event_bus = event_bus or EventBus()
        self.process_manager = process_manager or ProcessManager()

        self.wizard_engine = WizardEngine(store=self.store)
        self.workflow_registry = WorkflowRegistry()

        # Emit a startup event
        self.event_bus.publish_named("orchestrator.started", {})

    def register_wizard(self, definition: Any) -> None:
        """Convenience passthrough."""
        self.wizard_engine.register(definition)

    def start_wizard_session(self, wizard_id: str, **kwargs: Any) -> tuple[Any, Any]:
        session, ctx = self.wizard_engine.start_session(wizard_id, **kwargs)
        self.event_bus.publish_named(
            "wizard.session.started",
            {"session_id": session.id, "wizard_id": wizard_id},
        )
        return session, ctx

    def shutdown(self) -> None:
        self.process_manager.shutdown_all()
        self.event_bus.publish_named("orchestrator.shutdown", {})
