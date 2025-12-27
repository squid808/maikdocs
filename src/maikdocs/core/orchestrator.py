"""Build orchestration for documentation generation."""

from dataclasses import dataclass, field
from pathlib import Path

from maikdocs.core.config import MaikDocsConfig
from maikdocs.core.tracker import DocumentationTracker
from maikdocs.filesystem.scanner import FileSystemScanner
from maikdocs.generators.file_doc import FileDocumentationGenerator
from maikdocs.generators.index_doc import IndexDocumentationGenerator
from maikdocs.generators.project_doc import ProjectDocumentationGenerator
from maikdocs.parsers.base import ParserRegistry, ParsedModule
from maikdocs.parsers.python_parser import PythonParser
from maikdocs.utils.path_translator import PathTranslator


@dataclass
class BuildResult:
    """Result of a documentation build."""

    files_generated: list[Path] = field(default_factory=list)
    indexes_generated: list[Path] = field(default_factory=list)
    files_removed: list[Path] = field(default_factory=list)
    files_skipped: list[Path] = field(default_factory=list)
    errors: list[tuple[Path, str]] = field(default_factory=list)

    def add_generated(self, path: Path) -> None:
        """Add a generated file."""
        self.files_generated.append(path)

    def add_index(self, path: Path) -> None:
        """Add a generated index."""
        self.indexes_generated.append(path)

    def add_removed(self, path: Path) -> None:
        """Add a removed file."""
        self.files_removed.append(path)

    def add_skipped(self, path: Path) -> None:
        """Add a skipped file."""
        self.files_skipped.append(path)

    def add_error(self, path: Path, error: str) -> None:
        """Add an error."""
        self.errors.append((path, error))

    @property
    def total_generated(self) -> int:
        """Total files and indexes generated."""
        return len(self.files_generated) + len(self.indexes_generated)


class BuildOrchestrator:
    """Coordinates documentation generation using bottom-up strategy."""

    def __init__(self, config: MaikDocsConfig) -> None:
        """Initialize orchestrator with configuration.

        Args:
            config: Project configuration
        """
        self.config = config
        self.scanner = FileSystemScanner(config)
        self.tracker = DocumentationTracker(
            config.project_root / config.output_folder / ".maikdocs_state.json"
        )
        self.parser_registry = ParserRegistry()
        self.file_generator = FileDocumentationGenerator()
        self.index_generator = IndexDocumentationGenerator(config)
        self.project_generator = ProjectDocumentationGenerator(config)

        self._register_parsers()

    def _register_parsers(self) -> None:
        """Register available parsers."""
        python_parser = PythonParser(self.config.visibility_rules)
        self.parser_registry.register(python_parser)

    def generate_all(
        self,
        target: Path | None = None,
        recursive: bool = True,
        force: bool = False,
    ) -> BuildResult:
        """Generate documentation for entire project or specific target.

        Args:
            target: Target file or directory (None for entire project)
            recursive: Process directories recursively
            force: Force regeneration regardless of timestamps

        Returns:
            Build result with statistics
        """
        self.tracker.load_state()

        if target and target.is_file():
            sources = [target] if self.parser_registry.supports_file(target) else []
        else:
            root = target if target else self.config.project_root
            sources = self.scanner.scan(root, recursive)

        result = BuildResult()

        parsed_modules: dict[Path, ParsedModule] = {}
        for source in sources:
            try:
                if not force and not self.tracker.needs_update(
                    source,
                    self.config.get_output_path(source),
                    force
                ):
                    result.add_skipped(source)
                    continue

                parser = self.parser_registry.get_parser(source)
                parsed = parser.parse(source)
                parsed_modules[source] = parsed

                doc_path = self.config.get_output_path(source)
                self.file_generator.generate(parsed, doc_path)

                loc = len(source.read_text(encoding="utf-8").splitlines())
                self.tracker.mark_generated(source, doc_path, loc)

                result.add_generated(doc_path)

            except Exception as e:
                result.add_error(source, str(e))

        directories = self.scanner.get_directories(list(parsed_modules.keys()))
        for directory in sorted(directories, key=lambda d: len(d.parts), reverse=True):
            try:
                dir_modules = [
                    parsed_modules[src]
                    for src in parsed_modules.keys()
                    if src.parent == directory
                ]

                if dir_modules:
                    self.index_generator.generate(directory, dir_modules)
                    index_path = self.config.get_index_path(directory)
                    result.add_index(index_path)

                    dependencies = [src for src in parsed_modules.keys() if src.parent == directory]
                    self.tracker.mark_index_generated(index_path, dependencies)

            except Exception as e:
                result.add_error(directory, str(e))

        # Generate project overview if we processed the whole project (not a specific target)
        if not target or (target and target.is_dir()):
            try:
                all_modules = list(parsed_modules.values())
                self.project_generator.generate(all_modules, directories)
                project_path = self.config.project_root / self.config.output_folder / "PROJECT.md"
                result.add_index(project_path)
            except Exception as e:
                result.add_error(Path("PROJECT.md"), str(e))

        self.tracker.save_state()

        return result

    def update_incremental(
        self,
        target: Path | None = None,
        preserve_orphaned: bool | None = None,
    ) -> BuildResult:
        """Incrementally update documentation based on timestamps.

        Args:
            target: Target file or directory (None for entire project)
            preserve_orphaned: Override config for orphaned file handling

        Returns:
            Build result with statistics
        """
        self.tracker.load_state()

        root = target if target and target.is_dir() else self.config.project_root
        current_sources = set(self.scanner.scan(root, recursive=True))

        result = self.generate_all(target, recursive=True, force=False)

        preserve = preserve_orphaned if preserve_orphaned is not None else self.config.preserve_orphaned

        if not preserve:
            orphaned = self.tracker.get_orphaned_docs(current_sources)
            translator = PathTranslator(self.config)
            for orphan in orphaned:
                try:
                    orphan.unlink()
                    result.add_removed(orphan)

                    source_path = translator.doc_to_source(orphan)
                    if source_path:
                        self.tracker.remove_file(source_path)

                except Exception as e:
                    result.add_error(orphan, str(e))

            affected_indexes = self.tracker.get_affected_indexes(result.files_generated)
            for index_path in affected_indexes:
                try:
                    directory = index_path.parent
                    dir_modules = self._get_directory_modules(directory, current_sources)

                    if dir_modules:
                        self.index_generator.generate(directory, dir_modules)
                        result.add_index(index_path)

                except Exception as e:
                    result.add_error(index_path, str(e))

        self.tracker.save_state()

        return result

    def _get_directory_modules(
        self,
        directory: Path,
        sources: set[Path]
    ) -> list[ParsedModule]:
        """Get parsed modules for a directory.

        Args:
            directory: Directory path
            sources: Available source files

        Returns:
            List of parsed modules in directory
        """
        modules = []
        for source in sources:
            if source.parent == directory:
                try:
                    parser = self.parser_registry.get_parser(source)
                    parsed = parser.parse(source)
                    modules.append(parsed)
                except Exception:
                    pass

        return modules
