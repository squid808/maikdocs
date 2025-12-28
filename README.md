<div align="center">
  <img src="assets/maikdocs_logo.png" alt="maikdocs logo" width="400">
  <h3>AI-friendly documentation generator for multi-language codebases</h3>
</div>

## What is maikdocs?

maikdocs generates hierarchical markdown documentation optimized for AI consumption. Instead of reading entire source files (expensive for tokens), AI agents can navigate structured docs:

- **PROJECT.md** - High-level overview (what the project does, structure, key modules)
- **index_maik.md** - Directory-level summaries (what's in each module)
- **file_maik.md** - File-level details (classes, functions, signatures)

**Result:** 70-90% token reduction for AI codebase exploration.

## Why Use It?

**For AI Agents:**
- Start with overview, drill down as needed
- Structured format for easy parsing
- Token-efficient navigation (200-500 tokens vs 15,000+)

**For Humans:**
- Quick project understanding
- Documentation as code
- Multi-language support (architecture ready for expansion)

## Quick Start

```bash
cd /path/to/your/project
maikdocs init --language python
maikdocs generate
cat .maik/PROJECT.md  # Start here!
```

**Next steps:** See [Usage Patterns](docs/usage-patterns.md) for effective workflows.

## CLI Commands

All commands support `--help` for details. See [full command reference](docs/index.md#cli-commands).

| Command | Description |
|---------|-------------|
| **`init`** | Initialize configuration in project |
| **`generate`** | Generate all documentation from scratch |
| **`update`** | Incrementally update changed files |
| **`clean`** | Remove orphaned documentation |
| **`read`** | Read docs with optional filtering (`--types`) |
| **`extract`** | Extract source code for specific symbols |
| **`coverage`** | Analyze documentation gaps |

**Command documentation:** [init](docs/commands/init.md) · [generate](docs/commands/generate.md) · [update](docs/commands/update.md) · [clean](docs/commands/clean.md) · [read](docs/commands/read.md) · [extract](docs/commands/extract.md) · [coverage](docs/commands/coverage.md)

## Installation

### CLI Tool

```bash
git clone https://github.com/yourusername/maikdocs.git
cd maikdocs
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
maikdocs --help
```

**Requirements:** Python 3.12+, pip, git

**Full guide:** [Installation Documentation](docs/installation.md)

### Claude Code Skill

The skill in `.claude/skills/maikdocs/` teaches Claude to use maikdocs automatically during codebase exploration, saving 70-90% tokens.

**Setup:** [Installation > Claude Skill](docs/installation.md#claude-code-skill-installation)

## Examples

### Explore New Codebase

```bash
maikdocs generate
cat .maik/PROJECT.md
maikdocs read src/module/ --types classes
```

### Find Specific Code

```bash
cat .maik/PROJECT.md  # Identify relevant module
maikdocs read src/auth/authenticator.py --types classes
maikdocs extract --file src/auth/authenticator.py --sections AuthManager
```

**More examples:** [Real-World Examples](docs/examples.md) · [Usage Patterns](docs/usage-patterns.md)

## Language Support

**Currently supported:** Python (via [pdoc](https://github.com/mitmproxy/pdoc/))

**Multi-language ready:** Language-agnostic architecture with auto-discovery. Adding new languages requires only implementing a parser class (~100-200 lines).

**Learn more:** [Adding Language Support](docs/adding-languages.md)

## Documentation Structure

```
.maik/
├── PROJECT.md              # High-level overview
└── src/
    └── mypackage/
        ├── index_maik.md        # Module index
        ├── module_maik.md       # File documentation
        └── subpackage/
            └── ...
```

## Configuration

Created by `maikdocs init` as `.maikdocs.yaml`.

**Common customizations:**
- Exclude test files: `exclude_patterns: ['**/tests/**']`
- Include private members: `visibility_rules: {include_private: true}`
- Custom output folder: `output_folder: docs/ai`
- Multi-language: `languages: [python, javascript]`

**Example:**
```yaml
languages: [python]
exclude_patterns:
  - '**/tests/**'
  - '**/__pycache__/**'
visibility_rules:
  include_private: false
```

## Documentation

📚 **[Full Documentation](docs/index.md)**

**Getting Started:**
- [Installation Guide](docs/installation.md) - CLI + Skill setup
- [Usage Patterns](docs/usage-patterns.md) - Effective workflows
- [Examples](docs/examples.md) - Real-world scenarios

**Reference:**
- [Command Reference](docs/index.md#cli-commands) - All CLI commands
- [Piping & Workflows](docs/piping.md) - Advanced usage
- [Adding Languages](docs/adding-languages.md) - Implement parsers

## Features

- ✅ **Multi-language architecture** - Auto-discovery, generic data model, abstract generators
- ✅ **Smart incremental updates** - Only regenerates changed files
- ✅ **AI-optimized format** - Structured markdown with standard headers
- ✅ **Visibility control** - Filter public/private members
- ✅ **State tracking** - Detects changes and orphaned files
- ✅ **Path flexibility** - Use source paths or .maik paths interchangeably
- ✅ **Claude Code Skill** - Automatic AI integration

## License

[MIT License](LICENSE)

## Contributing

Contributions welcome! Especially language parser implementations.

**To add a language:**
1. Open an issue describing the language
2. Discuss AST library and challenges
3. Implement parser (see [guide](docs/adding-languages.md))
4. Add tests
5. Submit PR

**Priority languages:** JavaScript/TypeScript, Java, Go, Rust, C#

---

**Built for AI, useful for humans.**
