---
name: maikdocs
description: Uses maikdocs CLI Python tool for rapid, low-token codebase understanding and navigation. Generates docs before expensive code exploration, reads hierarchical documentation to save tokens, and auto-updates docs when code changes. Use when exploring codebases, making changes, or understanding project structure.
allowed-tools: Bash(maikdocs:*), Bash(.venv/bin/maikdocs:*), Read, Glob, Grep
---

# maikdocs Skill

Efficient codebase understanding using AI-optimized documentation.

## Critical Pre-Generation Check

**BEFORE any expensive code navigation** (reading multiple source files):

1. Check if `.maik/` directory exists
2. If missing:
   - STOP immediately
   - Inform user: "Generating maikdocs first to save tokens..."
   - Run: `maikdocs init && maikdocs generate`
   - Wait for completion before proceeding
3. If exists, proceed with hierarchical reading strategy

This prevents 40k+ token source file reads.

## Hierarchical Reading Strategy

Always navigate top-down through the documentation hierarchy:

1. **Start with PROJECT.md** - High-level overview
   - Read `.maik/PROJECT.md` for project structure and key modules
   - Understand what the project does and how it's organized

2. **Read relevant index files** - Module context
   - Read `.maik/{path}/index_maik.md` for directory summaries
   - Or use source path: `maikdocs read {path}/` (automatically reads index)
   - Identify which files contain the functionality you need

3. **Read specific file docs** - Implementation details
   - Use source paths: `maikdocs read {src_file}.py --types classes,functions`
   - Or .maik paths: `maikdocs read .maik/{path}/file_maik.md`
   - Source paths are simpler and recommended!

4. **Extract code only when needed** - Actual implementation
   - Use `maikdocs extract --file {src} --sections {symbol}` for specific code
   - Avoid reading entire source files

## Auto-Update Workflow

Run `maikdocs update` after making **meaningful changes** to source files:

**Update for:**
- Signature changes (parameters, return types)
- New symbols (classes, functions, methods)
- Docstring additions or updates
- New files created
- Return type modifications

**Do NOT update for:**
- Whitespace or formatting changes
- Comment-only changes
- Implementation details (inside function bodies)
- Variable renames within functions

**Commands:**
```bash
# After meaningful changes
maikdocs update

# Verify coverage (optional)
maikdocs coverage
```

## Common Commands

```bash
# Initialize in new project
maikdocs init --language python

# Generate all docs (first time)
maikdocs generate

# Update after changes (incremental)
maikdocs update

# Read filtered docs (supports both source and .maik paths)
maikdocs read src/core/config.py --types classes
# or: maikdocs read .maik/src/core/config_maik.md --types classes

# Extract specific code
maikdocs extract --file src/core/config.py --sections MaikDocsConfig

# Check documentation gaps
maikdocs coverage
```

## Token Optimization

**Without maikdocs:**
- Read 10 source files x 200 lines = 2000 lines
- Cost: ~1500 tokens per file = 15,000 tokens

**With maikdocs:**
- Read PROJECT.md (50 lines) = 40 tokens
- Read 2 index files (30 lines each) = 50 tokens
- Read 2 file docs (80 lines each) = 120 tokens
- Extract 1 function (30 lines) = 25 tokens
- **Total: ~235 tokens (98% reduction)**

## Usage Examples

**Understand new codebase:**
```
1. Check for .maik/ (ask to generate if missing)
2. Read .maik/PROJECT.md
3. Read relevant directories: maikdocs read src/module/
4. Read specific files: maikdocs read src/module/file.py
5. Extract code only when implementing
```

**Make changes to existing code:**
```
1. Use maikdocs to locate the right file (avoid source file reads)
2. Read docs using source path: maikdocs read src/file.py
3. Extract specific symbols if needed
4. Make changes
5. Run maikdocs update if signatures/symbols changed
```

**Find specific functionality:**
```
1. Read PROJECT.md to identify relevant module
2. Read module: maikdocs read src/module/
3. Read specific file with --types filter: maikdocs read src/file.py --types classes
4. Extract code when implementation details needed
```
