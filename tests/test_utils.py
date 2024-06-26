import unittest
from fsw_cmd_tlm_parser.utils import set_libclang_path, extract_type_info, expand_type
import clang.cindex

class TestUtils(unittest.TestCase):

    def test_set_libclang_path(self):
        self.assertTrue(set_libclang_path())

    def test_extract_type_info_basic(self):
        # Assuming `clang.cindex.Config` is properly configured in the real environment
        index = clang.cindex.Index.create()
        tu = index.parse('sample_files/command_functions.c')
        
        for cursor in tu.cursor.get_children():
            if cursor.kind == clang.cindex.CursorKind.STRUCT_DECL and cursor.spelling == "Status":
                type_info = extract_type_info(cursor.type)
                self.assertEqual(type_info['kind'], 'struct')
                self.assertEqual(type_info['name'], 'Status')
                self.assertEqual(len(type_info['fields']), 3)
                break

    def test_expand_type_basic(self):
        declared_types = {
            'Status': {
                'kind': 'struct',
                'name': 'Status',
                'fields': [
                    {'name': 'isConnected', 'type': 'unsigned int'},
                    {'name': 'errorCode', 'type': 'unsigned int'},
                    {'name': 'reserved', 'type': 'unsigned int'}
                ]
            }
        }

        type_info = {
            'kind': 'struct',
            'name': 'DataPacket',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'value', 'type': 'float'},
                {'name': 'status', 'type': 'Status'}
            ]
        }

        expanded_type = expand_type(type_info, declared_types)
        self.assertEqual(expanded_type['fields'][2]['type'], declared_types['Status'])

if __name__ == '__main__':
    unittest.main()
