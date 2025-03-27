# AutoRegFile Excel格式使用指南

## 1. 概述

AutoRegFile是一个自动生成寄存器文件的工具，支持多种Excel格式的配置文件。本文档详细介绍了AutoRegFile支持的各种Excel格式，特别是新添加的改进层次化设计格式，以帮助用户选择最适合自己需求的配置方式。

## 2. 功能特性

AutoRegFile目前支持以下特性：

- 多种Excel格式配置文件解析
- 自动检测配置文件格式
- 生成Verilog寄存器文件
- 生成APB总线接口
- 生成C语言头文件
- 生成Markdown文档
- 支持多种寄存器类型（ReadWrite, ReadOnly, WriteOnly, Write1Clear, Write1Set等）
- 支持字段级锁依赖和魔数依赖

## 3. 支持的Excel格式

AutoRegFile目前支持四种Excel配置格式：

1. **原有单表格格式**：最早实现的格式，全部信息放在同一个表格中
2. **层次化设计**：使用`row_type`列区分寄存器和字段
3. **多表分离设计**：将配置、寄存器和字段分开存储在不同的表格中
4. **改进层次化设计**：使用`register`和`field`两列区分寄存器和字段，更符合实际阅读习惯

### 3.1 原有单表格格式

最初的单表格格式将所有信息都放在同一个表格中，通过特定的列名来区分寄存器和字段信息。

### 3.2 层次化设计

层次化设计使用单个表格，但通过`row_type`列来区分寄存器行和字段行，使结构更清晰可见。

| row_type | name | address_or_bits | type | reset_value | description | sw_access | hw_access | function |
|----------|------|-----------------|------|-------------|-------------|-----------|-----------|----------|
| Register | CTRL_REG | 0x00 | ReadWrite | 0x00000000 | 控制寄存器 | READ_WRITE | | |
| Field | ENABLE | 0 | ReadWrite | 0 | 使能位 | READ_WRITE | | 系统使能控制 |
| Field | MODE | 2:1 | ReadWrite | 0 | 模式选择 | READ_WRITE | | 00=空闲, 01=低功耗 |

### 3.3 多表分离设计

多表分离设计将配置、寄存器和字段分开存储在不同的表格中，适合大量寄存器和字段的情况。

Excel文件包含三个表格：
- **Config**：全局配置信息
- **Registers**：寄存器定义
- **Fields**：字段定义

### 3.4 改进层次化设计（推荐）

改进层次化设计是最新实现的格式，使用`register`和`field`两列代替`row_type`，更符合实际工作中的寄存器表格习惯。

| register | field | address | bits | sw_access | hw_access | type | reset_value | description | function | lock | magic |
|----------|-------|---------|------|-----------|-----------|------|-------------|-------------|----------|------|-------|
| CTRL_REG |       | 0x00    |      | READ_WRITE|           | ReadWrite | 0x00000000 | 控制寄存器 |          |      |       |
|          | ENABLE|         | 0    | READ_WRITE|           | ReadWrite | 0 | 使能位 | The enable bit | | |
|          | MODE  |         | 2:1  | READ_WRITE|           | ReadWrite | 0 | 模式选择 | 00=空闲, 01=低功耗 | | |
| STATUS_REG |     | 0x04    |      | READ      | WRITE     | ReadOnly | 0x00000000 | 状态寄存器 |          |      |       |
|          | BUSY  |         | 0    | READ      | WRITE     | ReadOnly | 0 | 忙状态标志 | 指示系统当前是否正在运行 | | |

#### 主要特点：

- 使用`register`和`field`两列清晰区分寄存器和字段
- 寄存器行在`register`列填写寄存器名，`field`列留空
- 字段行在`field`列填写字段名，`register`列留空
- 字段紧跟在其所属寄存器后面
- 支持字段级的锁依赖和魔数依赖
- 列名大小写不敏感，方便使用

## 4. 如何选择合适的格式

- **简单项目**：对于简单的寄存器定义，可以使用原有单表格格式或层次化设计
- **大型项目**：对于包含大量寄存器的复杂项目，推荐使用改进层次化设计或多表分离设计
- **团队协作**：如果需要多人协作编辑，多表分离设计可能更合适
- **清晰直观**：如果希望配置文件更易于阅读和编辑，推荐使用改进层次化设计

## 5. 使用方法

### 5.1 安装

```bash
pip install autoregfile
```

### 5.2 创建Excel配置文件

根据需要选择一种Excel格式创建配置文件。推荐使用改进层次化设计格式，创建包含`Config`和`RegisterFields`两个表格的Excel文件。

### 5.3 生成寄存器文件

```bash
# 命令行方式
autoregfile -i your_config.xlsx -o output_directory

# Python代码方式
from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator
from autoregfile.regfile_gen import generate_regfile

# 解析Excel配置（自动检测格式）
parser = ExcelParser()
config = parser.parse("your_config.xlsx")

# 生成Verilog文件
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "output.v")

# 生成APB总线接口
generate_regfile("config.json", "output_apb.v", False, 'apb')
```

### 5.4 示例脚本

AutoRegFile提供了示例脚本，展示如何使用不同格式的Excel文件：

```bash
# 运行示例
python -m autoregfile.examples.improved_excel_format
```

## 6. 测试项

AutoRegFile包含了全面的测试，验证各种Excel格式和功能：

1. **格式检测测试**：测试自动检测Excel格式的功能
2. **解析测试**：测试解析不同Excel格式的功能
3. **寄存器类型测试**：测试支持的所有寄存器类型
4. **字段特性测试**：测试字段级锁依赖和魔数依赖
5. **代码生成测试**：测试生成的Verilog代码、APB接口等

运行测试：

```bash
# 运行所有测试
python -m autoregfile.test.run_all_tests

# 测试特定格式
python -m autoregfile.examples.improved_excel_format
```

## 7. 注意事项

- Excel文件中的列名大小写不敏感，但建议保持一致性
- 确保每个寄存器的地址是唯一的
- 字段的位范围不应重叠
- 测试生成的代码，确保功能符合预期

## 8. 常见问题

**Q: 如何添加锁依赖和魔数依赖？**  
A: 在改进层次化设计格式中，使用`lock`和`magic`列添加依赖。

**Q: 支持哪些寄存器类型？**  
A: 支持ReadWrite, ReadOnly, WriteOnly, Write1Clear, Write1Set, ReadClean等多种类型。

**Q: 如何处理大小端问题？**  
A: 可以在Config表中配置端序。

## 9. 更新历史

- **v1.0.0**: 初始版本，支持原有单表格格式
- **v1.1.0**: 添加层次化设计格式
- **v1.2.0**: 添加多表分离设计格式
- **v2.0.0**: 添加改进层次化设计格式，支持字段级锁依赖和魔数依赖 