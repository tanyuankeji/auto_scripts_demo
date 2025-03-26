# AutoRegFile - 自动寄存器文件生成器

AutoRegFile是一个用于自动生成RTL寄存器文件的工具，支持多种寄存器类型和特性，以及自动地址分配和多种总线协议。

## 主要特性

1. 支持多种寄存器类型（ReadOnly, ReadWrite, WriteOnly, Write1Clean, Write1Set等）
2. 支持寄存器锁定（通过其他寄存器的值锁定寄存器）
3. 自动进行寄存器地址分配和管理
4. 支持多个地址块配置
5. 支持多种总线协议（APB, AXI-Lite, 自定义总线）
6. 生成字段级别的访问控制逻辑
7. 生成完整的文档

## 安装

```bash
pip install autoregfile
```

## 基本用法

1. 创建一个JSON配置文件，描述你的寄存器文件
2. 使用命令行工具生成RTL代码

```bash
python -m autoregfile.regfile_gen -c config.json -o regfile.v
```

## 配置文件格式

配置文件是一个JSON文件，包含以下部分：

```json
{
    "module_name": "my_regfile",
    "data_width": 32,
    "addr_width": 8,
    "bus_protocol": "apb",
    "registers": [
        {
            "name": "CTRL_REG",
            "address": "0x00",
            "type": "ReadWrite",
            "reset_value": "0x00000000",
            "description": "Control Register",
            "fields": [
                {
                    "name": "ENABLE",
                    "bits": "0",
                    "description": "Enable bit"
                },
                {
                    "name": "MODE",
                    "bits": "2:1",
                    "description": "Mode selection"
                }
            ]
        }
    ]
}
```

## 支持的寄存器类型

AutoRegFile支持多种寄存器类型，适应不同的使用场景：

1. **ReadWrite** - 标准读写寄存器
2. **ReadOnly** - 只读寄存器，写操作无效
3. **WriteOnly** - 只写寄存器，读取返回0
4. **Write1Clean** - 写1清零寄存器 (写1到某位将清零该位)
5. **Write1Set** - 写1置位寄存器 (写1到某位将置位该位)
6. **Write0Clean** - 写0清零寄存器 (写0到某位将清零该位)
7. **Write0Set** - 写0置位寄存器 (写0到某位将置位该位)
8. **WriteOnce** - 只能写一次的寄存器
9. **WriteOnlyOnce** - 只能写一次且只写的寄存器
10. **ReadClean** - 读取后自动清零的寄存器
11. **ReadSet** - 读取后自动置位的寄存器
12. **WriteReadClean** - 可写且读取后自动清零的寄存器
13. **WriteReadSet** - 可写且读取后自动置位的寄存器
14. **Write1Pulse** - 写1产生脉冲的寄存器
15. **Write0Pulse** - 写0产生脉冲的寄存器

## 寄存器锁定功能

AutoRegFile支持通过另一个寄存器的值锁定寄存器，这在需要防止运行时修改某些配置时非常有用：

```json
{
    "name": "CONFIG_REG",
    "type": "ReadWrite",
    "locked_by": ["CTRL_REG"],
    "description": "配置寄存器（当CTRL_REG[0]=1时锁定）"
}
```

在上面的例子中，当`CTRL_REG`的第0位为1时，`CONFIG_REG`将被锁定，不能被修改。

## 地址规划功能

AutoRegFile支持自动的寄存器地址分配和冲突检测功能：

1. 自动分配寄存器地址，不需要手动指定
2. 支持管理多个地址块，每个地址块有自己的地址空间
3. 自动检测地址冲突和对齐问题
4. 生成内存映射文档

要启用地址规划功能，可以在配置文件中设置`auto_address: true`，或使用命令行选项`--auto-address`：

```bash
python -m autoregfile.regfile_gen -c config.json -o regfile.v --auto-address
```

多地址块配置示例：

```json
{
    "module_name": "multi_block_example",
    "data_width": 32,
    "addr_width": 12,
    "address_blocks": [
        {
            "name": "CONTROL",
            "base_address": "0x000",
            "size": "0x100",
            "description": "控制寄存器区域"
        },
        {
            "name": "STATUS",
            "base_address": "0x100",
            "size": "0x100",
            "description": "状态寄存器区域"
        }
    ],
    "registers": [
        {
            "name": "CTRL_REG",
            "block": "CONTROL",
            "type": "ReadWrite"
        },
        {
            "name": "STATUS_REG",
            "block": "STATUS",
            "type": "ReadOnly"
        }
    ]
}
```

## 总线协议支持

AutoRegFile支持多种总线协议，可以根据需要选择适合项目的总线接口。当前支持的总线协议包括：

1. **APB总线** - ARM外设总线，简单易用，适合低速外设
2. **AXI-Lite总线** - ARM高级可扩展接口的简化版本，适合寄存器访问
3. **自定义总线** - 简单的自定义总线接口，可根据需要调整

要指定使用的总线协议，可以在配置文件中设置`bus_protocol`字段，或使用命令行选项`--bus-protocol`：

```bash
python -m autoregfile.regfile_gen -c config.json -o regfile.v --bus-protocol apb
```

每种总线协议的示例配置文件可以在`examples`目录中找到：
- `apb_protocol.json` - APB总线示例
- `axi_lite_protocol.json` - AXI-Lite总线示例

### APB总线接口

APB总线是一种简单的低速总线，接口信号包括：
- `paddr` - 地址信号
- `psel` - 选择信号
- `penable` - 使能信号
- `pwrite` - 写信号
- `pwdata` - 写数据
- `prdata` - 读数据
- `pready` - 就绪信号
- `pslverr` - 错误信号

### AXI-Lite总线接口

AXI-Lite是AXI协议的简化版本，提供更全面的总线功能，接口信号包括：
- 写地址通道 (AWADDR, AWVALID, AWREADY)
- 写数据通道 (WDATA, WSTRB, WVALID, WREADY)
- 写响应通道 (BRESP, BVALID, BREADY)
- 读地址通道 (ARADDR, ARVALID, ARREADY)
- 读数据通道 (RDATA, RRESP, RVALID, RREADY)

### 自定义总线接口

自定义总线提供了一个简单的接口，适合快速定制的场景，接口信号包括：
- `addr` - 地址信号
- `chip_select` - 片选信号
- `write_en` - 写使能
- `read_en` - 读使能
- `write_data` - 写数据
- `read_data` - 读数据
- `data_valid` - 数据有效信号

## 命令行选项

AutoRegFile提供了多个命令行选项来控制生成过程：

```
usage: regfile_gen.py [-h] -c CONFIG -o OUTPUT [--auto-address] [--bus-protocol {apb,axi_lite,custom}]

Register file generator

options:
  -h, --help            显示帮助信息并退出
  -c CONFIG, --config CONFIG
                        配置文件 (JSON)
  -o OUTPUT, --output OUTPUT
                        输出文件名
  --auto-address        启用自动地址分配
  --bus-protocol {apb,axi_lite,custom}
                        使用的总线协议 (默认: custom)
```

## 贡献

欢迎贡献代码，请参阅`CONTRIBUTING.md`了解更多信息。

## 许可证

本项目采用MIT许可证。
