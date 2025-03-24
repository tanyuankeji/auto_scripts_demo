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