# AutoRegFile 用户指南

## 简介

AutoRegFile 是一个灵活的寄存器文件生成工具，可以根据配置文件生成各种总线协议的寄存器文件。本工具支持多种配置格式（Excel、JSON、YAML）以及多种总线协议（APB、AXI Lite、自定义总线等）。

## 安装

### 依赖项

- Python 3.6+
- 必要的包：pandas, openpyxl, jinja2

### 安装步骤

```bash
# 从源码安装
git clone https://github.com/yourusername/autoregfile.git
cd autoregfile
pip install -e .

# 或直接使用pip安装
pip install autoregfile
```

## 基本用法

### 命令行使用

```bash
# 基本用法
python -m autoregfile.regfile_gen -c config.xlsx -o regfile.v -p custom

# 指定总线协议
python -m autoregfile.regfile_gen -c config.xlsx -o regfile.v -p apb

# 使用自定义模板
python -m autoregfile.regfile_gen -c config.xlsx -o regfile.v -p custom -t /path/to/templates
```

### 参数说明

- `-c, --config`：配置文件路径，支持Excel、JSON、YAML格式
- `-o, --output`：输出文件路径
- `-p, --protocol`：总线协议，如apb、axi_lite、custom等
- `-t, --template-dir`：自定义模板目录
- `-v, --verbose`：显示详细日志信息
- `-h, --help`：显示帮助信息

## 配置文件格式

### Excel格式

Excel格式是最常用的配置方式，提供了直观的表格界面来定义寄存器。标准Excel配置文件应包含以下工作表：

1. **Registers**：定义寄存器的基本信息

   列名         | 说明
   ------------|------------------
   Register Name | 寄存器名称
   Address     | 寄存器地址（如0x00, 0x04）
   Description | 寄存器描述
   Type        | 寄存器类型（如RW, RO, WO）
   Fields      | 字段定义，格式为字段名(起始位:结束位)

2. **Fields**（可选）：定义字段的详细信息

   列名         | 说明
   ------------|------------------
   Register    | 所属寄存器名称
   Field Name  | 字段名称
   Bit Range   | 位范围（如7:0, 31:24）
   Access      | 访问类型（如RW, RO, WO）
   Reset Value | 复位值
   Description | 字段描述

### JSON格式

JSON格式提供更灵活的配置方式，适合程序化生成或修改。

```json
{
  "module_name": "my_regfile",
  "data_width": 32,
  "addr_width": 8,
  "bus_protocol": "custom",
  "registers": [
    {
      "name": "control",
      "address": "0x00",
      "description": "控制寄存器",
      "fields": [
        {
          "name": "enable",
          "bit_range": "0:0",
          "access": "RW",
          "reset_val": 0,
          "description": "使能位"
        },
        {
          "name": "mode",
          "bit_range": "2:1",
          "access": "RW",
          "reset_val": 0,
          "description": "模式选择"
        }
      ]
    }
  ]
}
```

## 支持的总线协议

AutoRegFile目前支持以下总线协议：

- **APB**：ARM外设总线，适用于低功耗、低带宽的外设接口
- **AXI Lite**：简化版AXI总线，用于简单的寄存器接口
- **Wishbone**：开源硬件接口，广泛用于SoC设计
- **Custom**：自定义总线协议，可通过模板和配置定制

## 模板系统

### 内置模板

AutoRegFile包含了一系列内置模板，适用于常见的总线协议。这些模板位于`autoregfile/templates`目录下。

### 自定义模板

用户可以创建自定义模板来满足特定需求。模板使用Jinja2模板引擎，支持条件、循环等高级功能。

#### 创建模板目录

```bash
python -m autoregfile.utils.template_tools create /path/to/templates -p apb
```

这将创建一个基于APB协议的模板目录结构：

```
templates/
├── verilog/
│   ├── bus/
│   │   └── custom.v.j2
│   ├── common/
│   └── field/
└── systemverilog/
```

#### 模板上下文变量

在模板中可使用的主要上下文变量：

- `module_name`：模块名称
- `data_width`：数据位宽
- `addr_width`：地址位宽
- `registers`：寄存器列表
- `bus_protocol`：总线协议名称
- `timestamp`：生成时间戳

## 高级功能

### 寄存器类型

AutoRegFile支持多种寄存器类型：

- **RW**：读写寄存器
- **RO**：只读寄存器
- **WO**：只写寄存器
- **W1C**：写1清零寄存器
- **W1S**：写1置位寄存器
- **RW1C**：读写，写1清零寄存器
- **RW1S**：读写，写1置位寄存器

### 自定义总线选项

可以通过配置文件中的`bus_options`字段来定制总线行为：

```json
{
  "bus_options": {
    "custom": {
      "enable_handshake": true,
      "addr_lsb": 2,
      "enable_bus_error": false
    }
  }
}
```

## 常见问题解答

### Q: 如何生成多个寄存器文件?

A: 可以使用不同的输出文件名多次运行程序，或者创建一个脚本来批量处理。

### Q: 如何调试模板渲染问题?

A: 使用`-v`参数启用详细日志，查看模板渲染过程中的错误信息。

### Q: 可以从代码中调用AutoRegFile吗?

A: 可以，使用`register_factory.py`提供的API：

```python
from autoregfile.register_factory import generate_register_file

# 从Excel配置生成
generate_register_file(
    config_file="config.xlsx", 
    output_file="regfile.v",
    bus_protocol="apb"
)

# 从字典配置生成
config = {
    "module_name": "my_regfile",
    "registers": [...]
}
generate_register_file(
    config_dict=config,
    output_file="regfile.v",
    bus_protocol="custom"
)
```

## 附录

### 完整配置选项

#### 全局选项

- `module_name`：模块名称
- `data_width`：数据位宽
- `addr_width`：地址位宽
- `bus_protocol`：总线协议

#### 寄存器选项

- `name`：寄存器名称
- `address`：寄存器地址
- `description`：寄存器描述
- `type`：寄存器类型

#### 字段选项

- `name`：字段名称
- `bit_range`：位范围
- `access`：访问类型
- `reset_val`：复位值
- `description`：字段描述 