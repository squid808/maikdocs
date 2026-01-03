← Back to [Documentation Index](../index.md)

# `maikdocs coverage`

## Description

Analyze documentation coverage and identify missing elements. This command helps you find functions, classes, and modules that lack docstrings, enabling you to improve documentation quality before generating docs for AI consumption.

## Synopsis

```bash
maikdocs coverage [OPTIONS]
```

## Arguments

None (uses options for targeting).

## Options

**`--file`** `PATH`
- Check coverage for a specific file
- Example: `--file src/core/config.py`

**`--directory, -d`** `PATH`
- Check coverage for a specific directory
- Recursively analyzes all source files
- Example: `-d src/core/`

**`--output, -o`** `PATH`
- Write coverage report to file instead of stdout
- Creates markdown formatted report
- Example: `-o coverage_report.md`

**`--noclobber`**
- Append to output file instead of overwriting
- Only applies when `--output` is specified
- Useful for aggregating multiple coverage runs

**`--help`**
- Show help message and exit

## Examples

### Example 1: Check entire project coverage

```bash
maikdocs coverage
```

**What it does:** Analyzes all source files, lists missing docstrings for modules, classes, and functions. Displays results in terminal.

### Example 2: Check specific file

```bash
maikdocs coverage --file src/core/config.py
```

**What it does:** Shows coverage report only for `config.py`, identifying any missing docstrings.

### Example 3: Check specific directory

```bash
maikdocs coverage --directory src/parsers/
```

**What it does:** Analyzes all files in `src/parsers/` recursively, useful for checking coverage of a module.

### Example 4: Export coverage report

```bash
maikdocs coverage --output docs/coverage_report.md
```

**What it does:** Generates a markdown report and saves it to file for documentation or review.

### Example 5: Append to existing report

```bash
maikdocs coverage --directory src/core/ --output report.md --noclobber
maikdocs coverage --directory src/parsers/ --output report.md --noclobber
```

**What it does:** Creates an aggregated report covering multiple directories.

### Example 6: Workflow for improving coverage

```bash
# 1. Check current coverage
maikdocs coverage --output before.md

# 2. Add missing docstrings to your code
vim src/core/config.py

# 3. Verify improvement
maikdocs coverage --output after.md

# 4. Regenerate documentation
maikdocs update
```

**What it does:** Complete workflow for identifying gaps, fixing them, and updating docs.

## Understanding Coverage Output

The coverage report shows:

**Missing Docstrings:**
- Module-level docstrings
- Class docstrings
- Function/method docstrings

**Example Output:**
```
Missing docstrings:
- src/utils/helpers.py (module) - No module docstring
- src/utils/helpers.py:process_data (function) - No docstring
- src/models/user.py:UserProfile (class) - No docstring
- src/models/user.py:UserProfile.validate (method) - No docstring
```

**Coverage Statistics:**
```
Total symbols: 150
Documented: 135
Missing: 15
Coverage: 90%
```

## Why Coverage Matters

**For AI agents:**
- Docstrings become summaries in documentation
- Missing docstrings = functions listed without explanation
- Good coverage = better AI understanding of code purpose

**For humans:**
- Identifies under-documented code
- Improves code maintainability
- Helps onboard new team members

## Related Commands

- [`update`](update.md) - Regenerate docs after adding docstrings
- [Usage Patterns](../usage-patterns.md#coverage-checking) - Complete coverage workflow
