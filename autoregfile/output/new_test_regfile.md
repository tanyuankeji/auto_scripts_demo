# test_regfile 寄存器说明文档

*自动生成于: 2025-03-24 19:57:34*  
*生成器版本: 2.0.0*

## 1. 概述

本文档描述 `test_regfile` 模块的寄存器配置和操作方法。

- 数据位宽: 32 位
- 地址位宽: 8 位
- 写端口数量: 1
- 读端口数量: 1

## 2. 寄存器列表

| 寄存器名称 | 地址 | 类型 | 描述 |
|------------|------|------|------|
| CTRL_REG | 0x0 | ReadWrite | 控制寄存器 |
| STATUS_REG | 0x0 | ReadOnly | 状态寄存器 |
| INT_EN_REG | 0x0 | ReadWrite | 中断使能寄存器 |
| INT_STATUS_REG | 0x0 | Write1Clean | 中断状态寄存器，写1清零 |
| VERSION_REG | 0x0 | ReadOnly | 版本寄存器 |
| CONFIG_REG | 0x0 | WriteOnce | 配置寄存器，只能写入一次 |

## 3. 寄存器详细说明

### 3.1 CTRL_REG (0x0)

**描述**: 控制寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| ENABLE | 0 | ReadWrite | 0x0 | 模块使能，1=启用，0=禁用 |
| MODE | 2:1 | ReadWrite | 0x0 | 工作模式: 00=正常, 01=低功耗, 10=测试, 11=保留 |
| RESET | 3 | ReadWrite | 0x0 | 软件复位位，写1触发复位 |








### 3.2 STATUS_REG (0x0)

**描述**: 状态寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| BUSY | 0 | ReadOnly | 0x0 | 忙状态指示，1=忙，0=空闲 |
| ERROR | 1 | ReadOnly | 0x0 | 错误指示，1=错误，0=正常 |
| STATE | 5:2 | ReadOnly | 0x0 | 当前状态 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。







### 3.3 INT_EN_REG (0x0)

**描述**: 中断使能寄存器

**类型**: ReadWrite (标准读写寄存器)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DATA_READY_EN | 0 | ReadWrite | 0x0 | 数据就绪中断使能 |
| ERROR_EN | 1 | ReadWrite | 0x0 | 错误中断使能 |
| TIMEOUT_EN | 2 | ReadWrite | 0x0 | 超时中断使能 |








### 3.4 INT_STATUS_REG (0x0)

**描述**: 中断状态寄存器，写1清零

**类型**: Write1Clean (写1清零对应位，可读)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DATA_READY | 0 | Write1Clean | 0x0 | 数据就绪中断状态 |
| ERROR | 1 | Write1Clean | 0x0 | 错误中断状态 |
| TIMEOUT | 2 | Write1Clean | 0x0 | 超时中断状态 |




**注意**: 写入1可清零对应位。




### 3.5 VERSION_REG (0x0)

**描述**: 版本寄存器

**类型**: ReadOnly (只读寄存器，忽略写操作)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| MAJOR | 31:16 | ReadOnly | 0x0 | 主版本号 |
| MINOR | 15:0 | ReadOnly | 0x0 | 次版本号 |

**注意**: 该寄存器为 ReadOnly 类型，只能读取，写入会被忽略。







### 3.6 CONFIG_REG (0x0)

**描述**: 配置寄存器，只能写入一次

**类型**: WriteOnce (只写一次寄存器，写入后不可再修改)
**复位值**: 0x0

**位域描述**:


| 位域 | 位 | 访问类型 | 复位值 | 描述 |
|------|---|----------|--------|------|
| DEVICE_ID | 7:0 | WriteOnce | 0x0 | 设备ID |
| FEATURES | 15:8 | WriteOnce | 0x0 | 特性配置 |






**注意**: 该寄存器只能写入一次，之后写入会被忽略。



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
    write_reg(TEST_REGFILE_CTRL_REG_ADDR, 0x12345678);
    // 读取 CTRL_REG
    uint32_t ctrl_reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    // 读取 STATUS_REG
    uint32_t status_reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    // 写入 INT_EN_REG
    write_reg(TEST_REGFILE_INT_EN_REG_ADDR, 0x12345678);
    // 读取 INT_EN_REG
    uint32_t int_en_reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    // 写入 INT_STATUS_REG
    write_reg(TEST_REGFILE_INT_STATUS_REG_ADDR, 0x12345678);
    // 读取 INT_STATUS_REG
    uint32_t int_status_reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    // 读取 VERSION_REG
    uint32_t version_reg_value = read_reg(TEST_REGFILE_VERSION_REG_ADDR);
    // 写入 CONFIG_REG
    write_reg(TEST_REGFILE_CONFIG_REG_ADDR, 0x12345678);
    // 读取 CONFIG_REG
    uint32_t config_reg_value = read_reg(TEST_REGFILE_CONFIG_REG_ADDR);
}
```

### 4.2 位域操作

```c
void field_operations() {
    // 设置 CTRL_REG 的 ENABLE 位
    uint32_t reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    reg_value = TEST_REGFILE_SET_CTRL_REG_ENABLE(reg_value, 1);
    write_reg(TEST_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 ENABLE 位
    reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_CTRL_REG_ENABLE(reg_value);
    // 设置 CTRL_REG 的 MODE 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    reg_value = TEST_REGFILE_SET_CTRL_REG_MODE(reg_value, 0x3);
    write_reg(TEST_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 MODE 字段
    reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_CTRL_REG_MODE(reg_value);
    // 设置 CTRL_REG 的 RESET 位
    uint32_t reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    reg_value = TEST_REGFILE_SET_CTRL_REG_RESET(reg_value, 1);
    write_reg(TEST_REGFILE_CTRL_REG_ADDR, reg_value);
    
    // 读取 CTRL_REG 的 RESET 位
    reg_value = read_reg(TEST_REGFILE_CTRL_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_CTRL_REG_RESET(reg_value);
    // 设置 STATUS_REG 的 BUSY 位
    uint32_t reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_STATUS_REG_BUSY(reg_value, 1);
    write_reg(TEST_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 BUSY 位
    reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_STATUS_REG_BUSY(reg_value);
    // 设置 STATUS_REG 的 ERROR 位
    uint32_t reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_STATUS_REG_ERROR(reg_value, 1);
    write_reg(TEST_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 ERROR 位
    reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_STATUS_REG_ERROR(reg_value);
    // 设置 STATUS_REG 的 STATE 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_STATUS_REG_STATE(reg_value, 0xF);
    write_reg(TEST_REGFILE_STATUS_REG_ADDR, reg_value);
    
    // 读取 STATUS_REG 的 STATE 字段
    reg_value = read_reg(TEST_REGFILE_STATUS_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_STATUS_REG_STATE(reg_value);
    // 设置 INT_EN_REG 的 DATA_READY_EN 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_EN_REG_DATA_READY_EN(reg_value, 1);
    write_reg(TEST_REGFILE_INT_EN_REG_ADDR, reg_value);
    
    // 读取 INT_EN_REG 的 DATA_READY_EN 位
    reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_EN_REG_DATA_READY_EN(reg_value);
    // 设置 INT_EN_REG 的 ERROR_EN 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_EN_REG_ERROR_EN(reg_value, 1);
    write_reg(TEST_REGFILE_INT_EN_REG_ADDR, reg_value);
    
    // 读取 INT_EN_REG 的 ERROR_EN 位
    reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_EN_REG_ERROR_EN(reg_value);
    // 设置 INT_EN_REG 的 TIMEOUT_EN 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_EN_REG_TIMEOUT_EN(reg_value, 1);
    write_reg(TEST_REGFILE_INT_EN_REG_ADDR, reg_value);
    
    // 读取 INT_EN_REG 的 TIMEOUT_EN 位
    reg_value = read_reg(TEST_REGFILE_INT_EN_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_EN_REG_TIMEOUT_EN(reg_value);
    // 设置 INT_STATUS_REG 的 DATA_READY 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_STATUS_REG_DATA_READY(reg_value, 1);
    write_reg(TEST_REGFILE_INT_STATUS_REG_ADDR, reg_value);
    
    // 读取 INT_STATUS_REG 的 DATA_READY 位
    reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_STATUS_REG_DATA_READY(reg_value);
    // 设置 INT_STATUS_REG 的 ERROR 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_STATUS_REG_ERROR(reg_value, 1);
    write_reg(TEST_REGFILE_INT_STATUS_REG_ADDR, reg_value);
    
    // 读取 INT_STATUS_REG 的 ERROR 位
    reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_STATUS_REG_ERROR(reg_value);
    // 设置 INT_STATUS_REG 的 TIMEOUT 位
    uint32_t reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    reg_value = TEST_REGFILE_SET_INT_STATUS_REG_TIMEOUT(reg_value, 1);
    write_reg(TEST_REGFILE_INT_STATUS_REG_ADDR, reg_value);
    
    // 读取 INT_STATUS_REG 的 TIMEOUT 位
    reg_value = read_reg(TEST_REGFILE_INT_STATUS_REG_ADDR);
    uint8_t bit_value = TEST_REGFILE_GET_INT_STATUS_REG_TIMEOUT(reg_value);
    // 设置 VERSION_REG 的 MAJOR 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_VERSION_REG_ADDR);
    reg_value = TEST_REGFILE_SET_VERSION_REG_MAJOR(reg_value, 0xFFFF);
    write_reg(TEST_REGFILE_VERSION_REG_ADDR, reg_value);
    
    // 读取 VERSION_REG 的 MAJOR 字段
    reg_value = read_reg(TEST_REGFILE_VERSION_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_VERSION_REG_MAJOR(reg_value);
    // 设置 VERSION_REG 的 MINOR 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_VERSION_REG_ADDR);
    reg_value = TEST_REGFILE_SET_VERSION_REG_MINOR(reg_value, 0xFFFF);
    write_reg(TEST_REGFILE_VERSION_REG_ADDR, reg_value);
    
    // 读取 VERSION_REG 的 MINOR 字段
    reg_value = read_reg(TEST_REGFILE_VERSION_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_VERSION_REG_MINOR(reg_value);
    // 设置 CONFIG_REG 的 DEVICE_ID 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_CONFIG_REG_ADDR);
    reg_value = TEST_REGFILE_SET_CONFIG_REG_DEVICE_ID(reg_value, 0xFF);
    write_reg(TEST_REGFILE_CONFIG_REG_ADDR, reg_value);
    
    // 读取 CONFIG_REG 的 DEVICE_ID 字段
    reg_value = read_reg(TEST_REGFILE_CONFIG_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_CONFIG_REG_DEVICE_ID(reg_value);
    // 设置 CONFIG_REG 的 FEATURES 字段
    uint32_t reg_value = read_reg(TEST_REGFILE_CONFIG_REG_ADDR);
    reg_value = TEST_REGFILE_SET_CONFIG_REG_FEATURES(reg_value, 0xFF);
    write_reg(TEST_REGFILE_CONFIG_REG_ADDR, reg_value);
    
    // 读取 CONFIG_REG 的 FEATURES 字段
    reg_value = read_reg(TEST_REGFILE_CONFIG_REG_ADDR);
    uint32_t field_value = TEST_REGFILE_GET_CONFIG_REG_FEATURES(reg_value);
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