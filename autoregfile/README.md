# AutoRegFile - 自动寄存器文件生成工具

AutoRegFile是一个用于自动生成寄存器文件的工具，支持从多种格式的配置文件生成Verilog代码、APB总线接口、C语言头文件和文档。

## 特性

- 多种配置格式支持:
  - JSON配置
  - Excel配置（包括原有单表格格式、层次化设计、多表分离设计和改进层次化设计）
  - YAML配置
- 自动检测Excel配置格式
- 代码生成:
  - Verilog寄存器文件
  - APB总线接口
  - C语言头文件
- 文档生成:
  - Markdown格式
- 支持多种寄存器类型:
  - ReadWrite (标准读写寄存器)
  - ReadOnly (只读寄存器)
  - WriteOnly (只写寄存器)
  - Write1Clean (写1清零寄存器)
  - Write1Set (写1置位寄存器)
  - Write0Clean (写0清零寄存器)
  - Write0Set (写0置位寄存器)
  - WriteOnce (只能写一次的寄存器)
  - WriteOnlyOnce (只能写一次且只写的寄存器)
  - ReadClean (读取后自动清零寄存器)
  - ReadSet (读取后自动置位寄存器)
  - WriteReadClean (可写且读取后自动清零寄存器)
  - WriteReadSet (可写且读取后自动置位寄存器)
  - Write1Pulse (写1产生脉冲寄存器)
  - Write0Pulse (写0产生脉冲寄存器)
- 支持字段级特性:
  - 锁依赖（某字段只有在特定条件下才能修改）
  - 魔数依赖（需要先向某寄存器写入特定值才能修改）

## 安装

```bash
pip install autoregfile
```

## 使用方法

### 命令行方式

```bash
# 从配置文件生成寄存器文件
autoregfile -i config.json -o output_directory

# 显示帮助信息
autoregfile --help
```

### Python代码方式

```python
from autoregfile.parsers import JSONParser, ExcelParser, YAMLParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator
from autoregfile.regfile_gen import generate_regfile

# 解析配置文件
parser = ExcelParser()  # 或JSONParser()、YAMLParser()
config = parser.parse("config.xlsx")  # 支持的Excel格式将被自动检测

# 生成Verilog寄存器文件
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "output.v")

# 生成APB总线接口
generate_regfile("config.json", "output_apb.v", False, 'apb')

# 生成C语言头文件
header_gen = HeaderGenerator()
header_code = header_gen.generate(config)
header_gen.save(header_code, "output.h")

# 生成Markdown文档
doc_gen = DocGenerator()
doc_content = doc_gen.generate(config)
doc_gen.save(doc_content, "output.md")
```

## Excel格式支持

AutoRegFile支持四种Excel配置格式：

1. **原有单表格格式**：最早实现的格式，全部信息放在同一个表格中
2. **层次化设计**：使用`row_type`列区分寄存器和字段
3. **多表分离设计**：将配置、寄存器和字段分开存储在不同的表格中
4. **改进层次化设计（推荐）**：使用`register`和`field`两列区分寄存器和字段，更符合实际阅读习惯

详细说明请参考文档：[Excel格式使用指南](docs/excel_format_guide.md) 和 [改进层次化设计详解](docs/improved_hierarchical_design.md)。

## 示例

查看 [examples](examples/) 目录获取更多示例：

- [基本用法](examples/basic_usage.py)
- [Excel配置示例](examples/excel_example.py)
- [改进Excel格式](examples/improved_excel_format.py)
- [测试所有寄存器类型](examples/test_all_reg_types.py)

## 文档

详细文档请参考 [docs](docs/) 目录：

- [用户指南](docs/user_guide.md)
- [Excel格式使用指南](docs/excel_format_guide.md)
- [改进层次化设计详解](docs/improved_hierarchical_design.md)
- [API文档](docs/api_docs.md)

## 开发

### 单元测试

```bash
pytest tests/
```

### 构建

```bash
python setup.py build
```

## 许可证

MIT

## 贡献

欢迎提交问题和功能请求。如果您想贡献代码，请提交pull request。
