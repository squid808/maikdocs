← Back to [Documentation Index](index.md)

# Adding Language Support

Guide for implementing parser support for new programming languages.

## Overview

maikdocs is built with a **language-agnostic architecture** designed for easy expansion. Adding a new language requires implementing a single parser class - the rest of the infrastructure automatically handles it.

### Architecture Benefits

- **Auto-discovery**: Parsers are automatically discovered via Python's module system - no hardcoded language lists
- **Generic data model**: Symbol types and modifiers work across all languages
- **Abstract generators**: Documentation rendering has zero language-specific logic
- **Plugin-ready**: Drop in a new `{language}_parser.py` file and it's automatically available

---

## What You Need to Implement

**Only one component:** A language parser class

**What you DON'T need to implement:**
- ❌ Documentation generators (already abstract)
- ❌ Configuration changes (accepts any language string)
- ❌ Orchestration logic (automatically discovers parsers)
- ❌ File tracking (language-agnostic)

---

## Quick Start: Adding a New Language

### Step 1: Create Parser File

Create `src/maikdocs/parsers/{language}_parser.py`

**Example:** For JavaScript, create `javascript_parser.py`

### Step 2: Implement LanguageParser Interface

```python
from pathlib import Path
from maikdocs.core.config import VisibilityRules
from maikdocs.parsers.base import LanguageParser, ParsedModule

class JavaScriptParser(LanguageParser):
    """Parser for JavaScript source files."""

    def __init__(self, visibility_rules: VisibilityRules):
        self.visibility_rules = visibility_rules

    def supports_file(self, path: Path) -> bool:
        """Declare which file extensions this parser handles."""
        return path.suffix in ['.js', '.mjs', '.cjs']

    def parse(self, source_path: Path) -> ParsedModule:
        """Parse JavaScript file and return structured data.

        Args:
            source_path: Path to .js file

        Returns:
            ParsedModule with extracted structure
        """
        # 1. Use language-specific AST parser (e.g., Babel for JS)
        # 2. Extract classes, functions, exports, etc.
        # 3. Map to maikdocs data structures
        # 4. Return ParsedModule
```

### Step 3: That's It!

The parser is automatically discovered and registered when maikdocs starts.

---

## Generic Data Model

All parsers return the same data structures defined in `src/maikdocs/parsers/base.py`.

### ParsedModule

```python
@dataclass
class ParsedModule:
    """Container for parsed module information."""

    file_path: Path                      # Source file path
    module_docstring: str | None         # Module-level documentation
    module_summary: str | None           # First line of docstring
    exports: list[str]                   # Public API exports
    classes: list[ParsedClass]           # Class definitions
    functions: list[ParsedFunction]      # Module-level functions
    constants: list[ParsedConstant]      # Module constants

    # Generic metadata
    container_type: str = "module"       # "module", "package", "namespace", "crate"
    container_name: str | None = None    # e.g., "com.example.app", "std::io"
```

### ParsedClass

```python
@dataclass
class ParsedClass:
    """Parsed class/interface/trait information."""

    name: str
    signature: str
    visibility: str = "public"
    docstring: str | None = None
    docstring_summary: str | None = None
    bases: list[str] = field(default_factory=list)
    methods: list[ParsedFunction] = field(default_factory=list)
    properties: list[ParsedConstant] = field(default_factory=list)

    # Generic metadata (language-agnostic)
    symbol_type: str = "class"           # "class", "interface", "trait", "enum", "struct"
    modifiers: list[str] = field(default_factory=list)  # ["abstract", "final", "sealed", etc.]
    parent_name: str | None = None       # For nested classes
    nesting_level: int = 0
```

### ParsedFunction

```python
@dataclass
class ParsedFunction:
    """Parsed function/method information."""

    name: str
    signature: str
    visibility: str = "public"
    docstring: str | None = None
    docstring_summary: str | None = None

    # Generic metadata
    symbol_type: str = "function"        # "function", "method", "constructor", "property"
    modifiers: list[str] = field(default_factory=list)  # ["static", "async", "readonly", etc.]
    parent_name: str | None = None
    nesting_level: int = 0
```

---

## Mapping Language Features

### Symbol Types

Use the appropriate symbol type for your language's constructs:

**Classes/Types:**
- `"class"` - Standard class (Python, Java, C++)
- `"interface"` - Interface (Java, TypeScript, Go)
- `"trait"` - Trait (Rust, Scala)
- `"protocol"` - Protocol (Swift)
- `"enum"` - Enumeration (many languages)
- `"struct"` - Structure (C, Go, Rust)

**Functions:**
- `"function"` - Module/free function
- `"method"` - Class method
- `"constructor"` - Constructor/initializer
- `"property"` - Property with getter/setter

**Data:**
- `"constant"` - Module or class constant
- `"attribute"` - Class attribute
- `"field"` - Struct field

### Modifiers

Add as many modifiers as needed from your language:

**Common modifiers:**
- `"static"` - Static member
- `"async"` - Asynchronous function
- `"readonly"` - Read-only property
- `"abstract"` - Abstract class/method
- `"final"` - Final/sealed class
- `"virtual"` - Virtual method
- `"override"` - Overridden method
- `"getter"`, `"setter"` - Property accessors

**Language-specific examples:**
- Python: `"classmethod"`, `"staticmethod"`, `"property"`
- Java: `"synchronized"`, `"transient"`, `"volatile"`
- Rust: `"unsafe"`, `"pub"`, `"const"`

### Visibility

Map your language's visibility levels:

**Common values:**
- `"public"` - Public API
- `"private"` - Internal implementation
- `"protected"` - Subclass accessible
- `"package"` - Package-private (Java)
- `"internal"` - Assembly-internal (C#)

### Container Info

Identify the module/package/namespace system:

```python
# Java package
container_type = "package"
container_name = "com.example.myapp"

# Python module
container_type = "module"
container_name = "myapp.core.config"

# Rust crate
container_type = "crate"
container_name = "std::collections"

# C++ namespace
container_type = "namespace"
container_name = "boost::filesystem"
```

---

## Example Implementations

### Example 1: Java Interface

```python
ParsedClass(
    name="Runnable",
    signature="public interface Runnable",
    symbol_type="interface",  # Not "class"!
    visibility="public",
    modifiers=[],
    methods=[
        ParsedFunction(
            name="run",
            signature="void run()",
            symbol_type="method",
            visibility="public",
            modifiers=["abstract"]
        )
    ]
)
```

**Generated documentation:**
```markdown
### Runnable

**Type:** Interface
**Visibility:** PUBLIC

**Methods:**
- PUBLIC `run() -> void` [abstract]
```

### Example 2: TypeScript Async Static Method

```python
ParsedFunction(
    name="fetchData",
    signature="static async fetchData(url: string): Promise<Data>",
    symbol_type="method",
    visibility="public",
    modifiers=["static", "async"]
)
```

**Generated documentation:**
```markdown
- PUBLIC `fetchData(url: string) -> Promise<Data>` [static, async]
```

### Example 3: Rust Trait

```python
ParsedClass(
    name="Display",
    signature="pub trait Display",
    symbol_type="trait",
    visibility="public",
    modifiers=[],
    methods=[...]
)
```

**Generated documentation:**
```markdown
### Display

**Type:** Trait
**Visibility:** PUBLIC
```

---

## Parser Implementation Tips

### 1. Use Existing AST Libraries

Don't write parsers from scratch. Use battle-tested libraries:

| Language | Recommended Library |
|----------|---------------------|
| JavaScript/TypeScript | [Babel](https://babeljs.io/), [@babel/parser](https://www.npmjs.com/package/@babel/parser) |
| Java | [JavaParser](https://javaparser.org/) |
| Go | [go/ast](https://pkg.go.dev/go/ast) |
| Rust | [syn](https://docs.rs/syn/) |
| C/C++ | [tree-sitter](https://tree-sitter.github.io/tree-sitter/) |
| Multi-language | [tree-sitter](https://tree-sitter.github.io/tree-sitter/) (supports many languages) |

### 2. Extract Container Information

Parse package/module declarations:

```python
# Java
# package com.example.myapp;
container_type = "package"
container_name = "com.example.myapp"

# Python
# No explicit declaration, use file path
container_type = "module"
container_name = "myapp.core.config"  # from src/myapp/core/config.py
```

### 3. Map Visibility Correctly

Each language has different visibility rules:

**Python**: Uses naming convention
```python
def _private_function():  # visibility = "private"
def public_function():    # visibility = "public"
```

**Java**: Four explicit levels
```java
public void method1()     // visibility = "public"
private void method2()    // visibility = "private"
protected void method3()  // visibility = "protected"
void method4()            // visibility = "package"
```

**Rust**: Pub keyword
```rust
pub fn public_fn()        // visibility = "public"
fn private_fn()           // visibility = "private"
```

### 4. Handle Edge Cases

**Nested classes:**
```python
ParsedClass(
    name="InnerClass",
    parent_name="OuterClass",
    nesting_level=1
)
```

**Anonymous functions:**
```python
# Skip anonymous/lambda functions or give them generated names
name = "<lambda_1>"
```

**Generics/Type Parameters:**
```python
# Include in signature, keep name simple
name = "List"
signature = "class List<T>"
```

### 5. Extract Docstrings

Map language-specific documentation formats:

| Language | Doc Format |
|----------|-----------|
| Python | `"""docstring"""` |
| Java | `/** javadoc */` |
| JavaScript | `/** JSDoc */` |
| Rust | `/// doc comment` or `//! module doc` |
| Go | `// comment above declaration` |

---

## Testing Your Parser

### Step 1: Create Test File

Create a sample source file in the target language with various constructs.

### Step 2: Generate Documentation

```bash
# Initialize with your language
maikdocs init --language yourlanguage

# Generate docs for test file
maikdocs generate path/to/test/file.ext
```

### Step 3: Verify Output

```bash
# Read generated documentation
maikdocs read path/to/test/file.ext

# Check that:
# - Classes/interfaces are detected
# - Functions are listed
# - Signatures are correct
# - Visibility is accurate
# - Modifiers appear correctly
```

### Step 4: Check Coverage

```bash
maikdocs coverage --file path/to/test/file.ext

# Should show which symbols lack documentation
```

### Step 5: Extract Code

```bash
maikdocs extract --file path/to/test/file.ext --sections ClassName

# Verify extraction works for symbols
```

---

## Implementation Checklist

- [ ] Create `{language}_parser.py` in `src/maikdocs/parsers/`
- [ ] Implement `LanguageParser` interface
- [ ] Implement `supports_file()` method (file extensions)
- [ ] Implement `parse()` method
- [ ] Use appropriate AST library for parsing
- [ ] Map language constructs to generic data model
- [ ] Set `symbol_type` correctly (class/interface/trait/etc.)
- [ ] Add relevant `modifiers` (static/async/abstract/etc.)
- [ ] Map visibility levels
- [ ] Extract docstrings/comments
- [ ] Handle container info (package/namespace/module)
- [ ] Test with sample files
- [ ] Verify `maikdocs generate` works
- [ ] Verify `maikdocs read` displays correctly
- [ ] Verify `maikdocs extract` works
- [ ] Check `maikdocs coverage` detects missing docs
- [ ] Add unit tests for parser
- [ ] Document language-specific notes

---

## Contributing Your Parser

We welcome language parser contributions!

### Before Implementing

1. **Open an issue** describing the language you want to add
2. **Discuss** the AST library you plan to use
3. **Identify** any language-specific challenges

### Implementation

1. Follow this guide to implement the parser
2. Add tests in `src/tests/test_parsers_{language}.py`
3. Test with real-world codebases in that language

### Submitting

1. **Create PR** with:
   - Parser implementation
   - Tests (minimum 80% coverage)
   - Example usage in PR description
   - List of tested file types/constructs

2. **Documentation** in PR:
   - Which AST library you used
   - Any limitations or known issues
   - Example code patterns that work well

---

## Reference: Python Parser

The Python parser (`src/maikdocs/parsers/python_parser.py`) is a complete reference implementation.

**Read it to see:**
- How to use an AST library (pdoc)
- How to extract docstrings
- How to handle visibility rules
- How to populate all data structures
- Edge cases and error handling

```bash
# Read Python parser implementation
maikdocs extract --file src/maikdocs/parsers/python_parser.py --sections PythonParser
```

---

## Future Languages

Community contributions wanted for:

- **JavaScript/TypeScript** (high priority - huge user base)
- **Java** (enterprise adoption)
- **Go** (growing popularity)
- **Rust** (systems programming)
- **C#** (.NET ecosystem)
- **Ruby** (web development)
- **PHP** (web backends)
- **Kotlin** (Android/JVM)
- **Swift** (iOS/macOS)

Open an issue to claim a language!

---

← Back to [Documentation Index](index.md)
