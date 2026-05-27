"""
Workflow subsystem (non-interactive DAG execution).

Currently lightweight scaffolding. Future home of pure DAG workflows
that do not require interactive pauses.
"""

from palm.core.workflow.dag import DAG, Node
from palm.core.workflow.executor import WorkflowExecutor
from palm.core.workflow.registry import WorkflowRegistry

__all__ = ["DAG", "Node", "WorkflowExecutor", "WorkflowRegistry"]
