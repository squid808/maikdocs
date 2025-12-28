← Back to [Documentation Index](index.md)

# Installation Guide

Complete guide for installing maikdocs CLI tool and Claude Code Skill integration.

## CLI Installation

### From Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/maikdocs.git
   cd maikdocs
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```

4. **Verify installation:**
   ```bash
   maikdocs --help
   ```

   You should see the main help message listing all available commands.

### System Requirements

- **Python**: 3.12 or higher
- **pip**: Python package manager (usually included with Python)
- **Git**: For cloning the repository

### Troubleshooting

**Issue: `maikdocs: command not found`**
- Ensure virtual environment is activated
- Check that `.venv/bin` (or `.venv/Scripts` on Windows) is in your PATH
- Try running with full path: `.venv/bin/maikdocs --help`

**Issue: `ModuleNotFoundError: No module named 'maikdocs'`**
- Ensure you ran `pip install -e .` from the maikdocs project root
- Check that you're in the correct virtual environment

**Issue: Python version too old**
- maikdocs requires Python 3.12+
- Check version: `python --version`
- Install newer Python from [python.org](https://www.python.org/)

---

## Claude Code Skill Installation

### What the Skill Does

The maikdocs Claude Code Skill teaches Claude to automatically use maikdocs for efficient codebase navigation, providing:

1. **Automatic documentation checking** - Generates `.maik/` before expensive source file reads
2. **Hierarchical reading** - Starts with PROJECT.md, then indexes, then specific files
3. **Smart filtering** - Reads only relevant symbol types (classes, functions, etc.)
4. **Targeted extraction** - Gets specific code instead of entire files
5. **Token optimization** - Saves 70-90% tokens during codebase exploration

**Expected behavior:**
- **Scenario: "Understand this codebase"**
  - Claude checks for `.maik/`, generates if missing (saves 40k+ tokens)
  - Reads PROJECT.md for overview
  - Explores modules hierarchically

- **Scenario: "Add new feature"**
  - Reads PROJECT.md to understand structure
  - Finds relevant modules via index files
  - Reads specific file docs for patterns
  - Extracts code only when implementing
  - Runs `maikdocs update` after adding classes/functions

### Setup Steps

1. **Install CLI** (see above)
   - The skill requires the maikdocs CLI to be available

2. **Skill auto-discovery**
   - If you're in the maikdocs project directory, the skill is already available at `.claude/skills/maikdocs/`
   - Claude Code automatically discovers skills in `.claude/skills/` folders

3. **Verify skill is active**
   - Start a new conversation in Claude Code
   - Ask: "explore this codebase"
   - Claude should invoke the maikdocs skill automatically

4. **Test the workflow**
   ```bash
   # In a test project
   cd /path/to/test/project
   # Ask Claude: "understand this codebase"
   # Claude should:
   # 1. Check for .maik/
   # 2. Run maikdocs init && maikdocs generate
   # 3. Read .maik/PROJECT.md
   ```

### Skill Files Location

The skill consists of multiple files in `.claude/skills/maikdocs/`:

- **`SKILL.md`** - Main skill definition and instructions
- **`reading-strategy.md`** - Hierarchical navigation guide
- **`auto-update-workflow.md`** - When to update documentation
- **`examples.md`** - Real-world usage scenarios

### Using in Other Projects

To use the maikdocs skill in your own projects:

**Option 1: Project-specific (recommended)**
```bash
# In your project
mkdir -p .claude/skills
cp -r /path/to/maikdocs/.claude/skills/maikdocs .claude/skills/
```

**Option 2: Global Claude setting**
- Configure Claude Code to look for skills in the maikdocs directory
- See Claude Code documentation for global skill configuration

### Manual Commands

You can still run maikdocs commands directly when needed:

```bash
# Force regenerate all docs
maikdocs generate --force

# Check documentation coverage
maikdocs coverage

# Clean all generated docs
maikdocs clean --all
```

**When to use manual commands:**
- Troubleshooting documentation issues
- Running coverage checks
- Forcing complete regeneration
- CI/CD pipelines (automated workflows)

---

## Next Steps

After installation:

1. **Initialize your first project:**
   ```bash
   cd /path/to/your/project
   maikdocs init --language python
   maikdocs generate
   ```

2. **Explore the generated docs:**
   ```bash
   cat .maik/PROJECT.md
   ```

3. **Learn usage patterns:**
   - Read [Usage Patterns](usage-patterns.md) for workflows
   - See [Examples](examples.md) for real-world scenarios

4. **Integrate with Claude:**
   - Test skill invocation with "understand this codebase"
   - Experience 70-90% token savings during exploration

---

← Back to [Documentation Index](index.md)
