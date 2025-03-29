# 寄存器文件Verilog设计规范

本文档描述了寄存器文件生成工具中使用的Verilog设计规范，特别是针对自定义总线接口的设计标准和最佳实践。

## 设计原则

1. **硬件接口简化**: 根据寄存器是否有子字段提供不同级别的硬件接口
2. **访问优先级控制**: 支持软件优先或硬件优先两种模式
3. **清晰的模块组织**: 代码结构清晰，便于理解和维护
4. **符合IC设计规范**: 遵循IC设计的编码标准和命名规范

## 寄存器类型与接口设计

### 无子字段的寄存器

对于没有定义子字段的寄存器，提供寄存器级别的接口:

```verilog
// 无子字段的寄存器 - 提供寄存器级接口
output wire [31:0] ctrl_reg_o,  // 寄存器值输出
input  wire [31:0] ctrl_reg_i,  // 硬件写入值
input  wire        ctrl_reg_wen // 硬件写使能
```

### 有子字段的寄存器

对于定义了子字段的寄存器，只提供字段级别的接口:

```verilog
// 有子字段的寄存器 - 只提供字段级接口
output wire [0:0] status_reg_busy_o,    // BUSY字段输出
input  wire [0:0] status_reg_busy_i,    // BUSY字段输入
input  wire       status_reg_busy_wen,  // BUSY字段写使能
output wire [0:0] status_reg_error_o,   // ERROR字段输出
```

这种设计避免了在有子字段的寄存器上同时提供寄存器级和字段级接口可能导致的冲突。

## 访问优先级控制

为满足不同应用场景的需要，支持两种访问优先级模式:

### 软件优先 (默认)

软件通过总线接口的写入操作优先于硬件接口的写入。适用于配置寄存器等场景，确保软件配置能够覆盖硬件的自动更新。

```verilog
// 软件优先级
if (write_active && sel_ctrl_reg) begin
    // 软件写入
    ctrl_reg_reg <= write_data;
end 
else if (ctrl_reg_wen) begin
    // 硬件写入（仅当软件未写入时）
    ctrl_reg_reg <= ctrl_reg_i;
end
```

### 硬件优先

硬件接口的写入操作优先于软件通过总线接口的写入。适用于状态寄存器、中断标志等场景，确保硬件状态能够立即反映在寄存器上。

```verilog
// 硬件优先级
if (int_flag_reg_wen) begin
    // 硬件写入
    int_flag_reg_reg <= int_flag_reg_i;
end
else if (write_active && sel_int_flag_reg) begin
    // 软件写入（仅当硬件未写入时）
    int_flag_reg_reg <= write_data;
end
```

## 配置选项

在寄存器文件配置中，可以通过以下选项控制访问优先级:

### 全局优先级设置

```json
{
  "bus_options": {
    "custom": {
      "access_priority": "sw"  // 全局默认优先级: "sw"或"hw"
    }
  }
}
```

### 寄存器级优先级设置

```json
{
  "registers": [
    {
      "name": "CTRL_REG",
      "address": "0x00",
      "type": "ReadWrite",
      "access_priority": "sw",  // 软件优先
      "fields": [...]
    },
    {
      "name": "INT_FLAG_REG",
      "address": "0x08",
      "type": "Write1Clean",
      "access_priority": "hw",  // 硬件优先
      "fields": [...]
    }
  ]
}
```

### 字段级优先级设置

也可以为单个字段设置优先级:

```json
"fields": [
  {
    "name": "ENABLE",
    "bit_range": "0:0",
    "type": "ReadWrite",
    "access_priority": "sw"  // 软件优先
  },
  {
    "name": "STATUS",
    "bit_range": "1:1",
    "type": "ReadWrite",
    "access_priority": "hw"  // 硬件优先
  }
]
```

## 寄存器类型

支持多种寄存器类型，每种类型具有不同的读写特性:

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| ReadOnly | 只读寄存器，只能通过硬件写入 | 状态寄存器，硬件计数器 |
| ReadWrite | 可读可写寄存器 | 配置寄存器，控制寄存器 |
| WriteOnly | 只写寄存器，写入后不可读取 | 命令寄存器 |
| Write1Clean | 写1清零寄存器 | 中断标志寄存器 |
| Write0Clean | 写0清零寄存器 | 特殊控制寄存器 |
| Write1Set | 写1置位寄存器 | 使能寄存器 |
| Write0Set | 写0置位寄存器 | 特殊控制寄存器 |
| WriteOnce | 只能写一次的寄存器 | 安全配置寄存器 |
| ReadClean | 读取后自动清零寄存器 | 数据队列，FIFO读取 |
| ReadSet | 读取后自动置位寄存器 | 特殊状态寄存器 |
| Write1Pulse | 写1产生脉冲寄存器 | 触发寄存器 |
| Write0Pulse | 写0产生脉冲寄存器 | 特殊触发寄存器 |

## 最佳实践

1. **正确使用寄存器/字段级接口**:
   - 如果寄存器只有一个没有分段的数据，使用寄存器级接口
   - 如果寄存器包含多个功能字段，使用字段级接口

2. **合理设置访问优先级**:
   - 配置寄存器通常使用软件优先
   - 状态寄存器、中断标志通常使用硬件优先

3. **寄存器/字段类型选择**:
   - 按实际功能需要选择合适的类型
   - 使用WriteOnly类型的寄存器进行单向命令传递
   - 使用Write1Clean/Write0Clean类型处理中断和状态标志

4. **字段位宽定义**:
   - 明确指定每个字段的位范围，例如"7:0"表示8位宽字段
   - 指定单个位时可使用单个数字，如"0"表示第0位

## 示例配置

下面是一个包含各种类型寄存器和访问优先级设置的配置示例:

```json
{
  "module_name": "example_regfile",
  "data_width": 32,
  "addr_width": 8,
  "bus_protocol": "custom",
  "bus_options": {
    "custom": {
      "access_priority": "sw",
      "field_level_access": true
    }
  },
  "registers": [
    {
      "name": "CTRL_REG",
      "address": "0x00",
      "type": "ReadWrite",
      "description": "控制寄存器",
      "access_priority": "sw",
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
      "name": "STATUS_REG",
      "address": "0x04",
      "type": "ReadOnly",
      "description": "状态寄存器",
      "access_priority": "hw",
      "fields": [
        {
          "name": "BUSY",
          "bit_range": "0:0",
          "type": "ReadOnly",
          "description": "忙状态位"
        },
        {
          "name": "ERROR",
          "bit_range": "1:1",
          "type": "ReadOnly",
          "description": "错误状态位"
        }
      ]
    },
    {
      "name": "DATA_REG",
      "address": "0x08",
      "type": "ReadWrite",
      "description": "数据寄存器",
      "bits": "31:0",
      "access_priority": "sw"
    }
  ]
}
``` 