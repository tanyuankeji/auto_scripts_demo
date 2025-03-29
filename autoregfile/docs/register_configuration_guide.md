# 寄存器配置指南

本文档提供了关于如何在Excel或JSON文件中配置各种类型寄存器的详细指南，特别关注位宽设置、字段定义和特殊寄存器类型的处理。

## 目录

1. [基本概念](#基本概念)
2. [Excel配置文件格式](#excel配置文件格式)
3. [JSON配置文件格式](#json配置文件格式)
4. [寄存器类型详解](#寄存器类型详解)
5. [位宽设置指南](#位宽设置指南)
6. [字段配置详解](#字段配置详解)
7. [访问优先级控制](#访问优先级控制)
8. [特殊寄存器配置示例](#特殊寄存器配置示例)
9. [常见问题与解决方法](#常见问题与解决方法)

## 基本概念

在寄存器文件生成系统中，我们使用以下关键概念：

- **寄存器（Register）**：CPU/总线可访问的存储单元，有特定的地址和类型
- **字段（Field）**：寄存器内的位段，可以独立访问和控制
- **位宽（Width）**：寄存器或字段的位数
- **位范围（Bit Range）**：字段在寄存器中的位置，格式为"高位:低位"
- **类型（Type）**：定义寄存器或字段的访问行为（如只读、读写、写1清零等）

## Excel配置文件格式

Excel配置文件是定义寄存器的推荐方式，支持两种主要格式：

### 改进的层次结构设计（推荐）

使用单个工作表`RegisterFields`定义所有寄存器和字段：

| register | field | bit_range | type | reset_value | description | address | bits |
|----------|-------|-----------|------|-------------|-------------|---------|------|
| CTRL_REG | ENABLE | 0:0 | ReadWrite | 0x0 | 使能位 | 0x00 | |
| CTRL_REG | MODE | 2:1 | ReadWrite | 0x0 | 模式选择 | | |
| STATUS_REG | BUSY | 0:0 | ReadOnly | 0x0 | 忙状态标志 | 0x04 | |
| WRITEONLY_REG | | | WriteOnly | 0x0 | 只写寄存器 | 0x0C | 7:0 |

**注意事项：**
- `bits`列用于定义无子字段寄存器的位宽（如`WRITEONLY_REG`）
- 地址只需在寄存器的第一行定义
- 寄存器类型在第一行定义，字段可以有自己的类型

### 传统的分离式设计

使用两个工作表：`Registers`和`Fields`分别定义寄存器和字段。

## JSON配置文件格式

JSON配置更灵活，适合编程创建或手动微调：

```json
{
  "module_name": "example_regfile",
  "data_width": 32,
  "addr_width": 8,
  "bus_protocol": "custom",
  "registers": [
    {
      "name": "CTRL_REG",
      "address": "0x00",
      "type": "ReadWrite",
      "description": "控制寄存器",
      "fields": [
        {
          "name": "ENABLE",
          "bit_range": "0:0",
          "type": "ReadWrite",
          "description": "使能位"
        },
        {
          "name": "MODE",
          "bit_range": "2:1",
          "type": "ReadWrite",
          "description": "模式选择"
        }
      ]
    },
    {
      "name": "WRITEONLY_REG",
      "address": "0x0C",
      "type": "WriteOnly",
      "description": "只写寄存器",
      "bits": "7:0"
    }
  ]
}
```

## 寄存器类型详解

系统支持多种寄存器类型，每种类型具有特定的行为：

| 类型 | 默认位宽 | 描述 | 使用场景 |
|------|--------|------|---------|
| ReadOnly | 32 | 只读寄存器，硬件可写入，软件只能读取 | 状态寄存器、硬件计数器值 |
| ReadWrite | 32 | 读写寄存器，硬件和软件都可读写 | 配置寄存器、控制寄存器 |
| WriteOnly | 8 | 只写寄存器，软件可写入但读回为0 | 命令寄存器、触发器 |
| Write1Clean | 32 | 写1清零寄存器，软件写1清除对应位 | 中断标志寄存器 |
| Write0Clean | 32 | 写0清零寄存器，软件写0清除对应位 | 特殊控制寄存器 |
| Write1Set | 8 | 写1置位寄存器，软件写1置位对应位 | 使能控制、标志设置 |
| Write0Set | 32 | 写0置位寄存器，软件写0置位对应位 | 特殊控制寄存器 |
| WriteOnce | 32 | 只能写一次的寄存器 | 安全配置、启动设置 |
| WriteOnlyOnce | 32 | 只能写一次且只写的寄存器 | 安全密钥、初始化命令 |
| ReadClean | 32 | 读取后自动清零寄存器 | FIFO数据读取 |
| ReadSet | 32 | 读取后自动置位寄存器 | 特殊状态标志 |
| Write1Pulse | 32 | 写1产生脉冲寄存器，自动在下一周期清零 | 触发命令 |
| Write0Pulse | 32 | 写0产生脉冲寄存器，自动在下一周期清零 | 特殊触发命令 |

**重要提示**：无子字段的特殊类型寄存器（如`WriteOnly`和`Write1Set`）通常使用8位宽度作为默认值。

## 位宽设置指南

位宽设置时，系统按照以下优先级确定寄存器的位宽：

1. **明确的bit_range**（首选）：通过`bit_range`属性指定，例如`"bit_range": "7:0"`表示8位宽
2. **bits属性**：通过`bits`属性指定，例如`"bits": "7:0"`
3. **类型默认值**：如果未指定，使用寄存器类型的默认值（见上表）
4. **全局数据宽度**：如果前三种方式均未提供，使用全局`data_width`（默认32位）

### 最佳实践

- 总是明确指定特殊寄存器的位宽（通过`bit_range`或`bits`属性）
- 对于非标准位宽的寄存器（非32位），必须指定位宽
- 单比特位可以使用单个数字指定，例如`"bit_range": "0"`
- 使用0-based索引（从0开始），例如8位寄存器的范围是`7:0`

## 字段配置详解

字段配置的关键点：

- **必须设置 bit_range**：所有字段必须指定位置范围
- **可选的类型**：字段可以有自己的类型，与寄存器类型不同
- **可选的复位值**：字段可以定义自己的复位值

### 无子字段寄存器

对于不需要细分位段的寄存器（如`WRITEONLY_REG`和`Write1SET_REG`），应该：

1. 在Excel中：留空`field`列，填写`bits`列（例如`7:0`表示8位宽度）
2. 在JSON中：不定义`fields`数组或设为空数组，添加`bits`属性

```json
{
  "name": "WRITEONLY_REG",
  "address": "0x0C",
  "type": "WriteOnly",
  "bits": "7:0",
  "fields": []  // 明确指示没有子字段
}
```

## 访问优先级控制

系统支持两种访问优先级模式，用于控制软件（通过总线）和硬件（通过专用接口）的访问优先级：

- **软件优先（默认）**：总线写入优先于硬件接口
- **硬件优先**：硬件接口写入优先于总线

### 设置优先级

在全局级、寄存器级或字段级设置优先级：

```json
{
  "bus_options": {
    "custom": {
      "access_priority": "sw"  // 全局默认：sw或hw
    }
  },
  "registers": [
    {
      "name": "CTRL_REG",
      "access_priority": "sw",  // 寄存器级设置
      "fields": [
        {
          "name": "STATUS",
          "access_priority": "hw"  // 字段级设置（覆盖寄存器设置）
        }
      ]
    }
  ]
}
```

## 特殊寄存器配置示例

### 只写寄存器（WriteOnly）

```json
{
  "name": "COMMAND_REG",
  "address": "0x10",
  "type": "WriteOnly",
  "bits": "7:0",  // 指定8位宽
  "description": "命令寄存器，写入触发操作，读回为0"
}
```

### 写1置位寄存器（Write1Set）

```json
{
  "name": "CONTROL_SET_REG",
  "address": "0x14",
  "type": "Write1Set",
  "bits": "7:0",  // 指定8位宽
  "description": "控制置位寄存器，写1置位对应位，写0保持不变"
}
```

### 只读寄存器（ReadOnly）

```json
{
  "name": "STATUS_REG",
  "address": "0x04",
  "type": "ReadOnly",
  "description": "状态寄存器，只能由硬件更新",
  "fields": [
    {
      "name": "BUSY",
      "bit_range": "0:0",
      "description": "忙状态位"
    },
    {
      "name": "ERROR",
      "bit_range": "1:1",
      "description": "错误标志位"
    }
  ]
}
```

### 写1清零寄存器（Write1Clean）

```json
{
  "name": "INT_FLAG_REG",
  "address": "0x08",
  "type": "Write1Clean",
  "description": "中断标志寄存器，写1清除对应中断位",
  "fields": [
    {
      "name": "DATA_READY",
      "bit_range": "0:0",
      "description": "数据就绪中断"
    },
    {
      "name": "ERROR",
      "bit_range": "1:1",
      "description": "错误中断"
    }
  ]
}
```

### 写1脉冲寄存器（Write1Pulse）

```json
{
  "name": "TRIGGER_REG",
  "address": "0x20",
  "type": "Write1Pulse",
  "description": "触发寄存器，写1后在下一个时钟周期自动清零",
  "fields": [
    {
      "name": "START",
      "bit_range": "0:0",
      "description": "启动操作"
    },
    {
      "name": "ABORT",
      "bit_range": "1:1",
      "description": "中止操作"
    }
  ]
}
```

## 常见问题与解决方法

### 问题1：位宽设置不正确

**症状**：生成的寄存器使用了32位宽度，而不是预期的8位。

**解决方法**：
- 确保在Excel的`bits`列或JSON的`bits`属性中明确指定位宽，例如`7:0`
- 对于特殊类型寄存器，不要定义子字段，留空`field`列或使用空的`fields`数组
- 在日志中查找与位宽相关的警告或错误

### 问题2：特殊寄存器未正确识别

**症状**：特殊类型寄存器（如WriteOnly或Write1Set）被错误地识别为有子字段。

**解决方法**：
- 确保Excel中没有为这些寄存器定义字段
- 检查生成器日志，确认寄存器被识别为特殊类型
- 使用`--debug`选项运行生成器，查看更详细的处理信息

### 问题3：字段位置重叠

**症状**：生成的代码有错误，或字段位置冲突警告。

**解决方法**：
- 确保所有字段的`bit_range`不重叠
- 检查高位和低位顺序是否正确（高位在前，例如`15:8`表示8位宽度的字段，位置在8-15）
- 验证所有字段位置在寄存器宽度范围内

### 问题4：寄存器行为不符合预期

**症状**：生成的寄存器不按预期工作（如清零、置位等）。

**解决方法**：
- 确认使用了正确的寄存器类型
- 检查寄存器及其字段的访问优先级设置
- 参考上述寄存器类型表，确保使用了正确的类型 