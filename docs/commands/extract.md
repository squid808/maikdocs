← Back to [Documentation Index](../index.md)

# `maikdocs extract`

## Description

Extract actual source code for specific symbols from a source file. Unlike `read` which shows documentation, `extract` returns the real implementation with syntax highlighting. Use this when you need to see actual code logic, not just signatures and docstrings.

## Synopsis

```bash
maikdocs extract [OPTIONS]
```

## Arguments

None (uses required options instead).

## Options

**`--file, -f`** `PATH` **(required)**
- Source file to extract from
- Must be a source code file (e.g., `.py`, `.js`), not a `.maik/` documentation file
- Example: `src/core/config.py`

**`--sections, -s`** `TEXT`
- Symbol names to extract (comma-separated)
- Can specify classes, functions, or methods
- Example: `MaikDocsConfig,load_config`

**`--help`**
- Show help message and exit

## Examples

### Example 1: Extract single class

```bash
maikdocs extract --file src/core/config.py --sections MaikDocsConfig
```

**What it does:** Extracts the complete `MaikDocsConfig` class definition with all methods and implementation, displayed with syntax highlighting.

### Example 2: Extract multiple symbols

```bash
maikdocs extract --file src/parsers/python_parser.py --sections PythonParser,extract_docstring
```

**What it does:** Extracts both the `PythonParser` class and `extract_docstring` function from the same file.

### Example 3: Extract function implementation

```bash
maikdocs extract --file src/utils/markdown.py --sections format_code_block
```

**What it does:** Shows the complete implementation of the `format_code_block` function with syntax highlighting.

### Example 4: Using with short flags

```bash
maikdocs extract -f src/core/orchestrator.py -s Orchestrator
```

**What it does:** Same as Example 1, using abbreviated option flags.

## Read vs Extract

**When to use `read`:**
- Understanding structure and architecture
- Finding available classes/functions
- Checking signatures and parameters
- Reading docstrings and API docs
- Saving tokens (documentation is much shorter)

**When to use `extract`:**
- Need to see actual implementation logic
- Understanding algorithms or complex code
- Debugging specific behavior
- Copying code patterns
- After using `read` to identify the right symbol

## Typical Workflow

```bash
# 1. Find what exists
maikdocs read src/core/ --types classes

# 2. Read signatures
maikdocs read src/core/orchestrator.py --types classes

# 3. Extract implementation when needed
maikdocs extract -f src/core/orchestrator.py -s Orchestrator
```

## Related Commands

- [`read`](read.md) - Read documentation instead of source code
- [Usage Patterns](../usage-patterns.md#finding-specific-code) - See extract in context
- [Examples](../examples.md) - Real-world usage scenarios
