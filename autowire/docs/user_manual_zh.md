# Autowire 用户手册

## 1. 介绍

Autowire 是一款提高生产力的工具，专为自动生成 Verilog/SystemVerilog 源文件中未声明信号的线网（wire）声明而设计。它能够扫描你的 RTL 代码，识别已使用但未声明的信号，并尽可能生成带有适当位宽的必要线网声明。

## 2. 安装

### 2.1 要求

- Python 3.6 或更高版本
- pip (Python 包安装器)

### 2.2 安装步骤

1. 克隆仓库或下载源代码包
2. 导航到项目根目录
3. 运行安装命令：

```bash
pip install -e .
```

## 3. 基本用法

工具的基本用法是：

```bash
autowire [选项] <verilog文件>
```

其中 `<verilog文件>` 是你想要分析的 Verilog/SystemVerilog 文件的路径。

### 3.1 示例

```bash
autowire path/to/your/design.v
```

这将会：
1. 分析文件 `design.v`
2. 识别未声明的信号
3. 在同一目录中生成一个带有线网声明的新文件，命名为 `design_auto_wire.v`

## 4. 命令行选项

| 选项 | 简写形式 | 描述 |
|--------|------------|-------------|
| `--width` | `-w` | 尝试根据使用情况推断信号位宽 |
| `--default-width WIDTH` | `-d WIDTH` | 为无法推断位宽的信号设置默认位宽（例如，"[7:0]" 或 "8"） |
| `--append` | `-a` | 将声明附加到原始文件，而不是创建新文件 |
| `--output-dir DIR` | `-o DIR` | 指定生成文件的输出目录 |
| `--exclude PATTERN1 [PATTERN2 ...]` | `-e PATTERN1 [PATTERN2 ...]` | 指定要从线网声明生成中排除的正则表达式模式 |
| `--config FILE` | `-c FILE` | 指定配置文件路径 |
| `--verbose` | `-v` | 在处理过程中显示详细信息 |
| `--help-detail` | | 显示详细帮助信息 |
| `--debug` | | 启用调试模式，显示中间处理结果 |

## 5. 配置文件

你可以使用 JSON 配置文件来控制工具的行为，而不是在命令行上指定选项。

### 5.1 示例配置文件

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

### 5.2 使用配置文件

```bash
autowire --config my_config.json design.v
```

## 6. 位宽推断

当使用 `--width` 选项时，Autowire 将尝试根据代码中的使用情况推断信号位宽：

1. 它会查找位选择操作，如 `signal[3:0]`
2. 它会检查已知位宽信号之间的赋值
3. 它会检查输入/输出声明
4. 对于无法确定位宽的信号，将使用默认位宽

## 7. 输出模式

### 7.1 新文件模式（默认）

默认情况下，工具会创建一个与输入文件同名但在扩展名前附加了 `_auto_wire` 的新文件。

示例：
```
输入: design.v
输出: design_auto_wire.v
```

### 7.2 追加模式

当使用 `--append` 选项时，工具会将线网声明直接添加到原始文件中，通常是在模块声明之后、其他任何声明之前。

## 8. 排除模式

你可以指定正则表达式模式来排除信号被声明：

```bash
autowire --exclude "^temp_" "_i$" design.v
```

此示例将排除：
- 以 "temp_" 开头的信号
- 以 "_i" 结尾的信号

## 9. 常用示例

### 9.1 带位宽推断的基本分析

```bash
autowire --width design.v
```

### 9.2 使用自定义默认位宽

```bash
autowire --width --default-width "[31:0]" design.v
```

### 9.3 追加到原始文件

```bash
autowire --width --append design.v
```

### 9.4 指定输出目录

```bash
autowire --output-dir ./generated design.v
```

### 9.5 带多个选项的完整示例

```bash
autowire --width --default-width "[15:0]" --exclude "^temp_" "_i$" --verbose --output-dir ./output design.v
```

## 10. 故障排除

### 10.1 调试模式

如果你遇到问题，可以启用调试模式以查看更详细的信息：

```bash
autowire --debug design.v
```

### 10.2 常见问题

- **未生成线网声明**：检查是否所有信号都已声明或是否匹配排除模式
- **位宽推断不正确**：使用 `--default-width` 选项设置特定位宽
- **解析器错误**：确保你的 Verilog 代码在语法上是正确的

## 11. 高级用法

### 11.1 处理多个文件

要处理多个文件，你可以使用 shell 脚本或批处理文件：

```bash
# Bash 脚本示例
for file in *.v; do
    autowire --width --config my_config.json "$file"
done
```

### 11.2 与构建系统集成

Autowire 可以集成到你的构建系统中，以便在综合前自动生成线网声明：

```makefile
# Makefile 规则示例
%.autowired.v: %.v
	autowire --width --output-dir build $<
``` 