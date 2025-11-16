

# code_parser.py
import ast

def parse_code(code_text):
    """
    Parse Python code and extract basic structure: functions, classes, imports.
    Returns a dict with simple lists to send to the LLM and to create a diagram.
    """
    try:
        tree = ast.parse(code_text)
    except Exception:
        return {"functions": [], "classes": [], "imports": []}

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "lineno": getattr(node, "lineno", None)
            })
        elif isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({
                "name": node.name,
                "methods": methods,
                "lineno": getattr(node, "lineno", None)
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    # Deduplicate imports while keeping order
    seen = set()
    imports_clean = []
    for im in imports:
        if im and im not in seen:
            seen.add(im)
            imports_clean.append(im)

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports_clean
    }


# import ast

# def parse_code(code_text):
#     try:
#         tree = ast.parse(code_text)

#         functions = []
#         classes = []
#         imports = []

#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 functions.append(node.name)
#             elif isinstance(node, ast.ClassDef):
#                 classes.append(node.name)
#             elif isinstance(node, ast.Import):
#                 imports.extend([alias.name for alias in node.names])
#             elif isinstance(node, ast.ImportFrom):
#                 imports.append(node.module)

#         return {
#             "functions": functions,
#             "classes": classes,
#             "imports": imports
#         }

#     except:
#         return {"functions": [], "classes": [], "imports": []}
