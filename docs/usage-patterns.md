← Back to [Documentation Index](index.md)

# Usage Patterns

Effective workflows for using maikdocs in different scenarios.

## Initial Exploration

**Goal:** Understand a new codebase quickly

**Workflow:**
1. Generate documentation (one-time):
   ```bash
   maikdocs init --language python
   maikdocs generate
   ```

2. Read project overview:
   ```bash
   cat .maik/PROJECT.md
   ```
   **What you get:** High-level description, main modules, key components

3. Explore module summaries:
   ```bash
   maikdocs read src/
   ```
   **What you get:** All modules with first-line docstring summaries

4. Drill down to specific files:
   ```bash
   maikdocs read src/core/orchestrator.py --types classes
   ```
   **What you get:** Class signatures, methods, parameters

**Token cost:** 150-300 tokens vs 15,000+ reading source files directly

**When to use:** First time seeing a codebase, onboarding, code review

---

## Finding Specific Code

**Goal:** Locate where functionality lives

**Workflow:**
1. Identify the relevant module:
   ```bash
   cat .maik/PROJECT.md
   ```
   Look for keywords like "authentication", "configuration", "database"

2. Find the specific file:
   ```bash
   maikdocs read src/auth/
   ```
   Review index to see which file contains what you need

3. Read targeted documentation:
   ```bash
   maikdocs read src/auth/manager.py --types classes,functions
   ```
   Filter to see only what matters

4. Extract implementation if needed:
   ```bash
   maikdocs extract -f src/auth/manager.py -s AuthManager
   ```

**Example: Finding authentication code**
```bash
# Step 1: Check PROJECT.md - find "auth in src/auth/"
cat .maik/PROJECT.md

# Step 2: Read auth module index
maikdocs read src/auth/

# Step 3: Find AuthManager class
maikdocs read src/auth/manager.py --types classes

# Step 4: Get implementation
maikdocs extract -f src/auth/manager.py -s AuthManager
```

**When to use:** Bug hunting, adding features, understanding specific logic

---

## Implementation Workflow

**Goal:** Add new feature or modify existing code

**Workflow:**

1. **Understand existing structure:**
   ```bash
   maikdocs read src/core/ --types classes
   ```
   See what patterns and abstractions already exist

2. **Read relevant file docs:**
   ```bash
   maikdocs read src/core/base.py
   ```
   Understand base classes or interfaces to extend

3. **Extract code for reference:**
   ```bash
   maikdocs extract -f src/core/base.py -s BaseProcessor
   ```
   Copy patterns and conventions

4. **Make your changes:**
   - Add new classes, functions, or methods
   - Update signatures
   - Add docstrings

5. **Update documentation:**
   ```bash
   maikdocs update
   ```
   Run only if you changed signatures or added new symbols

**When to update docs:**
- **DO update for:**
  - New classes, functions, methods
  - Signature changes (parameters, return types)
  - Docstring additions or modifications
  - New files created

- **DON'T update for:**
  - Implementation-only changes (inside function bodies)
  - Formatting or whitespace
  - Comments (not docstrings)
  - Variable renames within functions

**Example: Adding a new exporter**
```bash
# 1. Understand existing exporters
maikdocs read src/exporters/ --types classes

# 2. See the base pattern
maikdocs extract -f src/exporters/base.py -s BaseExporter

# 3. Create new exporter (src/exporters/json_exporter.py)
vim src/exporters/json_exporter.py

# 4. Update docs (new file with new class)
maikdocs update

# 5. Verify documentation
maikdocs read src/exporters/json_exporter.py
```

---

## Code Review Workflow

**Goal:** Review changes in a pull request

**Workflow:**

1. **Check old structure via maikdocs:**
   ```bash
   maikdocs read src/api/handlers.py --types classes
   maikdocs read src/models/user.py --types classes
   ```
   Understand what existed before changes

2. **Review actual source changes:**
   ```bash
   git diff main...feature-branch src/api/handlers.py
   ```
   See the implementation changes

3. **After merge, update documentation:**
   ```bash
   git checkout main
   git pull
   maikdocs update
   ```

4. **Verify docs updated correctly:**
   ```bash
   maikdocs read src/api/handlers.py
   ```

**When to use:** PR review, post-merge verification, architecture review

---

## Coverage Checking

**Goal:** Ensure good documentation quality

**Workflow:**

1. **Check current coverage:**
   ```bash
   maikdocs coverage
   ```
   Identifies missing docstrings

2. **Target specific areas:**
   ```bash
   maikdocs coverage --directory src/core/
   ```
   Focus on critical modules first

3. **Export for tracking:**
   ```bash
   maikdocs coverage --output coverage_report.md
   ```
   Document gaps for team review

4. **Add missing docstrings:**
   ```python
   def process_data(input: str) -> dict:
       """Process input string and return structured data.

       Args:
           input: Raw input string to process

       Returns:
           Dictionary with processed data
       """
       # implementation...
   ```

5. **Regenerate and verify:**
   ```bash
   maikdocs update
   maikdocs coverage --directory src/core/
   ```

**When to use:** Before releases, documentation sprints, quality checks

---

## Debugging Workflow

**Goal:** Understand code flow to fix a bug

**Workflow:**

1. **Find the entry point:**
   ```bash
   maikdocs read .maik/PROJECT.md
   ```
   Identify which module handles the problematic feature

2. **Trace through call hierarchy:**
   ```bash
   # Find the handler
   maikdocs read src/handlers/ --types functions

   # See what it calls
   maikdocs read src/handlers/request_handler.py

   # Find the service layer
   maikdocs read src/services/data_service.py --types classes
   ```

3. **Extract suspicious code:**
   ```bash
   maikdocs extract -f src/services/data_service.py -s process_request
   ```
   Get actual implementation to debug

4. **After fixing:**
   ```bash
   # If you only changed implementation
   # No need to update docs

   # If you changed signature or added validation
   maikdocs update src/services/data_service.py
   ```

---

## Multi-Language Projects

**Goal:** Document projects with multiple languages

**Setup:**
```bash
maikdocs init --language python --language javascript
```

**Workflow:**
```bash
# Generate for all languages
maikdocs generate

# Language-specific documentation appears in same structure
cat .maik/PROJECT.md  # Shows both Python and JS modules

# Read Python files
maikdocs read src/backend/api.py

# Read JavaScript files
maikdocs read src/frontend/app.js
```

**Note:** Currently only Python is fully supported. JavaScript, TypeScript, and other languages require parser implementation. See [Adding Language Support](adding-languages.md).

---

## CI/CD Integration

**Goal:** Automate documentation generation

**Workflow:**

```bash
# In CI pipeline (e.g., .github/workflows/docs.yml)

# Option 1: Verify docs are up-to-date
maikdocs update --whatif
if [ $? -ne 0 ]; then
    echo "Documentation out of date! Run 'maikdocs update'"
    exit 1
fi

# Option 2: Auto-generate and commit
maikdocs update
if [ -n "$(git status --porcelain .maik/)" ]; then
    git add .maik/
    git commit -m "docs: update maikdocs [skip ci]"
    git push
fi

# Option 3: Generate coverage report for PR
maikdocs coverage --output coverage_report.md
# Upload as CI artifact
```

---

## Quick Reference

| Task | Command |
|------|---------|
| First-time setup | `maikdocs init && maikdocs generate` |
| Read overview | `cat .maik/PROJECT.md` |
| Explore module | `maikdocs read src/module/` |
| Find classes | `maikdocs read src/file.py --types classes` |
| Get implementation | `maikdocs extract -f src/file.py -s ClassName` |
| After code changes | `maikdocs update` |
| Check coverage | `maikdocs coverage` |
| Clean orphaned files | `maikdocs clean` |

---

← Back to [Documentation Index](index.md)
