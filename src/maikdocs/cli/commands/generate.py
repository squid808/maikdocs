"""Generate command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from maikdocs.core.config import MaikDocsConfig
from maikdocs.core.orchestrator import BuildOrchestrator

console = Console()


def generate_command(
    target: Path | None = None,
    recursive: bool = True,
    force: bool = False,
    whatif: bool = False,
) -> None:
    """Generate documentation from scratch.

    Args:
        target: Target file, directory, or leave empty for entire project
        recursive: Process directories recursively
        force: Regenerate all documentation regardless of timestamps
        whatif: Show what would happen without making changes
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
        task = progress.add_task("Generating documentation...", total=None)

        result = orchestrator.generate_all(
            target=target,
            recursive=recursive,
            force=force,
        )

        progress.update(task, completed=True)

    console.print(f"\n[green]✓ Documentation generation complete[/green]\n")

    console.print(f"[cyan]Generated:[/cyan]")
    console.print(f"  - {len(result.files_generated)} file documentation files")
    console.print(f"  - {len(result.indexes_generated)} directory indexes")

    if result.files_skipped:
        console.print(f"\n[yellow]Skipped (up to date):[/yellow]")
        console.print(f"  - {len(result.files_skipped)} files")

    if result.errors:
        console.print(f"\n[red]Errors:[/red]")
        for path, error in result.errors[:5]:
            console.print(f"  - {path}: {error}")
        if len(result.errors) > 5:
            console.print(f"  ... and {len(result.errors) - 5} more errors")

    output_dir = config.project_root / config.output_folder
    console.print(f"\n[dim]Documentation saved to {output_dir}[/dim]")


def _load_config() -> MaikDocsConfig:
    """Load configuration from current directory.

    Returns:
        Loaded configuration

    Raises:
        typer.Exit: If configuration not found
    """
    config_path = Path.cwd() / ".maikdocs.yaml"

    parent = Path.cwd().parent
    while not config_path.exists() and parent != parent.parent:
        config_path = parent / ".maikdocs.yaml"
        parent = parent.parent

    if not config_path.exists():
        console.print("[red]No configuration found. Run 'maikdocs init' first.[/red]")
        raise typer.Exit(1)

    try:
        return MaikDocsConfig.load(config_path)
    except Exception as e:
        console.print(f"[red]Failed to load configuration: {e}[/red]")
        raise typer.Exit(1)
