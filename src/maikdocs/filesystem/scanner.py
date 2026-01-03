"""File system scanning with pattern matching."""

from pathlib import Path
from fnmatch import fnmatch
from typing import Iterator

from maikdocs.core.config import MaikDocsConfig


class FileSystemScanner:
    """Scans file system for source files matching patterns."""

    def __init__(self, config: MaikDocsConfig) -> None:
        """Initialize scanner with configuration.

        Args:
            config: Project configuration
        """
        self.config = config

    def scan(
        self,
        root: Path | None = None,
        recursive: bool = True
    ) -> list[Path]:
        """Scan for source files matching include/exclude patterns.

        Args:
            root: Root directory to scan (defaults to project_root)
            recursive: Whether to scan subdirectories

        Returns:
            List of source file paths
        """
        if root is None:
            root = self.config.project_root

        if not root.exists():
            return []

        pattern = "**/*" if recursive else "*"

        all_files = root.glob(pattern)

        matched_files = []
        for file_path in all_files:
            if not file_path.is_file():
                continue

            if self._should_exclude(file_path):
                continue

            if self._should_include(file_path):
                matched_files.append(file_path)

        return sorted(matched_files)

    def get_directories(self, sources: list[Path]) -> set[Path]:
        """Get all unique directories containing source files.

        Args:
            sources: List of source file paths

        Returns:
            Set of directory paths
        """
        directories = set()
        for source in sources:
            current = source.parent
            while current >= self.config.project_root:
                directories.add(current)
                if current == self.config.project_root:
                    break
                current = current.parent

        return directories

    def _should_include(self, path: Path) -> bool:
        """Check if file matches include patterns.

        Args:
            path: File path to check

        Returns:
            True if file should be included
        """
        if not self.config.include_patterns:
            return True

        relative_path = self._get_relative_path(path)

        return any(
            fnmatch(path.name, pattern) or fnmatch(str(relative_path), pattern)
            for pattern in self.config.include_patterns
        )

    def _should_exclude(self, path: Path) -> bool:
        """Check if file matches exclude patterns.

        Args:
            path: File path to check

        Returns:
            True if file should be excluded
        """
        relative_path = self._get_relative_path(path)

        if self.config.output_folder in path.parts:
            return True

        if any(part.startswith(".") and part != "." for part in path.parts):
            if not any(part == ".maik_meta.md" for part in path.parts):
                return True

        return any(
            fnmatch(path.name, pattern) or fnmatch(str(relative_path), pattern)
            for pattern in self.config.exclude_patterns
        )

    def _get_relative_path(self, path: Path) -> Path:
        """Get path relative to project root.

        Args:
            path: Absolute path

        Returns:
            Relative path
        """
        try:
            return path.relative_to(self.config.project_root)
        except ValueError:
            return path
