"""Read command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from maikdocs.utils.markdown import MarkdownSectionParser

console = Console()


def read_command(
    file: Path,
    types: list[str] | None = None,
) -> None:
    """Read documentation file with optional filtering.

    Args:
        file: Documentation file to read
        types: Symbol types to filter (method, function, field, class, description)
    """
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    if not file.suffix == ".md":
        console.print(f"[yellow]Warning: {file} is not a markdown file[/yellow]")

    parser = MarkdownSectionParser()

    if types:
        sections = parser.extract_symbol_types(file, types)

        if not sections:
            console.print(f"[yellow]No sections found for types: {', '.join(types)}[/yellow]")
            raise typer.Exit(1)

        for section_name, content in sections.items():
            console.print(f"\n[bold cyan]━━━ {section_name} ━━━[/bold cyan]\n")
            md = Markdown(content)
            console.print(md)

    else:
        content = file.read_text(encoding="utf-8")
        md = Markdown(content)
        console.print(md)
