"""Init command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from maikdocs.core.config import MaikDocsConfig

console = Console()


def init_command(
    directory: Path | None = None,
    languages: list[str] | None = None,
    output_folder: str = ".maik",
    force: bool = False,
) -> None:
    """Initialize maikdocs in a project directory.

    Args:
        directory: Project root directory (defaults to current directory)
        languages: Languages to support
        output_folder: Output folder for documentation
        force: Overwrite existing configuration
    """
    project_root = directory if directory else Path.cwd()

    if not project_root.exists():
        console.print(f"[red]Directory does not exist: {project_root}[/red]")
        raise typer.Exit(1)

    config_path = project_root / ".maikdocs.yaml"

    if config_path.exists() and not force:
        console.print(f"[yellow]Configuration already exists at {config_path}[/yellow]")
        console.print("Use --force to overwrite")
        raise typer.Exit(1)

    detected_root = _detect_project_root(project_root)
    if detected_root != project_root:
        console.print(f"[cyan]Detected project root: {detected_root}[/cyan]")
        if not Confirm.ask("Use this directory?", default=True):
            new_root = Prompt.ask("Enter project root", default=str(project_root))
            project_root = Path(new_root)

    if languages is None:
        console.print("\n[cyan]Available languages:[/cyan]")
        console.print("  1. Python (detected)")
        selected = Prompt.ask("Select language", default="python")
        languages = [selected.lower()]

    config = MaikDocsConfig(
        project_root=project_root,
        output_folder=output_folder,
        languages=languages,
    )

    config.save(config_path)

    output_dir = project_root / output_folder
    output_dir.mkdir(exist_ok=True)

    console.print(f"\n[green]✓ Configuration created: {config_path}[/green]")
    console.print(f"[green]✓ Output directory created: {output_dir}[/green]")

    console.print("\n[cyan]Next steps:[/cyan]")
    console.print(f"  1. Run [bold]maikdocs generate[/bold] to generate documentation")
    console.print(f"  2. Customize {config_path} as needed")


def _detect_project_root(start_path: Path) -> Path:
    """Detect project root by looking for markers.

    Args:
        start_path: Starting directory

    Returns:
        Detected project root
    """
    markers = [".git", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt"]

    current = start_path.resolve()

    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent

    return start_path
