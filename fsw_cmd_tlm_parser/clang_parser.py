import clang.cindex
import json
from utils import set_libclang_path, extract_type_info, expand_type

# Set the libclang path
if not set_libclang_path():
    raise RuntimeError("libclang library not found. Please install LLVM and set the correct path.")

def extract_declarations(filename):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(filename)
    
    declared_types = {}

    def visit_node(node):
        if node.kind in [clang.cindex.CursorKind.STRUCT_DECL, clang.cindex.CursorKind.UNION_DECL, clang.cindex.CursorKind.TYPEDEF_DECL]:
            print(f"Declaring type: {node.spelling}, kind: {node.kind}")  # Debugging print
            declared_types[node.spelling] = extract_type_info(node.type, declared_types)
        for child in node.get_children():
            visit_node(child)

    visit_node(translation_unit.cursor)
    return declared_types

def extract_function_declarations(filename, keyword, declared_types):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(filename)
    
    functions = []

    def visit_node(node):
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            if not keyword or keyword in node.spelling:
                if node.location.file and node.location.file.name == filename:
                    args = [{"name": arg.spelling, "type": expand_type(extract_type_info(arg.type, declared_types), declared_types)} for arg in node.get_arguments()]
                    print(f"Function {node.spelling} args: {args}")  # Debugging print
                    functions.append({
                        "name": node.spelling,
                        "return_type": expand_type(extract_type_info(node.result_type, declared_types), declared_types),
                        "args": args
                    })
        for child in node.get_children():
            visit_node(child)

    visit_node(translation_unit.cursor)

    return functions

def parse_code(command_file, telemetry_file, command_keyword, telemetry_keyword):
    declared_types = extract_declarations(command_file)
    declared_types.update(extract_declarations(telemetry_file))

    print(f"Declared types: {declared_types}")  # Debugging print

    commands = extract_function_declarations(command_file, command_keyword, declared_types)
    telemetry = extract_function_declarations(telemetry_file, telemetry_keyword, declared_types)

    return {"commands": commands, "telemetry": telemetry}

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
