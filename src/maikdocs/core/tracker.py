"""State tracking for incremental documentation updates."""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class FileMetadata:
    """Metadata for tracking file state."""

    source_path: str
    doc_path: str
    source_mtime: float
    doc_mtime: float
    loc: int
    last_generated: str
    checksum: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FileMetadata":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class IndexMetadata:
    """Metadata for index files."""

    path: str
    dependencies: list[str]
    last_generated: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "IndexMetadata":
        """Create from dictionary."""
        return cls(**data)


class DocumentationTracker:
    """Tracks documentation state across project."""

    def __init__(self, state_file: Path) -> None:
        """Initialize tracker with state file location.

        Args:
            state_file: Path to .maikdocs_state.json
        """
        self.state_file = state_file
        self.files: dict[str, FileMetadata] = {}
        self.indexes: dict[str, IndexMetadata] = {}
        self.version = "1.0"

    def load_state(self) -> None:
        """Load tracking state from disk."""
        if not self.state_file.exists():
            return

        try:
            with self.state_file.open("r") as f:
                data = json.load(f)

            self.version = data.get("version", "1.0")

            for path, file_data in data.get("files", {}).items():
                self.files[path] = FileMetadata.from_dict(file_data)

            for path, index_data in data.get("indexes", {}).items():
                self.indexes[path] = IndexMetadata.from_dict(index_data)

        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Corrupted state file: {e}")

    def save_state(self) -> None:
        """Persist tracking state to disk."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": self.version,
            "last_updated": datetime.now().isoformat(),
            "files": {path: meta.to_dict() for path, meta in self.files.items()},
            "indexes": {path: meta.to_dict() for path, meta in self.indexes.items()},
        }

        with self.state_file.open("w") as f:
            json.dump(data, f, indent=2)

    def needs_update(self, source_path: Path, doc_path: Path, force: bool = False) -> bool:
        """Check if source file is newer than its documentation.

        Args:
            source_path: Path to source file
            doc_path: Path to documentation file
            force: Force regeneration regardless of timestamps

        Returns:
            True if documentation needs to be regenerated
        """
        if force:
            return True

        if not doc_path.exists():
            return True

        source_key = str(source_path)
        if source_key not in self.files:
            return True

        metadata = self.files[source_key]

        source_mtime = source_path.stat().st_mtime
        if source_mtime > metadata.source_mtime:
            return True

        current_checksum = self._compute_checksum(source_path)
        if current_checksum != metadata.checksum:
            return True

        return False

    def mark_generated(
        self,
        source_path: Path,
        doc_path: Path,
        loc: int
    ) -> None:
        """Record successful documentation generation.

        Args:
            source_path: Path to source file
            doc_path: Path to generated documentation
            loc: Lines of code in source file
        """
        source_key = str(source_path)

        metadata = FileMetadata(
            source_path=source_key,
            doc_path=str(doc_path),
            source_mtime=source_path.stat().st_mtime,
            doc_mtime=doc_path.stat().st_mtime,
            loc=loc,
            last_generated=datetime.now().isoformat(),
            checksum=self._compute_checksum(source_path),
        )

        self.files[source_key] = metadata

    def mark_index_generated(
        self,
        index_path: Path,
        dependencies: list[Path]
    ) -> None:
        """Record index generation.

        Args:
            index_path: Path to index file
            dependencies: Source files that index depends on
        """
        index_key = str(index_path)

        metadata = IndexMetadata(
            path=index_key,
            dependencies=[str(d) for d in dependencies],
            last_generated=datetime.now().isoformat(),
        )

        self.indexes[index_key] = metadata

    def get_orphaned_docs(self, current_sources: set[Path]) -> list[Path]:
        """Find documentation files with no corresponding source.

        Args:
            current_sources: Set of current source file paths

        Returns:
            List of orphaned documentation file paths
        """
        current_sources_str = {str(p) for p in current_sources}
        orphaned = []

        for source_key, metadata in self.files.items():
            if source_key not in current_sources_str:
                doc_path = Path(metadata.doc_path)
                if doc_path.exists():
                    orphaned.append(doc_path)

        return orphaned

    def get_affected_indexes(self, changed_files: list[Path]) -> set[Path]:
        """Find index files that need regeneration due to file changes.

        Args:
            changed_files: List of changed source files

        Returns:
            Set of index file paths that need updating
        """
        changed_str = {str(f) for f in changed_files}
        affected = set()

        for index_key, metadata in self.indexes.items():
            if any(dep in changed_str for dep in metadata.dependencies):
                affected.add(Path(index_key))

        return affected

    def remove_file(self, source_path: Path) -> None:
        """Remove file from tracking state.

        Args:
            source_path: Source file to remove
        """
        source_key = str(source_path)
        if source_key in self.files:
            del self.files[source_key]

    def _compute_checksum(self, path: Path) -> str:
        """Compute SHA256 checksum of file.

        Args:
            path: File path

        Returns:
            Hexadecimal checksum string
        """
        hasher = hashlib.sha256()
        with path.open("rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()[:16]
