"""Hermetic job resource contract (0.54.1) — definition-facing params for neonroot jobs.

Palm definitions express work as **resource nodes**. When the node needs isolation
or a foreign toolchain, the provider is ``neonroot`` and the action is ``spawn``
(or ``health`` for preflight). Palm does **not** import/run arbitrary project
Python; the **command** runs inside a NeonRoot image (tmpfs workspace).

This module documents and validates the param shape used by
:mod:`palm.providers.neonroot.spawn`. It is the portable contract for flows,
DAG nodes (later), and examples.

Canonical spawn params
----------------------
``image`` (str, required)
    NeonRoot image name (e.g. ``palm-ci``, ``palm-docs``).

``command`` (list[str], required)
    Argv for the job inside the workspace (no shell).

``seed`` (str, default ``git-archive``)
    ``git-archive`` | host path | ``none``.

``seed_exclude`` (list[str], optional)
    Paths/globs skipped while seeding (also ``.neonrootignore`` on seed root).

``outputs`` (list, optional)
    After **successful** exit only: ``host:container`` or
    ``{host, container}`` maps (container path relative, no ``..``).

``vault`` (str, optional)
    NeonRoot vault name.

``sandbox`` (bool, default True) / ``isolated`` (bool, default False)
    Isolation flags (isolated implies no network).

``timeout`` (float, optional)
    Seconds; default 3600.

``name`` (str, optional)
    Workspace name for the spawn.

``cwd`` / ``repo_root`` (str, optional)
    Root for ``git-archive`` and relative seed paths.

Health (preflight)
------------------
Action ``health`` takes no job params; reports CLI availability.

See ADR-022, ADR-023 (hermetic jobs), VISION-0.54.
"""

from __future__ import annotations

from typing import Any

from palm.providers.neonroot.spawn import SpawnRequest, parse_spawn_params

# Documented field set for agents and schema docs (not a JSON Schema engine).
HERMETIC_JOB_SPAWN_FIELDS: frozenset[str] = frozenset(
    {
        "image",
        "command",
        "seed",
        "seed_exclude",
        "seed_excludes",
        "outputs",
        "output",
        "vault",
        "sandbox",
        "isolated",
        "keep",
        "timeout",
        "name",
        "cwd",
        "repo_root",
    }
)


def validate_hermetic_job_params(params: dict[str, Any] | None) -> SpawnRequest:
    """Validate neonroot ``spawn`` params; return a :class:`SpawnRequest`.

    Raises
    ------
    ValueError
        Missing image/command or invalid seed/outputs.
    """
    return parse_spawn_params(dict(params or {}))


def hermetic_job_summary(req: SpawnRequest) -> dict[str, Any]:
    """Stable summary dict for job state / Assist (no secrets)."""
    return {
        "kind": "hermetic_job",
        "provider": "neonroot",
        "action": "spawn",
        "image": req.image,
        "command": list(req.command),
        "seed": req.seed,
        "seed_exclude": list(req.seed_exclude),
        "outputs": list(req.outputs),
        "vault": req.vault,
        "sandbox": req.sandbox,
        "isolated": req.isolated,
        "timeout": req.timeout,
    }


__all__ = [
    "HERMETIC_JOB_SPAWN_FIELDS",
    "hermetic_job_summary",
    "validate_hermetic_job_params",
]
