# Register File Generator

一个用于自动生成Verilog寄存器文件的高级工具，支持多种配置选项和扩展功能。

## 简介

Register File Generator 是一个强大的Python工具，用于自动生成Verilog寄存器文件模块。它支持多种配置选项，可以根据用户需求生成定制化的寄存器文件，适用于SoC设计和FPGA开发。

## 特性

- **灵活的配置选项**：支持自定义数据宽度、地址宽度、读写端口数量等参数
- **支持的寄存器类型**：
  Null
  ReadWrite
  ReadOnly
  ReadClean
  ReadSet
  WriteReadClean
  WriteReadSet
  WriteOnly
  WriteOnlyClean
  WriteOnlySet
  WriteClean
  WriteCleanReadSet
  Write1Clean
  Write1CleanReadSet
  Write0Clean
  Write0CleanReadSet
  WriteSet
  WriteSetReadClean
  Write1Set
  Write1SetReadClean
  Write0Set
  Write0SetReadClean
  Write1Toggle
  Write0Toggle
  WriteOnce
  WriteOnlyOnce
  UserDefined
- **生成的寄存器是例化寄存器库形式的或者always块形式可选**
- **多种复位类型**：支持同步复位和异步复位
- **字节使能支持**：可选择性地启用字节使能功能
- **多格式配置文件**：支持从JSON, YAML和EXCEL文件加载配置
- **文档生成**：自动生成Markdown格式的寄存器文档
- **参数验证**：内置参数验证系统，确保生成的代码符合设计规范
- **模板引擎**：基于模板引擎架构，支持自定义模板

## 安装

### 依赖项

- Python 3.6+
- PyYAML (用于YAML配置文件支持)

```bash
pip install pyyaml
```

## 使用方法

### 基本用法

```bash
python regfile_generator.py -m my_regfile -d 32 -a 8 -o my_regfile.v
```

这将生成一个名为 `my_regfile`的寄存器文件模块，数据宽度为32位，地址宽度为8位（256个寄存器），输出文件为 `my_regfile.v`。

### 命令行参数

| 参数                   | 描述                               | 默认值    |
| ---------------------- | ---------------------------------- | --------- |
| `-m, --module`       | 模块名称                           | regfile   |
| `-d, --data-width`   | 数据宽度 (位)                      | 32        |
| `-a, --addr-width`   | 地址宽度 (位)                      | 5         |
| `-wr, --write-ports` | 写端口数量                         | 1         |
| `-rd, --read-ports`  | 读端口数量                         | 2         |
| `--sync-reset`       | 使用同步复位 (默认为异步复位)      | False     |
| `--reset-value`      | 复位初始化值 (支持十六进制，如0xF) | 0         |
| `--byte-enable`      | 启用字节使能                       | False     |
| `--config`           | 从JSON或YAML文件加载配置           | -         |
| `-o, --output`       | 输出Verilog文件名                  | regfile.v |
| `--gen-header`       | 生成C语言头文件                    | False     |
| `--header-output`    | C语言头文件输出路径                | -         |
| `--output-dir`       | 输出目录路径                       | -         |
| `--gen-doc`          | 生成Markdown文档                   | False     |
| `--doc-output`       | Markdown文档输出路径               | -         |

### 使用配置文件

可以使用JSON或YAML格式的配置文件来指定参数：

```bash
python regfile_generator.py --config my_config.json
```

配置文件示例 (JSON):

```json
{
  "module_name": "my_regfile",
  "data_width": 32,
  "addr_width": 8,
  "num_read_ports": 2,
  "num_write_ports": 1,
  "sync_reset": false,
  "reset_value": "0xF",
  "byte_enable": true
}
```

配置文件示例 (YAML):

```yaml
module_name: my_regfile
data_width: 32
addr_width: 8
num_read_ports: 2
num_write_ports: 1
sync_reset: false
reset_value: "0xF"
byte_enable: true
```

这将生成Verilog文件和对应的C语言头文件，用于软件访问寄存器。

### 生成文档

```bash
python regfile_generator.py -m my_regfile -d 32 -a 8 --gen-doc
```

这将生成Verilog文件和对应的Markdown文档，描述寄存器文件的参数和接口。

## 生成的代码结构

生成的Verilog代码包含以下部分：

1. 模块声明和端口定义
2. 寄存器数组声明
3. 复位逻辑（同步或异步）
4. 写逻辑（支持多个写端口）
5. 读逻辑（支持多个读端口）

## 扩展功能

### 自定义模板

可以通过扩展 `TemplateEngine`类来添加自定义模板：

```python
from regfile_generator import TemplateEngine, RegFileGenerator

# 创建自定义模板生成器
def my_custom_template(params):
    # 生成自定义代码
    return custom_code

# 注册自定义模板
template_engine = TemplateEngine()
template_engine.register_template('my_template', my_custom_template)

# 使用自定义模板引擎创建生成器
regfile_gen = RegFileGenerator()
regfile_gen.template_engine = template_engine
```

## 注意事项

- 当启用字节使能时，数据宽度必须是8的倍数
- 地址宽度过大可能导致生成的寄存器文件过大，影响综合性能
- 读端口和写端口数量必须至少为1

## 许可证

[MIT License](LICENSE)
