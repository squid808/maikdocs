← Back to [Documentation Index](index.md)

# Piping & Advanced Workflows

Advanced command-line usage, piping, and shell integration for power users.

## Path Flexibility

maikdocs accepts both source paths and `.maik/` documentation paths interchangeably, automatically translating between them.

### Source Paths (Recommended)

```bash
# Read using source file path
maikdocs read src/core/config.py

# Folder paths map to index files
maikdocs read src/core/  # → .maik/src/core/index_maik.md

# Works for all path-accepting commands
maikdocs extract --file src/utils/helpers.py --sections format_text
```

**Why use source paths:**
- ✅ Simpler - use the paths you already know
- ✅ Clearer - matches your mental model
- ✅ IDE-friendly - can copy paths from file explorer

### .maik Paths (Backwards Compatible)

```bash
# Read using documentation path
maikdocs read .maik/src/core/config_maik.md

# Extract still uses source paths
maikdocs extract --file src/core/config.py --sections MaikDocsConfig
```

**When to use .maik paths:**
- ✅ Backwards compatibility with older scripts
- ✅ Explicit documentation file references
- ✅ Shell completion on .maik/ directory

---

## Filtering Output

### Single Type Filter

```bash
# Read only classes
maikdocs read src/file.py --types classes

# Read only functions
maikdocs read src/file.py --types functions

# Read only module description
maikdocs read src/file.py --types description
```

### Multiple Type Filters

```bash
# Read classes and functions (exclude description)
maikdocs read src/file.py --types classes,functions

# Read description and classes only
maikdocs read src/file.py --types description,classes
```

### Available Symbol Types

| Type | Shows |
|------|-------|
| `description` | Module docstring, exports list |
| `classes` | Class definitions, methods, properties |
| `functions` | Module-level functions |
| `methods` | Included automatically with `classes` |
| `fields` | Module constants, class attributes |

---

## Combining with Shell Tools

### Grep Integration

```bash
# Find all classes named "Manager"
maikdocs read src/ | grep -A 5 "class.*Manager"

# Find functions with "validate" in name
maikdocs read src/validators/ --types functions | grep "validate"

# Count number of classes in a module
maikdocs read src/models/ --types classes | grep -c "^### "
```

### Finding Missing Documentation

```bash
# Find all missing docstrings
maikdocs coverage | grep "Missing"

# Export to file for review
maikdocs coverage | grep "Missing" > missing_docs.txt

# Count missing items
maikdocs coverage | grep -c "Missing docstring"
```

### Processing Multiple Files

```bash
# Extract multiple classes from different files
for file in src/models/*.py; do
    echo "=== $file ==="
    maikdocs read "$file" --types classes
done

# Extract all test files
for class in TestAuth TestConfig TestParser; do
    maikdocs extract --file src/tests/test_core.py --sections $class
done
```

---

## Output Redirection

### Save Documentation to Files

```bash
# Save module overview
maikdocs read src/core/ > docs/core_overview.md

# Save all class signatures
maikdocs read src/models/ --types classes > docs/data_models.md

# Append to existing file
maikdocs read src/utils/ --types functions >> docs/utilities.md
```

### Generate Reports

```bash
# Full coverage report
maikdocs coverage --output coverage_report.md

# Append multiple modules to one report
maikdocs coverage --directory src/core/ --output full_report.md
maikdocs coverage --directory src/parsers/ --output full_report.md --noclobber
maikdocs coverage --directory src/generators/ --output full_report.md --noclobber
```

---

## Whatif (Dry Run) Mode

Preview changes before executing them.

```bash
# See what would be generated
maikdocs generate --whatif

# See what would be updated
maikdocs update --whatif

# See what would be cleaned
maikdocs clean --whatif
maikdocs clean --all --whatif
```

**Use cases:**
- ✅ Validating include/exclude patterns
- ✅ Checking impact before regeneration
- ✅ Understanding orphaned files
- ✅ CI/CD verification steps

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/docs.yml
name: Update Documentation

on:
  push:
    branches: [main]
    paths:
      - 'src/**/*.py'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install maikdocs
        run: |
          pip install -e .

      - name: Update documentation
        run: |
          maikdocs update

      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .maik/
          git diff --quiet && git diff --staged --quiet || \
            git commit -m "docs: update maikdocs [skip ci]"
          git push
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Update maikdocs before commit
maikdocs update --whatif
if [ $? -ne 0 ]; then
    echo "Running maikdocs update..."
    maikdocs update
    git add .maik/
fi
```

### Verification in CI

```bash
# Fail CI if docs are out of date
maikdocs update --whatif
if [ $? -ne 0 ]; then
    echo "❌ Documentation is out of date!"
    echo "Run 'maikdocs update' and commit the changes."
    exit 1
fi

echo "✅ Documentation is up to date"
```

---

## Shell Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Quick maikdocs commands
alias mdocs='maikdocs'
alias mdocs-gen='maikdocs generate'
alias mdocs-up='maikdocs update'
alias mdocs-cov='maikdocs coverage'
alias mdocs-read='maikdocs read'

# Read project overview
alias mdocs-overview='cat .maik/PROJECT.md'

# Check coverage and show missing
alias mdocs-missing='maikdocs coverage | grep Missing'
```

---

## Advanced Filtering Examples

### Find All Async Functions

```bash
# Read all functions, grep for async
maikdocs read src/ --types functions | grep "async def"
```

### List All Public Classes

```bash
# Read classes, filter by PUBLIC visibility
maikdocs read src/ --types classes | grep "Visibility: PUBLIC" -B 2
```

### Extract Multiple Related Symbols

```bash
# Extract all parser classes
maikdocs extract -f src/parsers/python_parser.py -s PythonParser
maikdocs extract -f src/parsers/base.py -s LanguageParser,ParsedModule
```

---

## Batch Operations

### Document Multiple Projects

```bash
#!/bin/bash
# update_all_docs.sh

PROJECTS=(
    "/path/to/project1"
    "/path/to/project2"
    "/path/to/project3"
)

for project in "${PROJECTS[@]}"; do
    echo "Updating $project..."
    cd "$project"
    maikdocs update
    echo "✅ $project updated"
done
```

### Generate Coverage Reports for All Modules

```bash
#!/bin/bash
# coverage_all.sh

# Clear old report
> coverage_full.md

# Generate for each module
for dir in src/*/; do
    module=$(basename "$dir")
    echo "## $module" >> coverage_full.md
    maikdocs coverage --directory "$dir" --output coverage_full.md --noclobber
    echo "" >> coverage_full.md
done

echo "Coverage report generated: coverage_full.md"
```

---

## Tips & Tricks

### 1. Quick Class Lookup

```bash
# Find where a class is defined
grep -r "class YourClass" src/
# Then read its documentation
maikdocs read src/path/file.py --types classes | grep -A 10 "YourClass"
```

### 2. Compare Before/After

```bash
# Before changes
maikdocs read src/core/config.py --types classes > before.md

# Make changes to code

# After changes
maikdocs update
maikdocs read src/core/config.py --types classes > after.md

# Compare
diff before.md after.md
```

### 3. Monitor Documentation Quality

```bash
# Track coverage over time
echo "$(date): $(maikdocs coverage | grep -c 'Missing')" >> coverage_history.txt
```

---

← Back to [Documentation Index](index.md)
