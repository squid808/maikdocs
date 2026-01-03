← Back to [Documentation Index](index.md)

# Real-World Examples

Practical examples using actual codebases to demonstrate maikdocs workflows.

## Example 1: Human Developer - First Time Using maikdocs

**Scenario:** You clone the maikdocs project and want to understand how it works.

### Before maikdocs

**Traditional approach:**
- Read through 20+ Python files manually
- Grep for class definitions
- Try to piece together architecture
- Jump between files following imports
- **Time:** 2-3 hours
- **Clarity:** Fragmented, incomplete understanding

### With maikdocs

```bash
# 1. Generate docs (one-time, 10 seconds)
cd maikdocs
maikdocs init --language python
maikdocs generate

# 2. Read project overview (2 minutes)
cat .maik/PROJECT.md
```

**What you learn:**
- maikdocs has 4 main modules: core, parsers, generators, cli
- Entry point: `src/maikdocs/cli/app.py`
- Core orchestrator: `src/maikdocs/core/orchestrator.py`
- Architecture: bottom-up (files → indexes → project)

```bash
# 3. Explore core module (1 minute)
maikdocs read src/maikdocs/core/ --types classes
```

**What you learn:**
- `Orchestrator` - Main coordination class
- `MaikDocsConfig` - Configuration management
- `StateTracker` - Tracks file changes
- Each class shows methods and purpose

```bash
# 4. Get specific implementation (30 seconds)
maikdocs extract --file src/maikdocs/core/orchestrator.py --sections Orchestrator
```

**What you get:** Complete implementation with syntax highlighting

**Total time:** 5 minutes
**Clarity:** Complete hierarchical understanding

---

## Example 2: AI Agent - Understanding maikdocs Codebase

**Task:** Claude needs to understand how maikdocs works to help add a new feature.

**Scenario:** Using the actual maikdocs codebase.

### Step 1: Check for Documentation

```bash
ls -la .maik/
```

**Result:** Directory exists! Skip generation, proceed to reading.

### Step 2: Read Project Overview

```bash
cat .maik/PROJECT.md
```

**Claude sees:**
```markdown
# maikdocs

AI-friendly documentation generator...

## Architecture

- **core/** - Orchestration, configuration, state tracking
- **parsers/** - Language-specific code parsing (currently Python via pdoc)
- **generators/** - Markdown documentation generation
- **cli/** - Command-line interface (Typer-based)

## Key Components

- `Orchestrator` (core/orchestrator.py) - Coordinates documentation generation
- `PythonParser` (parsers/python_parser.py) - Extracts structure from Python files
- `FileDocGenerator` (generators/file_doc.py) - Generates file-level documentation
...
```

**Token cost:** ~60 tokens
**Understanding:** Complete project structure, knows where to look

### Step 3: Explore Core Module

```bash
maikdocs read src/maikdocs/core/ --types classes
```

**Claude sees:**
```markdown
## Orchestrator

Main orchestration class for documentation generation.

**Methods:**
- generate_documentation(target: Path | None) -> None
- update_documentation(target: Path | None) -> None
- clean_orphaned_files() -> None
...

## MaikDocsConfig

Configuration model for maikdocs.

**Methods:**
- load(path: Path) -> MaikDocsConfig
- save(path: Path) -> None
...
```

**Token cost:** ~80 tokens
**Understanding:** Core classes and their responsibilities

### Step 4: Read Specific Class

```bash
maikdocs read src/maikdocs/core/orchestrator.py --types classes
```

**Claude sees:** Full `Orchestrator` class with all methods, signatures, parameters, return types

**Token cost:** ~120 tokens
**Understanding:** Complete API surface of Orchestrator

### Summary

**Total token cost:** ~260 tokens
**Comparison:** Reading 10 source files directly = ~15,000 tokens
**Savings:** 98% token reduction!

**What Claude can now do:**
- Answer questions about architecture
- Suggest where to add new features
- Understand data flow
- Only extract specific code when implementing

---

## Example 3: Finding Authentication Code

**Task:** Locate authentication logic in a web application.

### Workflow

```bash
# Step 1: Check PROJECT.md for auth references
cat .maik/PROJECT.md | grep -i auth
```

**Result:** "Authentication handled in `src/auth/` module"

```bash
# Step 2: Explore auth module
maikdocs read src/auth/
```

**Result:**
```markdown
# src/auth/

- authenticator.py - Main authentication manager
- tokens.py - JWT token handling
- validators.py - Credential validation
```

```bash
# Step 3: Read authenticator classes
maikdocs read src/auth/authenticator.py --types classes
```

**Result:**
```markdown
### AuthManager

Main authentication coordinator.

**Methods:**
- verify_credentials(username: str, password: str) -> bool
- generate_token(user_id: int) -> str
- validate_token(token: str) -> dict | None
```

```bash
# Step 4: Extract implementation if needed
maikdocs extract --file src/auth/authenticator.py --sections AuthManager
```

**Total time:** < 1 minute
**Found:** Exact class and methods for authentication

---

## Example 4: Adding New Generator to maikdocs

**Task:** Add a new generator for project statistics.

### Step 1: Understand Existing Generators

```bash
# See what generators exist
maikdocs read src/maikdocs/generators/ --types classes
```

**Result:**
- `ProjectDocGenerator` - Generates PROJECT.md
- `IndexDocGenerator` - Generates index_maik.md files
- `FileDocGenerator` - Generates file-level docs

### Step 2: Study the Base Pattern

```bash
# Read base generator if exists
maikdocs read src/maikdocs/generators/ --types classes | grep -i base

# Read file doc generator as reference
maikdocs read src/maikdocs/generators/file_doc.py --types classes
```

**Result:** See the `FileDocGenerator` class structure:
- Constructor parameters
- `generate()` method signature
- Helper methods

### Step 3: Extract Reference Implementation

```bash
maikdocs extract --file src/maikdocs/generators/file_doc.py --sections FileDocGenerator
```

**Result:** Complete implementation to use as template

### Step 4: Create New Generator

```python
# src/maikdocs/generators/stats_generator.py

class StatsDocGenerator:
    """Generate project statistics documentation."""

    def __init__(self, config: MaikDocsConfig):
        self.config = config

    def generate(self, output_path: Path) -> None:
        """Generate statistics markdown file."""
        # Implementation based on FileDocGenerator pattern
        ...
```

### Step 5: Update Documentation

```bash
# Since we added a new class
maikdocs update
```

### Step 6: Verify

```bash
maikdocs read src/maikdocs/generators/stats_generator.py --types classes
```

---

## Example 5: Debugging Parser Issue

**Task:** Fix a bug where private methods are being included despite config.

### Step 1: Understand Parser Structure

```bash
# Find parser implementation
maikdocs read src/maikdocs/parsers/python_parser.py --types classes
```

**Result:** See `PythonParser` class with methods:
- `parse(source_path: Path) -> ParsedModule`
- `_should_include(element) -> bool`

### Step 2: Extract Suspect Code

```bash
# Get the filtering logic
maikdocs extract --file src/maikdocs/parsers/python_parser.py --sections _should_include
```

**Result:** See actual implementation of visibility filtering

### Step 3: Extract Test to Understand Expected Behavior

```bash
# Find tests
maikdocs read src/tests/test_parsers.py --types functions | grep -i private
```

### Step 4: Fix and Verify

```python
# Fix the bug in src/maikdocs/parsers/python_parser.py
# Update implementation-only, no signature change
```

```bash
# No need to update docs (implementation only)
# Just run tests
pytest src/tests/test_parsers.py
```

---

## Example 6: Documentation Coverage Before Release

**Task:** Ensure 100% documentation coverage before v1.0 release.

### Workflow

```bash
# Step 1: Generate coverage report
maikdocs coverage --output pre_release_coverage.md
```

**Result:**
```
Missing docstrings:
- src/utils/helpers.py (module) - No module docstring
- src/utils/helpers.py:format_text (function) - No docstring
- src/models/user.py:UserProfile.validate (method) - No docstring

Total symbols: 150
Documented: 147
Missing: 3
Coverage: 98%
```

### Step 2: Target Critical Modules

```bash
# Focus on core modules first
maikdocs coverage --directory src/core/
```

**Result:** 100% coverage in core 

```bash
# Check parsers
maikdocs coverage --directory src/parsers/
```

**Result:** 100% coverage in parsers 

### Step 3: Fix Missing Docstrings

```python
# src/utils/helpers.py
"""Utility helper functions for text formatting and processing."""

def format_text(text: str) -> str:
    """Format text by removing extra whitespace and normalizing line endings.

    Args:
        text: Raw input text

    Returns:
        Cleaned and formatted text
    """
    # implementation...
```

### Step 4: Update and Verify

```bash
# Regenerate docs
maikdocs update

# Check coverage again
maikdocs coverage --output post_fix_coverage.md
```

**Result:** 100% coverage! Ready for release.

---

## Example 7: Multi-File Refactoring

**Task:** Split large `config.py` file into `config.py` and `validators.py`.

### Before Refactoring

```bash
# Document current structure
maikdocs read src/core/config.py --types classes > config_before.md
```

### During Refactoring

```bash
# Create new validators.py
vim src/core/validators.py

# Move validation code
# Update imports in config.py
```

### After Refactoring

```bash
# Update documentation
maikdocs update

# Verify new structure
maikdocs read src/core/ --types classes

# Compare
maikdocs read src/core/config.py --types classes > config_after.md
maikdocs read src/core/validators.py --types classes > validators_new.md

diff config_before.md config_after.md
```

**Result:** Clear before/after documentation of architectural change

---

## Example 8: Onboarding New Team Member

**Task:** Help new developer understand maikdocs project quickly.

### Onboarding Doc

```markdown
# maikdocs Onboarding

Welcome! Here's how to get started:

## 1. Generate Documentation (30 seconds)
```bash
maikdocs init && maikdocs generate
```

## 2. Read Overview (5 minutes)
```bash
cat .maik/PROJECT.md
```

## 3. Explore by Interest

**Want to understand CLI?**
```bash
maikdocs read src/maikdocs/cli/app.py --types functions
```

**Want to understand parsing?**
```bash
maikdocs read src/maikdocs/parsers/
maikdocs extract -f src/maikdocs/parsers/python_parser.py -s PythonParser
```

**Want to understand generation?**
```bash
maikdocs read src/maikdocs/generators/ --types classes
```

## 4. Start Contributing
- Pick a GitHub issue
- Use maikdocs to understand relevant code
- Make changes
- Run `maikdocs update` if you changed signatures
- Submit PR
```

**Result:** New developer productive on day one

---

## Summary: Token Savings

| Scenario | Traditional (tokens) | With maikdocs (tokens) | Savings |
|----------|---------------------|------------------------|---------|
| Understand project | 15,000 | 260 | 98% |
| Find authentication | 8,000 | 150 | 98% |
| Add new feature | 12,000 | 400 | 97% |
| Debug parser issue | 5,000 | 200 | 96% |
| Code review | 10,000 | 300 | 97% |

**Average savings: 97-98% token reduction**

---

← Back to [Documentation Index](index.md)
