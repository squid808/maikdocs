---
name: maikdocs
description: FIRST STEP for codebase exploration - Use maikdocs to understand, navigate, find, and locate code BEFORE reading source files. Automatically generates hierarchical docs (PROJECT.md, index files, file summaries) saving 70-90% tokens. Essential when exploring, understanding structure, finding functions/classes, or locating code. Check maikdocs before using Read/Grep/Glob on source files. Prevents 40k+ token waste.
allowed-tools: Bash(maikdocs:*), Bash(.venv/bin/maikdocs:*), Read, Glob, Grep
---

# maikdocs Skill

Efficient codebase understanding using AI-optimized documentation.

## ⚠️ MANDATORY: Use Maikdocs BEFORE Reading Source Files

**STOP** before reading source files during exploration or code discovery.

**DO NOT use these tools on source files during exploration:**
- Read tool on .py/.js/.ts/.java files (costs 1000-2000 tokens each)
- Grep to search for functions/classes in code (maikdocs has this info)
- Glob followed by reading multiple files (use maikdocs hierarchy instead)

**ALWAYS use maikdocs first:**
1. Check if `.maik/` exists
2. If missing: `maikdocs init && maikdocs generate` (one-time setup)
3. Read PROJECT.md for overview (40-80 tokens)
4. Read index files for module navigation (20-40 tokens each)
5. Read file docs with --types filter (50-150 tokens)
6. Only then extract specific code or read targeted source files if needed

**Token comparison:**
- Reading 10 source files: 15,000 tokens
- Using maikdocs: 235 tokens (98% savings)

## When Should I Use Maikdocs?

```
Are you trying to:
- Understand a codebase?
- Find where code is located?
- Explore project structure?
- Locate specific functions/classes?
- Learn what modules do?

    ↓ YES to any? → USE MAIKDOCS FIRST

Does .maik/ directory exist?
├─ NO → Run: maikdocs init && maikdocs generate (saves 40k+ tokens!)
└─ YES → Follow hierarchy:
          1. Read .maik/PROJECT.md
          2. Read .maik/{module}/index_maik.md
          3. maikdocs read {file} --types classes,functions
          4. Only if needed: maikdocs extract or Read source

After using maikdocs, still need implementation details?
├─ YES → Use `maikdocs extract --file X --sections Y`
│        OR read specific source file (now you know which one!)
└─ NO → You're done! Proceed with task using info from maikdocs
```

## ⚠️ MANDATORY FIRST STEP: Check for .maik/ Directory

**BEFORE** reading source files, using Grep/Glob on code, or exploring:

1. Check if `.maik/` directory exists: `ls -la .maik/`
2. If missing:
   - STOP immediately
   - Inform user: "Generating maikdocs to save 40k+ tokens..."
   - Run: `maikdocs init && maikdocs generate`
   - Wait for completion
3. If exists, proceed with hierarchical reading

**This single step prevents:**
- Reading 20-50 source files individually (30k-50k tokens)
- Using Grep across entire codebase (expensive)
- Navigating blindly without structure map

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
