# Excel寄存器配置模板

本文档提供了Excel寄存器配置文件的模板和示例，演示如何正确配置各种类型的寄存器，特别是特殊寄存器类型和位宽设置。

## 基本结构

推荐使用改进的层次结构设计（单工作表模式），Excel文件应包含一个名为`RegisterFields`的工作表，其中包含以下列：

| 列名 | 说明 | 必填 | 示例 |
|-----|------|-----|-----|
| register | 寄存器名称 | 是 | CTRL_REG |
| field | 字段名称 | 否（无子字段寄存器留空） | ENABLE |
| bit_range | 字段位范围 | 仅字段必填 | 0:0 或 7:0 |
| type | 寄存器/字段类型 | 是 | ReadWrite |
| reset_value | 复位值 | 否 | 0x0 |
| description | 描述 | 否 | 控制寄存器 |
| address | 寄存器地址 | 是（每个寄存器首行） | 0x00 |
| bits | 无子字段寄存器位宽 | 仅无子字段寄存器需要 | 7:0 |

## 示例配置

以下是一个完整的寄存器配置表格示例：

### RegisterFields工作表示例

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| CTRL_REG | ENABLE | 0:0 | ReadWrite | 0x0 | 使能位 | 0x00 | |
| CTRL_REG | MODE | 2:1 | ReadWrite | 0x0 | 模式选择 | | |
| CTRL_REG | START | 3:3 | Write1Pulse | 0x0 | 启动位（写1自动清零） | | |
| STATUS_REG | BUSY | 0:0 | ReadOnly | 0x0 | 忙状态标志 | 0x04 | |
| STATUS_REG | ERROR | 1:1 | ReadOnly | 0x0 | 错误标志 | | |
| INT_FLAG_REG | DATA_READY | 0:0 | Write1Clean | 0x0 | 数据就绪中断 | 0x08 | |
| WRITEONLY_REG | | | WriteOnly | 0x0 | 只写寄存器 | 0x0C | 7:0 |
| LOCK_TEST_REG | LOCKED_FIELD | 7:0 | ReadWrite | 0x55 | 受锁控制的字段 | 0x14 | |
| LOCK_TEST_REG | MAGIC_FIELD | 15:8 | ReadWrite | 0xAA | 魔数控制的字段 | | |
| WRITE1SET_REG | | | Write1Set | 0x0 | 写1置位寄存器 | 0x1C | 7:0 |
| READ_CLEAN_REG | | | ReadClean | 0x0 | 读取后自动清零 | 0x20 | 31:0 |
| WRITE_ONCE_REG | | | WriteOnce | 0x0 | 只能写一次的寄存器 | 0x24 | 31:0 |
| PULSE_REG | TRIG0 | 0:0 | Write1Pulse | 0x0 | 触发脉冲0 | 0x28 | |
| PULSE_REG | TRIG1 | 1:1 | Write1Pulse | 0x0 | 触发脉冲1 | | |

## 特殊寄存器配置重点

### 无子字段寄存器

对于没有子字段的寄存器（如`WRITEONLY_REG`），必须：
1. 在`field`列留空
2. 在`bits`列指定位宽（如`7:0`表示8位宽度）

示例行：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITEONLY_REG | | | WriteOnly | 0x0 | 只写寄存器 | 0x0C | 7:0 |

### 写1置位寄存器（Write1Set）

写1置位寄存器通常使用无子字段模式，设置如下：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITE1SET_REG | | | Write1Set | 0x0 | 写1置位寄存器 | 0x1C | 7:0 |

### 脉冲型寄存器（Write1Pulse）

脉冲型寄存器可以有子字段，每个字段作为独立的触发源：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| PULSE_REG | TRIG0 | 0:0 | Write1Pulse | 0x0 | 触发脉冲0 | 0x28 | |
| PULSE_REG | TRIG1 | 1:1 | Write1Pulse | 0x0 | 触发脉冲1 | | |

也可以配置为无子字段的脉冲寄存器：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| PULSE_NO_FIELD_REG | | | Write1Pulse | 0x0 | 无子字段脉冲 | 0x2C | 7:0 |

### 只能写一次寄存器（WriteOnce）

只能写一次的寄存器通常配置为无子段模式：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITE_ONCE_REG | | | WriteOnce | 0x0 | 只能写一次 | 0x24 | 31:0 |

## 常见错误与正确配置

### 错误1：特殊寄存器位宽未指定

**错误配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITEONLY_REG | | | WriteOnly | 0x0 | 只写寄存器 | 0x0C | |

**正确配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITEONLY_REG | | | WriteOnly | 0x0 | 只写寄存器 | 0x0C | 7:0 |

### 错误2：为特殊寄存器添加了不必要的字段

**错误配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITE1SET_REG | BIT0 | 0:0 | Write1Set | 0x0 | 0号位 | 0x1C | |

**正确配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| WRITE1SET_REG | | | Write1Set | 0x0 | 写1置位寄存器 | 0x1C | 7:0 |

### 错误3：位范围格式错误

**错误配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| STATUS_REG | BUSY | 0-0 | ReadOnly | 0x0 | 忙状态标志 | 0x04 | |

**正确配置**：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| STATUS_REG | BUSY | 0:0 | ReadOnly | 0x0 | 忙状态标志 | 0x04 | |

## 导入注意事项

1. 确保Excel文件使用正确的格式和列名
2. 对于特殊寄存器，始终在`bits`列指定位宽
3. 对于有子字段的寄存器，确保字段位置不重叠且在寄存器宽度范围内
4. 地址只需在每个寄存器的首行填写
5. 位范围使用冒号分隔（如`7:0`），不要使用其他分隔符

## 验证方法

生成寄存器文件时，使用`--debug`选项查看处理日志：

```bash
python -m autoregfile.regfile_gen -c ./examples/test/test_regfile.xlsx -o ./examples/test/output.v -p custom --debug
```

检查日志中的警告和错误信息，确保每个寄存器都被正确识别并处理。 