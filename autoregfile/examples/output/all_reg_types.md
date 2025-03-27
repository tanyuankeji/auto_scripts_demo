# all_reg_types 寄存器说明文档

*自动生成于: 2025-03-27 21:09:05*  
*生成器版本: 2.0.0*

## 1. 概述

本文档描述 `all_reg_types` 模块的寄存器配置和操作方法。

- 数据位宽: 32 位
- 地址位宽: 10 位
- 写端口数量: 1
- 读端口数量: 1

## 2. 内存映射

# 内存映射



## 3. 寄存器列表

| 寄存器名称 | 地址 | 类型 | 描述 |
|------------|------|------|------|
| READWRITE_REG | 0x0 | ReadWrite | ReadWrite类型寄存器 |
| READONLY_REG | 0x0 | ReadOnly | ReadOnly类型寄存器 |
| WRITEONLY_REG | 0x0 | WriteOnly | WriteOnly类型寄存器 |
| WRITE1CLEAN_REG | 0x0 | Write1Clean | Write1Clean类型寄存器 |
| WRITE1SET_REG | 0x0 | Write1Set | Write1Set类型寄存器 |
| WRITE0CLEAN_REG | 0x0 | ReadWrite | Write0Clean类型寄存器 |
| WRITE0SET_REG | 0x0 | ReadWrite | Write0Set类型寄存器 |
| WRITEONCE_REG | 0x0 | WriteOnce | WriteOnce类型寄存器 |
| WRITEONLYONCE_REG | 0x0 | ReadWrite | WriteOnlyOnce类型寄存器 |
| READCLEAN_REG | 0x0 | ReadClean | ReadClean类型寄存器 |
| READSET_REG | 0x0 | ReadWrite | ReadSet类型寄存器 |
| WRITEREADCLEAN_REG | 0x0 | ReadWrite | WriteReadClean类型寄存器 |
| WRITEREADSET_REG | 0x0 | ReadWrite | WriteReadSet类型寄存器 |
| WRITE1PULSE_REG | 0x0 | Write1Pulse | Write1Pulse类型寄存器 |
| WRITE0PULSE_REG | 0x0 | Write0Pulse | Write0Pulse类型寄存器 |

## 4. 寄存器详细说明

### 4.1 READWRITE_REG (0x0)

**描述**: ReadWrite类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | ReadWrite类型字段 |









### 4.2 READONLY_REG (0x0)

**描述**: ReadOnly类型寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadOnly | 0x0 | ReadOnly类型字段 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。








### 4.3 WRITEONLY_REG (0x0)

**描述**: WriteOnly类型寄存器

**类型**: WriteOnly (只写寄存器，读取时返回0)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | WriteOnly | 0x0 | WriteOnly类型字段 |

**注意**: 该寄存器为 WriteOnly 类型，只能写入，读取将返回0。








### 4.4 WRITE1CLEAN_REG (0x0)

**描述**: Write1Clean类型寄存器

**类型**: Write1Clean (写1清零对应位，可读)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | Write1Clean | 0x0 | Write1Clean类型字段 |
| BIT0 | 0 | Write1Clean | 0x0 | Write1Clean位字段 |
| BITS | 4:1 | Write1Clean | 0x0 | Write1Clean多位字段 |




**注意**: 写入1可清零对应位。





### 4.5 WRITE1SET_REG (0x0)

**描述**: Write1Set类型寄存器

**类型**: Write1Set (写1置位对应位，可读)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | Write1Set | 0x0 | Write1Set类型字段 |
| BIT0 | 0 | Write1Set | 0x0 | Write1Set位字段 |
| BITS | 4:1 | Write1Set | 0x0 | Write1Set多位字段 |





**注意**: 写入1可置位对应位。




### 4.6 WRITE0CLEAN_REG (0x0)

**描述**: Write0Clean类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | Write0Clean类型字段 |
| BIT0 | 0 | ReadWrite | 0x0 | Write0Clean位字段 |
| BITS | 4:1 | ReadWrite | 0x0 | Write0Clean多位字段 |









### 4.7 WRITE0SET_REG (0x0)

**描述**: Write0Set类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | Write0Set类型字段 |
| BIT0 | 0 | ReadWrite | 0x0 | Write0Set位字段 |
| BITS | 4:1 | ReadWrite | 0x0 | Write0Set多位字段 |









### 4.8 WRITEONCE_REG (0x0)

**描述**: WriteOnce类型寄存器

**类型**: WriteOnce (只写一次寄存器，写入后不可再修改)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | WriteOnce | 0x0 | WriteOnce类型字段 |






**注意**: 该寄存器只能写入一次，之后写入会被忽略。



### 4.9 WRITEONLYONCE_REG (0x0)

**描述**: WriteOnlyOnce类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | WriteOnlyOnce类型字段 |









### 4.10 READCLEAN_REG (0x0)

**描述**: ReadClean类型寄存器

**类型**: ReadClean (读取后自动清零的寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadClean | 0x0 | ReadClean类型字段 |


**注意**: 该寄存器会在读取后自动清零。







### 4.11 READSET_REG (0x0)

**描述**: ReadSet类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | ReadSet类型字段 |









### 4.12 WRITEREADCLEAN_REG (0x0)

**描述**: WriteReadClean类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | WriteReadClean类型字段 |









### 4.13 WRITEREADSET_REG (0x0)

**描述**: WriteReadSet类型寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | ReadWrite | 0x0 | WriteReadSet类型字段 |









### 4.14 WRITE1PULSE_REG (0x0)

**描述**: Write1Pulse类型寄存器

**类型**: Write1Pulse (写1产生一个周期的脉冲，然后自动清零)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | Write1Pulse | 0x0 | Write1Pulse类型字段 |
| BIT0 | 0 | Write1Pulse | 0x0 | Write1Pulse位字段 |
| BITS | 4:1 | Write1Pulse | 0x0 | Write1Pulse多位字段 |







**注意**: 该寄存器为脉冲类型，写入1会产生一个时钟周期的脉冲输出。


### 4.15 WRITE0PULSE_REG (0x0)

**描述**: Write0Pulse类型寄存器

**类型**: Write0Pulse (写0产生一个周期的脉冲，然后自动清零)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| VALUE | 31:0 | Write0Pulse | 0x0 | Write0Pulse类型字段 |
| BIT0 | 0 | Write0Pulse | 0x0 | Write0Pulse位字段 |
| BITS | 4:1 | Write0Pulse | 0x0 | Write0Pulse多位字段 |







**注意**: 该寄存器为脉冲类型，写入0会产生一个时钟周期的脉冲输出。



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
    // 写入 READWRITE_REG
    write_reg(ALL_REG_TYPES_READWRITE_REG_ADDR, 0x12345678);
    // 读取 READWRITE_REG
    uint32_t readwrite_reg_value = read_reg(ALL_REG_TYPES_READWRITE_REG_ADDR);
    // 读取 READONLY_REG
    uint32_t readonly_reg_value = read_reg(ALL_REG_TYPES_READONLY_REG_ADDR);
    // 写入 WRITEONLY_REG
    write_reg(ALL_REG_TYPES_WRITEONLY_REG_ADDR, 0x12345678);
    // 写入 WRITE1CLEAN_REG
    write_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR, 0x12345678);
    // 读取 WRITE1CLEAN_REG
    uint32_t write1clean_reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    // 写入 WRITE1SET_REG
    write_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR, 0x12345678);
    // 读取 WRITE1SET_REG
    uint32_t write1set_reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    // 写入 WRITE0CLEAN_REG
    write_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR, 0x12345678);
    // 读取 WRITE0CLEAN_REG
    uint32_t write0clean_reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    // 写入 WRITE0SET_REG
    write_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR, 0x12345678);
    // 读取 WRITE0SET_REG
    uint32_t write0set_reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    // 写入 WRITEONCE_REG
    write_reg(ALL_REG_TYPES_WRITEONCE_REG_ADDR, 0x12345678);
    // 读取 WRITEONCE_REG
    uint32_t writeonce_reg_value = read_reg(ALL_REG_TYPES_WRITEONCE_REG_ADDR);
    // 写入 WRITEONLYONCE_REG
    write_reg(ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR, 0x12345678);
    // 读取 WRITEONLYONCE_REG
    uint32_t writeonlyonce_reg_value = read_reg(ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR);
    // 写入 READCLEAN_REG
    write_reg(ALL_REG_TYPES_READCLEAN_REG_ADDR, 0x12345678);
    // 读取 READCLEAN_REG
    uint32_t readclean_reg_value = read_reg(ALL_REG_TYPES_READCLEAN_REG_ADDR);
    // 写入 READSET_REG
    write_reg(ALL_REG_TYPES_READSET_REG_ADDR, 0x12345678);
    // 读取 READSET_REG
    uint32_t readset_reg_value = read_reg(ALL_REG_TYPES_READSET_REG_ADDR);
    // 写入 WRITEREADCLEAN_REG
    write_reg(ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR, 0x12345678);
    // 读取 WRITEREADCLEAN_REG
    uint32_t writereadclean_reg_value = read_reg(ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR);
    // 写入 WRITEREADSET_REG
    write_reg(ALL_REG_TYPES_WRITEREADSET_REG_ADDR, 0x12345678);
    // 读取 WRITEREADSET_REG
    uint32_t writereadset_reg_value = read_reg(ALL_REG_TYPES_WRITEREADSET_REG_ADDR);
    // 写入 WRITE1PULSE_REG
    write_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR, 0x12345678);
    // 读取 WRITE1PULSE_REG
    uint32_t write1pulse_reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    // 写入 WRITE0PULSE_REG
    write_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR, 0x12345678);
    // 读取 WRITE0PULSE_REG
    uint32_t write0pulse_reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
}
```

### 5.2 位域操作

```c
void field_operations() {
    // 设置 READWRITE_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_READWRITE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_READWRITE_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_READWRITE_REG_ADDR, reg_value);
    
    // 读取 READWRITE_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_READWRITE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_READWRITE_REG_VALUE(reg_value);
    // 设置 READONLY_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_READONLY_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_READONLY_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_READONLY_REG_ADDR, reg_value);
    
    // 读取 READONLY_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_READONLY_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_READONLY_REG_VALUE(reg_value);
    // 设置 WRITEONLY_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITEONLY_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITEONLY_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITEONLY_REG_ADDR, reg_value);
    
    // 读取 WRITEONLY_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITEONLY_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITEONLY_REG_VALUE(reg_value);
    // 设置 WRITE1CLEAN_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1CLEAN_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE1CLEAN_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1CLEAN_REG_VALUE(reg_value);
    // 设置 WRITE1CLEAN_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1CLEAN_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE1CLEAN_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE1CLEAN_REG_BIT0(reg_value);
    // 设置 WRITE1CLEAN_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1CLEAN_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE1CLEAN_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1CLEAN_REG_BITS(reg_value);
    // 设置 WRITE1SET_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1SET_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR, reg_value);
    
    // 读取 WRITE1SET_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1SET_REG_VALUE(reg_value);
    // 设置 WRITE1SET_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1SET_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR, reg_value);
    
    // 读取 WRITE1SET_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE1SET_REG_BIT0(reg_value);
    // 设置 WRITE1SET_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1SET_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR, reg_value);
    
    // 读取 WRITE1SET_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1SET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1SET_REG_BITS(reg_value);
    // 设置 WRITE0CLEAN_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0CLEAN_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE0CLEAN_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0CLEAN_REG_VALUE(reg_value);
    // 设置 WRITE0CLEAN_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0CLEAN_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE0CLEAN_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE0CLEAN_REG_BIT0(reg_value);
    // 设置 WRITE0CLEAN_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0CLEAN_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITE0CLEAN_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0CLEAN_REG_BITS(reg_value);
    // 设置 WRITE0SET_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0SET_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR, reg_value);
    
    // 读取 WRITE0SET_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0SET_REG_VALUE(reg_value);
    // 设置 WRITE0SET_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0SET_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR, reg_value);
    
    // 读取 WRITE0SET_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE0SET_REG_BIT0(reg_value);
    // 设置 WRITE0SET_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0SET_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR, reg_value);
    
    // 读取 WRITE0SET_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0SET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0SET_REG_BITS(reg_value);
    // 设置 WRITEONCE_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITEONCE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITEONCE_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITEONCE_REG_ADDR, reg_value);
    
    // 读取 WRITEONCE_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITEONCE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITEONCE_REG_VALUE(reg_value);
    // 设置 WRITEONLYONCE_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITEONLYONCE_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR, reg_value);
    
    // 读取 WRITEONLYONCE_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITEONLYONCE_REG_VALUE(reg_value);
    // 设置 READCLEAN_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_READCLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_READCLEAN_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_READCLEAN_REG_ADDR, reg_value);
    
    // 读取 READCLEAN_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_READCLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_READCLEAN_REG_VALUE(reg_value);
    // 设置 READSET_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_READSET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_READSET_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_READSET_REG_ADDR, reg_value);
    
    // 读取 READSET_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_READSET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_READSET_REG_VALUE(reg_value);
    // 设置 WRITEREADCLEAN_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITEREADCLEAN_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR, reg_value);
    
    // 读取 WRITEREADCLEAN_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITEREADCLEAN_REG_VALUE(reg_value);
    // 设置 WRITEREADSET_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITEREADSET_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITEREADSET_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITEREADSET_REG_ADDR, reg_value);
    
    // 读取 WRITEREADSET_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITEREADSET_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITEREADSET_REG_VALUE(reg_value);
    // 设置 WRITE1PULSE_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1PULSE_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE1PULSE_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1PULSE_REG_VALUE(reg_value);
    // 设置 WRITE1PULSE_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1PULSE_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE1PULSE_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE1PULSE_REG_BIT0(reg_value);
    // 设置 WRITE1PULSE_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE1PULSE_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE1PULSE_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE1PULSE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE1PULSE_REG_BITS(reg_value);
    // 设置 WRITE0PULSE_REG 的 VALUE 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0PULSE_REG_VALUE(reg_value, 0xFFFFFFFF);
    write_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE0PULSE_REG 的 VALUE 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0PULSE_REG_VALUE(reg_value);
    // 设置 WRITE0PULSE_REG 的 BIT0 位
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0PULSE_REG_BIT0(reg_value, 1);
    write_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE0PULSE_REG 的 BIT0 位
    reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    uint8_t bit_value = ALL_REG_TYPES_GET_WRITE0PULSE_REG_BIT0(reg_value);
    // 设置 WRITE0PULSE_REG 的 BITS 字段
    uint32_t reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    reg_value = ALL_REG_TYPES_SET_WRITE0PULSE_REG_BITS(reg_value, 0xF);
    write_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR, reg_value);
    
    // 读取 WRITE0PULSE_REG 的 BITS 字段
    reg_value = read_reg(ALL_REG_TYPES_WRITE0PULSE_REG_ADDR);
    uint32_t field_value = ALL_REG_TYPES_GET_WRITE0PULSE_REG_BITS(reg_value);
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