"""Configuration management for maikdocs."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class VisibilityRules(BaseModel):
    """Rules for controlling visibility of code elements."""

    include_private: bool = Field(
        default=False,
        description="Include private members (prefixed with _)"
    )


class MaikDocsConfig(BaseModel):
    """Configuration loaded from .maikdocs.yaml."""

    project_root: Path
    output_folder: str = Field(default=".maik", description="Folder for generated docs")
    file_pattern: str = Field(default="*_maik.md", description="Pattern for doc files")
    include_patterns: list[str] = Field(
        default_factory=lambda: ["*.py"],
        description="Patterns for files to include"
    )
    exclude_patterns: list[str] = Field(
        default_factory=list,
        description="Patterns for files to exclude"
    )
    visibility_rules: VisibilityRules = Field(default_factory=VisibilityRules)
    languages: list[Literal["python"]] = Field(
        default_factory=lambda: ["python"],
        description="Languages to document"
    )
    preserve_orphaned: bool = Field(
        default=False,
        description="Keep documentation for deleted source files"
    )

    @classmethod
    def load(cls, path: Path) -> "MaikDocsConfig":
        """Load configuration from YAML file.

        Args:
            path: Path to .maikdocs.yaml file

        Returns:
            Loaded configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is malformed
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        try:
            with path.open("r") as f:
                data = yaml.safe_load(f)

            if data is None:
                data = {}

            if "project_root" not in data:
                data["project_root"] = path.parent
            else:
                data["project_root"] = Path(data["project_root"])

            if "visibility_rules" in data and isinstance(data["visibility_rules"], dict):
                data["visibility_rules"] = VisibilityRules(**data["visibility_rules"])

            return cls(**data)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")

    @classmethod
    def create_default(cls, project_root: Path) -> "MaikDocsConfig":
        """Create a default configuration for a project.

        Args:
            project_root: Root directory of the project

        Returns:
            Default configuration
        """
        return cls(project_root=project_root)

    def save(self, path: Path) -> None:
        """Save configuration to YAML file.

        Args:
            path: Path where to save .maikdocs.yaml
        """
        data = self.model_dump(mode="python")
        data["project_root"] = str(self.project_root)

        if isinstance(data.get("visibility_rules"), dict):
            pass

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    def get_output_path(self, source_path: Path) -> Path:
        """Calculate .maik output path mirroring source structure.

        Args:
            source_path: Path to source file

        Returns:
            Path where documentation should be generated
        """
        try:
            relative = source_path.relative_to(self.project_root)
        except ValueError:
            relative = source_path

        doc_filename = source_path.stem + "_maik.md"

        doc_path = self.project_root / self.output_folder / relative.parent / doc_filename

        return doc_path

    def get_index_path(self, directory: Path) -> Path:
        """Get path for index_maik.md in a directory.

        Args:
            directory: Directory path

        Returns:
            Path to index file
        """
        try:
            relative = directory.relative_to(self.project_root)
        except ValueError:
            relative = Path(".")

        return self.project_root / self.output_folder / relative / "index_maik.md"

    def get_meta_path(self, directory: Path) -> Path:
        """Get path for .maik_meta.md in a directory.

        Args:
            directory: Directory path

        Returns:
            Path to metadata file
        """
        try:
            relative = directory.relative_to(self.project_root)
        except ValueError:
            relative = Path(".")

        return self.project_root / self.output_folder / relative / ".maik_meta.md"
