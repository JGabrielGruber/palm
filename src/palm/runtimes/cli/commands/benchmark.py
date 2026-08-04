"""
CLI present for vitality benchmark (0.61.11).

Law: thrash + metrics live in ``palm.system.vitality``; product door is
``InspectService.benchmark``; this module only parses args and renders.
"""

from __future__ import annotations

from typing import Any

from palm.runtimes.cli.shared.context import CliContext
from palm.runtimes.cli.shared.output import emit_json
from palm.system.vitality import (
    DEFAULT_ITERATIONS,
    DEFAULT_RECIPE,
    KNOWN_RECIPES,
)


def _parse_args(args: list[str]) -> dict[str, Any]:
    recipe = DEFAULT_RECIPE
    iterations = DEFAULT_ITERATIONS
    store_full = False
    as_json = False
    i = 0
    while i < len(args):
        tok = args[i]
        if tok in {"--recipe", "-r"} and i + 1 < len(args):
            recipe = str(args[i + 1]).strip().lower()
            i += 2
            continue
        if tok in {"-n", "--iterations"} and i + 1 < len(args):
            try:
                iterations = int(args[i + 1])
            except ValueError:
                iterations = DEFAULT_ITERATIONS
            i += 2
            continue
        if tok in {"--full", "--store-full"}:
            store_full = True
            i += 1
            continue
        if tok == "--format" and i + 1 < len(args):
            as_json = str(args[i + 1]).strip().lower() == "json"
            i += 2
            continue
        if tok == "--json":
            as_json = True
            i += 1
            continue
        if tok in {"--help", "-h"}:
            return {"help": True}
        # bare recipe name: ``benchmark pulse``
        if not tok.startswith("-") and tok.lower() in KNOWN_RECIPES:
            recipe = tok.lower()
            i += 1
            continue
        i += 1
    return {
        "recipe": recipe,
        "iterations": iterations,
        "store_full": store_full,
        "as_json": as_json,
    }


def cmd_benchmark(ctx: CliContext, args: list[str]) -> int:
    """Run vitality benchmark via host.inspect and present results."""
    opts = _parse_args(args)
    if opts.get("help"):
        ctx.console.print(
            "[bold]benchmark[/] — vitality load tool (opt-in; Inspect present)\n"
            "  benchmark [--recipe pulse|idle|walk|log_fill] [-n N] [--json] [--full]\n"
            "  benchmark pulse -n 50\n"
            "[dim]Does not run on everyday status/doctor. System tool via product door.[/]"
        )
        return 0

    if ctx.output_format == "json":
        opts["as_json"] = True

    inspect = getattr(ctx.host, "inspect", None)
    if inspect is None:
        ctx.console.print("[red]host.inspect not available[/]")
        return 1
    try:
        runtime = ctx.host.runtime()
    except Exception as exc:
        ctx.console.print(f"[red]runtime not ready:[/] {exc}")
        return 1

    recipe = str(opts.get("recipe") or DEFAULT_RECIPE)
    iterations = int(opts.get("iterations") or DEFAULT_ITERATIONS)
    store_full = bool(opts.get("store_full"))

    try:
        report = inspect.benchmark(
            runtime,
            recipe=recipe,
            iterations=iterations,
            store_full_snapshots=store_full,
        )
    except Exception as exc:
        ctx.console.print(f"[red]benchmark failed:[/] {exc}")
        return 1

    if opts.get("as_json"):
        emit_json(ctx.console, report)
        return 0 if report.get("state") == "ok" else 1

    return _render_human(ctx, report)


def _render_human(ctx: CliContext, report: dict[str, Any]) -> int:
    from rich.panel import Panel
    from rich.table import Table

    state = report.get("state")
    border = "green" if state == "ok" else "red"
    summary = report.get("summary") or {}
    timing = report.get("timing") or {}
    recipe_meta = report.get("recipe_meta") or {}

    header = (
        f"[bold]recipe[/] {report.get('recipe')!r}  "
        f"[bold]n[/] {report.get('iterations')}  "
        f"[bold]state[/] {state}\n"
        f"ops={recipe_meta.get('ops')}  "
        f"path={recipe_meta.get('path') or recipe_meta.get('kind') or '—'}  "
        f"recipe_ms={timing.get('recipe_ms')}  "
        f"total_ms={timing.get('total_ms')}\n"
        f"[dim]source={report.get('source')}  "
        f"kind={report.get('kind')}  "
        f"capability={report.get('capability_id')}[/]"
    )
    notes = report.get("notes") or []
    if notes:
        header += "\n[dim]" + " · ".join(str(n) for n in notes) + "[/]"

    ctx.console.print(
        Panel(header, title="Vitality benchmark", border_style=border)
    )

    diff = report.get("diff") or {}
    table = Table(title="Load point deltas", show_lines=False)
    table.add_column("metric", style="cyan")
    table.add_column("before", justify="right")
    table.add_column("after", justify="right")
    table.add_column("delta", justify="right")

    # Prefer numeric deltas first; skip pure labels.
    rows: list[tuple[str, Any, Any, Any]] = []
    for key, cell in sorted(diff.items()):
        if not isinstance(cell, dict):
            continue
        if key in {"sample_ts", "rss_kind"}:
            continue
        rows.append(
            (
                key,
                cell.get("before"),
                cell.get("after"),
                cell.get("delta"),
            )
        )
    # Highlight non-zero deltas first.
    rows.sort(
        key=lambda r: (
            0 if r[3] not in (None, 0, 0.0) else 1,
            str(r[0]),
        )
    )
    for key, before, after, delta in rows:
        delta_s = "—" if delta is None else str(delta)
        style = ""
        if isinstance(delta, (int, float)) and delta != 0:
            style = "bold yellow"
        table.add_row(
            key,
            _fmt(before),
            _fmt(after),
            f"[{style}]{delta_s}[/]" if style else delta_s,
        )
    ctx.console.print(table)

    deltas = summary.get("deltas") or {}
    moved = {k: v for k, v in deltas.items() if v not in (None, 0, 0.0)}
    if moved:
        ctx.console.print(
            Panel(
                "\n".join(f"{k}: {v}" for k, v in sorted(moved.items())),
                title="Non-zero deltas",
                border_style="yellow",
            )
        )
    else:
        ctx.console.print(
            "[dim]No non-zero load deltas (control/noise or peak RSS flat).[/]"
        )

    ctx.console.print(
        "[dim]Tip:[/] [cyan]benchmark log_fill -n 25[/] · "
        "[cyan]benchmark --json[/] · recipes: "
        + ", ".join(sorted(KNOWN_RECIPES))
    )
    return 0 if state == "ok" else 1


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


__all__ = ["cmd_benchmark"]
