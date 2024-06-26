import clang.cindex
import json
from utils import set_libclang_path, extract_type_info, expand_type

# Set the libclang path
if not set_libclang_path():
    raise RuntimeError("libclang library not found. Please install LLVM and set the correct path.")

def extract_declarations(filename):
    """
    Extract type declarations from a C source file.

    Parameters:
    filename (str): The path to the C source file.

    Returns:
    dict: A dictionary of declared types.
    """
    # Create an index for parsing
    index = clang.cindex.Index.create()
    # Parse the file to create a translation unit
    translation_unit = index.parse(filename)
    
    declared_types = {}

    def visit_node(node):
        # Check for type declarations (struct, union, typedef)
        if node.kind in [clang.cindex.CursorKind.STRUCT_DECL, clang.cindex.CursorKind.UNION_DECL, clang.cindex.CursorKind.TYPEDEF_DECL]:
            print(f"Declaring type: {node.spelling}, kind: {node.kind}")  # Debugging print
            # Extract type information and add to declared types dictionary
            declared_types[node.spelling] = extract_type_info(node.type, declared_types)
        # Recursively visit children nodes
        for child in node.get_children():
            visit_node(child)

    # Start visiting nodes from the root cursor
    visit_node(translation_unit.cursor)
    return declared_types

def extract_function_declarations(filename, keyword, declared_types):
    """
    Extract function declarations from a C source file.

    Parameters:
    filename (str): The path to the C source file.
    keyword (str): A keyword to filter function names.
    declared_types (dict): A dictionary of declared types.

    Returns:
    list: A list of dictionaries representing functions.
    """
    # Create an index for parsing
    index = clang.cindex.Index.create()
    # Parse the file to create a translation unit
    translation_unit = index.parse(filename)
    
    functions = []

    def visit_node(node):
        # Check if the node is a function declaration
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            # Check if the function name matches the keyword (if provided)
            if not keyword or keyword in node.spelling:
                # Ensure the function is defined in the specified file
                if node.location.file and node.location.file.name == filename:
                    # Extract arguments and expand their types
                    args = [{"name": arg.spelling, "type": expand_type(extract_type_info(arg.type, declared_types), declared_types)} for arg in node.get_arguments()]
                    print(f"Function {node.spelling} args: {args}")  # Debugging print
                    # Append function information to the functions list
                    functions.append({
                        "name": node.spelling,
                        "return_type": expand_type(extract_type_info(node.result_type, declared_types), declared_types),
                        "args": args
                    })
        # Recursively visit children nodes
        for child in node.get_children():
            visit_node(child)

    # Start visiting nodes from the root cursor
    visit_node(translation_unit.cursor)

    return functions

def parse_code(command_file, telemetry_file, command_keyword, telemetry_keyword):
    """
    Parse command and telemetry C source files.

    Parameters:
    command_file (str): The path to the command functions C source file.
    telemetry_file (str): The path to the telemetry functions C source file.
    command_keyword (str): A keyword to filter command function names.
    telemetry_keyword (str): A keyword to filter telemetry function names.

    Returns:
    dict: A dictionary containing parsed command and telemetry functions.
    """
    # Extract declarations from command and telemetry files
    declared_types = extract_declarations(command_file)
    declared_types.update(extract_declarations(telemetry_file))

    print(f"Declared types: {declared_types}")  # Debugging print

    # Extract function declarations for commands and telemetry
    commands = extract_function_declarations(command_file, command_keyword, declared_types)
    telemetry = extract_function_declarations(telemetry_file, telemetry_keyword, declared_types)

    return {"commands": commands, "telemetry": telemetry}

def save_to_json(data, filename):
    """
    Save parsed data to a JSON file.

    Parameters:
    data (dict): The parsed data to save.
    filename (str): The path to the output JSON file.
    """
    # Write data to a JSON file with indentation
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
