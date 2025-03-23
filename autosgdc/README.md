# AutoSGDC - 自动SGDC生成工具

AutoSGDC是一个用于自动分析Verilog代码并生成用于Spyglass CDC分析的SGDC（Synopsys Guidance Design Constraints）约束文件的工具。

## 主要功能

- 自动识别Verilog代码中的时钟信号
- 检测跨时钟域信号（CDC信号）
- 识别已有的同步器结构
- 生成完整的SGDC约束文件
- 支持交互式配置时钟属性
- 提供详细的CDC分析报告

## 系统要求

- Python 3.6+
- 无第三方依赖

## 安装

直接克隆代码库即可使用：

```bash
git clone https://github.com/your-username/autosgdc.git
cd autosgdc
```

## 使用方法

基本用法：

```bash
python src/auto_sgdc_gen_v2.py <verilog_files>
```

完整用法：

```bash
python src/auto_sgdc_gen_v2.py [-h] [-o OUTPUT] [-t TOP] [-i INCLUDE [INCLUDE ...]] 
                               [-c CLOCK_FILE] [-n] [-s] [-r] [-v]
                               verilog_files [verilog_files ...]
```

参数说明：

- `verilog_files`：Verilog源文件路径，支持多个文件
- `-o, --output`：输出SGDC文件名（默认为`<top_module>.sgdc`）
- `-t, --top`：指定顶层模块名称（默认自动检测）
- `-i, --include`：包含目录路径，用于查找其他模块文件
- `-c, --clock-file`：时钟配置文件路径，用于预设时钟属性
- `-n, --non-interactive`：非交互模式，使用默认时钟周期
- `-s, --skip-cdc`：跳过CDC检测分析
- `-r, --report`：生成详细分析报告
- `-v, --verbose`：显示详细日志

## 实例

对单个文件进行分析：

```bash
python src/auto_sgdc_gen_v2.py rtl/my_module.v
```

对多个文件进行分析，指定顶层模块：

```bash
python src/auto_sgdc_gen_v2.py -t top_module rtl/module1.v rtl/module2.v rtl/top_module.v
```

使用非交互模式，自动配置时钟属性：

```bash
python src/auto_sgdc_gen_v2.py -n rtl/my_design.v
```

生成详细报告：

```bash
python src/auto_sgdc_gen_v2.py -r rtl/my_design.v
```

## 时钟配置文件格式

时钟配置文件使用JSON格式，例如：

```json
{
  "clk_sys": {
    "period": 10.0,
    "uncertainty": 0.5,
    "waveform": [0, 5],
    "generated": false
  },
  "clk_div2": {
    "period": 20.0,
    "uncertainty": 1.0,
    "waveform": [0, 10],
    "generated": true,
    "source": "clk_sys",
    "divide_by": 2,
    "multiply_by": 1,
    "phase": 0.0
  }
}
```

## 项目结构

```
autosgdc/
├── src/                   # 源代码
│   ├── auto_sgdc_gen_v2.py  # 主程序
│   ├── verilog_parser.py    # Verilog解析器
│   ├── cdc_analyzer.py      # CDC分析器
│   ├── sgdc_generator.py    # SGDC生成器
│   └── utils.py             # 工具函数
├── rtl/                   # 示例Verilog文件
└── README.md              # 本文件
```

## 支持的约束

生成的SGDC文件包含以下约束：

1. 时钟定义
   - `create_clock`
   - `create_generated_clock`
   - `set_clock_uncertainty`

2. 时钟组约束
   - `set_clock_groups -asynchronous`

3. CDC信号约束
   - `set_cdc_signal`
   - `set_cdc_property`

4. 输入输出延迟
   - `set_input_delay`
   - `set_output_delay`

5. 虚假路径和多周期路径
   - `set_false_path`
   - `set_multicycle_path`

## 局限性

- 当前版本的CDC检测基于简化的信号流分析，可能无法检测到所有CDC情况
- 不支持FPGA特有的原语和IP核
- 生成时钟定义需要手动指定正确的时钟生成路径

## 贡献

欢迎提交问题报告和功能建议。如果您想贡献代码，请提交拉取请求。

## 许可证

本项目使用MIT许可证。 