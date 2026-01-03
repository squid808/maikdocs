← Back to [Documentation Index](../index.md)

# `maikdocs init`

## Description

Initialize maikdocs in a project directory by creating a `.maikdocs.yaml` configuration file with sensible defaults. This is the first step when setting up maikdocs for any codebase.

## Synopsis

```bash
maikdocs init [OPTIONS] [DIRECTORY]
```

## Arguments

**`directory`** (optional)
- Project root directory where configuration will be created
- Defaults to current directory if omitted

## Options

**`--language, -l`** `TEXT`
- Programming language(s) to document
- Can be specified multiple times for multi-language projects
- Default: `python`
- Example: `-l python -l javascript`

**`--output, -o`** `TEXT`
- Output folder for generated documentation
- Default: `.maik`

**`--force, -f`**
- Overwrite existing `.maikdocs.yaml` configuration if present
- Without this flag, init will fail if config already exists

**`--help`**
- Show help message and exit

## Examples

### Example 1: Initialize in current directory

```bash
maikdocs init --language python
```

**What it does:** Creates `.maikdocs.yaml` in the current directory with Python language configuration.

### Example 2: Initialize in specific directory

```bash
maikdocs init /path/to/project --language python
```

**What it does:** Creates configuration in the specified project directory.

### Example 3: Multi-language project

```bash
maikdocs init --language python --language javascript
```

**What it does:** Sets up configuration for documenting both Python and JavaScript files.

### Example 4: Custom output folder

```bash
maikdocs init --language python --output docs/ai
```

**What it does:** Creates configuration that generates documentation in `docs/ai/` instead of `.maik/`.

### Example 5: Overwrite existing config

```bash
maikdocs init --language python --force
```

**What it does:** Replaces existing `.maikdocs.yaml` with fresh defaults.

## Related Commands

- [`generate`](generate.md) - Next step after init: generate documentation
- See [Installation Guide](../installation.md) for complete setup workflow
