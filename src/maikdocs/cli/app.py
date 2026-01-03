"""Main CLI application for maikdocs."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from maikdocs.cli.commands.clean import clean_command
from maikdocs.cli.commands.coverage import coverage_command
from maikdocs.cli.commands.extract import extract_command
from maikdocs.cli.commands.generate import generate_command
from maikdocs.cli.commands.init import init_command
from maikdocs.cli.commands.read import read_command
from maikdocs.cli.commands.update import update_command

app = typer.Typer(
    name="maikdocs",
    help="Generate AI-friendly markdown documentation for Python codebases",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.command()
def init(
    directory: Annotated[
        Optional[Path],
        typer.Argument(help="Project root directory (defaults to current directory)")
    ] = None,
    languages: Annotated[
        Optional[list[str]],
        typer.Option("--language", "-l", help="Languages to support")
    ] = None,
    output_folder: Annotated[
        str,
        typer.Option("--output", "-o", help="Output folder for documentation")
    ] = ".maik",
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing configuration")
    ] = False,
) -> None:
    """Initialize maikdocs in a project directory."""
    init_command(directory, languages, output_folder, force)


@app.command()
def generate(
    target: Annotated[
        Optional[Path],
        typer.Argument(help="Target file, directory, or leave empty for entire project")
    ] = None,
    recursive: Annotated[
        bool,
        typer.Option("--recursive/--no-recursive", "-r/-R", help="Process directories recursively")
    ] = True,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Regenerate all documentation regardless of timestamps")
    ] = False,
    whatif: Annotated[
        bool,
        typer.Option("--whatif", help="Show what would happen without making changes")
    ] = False,
) -> None:
    """Generate documentation from scratch."""
    generate_command(target, recursive, force, whatif)


@app.command()
def update(
    target: Annotated[
        Optional[Path],
        typer.Argument(help="Target file, directory, or leave empty for entire project")
    ] = None,
    keep_orphaned: Annotated[
        Optional[bool],
        typer.Option("--keep-orphaned/--remove-orphaned", help="Preserve or remove orphaned documentation files")
    ] = None,
    whatif: Annotated[
        bool,
        typer.Option("--whatif", help="Show what would be updated without making changes")
    ] = False,
) -> None:
    """Incrementally update documentation based on file changes."""
    update_command(target, keep_orphaned, whatif)


@app.command()
def clean(
    all: Annotated[
        bool,
        typer.Option("--all", help="Remove all generated documentation and state")
    ] = False,
    whatif: Annotated[
        bool,
        typer.Option("--whatif", help="Show what would be deleted without removing files")
    ] = False,
) -> None:
    """Clean orphaned or all documentation files."""
    clean_command(all, whatif)


@app.command()
def read(
    file: Annotated[
        Path,
        typer.Argument(help="Documentation file to read")
    ],
    types: Annotated[
        Optional[list[str]],
        typer.Option("--types", "-t", help="Symbol types to filter (method, function, field, class, description)")
    ] = None,
) -> None:
    """Read documentation file with optional filtering."""
    read_command(file, types)


@app.command()
def extract(
    file: Annotated[
        Path,
        typer.Option("--file", "-f", help="Source file to extract from")
    ],
    sections: Annotated[
        Optional[list[str]],
        typer.Option("--sections", "-s", help="Symbol names to extract")
    ] = None,
) -> None:
    """Pull actual code from source file based on symbols."""
    extract_command(file, sections)


@app.command()
def coverage(
    file: Annotated[
        Optional[Path],
        typer.Option("--file", help="Check specific file")
    ] = None,
    directory: Annotated[
        Optional[Path],
        typer.Option("--directory", "-d", help="Check specific directory")
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output file for results")
    ] = None,
    noclobber: Annotated[
        bool,
        typer.Option("--noclobber", help="Append to output file instead of replacing")
    ] = False,
) -> None:
    """Show documentation coverage and missing elements."""
    coverage_command(file, directory, output, noclobber)


if __name__ == "__main__":
    app()
