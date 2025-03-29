# AutoRegFile 调试功能详细指南

## 概述

本文档详细介绍 AutoRegFile 中的调试功能，包括调试信息控制、位宽计算调试以及字段位置跟踪等功能。这些功能对于排查寄存器定义和代码生成问题非常有用。

## 调试信息控制功能

从 v1.2.0 版本开始，AutoRegFile 支持在生成的 Verilog 文件中包含详细的调试信息。这些调试信息以注释形式添加到生成文件中，不会影响代码的功能，但可以帮助开发人员理解寄存器的结构和生成过程。

### 调试信息内容

调试信息主要包括两部分：

1. **字段位置信息**：
   - 每个寄存器包含的字段数量
   - 每个字段的名称
   - 每个字段的位范围（high和low位）
   - 每个字段的宽度

2. **寄存器宽度信息**：
   - 每个寄存器的计算宽度

### 使用方法

#### 命令行方式

使用 `--debug-info` 命令行选项开启调试信息：

```bash
# 不包含调试信息的标准生成（默认）
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v

# 包含调试信息的生成
python -m autoregfile.regfile_gen -c ./config.xlsx -o ./output.v --debug-info
```

#### Python API方式

在程序中使用 API 控制调试信息：

```python
from autoregfile.register_factory import get_register_factory

# 获取工厂实例
factory = get_register_factory()

# 生成带调试信息的寄存器文件
factory.generate_regfile(
    config_file="./config.xlsx",
    output_file="./output.v",
    enable_debug_info=True  # 开启调试信息
)
```

#### 自定义生成器中使用

如果你实现了自己的总线生成器，可以添加调试信息支持：

```python
class MyBusGenerator(BaseBusGenerator):
    def __init__(self, config, template_dirs=None):
        # 从配置中获取调试信息标志
        self.enable_debug_info = config.get("enable_debug_info", False)
        super().__init__(config, template_dirs)
        
    def generate(self, output_file, enable_debug_info=None):
        # 如果指定了enable_debug_info参数，则使用该值覆盖实例属性
        if enable_debug_info is not None:
            self.enable_debug_info = enable_debug_info
        
        # 准备上下文
        context = self._prepare_context()
        
        # 将调试信息标志添加到上下文
        context["enable_debug_info"] = self.enable_debug_info
        
        # ... 渲染模板并输出文件 ...
```

## 调试信息示例

以下是启用调试信息后生成的 Verilog 文件的开头部分示例：

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

// 正常的 Verilog 代码...
```

## 调试工作流

### 基本调试工作流

1. **发现问题**：生成的寄存器代码与预期不符
2. **开启调试**：使用 `--debug-info` 选项重新生成
3. **查看信息**：分析生成文件中的调试信息部分
4. **定位问题**：找出字段位置或宽度计算中的问题
5. **修复问题**：更新配置文件或报告代码生成器问题
6. **验证解决**：重新生成并确认问题已解决

### 常见问题与排查方法

#### 1. 寄存器宽度计算错误

**问题表现**：生成的寄存器宽度与预期不符

**排查步骤**：
1. 查看调试信息中的寄存器宽度信息
2. 确认最高位字段的位置是否正确
3. 检查宽度计算逻辑是否考虑了所有字段

**示例**：
```verilog
// DEBUG: 寄存器宽度信息
// CTRL_REG 寄存器宽度: 4   // 应该是32位?
```

**解决方案**：
- 检查配置文件中的字段位置定义
- 确认字段的 bit_range 信息是否正确
- 可能需要在配置中明确指定寄存器宽度

#### 2. 字段位置错误

**问题表现**：字段位置与预期不符，可能导致功能错误

**排查步骤**：
1. 查看调试信息中的字段位置信息
2. 确认每个字段的 high 和 low 位是否与设计一致
3. 检查是否有字段位置重叠

**示例**：
```verilog
// 字段名: mode, 位范围: high=2, low=1, width=2  // 应该是 high=3, low=2?
```

**解决方案**：
- 修正配置文件中的字段位置定义
- 确保字段之间没有重叠或间隙

#### 3. 字段数量不一致

**问题表现**：生成的代码缺少某些字段或包含多余字段

**排查步骤**：
1. 查看调试信息中报告的原始字段数量
2. 与设计规格对比，确认是否有缺失或多余字段

**示例**：
```verilog
// CTRL_REG 寄存器字段调试信息
// 原始字段数量: 2  // 应该有3个字段?
```

**解决方案**：
- 检查配置文件中的字段定义
- 确认所有字段都被正确加载

## 实现细节

### 调试信息生成流程

1. **命令行解析**：
   - `regfile_gen.py` 解析 `--debug-info` 命令行参数
   - 将参数传递给 `RegisterFactory.generate_regfile()` 方法

2. **总线生成器**：
   - 将 `enable_debug_info` 参数传递给总线生成器
   - 总线生成器将该参数添加到模板上下文

3. **模板渲染**：
   - 模板使用条件语句根据 `enable_debug_info` 值决定是否生成调试信息
   - 调试信息以注释形式添加到生成的代码中

### 配置传递机制

调试信息配置通过以下路径传递：

```
命令行参数 --debug-info
    ↓
regfile_gen.py:main()
    ↓
RegisterFactory.generate_regfile(enable_debug_info=args.debug_info)
    ↓
BusGenerator.generate(enable_debug_info=enable_debug_info)
    ↓
模板上下文: context["enable_debug_info"] = self.enable_debug_info
    ↓
模板条件语句: {% if enable_debug_info|default(false) %}
```

## 高级调试技巧

### 自定义调试信息

你可以通过修改模板添加自定义调试信息，例如：

```jinja
{% if enable_debug_info|default(false) %}
// 自定义调试信息
// 总线配置: 数据宽度={{ data_width }}, 地址宽度={{ addr_width }}
// 总寄存器数量: {{ registers|length }}

// 寄存器偏移量:
{% for reg in registers %}
// {{ reg.name }}: 偏移量=0x{{ '%X' % reg.address|replace('0x', '')|int(16) }}
{% endfor %}
{% endif %}
```

### 调试寄存器宽度计算

可以在模板中添加更详细的寄存器宽度计算过程调试信息：

```jinja
{% if enable_debug_info|default(false) %}
// 宽度计算过程调试
{% for reg in registers %}
// {{ reg.name }} 宽度计算:
{% set max_high = -1 %}
{% for field in reg.fields %}
// 考虑字段 {{ field.name }}: high={{ field.bit_range.high }}
{% set max_high = [max_high, field.bit_range.high]|max %}
{% endfor %}
// 最终最高位: {{ max_high }}
// 计算宽度: {{ max_high + 1 }}
{% endfor %}
{% endif %}
```

### 程序化调试

对于复杂问题，你可以编写专门的调试脚本：

```python
from autoregfile.parsers import ExcelParser
from autoregfile.core.bus_generators.custom_generator import CustomBusGenerator

# 解析配置文件
parser = ExcelParser()
config = parser.parse("./config.xlsx")

# 创建生成器
generator = CustomBusGenerator(config)

# 打印寄存器信息
for reg in config.get("registers", []):
    print(f"寄存器: {reg.get('name')}")
    print(f"  地址: {reg.get('address')}")
    print(f"  宽度: {reg.get('width', '未指定')}")
    
    if "fields" in reg:
        print(f"  字段数量: {len(reg['fields'])}")
        for field in reg["fields"]:
            bit_range = field.get("bit_range", {})
            high = bit_range.get("high", -1)
            low = bit_range.get("low", -1)
            width = high - low + 1 if high >= 0 and low >= 0 else "未知"
            print(f"    字段: {field.get('name')}, 位置: high={high}, low={low}, 宽度: {width}")
```

## 注意事项

1. **性能影响**：调试信息生成可能略微增加代码生成时间，但通常可以忽略不计
2. **文件大小**：对于大型寄存器文件，调试信息可能显著增加文件大小
3. **生产环境**：在生产环境中应关闭调试信息，以减小文件大小和提高清晰度
4. **模板兼容性**：确保自定义模板正确处理 `enable_debug_info` 变量，使用 `|default(false)` 确保向后兼容 