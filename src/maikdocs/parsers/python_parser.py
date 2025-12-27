"""Python parser using pdoc."""

import inspect
import re
from pathlib import Path
from typing import Any

import pdoc
import pdoc.doc

from maikdocs.core.config import VisibilityRules
from maikdocs.parsers.base import (
    LanguageParser,
    Parameter,
    ParsedAttribute,
    ParsedClass,
    ParsedConstant,
    ParsedFunction,
    ParsedModule,
)


class PythonParser(LanguageParser):
    """Parser for Python files using pdoc."""

    def __init__(self, visibility_rules: VisibilityRules) -> None:
        """Initialize parser with visibility rules.

        Args:
            visibility_rules: Rules for filtering private/public elements
        """
        self.visibility_rules = visibility_rules

    def parse(self, source_path: Path) -> ParsedModule:
        """Parse Python file using pdoc.

        Args:
            source_path: Path to Python source file

        Returns:
            Parsed module structure

        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If source file cannot be parsed
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        try:
            module = pdoc.doc.Module.from_name(self._path_to_module_name(source_path))

            parsed = ParsedModule(
                path=source_path,
                docstring=module.docstring if module.docstring else None,
                docstring_summary=self._extract_summary(module.docstring) if module.docstring else None,
            )

            for name, member in module.members.items():
                if not self._should_include(name):
                    continue

                if isinstance(member, pdoc.doc.Class):
                    parsed.classes.append(self._parse_class(member))
                elif isinstance(member, pdoc.doc.Function):
                    parsed.functions.append(self._parse_function(member))
                elif isinstance(member, pdoc.doc.Variable):
                    if self._is_constant(name):
                        parsed.constants.append(self._parse_constant(member))
                    else:
                        parsed.attributes.append(self._parse_attribute(member))

            return parsed

        except Exception as e:
            raise ValueError(f"Failed to parse {source_path}: {e}")

    def supports_file(self, path: Path) -> bool:
        """Check if file is a Python file.

        Args:
            path: File path

        Returns:
            True if file has .py extension
        """
        return path.suffix == ".py"

    def _path_to_module_name(self, path: Path) -> str:
        """Convert file path to Python module name.

        Args:
            path: Path to Python file

        Returns:
            Module name (e.g., "mypackage.module")
        """
        parts = []
        for part in reversed(path.parts):
            if part.endswith(".py"):
                parts.insert(0, part[:-3])
            elif part in ("src", "lib"):
                break
            else:
                parts.insert(0, part)

        return ".".join(parts)

    def _should_include(self, name: str) -> bool:
        """Check if element should be included based on visibility.

        Args:
            name: Element name

        Returns:
            True if element should be included
        """
        if name.startswith("__") and name.endswith("__"):
            return False

        if name.startswith("_"):
            return self.visibility_rules.include_private

        return True

    def _get_visibility(self, name: str) -> str:
        """Determine visibility of an element.

        Args:
            name: Element name

        Returns:
            "public" or "private"
        """
        return "private" if name.startswith("_") else "public"

    def _is_constant(self, name: str) -> bool:
        """Check if name looks like a constant.

        Args:
            name: Variable name

        Returns:
            True if name is all uppercase
        """
        return name.isupper() and not name.startswith("_")

    def _extract_summary(self, docstring: str | None) -> str | None:
        """Extract first paragraph from docstring.

        Args:
            docstring: Full docstring

        Returns:
            First paragraph or None
        """
        if not docstring:
            return None

        lines = docstring.strip().split("\n")
        summary_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped and summary_lines:
                break
            if stripped:
                summary_lines.append(stripped)

        return " ".join(summary_lines) if summary_lines else None

    def _clean_type_hint(self, annotation: Any) -> str:
        """Clean type hint for better readability in documentation.

        Extracts actual types from typing.Annotated and formats them cleanly.
        Removes verbose module prefixes and uses modern type syntax.

        Args:
            annotation: Type annotation object from inspect

        Returns:
            Cleaned string representation of the type

        Examples:
            typing.Annotated[Optional[Path], metadata] -> Path | None
            typing.Optional[list[str]] -> list[str] | None
            pathlib.Path -> Path
        """
        import typing

        # Handle typing.Annotated - extract just the first argument (the actual type)
        if hasattr(typing, 'get_origin') and hasattr(typing, 'get_args'):
            origin = typing.get_origin(annotation)
            if origin is typing.Annotated:
                # Get the actual type (first argument of Annotated)
                args = typing.get_args(annotation)
                if args:
                    annotation = args[0]

        # Convert to string
        type_str = str(annotation)

        # Clean up common verbose patterns
        type_str = type_str.replace('typing.', '')
        type_str = type_str.replace('pathlib.', '')

        # Handle <class 'inspect._empty'> and similar
        if type_str.startswith("<class '") and type_str.endswith("'>"):
            # Extract just the class name
            match = re.match(r"<class '(?:\w+\.)*(\w+)'>", type_str)
            if match:
                type_str = match.group(1)

        # Convert Optional[X] to X | None (modern syntax)
        optional_match = re.match(r'Optional\[(.+)\]$', type_str)
        if optional_match:
            inner_type = optional_match.group(1)
            type_str = f'{inner_type} | None'

        # Convert Union[X, None] to X | None
        union_none_match = re.match(r'Union\[(.+), None\]$', type_str)
        if union_none_match:
            inner_type = union_none_match.group(1)
            type_str = f'{inner_type} | None'

        return type_str

    def _parse_function(self, func: pdoc.doc.Function) -> ParsedFunction:
        """Parse function/method from pdoc.

        Args:
            func: pdoc Function object

        Returns:
            ParsedFunction
        """
        parameters = []
        if func.signature:
            sig = inspect.signature(func.obj)
            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue

                type_hint = None
                if param.annotation != inspect.Parameter.empty:
                    type_hint = self._clean_type_hint(param.annotation)

                default = None
                if param.default != inspect.Parameter.empty:
                    default = repr(param.default)

                parameters.append(Parameter(
                    name=param_name,
                    type_hint=type_hint,
                    default_value=default,
                ))

        return_type = None
        if func.signature:
            sig = inspect.signature(func.obj)
            if sig.return_annotation != inspect.Signature.empty:
                return_type = self._clean_type_hint(sig.return_annotation)

        return ParsedFunction(
            name=func.name,
            signature=str(func.signature) if func.signature else f"{func.name}()",
            visibility=self._get_visibility(func.name),
            docstring=func.docstring,
            docstring_summary=self._extract_summary(func.docstring),
            parameters=parameters,
            return_type=return_type,
            is_async=inspect.iscoroutinefunction(func.obj),
        )

    def _parse_class(self, cls: pdoc.doc.Class) -> ParsedClass:
        """Parse class from pdoc.

        Args:
            cls: pdoc Class object

        Returns:
            ParsedClass
        """
        methods = []
        attributes = []

        for name, member in cls.members.items():
            if not self._should_include(name):
                continue

            if isinstance(member, pdoc.doc.Function):
                methods.append(self._parse_function(member))
            elif isinstance(member, pdoc.doc.Variable):
                attributes.append(self._parse_attribute(member))

        base_classes = []
        if hasattr(cls.obj, "__bases__"):
            for base in cls.obj.__bases__:
                if base.__name__ != "object":
                    base_classes.append(base.__name__)

        return ParsedClass(
            name=cls.name,
            signature=f"class {cls.name}",
            visibility=self._get_visibility(cls.name),
            docstring=cls.docstring,
            docstring_summary=self._extract_summary(cls.docstring),
            methods=methods,
            attributes=attributes,
            base_classes=base_classes,
        )

    def _parse_attribute(self, var: pdoc.doc.Variable) -> ParsedAttribute:
        """Parse attribute/variable from pdoc.

        Args:
            var: pdoc Variable object

        Returns:
            ParsedAttribute
        """
        type_hint = None
        if var.annotation:
            type_hint = self._clean_type_hint(var.annotation)

        return ParsedAttribute(
            name=var.name,
            signature=f"{var.name}: {type_hint}" if type_hint else var.name,
            visibility=self._get_visibility(var.name),
            docstring=var.docstring,
            docstring_summary=self._extract_summary(var.docstring),
            type_hint=type_hint,
        )

    def _parse_constant(self, var: pdoc.doc.Variable) -> ParsedConstant:
        """Parse constant from pdoc.

        Args:
            var: pdoc Variable object

        Returns:
            ParsedConstant
        """
        type_hint = None
        if var.annotation:
            type_hint = self._clean_type_hint(var.annotation)

        return ParsedConstant(
            name=var.name,
            signature=f"{var.name}: {type_hint}" if type_hint else var.name,
            visibility=self._get_visibility(var.name),
            docstring=var.docstring,
            docstring_summary=self._extract_summary(var.docstring),
            type_hint=type_hint,
        )
