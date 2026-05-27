"""
Interactive REPL for Palm Solid Admin CLI.

Built with prompt_toolkit for excellent UX (history, completion, multiline).
Uses Rich for beautiful output.
"""

from __future__ import annotations

import shlex
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from palm.config.settings import settings
from palm.core.orchestrator import Orchestrator
from palm.core.wizard.engine import WizardEngine
from palm.exceptions import PalmError


class PalmCommandCompleter(Completer):
    """Basic command completion."""

    COMMANDS = [
        "help",
        "wizard list",
        "wizard start",
        "wizard status",
        "wizard input",
        "back",
        "ps",
        "sessions",
        "clear",
        "exit",
        "quit",
    ]

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower()
        for cmd in self.COMMANDS:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))


class PalmREPL:
    """Main REPL loop."""

    def __init__(
        self,
        orchestrator: Orchestrator,
        engine: WizardEngine,
        console: Console,
    ) -> None:
        self.orchestrator = orchestrator
        self.engine = engine
        self.console = console

        self.session: PromptSession[str] = PromptSession(
            history=FileHistory(str(settings.resolved_history_file)),
            completer=PalmCommandCompleter(),
            style=Style.from_dict(
                {
                    "prompt": "ansicyan bold",
                }
            ),
            multiline=False,
        )

        self.active_session_id: str | None = None  # convenience for quick input

        self.commands: dict[str, Any] = {
            "help": self.cmd_help,
            "wizard list": self.cmd_wizard_list,
            "wizard start": self.cmd_wizard_start,
            "wizard status": self.cmd_wizard_status,
            "wizard input": self.cmd_wizard_input,
            "back": self.cmd_back,
            "ps": self.cmd_ps,
            "sessions": self.cmd_sessions,
            "clear": self.cmd_clear,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
        }

    def run(self) -> None:
        while True:
            try:
                text = self.session.prompt(self._get_prompt())
                if not text.strip():
                    continue
                self._dispatch(text.strip())
            except EOFError:
                self.console.print("\n[dim]Goodbye.[/]")
                break
            except KeyboardInterrupt:
                self.console.print("^C")
                continue
            except PalmError as e:
                self.console.print(f"[red]Error:[/] {e}")
            except Exception as e:
                self.console.print(f"[red bold]Unexpected error:[/] {e}")

    def _get_prompt(self) -> str:
        if self.active_session_id:
            short = self.active_session_id[:8]
            return f"[palm:{short}]> "
        return settings.cli_prompt

    def _dispatch(self, line: str) -> None:
        parts = shlex.split(line)
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        # Two-word commands
        if len(parts) >= 2:
            two_word = f"{parts[0]} {parts[1]}"
            if two_word in self.commands:
                self.commands[two_word](args[1:] if len(args) > 1 else [])
                return

        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            self.console.print(f"[yellow]Unknown command:[/] {cmd}. Type [bold]help[/].")

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def cmd_help(self, args: list[str]) -> None:
        help_text = """
[bold cyan]Palm Solid Admin CLI Commands[/]

[bold]Wizard Management[/]
  wizard list                     List all registered wizards
  wizard start <wizard_id>        Start a new wizard session
  wizard status [session_id]      Show status (uses active if omitted)
  wizard input <session_id> <val> Submit input to a session

[bold]Session Control[/]
  back <session_id> <step_slug>   Backtrack a session to a previous step
  sessions                        List active/persisted sessions

[bold]System[/]
  ps                              Show running processes (ProcessManager)
  clear                           Clear the screen
  help                            This message
  exit / quit                     Leave the REPL

[bold]Tips[/]
  • After starting a wizard, the session ID becomes "active".
  • You can then use short forms in many contexts (future enhancement).
  • Use Tab for command completion.
"""
        self.console.print(Panel(help_text.strip(), title="Help", border_style="cyan"))

    def cmd_wizard_list(self, args: list[str]) -> None:
        wizards = self.engine.list_wizards()
        if not wizards:
            self.console.print("[yellow]No wizards registered.[/]")
            return

        table = Table(title="Registered Wizards", show_lines=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Version", style="dim")
        table.add_column("Steps", justify="right")
        table.add_column("Description", style="white")

        for w in wizards:
            table.add_row(
                w["id"],
                w["name"],
                w["version"],
                str(w["step_count"]),
                w["description"][:60] + ("..." if len(w["description"]) > 60 else ""),
            )
        self.console.print(table)

    def cmd_wizard_start(self, args: list[str]) -> None:
        if not args:
            self.console.print("[red]Usage:[/] wizard start <wizard_id>")
            return

        wizard_id = args[0]
        try:
            session, ctx = self.engine.start_session(wizard_id)
            self.active_session_id = session.id
            self._render_context(ctx)
            self.console.print(f"\n[dim]Session ID:[/] [bold]{session.id}[/] (now active)")
        except PalmError as e:
            self.console.print(f"[red]Failed to start wizard:[/] {e}")

    def cmd_wizard_status(self, args: list[str]) -> None:
        sid = args[0] if args else self.active_session_id
        if not sid:
            self.console.print("[red]No session id provided and no active session.[/]")
            return
        try:
            status = self.engine.get_status(sid)
            table = Table(title=f"Session {sid[:12]}...", show_header=False)
            for k, v in status.items():
                table.add_row(f"[bold]{k}[/]", str(v))
            self.console.print(table)
        except PalmError as e:
            self.console.print(f"[red]{e}[/]")

    def cmd_wizard_input(self, args: list[str]) -> None:
        if len(args) < 2:
            self.console.print("[red]Usage:[/] wizard input <session_id> <value>")
            return

        sid = args[0]
        # Join the rest in case value contains spaces
        value = " ".join(args[1:])

        try:
            ctx = self.engine.process_input(sid, value)
            self._render_context(ctx)
            if ctx.status.value == "committed":
                self.active_session_id = None
        except PalmError as e:
            self.console.print(f"[red]Input error:[/] {e}")
            # Re-show last context if possible
            try:
                status = self.engine.get_status(sid)
                self.console.print(f"[dim]Current step: {status.get('current_step')}[/]")
            except Exception:
                pass

    def cmd_back(self, args: list[str]) -> None:
        if len(args) < 2:
            self.console.print("[red]Usage:[/] back <session_id> <step_slug>")
            return

        sid, target = args[0], args[1]
        try:
            ctx = self.engine.backtrack(sid, target)
            self._render_context(ctx)
            self.console.print(f"[green]Backtracked to[/] [bold]{target}[/]")
        except PalmError as e:
            self.console.print(f"[red]{e}[/]")

    def cmd_ps(self, args: list[str]) -> None:
        procs = self.orchestrator.process_manager.list()
        if not procs:
            self.console.print("[dim]No managed processes currently running.[/]")
            return
        table = Table(title="Managed Processes")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("OS PID")
        table.add_column("Alive")
        table.add_column("Status")
        for p in procs:
            table.add_row(
                p["id"][:20],
                p["name"],
                str(p["os_pid"]),
                "✓" if p["alive"] else "✗",
                p["status"],
            )
        self.console.print(table)

    def cmd_sessions(self, args: list[str]) -> None:
        sessions = self.orchestrator.store.list_active()
        if not sessions:
            self.console.print("[dim]No active sessions.[/]")
            return

        table = Table(title="Active Sessions")
        table.add_column("ID", style="cyan")
        table.add_column("Wizard")
        table.add_column("Status", style="yellow")
        table.add_column("Step")
        table.add_column("Last Activity")

        for s in sessions:
            table.add_row(
                s.id[:12],
                s.wizard_id,
                s.status.value,
                s.current_step_slug or "-",
                s.last_activity_at.strftime("%H:%M:%S"),
            )
        self.console.print(table)

    def cmd_clear(self, args: list[str]) -> None:
        self.console.clear()

    def cmd_exit(self, args: list[str]) -> None:
        self.console.print("[dim]Shutting down...[/]")
        self.orchestrator.shutdown()
        raise EOFError()

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _render_context(self, ctx: Any) -> None:
        """Beautifully render a RichContext using Rich panels."""
        title = f"[bold]{ctx.wizard_name}[/] — [cyan]{ctx.current_step_slug}[/] ({ctx.current_step_type})"

        body = f"[bold]{ctx.prompt}[/]\n"
        if ctx.guidelines:
            body += f"\n[dim]{ctx.guidelines}[/]\n"

        if ctx.choices:
            body += "\n[bold]Choices:[/]\n"
            for c in ctx.choices:
                val = c.get("value", c)
                label = c.get("label", val)
                body += f"  • [green]{val}[/]: {label}\n"

        if ctx.allowed_back_steps:
            body += f"\n[dim]Back: {' | '.join(ctx.allowed_back_steps)}[/]"

        if ctx.collected_data:
            body += "\n\n[dim]Collected so far:[/]\n"
            for k, v in list(ctx.collected_data.items())[:6]:
                if not k.startswith("__"):
                    body += f"  {k}: [white]{v}[/]\n"

        panel = Panel(
            body.strip(),
            title=title,
            border_style="blue",
            subtitle=f"Session: {ctx.session_id[:8]}  |  Status: {ctx.status}",
        )
        self.console.print(panel)

        if ctx.status.value == "committed":
            self.console.print(
                Panel(
                    f"[bold green]✓ Wizard completed successfully![/]\n\n"
                    f"Result: {ctx.metadata.get('commit_result', {})}",
                    border_style="green",
                )
            )
