# Excel 配置文件格式

AutoRegFile 支持使用 Excel 文件来配置寄存器和位域定义，本文档详细说明如何创建和使用 Excel 配置文件。

## Excel 文件结构

一个有效的 Excel 配置文件需要包含至少两个工作表：

1. `Registers` 工作表：定义所有寄存器
2. `Fields` 工作表：定义所有位域

此外，还可以包含一个可选的 `Config` 工作表，用于定义全局配置参数。

### Registers 工作表格式

`Registers` 工作表必须包含以下列：

| name | address | type | reset_value | description |
|------|---------|------|-------------|-------------|
| 寄存器名称 | 寄存器地址 | 寄存器类型 | 复位值 | 描述信息 |

示例内容：

| name | address | type | reset_value | description |
|------|---------|------|-------------|-------------|
| CTRL_REG | 0x00 | ReadWrite | 0x00000000 | 控制寄存器 |
| STATUS_REG | 0x04 | ReadOnly | 0x00000000 | 状态寄存器 |
| INT_FLAGS | 0x08 | ReadClean | 0x00000000 | 中断标志寄存器 |
| INT_ENABLE | 0x0C | ReadWrite | 0x00000000 | 中断使能寄存器 |

### Fields 工作表格式

`Fields` 工作表必须包含以下列：

| register | name | bit_range | description |
|----------|------|-----------|-------------|
| 所属寄存器名称 | 位域名称 | 位域范围 | 描述信息 |

示例内容：

| register | name | bit_range | description |
|----------|------|-----------|-------------|
| CTRL_REG | ENABLE | 0 | 使能位 |
| CTRL_REG | MODE | 2:1 | 模式设置 |
| CTRL_REG | START | 3 | 启动位 |
| STATUS_REG | BUSY | 0 | 忙状态标志 |
| STATUS_REG | ERROR | 1 | 错误标志 |
| INT_FLAGS | DATA_READY | 0 | 数据就绪中断 |
| INT_FLAGS | ERROR_FLAG | 1 | 错误中断 |
| INT_ENABLE | DATA_READY_EN | 0 | 数据就绪中断使能 |
| INT_ENABLE | ERROR_EN | 1 | 错误中断使能 |

### Config 工作表格式 (可选)

`Config` 工作表用于定义全局配置参数：

| parameter | value |
|-----------|-------|
| module_name | example_regfile |
| data_width | 32 |
| addr_width | 8 |
| num_write_ports | 1 |
| num_read_ports | 2 |
| sync_reset | false |
| reset_value | 0x00000000 |
| byte_enable | true |

## 使用 Excel 配置的优势

1. **直观易用**：Excel 是一个广泛使用的工具，对于非程序员也很友好
2. **表格格式**：数据以表格形式组织，便于查看和编辑
3. **导入导出**：可以轻松导入/导出为 CSV 或其他格式
4. **筛选和排序**：可以利用 Excel 的功能对数据进行筛选和排序
5. **公式计算**：可以使用公式自动计算地址偏移等

## 注意事项

1. 列名称必须与上述示例完全匹配（区分大小写）
2. 工作表名称必须为 `Registers`、`Fields` 和 `Config`（区分大小写）
3. Excel 文件可以是 `.xlsx` 或 `.xls` 格式
4. 数值可以使用十六进制（以 `0x` 开头）或十进制
5. 字符串值不需要引号

## 从其他格式转换

### 从 JSON 转换为 Excel

可以使用以下 Python 脚本将 JSON 配置转换为 Excel 格式：

```python
import json
import pandas as pd
from pathlib import Path

def json_to_excel(json_file, excel_file):
    # 读取 JSON 文件
    with open(json_file, 'r') as f:
        config = json.load(f)
    
    # 提取全局配置
    global_config = {k: v for k, v in config.items() if k not in ('registers', 'fields')}
    config_df = pd.DataFrame([(k, v) for k, v in global_config.items()], 
                            columns=['parameter', 'value'])
    
    # 提取寄存器定义
    registers_df = pd.DataFrame(config['registers'])
    
    # 提取位域定义
    fields_df = pd.DataFrame(config['fields'])
    
    # 创建 Excel 写入器
    with pd.ExcelWriter(excel_file) as writer:
        config_df.to_excel(writer, sheet_name='Config', index=False)
        registers_df.to_excel(writer, sheet_name='Registers', index=False)
        fields_df.to_excel(writer, sheet_name='Fields', index=False)
    
    print(f"已将 {json_file} 转换为 {excel_file}")

# 使用示例
json_to_excel('config.json', 'config.xlsx')
```

### 从 Excel 转换为 JSON

同样，可以使用以下脚本将 Excel 配置转换为 JSON 格式：

```python
import pandas as pd
import json
from pathlib import Path

def excel_to_json(excel_file, json_file):
    # 读取 Excel 文件中的工作表
    config_df = pd.read_excel(excel_file, sheet_name='Config')
    registers_df = pd.read_excel(excel_file, sheet_name='Registers')
    fields_df = pd.read_excel(excel_file, sheet_name='Fields')
    
    # 转换全局配置
    config_dict = {row['parameter']: row['value'] 
                  for _, row in config_df.iterrows()}
    
    # 添加寄存器和位域列表
    config_dict['registers'] = registers_df.to_dict('records')
    config_dict['fields'] = fields_df.to_dict('records')
    
    # 写入 JSON 文件
    with open(json_file, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"已将 {excel_file} 转换为 {json_file}")

# 使用示例
excel_to_json('config.xlsx', 'config.json')
```

## 示例

请参考 `examples/configs/example_config.xlsx` 作为 Excel 配置文件的示例。 