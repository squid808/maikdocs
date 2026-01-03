"""Coverage command implementation."""

from dataclasses import dataclass, field
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from maikdocs.cli.commands.generate import _load_config
from maikdocs.core.orchestrator import BuildOrchestrator
from maikdocs.filesystem.scanner import FileSystemScanner

console = Console()


@dataclass
class CoverageReport:
    """Documentation coverage report."""

    total_files: int = 0
    documented_files: int = 0
    missing_docs: list[Path] = field(default_factory=list)
    outdated_docs: list[Path] = field(default_factory=list)
    missing_docstrings: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        """Calculate coverage percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.documented_files / self.total_files) * 100


def coverage_command(
    file: Path | None = None,
    directory: Path | None = None,
    output: Path | None = None,
    noclobber: bool = False,
) -> None:
    """Show documentation coverage and missing elements.

    Args:
        file: Check specific file
        directory: Check specific directory
        output: Output file for results
        noclobber: Append to output file instead of replacing
    """
    config = _load_config()
    scanner = FileSystemScanner(config)
    orchestrator = BuildOrchestrator(config)
    orchestrator.tracker.load_state()

    if file:
        sources = [file] if file.exists() else []
    elif directory:
        sources = scanner.scan(directory, recursive=True)
    else:
        sources = scanner.scan(config.project_root, recursive=True)

    report = CoverageReport()
    report.total_files = len(sources)

    for source in sources:
        doc_path = config.get_output_path(source)

        if not doc_path.exists():
            report.missing_docs.append(source)
        elif orchestrator.tracker.needs_update(source, doc_path):
            report.outdated_docs.append(source)
            report.documented_files += 1
        else:
            report.documented_files += 1

        missing = _check_missing_docstrings(source, orchestrator)
        if missing:
            report.missing_docstrings.extend((source, item) for item in missing)

    _display_report(report)

    if output:
        _write_report(report, output, noclobber)


def _check_missing_docstrings(source_path: Path, orchestrator: BuildOrchestrator) -> list[str]:
    """Check for missing docstrings in source file.

    Args:
        source_path: Path to source file
        orchestrator: Build orchestrator with parser registry

    Returns:
        List of items missing docstrings
    """
    try:
        # Get appropriate parser from registry
        parser = orchestrator.parser_registry.get_parser(source_path)
        if not parser:
            return []

        parsed = parser.parse(source_path)

        missing = []

        if not parsed.docstring:
            missing.append("module")

        for cls in parsed.classes:
            if not cls.docstring and cls.visibility == "public":
                missing.append(f"class {cls.name}")

            for method in cls.methods:
                if not method.docstring and method.visibility == "public":
                    missing.append(f"{cls.name}.{method.name}")

        for func in parsed.functions:
            if not func.docstring and func.visibility == "public":
                missing.append(f"function {func.name}")

        return missing

    except Exception:
        return []


def _display_report(report: CoverageReport) -> None:
    """Display coverage report to console.

    Args:
        report: Coverage report
    """
    console.print("\n[bold cyan]Documentation Coverage Report[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Total Files", str(report.total_files))
    table.add_row("Documented Files", str(report.documented_files))
    table.add_row(
        "Coverage",
        f"{report.coverage_percentage:.1f}%",
        style="green" if report.coverage_percentage >= 80 else "yellow"
    )
    table.add_row("Missing Documentation", str(len(report.missing_docs)))
    table.add_row("Outdated Documentation", str(len(report.outdated_docs)))
    table.add_row("Missing Docstrings", str(len(report.missing_docstrings)))

    console.print(table)

    if report.missing_docs:
        console.print("\n[yellow]Files without documentation:[/yellow]")
        for path in report.missing_docs[:10]:
            console.print(f"  - {path}")
        if len(report.missing_docs) > 10:
            console.print(f"  ... and {len(report.missing_docs) - 10} more")

    if report.outdated_docs:
        console.print("\n[yellow]Outdated documentation:[/yellow]")
        for path in report.outdated_docs[:10]:
            console.print(f"  - {path}")
        if len(report.outdated_docs) > 10:
            console.print(f"  ... and {len(report.outdated_docs) - 10} more")

    if report.missing_docstrings:
        console.print("\n[yellow]Missing docstrings:[/yellow]")
        displayed = {}
        for source, item in report.missing_docstrings[:20]:
            if source not in displayed:
                displayed[source] = []
            displayed[source].append(item)

        for source, items in list(displayed.items())[:10]:
            console.print(f"  {source}:")
            for item in items[:5]:
                console.print(f"    - {item}")
            if len(items) > 5:
                console.print(f"    ... and {len(items) - 5} more")

        if len(report.missing_docstrings) > 20:
            console.print(f"  ... and {len(report.missing_docstrings) - 20} more")


def _write_report(report: CoverageReport, output_path: Path, append: bool) -> None:
    """Write coverage report to file.

    Args:
        report: Coverage report
        output_path: Output file path
        append: Whether to append or replace
    """
    mode = "a" if append else "w"

    with output_path.open(mode, encoding="utf-8") as f:
        f.write("# Documentation Coverage Report\n\n")
        f.write(f"Total Files: {report.total_files}\n")
        f.write(f"Documented Files: {report.documented_files}\n")
        f.write(f"Coverage: {report.coverage_percentage:.1f}%\n\n")

        if report.missing_docs:
            f.write("## Missing Documentation\n\n")
            for path in report.missing_docs:
                f.write(f"- {path}\n")
            f.write("\n")

        if report.outdated_docs:
            f.write("## Outdated Documentation\n\n")
            for path in report.outdated_docs:
                f.write(f"- {path}\n")
            f.write("\n")

        if report.missing_docstrings:
            f.write("## Missing Docstrings\n\n")
            current_file = None
            for source, item in report.missing_docstrings:
                if source != current_file:
                    f.write(f"\n### {source}\n\n")
                    current_file = source
                f.write(f"- {item}\n")

    console.print(f"\n[green]✓ Report written to {output_path}[/green]")
