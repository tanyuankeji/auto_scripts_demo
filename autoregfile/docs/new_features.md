# AutoRegFile 新功能文档

## 新增功能概述

1. **单表格Excel格式支持**
   - 寄存器和字段定义现在可以放在同一个Excel表格中
   - 简化配置文件创建和维护
   - 更清晰地展示寄存器及其字段之间的关系

2. **字段属性扩展**
   - 每个字段可配置寄存器类型
   - 每个字段可配置默认值
   - 新增"功能"属性，用于描述字段实现的具体功能

3. **软硬件访问类型支持**
   - 新增SoftwareAccessType：通过总线实现读写
   - 新增HardwareAccessType：通过信号输入输出实现
   - 支持在寄存器和字段级别配置访问类型

4. **改进的Verilog生成**
   - 每个字段使用独立的always块实现
   - 为每个寄存器和字段添加详细注释
   - 支持硬件接口生成

5. **字段锁定和魔术数字依赖**
   - 支持字段锁定机制，防止意外修改
   - 支持魔术数字依赖，增强安全性
   - 字段级别的锁定和魔术数字校验

## 单表格Excel格式

新的Excel格式包含以下sheet:

1. **Config** - 全局配置参数
2. **RegisterFields** - 寄存器和字段定义（合并在一个表格）

### RegisterFields表格列定义

寄存器信息列：
- `register_name`: 寄存器名称（只在寄存器第一行填写）
- `address`: 寄存器地址（只在寄存器第一行填写）
- `register_type`: 寄存器类型（只在寄存器第一行填写）
- `register_reset_value`: 寄存器复位值（只在寄存器第一行填写）
- `register_description`: 寄存器描述（只在寄存器第一行填写）
- `sw_access_type`: 软件访问类型（只在寄存器第一行填写）
- `hw_access_type`: 硬件访问类型（只在寄存器第一行填写）
- `lock_dependency`: 寄存器锁定依赖（只在寄存器第一行填写）
- `magic_dependency`: 寄存器魔术数字依赖（只在寄存器第一行填写）

字段信息列：
- `field_name`: 字段名称
- `bit_range`: 位范围（如 "0" 或 "7:0"）
- `field_type`: 字段类型
- `field_reset_value`: 字段复位值
- `field_description`: 字段描述
- `field_function`: 字段功能说明
- `field_sw_access_type`: 字段级软件访问类型
- `field_hw_access_type`: 字段级硬件访问类型
- `field_lock_dependency`: 字段锁定依赖
- `magic_dependency`: 字段魔术数字依赖

### 使用示例

创建表格格式如下：

每个寄存器使用多行描述，第一行包含寄存器信息，随后的行包含该寄存器的字段：

| register_name | address | register_type | ... | field_name | bit_range | field_type | ... |
|---------------|---------|---------------|-----|------------|-----------|------------|-----|
| CTRL_REG      | 0x00    | ReadWrite     | ... |            |           |            |     |
|               |         |               |     | ENABLE     | 0         | ReadWrite  | ... |
|               |         |               |     | MODE       | 2:1       | ReadWrite  | ... |
| STATUS_REG    | 0x04    | ReadOnly      | ... |            |           |            |     |
|               |         |               |     | BUSY       | 0         | ReadOnly   | ... |

## 软硬件访问类型

### 软件访问类型 (SoftwareAccessType)

可选值：
- `READ_WRITE`: 可读可写
- `READ`: 只读
- `WRITE`: 只写

### 硬件访问类型 (HardwareAccessType)

可选值：
- `READ`: 硬件可读（生成对应的输出信号）
- `WRITE`: 硬件可写（生成对应的输入信号）
- `READ_WRITE`: 硬件可读可写（生成输入输出信号）

### 硬件接口示例

寄存器级别的硬件接口（以CTRL_REG为例）：

```verilog
// CTRL_REG - 硬件读接口 
output wire [31:0] ctrl_reg_hwout,

// CTRL_REG - 硬件写接口
input wire [31:0] ctrl_reg_hwin,
input wire        ctrl_reg_hwen,
```

字段级别的硬件接口（以CTRL_REG.ENABLE为例）：

```verilog
// CTRL_REG.ENABLE - 硬件读接口
output wire ctrl_reg_enable_hwout,

// CTRL_REG.ENABLE - 硬件写接口
input wire ctrl_reg_enable_hwin,
input wire ctrl_reg_enable_hwen,
```

## 锁定依赖和魔术数字依赖

### 锁定依赖机制

锁定依赖允许某个寄存器或字段被另一个寄存器的特定位锁定，防止意外修改。

**配置方式**:
- 在RegisterFields表格中，使用`lock_dependency`或`field_lock_dependency`列配置锁定关系
- 值格式为锁定寄存器和位的引用，如`LOCK_REG.LOCK_BIT`
- 多个锁定条件可使用逗号分隔

**生成的Verilog代码**:
```verilog
// 锁定逻辑
assign ctrl_reg_enable_locked = lock_reg_reg[0];  // LOCK_REG.LOCK_BIT

// 在写入条件中使用锁定验证
if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && !ctrl_reg_enable_locked) begin
    // 写入逻辑
end
```

### 魔术数字依赖机制

魔术数字依赖要求某个寄存器或字段的写入操作必须在特定寄存器包含特定值时才能执行，增强安全性。

**配置方式**:
- 在RegisterFields表格中，使用`magic_dependency`列配置魔术数字依赖
- 值为魔术数字寄存器的引用，如`MAGIC_REG`
- 默认使用被引用寄存器的复位值作为魔术数字值

**生成的Verilog代码**:
```verilog
// 魔术数字依赖逻辑
wire ctrl_reg_start_magic_valid;
assign ctrl_reg_start_magic_valid = magic_reg_reg == 32'hDEADBEEF;

// 在写入条件中使用魔术数字验证
if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && ctrl_reg_start_magic_valid) begin
    // 写入逻辑
end
```

### 使用场景

1. **安全关键控制寄存器**:
   使用锁定机制防止关键控制寄存器被意外修改

2. **特权操作**:
   使用魔术数字依赖确保只有授权软件可以执行特定操作

3. **调试功能**:
   锁定测试/调试寄存器，防止在正常操作中被意外访问

4. **配置保护**:
   在初始化完成后锁定配置寄存器，防止运行时被修改

## 使用方法

### 创建单表格Excel配置文件

使用提供的`create_single_sheet_excel.py`脚本创建示例：

```bash
python examples/create_single_sheet_excel.py
```

### 使用单表格配置生成RTL

使用提供的`single_sheet_usage.py`脚本：

```bash
python examples/single_sheet_usage.py
```

### 手动创建配置文件

1. 创建Excel文件，包含Config和RegisterFields两个sheet
2. 在RegisterFields中，按照上述格式定义寄存器和字段
3. 使用ExcelParser解析配置文件

```python
from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator

# 解析Excel配置
parser = ExcelParser()
config = parser.parse("my_config.xlsx")

# 生成Verilog代码
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "output_regfile.v")
```

## 生成的Verilog代码特点

1. **每个字段的always块**:
   每个字段使用独立的always块实现，增强代码的模块化和可读性

   ```verilog
   // CTRL_REG.ENABLE 字段逻辑
   // 位位置: [0:0]
   // 描述: 使能位
   // 功能: 控制系统工作使能
   // 类型: ReadWrite
   // 默认值: 0
   always @(posedge clk or negedge rst_n) begin
       if (!rst_n) begin
           ctrl_reg_reg[0] <= 1'd0;
       end
       else begin
           // 软件写逻辑
           if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
               ctrl_reg_reg[0] <= wr_data_0[0];
           end
       end
   end
   ```

2. **硬件接口连接**:
   自动生成的硬件接口连接逻辑

   ```verilog
   // 硬件访问输出连接
   assign ctrl_reg_hwout = ctrl_reg_reg;
   assign ctrl_reg_enable_hwout = ctrl_reg_reg[0];
   ```

3. **详细的注释**:
   每个寄存器和字段都有详细的注释，包括功能、位位置、类型和默认值 