"""Path translation utilities for converting between source and .maik documentation paths."""

from pathlib import Path
from typing import Literal

from maikdocs.core.config import MaikDocsConfig


class PathTranslationError(Exception):
    """Base exception for path translation errors."""


class PathNotFoundError(PathTranslationError):
    """Path doesn't exist in either source or .maik location."""


class AmbiguousPathError(PathTranslationError):
    """Path exists in both locations, unclear which to use."""


class PathTranslator:
    """Bidirectional translation between source and .maik documentation paths.

    This class handles automatic path translation, allowing users to provide
    either source file paths or .maik documentation paths interchangeably.
    """

    # Extension mapping for supported languages
    EXTENSION_MAP: dict[str, str] = {
        "python": ".py",
        # Future: "javascript": ".js", "typescript": ".ts", etc.
    }

    def __init__(self, config: MaikDocsConfig):
        """Initialize path translator with configuration.

        Args:
            config: MaikDocs configuration
        """
        self.config = config

    def translate(
        self,
        path: Path,
        command_context: Literal["read", "generate", "update", "extract"] = "read"
    ) -> Path:
        """Auto-detect and translate paths intelligently.

        This method determines whether the input path is a source path or
        .maik documentation path, and translates it appropriately based on
        the command context.

        Args:
            path: Input path (source or .maik documentation path)
            command_context: Command using this translation

        Returns:
            Translated path

        Raises:
            PathNotFoundError: If path doesn't exist and can't be translated

        Examples:
            >>> translator.translate(Path("src/core/config.py"), "read")
            Path(".maik/src/core/config_maik.md")

            >>> translator.translate(Path("src/core/"), "read")
            Path(".maik/src/core/index_maik.md")

            >>> translator.translate(Path(".maik/src/core/config_maik.md"), "read")
            Path(".maik/src/core/config_maik.md")  # Pass through
        """
        # Resolve to absolute path
        resolved_path = path.resolve()

        # If path contains .maik/, assume it's already a documentation path
        if self.is_doc_path(resolved_path):
            return resolved_path

        # Handle folder paths
        if resolved_path.is_dir():
            return self.resolve_folder_path(resolved_path, command_context)

        # Handle file paths - translate source to .maik
        if resolved_path.is_file():
            return self.source_to_doc(resolved_path)

        # Path doesn't exist - try to determine what it should be
        # Check if it looks like a source path (has extension)
        if resolved_path.suffix:
            # Assume it's a source file that should have documentation
            doc_path = self.source_to_doc(resolved_path)
            if not doc_path.exists():
                raise PathNotFoundError(
                    f"Documentation not found for: {path}\n"
                    f"Expected at: {doc_path}\n"
                    f"Hint: Run 'maikdocs generate {path}' first"
                )
            return doc_path

        # No extension - might be a folder
        # Try as folder path
        try:
            return self.resolve_folder_path(resolved_path, command_context)
        except PathNotFoundError:
            raise PathNotFoundError(
                f"Path not found: {path}\n"
                f"Could not determine if this is a source or documentation path."
            )

    def source_to_doc(self, source_path: Path) -> Path:
        """Forward translation: source file → .maik documentation.

        Delegates to config.get_output_path() for consistency with
        documentation generation logic.

        Args:
            source_path: Path to source file

        Returns:
            Path to corresponding .maik documentation file

        Example:
            >>> translator.source_to_doc(Path("src/core/config.py"))
            Path(".maik/src/core/config_maik.md")
        """
        return self.config.get_output_path(source_path)

    def doc_to_source(self, doc_path: Path) -> Path | None:
        """Reverse translation: .maik documentation → source file.

        Supports multiple language extensions by trying all configured
        languages in order.

        Args:
            doc_path: Path to .maik documentation file

        Returns:
            Path to source file if found, None otherwise

        Example:
            >>> translator.doc_to_source(Path(".maik/src/core/config_maik.md"))
            Path("src/core/config.py")
        """
        try:
            # Get relative path from .maik folder
            relative = doc_path.relative_to(
                self.config.project_root / self.config.output_folder
            )
        except ValueError:
            # Path is not under .maik folder
            return None

        # Get base name without _maik suffix
        if not doc_path.stem.endswith("_maik"):
            # This might be index_maik.md or other special file
            if doc_path.name == "index_maik.md":
                # index_maik.md doesn't have a direct source file
                return None
            return None

        base_name = doc_path.stem.replace("_maik", "")

        # Try extensions based on configured languages
        for lang in self.config.languages:
            ext = self.EXTENSION_MAP.get(lang)
            if ext:
                source_path = self.config.project_root / relative.parent / (base_name + ext)
                if source_path.exists():
                    return source_path

        # No source file found with any configured extension
        return None

    def is_doc_path(self, path: Path) -> bool:
        """Check if path is in .maik documentation folder.

        Args:
            path: Path to check

        Returns:
            True if path contains .maik/ folder
        """
        try:
            path.relative_to(self.config.project_root / self.config.output_folder)
            return True
        except ValueError:
            return False

    def resolve_folder_path(
        self,
        path: Path,
        command_context: Literal["read", "generate", "update", "extract"]
    ) -> Path:
        """Handle folder paths based on command context.

        Different commands treat folders differently:
        - read: folder → index_maik.md
        - generate/update: use folder as target directory (pass through)
        - extract: folders not supported

        Args:
            path: Folder path
            command_context: Command using this translation

        Returns:
            Translated path

        Raises:
            PathNotFoundError: If folder or resulting file doesn't exist
        """
        if command_context == "read":
            # For read command, translate folder to index_maik.md
            if self.is_doc_path(path):
                # Already a .maik path - add index_maik.md
                index_path = path / "index_maik.md"
            else:
                # Source folder - get corresponding index
                index_path = self.config.get_index_path(path)

            if not index_path.exists():
                raise PathNotFoundError(
                    f"Index documentation not found: {index_path}\n"
                    f"Hint: Run 'maikdocs generate {path}' first"
                )
            return index_path

        elif command_context in ("generate", "update"):
            # For generate/update, use folder as-is (target directory)
            return path

        elif command_context == "extract":
            raise PathNotFoundError(
                f"Extract command requires a file path, not a folder: {path}"
            )

        # Default: pass through
        return path
