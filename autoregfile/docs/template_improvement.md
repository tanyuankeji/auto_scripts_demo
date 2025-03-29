# 寄存器模板改进文档

## 概述

本文档记录了对`custom.v.j2`模板的重构和改进，以生成更符合Verilog设计规范的寄存器文件代码。改进后的模板解决了原有模板中存在的格式问题、逻辑冗余问题，并优化了优先级控制的实现。

## 主要改进

### 1. 代码结构优化

- **清晰的区块划分**：
  - 系统信号部分
  - 总线接口部分
  - 硬件接口部分
  - 内部信号定义部分
  - 常量和字段位置定义部分
  - 寄存器/字段接口连接部分
  - 读取逻辑部分
  - 写入逻辑部分

- **代码注释简化**：
  - 减少冗余注释，提高代码可读性
  - 关键逻辑处保留必要注释
  - 使用一致的注释风格

### 2. 寄存器接口优化

- **接口生成策略改进**：
  - 无子字段寄存器提供寄存器级接口
  - 有子字段寄存器仅提供字段级接口，避免接口冲突
  - 接口信号命名更加规范一致

- **寄存器读写逻辑优化**：
  - 读逻辑使用case语句，提高效率和可读性
  - 写逻辑按寄存器分组，更清晰地表达每个寄存器的行为
  - 特殊类型寄存器（如ReadClean、Write1Pulse等）逻辑更加清晰

### 3. 优先级控制机制增强

- **灵活的优先级设置**：
  - 支持全局级、寄存器级和字段级的优先级设置
  - 软件优先和硬件优先两种模式可自由切换
  - 不同寄存器/字段可设置不同的优先级模式

- **优先级逻辑实现改进**：
  - 优化条件判断语句，减少嵌套层次
  - 优先级控制逻辑更加清晰直观
  - 硬件和软件操作互不干扰

### 4. 字段处理优化

- **字段位置定义规范化**：
  - 统一使用位置参数(POS)、宽度(WIDTH)和掩码(MASK)定义
  - 位域常量命名规范统一
  - 改进掩码计算方式，避免位宽错误

- **字段操作逻辑增强**：
  - 增强类型特定操作（如Write1Clean、Write0Set等）的实现
  - 简化字段读写操作的代码
  - 支持字段级的优先级控制

## 技术细节

### 位域常量定义

```verilog
localparam REG_NAME_FIELD_NAME_POS = <低位>;
localparam REG_NAME_FIELD_NAME_WIDTH = <宽度>;
localparam REG_NAME_FIELD_NAME_MASK = ((1 << <宽度>) - 1) << <低位>;
```

### 优先级控制实现

**硬件优先模式**:
```verilog
// 硬件优先
if (field_wen) begin
    // 硬件写入逻辑
end
else if (write_active && sel_reg) begin
    // 软件写入逻辑
end
```

**软件优先模式**:
```verilog
// 软件优先
if (write_active && sel_reg) begin
    // 软件写入逻辑
end
else if (field_wen) begin
    // 硬件写入逻辑
end
```

### 字段读取接口

```verilog
assign reg_name_field_name_o = reg_name_reg[high:low];
```

## 配置示例

```json
{
  "module_name": "example_regfile",
  "bus_protocol": "custom",
  "bus_options": {
    "custom": {
      "access_priority": "sw",  // 全局默认优先级
      "byte_enable": true
    }
  },
  "registers": [
    {
      "name": "CONTROL",
      "address": "0x00",
      "type": "ReadWrite",
      "access_priority": "sw",  // 寄存器级优先级
      "fields": [
        {
          "name": "ENABLE",
          "bit_range": "0:0",
          "type": "ReadWrite"
        },
        {
          "name": "MODE",
          "bit_range": "2:1",
          "type": "ReadWrite",
          "access_priority": "hw"  // 字段级优先级
        }
      ]
    },
    {
      "name": "STATUS",
      "address": "0x04",
      "type": "ReadOnly",
      "access_priority": "hw",
      "has_no_fields": true
    }
  ]
}
```

## 后续工作

1. 对APB、AXI Lite和Wishbone总线模板进行类似优化
2. 进一步简化生成的Verilog代码，减少冗余
3. 添加更多可配置项，提高模板灵活性
4. 开发单元测试验证生成的寄存器文件功能 