# separated_regfile 寄存器说明文档

*自动生成于: 2025-03-27 21:39:49*  
*生成器版本: 2.0.0*

## 1. 概述

本文档描述 `separated_regfile` 模块的寄存器配置和操作方法。

- 数据位宽: 32 位
- 地址位宽: 8 位
- 写端口数量: 1
- 读端口数量: 1

## 2. 内存映射

# 寄存器内存映射

| 地址 | 寄存器名 | 描述 | 类型 |
|------|----------|------|------|
| 0x00 | CTRL_REG | 控制寄存器 | ReadWrite |
| 0x04 | STATUS_REG | 状态寄存器 | ReadOnly |
| 0x08 | INT_FLAG_REG | 中断标志寄存器 | ReadWrite |
| 0x0C | WRITEONLY_REG | 只写寄存器 | WriteOnly |
| 0x10 | WRITE1SET_REG | 写1置位寄存器 | Write1Set |


## 3. 寄存器列表

| 寄存器名称 | 地址 | 类型 | 描述 |
|------------|------|------|------|
| CTRL_REG | 0x0 | ReadWrite | 控制寄存器 |
| STATUS_REG | 0x0 | ReadOnly | 状态寄存器 |
| INT_FLAG_REG | 0x0 | ReadWrite | 中断标志寄存器 |
| WRITEONLY_REG | 0x0 | WriteOnly | 只写寄存器 |
| WRITE1SET_REG | 0x0 | Write1Set | 写1置位寄存器 |

## 4. 寄存器详细说明

### 4.1 CTRL_REG (0x0)

**描述**: 控制寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| ENABLE | 0 | ReadWrite | 0x0 | 使能位 |
| MODE | 2:1 | ReadWrite | 0x0 | 模式选择 |
| START | 3 | Write1Pulse | 0x0 | 启动位 |









### 4.2 STATUS_REG (0x0)

**描述**: 状态寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| BUSY | 0 | ReadOnly | 0x0 | 忙状态标志 |
| ERROR | 1 | ReadOnly | 0x0 | 错误标志 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。








### 4.3 INT_FLAG_REG (0x0)

**描述**: 中断标志寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DATA_READY | 0 | ReadWrite | 0x0 | 数据就绪中断 |









### 4.4 WRITEONLY_REG (0x0)

**描述**: 只写寄存器

**类型**: WriteOnly (只写寄存器，读取时返回0)
**复位值**: 0x0

**位域描述**:

*没有定义位域*

### 4.5 WRITE1SET_REG (0x0)

**描述**: 写1置位寄存器

**类型**: Write1Set (写1置位对应位，可读)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| BIT0 | 0 | Write1Set | 0x0 | 写1置位的位字段 |





**注意**: 写入1可置位对应位。





## 5. 编程指南

### 5.1 基本读写操作

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
    write_reg(SEPARATED_REGFILE_CTRL_REG_ADDR, 0x12345678);
    // 读取 CTRL_REG
    uint32_t ctrl_reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    // 读取 STATUS_REG
    uint32_t status_reg_value = read_reg(SEPARATED_REGFILE_STATUS_REG_ADDR);
    // 写入 INT_FLAG_REG
    write_reg(SEPARATED_REGFILE_INT_FLAG_REG_ADDR, 0x12345678);
    // 读取 INT_FLAG_REG
    uint32_t int_flag_reg_value = read_reg(SEPARATED_REGFILE_INT_FLAG_REG_ADDR);
    // 写入 WRITEONLY_REG
    write_reg(SEPARATED_REGFILE_WRITEONLY_REG_ADDR, 0x12345678);
    // 写入 WRITE1SET_REG
    write_reg(SEPARATED_REGFILE_WRITE1SET_REG_ADDR, 0x12345678);
    // 读取 WRITE1SET_REG
    uint32_t write1set_reg_value = read_reg(SEPARATED_REGFILE_WRITE1SET_REG_ADDR);
}
```

### 5.2 位域操作

```c
void field_operations() {
    // 设置 CTRL_REG 的 ENABLE 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_CTRL_REG_ENABLE(reg_value, 1);
    write_reg(SEPARATED_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 ENABLE 位
    reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_CTRL_REG_ENABLE(reg_value);
    // 设置 CTRL_REG 的 MODE 字段
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_CTRL_REG_MODE(reg_value, 0x3);
    write_reg(SEPARATED_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 MODE 字段
    reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    uint32_t field_value = SEPARATED_REGFILE_GET_CTRL_REG_MODE(reg_value);
    // 设置 CTRL_REG 的 START 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_CTRL_REG_START(reg_value, 1);
    write_reg(SEPARATED_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 START 位
    reg_value = read_reg(SEPARATED_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_CTRL_REG_START(reg_value);
    // 设置 STATUS_REG 的 BUSY 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_STATUS_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_STATUS_REG_BUSY(reg_value, 1);
    write_reg(SEPARATED_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 BUSY 位
    reg_value = read_reg(SEPARATED_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_STATUS_REG_BUSY(reg_value);
    // 设置 STATUS_REG 的 ERROR 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_STATUS_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_STATUS_REG_ERROR(reg_value, 1);
    write_reg(SEPARATED_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 ERROR 位
    reg_value = read_reg(SEPARATED_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_STATUS_REG_ERROR(reg_value);
    // 设置 INT_FLAG_REG 的 DATA_READY 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_INT_FLAG_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_INT_FLAG_REG_DATA_READY(reg_value, 1);
    write_reg(SEPARATED_REGFILE_INT_FLAG_REG_ADDR, reg_value);
    
    // 读取 INT_FLAG_REG 的 DATA_READY 位
    reg_value = read_reg(SEPARATED_REGFILE_INT_FLAG_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_INT_FLAG_REG_DATA_READY(reg_value);
    // 设置 WRITE1SET_REG 的 BIT0 位
    uint32_t reg_value = read_reg(SEPARATED_REGFILE_WRITE1SET_REG_ADDR);
    reg_value = SEPARATED_REGFILE_SET_WRITE1SET_REG_BIT0(reg_value, 1);
    write_reg(SEPARATED_REGFILE_WRITE1SET_REG_ADDR, reg_value);
    
    // 读取 WRITE1SET_REG 的 BIT0 位
    reg_value = read_reg(SEPARATED_REGFILE_WRITE1SET_REG_ADDR);
    uint8_t bit_value = SEPARATED_REGFILE_GET_WRITE1SET_REG_BIT0(reg_value);
}
```

## 6. 时序要求

- 该模块使用**异步复位**
- 所有寄存器操作都是在时钟上升沿完成
- 读操作无需等待，组合逻辑直接输出
- 写操作在下一个时钟上升沿生效

## 7. 修订历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| 1.0 | 2025-03-27 | 初始版本 | 