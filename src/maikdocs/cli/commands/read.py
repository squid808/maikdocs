"""Read command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from maikdocs.cli.commands.generate import _load_config
from maikdocs.utils.markdown import MarkdownSectionParser
from maikdocs.utils.path_translator import PathNotFoundError, PathTranslator

console = Console()


def read_command(
    file: Path,
    types: list[str] | None = None,
) -> None:
    """Read documentation file with optional filtering.

    Supports both source file paths and .maik documentation paths.
    The command will automatically translate source paths to their
    corresponding .maik documentation paths.

    Args:
        file: Source file, folder, or .maik documentation path to read
        types: Symbol types to filter (method, function, field, class, description)

    Examples:
        # Read using source path
        maikdocs read src/core/config.py

        # Read using folder path (reads index_maik.md)
        maikdocs read src/core/

        # Read using .maik path (backwards compatible)
        maikdocs read .maik/src/core/config_maik.md
    """
    # Load config and create translator
    config = _load_config()
    translator = PathTranslator(config)

    # Translate path (handles source files, folders, .maik paths)
    try:
        doc_file = translator.translate(file, command_context="read")
    except PathNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if not doc_file.exists():
        console.print(f"[red]Documentation file not found: {doc_file}[/red]")
        console.print(f"[dim]Hint: Run 'maikdocs generate {file}' first[/dim]")
        raise typer.Exit(1)

    if not doc_file.suffix == ".md":
        console.print(f"[yellow]Warning: {doc_file} is not a markdown file[/yellow]")

    parser = MarkdownSectionParser()

    if types:
        sections = parser.extract_symbol_types(doc_file, types)

        if not sections:
            console.print(f"[yellow]No sections found for types: {', '.join(types)}[/yellow]")
            raise typer.Exit(1)

        for section_name, content in sections.items():
            console.print(f"\n[bold cyan]━━━ {section_name} ━━━[/bold cyan]\n")
            md = Markdown(content)
            console.print(md)

    else:
        content = doc_file.read_text(encoding="utf-8")
        md = Markdown(content)
        console.print(md)
