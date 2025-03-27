# extended_field_regfile 寄存器说明文档

*自动生成于: 2025-03-27 20:51:43*  
*生成器版本: 2.0.0*

## 1. 概述

本文档描述 `extended_field_regfile` 模块的寄存器配置和操作方法。

- 数据位宽: 32 位
- 地址位宽: 8 位
- 写端口数量: 1
- 读端口数量: 2

## 2. 内存映射

# 内存映射



## 3. 寄存器列表

| 寄存器名称 | 地址 | 类型 | 描述 |
|------------|------|------|------|
| CTRL_REG | 0x0 | ReadWrite | 控制寄存器 |
| STATUS_REG | 0x0 | ReadOnly | 状态寄存器 |
| LOCK_REG | 0x0 | ReadWrite | 锁定寄存器 |
| MAGIC_REG | 0x0 | ReadWrite | 魔术数字寄存器 |

## 4. 寄存器详细说明

### 4.1 CTRL_REG (0x0)

**描述**: 控制寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| ENABLE | 0 | ReadWrite | 0x0 | 使能位 |
| START | 1 | ReadWrite | 0x0 | 启动位 |









### 4.2 STATUS_REG (0x0)

**描述**: 状态寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| BUSY | 0 | ReadOnly | 0x0 | 忙状态标志 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。








### 4.3 LOCK_REG (0x0)

**描述**: 锁定寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| LOCK_BIT | 0 | ReadWrite | 0x0 | 锁定位 |









### 4.4 MAGIC_REG (0x0)

**描述**: 魔术数字寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| MAGIC_VALUE | 31:0 | ReadWrite | 0x0 | 魔术数字值 |










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
    write_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR, 0x12345678);
    // 读取 CTRL_REG
    uint32_t ctrl_reg_value = read_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR);
    // 读取 STATUS_REG
    uint32_t status_reg_value = read_reg(EXTENDED_FIELD_REGFILE_STATUS_REG_ADDR);
    // 写入 LOCK_REG
    write_reg(EXTENDED_FIELD_REGFILE_LOCK_REG_ADDR, 0x12345678);
    // 读取 LOCK_REG
    uint32_t lock_reg_value = read_reg(EXTENDED_FIELD_REGFILE_LOCK_REG_ADDR);
    // 写入 MAGIC_REG
    write_reg(EXTENDED_FIELD_REGFILE_MAGIC_REG_ADDR, 0x12345678);
    // 读取 MAGIC_REG
    uint32_t magic_reg_value = read_reg(EXTENDED_FIELD_REGFILE_MAGIC_REG_ADDR);
}
```

### 5.2 位域操作

```c
void field_operations() {
    // 设置 CTRL_REG 的 ENABLE 位
    uint32_t reg_value = read_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR);
    reg_value = EXTENDED_FIELD_REGFILE_SET_CTRL_REG_ENABLE(reg_value, 1);
    write_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 ENABLE 位
    reg_value = read_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = EXTENDED_FIELD_REGFILE_GET_CTRL_REG_ENABLE(reg_value);
    // 设置 CTRL_REG 的 START 位
    uint32_t reg_value = read_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR);
    reg_value = EXTENDED_FIELD_REGFILE_SET_CTRL_REG_START(reg_value, 1);
    write_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 START 位
    reg_value = read_reg(EXTENDED_FIELD_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = EXTENDED_FIELD_REGFILE_GET_CTRL_REG_START(reg_value);
    // 设置 STATUS_REG 的 BUSY 位
    uint32_t reg_value = read_reg(EXTENDED_FIELD_REGFILE_STATUS_REG_ADDR);
    reg_value = EXTENDED_FIELD_REGFILE_SET_STATUS_REG_BUSY(reg_value, 1);
    write_reg(EXTENDED_FIELD_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 BUSY 位
    reg_value = read_reg(EXTENDED_FIELD_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = EXTENDED_FIELD_REGFILE_GET_STATUS_REG_BUSY(reg_value);
    // 设置 LOCK_REG 的 LOCK_BIT 位
    uint32_t reg_value = read_reg(EXTENDED_FIELD_REGFILE_LOCK_REG_ADDR);
    reg_value = EXTENDED_FIELD_REGFILE_SET_LOCK_REG_LOCK_BIT(reg_value, 1);
    write_reg(EXTENDED_FIELD_REGFILE_LOCK_REG_ADDR, reg_value);
    
    // 读取 LOCK_REG 的 LOCK_BIT 位
    reg_value = read_reg(EXTENDED_FIELD_REGFILE_LOCK_REG_ADDR);
    uint8_t bit_value = EXTENDED_FIELD_REGFILE_GET_LOCK_REG_LOCK_BIT(reg_value);
    // 设置 MAGIC_REG 的 MAGIC_VALUE 字段
    uint32_t reg_value = read_reg(EXTENDED_FIELD_REGFILE_MAGIC_REG_ADDR);
    reg_value = EXTENDED_FIELD_REGFILE_SET_MAGIC_REG_MAGIC_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(EXTENDED_FIELD_REGFILE_MAGIC_REG_ADDR, reg_value);
    
    // 读取 MAGIC_REG 的 MAGIC_VALUE 字段
    reg_value = read_reg(EXTENDED_FIELD_REGFILE_MAGIC_REG_ADDR);
    uint32_t field_value = EXTENDED_FIELD_REGFILE_GET_MAGIC_REG_MAGIC_VALUE(reg_value);
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