# Auto-Update Workflow

When and how to keep maikdocs synchronized with code changes.

## Update Triggers (Meaningful Changes)

Run `maikdocs update` after changes that affect **public interface or structure**:

### Always Update For

**Signature Changes:**
```python
# Before
def process(data: str) -> bool:

# After - added parameter
def process(data: str, validate: bool = True) -> bool:
```

**New Symbols:**
```python
# Added new class
class DataValidator:
    pass

# Added new function
def validate_input(data: str) -> bool:
    pass
```

**Docstring Updates:**
```python
# Before
def load():
    pass

# After - added docstring
def load():
    """Load configuration from file."""
    pass
```

**Return Type Changes:**
```python
# Before
def get_config() -> dict:

# After
def get_config() -> Config:
```

**New Files:**
- Created new .py file
- Added new module to package

### Never Update For

**Whitespace/Formatting:**
```python
# Whitespace changes
def   foo(  ):  pass  # Don't update

# Formatting changes
def foo():
    pass  # vs same function reformatted
```

**Comments:**
```python
# Added/changed comments
def process(data):
    # This is a comment - doesn't affect docs
    return data.strip()
```

**Implementation Details:**
```python
# Before
def calculate(x):
    return x * 2

# After - implementation changed, signature same
def calculate(x):
    result = x + x  # Different implementation, same interface
    return result
```

**Variable Renames (inside functions):**
```python
# Before
def process(data):
    temp = data.strip()
    return temp

# After - internal variable renamed
def process(data):
    cleaned = data.strip()  # Just renamed temp->cleaned
    return cleaned
```

## Update Commands

### Incremental Update (Recommended)

After making meaningful changes:
```bash
maikdocs update
```

This only regenerates docs for changed files (fast).

### Force Regeneration (Rarely Needed)

If docs seem out of sync:
```bash
maikdocs generate --force
```

This regenerates everything (slow).

### Check Coverage (Optional)

See what's missing docstrings:
```bash
maikdocs coverage
```

## Workflow Examples

### Example 1: Add New Feature

```bash
# 1. Make changes to code
vim src/features/new_feature.py

# Changes made:
# - Added new class NewFeature
# - Added docstrings
# - New file created

# 2. Update docs (meaningful changes)
maikdocs update

# 3. Verify (optional)
maikdocs coverage
```

### Example 2: Refactor Implementation

```bash
# 1. Refactor function internals
vim src/core/processor.py

# Changes made:
# - Rewrote algorithm (same signature)
# - Renamed local variables
# - Added comments

# 2. No update needed (implementation only)
# Skip maikdocs update
```

### Example 3: Update API

```bash
# 1. Change function signature
vim src/api/handlers.py

# Changes made:
# - Added parameter to handle_request()
# - Changed return type
# - Updated docstring

# 2. Update docs (signature changed)
maikdocs update
```

### Example 4: Fix Formatting

```bash
# 1. Run code formatter
black src/

# Changes made:
# - Reformatted all files
# - No signature changes

# 2. No update needed (formatting only)
# Skip maikdocs update
```

## Handling Orphaned Files

When you delete source files, their docs become "orphaned".

**Default behavior:**
```bash
maikdocs update  # Removes orphaned docs automatically
```

**Keep orphaned docs:**
```bash
maikdocs update --keep-orphaned
```

**Clean up later:**
```bash
maikdocs clean  # Remove orphaned docs
maikdocs clean --all  # Remove all generated docs
```

## Update Frequency

**Update immediately after:**
- Adding new public classes/functions
- Changing function signatures
- Adding/updating docstrings
- Creating new files

**Update periodically after:**
- Multiple small changes accumulate
- Before committing to version control
- Before code review

**Never update for:**
- Every save
- Formatting changes
- Internal refactoring
- Comment updates

## Verifying Updates

After running update:

```bash
# Check what was updated
maikdocs update  # Shows "Updated: 3 files, 1 index"

# Verify specific file
maikdocs read .maik/src/feature/new_file_maik.md

# Check coverage
maikdocs coverage
```

## Integration with Git

**Pre-commit hook (optional):**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Update docs for staged Python files
git diff --cached --name-only --diff-filter=ACM | grep '\.py$' && maikdocs update
```

**CI/CD (recommended):**
```yaml
# .github/workflows/docs.yml
- name: Generate docs
  run: |
    maikdocs init
    maikdocs generate
    maikdocs coverage
```

## Decision Matrix

| Change Type | Example | Update? |
|------------|---------|---------|
| New class | `class Foo:` | Yes |
| New function | `def bar():` | Yes |
| Signature change | Add parameter | Yes |
| Return type change | `-> int` to `-> str` | Yes |
| Docstring added | Add `"""docs"""` | Yes |
| New file | Create module.py | Yes |
| Whitespace | Reformat with black | No |
| Comments | `# comment` | No |
| Implementation | Change algorithm | No |
| Variable rename | `temp` to `result` | No |
| Import changes | `import foo` | No |
