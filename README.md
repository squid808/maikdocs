# maikdocs

AI-friendly documentation generator for Python codebases.

## What is maikdocs?

maikdocs (mAIkdocs, get it?) generates structured markdown documentation from source code designed specifically for AI consumption. Unlike traditional documentation tools that create human-readable HTML or PDFs, maikdocs creates a hierarchy of markdown files optimized for AI agents to efficiently understand large codebases.

### Why AI-Optimized Documentation?

When AI agents need to understand a codebase, they face two challenges:
1. **Token limits**: Reading entire source files is expensive and often hits context limits
2. **Finding relevant code**: Navigating large projects to find specific functionality wastes tokens

maikdocs solves this by creating a **hierarchical documentation structure**:
- **PROJECT.md**: High-level overview (what the project does, structure, key modules)
- **index_maik.md**: Directory-level summaries (what's in each module)
- **file_maik.md**: File-level details (classes, functions, signatures)

This allows AI agents to:
- Start with `PROJECT.md` to understand the big picture (cheap)
- Read relevant `index_maik.md` files to find the right module (moderate)
- Only read specific `*_maik.md` files for implementation details (targeted)

### Integration with AI Workflows

maikdocs works best when:
- **Paired with Claude Code skills**: Use custom skills to automatically read relevant maikdocs when working on code
- **Used in prompts**: Instruct agents like "First read .maik/PROJECT.md, then explore relevant modules"
- **Combined with MCP servers**: Future integration will allow seamless codebase exploration
- **Manual AI sessions**: Explicitly tell your AI assistant to use maikdocs files instead of raw source code

By using maikdocs, you can reduce token usage by 70-90% when helping AI understand your codebase, while providing better context through structured summaries.

## What Gets Documented (and What You Need to Provide)

maikdocs automatically extracts documentation from your code, but the quality improves with good practices:

### Automatically Extracted (No User Action Required)
- **Code structure** - Classes, functions, methods, constants
- **Signatures** - Function parameters, type hints, return types
- **Visibility** - Public vs private members (based on naming)
- **File metadata** - Lines of code, last modified timestamps
- **Project structure** - Directory hierarchy, module organization

### Enhanced by Docstrings (Highly Recommended)
- **Module docstrings** - Explain what each file does (first line used in summaries)
- **Class docstrings** - Describe the class purpose
- **Function docstrings** - Explain what functions do (first paragraph extracted)

**Example:**
```python
"""Configuration management for the application.

This module handles loading, validating, and saving configuration
from YAML files using Pydantic models.
"""

class Config:
    """Application configuration with validation.

    Loads settings from .config.yaml and validates all required fields.
    """
    def load(self, path: Path) -> None:
        """Load configuration from YAML file.

        Args:
            path: Path to configuration file
        """
```

### Optional User-Provided Context
- **`.maik_meta.md` files** - Add custom descriptions for directories/modules
- Place in any directory alongside source files
- maikdocs merges this content into `index_maik.md`
- Useful for architectural notes, module purposes, design decisions

**Example** - `src/core/.maik_meta.md`:
```markdown
## Core Module

This module contains the fundamental building blocks of the application.
All other modules depend on the abstractions defined here.

**Design principle:** Keep this module dependency-free to maintain
a clean architecture.
```

### What Happens When Documentation is Missing?

| Missing Element | Result |
|----------------|---------|
| No module docstring | File listed without description in index |
| No function docstring | Function signature shown, no explanation |
| No `.maik_meta.md` | Index contains only file listings |
| No type hints | Shows as `typing.Any` or no type info |

**Use `maikdocs coverage`** to find missing documentation and improve your docs!

## Current Language Support:

- Python (via [`pdoc`](https://github.com/mitmproxy/pdoc/))

## Features

- **Smart incremental updates**: Only regenerates docs when source files change
- **Bottom-up architecture**: Files → directory indexes → project structure
- **AI-optimized format**: Structured markdown with standard headers for easy section extraction
- **State tracking**: Maintains metadata to detect changes and orphaned files
- **Visibility control**: Filter public/private members
- **Configurable**: YAML-based configuration with sensible defaults

## Installation

### From Source

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/yourusername/maikdocs.git
   cd maikdocs
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```

4. **Verify installation:**
   ```bash
   maikdocs --help
   ```

### System Requirements

- Python 3.12 or higher
- pip (Python package manager)
- Git (for installation from source)

## Quick Start

**Start in your Python project's root directory** (where your `src/` or main package folder is located):

```bash
# 1. Navigate to your project root
cd /path/to/your/python/project

# 2. Initialize maikdocs (creates .maikdocs.yaml)
maikdocs init --language python

# 3. Generate documentation for the entire project
maikdocs generate

# 4. After making code changes, update incrementally
maikdocs update

# 5. Clean up orphaned documentation files
maikdocs clean
```

**Where to start reading the generated docs:**
1. `.maik/PROJECT.md` - High-level project overview
2. `.maik/src/yourpackage/index_maik.md` - Module summaries
3. `.maik/src/yourpackage/file_maik.md` - Specific file details

## Documentation Structure

maikdocs creates a `.maik/` folder that mirrors your source structure:

```
project/
├── src/
│   └── mypackage/
│       ├── module.py
│       └── subpackage/
│           └── other.py
└── .maik/
    └── src/
        └── mypackage/
            ├── module_maik.md       # Documentation for module.py
            ├── index_maik.md        # Directory index
            └── subpackage/
                ├── other_maik.md
                └── index_maik.md
```

## Generated Documentation Format

Each file gets a markdown doc with:
- Module docstring summary
- Public exports list
- Classes with methods and attributes
- Functions with parameters and return types
- Constants and module attributes
- Visibility markers (PUBLIC / PRIVATE)

## Commands

### Path Flexibility

maikdocs commands accept both source paths and `.maik/` documentation paths interchangeably. The tool automatically translates between them:

```bash
# Use source file paths (recommended for simplicity)
maikdocs read src/core/config.py

# Or use .maik documentation paths (backwards compatible)
maikdocs read .maik/src/core/config_maik.md

# Folders automatically map to index files
maikdocs read src/core/  # Reads .maik/src/core/index_maik.md
```

This works for any command that accepts file paths, making it easier to work with maikdocs without remembering the `.maik/` structure.

### `maikdocs init`
Initialize configuration in a project directory.

**Options:**
- `--language, -l`: Languages to support (default: python)
- `--output, -o`: Output folder (default: .maik)
- `--force, -f`: Overwrite existing config

### `maikdocs generate [target]`
Generate documentation from scratch.

**Options:**
- `--recursive/--no-recursive`: Process directories recursively (default: true)
- `--force, -f`: Regenerate all regardless of timestamps
- `--whatif`: Show what would happen without making changes

### `maikdocs update [target]`
Incrementally update based on file changes.

**Options:**
- `--keep-orphaned/--remove-orphaned`: Handle orphaned files
- `--whatif`: Dry run mode

### `maikdocs clean`
Clean orphaned documentation files.

**Options:**
- `--all`: Remove all generated documentation
- `--whatif`: Show what would be deleted

### `maikdocs read <file>`
Read documentation file with optional symbol filtering.

Supports both source paths and `.maik/` documentation paths - use whichever is more convenient.

**Options:**
- `--types, -t`: Filter by symbol types (classes, functions, methods, fields, description)

**Examples:**
```bash
# Read documentation using source path (simple!)
maikdocs read src/mypackage/module.py

# Or use .maik path (backwards compatible)
maikdocs read .maik/src/mypackage/module_maik.md

# Read only classes using source path
maikdocs read src/mypackage/module.py --types classes

# Read directory index (folder paths map to index_maik.md)
maikdocs read src/mypackage/
```

### `maikdocs extract --file <file>`
Extract actual source code for specific symbols.

**Options:**
- `--file, -f`: Source file to extract from
- `--sections, -s`: Symbol names to extract

**Example:**
```bash
# Extract specific class code with syntax highlighting
maikdocs extract --file src/mypackage/module.py --sections MyClass
```

### `maikdocs coverage`
Analyze documentation coverage and gaps.

**Options:**
- `--file`: Check specific file
- `--directory, -d`: Check specific directory
- `--output, -o`: Export report to file
- `--noclobber`: Append to output file

**Example:**
```bash
# Check coverage and export report
maikdocs coverage --output coverage_report.md
```

## Configuration

The `.maikdocs.yaml` file controls how documentation is generated. It's created automatically by `maikdocs init`, but you can customize it for your project's needs.

### When to Customize Configuration

**Common use cases:**

1. **Exclude test files or build artifacts:**
   ```yaml
   exclude_patterns:
     - '**/tests/**'
     - '**/test_*.py'
     - '**/__pycache__/**'
     - '**/build/**'
   ```

2. **Include private/internal APIs for complete documentation:**
   ```yaml
   visibility_rules:
     include_private: true  # Document underscore-prefixed members
   ```

3. **Change output folder location:**
   ```yaml
   output_folder: docs/ai  # Use 'docs/ai' instead of '.maik'
   ```

4. **Focus on specific file patterns:**
   ```yaml
   include_patterns:
     - 'src/**/*.py'  # Only document files in src/
     - '!src/**/deprecated/**'  # Exclude deprecated code
   ```

5. **Preserve orphaned documentation (for archived code):**
   ```yaml
   preserve_orphaned: true  # Keep docs even if source file deleted
   ```

### Full Configuration Example

```yaml
# Auto-detected project root (usually don't need to change)
project_root: /path/to/project

# Where to generate documentation
output_folder: .maik

# Naming pattern for generated files
file_pattern: '*_maik.md'

# Which files to document
include_patterns:
  - '*.py'
  - 'src/**/*.py'

# Which files to skip
exclude_patterns:
  - '**/tests/**'
  - '**/test_*.py'
  - '**/__pycache__/**'
  - '**/venv/**'
  - '**/.venv/**'

# Documentation detail level
visibility_rules:
  include_private: false  # Set true to document _private members

# Languages to process (Python only for now)
languages:
  - python

# Orphaned file handling
preserve_orphaned: false  # Auto-remove docs for deleted source files
```

### Why Use Configuration?

- **Team consistency**: Commit `.maikdocs.yaml` to share settings across your team
- **CI/CD integration**: Use in automated pipelines to generate up-to-date docs
- **Large codebases**: Exclude unnecessary files to keep documentation focused
- **Multiple projects**: Different configs for different documentation needs (internal vs public API)

## Example Output

Generated documentation for `src/maikdocs/core/config.py`:

```markdown
# config.py

*Auto-generated by maikdocs on 2025-12-26 16:54:55*

## Module

Configuration management for maikdocs.

**Public exports:** `VisibilityRules`, `MaikDocsConfig`

## Classes

### `MaikDocsConfig`

Inherits from: `BaseModel`

Visibility: PUBLIC

Configuration loaded from .maikdocs.yaml.

**Methods:**
- PUBLIC `load(path: Path) -> MaikDocsConfig`
  - Load configuration from YAML file.
- PUBLIC `save(path: Path) -> None`
  - Save configuration to YAML file.
...
```

## Claude Skill Integration

maikdocs includes a Claude Skill that teaches Claude Code to use maikdocs automatically for efficient codebase navigation.

### What the Skill Does

The skill is located in `.claude/skills/maikdocs/` and automatically:

1. **Checks for documentation before expensive exploration** - If `.maik/` doesn't exist, Claude will generate it first to prevent 40k+ token source file reads
2. **Reads hierarchically** - Starts with PROJECT.md, then indexes, then specific files
3. **Uses filtering** - Reads only classes, functions, or specific symbol types as needed
4. **Extracts targeted code** - Gets specific symbols instead of entire files
5. **Auto-updates after changes** - Runs `maikdocs update` when signatures or symbols change

### Using the Skill

The skill is **model-invoked** (automatic). When you ask Claude to:
- Understand a codebase
- Make changes to code
- Find specific functionality

Claude will automatically use maikdocs to navigate efficiently, saving 70-90% of tokens.

### Manual Commands

You can still run maikdocs commands directly:
```bash
maikdocs generate --force  # Regenerate all docs
maikdocs coverage          # Check documentation gaps
maikdocs clean --all       # Remove all generated docs
```

### Expected Behavior

**Scenario: "Understand this project"**
- Claude checks for `.maik/` directory
- If missing, generates docs first (saves 40k+ tokens)
- Reads `.maik/PROJECT.md` for overview
- Explores modules hierarchically as needed

**Scenario: "Add authentication feature"**
- Claude reads PROJECT.md to understand structure
- Reads relevant index files to find auth module
- Reads specific file docs for patterns
- Extracts code only when implementing
- Runs `maikdocs update` after adding new classes/functions

### Skill Files

- `.claude/skills/maikdocs/SKILL.md` - Main skill definition
- `.claude/skills/maikdocs/reading-strategy.md` - Hierarchical navigation guide
- `.claude/skills/maikdocs/auto-update-workflow.md` - When to update docs
- `.claude/skills/maikdocs/examples.md` - Real-world usage scenarios