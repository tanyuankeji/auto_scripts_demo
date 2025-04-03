# 自动生成Testbench工具

本工具用于自动分析Verilog设计文件并生成对应的testbench，支持信号自动驱动和验证环境自动生成。

## 功能特点

- 自动解析Verilog设计文件，提取模块接口和参数
- 支持使用pyverilog进行更准确的解析（如果安装）
- 使用jinja2模板引擎生成testbench（如果安装）
- 自动识别valid/ready握手信号并生成相应的驱动逻辑
- 支持生成自动验证环境，包括信号采集和比对
- 支持自定义testbench名称、时钟信号名和复位信号名
- 支持在指定相对路径生成简化版testbench文件
- 生成的testbench默认包含模块名称作为后缀
- 可单独指定验证环境的生成路径
- 自动初始化时钟和复位信号，避免仿真警告

## 安装依赖

```bash
pip install pyverilog jinja2
```

## 使用方法

### 基本用法

```bash
./autotest -f <Verilog文件路径>
```

### 生成验证环境

```bash
./autotest -f <Verilog文件路径> -v
```

### 生成演示环境

```bash
./autotest --demo
```

### 自定义testbench名称

```bash
./autotest -f <Verilog文件路径> --tb-name <名称前缀>
```
例如，使用`--tb-name my_tb`将生成`my_tb_<模块名>.sv`文件。现在，无论是否指定前缀，生成的文件都会包含模块名。

### 自定义时钟和复位信号名称

```bash
./autotest -f <Verilog文件路径> --clk-name <时钟名> --rst-name <复位名>
```
例如，使用`--clk-name sys_clk --rst-name sys_rst_n`将使testbench中使用这些名称。所有信号都会被自动初始化，避免仿真时出现未定义值的警告。

#### 关于时钟与复位信号的详细说明

工具会自动处理以下情况：

1. **自动添加时钟和复位信号**：即使在原始设计中不存在这些名称的信号，testbench也会自动添加用户指定的时钟和复位信号。

2. **自动初始化**：生成的testbench会自动包含这些信号的初始化代码，确保时钟从0开始，复位信号从0开始：
   ```verilog
   // 初始化时钟和复位信号
   initial begin
       sys_clk = 1'b0;
       sys_rstn = 1'b0;
   end
   ```

3. **自动生成时钟**：testbench会自动生成时钟信号，默认周期为10ns：
   ```verilog
   // 时钟生成
   initial forever #5ns sys_clk = ~sys_clk;
   ```

4. **复位控制**：testbench会自动包含复位控制逻辑，在30个时钟周期后释放复位：
   ```verilog
   // 复位控制
   initial begin
       sys_rstn = 1'b0;
       `DELAY(30, sys_clk);
       sys_rstn = 1'b1;
   end
   ```

这些自动化功能可确保仿真环境中不会出现未初始化信号导致的警告或错误。

### 指定输出文件的相对路径

```bash
./autotest -f <Verilog文件路径> --rel-path <相对路径>
```
例如，使用`--rel-path custom_dir`将在当前目录下的custom_dir文件夹中生成简化版testbench。

### 指定验证环境的路径

```bash
./autotest -f <Verilog文件路径> -v --ver-path <验证环境路径>
```
例如，使用`--ver-path verification_env`将在verification_env目录下生成完整的验证环境，而testbench文件仍将输出到`--rel-path`指定的位置。

### 更多选项

```bash
./autotest --help
```

## 目录结构

```
auto_scripts_demo/autotest/
├── auto_tb.py            # 主脚本
├── parsers/              # 解析器模块
│   └── verilog_parser.py # Verilog解析器
├── generators/           # 生成器模块
│   ├── testbench_generator.py     # Testbench生成器
│   └── verification_generator.py  # 验证环境生成器
└── templates/            # 模板目录
    ├── testbench.sv.j2   # jinja2模板
    └── vcs_demo/         # VCS环境模板
```

## 功能扩展

1. 添加自定义模板：将模板放在templates目录，并使用`-t`参数指定
2. 扩展信号解析：修改parsers/verilog_parser.py
3. 扩展testbench生成：修改generators/testbench_generator.py

## 示例

```bash
# 生成基本testbench（默认含模块名）
./autotest -f design/my_module.v

# 生成验证环境
./autotest -f design/my_module.v -v -o output_dir

# 生成演示环境
./autotest --demo

# 自定义testbench名称和信号名
./autotest -f design/my_module.v --tb-name custom_tb --clk-name sys_clk --rst-name rst_n

# 指定生成路径
./autotest -f design/my_module.v --rel-path verification/testbenches

# 指定验证环境路径
./autotest -f design/my_module.v -v --ver-path verification_env

# 组合使用多个选项
./autotest -f design/my_module.v -v --tb-name custom_tb --clk-name sys_clk --rst-name rst_n --rel-path tb_files --ver-path verification_env
``` 