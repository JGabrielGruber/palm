"""
Entry point for the Palm Solid Admin CLI.

Usage:
    palm
    python -m palm.cli.solid
    python main.py
"""

from __future__ import annotations

import sys

from rich.console import Console

from palm.cli.solid.repl import PalmREPL
from palm.core.orchestrator import Orchestrator
from palm.core.wizard.engine import WizardEngine


def main() -> None:
    console = Console()

    console.print("[bold green]🌴 Palm Orchestration Engine[/] - Solid Admin CLI")
    console.print("Type [bold]help[/] for available commands. [dim]Ctrl+D or 'exit' to quit.[/]\n")

    # Create a fresh orchestrator + engine for this CLI session
    orchestrator = Orchestrator()
    engine: WizardEngine = orchestrator.wizard_engine

    # Auto-register any wizards found in the wizards/ package (best effort)
    _auto_register_example_wizards(engine, console)

    repl = PalmREPL(orchestrator=orchestrator, engine=engine, console=console)
    try:
        repl.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Goodbye.[/]")
        sys.exit(0)


def _auto_register_example_wizards(engine: WizardEngine, console: Console) -> None:
    """Try to load the built-in example wizard(s)."""
    try:
        from wizards.examples.create_ape_profile import create_ape_profile_wizard

        engine.register(create_ape_profile_wizard())
        console.print("[dim]Loaded example wizard: create_ape_profile[/]")
    except Exception as exc:
        console.print(f"[dim yellow]Could not auto-load example wizards: {exc}[/]")


if __name__ == "__main__":
    main()
