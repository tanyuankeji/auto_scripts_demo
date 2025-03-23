# Autowire 工具技术文档

## 1. 项目概述

Autowire 是一个自动化工具，用于扫描 Verilog/SystemVerilog 代码并自动生成未声明信号的 wire 声明。该工具支持多种功能，包括信号位宽推断、排除模式配置、输出格式定制等。

### 1.1 主要特性

- 保持信号的原始出现顺序
- 自动推断信号位宽
- 支持 parameter 定义的信号
- 多种输出模式（独立文件或追加到原文件）
- 支持用户自定义排除匹配模式
- 增强的模块实例化名称识别
- 支持 generate/endgenerate 关键字
- 支持 Verilog 数值常量
- 支持多行注释和宏定义

## 2. 项目结构

```
autowire/
├── cli/               # 命令行接口模块
│   ├── __init__.py
│   └── main.py        # 命令行入口点
├── config/            # 配置模块
│   ├── __init__.py
│   ├── config.py      # 配置管理
│   └── auto_wire_config.json  # 默认配置文件
├── core/              # 核心功能模块
│   ├── __init__.py
│   ├── analyzer.py    # 信号分析器
│   ├── generator.py   # 代码生成器
│   ├── parser.py      # Verilog解析器
│   └── utils.py       # 工具函数
├── rtl/               # 测试用RTL文件
├── __init__.py        # 包初始化
└── __main__.py        # 程序入口点
```

## 3. 核心模块说明

### 3.1 Parser模块 (core/parser.py)

Verilog解析器模块，负责解析Verilog代码并提取基础信息。

#### 主要类和方法

##### `VerilogParser` 类
```python
class VerilogParser:
    def __init__(self)
    def parse_file(self, file_path: str) -> None
    def get_undefined_signals(self, exclude_patterns: List[str] = None) -> List[str]
    def get_signal_widths(self, signals: List[str]) -> Dict[str, Optional[str]]
```

| 方法 | 描述 |
|-----|-----|
| `parse_file(file_path)` | 解析指定路径的Verilog文件 |
| `get_undefined_signals(exclude_patterns)` | 获取未定义信号列表，可选择排除特定模式 |
| `get_signal_widths(signals)` | 获取指定信号列表的位宽信息 |
| `_extract_signals()` | 提取所有信号 |
| `_extract_defined_signals()` | 提取已定义的信号 |
| `_extract_signals_by_pattern(pattern, signal_set)` | 根据正则表达式模式提取信号 |
| `_extract_module_info()` | 提取模块相关信息 |
| `_extract_port_signals_from_module_declaration()` | 从模块声明中提取端口信号 |
| `_exclude_port_signal_wire_declaration()` | 排除端口信号重复声明 |
| `get_signal_bitwidth(signal_name)` | 获取单个信号的位宽 |

### 3.2 Analyzer模块 (core/analyzer.py)

信号分析器模块，负责分析Verilog代码中的信号定义和使用。

#### 主要类和方法

##### `SignalAnalyzer` 类
```python
class SignalAnalyzer:
    def __init__(self)
    def setup(self, parser: VerilogParser, exclude_patterns: List[str] = None, default_width: Optional[str] = None) -> None
    def analyze(self) -> None
    def get_undefined_signals(self) -> List[str]
```

| 方法 | 描述 |
|-----|-----|
| `setup(parser, exclude_patterns, default_width)` | 设置分析器，指定解析器实例和排除模式 |
| `analyze()` | 执行信号分析 |
| `analyze_signal_widths()` | 分析信号位宽 |
| `get_undefined_signals()` | 获取未定义信号列表 |
| `get_signal_width(signal)` | 获取特定信号的位宽 |
| `get_formatted_signal_widths()` | 获取格式化的信号位宽字典 |
| `get_signal_definitions()` | 获取信号定义字典 |
| `get_report()` | 获取分析报告 |

### 3.3 Generator模块 (core/generator.py)

代码生成器模块，负责生成wire声明代码并处理输出。

#### 主要类和方法

##### `CodeGenerator` 类
```python
class CodeGenerator:
    def __init__(self)
    def setup(self, analyzer: SignalAnalyzer, file_path: str, output_dir: Optional[str] = None, append: bool = False) -> None
    def generate(self) -> List[str]
    def write_to_file(self) -> str
```

| 方法 | 描述 |
|-----|-----|
| `setup(analyzer, file_path, output_dir, append)` | 设置生成器，指定分析器实例和输出选项 |
| `generate()` | 生成wire声明代码 |
| `write_to_file()` | 将生成的代码写入文件 |
| `_write_to_new_file()` | 写入新文件 |
| `_append_to_original()` | 追加到原始文件 |
| `get_summary()` | 获取生成摘要 |

### 3.4 Utils模块 (core/utils.py)

工具函数模块，提供各种辅助函数。

#### 主要函数和类

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

| 函数/类 | 描述 |
|--------|-----|
| `VerilogError` | Verilog错误异常基类 |
| `ParseError` | 解析错误异常类 |
| `AnalysisError` | 分析错误异常类 |
| `ConfigError` | 配置错误异常类 |
| `handle_error(error, debug)` | 处理异常并打印错误信息 |
| `read_file(file_path)` | 读取文件内容 |
| `write_file(file_path, content)` | 写入文件内容 |
| `ensure_dir(directory)` | 确保目录存在 |
| `remove_comments(content)` | 移除Verilog代码中的注释 |
| `format_width(width)` | 格式化信号位宽 |
| `extract_parameters(content)` | 提取Verilog代码中的参数定义 |
| `is_common_constant(signal)` | 检查信号名是否是常见常量名 |

### 3.5 Config模块 (config/config.py)

配置管理模块，包含配置加载和管理功能。

#### 主要类和方法

##### `Config` 类
```python
class Config:
    def __init__(self)
    def load_from_file(self, file_path: str) -> None
    def load_from_args(self, args: Any) -> None
    def get_default_config_path(self) -> str
    def save_to_file(self, file_path: str) -> None
    def validate(self) -> None
```

| 方法 | 描述 |
|-----|-----|
| `load_from_file(file_path)` | 从文件加载配置 |
| `load_from_args(args)` | 从命令行参数加载配置 |
| `get_default_config_path()` | 获取默认配置文件路径 |
| `save_to_file(file_path)` | 保存配置到文件 |
| `validate()` | 验证配置有效性 |

### 3.6 命令行接口 (cli/main.py)

命令行入口模块，处理命令行参数解析和程序执行流程。

#### 主要函数

```python
def parse_arguments(args: List[str] = None) -> argparse.Namespace
def print_detailed_help() -> None
def run(args: argparse.Namespace) -> int
def main() -> int
```

| 函数 | 描述 |
|-----|-----|
| `parse_arguments(args)` | 解析命令行参数 |
| `print_detailed_help()` | 打印详细帮助信息 |
| `run(args)` | 执行主程序 |
| `main()` | 主函数，程序入口点 |

## 4. 使用流程

1. **解析** (Parser): 解析Verilog文件，提取已定义信号和所有可能的信号
2. **分析** (Analyzer): 分析信号，识别未定义信号并推断位宽
3. **生成** (Generator): 生成wire声明代码
4. **输出** (Generator): 将生成的代码写入新文件或追加到原始文件

## 5. 关键算法说明

### 5.1 信号提取算法

- 使用正则表达式匹配不同类型的信号声明（wire、reg、logic、input、output、inout）
- 解析模块声明中的端口列表
- 识别并排除模块实例化和常量

### 5.2 位宽推断算法

- 从信号使用上下文中提取位宽信息
- 支持标准位宽格式（如 `[7:0]`）和参数化位宽（如 `[WIDTH-1:0]`）
- 从输入/输出信号声明中提取位宽信息

### 5.3 端口信号处理

- 识别模块端口信号，确保不会重复声明
- 特别处理输入/输出信号，确保它们不会出现在自动生成的wire声明中

## 6. 注意事项与限制

- 目前不支持复杂的宏定义和条件编译
- 位宽推断可能不适用于所有复杂表达式
- 使用原始未处理内容进行某些匹配，以确保准确识别输入/输出信号

## 7. 未来改进方向

- 支持更复杂的宏定义和条件编译
- 增强位宽推断能力
- 提供更多自定义选项
- 支持更多Verilog/SystemVerilog特性
- 添加更详细的日志和调试信息 