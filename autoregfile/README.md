# AutoRegFile - 自动寄存器文件生成器

AutoRegFile是一个功能强大的工具，用于根据配置文件自动生成Verilog寄存器文件、C语言头文件和文档。它支持多种寄存器类型，满足各种数字设计需求。

## 特点

- **多种配置格式**：支持JSON、YAML和Excel格式的配置文件
- **丰富的寄存器类型**：支持ReadWrite、ReadOnly、WriteOnly、ReadClean、Write1Clean、Write1Set、WriteOnce等25种寄存器类型
- **多种输出格式**：生成Verilog寄存器文件、C语言头文件和Markdown文档
- **灵活的模板系统**：基于Jinja2的模板引擎，支持自定义模板
- **完整的命令行支持**：提供丰富的命令行选项，方便集成到工作流程中

## 功能详解

### 支持的寄存器类型功能

| 寄存器类型 | 功能描述 | 应用场景 |
|------------|----------|----------|
| `ReadWrite` | 标准读写寄存器 | 常规配置寄存器 |
| `ReadOnly` | 只读寄存器 | 状态指示、版本信息 |
| `WriteOnly` | 只写寄存器 | 触发器、命令寄存器 |
| `ReadClean` | 读取后自动清零 | 状态标志、中断标志 |
| `ReadSet` | 读取后自动置位 | 触发器功能 |
| `Write1Clean` | 写1清零对应位 | 中断清除 |
| `Write1Set` | 写1置位对应位 | 中断使能 |
| `Write0Clean` | 写0清零对应位 | 反向控制 |
| `Write0Set` | 写0置位对应位 | 反向控制 |
| `WriteOnce` | 只能写入一次 | 安全设置、锁定设置 |

### 输出格式说明

1. **Verilog 文件**
   - 完整的寄存器模块，包含地址解码、写入逻辑和读取逻辑
   - 支持多种复位类型（同步或异步）
   - 支持可配置的端口数量
   - 支持字节使能功能

2. **C语言头文件**
   - 寄存器地址定义
   - 位域掩码和位移定义
   - 帮助软件层进行寄存器访问

3. **Markdown文档**
   - 寄存器映射表
   - 接口信号说明
   - 寄存器详细功能描述
   - 位域功能说明

## 安装

### 使用pip安装

```bash
pip install autoregfile
```

### 从源码安装

```bash
git clone https://github.com/yourusername/autoregfile.git
cd autoregfile
pip install -e .
```

## 使用方法

### 基本使用流程

1. 创建配置文件（JSON、YAML或Excel格式）
2. 使用命令行工具或Python API生成寄存器文件
3. 将生成的文件集成到您的项目中

### 命令行使用

生成Verilog文件：

```bash
python regfile-gen.py -c config.json -o regfile.v
```

同时生成C语言头文件和文档：

```bash
python regfile-gen.py -c config.json -o regfile.v --header --doc
```

使用详细输出模式：

```bash
python regfile-gen.py -c config.json -o regfile.v --header --doc -v
```

使用自定义模板：

```bash
python regfile-gen.py -c config.json -o regfile.v -t my_templates_dir
```

### Python API使用

基本用法：

```python
from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator

# 解析配置
parser = JsonParser()
config = parser.parse("config.json")

# 生成Verilog文件
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "example_regfile.v")
```

生成多种输出：

```python
from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator

# 解析配置
parser = JsonParser()
config = parser.parse("config.json")

# 生成Verilog文件
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "example_regfile.v")

# 生成C语言头文件
header_gen = HeaderGenerator()
header_code = header_gen.generate(config)
header_gen.save(header_code, "example_regfile.h")

# 生成Markdown文档
doc_gen = DocGenerator()
doc_content = doc_gen.generate(config)
doc_gen.save(doc_content, "example_regfile.md")
```

使用YAML配置：

```python
from autoregfile.parsers import YamlParser
from autoregfile.generators import VerilogGenerator

parser = YamlParser()
config = parser.parse("config.yaml")
# 生成过程同上
```

使用Excel配置：

```python
from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator

parser = ExcelParser()
config = parser.parse("config.xlsx")
# 生成过程同上
```

## 配置文件格式

### JSON配置示例

```json
{
  "module_name": "example_regfile",
  "data_width": 32,
  "addr_width": 8,
  "num_write_ports": 1,
  "num_read_ports": 2,
  "sync_reset": false,
  "reset_value": "0x00000000",
  "byte_enable": true,
  "registers": [
    {
      "name": "CTRL_REG",
      "address": "0x00",
      "type": "ReadWrite",
      "reset_value": "0x00000000",
      "description": "控制寄存器"
    },
    {
      "name": "STATUS_REG",
      "address": "0x04",
      "type": "ReadOnly",
      "reset_value": "0x00000000",
      "description": "状态寄存器"
    }
  ],
  "fields": [
    {
      "register": "CTRL_REG",
      "name": "ENABLE",
      "bit_range": "0",
      "description": "使能位"
    },
    {
      "register": "CTRL_REG",
      "name": "MODE",
      "bit_range": "2:1",
      "description": "模式设置"
    }
  ]
}
```

### YAML配置示例

```yaml
module_name: example_regfile
data_width: 32
addr_width: 8
num_write_ports: 1
num_read_ports: 2
sync_reset: false
reset_value: "0x00000000"
byte_enable: true
registers:
  - name: CTRL_REG
    address: "0x00"
    type: ReadWrite
    reset_value: "0x00000000"
    description: 控制寄存器
  - name: STATUS_REG
    address: "0x04"
    type: ReadOnly
    reset_value: "0x00000000"
    description: 状态寄存器
fields:
  - register: CTRL_REG
    name: ENABLE
    bit_range: "0"
    description: 使能位
  - register: CTRL_REG
    name: MODE
    bit_range: "2:1"
    description: 模式设置
```

### Excel配置格式

Excel文件需要包含以下两个工作表：

1. `Registers`工作表：包含寄存器定义
   - 列：name, address, type, reset_value, description

2. `Fields`工作表：包含位域定义
   - 列：register, name, bit_range, description

## 高级使用

### 自定义模板

您可以创建自定义模板来控制生成的代码格式。详细信息请参考 [templates.md](docs/templates.md)。

### 命令行选项

```
usage: regfile-gen [-h] -c CONFIG -o OUTPUT [--verilog] [--header] [--doc] [-t TEMPLATES] [-v]

寄存器文件生成工具

optional arguments:
  -h, --help            显示帮助信息
  -c CONFIG, --config CONFIG
                        配置文件路径 (支持JSON, YAML, Excel)
  -o OUTPUT, --output OUTPUT
                        输出目录或文件路径
  --verilog             生成Verilog文件 (默认开启)
  --header              生成C语言头文件
  --doc                 生成Markdown文档
  -t TEMPLATES, --templates TEMPLATES
                        自定义模板目录
  -v, --verbose         显示详细输出
```

### 集成到CI/CD流程

AutoRegFile可以轻松集成到CI/CD流程中：

```bash
# 在CI脚本中
pip install autoregfile
python -m regfile-gen -c config.json -o rtl/regfile.v --header --doc
```

## 使用技巧

1. **增量更新**：更新配置文件后重新生成，集成到版本控制系统
2. **版本管理**：在配置文件中添加版本信息，自动反映在生成的文档中
3. **模块化设计**：为不同子系统创建独立的寄存器文件
4. **自动化测试**：为生成的寄存器文件创建自动测试脚本

## 实际应用场景

- **SoC设计**：生成全芯片的寄存器映射
- **FPGA开发**：为各个IP核创建寄存器接口
- **验证环境**：自动生成一致的软件和硬件接口
- **文档生成**：维护最新的寄存器说明文档

## 项目结构

```
autoregfile/
├── autoregfile/          # 核心包
│   ├── core/             # 核心功能模块
│   ├── generators/       # 代码生成器
│   ├── parsers/          # 配置解析器
│   ├── templates/        # 模板文件
│   └── utils/            # 工具函数
├── docs/                 # 文档
├── examples/             # 示例
│   ├── configs/          # 示例配置
│   └── output/           # 示例输出
├── scripts/              # 脚本工具
│   └── generate_regfile.py  # 命令行入口
├── tests/                # 测试文件
├── setup.py              # 包安装配置
└── README.md             # 说明文档
```

## 示例

详细示例请参考 `examples` 目录：

- `examples/simple_usage.py`: 简单使用示例
- `examples/configs/`: 各种配置文件示例
- `examples/output/`: 生成的输出文件示例

## 故障排除

- **安装问题**：确保已安装所有依赖 (`pip install -e ".[dev]"`)
- **配置格式错误**：检查配置文件是否符合要求格式
- **模板问题**：确保自定义模板遵循Jinja2语法

## 许可证

本项目采用MIT许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。 