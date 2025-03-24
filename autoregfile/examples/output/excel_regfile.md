# excel_regfile 寄存器说明文档

*自动生成于: 2025-03-24 20:22:46*  
*生成器版本: 2.0.0*

## 1. 概述

本文档描述 `excel_regfile` 模块的寄存器配置和操作方法。

- 数据位宽: 32 位
- 地址位宽: 8 位
- 写端口数量: 1
- 读端口数量: 2

## 2. 寄存器列表

| 寄存器名称 | 地址 | 类型 | 描述 |
|------------|------|------|------|
| CTRL_REG | 0x0 | ReadWrite | 控制寄存器 |
| STATUS_REG | 0x0 | ReadOnly | 状态寄存器 |
| INT_FLAGS | 0x0 | ReadClean | 中断标志寄存器 |
| INT_ENABLE | 0x0 | ReadWrite | 中断使能寄存器 |

## 3. 寄存器详细说明

### 3.1 CTRL_REG (0x0)

**描述**: 控制寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| ENABLE | 0 | ReadWrite | 0x0 | 使能位 |
| MODE | 2:1 | ReadWrite | 0x0 | 模式设置 |
| START | 3 | ReadWrite | 0x0 | 启动位 |








### 3.2 STATUS_REG (0x0)

**描述**: 状态寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| BUSY | 0 | ReadOnly | 0x0 | 忙状态标志 |
| ERROR | 1 | ReadOnly | 0x0 | 错误标志 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。







### 3.3 INT_FLAGS (0x0)

**描述**: 中断标志寄存器

**类型**: ReadClean (读取后自动清零的寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DATA_READY | 0 | ReadClean | 0x0 | 数据就绪中断 |
| ERROR_FLAG | 1 | ReadClean | 0x0 | 错误中断 |


**注意**: 该寄存器会在读取后自动清零。






### 3.4 INT_ENABLE (0x0)

**描述**: 中断使能寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DATA_READY_EN | 0 | ReadWrite | 0x0 | 数据就绪中断使能 |
| ERROR_EN | 1 | ReadWrite | 0x0 | 错误中断使能 |









## 4. 编程指南

### 4.1 基本读写操作

```c
// 写寄存器示例
void write_reg(uint32_t addr, uint32_t data) {
    // 根据实际总线接口实现写操作
    // ...
}

// 读寄存器示例
uint32_t read_reg(uint32_t addr) {
    // 根据实际总线接口实现读操作
    // ...
    return data;
}

// 使用示例
void example() {
    // 写入 CTRL_REG
    write_reg(EXCEL_REGFILE_CTRL_REG_ADDR, 0x12345678);
    // 读取 CTRL_REG
    uint32_t ctrl_reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    // 读取 STATUS_REG
    uint32_t status_reg_value = read_reg(EXCEL_REGFILE_STATUS_REG_ADDR);
    // 写入 INT_FLAGS
    write_reg(EXCEL_REGFILE_INT_FLAGS_ADDR, 0x12345678);
    // 读取 INT_FLAGS
    uint32_t int_flags_value = read_reg(EXCEL_REGFILE_INT_FLAGS_ADDR);
    // 写入 INT_ENABLE
    write_reg(EXCEL_REGFILE_INT_ENABLE_ADDR, 0x12345678);
    // 读取 INT_ENABLE
    uint32_t int_enable_value = read_reg(EXCEL_REGFILE_INT_ENABLE_ADDR);
}
```

### 4.2 位域操作

```c
void field_operations() {
    // 设置 CTRL_REG 的 ENABLE 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    reg_value = EXCEL_REGFILE_SET_CTRL_REG_ENABLE(reg_value, 1);
    write_reg(EXCEL_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 ENABLE 位
    reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_CTRL_REG_ENABLE(reg_value);
    // 设置 CTRL_REG 的 MODE 字段
    uint32_t reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    reg_value = EXCEL_REGFILE_SET_CTRL_REG_MODE(reg_value, 0x3);
    write_reg(EXCEL_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 MODE 字段
    reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    uint32_t field_value = EXCEL_REGFILE_GET_CTRL_REG_MODE(reg_value);
    // 设置 CTRL_REG 的 START 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    reg_value = EXCEL_REGFILE_SET_CTRL_REG_START(reg_value, 1);
    write_reg(EXCEL_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 START 位
    reg_value = read_reg(EXCEL_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_CTRL_REG_START(reg_value);
    // 设置 STATUS_REG 的 BUSY 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_STATUS_REG_ADDR);
    reg_value = EXCEL_REGFILE_SET_STATUS_REG_BUSY(reg_value, 1);
    write_reg(EXCEL_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 BUSY 位
    reg_value = read_reg(EXCEL_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_STATUS_REG_BUSY(reg_value);
    // 设置 STATUS_REG 的 ERROR 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_STATUS_REG_ADDR);
    reg_value = EXCEL_REGFILE_SET_STATUS_REG_ERROR(reg_value, 1);
    write_reg(EXCEL_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 ERROR 位
    reg_value = read_reg(EXCEL_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_STATUS_REG_ERROR(reg_value);
    // 设置 INT_FLAGS 的 DATA_READY 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_INT_FLAGS_ADDR);
    reg_value = EXCEL_REGFILE_SET_INT_FLAGS_DATA_READY(reg_value, 1);
    write_reg(EXCEL_REGFILE_INT_FLAGS_ADDR, reg_value);
    
    // 读取 INT_FLAGS 的 DATA_READY 位
    reg_value = read_reg(EXCEL_REGFILE_INT_FLAGS_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_INT_FLAGS_DATA_READY(reg_value);
    // 设置 INT_FLAGS 的 ERROR_FLAG 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_INT_FLAGS_ADDR);
    reg_value = EXCEL_REGFILE_SET_INT_FLAGS_ERROR_FLAG(reg_value, 1);
    write_reg(EXCEL_REGFILE_INT_FLAGS_ADDR, reg_value);
    
    // 读取 INT_FLAGS 的 ERROR_FLAG 位
    reg_value = read_reg(EXCEL_REGFILE_INT_FLAGS_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_INT_FLAGS_ERROR_FLAG(reg_value);
    // 设置 INT_ENABLE 的 DATA_READY_EN 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_INT_ENABLE_ADDR);
    reg_value = EXCEL_REGFILE_SET_INT_ENABLE_DATA_READY_EN(reg_value, 1);
    write_reg(EXCEL_REGFILE_INT_ENABLE_ADDR, reg_value);
    
    // 读取 INT_ENABLE 的 DATA_READY_EN 位
    reg_value = read_reg(EXCEL_REGFILE_INT_ENABLE_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_INT_ENABLE_DATA_READY_EN(reg_value);
    // 设置 INT_ENABLE 的 ERROR_EN 位
    uint32_t reg_value = read_reg(EXCEL_REGFILE_INT_ENABLE_ADDR);
    reg_value = EXCEL_REGFILE_SET_INT_ENABLE_ERROR_EN(reg_value, 1);
    write_reg(EXCEL_REGFILE_INT_ENABLE_ADDR, reg_value);
    
    // 读取 INT_ENABLE 的 ERROR_EN 位
    reg_value = read_reg(EXCEL_REGFILE_INT_ENABLE_ADDR);
    uint8_t bit_value = EXCEL_REGFILE_GET_INT_ENABLE_ERROR_EN(reg_value);
}
```

## 5. 时序要求

- 该模块使用**异步复位**
- 所有寄存器操作都是在时钟上升沿完成
- 读操作无需等待，组合逻辑直接输出
- 写操作在下一个时钟上升沿生效

## 6. 修订历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| 1.0 | 2025-03-24 | 初始版本 | 