# utils.py
import ast

def extract_code_pieces(
    text: str, 
    start: str = "```", end: str = "```",
    do_split: bool = True,
) -> list[str]:
    """Extract code pieces from a text string.
    Args:
        text: str, model prediciton text.
    Rets:
        code_pieces: list[str], code pieces in the text.
    """
    code_pieces = []
    while start in text:
        st_idx = text.index(start) + len(start)
        if end in text[st_idx:]:
            end_idx = text.index(end, st_idx)
        else: 
            end_idx = len(text)
        
        if do_split:
            code_pieces.extend(text[st_idx:end_idx].strip().split("\n"))
        else:
            code_pieces.append(text[st_idx:end_idx].strip())
        text = text[end_idx+len(end):].strip()
    return code_pieces

def count_function_calls(function_code: str, threshold: int = 1):
    """
    Count the number of function calls in the given function implementation.

    Args:
        function_code (str): The code of the function as a string.
        threshold (int): The minimum number of function calls to return True.

    Returns:
        int: The number of function calls in the code.
    """
    # Parse the function code into an AST
    tree = ast.parse(function_code)
    
    # Find all nodes that are function calls
    function_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    
    # Return the number of function call nodes
    def_counts = function_code.count("def ")
    return len(function_calls) > (threshold * def_counts)


def get_function_names(function_code: str, existing_names: list[str] = []) -> list[str]:
    """Get the names of defined functions in the code."""
    tree = ast.parse(function_code)
    names = [
        fdef.name for fdef in tree.body 
        if isinstance(fdef, ast.FunctionDef)
    ]
    names = [n for n in names if n not in existing_names]
    return names