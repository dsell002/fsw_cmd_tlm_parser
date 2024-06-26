import clang.cindex
import os
import sys

def set_libclang_path():
    if sys.platform == 'win32':
        # Windows
        possible_paths = [
            'C:/Program Files/LLVM/bin/libclang.dll',
            'C:/Program Files (x86)/LLVM/bin/libclang.dll'
        ]
    elif sys.platform == 'darwin':
        # macOS
        possible_paths = ['/usr/local/opt/llvm/lib/libclang.dylib']
    else:
        # Linux
        possible_paths = [
            '/usr/lib/llvm-10/lib/libclang.so',
            '/usr/lib/llvm-11/lib/libclang.so',
            '/usr/lib/llvm-12/lib/libclang.so',
            '/usr/lib/llvm-13/lib/libclang.so',
            '/usr/lib/llvm-14/lib/libclang.so',
            '/usr/lib/llvm/libclang.so'
        ]

    for path in possible_paths:
        if os.path.exists(path):
            clang.cindex.Config.set_library_file(path)
            return True
    return False

def extract_type_info(t, declared_types=None):
    print(f"Extracting type info for: {t.spelling}, kind: {t.kind}")  # Debugging print
    if t.kind == clang.cindex.TypeKind.RECORD:
        cursor = t.get_declaration()
        fields = []
        for field in cursor.get_children():
            field_info = {"name": field.spelling, "type": extract_type_info(field.type, declared_types)}
            if field.is_bitfield():
                field_info["bitfield_width"] = field.get_bitfield_width()
            fields.append(field_info)
        kind = "union" if cursor.kind == clang.cindex.CursorKind.UNION_DECL else "struct"
        return {"kind": kind, "name": cursor.spelling, "fields": fields}
    elif t.kind == clang.cindex.TypeKind.CONSTANTARRAY:
        return {"kind": "array", "element_type": extract_type_info(t.get_array_element_type(), declared_types), "size": t.get_array_size()}
    elif t.kind == clang.cindex.TypeKind.POINTER:
        pointee_type = t.get_pointee()
        return {"kind": "pointer", "pointee_type": extract_type_info(pointee_type, declared_types)}
    elif t.kind == clang.cindex.TypeKind.ENUM:
        enum_constants = [{"name": enum.spelling, "value": enum.enum_value} for enum in t.get_declaration().get_children()]
        return {"kind": "enum", "constants": enum_constants}
    elif t.kind == clang.cindex.TypeKind.TYPEDEF:
        underlying_type = extract_type_info(t.get_canonical(), declared_types)
        return {"kind": "typedef", "name": t.spelling, "underlying_type": underlying_type}
    elif t.kind == clang.cindex.TypeKind.FUNCTIONPROTO:
        return_type = extract_type_info(t.get_result(), declared_types)
        args = [{"name": f"arg{i}", "type": extract_type_info(arg, declared_types)} for i, arg in enumerate(t.argument_types())]
        return {"kind": "function", "return_type": return_type, "args": args}
    elif t.kind == clang.cindex.TypeKind.ELABORATED:
        cursor = t.get_declaration()
        return extract_type_info(cursor.type, declared_types)
    else:
        return t.spelling

def expand_type(t, declared_types, expanded_types=None):
    if expanded_types is None:
        expanded_types = set()
    
    print(f"Expanding type: {t}")  # Debugging print
    if isinstance(t, dict) and "kind" in t:
        if t["kind"] == "typedef":
            name = t.get("name")
            if name and name in declared_types and name not in expanded_types:
                expanded_types.add(name)
                underlying_type = declared_types[name]
                t["underlying_type"] = expand_type(underlying_type, declared_types, expanded_types)
                return t
        elif t["kind"] in ["struct", "union"]:
            if "fields" in t:
                for field in t["fields"]:
                    field["type"] = expand_type(field["type"], declared_types, expanded_types)
            return t
        elif t["kind"] == "pointer":
            t["pointee_type"] = expand_type(t["pointee_type"], declared_types, expanded_types)
            return t
        elif t["kind"] == "function":
            t["return_type"] = expand_type(t["return_type"], declared_types, expanded_types)
            for arg in t["args"]:
                arg["type"] = expand_type(arg["type"], declared_types, expanded_types)
            return t
    return t
