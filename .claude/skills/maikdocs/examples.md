# Usage Examples

Real-world scenarios for using maikdocs efficiently.

## Scenario 1: Understand New Codebase

**Task:** User asks "What does this project do?"

**Without maikdocs (expensive):**
```
1. Read src/__init__.py (500 tokens)
2. Read src/main.py (1200 tokens)
3. Read src/core/app.py (1500 tokens)
4. Read src/utils/helpers.py (800 tokens)
Total: 4000 tokens
```

**With maikdocs (efficient):**
```
1. Check for .maik/ directory
   - If missing: maikdocs init && maikdocs generate

2. Read .maik/PROJECT.md (60 tokens)
   - Project overview
   - Module structure
   - Key components

3. Read .maik/src/index_maik.md (25 tokens)
   - Module summaries

4. Answer user based on overview
Total: 85 tokens (98% reduction)
```

## Scenario 2: Find Authentication Logic

**Task:** User asks "How does authentication work?"

**Workflow:**
```bash
# 1. Read project overview
Read .maik/PROJECT.md
# Find: Authentication handled in src/auth module

# 2. Read auth module index
Read .maik/src/auth/index_maik.md
# Find: authenticator.py, tokens.py, validators.py

# 3. Read authenticator docs
maikdocs read .maik/src/auth/authenticator_maik.md --types classes
# See: AuthManager class with verify_credentials() method

# 4. Extract specific code (if needed)
maikdocs extract --file src/auth/authenticator.py --sections AuthManager
```

**Token cost:** ~150 tokens (vs 3000+ reading source files)

## Scenario 3: Add New Feature

**Task:** Add a new data export feature

**Workflow:**
```bash
# 1. Understand existing structure
Read .maik/PROJECT.md  # Where does export logic go?
Read .maik/src/exporters/index_maik.md  # What exporters exist?

# 2. Check existing patterns
maikdocs read .maik/src/exporters/csv_exporter_maik.md --types classes
# See: BaseExporter class structure

# 3. Extract base class if needed
maikdocs extract --file src/exporters/base.py --sections BaseExporter

# 4. Create new file
vim src/exporters/json_exporter.py
# Implement JsonExporter(BaseExporter)

# 5. Update docs (new file created)
maikdocs update

# 6. Verify
maikdocs read .maik/src/exporters/json_exporter_maik.md
```

## Scenario 4: Fix a Bug

**Task:** Fix error in user validation

**Workflow:**
```bash
# 1. Locate validation code
Read .maik/PROJECT.md  # Find validation module
Read .maik/src/validators/index_maik.md  # Find user_validator.py

# 2. Read function signatures
maikdocs read .maik/src/validators/user_validator_maik.md --types functions
# Find: validate_email(email: str) -> bool

# 3. Extract specific function
maikdocs extract --file src/validators/user_validator.py --sections validate_email

# 4. Fix the bug
vim src/validators/user_validator.py
# Fix implementation (no signature change)

# 5. No update needed (implementation only)
# Skip maikdocs update
```

## Scenario 5: Refactor Module

**Task:** Refactor configuration system

**Workflow:**
```bash
# 1. Understand current structure
Read .maik/src/core/config_maik.md --types classes
# See: Config class with load() and save() methods

# 2. Extract code
maikdocs extract --file src/core/config.py --sections Config

# 3. Refactor
vim src/core/config.py
# Changes:
# - Split Config into ConfigLoader and ConfigValidator
# - Add new methods
# - Update docstrings

# 4. Update docs (signatures changed, new classes)
maikdocs update

# 5. Verify changes
maikdocs read .maik/src/core/config_maik.md --types classes
```

## Scenario 6: Code Review

**Task:** Review pull request changes

**Workflow:**
```bash
# 1. See what changed
git diff main...feature-branch --name-only
# Files: src/api/handlers.py, src/models/user.py

# 2. Check old structure
maikdocs read .maik/src/api/handlers_maik.md --types functions
maikdocs read .maik/src/models/user_maik.md --types classes

# 3. Review changes in context
Read source files knowing structure

# 4. After merge, update docs
maikdocs update
```

## Scenario 7: Debug Performance Issue

**Task:** Optimize slow database queries

**Workflow:**
```bash
# 1. Find database code
Read .maik/PROJECT.md  # Locate database module
Read .maik/src/database/index_maik.md

# 2. Identify query methods
maikdocs read .maik/src/database/queries_maik.md --types functions
# Find: get_user_data(), fetch_orders(), etc.

# 3. Extract specific method
maikdocs extract --file src/database/queries.py --sections get_user_data

# 4. Optimize implementation
vim src/database/queries.py
# Optimize query (no signature change)

# 5. No update needed (implementation only)
# Skip maikdocs update
```

## Scenario 8: Document Coverage Check

**Task:** Ensure good documentation before release

**Workflow:**
```bash
# 1. Check current coverage
maikdocs coverage

# Output:
# Missing docstrings:
# - src/utils/helpers.py:process_data (function)
# - src/models/user.py:UserProfile (class)

# 2. Add docstrings
vim src/utils/helpers.py
vim src/models/user.py

# 3. Update docs (docstrings added)
maikdocs update

# 4. Verify coverage
maikdocs coverage
# 100% coverage
```

## Scenario 9: Multi-File Feature

**Task:** Add user notification system

**Workflow:**
```bash
# 1. Plan structure (check existing patterns)
Read .maik/PROJECT.md
Read .maik/src/index_maik.md

# 2. Create files
vim src/notifications/__init__.py
vim src/notifications/email.py
vim src/notifications/sms.py
vim src/notifications/manager.py

# 3. Generate docs for new module
maikdocs update

# 4. Verify structure
Read .maik/src/notifications/index_maik.md
maikdocs read .maik/src/notifications/manager_maik.md --types classes
```

## Scenario 10: Explore Large Codebase

**Task:** Understand unfamiliar 100-file project

**Workflow:**
```bash
# 1. Generate docs first (CRITICAL)
maikdocs init
maikdocs generate
# Prevents reading 100+ source files (50k+ tokens)

# 2. Start with overview
Read .maik/PROJECT.md
# Understand: 10 main modules, 25 key classes

# 3. Explore by module
Read .maik/src/core/index_maik.md
Read .maik/src/api/index_maik.md
Read .maik/src/database/index_maik.md

# 4. Dive into specifics as needed
maikdocs read .maik/src/core/orchestrator_maik.md --types classes

# 5. Extract code only when implementing
maikdocs extract --file src/core/orchestrator.py --sections Orchestrator
```

**Token savings:** 200-300 tokens (overview) vs 50,000+ tokens (reading all source files)

## Quick Reference

**First time with a project:**
```bash
maikdocs init && maikdocs generate
Read .maik/PROJECT.md
```

**Understanding specific module:**
```bash
Read .maik/{path}/index_maik.md
maikdocs read .maik/{path}/file_maik.md --types classes,functions
```

**Finding functionality:**
```bash
Read .maik/PROJECT.md  # Identify module
Read .maik/{module}/index_maik.md  # Identify file
maikdocs read .maik/{module}/file_maik.md --types {type}
```

**Getting implementation:**
```bash
maikdocs extract --file {source} --sections {symbol}
```

**After making changes:**
```bash
maikdocs update  # If signatures/symbols changed
# Skip if only implementation changed
```

**Check documentation quality:**
```bash
maikdocs coverage
```
