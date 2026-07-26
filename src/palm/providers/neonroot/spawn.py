"""NeonRoot ``spawn`` action — hermetic command run (0.53.2).

Maps to::

    neonroot spawn [name] --image <img> [--vault …] [--sandbox] [--isolated]
        [--seed <dir>] -- <command…>

``seed`` policy (ADR-022):

- ``git-archive`` (default for hermetic claims) — ``git archive HEAD`` into a
  temp directory, seed that path, delete after spawn.
- absolute/relative path — seed that host directory; **explicit** non-hermetic
  workspace seed (dirty tree possible).
- omit / empty with ``seed_mode: none`` — no ``--seed`` flag.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from palm.providers.neonroot.cli import find_neonroot_binary, probe_neonroot

# Captured stream tails — enough for doctor / Assist, not full log dumps.
_DEFAULT_TAIL = 8000
_DEFAULT_TIMEOUT = 3600.0


@dataclass(frozen=True)
class SpawnRequest:
    """Validated spawn parameters."""

    image: str
    command: tuple[str, ...]
    vault: str | None = None
    name: str | None = None
    seed: str = "git-archive"
    sandbox: bool = True
    isolated: bool = False
    keep: bool = False
    timeout: float = _DEFAULT_TIMEOUT
    cwd: str | None = None  # git-archive root; default: process cwd / repo


def _as_str_list(value: Any, *, field: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        # Allow shell-ish single string only if non-empty; prefer argv lists.
        parts = value.strip().split()
        if not parts:
            raise ValueError(f"{field} must be a non-empty command list or string")
        return parts
    if isinstance(value, list | tuple):
        out = [str(x) for x in value]
        if not out:
            raise ValueError(f"{field} must be a non-empty list")
        return out
    raise ValueError(f"{field} must be a list of strings (got {type(value).__name__})")


def parse_spawn_params(params: dict[str, Any]) -> SpawnRequest:
    """Build a :class:`SpawnRequest` from provider invoke params."""
    image = params.get("image")
    if not image or not str(image).strip():
        raise ValueError("spawn requires params.image (NeonRoot image name)")

    command = _as_str_list(params.get("command"), field="command")
    vault = params.get("vault")
    name = params.get("name")
    seed = params.get("seed", "git-archive")
    if seed is None:
        seed = "git-archive"
    seed = str(seed)

    sandbox = bool(params.get("sandbox", True))
    isolated = bool(params.get("isolated", False))
    keep = bool(params.get("keep", False))
    timeout = float(params.get("timeout", _DEFAULT_TIMEOUT))
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    cwd = params.get("cwd") or params.get("repo_root")
    return SpawnRequest(
        image=str(image).strip(),
        command=tuple(command),
        vault=str(vault).strip() if vault else None,
        name=str(name).strip() if name else None,
        seed=seed,
        sandbox=sandbox,
        isolated=isolated,
        keep=keep,
        timeout=timeout,
        cwd=str(cwd) if cwd else None,
    )


def _tail(text: str, limit: int = _DEFAULT_TAIL) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _prepare_seed(
    seed: str,
    *,
    repo_root: Path,
) -> tuple[str | None, Path | None]:
    """Return (seed_path_for_cli, temp_dir_to_cleanup)."""
    if seed in ("", "none", "false", "no"):
        return None, None
    if seed == "git-archive":
        tmp = Path(tempfile.mkdtemp(prefix="palm-neonroot-seed-"))
        try:
            proc = subprocess.run(
                ["git", "archive", "HEAD"],
                cwd=repo_root,
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace")
                shutil.rmtree(tmp, ignore_errors=True)
                raise RuntimeError(f"git archive HEAD failed: {err.strip() or proc.returncode}")
            subprocess.run(
                ["tar", "-x", "-C", str(tmp)],
                input=proc.stdout,
                check=True,
            )
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        return str(tmp), tmp

    path = Path(seed).expanduser()
    if not path.is_absolute():
        path = (repo_root / path).resolve()
    else:
        path = path.resolve()
    if not path.is_dir():
        raise ValueError(f"seed path is not a directory: {path}")
    return str(path), None


def build_spawn_argv(
    neonroot_bin: str,
    req: SpawnRequest,
    *,
    seed_path: str | None,
) -> list[str]:
    """Construct the ``neonroot spawn …`` argv (no shell)."""
    argv: list[str] = [neonroot_bin, "spawn"]
    if req.name:
        argv.append(req.name)
    argv.extend(["--image", req.image])
    if req.vault:
        argv.extend(["--vault", req.vault])
    if req.isolated:
        argv.append("--isolated")
    elif req.sandbox:
        argv.append("--sandbox")
    if req.keep:
        argv.append("--keep")
    if seed_path:
        argv.extend(["--seed", seed_path])
    argv.append("--")
    argv.extend(req.command)
    return argv


def run_spawn(
    params: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Execute spawn; return a serializable result dict (success via exit_code)."""
    probe = probe_neonroot()
    if not probe.available or not probe.path:
        raise RuntimeError(probe.error or "neonroot not available")

    req = parse_spawn_params(params)
    root = Path(req.cwd) if req.cwd else (repo_root or Path.cwd())
    root = root.resolve()

    seed_path, cleanup = _prepare_seed(req.seed, repo_root=root)
    argv = build_spawn_argv(probe.path, req, seed_path=seed_path)
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=req.timeout,
            check=False,
            cwd=str(root),
        )
        duration = time.monotonic() - started
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        return {
            "exit_code": proc.returncode,
            "duration_s": round(duration, 3),
            "argv": argv,
            "image": req.image,
            "vault": req.vault,
            "seed": req.seed,
            "seed_path": seed_path,
            "sandbox": req.sandbox,
            "isolated": req.isolated,
            "command": list(req.command),
            "stdout_tail": _tail(stdout),
            "stderr_tail": _tail(stderr),
            "neonroot": probe.as_dict(),
        }
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        return {
            "exit_code": None,
            "timed_out": True,
            "duration_s": round(duration, 3),
            "argv": argv,
            "image": req.image,
            "vault": req.vault,
            "seed": req.seed,
            "seed_path": seed_path,
            "command": list(req.command),
            "stdout_tail": _tail(stdout),
            "stderr_tail": _tail(stderr or f"timeout after {req.timeout}s"),
            "neonroot": probe.as_dict(),
            "error": f"spawn timed out after {req.timeout}s",
        }
    finally:
        if cleanup is not None:
            shutil.rmtree(cleanup, ignore_errors=True)


def resolve_repo_root() -> Path:
    """Best-effort package / checkout root (for git-archive)."""
    # providers/neonroot/spawn.py → parents[3] = src, [4] = repo if src layout
    here = Path(__file__).resolve()
    # …/src/palm/providers/neonroot/spawn.py → repo root is parents[4]
    candidate = here.parents[4]
    if (candidate / "pyproject.toml").is_file():
        return candidate
    # editable / odd layouts
    binary = find_neonroot_binary()
    _ = binary
    return Path.cwd()


__all__ = [
    "SpawnRequest",
    "build_spawn_argv",
    "parse_spawn_params",
    "resolve_repo_root",
    "run_spawn",
]
