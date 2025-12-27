"""Update command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from maikdocs.cli.commands.generate import _load_config
from maikdocs.core.orchestrator import BuildOrchestrator

console = Console()


def update_command(
    target: Path | None = None,
    keep_orphaned: bool | None = None,
    whatif: bool = False,
) -> None:
    """Incrementally update documentation based on file changes.

    Args:
        target: Target file, directory, or leave empty for entire project
        keep_orphaned: Preserve or remove orphaned documentation files
        whatif: Show what would be updated without making changes
    """
    config = _load_config()

    if whatif:
        console.print("[yellow]Running in --whatif mode (no changes will be made)[/yellow]\n")

    orchestrator = BuildOrchestrator(config)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Checking for changes...", total=None)

        result = orchestrator.update_incremental(
            target=target,
            preserve_orphaned=keep_orphaned,
        )

        progress.update(task, completed=True)

    console.print(f"\n[green]✓ Documentation update complete[/green]\n")

    if result.files_generated:
        console.print(f"[cyan]Updated:[/cyan]")
        console.print(f"  - {len(result.files_generated)} file documentation files")

    if result.indexes_generated:
        console.print(f"  - {len(result.indexes_generated)} directory indexes")

    if result.files_removed:
        console.print(f"\n[yellow]Removed (orphaned):[/yellow]")
        console.print(f"  - {len(result.files_removed)} files")

    if result.files_skipped:
        console.print(f"\n[dim]Skipped (up to date): {len(result.files_skipped)} files[/dim]")

    if not result.files_generated and not result.files_removed and not result.indexes_generated:
        console.print("[cyan]No changes detected - all documentation is up to date[/cyan]")

    if result.errors:
        console.print(f"\n[red]Errors:[/red]")
        for path, error in result.errors[:5]:
            console.print(f"  - {path}: {error}")
        if len(result.errors) > 5:
            console.print(f"  ... and {len(result.errors) - 5} more errors")
