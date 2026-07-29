"""
Execution runtimes — surfaces that host Palm engines.

Use ``palm.runtimes.cli:main`` as the CLI entry point. Library code should
import concrete runtimes from their subpackages (``embedded``, ``daemon``, ``server``).
System instance and ports live in ``palm.system``. Shared server transport
lives in the exposed kit :mod:`palm.kits.server`.
"""

from palm.system.runtime.base import BaseRuntime
from palm.system.runtime.host import RuntimeHost
from palm.system.runtime.hooks import (
    AuthMiddleware,
    DriveObservabilityHook,
    DriveSlice,
)
from palm.runtimes.daemon import DaemonRuntime, run_daemon
from palm.runtimes.embedded import EmbeddedRuntime
from palm.runtimes.server import ServerRuntime, run_server

__all__ = [
    "AuthMiddleware",
    "BaseRuntime",
    "DaemonRuntime",
    "DriveObservabilityHook",
    "DriveSlice",
    "EmbeddedRuntime",
    "RuntimeHost",
    "ServerRuntime",
    "run_daemon",
    "run_server",
]
