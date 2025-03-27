# AutoRegFile 用户指南 - 锁定依赖与魔术数字依赖

## 概述

本指南详细说明了AutoRegFile工具中锁定依赖和魔术数字依赖功能的使用方法，这两个功能可以显著提高寄存器访问的安全性和可靠性。

## 锁定依赖功能

### 什么是锁定依赖？

锁定依赖允许某个寄存器或字段被另一个寄存器的特定位锁定，防止意外修改。当锁定位为1时，被锁定的寄存器或字段将不能被写入。

### 配置方法

在Excel配置文件的RegisterFields表格中：

1. **寄存器级锁定**：
   - 在寄存器的第一行中找到`lock_dependency`列
   - 填入锁定该寄存器的寄存器和位的引用，如`LOCK_REG.LOCK_BIT`

2. **字段级锁定**：
   - 在字段行中找到`field_lock_dependency`列
   - 填入锁定该字段的寄存器和位的引用，如`LOCK_REG.LOCK_BIT`

3. **多重锁定**：
   - 可使用逗号分隔多个锁定条件，如`LOCK_REG.LOCK_BIT1,LOCK_REG.LOCK_BIT2`
   - 所有条件必须满足（所有锁都解锁），才能写入被锁定的寄存器或字段

### 示例配置

| register_name | address | ... | lock_dependency | field_name | ... | field_lock_dependency |
|---------------|---------|-----|-----------------|------------|-----|------------------------|
| CTRL_REG      | 0x00    | ... | LOCK_REG.LOCK_BIT |           | ... |                        |
|               |         |     |                  | ENABLE    | ... |                        |
|               |         |     |                  | MODE      | ... | LOCK_REG.MODE_LOCK     |
| LOCK_REG      | 0x04    | ... |                  |           | ... |                        |
|               |         |     |                  | LOCK_BIT  | ... |                        |
|               |         |     |                  | MODE_LOCK | ... |                        |

## 魔术数字依赖功能

### 什么是魔术数字依赖？

魔术数字依赖是一种安全机制，要求在写入某个寄存器或字段之前，必须先将特定的"魔术数字"写入到指定的寄存器中。这类似于需要密码才能操作的功能。

### 配置方法

在Excel配置文件的RegisterFields表格中：

1. **寄存器级魔术数字依赖**：
   - 在寄存器的第一行中找到`magic_dependency`列
   - 填入作为魔术数字的寄存器名称，如`MAGIC_REG`

2. **字段级魔术数字依赖**：
   - 在字段行中找到`magic_dependency`列
   - 填入作为魔术数字的寄存器名称，如`MAGIC_REG`

3. **魔术数字值**：
   - 默认使用被引用寄存器的复位值作为魔术数字值
   - 例如，如果MAGIC_REG的复位值是0xDEADBEEF，那么必须写入这个值才能解锁

### 示例配置

| register_name | address | register_reset_value | magic_dependency | field_name | ... | magic_dependency |
|---------------|---------|----------------------|------------------|------------|-----|------------------|
| CTRL_REG      | 0x00    | 0x00000000           |                  |            | ... |                  |
|               |         |                      |                  | START      | ... | MAGIC_REG        |
|               |         |                      |                  | STOP       | ... |                  |
| MAGIC_REG     | 0x04    | 0xDEADBEEF           |                  |            | ... |                  |

## 生成的Verilog代码

### 锁定依赖的Verilog代码

```verilog
// 生成锁定条件信号
wire ctrl_reg_locked;
assign ctrl_reg_locked = lock_reg_reg[0];  // LOCK_REG.LOCK_BIT

// 字段级锁定信号
wire ctrl_reg_mode_locked;
assign ctrl_reg_mode_locked = lock_reg_reg[1];  // LOCK_REG.MODE_LOCK

// 在写入条件中使用锁定验证
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[0] <= 1'b0;  // ENABLE位
    end
    else begin
        // 寄存器级锁定检查
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && !ctrl_reg_locked) begin
            ctrl_reg_reg[0] <= wr_data_0[0];
        end
    end
end

// MODE字段的写入包含字段级锁定检查
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[2:1] <= 2'b00;  // MODE位
    end
    else begin
        // 字段级锁定检查
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && !ctrl_reg_mode_locked) begin
            ctrl_reg_reg[2:1] <= wr_data_0[2:1];
        end
    end
end
```

### 魔术数字依赖的Verilog代码

```verilog
// 魔术数字验证逻辑
wire ctrl_reg_start_magic_valid;
assign ctrl_reg_start_magic_valid = magic_reg_reg == 32'hDEADBEEF;

// START字段的写入包含魔术数字验证
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[0] <= 1'b0;  // START位
    end
    else begin
        // 魔术数字验证
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && ctrl_reg_start_magic_valid) begin
            ctrl_reg_reg[0] <= wr_data_0[0];
        end
    end
end
```

## 软件使用示例

下面是软件应如何访问带有锁定依赖和魔术数字依赖的寄存器的伪代码：

```c
// 解锁锁定依赖
write_register(LOCK_REG, 0x00000000);  // 清除锁定位

// 写入魔术数字
write_register(MAGIC_REG, 0xDEADBEEF);  // 写入魔术数字

// 现在可以安全写入受保护的寄存器/字段
write_register(CTRL_REG, 0x00000001);  // 写入START位
```

## 最佳实践

1. **妥善保管魔术数字值**：
   - 将魔术数字值作为安全敏感信息管理
   - 避免在代码中硬编码，考虑使用加密存储或安全启动过程中动态生成

2. **锁定依赖使用建议**：
   - 优先使用字段级锁定，而不是寄存器级锁定，以获得更细粒度的控制
   - 为关键配置寄存器提供自锁功能（写入后自动锁定）

3. **安全性考虑**：
   - 魔术数字依赖主要是防止意外访问，不是安全加密措施
   - 对于高安全性要求，应结合其他硬件安全措施

## 调试提示

1. 使用`examples/test_magic_number.py`脚本测试魔术数字依赖功能
2. 检查生成的Verilog代码中是否包含正确的锁定和魔术数字验证逻辑
3. 使用仿真工具验证锁定和魔术数字功能是否按预期工作 