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

# 命令行参数详解

AutoRegFile提供了丰富的命令行参数，用于控制寄存器文件的生成过程。以下是完整的参数列表及其说明：

| 参数 | 简写 | 说明 |
|-----|-----|-----|
| `--config` | `-c` | 配置文件路径（必须） |
| `--output` | `-o` | 输出文件路径 |
| `--protocol` | `-p` | 总线协议 |
| `--template-dir` | `-t` | 模板目录路径（可多次使用） |
| `--debug` | `-d` | 启用调试模式（更详细的日志） |
| `--log-file` | 无 | 日志文件路径 |
| `--debug-info` | 无 | 在生成的Verilog文件中包含调试信息 |

## 参数使用说明

### 基本参数

- `--config`/`-c`：（必需）指定配置文件路径，支持Excel、JSON、YAML等格式
- `--output`/`-o`：指定生成的Verilog文件输出路径，如未指定则使用配置文件名自动生成

### 总线协议参数

- `--protocol`/`-p`：指定总线协议，可选值包括：
  - `custom`：自定义总线（默认）
  - `apb`：APB总线
  - `ahb`：AHB总线
  - `axi`：AXI总线
  - `avalon`：Avalon总线
  - `wishbone`：Wishbone总线

### 模板相关参数

- `--template-dir`/`-t`：指定自定义模板目录，可以多次使用该参数指定多个目录

### 调试相关参数

- `--debug`/`-d`：启用调试模式，会输出更详细的日志信息
- `--log-file`：指定日志输出文件路径
- `--debug-info`：在生成的Verilog文件中包含调试信息，用于排查问题

## 命令行示例

### 基本使用

```bash
# 使用Excel配置文件生成自定义总线寄存器文件
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v

# 使用JSON配置文件生成APB总线寄存器文件
python -m autoregfile.regfile_gen -c ./config.json -o ./output_apb.v -p apb
```

### 使用调试功能

```bash
# 生成带调试信息的寄存器文件
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v --debug-info

# 启用详细日志并输出到文件
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v -d --log-file ./generation.log
```

### 使用自定义模板

```bash
# 使用自定义模板目录
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v -t ./my_templates

# 使用多个模板目录
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v -t ./templates1 -t ./templates2
```

# 调试功能详解

## 调试信息功能

从v1.2.0版本开始，AutoRegFile支持在生成的Verilog文件中包含调试信息，用于排查寄存器定义和生成过程中的问题。

### 调试信息内容

生成的调试信息包括：

1. **字段位置信息**：
   - 每个寄存器的字段数量
   - 每个字段的名称
   - 每个字段的位范围（high和low位）
   - 每个字段的宽度

2. **寄存器宽度信息**：
   - 每个寄存器计算得到的总宽度

### 开启调试信息

调试信息默认是关闭的，可以通过以下方式开启：

1. **命令行方式**：
   ```bash
   python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v --debug-info
   ```

2. **Python API方式**：
   ```python
   from autoregfile.register_factory import get_register_factory
   
   factory = get_register_factory()
   factory.generate_regfile(
       config_file="./config.xlsx",
       output_file="./output.v",
       enable_debug_info=True  # 开启调试信息
   )
   ```

### 调试信息示例

下面是启用调试信息生成的Verilog文件的一部分：

```verilog
// =============================================================================
// 自动生成的寄存器文件: test_regfile
// 生成时间: 2023-09-01 10:15:30
// =============================================================================

// =============================================================================
// 调试信息（仅在开启调试模式时生成）
// =============================================================================
// DEBUG: 字段位置信息
// CTRL_REG 寄存器字段调试信息
// 原始字段数量: 3
// 字段名: enable, 位范围: high=0, low=0, width=1
// 字段名: mode, 位范围: high=2, low=1, width=2
// 字段名: start, 位范围: high=3, low=3, width=1

// STATUS_REG 寄存器字段调试信息
// 原始字段数量: 2
// 字段名: busy, 位范围: high=0, low=0, width=1
// 字段名: error, 位范围: high=1, low=1, width=1

// DEBUG: 寄存器宽度信息
// CTRL_REG 寄存器宽度: 4
// STATUS_REG 寄存器宽度: 2
// =============================================================================

// 正常的Verilog代码...
```

## 排查常见问题

### 字段位置问题

如果发现寄存器中的字段位置与预期不符，请检查生成的调试信息中的字段位置信息：

1. 确认每个字段的high和low位是否正确
2. 检查是否有字段位置重叠
3. 确认总宽度计算是否与预期一致

### 寄存器宽度问题

如果发现寄存器宽度计算与预期不符，请检查：

1. 调试信息中的寄存器宽度是否正确
2. 最高位的字段位置是否正确
3. 位宽度计算是否考虑了所有字段

### 调试工作流建议

1. 遇到生成文件不符合预期时，首先开启调试信息
2. 分析调试信息中的字段位置和寄存器宽度
3. 根据分析结果修改配置文件或报告问题
4. 重新生成并验证结果 