# AutoRegFile 总线协议增强功能

本文档总结了AutoRegFile工具的总线协议增强功能，包括新增的总线协议支持、自定义模板功能、配置选项和验证功能。

## 1. 新增总线协议

除了原有的APB、AXI-Lite和自定义总线协议外，我们新增了以下总线协议支持：

- **Wishbone总线** - 开源总线标准，广泛用于开源硬件设计
- **OCP总线** - 开放核心协议，用于IP核互连

### 使用新增总线协议

可以通过配置文件或命令行参数指定要使用的总线协议：

**配置文件示例：**
```json
{
    "module_name": "my_regfile",
    "data_width": 32,
    "addr_width": 8,
    "bus_protocol": "wishbone",
    "registers": [
        // ...寄存器定义...
    ]
}
```

**命令行示例：**
```bash
regfile-gen -c config.json -o regfile.v --bus-protocol wishbone
```

## 2. 总线协议配置选项

新增了丰富的配置选项，可以根据需要调整总线协议的行为。

### 通用配置选项

所有总线协议都支持以下配置选项：

- **超时配置** - 设置超时检测和处理
- **延迟配置** - 设置读写操作的延迟
- **错误处理配置** - 定制错误响应方式

### 配置示例

```json
{
    "bus_options": {
        "common": {
            "timeout": {
                "enable": true,
                "cycles": 16,
                "action": "error"
            },
            "delay": {
                "read": 2,
                "write": 1,
                "response": 0
            },
            "error_handling": {
                "response": "error",
                "reporting": true
            }
        },
        "wishbone": {
            "classic_cycle": true
        },
        "axi_lite": {
            "write_strobes": true
        }
    }
}
```

## 3. 自定义总线模板

### 总线模板管理工具

添加了专用的模板管理工具，可通过以下命令使用：

```bash
# 列出所有模板
template-manager --list

# 列出总线模板
template-manager --list-bus

# 创建用户模板目录
template-manager --create-dir

# 复制系统模板
template-manager --copy verilog/bus/apb.v.j2

# 创建新的总线模板
template-manager --create-bus my_custom_bus
```

### 使用自定义模板

可以在配置文件中指定要使用的自定义模板：

```json
{
    "bus_options": {
        "template": "verilog/bus/my_custom_bus.v.j2"
    }
}
```

或通过命令行参数指定：

```bash
regfile-gen -c config.json -o regfile.v --custom-template verilog/bus/my_custom_bus.v.j2
```

## 4. 总线协议验证

增加了总线协议验证功能，确保生成的RTL代码符合总线规范。验证内容包括：

- 数据和地址宽度是否符合协议规范
- 寄存器地址是否按协议要求对齐
- 寄存器类型与总线协议的兼容性
- 配置选项的有效性

验证结果会以警告或错误的形式报告，在生成过程中直接显示。

## 5. 命令行工具增强

更新了主命令行工具，添加了新的参数和功能：

```bash
# 列出支持的总线协议
regfile-gen --list-protocols

# 列出可用的模板
regfile-gen --list-templates

# 列出总线模板
regfile-gen --list-bus-templates

# 复制模板
regfile-gen --copy-template verilog/bus/apb.v.j2

# 创建模板目录
regfile-gen --create-template-dir

# 使用自定义模板
regfile-gen -c config.json -o regfile.v --custom-template verilog/bus/my_custom_bus.v.j2

# 使用自定义模板目录
regfile-gen -c config.json -o regfile.v --template-dir ~/my_templates

# 启用调试模式
regfile-gen -c config.json -o regfile.v --debug
```

## 6. 示例配置文件

提供了多个示例配置文件，演示不同的功能：

- `examples/bus_options_example.json` - 展示总线配置选项
- `examples/custom_template_example.json` - 展示自定义模板使用方法
- `examples/wishbone_example.json` - Wishbone总线示例
- `examples/ocp_example.json` - OCP总线示例

## 7. 使用流程示例

### 创建并使用自定义总线模板

1. 创建模板目录
   ```bash
   template-manager --create-dir
   ```

2. 创建新的总线模板
   ```bash
   template-manager --create-bus my_protocol
   ```

3. 编辑生成的模板文件
   ```bash
   vim ~/.autoregfile/templates/verilog/bus/my_protocol.v.j2
   ```

4. 创建使用该模板的配置文件
   ```json
   {
       "module_name": "my_regfile",
       "data_width": 32,
       "addr_width": 8,
       "bus_protocol": "custom",
       "bus_options": {
           "template": "verilog/bus/my_protocol.v.j2"
       },
       "registers": [
           // ...寄存器定义...
       ]
   }
   ```

5. 生成寄存器文件
   ```bash
   regfile-gen -c my_config.json -o my_regfile.v
   ```

### 使用总线配置选项

1. 创建配置文件，包含总线配置选项
   ```json
   {
       "module_name": "my_regfile",
       "data_width": 32,
       "addr_width": 8,
       "bus_protocol": "wishbone",
       "bus_options": {
           "common": {
               "timeout": {
                   "enable": true,
                   "cycles": 16,
                   "action": "error"
               }
           },
           "wishbone": {
               "classic_cycle": true
           }
       },
       "registers": [
           // ...寄存器定义...
       ]
   }
   ```

2. 生成寄存器文件
   ```bash
   regfile-gen -c my_config.json -o my_regfile.v
   ```

## 8. 后续开发建议

以下是对AutoRegFile工具总线协议支持的后续开发建议：

1. 添加更多总线协议支持，如SPI、I2C等串行接口协议
2. 实现总线协议转换功能，支持不同总线协议之间的桥接
3. 添加总线性能分析功能，提供带宽和延迟等指标的评估
4. 增强验证功能，支持形式化验证和仿真测试生成
5. 添加总线协议可视化功能，生成波形图和时序图
6. 支持更多硬件描述语言，如VHDL、SystemVerilog等 