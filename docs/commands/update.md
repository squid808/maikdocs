← Back to [Documentation Index](../index.md)

# `maikdocs update`

## Description

Incrementally update documentation based on file changes. This is the recommended command for day-to-day use after initial generation. It only processes files that have changed since the last run, making it much faster than `generate`.

## Synopsis

```bash
maikdocs update [OPTIONS] [TARGET]
```

## Arguments

**`target`** (optional)
- Target file, directory, or leave empty for entire project
- Only changed files within target will be updated
- Default: Entire project

## Options

**`--keep-orphaned` / `--remove-orphaned`**
- Preserve or remove orphaned documentation files
- Orphaned files = documentation exists but source file was deleted
- Default behavior determined by `preserve_orphaned` in config

**`--whatif`**
- Show what would be updated without making changes
- Dry-run mode for previewing actions
- Lists files that would be regenerated

**`--help`**
- Show help message and exit

## Examples

### Example 1: Update entire project

```bash
maikdocs update
```

**What it does:** Checks all source files for changes, regenerates documentation only for modified files, and updates PROJECT.md and relevant index files.

### Example 2: Update specific module

```bash
maikdocs update src/core/
```

**What it does:** Updates documentation only for changed files in `src/core/` directory.

### Example 3: Remove orphaned documentation

```bash
maikdocs update --remove-orphaned
```

**What it does:** Updates changed files and removes documentation for any deleted source files.

### Example 4: Preview updates

```bash
maikdocs update --whatif
```

**What it does:** Shows which files would be regenerated without making changes.

### Example 5: After adding new class

```bash
# You added a new class to src/auth/manager.py
maikdocs update src/auth/manager.py
```

**What it does:** Regenerates documentation for the modified file, updating signatures and docstrings.

## When to Use Update vs Generate

**Use `update` when:**
- ✅ Adding new functions, classes, or methods
- ✅ Changing function signatures or parameters
- ✅ Adding or modifying docstrings
- ✅ Day-to-day development workflow
- ✅ You want fast incremental updates

**Use `generate --force` when:**
- ❌ Configuration file changed significantly
- ❌ Troubleshooting documentation issues
- ❌ First-time setup or complete rebuild needed

**Skip both when:**
- Implementation-only changes (no signature/docstring changes)
- Formatting, comments, or internal logic changes

## Related Commands

- [`generate`](generate.md) - Full documentation generation
- [`clean`](clean.md) - Remove orphaned files separately
- [Usage Patterns](../usage-patterns.md#implementation-workflow) - See when to update docs
