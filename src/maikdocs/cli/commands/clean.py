"""Clean command implementation."""

import typer
from rich.console import Console
from rich.prompt import Confirm

from maikdocs.cli.commands.generate import _load_config
from maikdocs.core.tracker import DocumentationTracker
from maikdocs.filesystem.cleaner import DocumentationCleaner
from maikdocs.filesystem.scanner import FileSystemScanner
from maikdocs.utils.path_translator import PathTranslator

console = Console()


def clean_command(
    all: bool = False,
    whatif: bool = False,
) -> None:
    """Clean orphaned or all documentation files.

    Args:
        all: Remove all generated documentation and state
        whatif: Show what would be deleted without removing files
    """
    config = _load_config()
    cleaner = DocumentationCleaner(config)

    if all:
        if not whatif and not Confirm.ask(
            "[yellow]This will remove all generated documentation. Continue?[/yellow]",
            default=False
        ):
            console.print("[dim]Cancelled[/dim]")
            raise typer.Exit(0)

        deleted = cleaner.clean_all(dry_run=whatif)

        if whatif:
            console.print(f"\n[yellow]Would delete {len(deleted)} files[/yellow]")
        else:
            console.print(f"\n[green]✓ Removed {len(deleted)} files[/green]")

        return

    tracker = DocumentationTracker(
        config.project_root / config.output_folder / ".maikdocs_state.json"
    )
    tracker.load_state()

    scanner = FileSystemScanner(config)
    current_sources = set(scanner.scan())

    orphaned = tracker.get_orphaned_docs(current_sources)

    if not orphaned:
        console.print("[cyan]No orphaned documentation files found[/cyan]")
        return

    console.print(f"\n[yellow]Found {len(orphaned)} orphaned documentation files[/yellow]")

    if not whatif:
        for orphan in orphaned[:5]:
            console.print(f"  - {orphan}")
        if len(orphaned) > 5:
            console.print(f"  ... and {len(orphaned) - 5} more")

    if not whatif and not Confirm.ask("\nRemove orphaned files?", default=True):
        console.print("[dim]Cancelled[/dim]")
        raise typer.Exit(0)

    deleted = cleaner.clean_orphaned(orphaned, dry_run=whatif)

    if whatif:
        console.print(f"\n[yellow]Would delete {len(deleted)} files[/yellow]")
    else:
        console.print(f"\n[green]✓ Removed {len(deleted)} orphaned files[/green]")

        translator = PathTranslator(config)
        for orphan in orphaned:
            source_path = translator.doc_to_source(orphan)
            if source_path:
                tracker.remove_file(source_path)

        tracker.save_state()
