# Reading Strategy

Efficient hierarchical navigation through maikdocs documentation.

## ❌ Anti-Pattern: Reading Source Files First

**WRONG APPROACH (wastes 15k+ tokens):**
```
User asks: "Find the authentication code"
Claude:
1. Read src/auth/auth.py (1500 tokens)
2. Read src/auth/tokens.py (1200 tokens)
3. Read src/auth/validator.py (1000 tokens)
Total: 3700 tokens, didn't even find the right file yet!
```

**CORRECT APPROACH (uses 150 tokens):**
```
User asks: "Find the authentication code"
Claude:
1. Read .maik/PROJECT.md (60 tokens) → Find: auth in src/auth/
2. Read .maik/src/auth/index_maik.md (30 tokens) → Find: authenticator.py has AuthManager
3. maikdocs read src/auth/authenticator.py --types classes (60 tokens)
Total: 150 tokens, found exact class with all methods!
```

**When it's OK to read source files:**
- After using maikdocs to identify the exact file
- When you need actual implementation logic (not structure)
- For debugging specific code
- User explicitly asks for a specific file

## The Hierarchy

```
.maik/PROJECT.md              # Project overview (50-100 lines)
├── .maik/src/index_maik.md   # Top-level module index (20-40 lines)
│   ├── module1_maik.md       # File-level details (50-150 lines)
│   └── module2_maik.md
└── .maik/src/package/
    ├── index_maik.md         # Package index (20-40 lines)
    ├── file1_maik.md         # File-level details (50-150 lines)
    └── file2_maik.md
```

## Reading Order

### 1. PROJECT.md First (Always)

Read `.maik/PROJECT.md` to understand:
- What the project does
- Main modules and their purposes
- Project structure
- Key entry points

**Token cost:** 40-80 tokens (vs 500+ for reading source files)

### 2. Index Files for Context

Read `.maik/{path}/index_maik.md` to:
- See what files are in a directory
- Read module docstrings (first line summaries)
- Identify public APIs
- Locate relevant files

**Token cost:** 20-40 tokens per index

### 3. File Docs for Details

Read `.maik/{path}/file_maik.md` for:
- Class and function signatures
- Method lists
- Parameter types and return values
- Docstring summaries

**Use filtering:**
```bash
# Only read classes
maikdocs read .maik/src/core/config_maik.md --types classes

# Only read functions
maikdocs read .maik/src/utils/markdown_maik.md --types functions

# Multiple types
maikdocs read .maik/src/cli/app_maik.md --types classes,functions
```

**Token cost:** 50-150 tokens per file (vs 1000-2000 for source)

### 4. Extract Code (When Needed)

Only extract actual source code when:
- Implementing similar functionality
- Understanding complex logic
- Debugging specific issues

```bash
# Extract single symbol
maikdocs extract --file src/core/config.py --sections MaikDocsConfig

# Extract multiple symbols
maikdocs extract --file src/parsers/python_parser.py --sections PythonParser,extract_docstring
```

**Token cost:** 20-100 tokens per symbol (targeted)

## Decision Tree

```
Need to understand codebase?
├── Yes: Read .maik/PROJECT.md
│   └── Need specific module?
│       ├── Yes: Read .maik/{module}/index_maik.md
│       │   └── Need implementation details?
│       │       ├── Yes: Read .maik/{module}/file_maik.md
│       │       │   └── Need actual code?
│       │       │       └── Yes: maikdocs extract
│       │       └── No: Use signatures from file_maik.md
│       └── No: Use PROJECT.md overview
└── No: Proceed with task
```

## Filtering by Symbol Type

Available types:
- `description` - Module docstring and overview
- `classes` - Class definitions and methods
- `functions` - Module-level functions
- `methods` - Class methods (included with classes)
- `fields` - Class attributes and module constants

**Examples:**

```bash
# Architecture overview (classes only)
maikdocs read .maik/src/core/orchestrator_maik.md --types classes

# Public API (functions only)
maikdocs read .maik/src/utils/markdown_maik.md --types functions

# Full module understanding
maikdocs read .maik/src/parsers/base_maik.md --types description,classes
```

## Token Savings Examples

**Scenario: Find authentication configuration**

Without maikdocs (naive approach):
1. Read src/core/config.py (200 lines) = 1500 tokens
2. Read src/core/auth.py (150 lines) = 1200 tokens
3. Read src/core/settings.py (100 lines) = 800 tokens
**Total: 3500 tokens**

With maikdocs (smart approach):
1. Read .maik/PROJECT.md (80 lines) = 60 tokens
2. Read .maik/src/core/index_maik.md (30 lines) = 25 tokens
3. Read .maik/src/core/config_maik.md --types classes (40 lines) = 30 tokens
**Total: 115 tokens (97% reduction)**

**Scenario: Understand class structure**

Without maikdocs:
1. Read entire source file to see class definition
**Cost: 1000-2000 tokens**

With maikdocs:
1. Read file_maik.md --types classes
**Cost: 50-100 tokens (95% reduction)**

## When to Read Source vs Docs

**Read maikdocs when:**
- Understanding structure
- Finding functionality
- Checking signatures
- Exploring unfamiliar code
- Planning changes

**Read source when:**
- Implementing complex logic
- Debugging specific issues
- Understanding algorithms
- After identifying exact location via maikdocs
