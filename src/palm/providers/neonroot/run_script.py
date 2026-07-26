"""Hermetic run_script — stage code, spawn NeonRoot, return result (Assist run-code).

Does **not** exec code inside Palm. Stages a run dir and invokes NeonRoot
``spawn`` (tmpfs or bind). See VISION-0.54 horizon / HERMETIC-JOBS.
"""

from __future__ import annotations

from typing import Any

from palm.providers.neonroot.run_dir import (
    create_run_dir,
    remove_run_dir,
    write_payload_file,
)
from palm.providers.neonroot.spawn import resolve_repo_root, run_spawn

# Security: only these images by default (override via params.allowed_images).
DEFAULT_ALLOWED_IMAGES: tuple[str, ...] = ("palm-ci", "palm-docs")

# palm-ci / palm-docs ship ``uv`` + UV_PYTHON (no system python on PATH).
_LANG_FILES = {
    "python": (
        "main.py",
        ["uv", "run", "--no-project", "python", "payload/main.py"],
    ),
}


def run_script_job(params: dict[str, Any]) -> dict[str, Any]:
    """Stage ``code`` and run it under ``image`` via neonroot spawn.

    Required params
    ---------------
    code : str
    image : str

    Optional
    --------
    language : str = \"python\"
    vault : str = image
    seed_mode : copy | bind (default bind so payload is visible; code is staged)
    data_dir : str — parent for hermetic runs
    allowed_images : list[str]
    keep_run_dir : bool — if True, do not GC after run
    timeout, sandbox, isolated — passed to spawn
    """
    code = params.get("code")
    if code is None or not str(code).strip():
        raise ValueError("run_script requires non-empty params.code")
    code_s = str(code)
    if len(code_s.encode("utf-8")) > int(params.get("max_code_bytes") or 256_000):
        raise ValueError("run_script code exceeds max_code_bytes")

    image = str(params.get("image") or "").strip()
    if not image:
        raise ValueError("run_script requires params.image")

    allowed = params.get("allowed_images")
    if allowed is None:
        allowed_set = set(DEFAULT_ALLOWED_IMAGES)
    elif isinstance(allowed, list | tuple):
        allowed_set = {str(x).strip() for x in allowed if str(x).strip()}
    else:
        raise ValueError("allowed_images must be a list of image names")
    if image not in allowed_set:
        raise ValueError(
            f"image {image!r} not in allowlist {sorted(allowed_set)}; "
            "pass allowed_images to extend (security policy)"
        )

    language = str(params.get("language") or "python").strip().lower()
    if language not in _LANG_FILES:
        raise ValueError(
            f"unsupported language {language!r}; supported: {sorted(_LANG_FILES)}"
        )
    filename, default_cmd = _LANG_FILES[language]

    data_dir = params.get("data_dir")
    if data_dir is None:
        # Prefer host data_dir next to repo if present
        root = resolve_repo_root()
        candidate = root / "data"
        data_dir = candidate if candidate.is_dir() else root / "data"

    run = create_run_dir(
        data_dir=data_dir,
        meta={
            "purpose": "run_script",
            "image": image,
            "language": language,
        },
    )
    write_payload_file(run, filename, code_s)

    seed_mode = str(params.get("seed_mode") or "bind").strip().lower()
    if seed_mode not in ("copy", "bind"):
        raise ValueError("seed_mode must be copy or bind")

    command = params.get("command")
    if command is None:
        cmd = list(default_cmd)
    elif isinstance(command, list | tuple):
        cmd = [str(c) for c in command]
    else:
        raise ValueError("command must be a list of strings if provided")

    spawn_params: dict[str, Any] = {
        "image": image,
        "command": cmd,
        "seed": str(run.root.resolve()),
        "seed_mode": seed_mode,
        "sandbox": bool(params.get("sandbox", True)),
        "isolated": bool(params.get("isolated", False)),
        "timeout": float(params.get("timeout") or 120),
    }
    vault = params.get("vault")
    if vault:
        spawn_params["vault"] = str(vault)
    else:
        spawn_params["vault"] = image

    keep = bool(params.get("keep_run_dir", False))
    try:
        payload = run_spawn(spawn_params, repo_root=resolve_repo_root())
    finally:
        if not keep:
            remove_run_dir(run, missing_ok=True)

    payload = dict(payload)
    payload["run_id"] = run.run_id
    payload["language"] = language
    payload["image"] = image
    payload["entrypoint"] = cmd
    # Flat memory keys for wizard state / Assist display (alias tails).
    payload["stdout"] = str(payload.get("stdout_tail") or "")
    payload["stderr"] = str(payload.get("stderr_tail") or "")
    # Do not echo full source by default (size / logs); optional flag later
    return payload


__all__ = ["DEFAULT_ALLOWED_IMAGES", "run_script_job"]
