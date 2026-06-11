import ast


def analyze_python_code(code):

    try:

        tree = ast.parse(code)  ## convert the code to ast tree like structure

    except Exception:

        return None

    functions = []

    classes = []

    imports = []

    loops = 0

    ##containers to store information 

    for node in ast.walk(tree):##visit every single node in tree

        if isinstance(node, ast.FunctionDef):

            functions.append(node.name)  ##add to functions if function similarly for rest
                                        ## we add only function name
        elif isinstance(node, ast.ClassDef):

            classes.append(node.name)  

        elif isinstance(node, ast.Import):

            for alias in node.names:
                    ##each imported module stored as alias  handles this import math
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):

            imports.append(node.module)     ##handles this-- from math import sqrt

        elif isinstance(node, (ast.For, ast.While)):
                ##stores if for loop while loop ,its count
            loops += 1

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "loops": loops
    }