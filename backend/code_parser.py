import ast

def parse_code(code_text):
    """
    Parses Python code and extracts:
    - functions
    - classes
    - imports
    """

    tree = ast.parse(code_text)

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):

        # FUNCTION DEFINITIONS
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "arguments": [arg.arg for arg in node.args.args],
                "start_line": node.lineno
            })

        # CLASS DEFINITIONS
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                "start_line": node.lineno
            })

        # IMPORTS
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)

        if isinstance(node, ast.ImportFrom):
            imports.append(node.module)

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports
    }
