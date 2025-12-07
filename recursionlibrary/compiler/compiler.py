"""
RecursionLibrary Compiler
Compiles .rl files (simplified Python-like syntax) to Python code.
"""

from lark import Lark, Transformer, v_args
from pathlib import Path


# Lark Grammar for the RecursionLibrary Language
GRAMMAR = r"""
    ?start: program

    program: function+

    function: NAME "(" parameters? ")" _NL block "end" _NL*

    parameters: NAME ("," NAME)*

    block: statement+

    ?statement: assignment
              | return_stmt
              | if_stmt
              | while_stmt
              | for_stmt
              | expr_stmt

    assignment: NAME ":=" expr _NL

    return_stmt: "return" expr _NL

    if_stmt: "if" expr _NL block ("else" "if" expr _NL block)* ("else" _NL block)? "end" _NL

    while_stmt: "while" expr _NL block "end" _NL

    for_stmt: "for" NAME "in" expr _NL block "end" _NL

    expr_stmt: expr _NL

    ?expr: logical_or

    ?logical_or: logical_and ("or" logical_and)*

    ?logical_and: comparison ("and" comparison)*

    ?comparison: arith_expr (COMP_OP arith_expr)*

    ?arith_expr: term (ADD_OP term)*

    ?term: factor (MUL_OP factor)*

    ?factor: (ADD_OP | "not") factor
           | power

    ?power: atom ("**" factor)?

    ?atom: NUMBER
         | STRING
         | BOOLEAN
         | NAME
         | list_literal
         | array_literal
         | map_literal
         | dict_access
         | list_access
         | function_call
         | "(" expr ")"

    list_literal: "list" "[" (expr ("," expr)*)? "]"

    array_literal: "array" "[" (expr ("," expr)*)? "]"

    map_literal: "map" "{" (map_pair ("," map_pair)*)? "}"

    map_pair: expr ":" expr

    dict_access: atom "[" expr "]"

    list_access: atom "[" expr "]"

    function_call: NAME "(" arguments? ")"

    arguments: expr ("," expr)*

    COMP_OP: "=" | "!=" | "<" | ">" | "<=" | ">="
    ADD_OP: "+" | "-"
    MUL_OP: "*" | "/" | "//" | "%"

    BOOLEAN: "True" | "False"

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMBER: /[0-9]+\.?[0-9]*/
    STRING: /"([^"\\]|\\.)*"/ | /'([^'\\]|\\.)*'/

    _NL: /\r?\n/+

    %import common.WS_INLINE
    %ignore WS_INLINE
    COMMENT: "#" /[^\n]*/
    %ignore COMMENT
"""


@v_args(inline=True)
class PythonCompiler(Transformer):
    """Transforms the parse tree into Python code."""

    def __init__(self):
        self.indent_level = 0

    def _indent(self):
        return "    " * self.indent_level

    def program(self, *functions):
        return "\n\n".join(functions)

    def function(self, name, params, block):
        params_str = params if params else ""
        self.indent_level = 1
        body = block
        self.indent_level = 0
        return f"def {name}({params_str}):\n{body}"

    def parameters(self, *params):
        return ", ".join(params)

    def block(self, *statements):
        return "".join(statements)

    def assignment(self, name, expr):
        return f"{self._indent()}{name} = {expr}\n"

    def return_stmt(self, expr):
        return f"{self._indent()}return {expr}\n"

    def if_stmt(self, *args):
        # args: condition, block, [else_if_condition, else_if_block]*, [else_block]?
        result = []
        condition = args[0]
        block = args[1]
        
        self.indent_level += 1
        body = block
        self.indent_level -= 1
        
        result.append(f"{self._indent()}if {condition}:\n{body}")
        
        i = 2
        while i < len(args) - 1:
            # Check if this is an else-if pair
            if isinstance(args[i], str) and i + 1 < len(args):
                else_if_cond = args[i]
                self.indent_level += 1
                else_if_body = args[i + 1]
                self.indent_level -= 1
                result.append(f"{self._indent()}elif {else_if_cond}:\n{else_if_body}")
                i += 2
            else:
                break
        
        # Check for else block
        if i < len(args):
            self.indent_level += 1
            else_body = args[i]
            self.indent_level -= 1
            result.append(f"{self._indent()}else:\n{else_body}")
        
        return "".join(result)

    def while_stmt(self, condition, block):
        self.indent_level += 1
        body = block
        self.indent_level -= 1
        return f"{self._indent()}while {condition}:\n{body}"

    def for_stmt(self, var, iterable, block):
        self.indent_level += 1
        body = block
        self.indent_level -= 1
        return f"{self._indent()}for {var} in {iterable}:\n{body}"

    def expr_stmt(self, expr):
        return f"{self._indent()}{expr}\n"

    def logical_or(self, *args):
        return " or ".join(map(str, args))

    def logical_and(self, *args):
        return " and ".join(map(str, args))

    def comparison(self, *args):
        return " ".join(map(str, args))

    def arith_expr(self, *args):
        return " ".join(map(str, args))

    def term(self, *args):
        return " ".join(map(str, args))

    def factor(self, *args):
        if len(args) == 1:
            return str(args[0])
        return " ".join(map(str, args))

    def power(self, *args):
        return " ** ".join(map(str, args))

    def list_literal(self, *items):
        if items:
            return f"[{', '.join(map(str, items))}]"
        return "[]"

    def array_literal(self, *items):
        # In Python, both are lists, but we keep the semantic distinction in comments
        if items:
            return f"[{', '.join(map(str, items))}]  # array"
        return "[]  # array"

    def map_literal(self, *pairs):
        if pairs:
            return "{" + ", ".join(map(str, pairs)) + "}"
        return "{}"

    def map_pair(self, key, value):
        return f"{key}: {value}"

    def dict_access(self, obj, key):
        return f"{obj}[{key}]"

    def list_access(self, obj, index):
        return f"{obj}[{index}]"

    def function_call(self, name, args=None):
        args_str = args if args else ""
        return f"{name}({args_str})"

    def arguments(self, *args):
        return ", ".join(map(str, args))

    def NAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return str(token)

    def STRING(self, token):
        return str(token)

    def BOOLEAN(self, token):
        return str(token)

    def COMP_OP(self, token):
        # Convert = to ==
        if token == "=":
            return "=="
        return str(token)

    def ADD_OP(self, token):
        return str(token)

    def MUL_OP(self, token):
        return str(token)


class RLCompiler:
    """Main compiler class for .rl files."""

    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', start='program')
        self.transformer = PythonCompiler()

    def compile(self, source_code: str) -> str:
        """Compile .rl source code to Python code."""
        tree = self.parser.parse(source_code)
        python_code = self.transformer.transform(tree)
        return python_code

    def compile_file(self, input_path: str, output_path: str = None):
        """Compile a .rl file to a .py file."""
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.with_suffix('.py')
        else:
            output_path = Path(output_path)

        with open(input_path, 'r') as f:
            source = f.read()

        compiled = self.compile(source)

        with open(output_path, 'w') as f:
            f.write(compiled)

        return output_path


def main():
    """Command-line interface for the compiler."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <input.rl> [output.py]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    compiler = RLCompiler()
    
    try:
        output_path = compiler.compile_file(input_file, output_file)
        print(f"Successfully compiled {input_file} -> {output_path}")
    except Exception as e:
        print(f"Compilation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
