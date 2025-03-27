# 改进层次化设计格式详解

## 1. 概述

改进层次化设计是AutoRegFile支持的最新Excel配置格式，它使用`register`和`field`两列代替传统的`row_type`列，更符合实际工作中的寄存器表格习惯。本文档详细介绍这种格式的结构、特点和使用方法。

## 2. 格式结构

改进层次化设计Excel文件包含两个表格：
- **Config**：全局配置表，定义模块名称、数据宽度等基本参数
- **RegisterFields**：寄存器和字段定义表，以层次化方式组织寄存器和字段

### 2.1 Config表格式

Config表用于定义全局配置参数，包含以下列：

| parameter | value |
|-----------|-------|
| module_name | regfile_name |
| data_width | 32 |
| addr_width | 8 |
| bus_protocol | apb |
| num_write_ports | 1 |
| num_read_ports | 1 |
| sync_reset | false |
| reset_value | 0x00000000 |
| byte_enable | true |

### 2.2 RegisterFields表格式

RegisterFields表以层次化方式组织寄存器和字段，主要列包括：

| register | field | address | bits | sw_access | hw_access | type | reset_value | description | function | lock | magic |
|----------|-------|---------|------|-----------|-----------|------|-------------|-------------|----------|------|-------|
| CTRL_REG |       | 0x00    |      | READ_WRITE|           | ReadWrite | 0x00000000 | 控制寄存器 |          |      |       |
|          | ENABLE|         | 0    | READ_WRITE|           | ReadWrite | 0 | 使能位 | 系统使能控制 | | |
|          | MODE  |         | 2:1  | READ_WRITE|           | ReadWrite | 0 | 模式选择 | 00=空闲, 01=低功耗 | | |

**列说明**：
- **register**：寄存器名称（只在寄存器行填写）
- **field**：字段名称（只在字段行填写）
- **address**：寄存器地址（只在寄存器行填写）
- **bits**：字段位范围（只在字段行填写）
- **sw_access**：软件访问类型（READ_WRITE, READ, WRITE）
- **hw_access**：硬件访问类型（READ_WRITE, READ, WRITE）
- **type**：寄存器/字段类型（如ReadWrite, ReadOnly, WriteOnly等）
- **reset_value**：复位值
- **description**：描述信息
- **function**：功能说明（主要用于字段）
- **lock**：锁依赖
- **magic**：魔数依赖

## 3. 数据组织规则

改进层次化设计遵循以下组织规则：

1. **寄存器定义行**：
   - `register`列填写寄存器名称
   - `field`列保持为空
   - `address`列填写寄存器地址
   - 其他列填写寄存器级属性

2. **字段定义行**：
   - `register`列保持为空
   - `field`列填写字段名称
   - `bits`列填写字段位范围
   - 其他列填写字段级属性

3. **层次关系**：
   - 寄存器行后紧跟该寄存器的所有字段行
   - 新的寄存器定义表示上一个寄存器的字段定义结束

## 4. 特殊属性

### 4.1 锁依赖

通过`lock`列可以定义字段的锁定依赖关系：

| register | field | ... | lock | ... |
|----------|-------|-----|------|-----|
| LOCK_REG |       | ... |      | ... |
|          | LOCKED_FIELD | ... | CTRL_REG.ENABLE | ... |

上例表示`LOCKED_FIELD`字段只有在`CTRL_REG.ENABLE`为1时才能被修改。

### 4.2 魔数依赖

通过`magic`列可以定义字段的魔数依赖关系：

| register | field | ... | magic | ... |
|----------|-------|-----|-------|-----|
| MAGIC_REG |      | ... |       | ... |
|           | MAGIC_FIELD | ... | MAGIC_REG | ... |

上例表示`MAGIC_FIELD`字段只有在向`MAGIC_REG`写入特定值后才能被修改。

## 5. 与其他格式的对比

### 5.1 与层次化设计的对比

| 特性 | 改进层次化设计 | 层次化设计 |
|------|--------------|----------|
| 区分方式 | register/field列 | row_type列 |
| 直观性 | 更直观，符合表格习惯 | 较直观，但使用非常规列 |
| 编辑便捷性 | 更便捷，符合工作习惯 | 一般 |
| 兼容性 | 列名大小写不敏感 | 列名固定 |

### 5.2 与多表分离设计的对比

| 特性 | 改进层次化设计 | 多表分离设计 |
|------|--------------|------------|
| 表格数量 | 2个（Config + RegisterFields） | 3个（Config + Registers + Fields） |
| 直观性 | 寄存器和字段关系一目了然 | 需要跨表查看关系 |
| 适用场景 | 中小规模项目，强调直观性 | 大型项目，强调模块化 |

## 6. 实际示例

### 6.1 完整示例

```python
# 创建改进层次化设计Excel文件
import pandas as pd

# 全局配置
config_data = {
    'parameter': ['module_name', 'data_width', 'addr_width', 'bus_protocol'],
    'value': ['my_regfile', 32, 8, 'apb']
}
config_df = pd.DataFrame(config_data)

# 寄存器和字段数据
regfield_data = {
    'register': ['CTRL_REG', '', '', 'STATUS_REG', '', ''],
    'field': ['', 'ENABLE', 'MODE', '', 'BUSY', 'ERROR'],
    'address': ['0x00', '', '', '0x04', '', ''],
    'bits': ['', '0', '2:1', '', '0', '1'],
    'sw_access': ['READ_WRITE', 'READ_WRITE', 'READ_WRITE', 'READ', 'READ', 'READ'],
    'hw_access': ['', '', '', 'WRITE', 'WRITE', 'WRITE'],
    'type': ['ReadWrite', 'ReadWrite', 'ReadWrite', 'ReadOnly', 'ReadOnly', 'ReadOnly'],
    'reset_value': ['0x00000000', '0', '0', '0x00000000', '0', '0'],
    'description': ['控制寄存器', '使能位', '模式选择', '状态寄存器', '忙状态', '错误状态'],
    'function': ['', '系统使能控制', '00=空闲,01=低功耗', '', '指示系统忙状态', '指示错误状态'],
    'lock': ['', '', '', '', '', ''],
    'magic': ['', '', '', '', '', '']
}
regfield_df = pd.DataFrame(regfield_data)

# 保存Excel文件
with pd.ExcelWriter('my_regfile.xlsx') as writer:
    config_df.to_excel(writer, sheet_name='Config', index=False)
    regfield_df.to_excel(writer, sheet_name='RegisterFields', index=False)
```

### 6.2 解析示例

```python
from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator

# 解析Excel配置
parser = ExcelParser()
config = parser.parse("my_regfile.xlsx")  # 自动检测为改进层次化设计格式

# 生成Verilog代码
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "my_regfile.v")
```

## 7. 最佳实践

1. **列名一致性**：虽然列名大小写不敏感，但建议在Excel文件中保持一致的命名风格
2. **寄存器分组**：相关的寄存器可以放在一起，便于阅读和维护
3. **文档注释**：充分利用`description`和`function`列提供清晰的文档
4. **地址规划**：建议按照4字节对齐安排寄存器地址
5. **避免特殊字符**：在寄存器和字段名中避免使用特殊字符
6. **复位值**：明确指定所有寄存器和字段的复位值
7. **访问类型**：明确指定软件/硬件访问类型

## 8. 结论

改进层次化设计格式结合了直观性和易用性，特别适合需要清晰表达寄存器结构的场景。它保持了表格的简洁性，同时提供了丰富的功能支持，是AutoRegFile推荐的首选配置格式。 