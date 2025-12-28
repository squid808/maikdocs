← Back to [Documentation Index](../index.md)

# `maikdocs clean`

## Description

Clean orphaned or all documentation files. Orphaned files are documentation pages that exist but whose source files have been deleted. This command helps maintain a clean documentation directory.

## Synopsis

```bash
maikdocs clean [OPTIONS]
```

## Arguments

None.

## Options

**`--all`**
- Remove **all** generated documentation and state
- Deletes the entire output folder (`.maik/` by default)
- Use when you want a completely fresh start

**`--whatif`**
- Show what would be deleted without removing files
- Dry-run mode for previewing deletions
- Lists all files that would be removed

**`--help`**
- Show help message and exit

## Examples

### Example 1: Clean orphaned files

```bash
maikdocs clean
```

**What it does:** Removes only documentation files whose source no longer exists. Preserves all valid documentation.

### Example 2: Preview what will be cleaned

```bash
maikdocs clean --whatif
```

**What it does:** Lists orphaned files that would be removed without actually deleting them.

### Example 3: Remove all documentation

```bash
maikdocs clean --all
```

**What it does:** Deletes the entire `.maik/` folder and all generated documentation. Useful before regenerating everything or when archiving a project.

### Example 4: Preview complete removal

```bash
maikdocs clean --all --whatif
```

**What it does:** Shows all files that would be deleted if using `--all`, without removing anything.

### Example 5: Workflow after refactoring

```bash
# After moving/deleting many source files
maikdocs clean --whatif          # Preview orphaned docs
maikdocs clean                   # Remove them
maikdocs update                  # Update remaining docs
```

**What it does:** Complete cleanup workflow after major code reorganization.

## When to Use Clean

**Use `clean` when:**
- Source files have been deleted or moved
- Refactoring changed project structure
- Documentation directory has old/stale files
- Preparing to regenerate everything

**Use `clean --all` when:**
- Starting completely fresh
- Troubleshooting documentation issues
- Archiving or removing maikdocs from project
- Switching to different output folder

**Avoid when:**
- Just updating code (use `update` instead)
- Unsure about orphaned files (use `--whatif` first)

## Related Commands

- [`update`](update.md) - Can also remove orphaned files with `--remove-orphaned`
- [`generate`](generate.md) - Regenerate after cleaning with `--all`
- [Usage Patterns](../usage-patterns.md) - See clean in context of workflows
