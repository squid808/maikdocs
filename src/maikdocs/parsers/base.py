"""Base classes and data structures for language parsers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class Parameter:
    """Function/method parameter."""

    name: str
    type_hint: str | None = None
    default_value: str | None = None
    description: str | None = None


@dataclass
class ParsedElement(ABC):
    """Base class for parsed code elements."""

    name: str
    signature: str
    visibility: Literal["public", "private"]
    docstring: str | None = None
    docstring_summary: str | None = None


@dataclass
class ParsedAttribute(ParsedElement):
    """Class or module attribute."""

    type_hint: str | None = None
    value: str | None = None


@dataclass
class ParsedFunction(ParsedElement):
    """Function or method."""

    parameters: list[Parameter] = field(default_factory=list)
    return_type: str | None = None
    is_async: bool = False
    is_staticmethod: bool = False
    is_classmethod: bool = False
    is_property: bool = False


@dataclass
class ParsedClass(ParsedElement):
    """Class definition."""

    methods: list[ParsedFunction] = field(default_factory=list)
    attributes: list[ParsedAttribute] = field(default_factory=list)
    base_classes: list[str] = field(default_factory=list)
    is_dataclass: bool = False
    is_abstract: bool = False


@dataclass
class ParsedConstant(ParsedElement):
    """Module-level constant."""

    type_hint: str | None = None
    value: str | None = None


@dataclass
class ParsedModule:
    """Parsed module structure."""

    path: Path
    docstring: str | None = None
    docstring_summary: str | None = None
    classes: list[ParsedClass] = field(default_factory=list)
    functions: list[ParsedFunction] = field(default_factory=list)
    constants: list[ParsedConstant] = field(default_factory=list)
    attributes: list[ParsedAttribute] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)

    def get_public_exports(self) -> list[str]:
        """Get list of public API elements.

        Returns:
            Names of public classes, functions, and constants
        """
        exports = []

        for cls in self.classes:
            if cls.visibility == "public":
                exports.append(cls.name)

        for func in self.functions:
            if func.visibility == "public":
                exports.append(func.name)

        for const in self.constants:
            if const.visibility == "public":
                exports.append(const.name)

        return exports


class LanguageParser(ABC):
    """Abstract base for language-specific parsers."""

    @abstractmethod
    def parse(self, source_path: Path) -> ParsedModule:
        """Parse source file into structured representation.

        Args:
            source_path: Path to source file

        Returns:
            Parsed module structure

        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If source file cannot be parsed
        """
        pass

    @abstractmethod
    def supports_file(self, path: Path) -> bool:
        """Check if parser can handle this file.

        Args:
            path: File path to check

        Returns:
            True if parser supports this file type
        """
        pass


class ParserRegistry:
    """Registry for language-specific parsers."""

    def __init__(self) -> None:
        """Initialize empty parser registry."""
        self._parsers: list[LanguageParser] = []

    def register(self, parser: LanguageParser) -> None:
        """Register a parser.

        Args:
            parser: Parser instance to register
        """
        self._parsers.append(parser)

    def get_parser(self, path: Path) -> LanguageParser:
        """Get appropriate parser for a file.

        Args:
            path: File path

        Returns:
            Parser that supports this file

        Raises:
            ValueError: If no parser supports this file
        """
        for parser in self._parsers:
            if parser.supports_file(path):
                return parser

        raise ValueError(f"No parser found for file: {path}")

    def supports_file(self, path: Path) -> bool:
        """Check if any parser supports this file.

        Args:
            path: File path to check

        Returns:
            True if at least one parser supports this file
        """
        return any(parser.supports_file(path) for parser in self._parsers)
