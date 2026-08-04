# Visual Recursion

> ⚠️ **Work in Progress** - This project is currently under active development

A framework for modeling, visualizing, and optimizing recursive algorithms through tree structures.

## Overview

Visual Recursion provides two complementary approaches to working with recursive algorithms:

1. **RecursionLibrary (Python)**: A template-based system for visualizing recursive algorithms as tree structures
2. **Compiler (JavaScript)**: A high-performance compiler that transforms recursive specifications into optimized native code

## Architecture

### RecursionLibrary (`recursionlibrary/`)

The core Python library provides `appendChilds()`, a powerful function that builds tree representations of recursive algorithms. It's designed for visualization and understanding, supporting:

- **Tree-based visualization** of recursive calls
- **Example nodes** for intuitive algorithm modeling
- **Delta functions** that specify how parameters change between recursive calls
- **Flexible callbacks** for assignment, combination, and result handling

**Example** (Python):
```python
from recursionlibrary import appendChilds

def fak(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1]
    
    def untilCallback(node):
        return [node['value'] >= 2, 1]
    
    def combineCallback(node):
        return node['value'] * node['childs'][0]['value']
    
    return appendChilds([n], delta, untilCallback=untilCallback, 
                       combineCallback=combineCallback)
```

**Limitation**: The tree-building approach has performance overhead due to list structure creation.

---

### Compiler (`compiler/`)

The compiler solves the performance issue by transforming high-level recursive specifications into optimized native code. It's especially effective for mathematical functions (factorial, fibonacci, etc.) where the tree structure is purely for visualization.

#### How it Works

1. **Specification**: Define recursion using a declarative DSL with marker-based expressions
2. **Transformation**: The compiler transforms markers (`#node.value#`, `#node.children[i].value#`) into efficient code
3. **Code Generation**: Produces clean, native recursive functions with optimal performance

**Example** (JavaScript):
```javascript
import RecursionLibrary from './compiler/recursion-library.js'

function fak(n) {
    return {
        delta: function (node) {
            return ['#node.value# - 1']
        },
        
        combine: function (node) {
            return '#node.value# * #node.children[0].value#'
        },
        
        until: function (node) {
            return { 
                condition: '#node.value# === 1', 
                result: '1' 
            }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(fak)
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
```

**Generated Output**:
```javascript
function fak(n) {
    if (n === 1) {
        return 1
    }

    const deltaed = [fak(n - 1)]

    const combined = n * deltaed[0]

    return combined
}
```

---

## Marker Syntax

The compiler uses special markers to identify transformation points:

- `#node.value#` → Replaced with the function parameter (e.g., `n`)
- `#node.children[i].value#` → Replaced with `deltaed[i]` (recursive call results)

**Why markers?**  
Markers provide robust, unambiguous identification of transformation points without complex AST parsing.

---

## Project Structure

```
VisualRecursion/
├── recursionlibrary/          # Python template library
│   ├── recursionlibrary.py   # Core appendChilds function
│   ├── demos/                 # Example implementations
│   └── compiler/              # Legacy compiler experiments
│
├── compiler/                  # JavaScript compiler
│   ├── recursion-library.js  # Main compiler implementation
│   └── demos/                 # Example recursive functions
│       └── fak.js            # Factorial example
│
└── v2/                        # Development/experimentation
    └── recursion-library.js  # Compiler development version
```

---

## Use Cases

### When to use RecursionLibrary (Python):
- Visualizing recursive algorithms for education
- Prototyping and understanding recursive behavior
- Building tree-based representations for analysis
- Cases where performance is not critical

### When to use the Compiler (JavaScript):
- Production code requiring optimal performance
- Mathematical recursive functions (factorial, fibonacci, etc.)
- When tree structure is only needed for specification, not runtime
- Generating clean, maintainable recursive functions

---

## Future Development

### Planned Features:
1. **WYSIWYG Editor**: Visual editor for modeling recursions as tree structures
2. **Pattern Recognition**: Automatic delta inference from example nodes
3. **Multi-language Compilation**: Generate optimized code for Python, JavaScript, and other languages
4. **Abstraction Layers**: Multiple complexity levels of the template system
5. **Performance Benchmarking**: Comparison tools for different approaches

---

## Getting Started

### Python (RecursionLibrary):
```bash
cd recursionlibrary/demos
python fak.py
```

### JavaScript (Compiler):
```bash
cd compiler/demos
node fak.js
```

---

## Philosophy

Visual Recursion bridges the gap between **understanding** and **performance**:

- Use the **template library** to model and understand recursive algorithms
- Use the **compiler** to transform specifications into production-ready code
- The same conceptual model works for both visualization and optimization

This separation allows developers to think at a high level while still achieving native performance.