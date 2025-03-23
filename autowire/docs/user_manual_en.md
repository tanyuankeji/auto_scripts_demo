# Autowire User Manual

## 1. Introduction

Autowire is a productivity tool designed to automatically generate wire declarations for undeclared signals in Verilog/SystemVerilog source files. It scans your RTL code, identifies signals that are used but not declared, and generates the necessary wire declarations with appropriate bit widths where possible.

## 2. Installation

### 2.1 Requirements

- Python 3.6 or higher
- pip (Python package installer)

### 2.2 Installation Steps

1. Clone the repository or download the source package
2. Navigate to the project root directory
3. Run the installation command:

```bash
pip install -e .
```

## 3. Basic Usage

The basic usage of the tool is:

```bash
autowire [options] <verilog_file>
```

Where `<verilog_file>` is the path to the Verilog/SystemVerilog file you want to analyze.

### 3.1 Example

```bash
autowire path/to/your/design.v
```

This will:
1. Analyze the file `design.v`
2. Identify undeclared signals
3. Generate a new file with wire declarations in the same directory named `design_auto_wire.v`

## 4. Command Line Options

| Option | Short Form | Description |
|--------|------------|-------------|
| `--width` | `-w` | Try to infer signal widths based on usage |
| `--default-width WIDTH` | `-d WIDTH` | Set default width for signals where width can't be inferred (e.g., "[7:0]" or "8") |
| `--append` | `-a` | Append declarations to the original file instead of creating a new file |
| `--output-dir DIR` | `-o DIR` | Specify output directory for generated files |
| `--exclude PATTERN1 [PATTERN2 ...]` | `-e PATTERN1 [PATTERN2 ...]` | Specify regex patterns to exclude from wire declaration generation |
| `--config FILE` | `-c FILE` | Specify a configuration file path |
| `--verbose` | `-v` | Show detailed information during processing |
| `--help-detail` | | Show detailed help information |
| `--debug` | | Enable debug mode, showing intermediate processing results |

## 5. Configuration Files

You can use a JSON configuration file to control the tool's behavior instead of specifying options on the command line.

### 5.1 Example Configuration File

```json
{
    "width": true,
    "default_width": "[7:0]",
    "append": false,
    "output_dir": "./output",
    "exclude_patterns": [
        "^tb_",
        "_i$"
    ]
}
```

### 5.2 Using a Configuration File

```bash
autowire --config my_config.json design.v
```

## 6. Width Inference

When using the `--width` option, Autowire will attempt to infer signal widths based on how they're used in the code:

1. It looks for bit select operations like `signal[3:0]`
2. It checks assignments between signals of known width
3. It examines input/output declarations
4. For signals where width can't be determined, the default width is used

## 7. Output Modes

### 7.1 New File Mode (Default)

By default, the tool creates a new file with the same name as the input file but with `_auto_wire` appended before the extension.

Example:
```
input: design.v
output: design_auto_wire.v
```

### 7.2 Append Mode

When using the `--append` option, the tool will add the wire declarations directly to the original file, typically after the module declaration and before any other declarations.

## 8. Exclusion Patterns

You can specify regex patterns to exclude signals from being declared:

```bash
autowire --exclude "^temp_" "_i$" design.v
```

This example would exclude:
- Signals starting with "temp_"
- Signals ending with "_i" 

## 9. Common Examples

### 9.1 Basic Analysis with Width Inference

```bash
autowire --width design.v
```

### 9.2 Using a Custom Default Width

```bash
autowire --width --default-width "[31:0]" design.v
```

### 9.3 Appending to Original File

```bash
autowire --width --append design.v
```

### 9.4 Specifying Output Directory

```bash
autowire --output-dir ./generated design.v
```

### 9.5 Full Example with Multiple Options

```bash
autowire --width --default-width "[15:0]" --exclude "^temp_" "_i$" --verbose --output-dir ./output design.v
```

## 10. Troubleshooting

### 10.1 Debug Mode

If you encounter issues, you can enable debug mode to see more detailed information:

```bash
autowire --debug design.v
```

### 10.2 Common Issues

- **No wire declarations generated**: Check if all signals are already declared or if they match exclusion patterns
- **Incorrect width inference**: Use the `--default-width` option to set a specific width
- **Parser errors**: Ensure your Verilog code is syntactically correct

## 11. Advanced Usage

### 11.1 Processing Multiple Files

To process multiple files, you can use shell scripts or batch files:

```bash
# Example bash script
for file in *.v; do
    autowire --width --config my_config.json "$file"
done
```

### 11.2 Integration with Build Systems

Autowire can be integrated into your build system to automatically generate wire declarations before synthesis:

```makefile
# Example Makefile rule
%.autowired.v: %.v
	autowire --width --output-dir build $<
``` 