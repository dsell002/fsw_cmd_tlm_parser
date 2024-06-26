import unittest
from fsw_cmd_tlm_parser.clang_parser import parse_code

class TestClangParser(unittest.TestCase):

    def test_parse_command_functions(self):
        command_file = 'sample_files/command_functions.c'
        telemetry_file = 'sample_files/telemetry_functions.c'
        command_keyword = 'Cmd'
        telemetry_keyword = 'Tlm'
        
        result = parse_code(command_file, telemetry_file, command_keyword, telemetry_keyword)
        
        self.assertIn('commands', result)
        self.assertIn('telemetry', result)
        self.assertGreater(len(result['commands']), 0)
        self.assertGreater(len(result['telemetry']), 0)
        
        # Additional checks for specific command functions
        command_names = [cmd['name'] for cmd in result['commands']]
        self.assertIn('CmdSetSpeed', command_names)
        self.assertIn('CmdProcessData', command_names)
        self.assertIn('CmdHandleUnion', command_names)
        self.assertIn('CmdUseTypedef', command_names)
        self.assertIn('CmdUseFunctionPointer', command_names)

        # Additional checks for specific telemetry functions
        telemetry_names = [tlm['name'] for tlm in result['telemetry']]
        self.assertIn('TlmEngineStatus', telemetry_names)
        self.assertIn('TlmSpeed', telemetry_names)
        self.assertIn('TlmFuelLevel', telemetry_names)

if __name__ == '__main__':
    unittest.main()
