"""Extract command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.syntax import Syntax

from maikdocs.utils.markdown import CodeExtractor

console = Console()


def extract_command(
    file: Path,
    sections: list[str] | None = None,
) -> None:
    """Pull actual code from source file based on symbols.

    Args:
        file: Source file to extract from
        sections: Symbol names to extract
    """
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)

    extractor = CodeExtractor()

    if sections:
        extracted = extractor.extract_by_symbols(file, sections)

        if not extracted:
            console.print(f"[yellow]No symbols found: {', '.join(sections)}[/yellow]")
            raise typer.Exit(1)

        for symbol_name, code in extracted.items():
            console.print(f"\n[bold cyan]━━━ {symbol_name} ━━━[/bold cyan]\n")

            syntax = Syntax(
                code,
                "python",
                theme="monokai",
                line_numbers=True,
            )
            console.print(syntax)

    else:
        imports = extractor.extract_imports(file)

        if imports:
            console.print("[bold cyan]━━━ Imports ━━━[/bold cyan]\n")
            syntax = Syntax(imports, "python", theme="monokai")
            console.print(syntax)
        else:
            console.print("[yellow]No imports found or no sections specified[/yellow]")
            console.print("Use --sections to specify symbols to extract")
