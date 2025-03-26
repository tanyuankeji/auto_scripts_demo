# AutoRegFile 总线协议支持

本文档详细介绍了 AutoRegFile 工具对各种总线协议的支持情况、配置选项以及自定义模板功能。

## 支持的总线协议

AutoRegFile 当前支持以下总线协议：

1. **APB 总线** - ARM 外设总线，简单易用，适合低速外设
2. **AXI-Lite 总线** - ARM 高级可扩展接口的简化版本，适合寄存器访问
3. **Wishbone 总线** - 开源总线标准，广泛用于开源硬件设计
4. **OCP (Open Core Protocol)** - 开放核心协议，用于IP核互连
5. **自定义总线** - 简单的自定义总线接口，可根据需要调整

## 如何指定总线协议

有两种方式可以指定要使用的总线协议：

### 1. 在配置文件中指定

在 JSON 配置文件中添加 `bus_protocol` 字段：

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

### 2. 通过命令行参数指定

使用 `--bus-protocol` 命令行选项：

```bash
regfile-gen -c config.json -o regfile.v --bus-protocol wishbone
```

命令行参数会覆盖配置文件中的设置。

## 总线协议详解

### APB 总线

APB (Advanced Peripheral Bus) 是 ARM AMBA 协议规范的一部分，主要用于低性能外设的控制和状态寄存器访问。

#### 接口信号

| 信号名 | 方向 | 描述 |
|-------|------|------|
| `paddr` | 输入 | 地址总线 |
| `psel` | 输入 | 从设备选择信号 |
| `penable` | 输入 | 使能信号，表示传输的第二个周期 |
| `pwrite` | 输入 | 读写控制信号 |
| `pwdata` | 输入 | 写数据总线 |
| `prdata` | 输出 | 读数据总线 |
| `pready` | 输出 | 就绪信号，表示从设备准备好完成传输 |
| `pslverr` | 输出 | 错误信号，表示传输错误 |

#### 时序图

```
      T1       T2       T3       T4
   _______   _______   _______   _______
  |       | |       | |       | |       |
__|       |_|       |_|       |_|       |__ 时钟

  _________XXXXXXXXX_____________________ 地址 (paddr)
                    
  _________         _____________________ 选择信号 (psel)
                    
  _________________         ___________ 使能信号 (penable)
                    
  _________XXXXXXXXX_____________________ 读写控制 (pwrite)
                    
  _________XXXXXXXXX_____________________ 写数据 (pwdata)
                    
  _________________XXXXXXXXX___________ 读数据 (prdata)
```

### AXI-Lite 总线

AXI-Lite (Advanced eXtensible Interface Lite) 是 ARM AMBA 协议的简化版本，适用于寄存器访问。它比 APB 提供了更好的性能和更全面的功能，同时比完整的 AXI 协议更简单。

#### 通道描述

AXI-Lite 协议包含五个独立的通道：

1. **写地址通道** - 传输写操作的地址
2. **写数据通道** - 传输写操作的数据
3. **写响应通道** - 从设备对写操作的响应
4. **读地址通道** - 传输读操作的地址
5. **读数据通道** - 传输读操作的数据和响应

#### 接口信号

##### 写地址通道
| 信号名 | 方向 | 描述 |
|-------|------|------|
| `s_axil_awaddr` | 输入 | 写地址 |
| `s_axil_awvalid` | 输入 | 写地址有效 |
| `s_axil_awready` | 输出 | 写地址就绪 |

##### 写数据通道
| 信号名 | 方向 | 描述 |
|-------|------|------|
| `s_axil_wdata` | 输入 | 写数据 |
| `s_axil_wstrb` | 输入 | 写数据字节有效信号 |
| `s_axil_wvalid` | 输入 | 写数据有效 |
| `s_axil_wready` | 输出 | 写数据就绪 |

##### 写响应通道
| 信号名 | 方向 | 描述 |
|-------|------|------|
| `s_axil_bresp` | 输出 | 写响应状态 |
| `s_axil_bvalid` | 输出 | 写响应有效 |
| `s_axil_bready` | 输入 | 写响应就绪 |

##### 读地址通道
| 信号名 | 方向 | 描述 |
|-------|------|------|
| `s_axil_araddr` | 输入 | 读地址 |
| `s_axil_arvalid` | 输入 | 读地址有效 |
| `s_axil_arready` | 输出 | 读地址就绪 |

##### 读数据通道
| 信号名 | 方向 | 描述 |
|-------|------|------|
| `s_axil_rdata` | 输出 | 读数据 |
| `s_axil_rresp` | 输出 | 读响应状态 |
| `s_axil_rvalid` | 输出 | 读数据有效 |
| `s_axil_rready` | 输入 | 读数据就绪 |

### Wishbone 总线

Wishbone 是一种开源的片上互连总线规范，被广泛用于开源硬件设计中。它提供了简单、灵活的接口，支持不同的传输类型。

#### 接口信号

| 信号名 | 方向 | 描述 |
|-------|------|------|
| `wb_adr_i` | 输入 | 地址输入 |
| `wb_dat_i` | 输入 | 数据输入 |
| `wb_dat_o` | 输出 | 数据输出 |
| `wb_we_i` | 输入 | 写使能信号 |
| `wb_sel_i` | 输入 | 字节选通信号 |
| `wb_stb_i` | 输入 | 选通信号 |
| `wb_cyc_i` | 输入 | 总线周期信号 |
| `wb_ack_o` | 输出 | 确认信号 |
| `wb_err_o` | 输出 | 错误信号 |

### OCP 总线

OCP (Open Core Protocol) 是一种开放的标准接口，用于IP核之间的通信。它提供了一套灵活的接口，适用于各种不同的IP集成场景。

#### 接口信号

| 信号名 | 方向 | 描述 |
|-------|------|------|
| `MAddr` | 输入 | 主地址 |
| `MCmd` | 输入 | 主命令 (0:空闲, 1:写, 2:读) |
| `MData` | 输入 | 主写数据 |
| `MByteEn` | 输入 | 主字节使能 |
| `MRespAccept` | 输入 | 主响应接收 |
| `SData` | 输出 | 从读数据 |
| `SResp` | 输出 | 从响应状态 (0:空闲, 1:完成, 2:错误) |
| `SCmdAccept` | 输出 | 从命令接收 |

### 自定义总线

自定义总线提供了一个简单的通用接口，适用于特定的定制需求。它采用简单的握手机制和分离的读写控制信号。

#### 接口信号

| 信号名 | 方向 | 描述 |
|-------|------|------|
| `addr` | 输入 | 地址总线 |
| `chip_select` | 输入 | 片选信号 |
| `write_en` | 输入 | 写使能 |
| `read_en` | 输入 | 读使能 |
| `write_data` | 输入 | 写数据总线 |
| `read_data` | 输出 | 读数据总线 |
| `data_valid` | 输出 | 数据有效信号 |

## 总线协议高级配置选项

AutoRegFile 提供了丰富的配置选项，可以根据需要调整总线协议的行为。这些配置选项可以在 JSON 配置文件中的 `bus_options` 字段中指定。

### 配置选项结构

```json
{
    "bus_options": {
        "common": {
            // 适用于所有总线协议的通用配置
        },
        "apb": {
            // 仅适用于 APB 总线协议的配置
        },
        "axi_lite": {
            // 仅适用于 AXI-Lite 总线协议的配置
        },
        "wishbone": {
            // 仅适用于 Wishbone 总线协议的配置
        },
        "ocp": {
            // 仅适用于 OCP 总线协议的配置
        }
    }
}
```

### 通用配置选项

以下配置选项适用于所有总线协议：

#### 超时配置

```json
"timeout": {
    "enable": true,        // 是否启用超时机制
    "cycles": 16,          // 超时周期数
    "action": "error"      // 超时动作：error (错误), reset (复位), interrupt (中断)
}
```

#### 延迟配置

```json
"delay": {
    "read": 2,             // 读操作延迟周期数
    "write": 1,            // 写操作延迟周期数
    "response": 0          // 响应延迟周期数
}
```

#### 错误处理配置

```json
"error_handling": {
    "response": "error",   // 错误响应类型：default (默认), error (错误), busy (忙), timeout (超时)
    "reporting": true      // 是否启用错误报告
}
```

### 特定总线协议配置选项

#### AXI-Lite 特有配置

```json
"write_strobes": true      // 是否支持字节选通写入
```

#### Wishbone 特有配置

```json
"classic_cycle": true      // 是否使用经典周期模式
```

### 示例配置

下面是一个包含多种总线协议配置选项的完整示例：

```json
{
    "bus_options": {
        "common": {
            "timeout": {
                "enable": true,
                "cycles": 16,
                "action": "error"
            },
            "error_handling": {
                "response": "error",
                "reporting": true
            }
        },
        "wishbone": {
            "classic_cycle": true,
            "delay": {
                "read": 2,
                "write": 1,
                "response": 0
            }
        },
        "axi_lite": {
            "write_strobes": true,
            "delay": {
                "read": 1,
                "write": 1,
                "response": 2
            }
        }
    }
}
```

完整的示例配置文件可以在 `examples/bus_options_example.json` 中找到。

## 自定义总线模板

AutoRegFile 支持自定义总线模板，允许用户定义自己的总线接口实现。

### 使用自定义模板

有两种方式可以指定自定义模板：

#### 1. 在配置文件中指定

```json
{
    "bus_options": {
        "template": "verilog/bus/my_custom_bus.v.j2"
    }
}
```

#### 2. 通过命令行参数指定

```bash
regfile-gen -c config.json -o regfile.v --custom-template verilog/bus/my_custom_bus.v.j2
```

### 创建自定义模板

#### 步骤 1: 创建用户模板目录

使用以下命令创建用户模板目录：

```bash
regfile-gen --create-template-dir
```

这将在 `~/.autoregfile/templates` 目录下创建必要的目录结构。

#### 步骤 2: 复制现有模板作为基础

复制现有的总线模板作为自定义模板的基础：

```bash
regfile-gen --copy-template verilog/bus/apb.v.j2
```

这将把系统模板复制到用户模板目录，然后可以进行修改。

#### 步骤 3: 修改模板

编辑复制的模板文件，根据需要进行自定义。模板使用 Jinja2 模板语法，可以访问配置数据和定义好的上下文变量。

#### 步骤 4: 使用自定义模板

```bash
regfile-gen -c config.json -o regfile.v --custom-template ~/.autoregfile/templates/verilog/bus/my_custom_bus.v.j2
```

### 模板上下文变量

模板中可以使用以下上下文变量：

- `module_name` - 模块名称
- `data_width` - 数据宽度
- `addr_width` - 地址宽度
- `registers` - 寄存器列表
- `generation_time` - 生成时间戳
- `bus_protocol` - 总线协议名称
- `register_outputs` - 自动生成的寄存器输出端口
- 各种配置选项 - 如 `timeout_enable`, `read_delay` 等

## 总线协议验证

AutoRegFile 包含总线协议验证功能，确保生成的 RTL 代码符合总线规范。验证过程会检查以下内容：

1. 数据和地址宽度是否符合协议规范
2. 寄存器地址是否按协议要求对齐
3. 寄存器类型是否与总线协议兼容
4. 配置选项是否有效

验证过程中发现的问题会以警告或错误的形式报告。严重错误会导致生成过程中止，而警告则会继续生成过程但可能导致生成的代码不符合预期。

### 验证示例

```bash
regfile-gen -c config.json -o regfile.v --debug
```

使用 `--debug` 选项可以查看更详细的验证信息。

## 高级特性与总线协议的交互

### 脉冲寄存器

脉冲寄存器（`Write1Pulse` 和 `Write0Pulse` 类型）在使用总线协议时会生成额外的输出信号。对于每个脉冲寄存器，将生成一个同名但以 `_pulse` 为后缀的输出端口。

### 寄存器锁定

使用 `locked_by` 属性可以指定寄存器被锁定的条件。锁定后的寄存器在总线写操作中将被忽略。

## 管理总线模板

### 列出所有支持的总线协议

```bash
regfile-gen --list-protocols
```

### 列出所有可用的总线模板

```bash
regfile-gen --list-bus-templates
```

### 列出所有模板

```bash
regfile-gen --list-templates
```

## 测试总线协议功能

可以使用 `tests/test_bus_protocol.py` 脚本来测试总线协议功能：

```bash
cd autoregfile
python -m tests.test_bus_protocol
```

该测试验证了：
- 各种总线协议的生成
- 脉冲寄存器在总线接口中的实现
- 寄存器锁定功能在总线接口中的实现
- 总线配置选项的应用 