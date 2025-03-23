# Autowire Tool Technical Documentation

## 1. Project Overview

Autowire is an automated tool for scanning Verilog/SystemVerilog code and automatically generating wire declarations for undeclared signals. The tool supports various features including signal width inference, exclusion pattern configuration, and output format customization.

### 1.1 Key Features

- Preserves the original order of signals
- Automatically infers signal widths
- Supports signals defined with parameters
- Multiple output modes (separate file or append to original file)
- Supports user-defined exclusion patterns
- Enhanced module instantiation name recognition
- Supports generate/endgenerate keywords
- Supports Verilog numeric constants
- Supports multi-line comments and macro definitions

## 2. Project Structure

```
autowire/
├── cli/               # Command-line interface module
│   ├── __init__.py
│   └── main.py        # Command-line entry point
├── config/            # Configuration module
│   ├── __init__.py
│   ├── config.py      # Configuration management
│   └── auto_wire_config.json  # Default configuration file
├── core/              # Core functionality modules
│   ├── __init__.py
│   ├── analyzer.py    # Signal analyzer
│   ├── generator.py   # Code generator
│   ├── parser.py      # Verilog parser
│   └── utils.py       # Utility functions
├── rtl/               # Test RTL files
├── __init__.py        # Package initialization
└── __main__.py        # Program entry point
```

## 3. Core Module Descriptions

### 3.1 Parser Module (core/parser.py)

The Verilog parser module is responsible for parsing Verilog code and extracting basic information.

#### Main Classes and Methods

##### `VerilogParser` Class
```python
class VerilogParser:
    def __init__(self)
    def parse_file(self, file_path: str) -> None
    def get_undefined_signals(self, exclude_patterns: List[str] = None) -> List[str]
    def get_signal_widths(self, signals: List[str]) -> Dict[str, Optional[str]]
```

| Method | Description |
|-----|-----|
| `parse_file(file_path)` | Parses a Verilog file at the specified path |
| `get_undefined_signals(exclude_patterns)` | Gets a list of undefined signals, optionally excluding specific patterns |
| `get_signal_widths(signals)` | Gets width information for the specified list of signals |
| `_extract_signals()` | Extracts all signals |
| `_extract_defined_signals()` | Extracts defined signals |
| `_extract_signals_by_pattern(pattern, signal_set)` | Extracts signals using a regex pattern |
| `_extract_module_info()` | Extracts module-related information |
| `_extract_port_signals_from_module_declaration()` | Extracts port signals from the module declaration |
| `_exclude_port_signal_wire_declaration()` | Excludes duplicate port signal declarations |
| `get_signal_bitwidth(signal_name)` | Gets the bit width of a single signal |

### 3.2 Analyzer Module (core/analyzer.py)

The signal analyzer module is responsible for analyzing signal definitions and usage in Verilog code.

#### Main Classes and Methods

##### `SignalAnalyzer` Class
```python
class SignalAnalyzer:
    def __init__(self)
    def setup(self, parser: VerilogParser, exclude_patterns: List[str] = None, default_width: Optional[str] = None) -> None
    def analyze(self) -> None
    def get_undefined_signals(self) -> List[str]
```

| Method | Description |
|-----|-----|
| `setup(parser, exclude_patterns, default_width)` | Sets up the analyzer with a parser instance and exclusion patterns |
| `analyze()` | Performs signal analysis |
| `analyze_signal_widths()` | Analyzes signal widths |
| `get_undefined_signals()` | Gets a list of undefined signals |
| `get_signal_width(signal)` | Gets the width of a specific signal |
| `get_formatted_signal_widths()` | Gets a dictionary of formatted signal widths |
| `get_signal_definitions()` | Gets a dictionary of signal definitions |
| `get_report()` | Gets an analysis report |

### 3.3 Generator Module (core/generator.py)

The code generator module is responsible for generating wire declaration code and handling output.

#### Main Classes and Methods

##### `CodeGenerator` Class
```python
class CodeGenerator:
    def __init__(self)
    def setup(self, analyzer: SignalAnalyzer, file_path: str, output_dir: Optional[str] = None, append: bool = False) -> None
    def generate(self) -> List[str]
    def write_to_file(self) -> str
```

| Method | Description |
|-----|-----|
| `setup(analyzer, file_path, output_dir, append)` | Sets up the generator with an analyzer instance and output options |
| `generate()` | Generates wire declaration code |
| `write_to_file()` | Writes the generated code to a file |
| `_write_to_new_file()` | Writes to a new file |
| `_append_to_original()` | Appends to the original file |
| `get_summary()` | Gets a generation summary |

### 3.4 Utils Module (core/utils.py)

The utility functions module provides various helper functions.

#### Main Functions and Classes

```python
def handle_error(error: Exception, debug: bool = False) -> None
def read_file(file_path: str) -> str
def write_file(file_path: str, content: str) -> None
def ensure_dir(directory: str) -> None
def remove_comments(content: str) -> str
def format_width(width: str) -> str
def extract_parameters(content: str) -> Dict[str, str]
def is_common_constant(signal: str) -> bool
```

| Function/Class | Description |
|--------|-----|
| `VerilogError` | Base exception class for Verilog errors |
| `ParseError` | Exception class for parsing errors |
| `AnalysisError` | Exception class for analysis errors |
| `ConfigError` | Exception class for configuration errors |
| `handle_error(error, debug)` | Handles exceptions and prints error messages |
| `read_file(file_path)` | Reads file content |
| `write_file(file_path, content)` | Writes content to a file |
| `ensure_dir(directory)` | Ensures a directory exists |
| `remove_comments(content)` | Removes comments from Verilog code |
| `format_width(width)` | Formats signal width |
| `extract_parameters(content)` | Extracts parameter definitions from Verilog code |
| `is_common_constant(signal)` | Checks if a signal name is a common constant name |

### 3.5 Config Module (config/config.py)

The configuration management module contains configuration loading and management functionality.

#### Main Classes and Methods

##### `Config` Class
```python
class Config:
    def __init__(self)
    def load_from_file(self, file_path: str) -> None
    def load_from_args(self, args: Any) -> None
    def get_default_config_path(self) -> str
    def save_to_file(self, file_path: str) -> None
    def validate(self) -> None
```

| Method | Description |
|-----|-----|
| `load_from_file(file_path)` | Loads configuration from a file |
| `load_from_args(args)` | Loads configuration from command-line arguments |
| `get_default_config_path()` | Gets the default configuration file path |
| `save_to_file(file_path)` | Saves configuration to a file |
| `validate()` | Validates configuration validity |

### 3.6 Command-Line Interface (cli/main.py)

The command-line entry module handles command-line argument parsing and program execution flow.

#### Main Functions

```python
def parse_arguments(args: List[str] = None) -> argparse.Namespace
def print_detailed_help() -> None
def run(args: argparse.Namespace) -> int
def main() -> int
```

| Function | Description |
|-----|-----|
| `parse_arguments(args)` | Parses command-line arguments |
| `print_detailed_help()` | Prints detailed help information |
| `run(args)` | Executes the main program |
| `main()` | Main function, program entry point |

## 4. Usage Flow

1. **Parsing** (Parser): Parse Verilog file, extract defined signals and all possible signals
2. **Analysis** (Analyzer): Analyze signals, identify undefined signals, and infer widths
3. **Generation** (Generator): Generate wire declaration code
4. **Output** (Generator): Write the generated code to a new file or append to the original file

## 5. Key Algorithm Explanations

### 5.1 Signal Extraction Algorithm

- Uses regular expressions to match different types of signal declarations (wire, reg, logic, input, output, inout)
- Parses the port list in module declarations
- Identifies and excludes module instantiations and constants

### 5.2 Width Inference Algorithm

- Extracts width information from signal usage context
- Supports standard width formats (e.g., `[7:0]`) and parameterized widths (e.g., `[WIDTH-1:0]`)
- Extracts width information from input/output signal declarations

### 5.3 Port Signal Handling

- Identifies module port signals to prevent duplicate declarations
- Specially handles input/output signals to ensure they don't appear in automatically generated wire declarations

## 6. Considerations and Limitations

- Currently does not support complex macro definitions and conditional compilation
- Width inference may not apply to all complex expressions
- Uses the original unprocessed content for certain matching to ensure accurate identification of input/output signals

## 7. Future Improvement Directions

- Support for more complex macro definitions and conditional compilation
- Enhanced width inference capabilities
- More customization options
- Support for more Verilog/SystemVerilog features
- Addition of more detailed logging and debugging information 