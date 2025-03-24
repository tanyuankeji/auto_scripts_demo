# AutoRegFile 高级用法

本文档介绍 AutoRegFile 的高级用法，包括复杂配置、自定义模板和集成到开发流程中。

## 高级配置选项

除了基本配置外，AutoRegFile 还支持以下高级配置选项：

### 多写端口/多读端口

您可以配置多个写端口和读端口：

```json
{
  "module_name": "multi_port_regfile",
  "data_width": 32,
  "addr_width": 8,
  "num_write_ports": 2,
  "num_read_ports": 3,
  ...
}
```

这将生成带有2个写端口和3个读端口的寄存器文件，适用于多主设备访问的场景。

### 同步复位

默认情况下，生成的寄存器文件使用异步复位。您可以通过设置 `sync_reset` 选项来使用同步复位：

```json
{
  "sync_reset": true,
  ...
}
```

同步复位通常在高速设计中更受欢迎，因为它可以避免亚稳态问题。

### 字节使能

对于32位寄存器，您可以启用字节使能功能，允许按字节写入：

```json
{
  "byte_enable": true,
  ...
}
```

启用后，每个写端口将包含一个额外的 `wr_be_*` 信号，用于控制哪些字节被写入。

## 高级寄存器类型

### 复合类型寄存器

除了基本类型外，AutoRegFile 还支持复合类型寄存器：

- **WriteCleanReadSet**：写操作清零，读操作置位
- **WriteSetReadClean**：写操作置位，读操作清零
- **Write1CleanReadSet**：写1清零，读取置位
- **Write1SetReadClean**：写1置位，读取清零

### 特殊类型寄存器

- **Write1Toggle**：写1翻转对应位的值
- **Write0Toggle**：写0翻转对应位的值
- **UserDefined**：用户自定义行为（需要提供自定义代码）

示例：

```json
{
  "registers": [
    {
      "name": "TOG_REG",
      "address": "0x34",
      "type": "Write1Toggle",
      "reset_value": "0x00000000",
      "description": "翻转寄存器，写1翻转对应位"
    }
  ]
}
```

## 工作流集成

### 命令行集成

将 AutoRegFile 集成到Makefile：

```makefile
REGFILE_CONFIG = config/regfile.json
REGFILE_OUTPUT = rtl/regfile.v
REGFILE_HEADER = sw/include/regfile.h
REGFILE_DOC = doc/regfile.md

regfile: $(REGFILE_CONFIG)
	python -m regfile-gen -c $(REGFILE_CONFIG) -o $(REGFILE_OUTPUT) --header --doc
```

### 版本控制集成

在CI流程中生成寄存器文件：

```yaml
# .gitlab-ci.yml
stages:
  - generate
  - build

generate_regfiles:
  stage: generate
  script:
    - pip install autoregfile
    - python -m regfile-gen -c config/regfile.json -o rtl/regfile.v --header --doc
  artifacts:
    paths:
      - rtl/regfile.v
      - sw/include/regfile.h
      - doc/regfile.md
```

## 高级Python API用法

### 定制生成过程

您可以通过继承现有生成器类来定制生成过程：

```python
from autoregfile.generators import VerilogGenerator

class CustomVerilogGenerator(VerilogGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 添加自定义初始化代码
    
    def pre_process(self, config):
        # 在生成之前处理配置
        return config
    
    def post_process(self, code):
        # 在生成之后处理代码
        return code

# 使用自定义生成器
gen = CustomVerilogGenerator()
code = gen.generate(config)
```

### 批量生成

一次性生成多个寄存器文件：

```python
import os
from pathlib import Path
from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator

def generate_all_regfiles(config_dir, output_dir):
    parser = JsonParser()
    gen = VerilogGenerator()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找所有JSON配置文件
    config_files = Path(config_dir).glob("*.json")
    
    for config_file in config_files:
        try:
            # 解析配置
            config = parser.parse(config_file)
            
            # 生成输出文件名
            module_name = config.get("module_name", "regfile")
            output_file = Path(output_dir) / f"{module_name}.v"
            
            # 生成代码
            code = gen.generate(config)
            gen.save(code, output_file)
            
            print(f"Generated: {output_file}")
        except Exception as e:
            print(f"Error processing {config_file}: {e}")

# 使用示例
generate_all_regfiles("configs", "output")
```

## 自定义模板高级用法

### 创建分层模板

您可以创建分层模板，将复杂的模板拆分为多个子模板：

```jinja
{# main.v.j2 #}
{% include "header.v.j2" %}

module {{ module_name }} (
    {% include "ports.v.j2" %}
);

{% include "params.v.j2" %}
{% include "registers.v.j2" %}
{% include "logic.v.j2" %}

endmodule
```

### 使用条件模板

根据配置选择不同的模板：

```python
from autoregfile.generators import VerilogGenerator

class ConditionalGenerator(VerilogGenerator):
    def select_template(self, config):
        if config.get("advanced_mode", False):
            return "advanced_template.v.j2"
        else:
            return "basic_template.v.j2"
    
    def generate(self, config):
        template_name = self.select_template(config)
        template = self.env.get_template(template_name)
        return template.render(**config)
```

## 性能优化

### 大型寄存器文件优化

对于包含大量寄存器的配置（>100个寄存器），可以使用以下优化技巧：

1. **分块生成**：将寄存器分为多个块，每个块生成一个单独的模块
2. **使用生成循环**：在Verilog中使用生成循环来减小代码大小
3. **优化解码逻辑**：使用分层解码，减少组合逻辑深度

示例配置：

```json
{
  "module_name": "large_regfile",
  "optimization": {
    "use_blocks": true,
    "block_size": 32,
    "use_generate": true,
    "hierarchical_decode": true
  },
  ...
}
```

## 调试技巧

### 调试模式

启用调试输出：

```bash
python -m regfile-gen -c config.json -o regfile.v --debug
```

### 验证生成的代码

生成后自动运行语法检查：

```bash
python -m regfile-gen -c config.json -o regfile.v --verify
```

这将使用外部工具（如Icarus Verilog或Verilator）来验证生成的Verilog代码语法是否正确。

## 最佳实践

1. **保持配置文件模块化**：为不同的功能模块创建单独的配置文件
2. **使用版本控制**：将配置文件纳入版本控制系统
3. **自动化生成**：在构建流程中自动生成寄存器文件
4. **使用一致的命名约定**：为寄存器和位域使用一致的命名约定
5. **添加详细注释**：在配置文件中添加详细的描述和注释
6. **定期备份**：备份配置文件，以防意外更改 