# 自定义模板

AutoRegFile 使用 Jinja2 模板引擎来生成各种输出文件。本文档介绍如何创建和使用自定义模板。

## 模板目录结构

标准模板目录结构如下：

```
templates/
├── verilog/          # Verilog 模板
│   ├── module.v.j2   # 模块模板
│   ├── regbank.v.j2  # 寄存器组模板
│   └── register.v.j2 # 单个寄存器模板
├── header/           # C 语言头文件模板
│   └── header.h.j2   # 头文件模板
└── doc/              # 文档模板
    └── doc.md.j2     # Markdown 文档模板
```

## 模板变量

### 所有模板共享的变量

- `module_name`: 模块名称
- `data_width`: 数据位宽
- `addr_width`: 地址位宽
- `num_write_ports`: 写端口数量
- `num_read_ports`: 读端口数量
- `sync_reset`: 是否使用同步复位
- `reset_value`: 复位值
- `byte_enable`: 是否启用字节使能
- `registers`: 寄存器列表
- `fields`: 位域列表

### Verilog 模板变量

- `word_count`: 寄存器字数
- `byte_count`: 字节数
- `byte_width`: 字节位宽

### 头文件模板变量

- `header_guard`: 头文件保护宏
- `module_upper`: 大写模块名称

### 文档模板变量

- `generation_time`: 生成时间
- `version`: 工具版本

## 创建自定义模板

### Verilog 模板示例

```jinja
// 自动生成的寄存器文件
// 生成时间: {{ generation_time }}
// 生成器版本: {{ version }}

module {{ module_name }} (
    input wire                      clk,
    input wire                      rst_n,
    
    {% for i in range(num_write_ports) %}
    // 写端口 {{ i }}
    input wire                      wr_en_{{ i }},
    input wire [{{ addr_width-1 }}:0]  wr_addr_{{ i }},
    input wire [{{ data_width-1 }}:0]  wr_data_{{ i }},
    {% if byte_enable %}
    input wire [{{ (data_width//8)-1 }}:0]  wr_be_{{ i }},
    {% endif %}
    {% endfor %}
    
    {% for i in range(num_read_ports) %}
    // 读端口 {{ i }}
    input wire [{{ addr_width-1 }}:0]  rd_addr_{{ i }},
    output reg [{{ data_width-1 }}:0]  rd_data_{{ i }}{% if not loop.last %},{% endif %}
    {% endfor %}
 );

// 寄存器地址常量定义
{% for reg in registers %}
localparam ADDR_{{ reg.name }} = {{ addr_width }}'h{{ reg.address[2:] }};   // {{ reg.description }} ({{ reg.type }}类型)
{% endfor %} 

// 寄存器声明
{% for reg in registers %}
reg [{{ data_width-1 }}:0] {{ reg.name|lower }}_reg;            // {{ reg.description }}
{% if reg.type == 'WriteOnce' %}
reg        {{ reg.name|lower }}_written;            // {{ reg.name }} 写标志
{% endif %}
{% endfor %} 

// 复位逻辑
{% if sync_reset %}
always @(posedge clk) begin
    if (rst_n == 1'b0) begin
{% else %}
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
{% endif %}
    {% for reg in registers %}
        {{ reg.name|lower }}_reg <= {{ data_width }}'h{{ reg.reset_value[2:] }};
        {% if reg.type == 'WriteOnce' %}
        {{ reg.name|lower }}_written <= 1'b0;
        {% endif %}
    {% endfor %}
    end
    else begin
        // 寄存器写逻辑
        {% for reg in registers %}
        {% if reg.type != 'ReadOnly' %}
        // {{ reg.name }} 是{{ reg.type }}类型寄存器
        {% for i in range(num_write_ports) %}
        {% if reg.type == 'WriteOnce' %}
        if (wr_en_{{ i }} && wr_addr_{{ i }} == ADDR_{{ reg.name }} && !{{ reg.name|lower }}_written) begin
            {{ reg.name|lower }}_written <= 1'b1;
        {% else %}
        if (wr_en_{{ i }} && wr_addr_{{ i }} == ADDR_{{ reg.name }}) begin
        {% endif %}
            {% if byte_enable %}
            if (wr_be_{{ i }}[0]) {{ reg.name|lower }}_reg[7:0] <= 
                {%- if reg.type == 'Write1Clean' %} {{ reg.name|lower }}_reg[7:0] & ~wr_data_{{ i }}[7:0];
                {%- elif reg.type == 'Write1Set' %} {{ reg.name|lower }}_reg[7:0] | wr_data_{{ i }}[7:0];
                {%- elif reg.type == 'Write0Clean' %} {{ reg.name|lower }}_reg[7:0] & wr_data_{{ i }}[7:0];
                {%- elif reg.type == 'Write0Set' %} {{ reg.name|lower }}_reg[7:0] | ~wr_data_{{ i }}[7:0];
                {%- else %} wr_data_{{ i }}[7:0];
                {%- endif %}
            // ... 其他字节
            {% else %}
            {{ reg.name|lower }}_reg <= 
                {%- if reg.type == 'Write1Clean' %} {{ reg.name|lower }}_reg & ~wr_data_{{ i }};
                {%- elif reg.type == 'Write1Set' %} {{ reg.name|lower }}_reg | wr_data_{{ i }};
                {%- elif reg.type == 'Write0Clean' %} {{ reg.name|lower }}_reg & wr_data_{{ i }};
                {%- elif reg.type == 'Write0Set' %} {{ reg.name|lower }}_reg | ~wr_data_{{ i }};
                {%- else %} wr_data_{{ i }};
                {%- endif %}
            {% endif %}
        end
        {% endfor %}
        {% endif %}
        {% endfor %}
        
        // 寄存器读逻辑
        {% for reg in registers %}
        {% if reg.type == 'ReadClean' %}
        // {{ reg.name }} 是 ReadClean 类型，读取后自动清零
        {% for i in range(num_read_ports) %}
        if (rd_addr_{{ i }} == ADDR_{{ reg.name }}) begin
            {{ reg.name|lower }}_reg <= {{ data_width }}'h0;
        end
        {% endfor %}
        {% elif reg.type == 'ReadSet' %}
        // {{ reg.name }} 是 ReadSet 类型，读取后自动置位
        {% for i in range(num_read_ports) %}
        if (rd_addr_{{ i }} == ADDR_{{ reg.name }}) begin
            {{ reg.name|lower }}_reg <= {{{ data_width }}{1'b1}};
        end
        {% endfor %}
        {% endif %}
        {% endfor %}
    end
end

// 读数据输出
{% for i in range(num_read_ports) %}
always @(*) begin
    case (rd_addr_{{ i }})
    {% for reg in registers %}
    {% if reg.type != 'WriteOnly' %}
        ADDR_{{ reg.name }}: rd_data_{{ i }} = {{ reg.name|lower }}_reg;
    {% else %}
        ADDR_{{ reg.name }}: rd_data_{{ i }} = {{ data_width }}'h0; // WriteOnly 类型，读取返回0
    {% endif %}
    {% endfor %}
        default: rd_data_{{ i }} = {{ data_width }}'h0;
    endcase
end
{% endfor %}

endmodule
```

### 头文件模板示例

```jinja
/**
 * @file {{ module_name }}.h
 * @brief 自动生成的寄存器头文件
 * @details 生成时间: {{ generation_time }}
 *          生成器版本: {{ version }}
 */

#ifndef {{ header_guard }}
#define {{ header_guard }}

/* 寄存器地址定义 */
{% for reg in registers %}
#define {{ module_upper }}_{{ reg.name }} 0x{{ reg.address[2:] }} /**< {{ reg.description }} */
{% endfor %}

/* 位域定义 */
{% for field in fields %}
#define {{ module_upper }}_{{ field.register }}_{{ field.name }}_MASK {% if ':' in field.bit_range %}{% set bits = field.bit_range.split(':') %}0x{{ '%08X' % ((2 ** (int(bits[0]) - int(bits[1]) + 1) - 1) << int(bits[1])) }}{% else %}0x{{ '%08X' % (1 << int(field.bit_range)) }}{% endif %} /**< {{ field.description }} */
#define {{ module_upper }}_{{ field.register }}_{{ field.name }}_SHIFT {% if ':' in field.bit_range %}{{ field.bit_range.split(':')[1] }}{% else %}{{ field.bit_range }}{% endif %} /**< {{ field.description }} 位偏移 */
{% endfor %}

#endif /* {{ header_guard }} */
```

### 文档模板示例

```jinja
# {{ module_name }} 寄存器手册

> 生成时间: {{ generation_time }}  
> 版本: {{ version }}

## 概述

本文档描述了 {{ module_name }} 模块的寄存器映射和功能。

## 接口信号

| 信号名 | 方向 | 位宽 | 描述 |
| ----- | ---- | ---- | ---- |
| clk | 输入 | 1 | 时钟信号 |
| rst_n | 输入 | 1 | 复位信号（低电平有效）|
{% for i in range(num_write_ports) %}
| wr_en_{{ i }} | 输入 | 1 | 写使能信号 (端口 {{ i }}) |
| wr_addr_{{ i }} | 输入 | {{ addr_width }} | 写地址 (端口 {{ i }}) |
| wr_data_{{ i }} | 输入 | {{ data_width }} | 写数据 (端口 {{ i }}) |
{% if byte_enable %}| wr_be_{{ i }} | 输入 | {{ data_width//8 }} | 字节使能 (端口 {{ i }}) |{% endif %}
{% endfor %}
{% for i in range(num_read_ports) %}
| rd_addr_{{ i }} | 输入 | {{ addr_width }} | 读地址 (端口 {{ i }}) |
| rd_data_{{ i }} | 输出 | {{ data_width }} | 读数据 (端口 {{ i }}) |
{% endfor %}

## 寄存器映射

| 地址 | 名称 | 类型 | 复位值 | 描述 |
| ---- | ---- | ---- | ------ | ---- |
{% for reg in registers %}
| 0x{{ reg.address[2:] }} | {{ reg.name }} | {{ reg.type }} | 0x{{ reg.reset_value[2:] }} | {{ reg.description }} |
{% endfor %}

## 寄存器详细说明

{% for reg in registers %}
### {{ reg.name }} (0x{{ reg.address[2:] }})

**描述**: {{ reg.description }}

**类型**: {{ reg.type }}

**复位值**: 0x{{ reg.reset_value[2:] }}

| 位域 | 名称 | 描述 |
| ---- | ---- | ---- |
{% for field in fields %}
{% if field.register == reg.name %}
| {% if ':' in field.bit_range %}{{ field.bit_range }}{% else %}{{ field.bit_range }}{% endif %} | {{ field.name }} | {{ field.description }} |
{% endif %}
{% endfor %}

{% endfor %}
```

## 使用自定义模板

使用命令行参数指定自定义模板目录：

```bash
regfile-gen -c config.json -o output.v -t my_templates_dir
```

或者在Python代码中指定：

```python
from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator

parser = JsonParser()
config = parser.parse("config.json")

verilog_gen = VerilogGenerator(template_dir="my_templates_dir")
verilog_code = verilog_gen.generate(config)
verilog_gen.save(verilog_code, "example_regfile.v")
```

## 模板开发建议

1. 首先复制默认模板作为基础
2. 逐步修改需要定制的部分
3. 保持模板变量名称不变
4. 添加注释说明模板逻辑
5. 测试模板在不同配置下的输出结果

## 注意事项

1. 模板使用 Jinja2 语法，支持控制流、过滤器和宏
2. 确保模板目录结构与默认结构一致
3. 自定义模板可能需要根据工具版本更新 

## 在模板中支持调试信息功能

从v1.2.0版本开始，AutoRegFile支持在生成的Verilog文件中添加调试信息，帮助开发人员更好地理解寄存器的生成过程和排查问题。本节介绍如何在自定义模板中实现调试信息控制。

### 调试信息上下文变量

在模板上下文中，我们提供了以下变量用于控制调试信息的显示：

- `enable_debug_info`: 布尔值，表示是否启用调试信息。这个值由用户通过命令行参数`--debug-info`或API中的`enable_debug_info`参数控制。

### 在模板中使用调试信息控制

下面是一个模板示例，展示如何在模板中使用条件语句控制调试信息的生成：

```jinja
// =============================================================================
// 自动生成的寄存器文件: {{ module_name }}
// 生成时间: {{ generation_time }}
// =============================================================================

{% if enable_debug_info|default(false) %}
// =============================================================================
// 调试信息（仅在开启调试模式时生成）
// =============================================================================
// DEBUG: 字段位置信息
{% for reg in registers %}
// {{ reg.name }} 寄存器字段调试信息
{% if reg.has_fields %}
// 原始字段数量: {{ reg.fields|length }}
{% for field in reg.fields %}
// 字段名: {{ field.name }}, 位范围: high={{ field.bit_range.high }}, low={{ field.bit_range.low }}, width={{ field.width }}
{% endfor %}
{% endif %}
{% endfor %}

// DEBUG: 寄存器宽度信息
{% for reg in registers %}
// {{ reg.name }} 寄存器宽度: {{ reg.width }}
{% endfor %}
// =============================================================================
{% endif %}

// 常规Verilog代码...
```

### 最佳实践

1. **条件包装**：始终使用条件语句包装调试信息，确保只有在用户明确请求时才生成
   ```jinja
   {% if enable_debug_info|default(false) %}
   // 调试信息内容
   {% endif %}
   ```

2. **明确标记**：使用明显的注释标记调试信息的开始和结束，便于在生成文件中识别
   ```jinja
   // =============================================================================
   // 调试信息（仅在开启调试模式时生成）
   // =============================================================================
   ```

3. **分类信息**：将不同类型的调试信息分类展示，增强可读性
   ```jinja
   // DEBUG: 字段位置信息
   // ...
   
   // DEBUG: 寄存器宽度信息
   // ...
   ```

4. **提供默认值**：使用`default`过滤器为`enable_debug_info`提供默认值，增强模板的健壮性
   ```jinja
   {% if enable_debug_info|default(false) %}
   ```

5. **放置位置**：将调试信息放在文件开头，便于快速定位和查看

### 添加自定义调试信息

除了标准的字段位置和寄存器宽度信息外，你还可以添加自定义的调试信息：

```jinja
{% if enable_debug_info|default(false) %}
// 自定义调试信息
// 总线配置: 数据宽度={{ data_width }}, 地址宽度={{ addr_width }}
// 总寄存器数量: {{ registers|length }}

// 寄存器地址映射:
{% for reg in registers %}
// {{ reg.name }}: 地址=0x{{ '%08X' % reg.address|replace('0x', '')|int(16) }}
{% endfor %}
{% endif %}
```

### 调试复杂计算

对于复杂的模板计算逻辑，可以添加中间步骤的调试信息：

```jinja
{% if enable_debug_info|default(false) %}
// 宽度计算过程调试
{% for reg in registers %}
{% if reg.has_fields %}
// {{ reg.name }} 宽度计算:
{% set max_high = -1 %}
{% for field in reg.fields %}
// 考虑字段 {{ field.name }}: high={{ field.bit_range.high }}
{% set max_high = [max_high, field.bit_range.high]|max %}
{% endfor %}
// 最终最高位: {{ max_high }}
// 计算宽度: {{ max_high + 1 }}
{% endif %}
{% endfor %}
{% endif %}
```

### 排查模板问题

如果你的模板生成的内容不符合预期，开启调试信息可以帮助你：

1. 确认上下文数据是否正确：打印关键变量的值
2. 追踪复杂计算的中间结果：在关键步骤添加调试信息
3. 验证条件分支执行情况：在不同条件分支添加标记，查看哪些分支被执行

### 示例：排查寄存器宽度计算问题

```jinja
{% if enable_debug_info|default(false) %}
// 排查宽度计算问题
{% for reg in registers %}
// {{ reg.name }} 宽度调试:
// 1. 直接指定宽度: {{ reg.width|default('未指定') }}
// 2. 从bit_range计算:
{% if reg.bit_range is defined %}
//    bit_range: {{ reg.bit_range|string }}
//    计算宽度: {{ reg.bit_range.high - reg.bit_range.low + 1 if reg.bit_range is mapping else '无法计算' }}
{% else %}
//    无bit_range定义
{% endif %}
// 3. 从字段计算:
{% if reg.has_fields %}
//    字段数量: {{ reg.fields|length }}
//    最高位字段: {{ reg.fields|sort(attribute='bit_range.high')|last|string|default('无字段') if reg.fields else '无字段' }}
//    最高位: {{ reg.fields|map(attribute='bit_range.high')|max|default(-1) if reg.fields else '无法确定' }}
{% else %}
//    无字段定义
{% endif %}
// 最终使用的宽度: {{ reg.width|default('使用默认值 ' ~ data_width) }}
{% endfor %}
{% endif %}
```

### 总结

调试信息是一个强大的工具，可以帮助你理解寄存器文件的生成过程，更快地排查问题。通过在自定义模板中实现良好的调试支持，你可以显著提高开发效率和代码质量。实践中应谨记：

1. 调试信息应当是有选择性的，不要默认启用
2. 调试信息应当是全面的，覆盖关键数据结构和计算过程
3. 调试信息应当是可读的，使用清晰的格式和分类
4. 调试信息不应影响生成代码的功能 