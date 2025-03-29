# AutoRegFile - 寄存器文件生成器

AutoRegFile是一个灵活的寄存器文件生成工具，可以根据配置文件生成各种总线协议的寄存器文件。

## 项目架构

本项目采用模块化设计，主要组件包括：

```
autoregfile/
├── cli/                 # 命令行界面
├── core/                # 核心功能模块
│   ├── config/          # 配置管理
│   ├── template/        # 模板管理
│   ├── bus_generators/  # 总线生成器
│   │   ├── base_generator.py    # 总线生成器基类
│   │   ├── custom_generator.py  # 自定义总线生成器
│   │   ├── factory.py           # 总线生成器工厂
│   │   └── ...                  # 其他总线生成器
├── parsers/             # 配置解析器
│   ├── parser_base.py   # 解析器基类
│   ├── excel_parser.py  # Excel配置解析器
│   ├── json_parser.py   # JSON配置解析器
│   └── ...              # 其他格式解析器
├── templates/           # 模板文件
│   ├── verilog/         # Verilog模板
│   │   ├── bus/         # 总线接口模板
│   │   ├── common/      # 通用模板片段
│   │   └── field/       # 字段访问模板
│   └── systemverilog/   # SystemVerilog模板
├── utils/               # 工具函数
└── register_factory.py  # 主接口
```

## 已完成组件

目前已经完成了以下组件的重构：

1. **日志工具模块** (`utils/logger.py`)
   - 支持多级别日志
   - 可配置输出格式和目标

2. **寄存器类型管理模块** (`core/regtype.py`)
   - 支持多种寄存器类型定义
   - 提供类型验证和管理功能

3. **解析器系统** 
   - 基础解析器接口 (`parsers/parser_base.py`)
   - Excel配置解析器 (`parsers/excel_parser.py`)
   - JSON配置解析器 (`parsers/json_parser.py`)

4. **总线生成器系统**
   - 总线生成器工厂 (`core/bus_generators/factory.py`)
   - 总线生成器基类 (`core/bus_generators/base_generator.py`)
   - 自定义总线生成器 (`core/bus_generators/custom_generator.py`)

5. **模板管理系统**
   - 模板管理器 (`core/template_manager.py`)
   - 模板工具模块 (`utils/template_tools.py`)

6. **主接口**
   - 寄存器工厂 (`register_factory.py`)
   - 命令行入口 (`regfile_gen.py`)

## 使用方法

### 基本用法

```bash
python -m autoregfile.regfile_gen config.xlsx -o regfile.v -p custom
```

### 高级用法

#### 使用自定义模板

```bash
python -m autoregfile.regfile_gen config.xlsx -o regfile.v -p custom -t /path/to/template/dir
```

#### 创建自定义模板目录

```bash
python -m autoregfile.utils.template_tools create /path/to/template/dir -p custom
```

#### 列出可用模板

```bash
python -m autoregfile.utils.template_tools list -c bus
```

## 扩展指南

### 添加新的总线协议生成器

1. 创建继承自`BaseBusGenerator`的新类
2. 使用`@BusGeneratorFactory.register_protocol`装饰器注册
3. 创建对应的总线模板

### 添加新的配置格式解析器

1. 创建继承自`ParserBase`的新类
2. 在`__init__.py`中注册解析器

## 开发计划

- [ ] 添加图形用户界面
- [ ] 支持更多总线协议（AXI4, Wishbone）
- [ ] 支持更多输出格式（SystemVerilog, YAML）
- [ ] 验证功能和测试生成 