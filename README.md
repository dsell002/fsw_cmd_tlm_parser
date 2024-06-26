# FSW Command and Telemetry Parser

This project provides a tool for parsing command and telemetry files in flight software using `clang`. The tool extracts data types and function declarations to generate a JSON file, which can be used to build command and telemetry interfaces.

## Features

- Parses C source files for command and telemetry functions.
- Supports complex data types including structures, unions, and typedefs.
- Generates a JSON file with parsed data.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/dsell002/fsw_cmd_tlm_parser.git
cd FSWCmdTlmParser
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage
Run the parser tool using the following command:
```bash
python fsw_cmd_tlm_parser/main.py
```

## Project Structure
```plaintext
FSWCmdTlmParser/
├── sample_files/
│   ├── command_functions.c
│   ├── telemetry_functions.c
│   └── output.json
├── fsw_cmd_tlm_parser/
│   ├── __init__.py
│   ├── clang_parser.py
│   ├── utils.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_clang_parser.py
│   └── test_utils.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Running Tests
To run the unit tests, use the following command:
```bash
python -m unittest discover tests
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
