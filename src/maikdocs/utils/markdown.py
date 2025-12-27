"""Markdown parsing and manipulation utilities."""

import re
from pathlib import Path


class MarkdownSectionParser:
    """Parse markdown into navigable sections."""

    def parse_sections(self, md_path: Path) -> dict[str, str]:
        """Extract sections by header.

        Args:
            md_path: Path to markdown file

        Returns:
            Dictionary mapping section names to content
        """
        if not md_path.exists():
            return {}

        sections = {}
        current_section = None
        current_content = []

        for line in md_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = line[3:].strip()
                current_content = [line]
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content)

        return sections

    def extract_section(self, md_path: Path, section_name: str) -> str | None:
        """Extract single section without parsing entire file.

        Args:
            md_path: Path to markdown file
            section_name: Name of section to extract

        Returns:
            Section content or None if not found
        """
        if not md_path.exists():
            return None

        content = md_path.read_text(encoding="utf-8")
        pattern = rf"(## {re.escape(section_name)}.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else None

    def extract_symbol_types(
        self,
        md_path: Path,
        symbol_types: list[str]
    ) -> dict[str, str]:
        """Extract specific symbol types from documentation.

        Args:
            md_path: Path to markdown file
            symbol_types: Types to extract (classes, functions, constants, etc.)

        Returns:
            Dictionary of extracted sections
        """
        type_mapping = {
            "class": "Classes",
            "classes": "Classes",
            "function": "Functions",
            "functions": "Functions",
            "method": "Functions",
            "methods": "Functions",
            "constant": "Constants",
            "constants": "Constants",
            "field": "Module Attributes",
            "fields": "Module Attributes",
            "attribute": "Module Attributes",
            "attributes": "Module Attributes",
            "description": "Module",
            "module": "Module",
        }

        sections = self.parse_sections(md_path)
        result = {}

        for sym_type in symbol_types:
            section_name = type_mapping.get(sym_type.lower())
            if section_name and section_name in sections:
                result[section_name] = sections[section_name]

        return result

    def extract_symbols_by_name(
        self,
        md_path: Path,
        symbol_names: list[str]
    ) -> dict[str, str]:
        """Extract specific symbols by name from documentation.

        Args:
            md_path: Path to markdown file
            symbol_names: Names of symbols to extract

        Returns:
            Dictionary mapping symbol names to their content
        """
        if not md_path.exists():
            return {}

        content = md_path.read_text(encoding="utf-8")
        result = {}

        for name in symbol_names:
            pattern = rf"(### .*`{re.escape(name)}`.*?)(?=\n### |\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                result[name] = match.group(1).strip()

        return result


class CodeExtractor:
    """Extract code sections from source files."""

    def extract_by_symbols(
        self,
        source_path: Path,
        symbol_names: list[str]
    ) -> dict[str, str]:
        """Extract code for specific symbols from source file.

        Args:
            source_path: Path to source file
            symbol_names: Names of symbols to extract

        Returns:
            Dictionary mapping symbol names to their code
        """
        if not source_path.exists():
            return {}

        content = source_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        result = {}

        for name in symbol_names:
            code = self._extract_symbol(lines, name)
            if code:
                result[name] = code

        return result

    def _extract_symbol(self, lines: list[str], symbol_name: str) -> str | None:
        """Extract a single symbol from source lines.

        Args:
            lines: Source file lines
            symbol_name: Name of symbol to extract

        Returns:
            Symbol code or None if not found
        """
        # Pattern for class or function definition
        class_pattern = rf"^class\s+{re.escape(symbol_name)}\s*[\(:]"
        func_pattern = rf"^(?:async\s+)?def\s+{re.escape(symbol_name)}\s*\("

        start_idx = None
        indent_level = None

        for i, line in enumerate(lines):
            if re.match(class_pattern, line.strip()) or re.match(func_pattern, line.strip()):
                start_idx = i
                indent_level = len(line) - len(line.lstrip())
                break

        if start_idx is None:
            return None

        # Extract until we hit same or lower indentation level
        extracted = [lines[start_idx]]
        for i in range(start_idx + 1, len(lines)):
            line = lines[i]

            # Skip empty lines
            if not line.strip():
                extracted.append(line)
                continue

            # Check indentation
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level and line.strip():
                break

            extracted.append(line)

        return "\n".join(extracted)

    def extract_imports(self, source_path: Path) -> str:
        """Extract import statements from source file.

        Args:
            source_path: Path to source file

        Returns:
            All import statements
        """
        if not source_path.exists():
            return ""

        lines = source_path.read_text(encoding="utf-8").splitlines()
        imports = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                imports.append(line)
            elif imports and not stripped:
                continue
            elif imports:
                break

        return "\n".join(imports)
