← Back to [Documentation Index](../index.md)

# `maikdocs read`

## Description

Read documentation files with optional symbol type filtering. This is the primary command for consuming generated documentation, allowing you to view only specific types of symbols (classes, functions, etc.) instead of entire files.

Supports both source paths and `.maik/` documentation paths for convenience.

## Synopsis

```bash
maikdocs read [OPTIONS] FILE
```

## Arguments

**`file`** (required)
- Documentation file to read
- Accepts source paths: `src/module.py` (automatically maps to `.maik/`)
- Accepts .maik paths: `.maik/src/module_maik.md` (backwards compatible)
- Folder paths map to `index_maik.md`: `src/core/` → `.maik/src/core/index_maik.md`

## Options

**`--types, -t`** `TEXT`
- Filter by symbol types (comma-separated)
- Available types: `description`, `classes`, `functions`, `methods`, `fields`
- Can specify multiple: `--types classes,functions`
- Default: Show all content (no filtering)

**`--help`**
- Show help message and exit

## Examples

### Example 1: Read entire file documentation

```bash
maikdocs read src/core/config.py
```

**What it does:** Displays complete documentation for `config.py` including module description, classes, functions, and fields.

### Example 2: Read only classes

```bash
maikdocs read src/core/config.py --types classes
```

**What it does:** Shows only class definitions, methods, and attributes. Filters out module-level functions and description.

### Example 3: Read only functions

```bash
maikdocs read src/utils/helpers.py --types functions
```

**What it does:** Shows only module-level functions, excluding classes and module description.

### Example 4: Read module description only

```bash
maikdocs read src/parsers/python_parser.py --types description
```

**What it does:** Shows only the module docstring summary, useful for quick overview.

### Example 5: Multiple symbol types

```bash
maikdocs read src/core/orchestrator.py --types classes,functions
```

**What it does:** Shows both classes and functions, excluding only the module description and fields.

### Example 6: Read directory index

```bash
maikdocs read src/core/
```

**What it does:** Displays the index file for the `src/core/` directory, showing all modules and their summaries.

### Example 7: Using .maik path directly

```bash
maikdocs read .maik/src/core/config_maik.md --types classes
```

**What it does:** Same as Example 2, but using the documentation path directly (backwards compatible).

## Symbol Type Reference

| Type | Description | Includes |
|------|-------------|----------|
| `description` | Module-level docstring and overview | File purpose, exports list |
| `classes` | Class definitions | Methods, properties, inheritance |
| `functions` | Module-level functions | Parameters, return types, docstrings |
| `methods` | Class methods | Included when `classes` is specified |
| `fields` | Module and class attributes | Constants, class variables |

## Related Commands

- [`extract`](extract.md) - Extract actual source code instead of documentation
- [Piping & Workflows](../piping.md) - Advanced filtering and shell integration
- [Usage Patterns](../usage-patterns.md) - See `read` in context of exploration workflows
