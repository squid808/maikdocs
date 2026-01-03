"""Cleanup utilities for documentation files."""

from pathlib import Path

from maikdocs.core.config import MaikDocsConfig


class DocumentationCleaner:
    """Handles cleanup of documentation files."""

    def __init__(self, config: MaikDocsConfig) -> None:
        """Initialize cleaner with configuration.

        Args:
            config: Project configuration
        """
        self.config = config

    def clean_all(self, dry_run: bool = False) -> list[Path]:
        """Remove all generated documentation.

        Args:
            dry_run: If True, return what would be deleted without deleting

        Returns:
            List of files that were (or would be) deleted
        """
        output_dir = self.config.project_root / self.config.output_folder

        if not output_dir.exists():
            return []

        deleted = []

        for item in output_dir.rglob("*"):
            if item.is_file():
                deleted.append(item)
                if not dry_run:
                    item.unlink()

        if not dry_run:
            for item in sorted(output_dir.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                if item.is_dir() and not any(item.iterdir()):
                    item.rmdir()

            if output_dir.exists() and not any(output_dir.iterdir()):
                output_dir.rmdir()

        return deleted

    def clean_orphaned(
        self,
        orphaned: list[Path],
        dry_run: bool = False
    ) -> list[Path]:
        """Remove orphaned documentation files.

        Args:
            orphaned: List of orphaned file paths
            dry_run: If True, return what would be deleted without deleting

        Returns:
            List of files that were (or would be) deleted
        """
        deleted = []

        for path in orphaned:
            if path.exists():
                deleted.append(path)
                if not dry_run:
                    path.unlink()

        if not dry_run:
            self._cleanup_empty_dirs()

        return deleted

    def _cleanup_empty_dirs(self) -> None:
        """Remove empty directories in output folder."""
        output_dir = self.config.project_root / self.config.output_folder

        if not output_dir.exists():
            return

        for item in sorted(output_dir.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if item.is_dir() and not any(item.iterdir()):
                try:
                    item.rmdir()
                except OSError:
                    pass
