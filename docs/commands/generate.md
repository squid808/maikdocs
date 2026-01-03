← Back to [Documentation Index](../index.md)

# `maikdocs generate`

## Description

Generate documentation from scratch for your entire project or specific targets. This command analyzes source files, extracts structure and docstrings, and creates hierarchical markdown documentation optimized for AI consumption.

Use this for initial documentation generation or when you want to regenerate everything.

## Synopsis

```bash
maikdocs generate [OPTIONS] [TARGET]
```

## Arguments

**`target`** (optional)
- Target file, directory, or leave empty for entire project
- Examples: `src/module.py`, `src/core/`, or omit for full project
- Default: Entire project (from config root)

## Options

**`--recursive, -r` / `--no-recursive, -R`**
- Process directories recursively (default) or only top-level files
- Default: `--recursive` (process all subdirectories)

**`--force, -f`**
- Regenerate all documentation regardless of timestamps
- Normally, generate skips files that haven't changed
- Use when you want a complete rebuild

**`--whatif`**
- Show what would happen without making changes
- Dry-run mode for previewing actions
- Useful for understanding scope before execution

**`--help`**
- Show help message and exit

## Examples

### Example 1: Generate docs for entire project

```bash
maikdocs generate
```

**What it does:** Scans entire project (based on `.maikdocs.yaml`), generates `.maik/PROJECT.md`, directory indexes, and file documentation for all source files.

### Example 2: Generate docs for specific module

```bash
maikdocs generate src/core/
```

**What it does:** Generates documentation only for files in `src/core/` and subdirectories.

### Example 3: Force complete regeneration

```bash
maikdocs generate --force
```

**What it does:** Regenerates all documentation files even if source hasn't changed. Useful after config changes or when troubleshooting.

### Example 4: Preview what will be generated

```bash
maikdocs generate --whatif
```

**What it does:** Shows which files would be documented without creating any .md files. Useful for validating include/exclude patterns.

### Example 5: Generate for single file

```bash
maikdocs generate src/maikdocs/core/config.py
```

**What it does:** Generates documentation only for the specified Python file.

## Related Commands

- [`init`](init.md) - Must run first to create configuration
- [`update`](update.md) - Faster incremental updates for changed files
- [`clean`](clean.md) - Remove generated documentation
- [Usage Patterns](../usage-patterns.md#initial-exploration) - See complete workflow
