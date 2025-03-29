# 寄存器生成器架构重构实施计划

## 总体目标

重构`autoregfile`项目的架构，改善代码组织，提高可扩展性和可维护性，为未来的功能增强奠定基础。

## 阶段划分

本实施计划将分为5个主要阶段，每个阶段都有明确的目标和可交付成果，以确保平稳过渡到新架构。

### 阶段1：准备与规划（第1周）

**目标**：完成初始设置和详细规划

**任务**：
1. 备份当前代码版本
2. 创建新的目录结构
3. 建立基础CI/CD流程
4. 编写详细的模块接口规范
5. 创建初始化的包结构

**可交付成果**：
- 完整的代码备份
- 新的目录结构
- 模块接口文档
- 初始化的包结构，包含`__init__.py`文件

### 阶段2：核心基础设施（第2-3周）

**目标**：实现新架构的核心组件

**任务**：
1. 实现日志系统（`utils/logger.py`）
2. 开发配置验证和规范化模块（`core/config/`）
3. 实现改进的模板管理系统（`core/template/`）
4. 创建寄存器类型系统（`core/data_model.py`）
5. 开发文件工具函数（`utils/file_utils.py`）

**可交付成果**：
- 可运行的核心基础设施组件
- 单元测试覆盖核心组件
- 核心组件的文档

### 阶段3：总线生成器重构（第4-5周）

**目标**：重构总线生成器系统

**任务**：
1. 实现基于装饰器的总线生成器注册机制（`core/bus_generators/factory.py`）
2. 增强基础总线生成器类（`core/bus_generators/base_generator.py`）
3. 迁移并改进自定义总线生成器（`core/bus_generators/custom_generator.py`）
4. 迁移并改进其他总线生成器（APB、AXI Lite、Wishbone）
5. 实现生成器测试

**可交付成果**：
- 完整的总线生成器框架
- 各总线协议的生成器实现
- 测试用例证明功能等同于之前版本

### 阶段4：解析器和主接口（第6周）

**目标**：重构解析器系统和主接口

**任务**：
1. 实现解析器基类（`parsers/base_parser.py`）
2. 迁移并改进Excel解析器（`parsers/excel_parser.py`）
3. 实现JSON解析器（`parsers/json_parser.py`）
4. 创建RegisterFactory类（`register_factory.py`）
5. 实现向后兼容的入口点（`regfile_gen.py`）

**可交付成果**：
- 完整的解析器系统
- 主接口实现
- 向后兼容的命令行入口

### 阶段5：CLI和测试完善（第7-8周）

**目标**：完善命令行接口和测试

**任务**：
1. 实现改进的命令行接口（`cli/`）
2. 创建集成测试
3. 添加示例和文档
4. 性能测试与优化
5. 代码审查和清理

**可交付成果**：
- 完整的命令行界面
- 全面的测试套件
- 更新的文档和示例
- 最终版本的发布准备

## 实施细节

### 目录结构创建

```bash
# 创建新的目录结构
mkdir -p autoregfile/cli
mkdir -p autoregfile/core/config
mkdir -p autoregfile/core/template
mkdir -p autoregfile/core/bus_generators
mkdir -p autoregfile/parsers
mkdir -p autoregfile/utils
mkdir -p autoregfile/templates/verilog/common
mkdir -p autoregfile/templates/verilog/bus
mkdir -p autoregfile/templates/verilog/field
mkdir -p autoregfile/templates/systemverilog
```

### 迁移策略

1. **逐模块迁移**：按照依赖顺序逐个迁移模块，从最基础的工具模块开始
2. **保持向后兼容**：确保原有入口点（`regfile_gen.py`）继续可用
3. **增量式测试**：每个模块迁移后立即进行测试
4. **并行开发**：依赖少的模块可并行开发

### 关键接口定义

#### `BusGeneratorFactory`接口

```python
@classmethod
def register(cls, protocol_name, generator_class): ...

@classmethod
def create_generator(cls, protocol_name, config, template_dirs=None): ...

@classmethod
def list_supported_protocols(cls): ...
```

#### `BaseBusGenerator`接口

```python
def __init__(self, config, template_dirs=None): ...

def generate(self, output_file): ...

def _prepare_context(self): ...

def _validate_protocol(self): ...
```

#### `RegisterFactory`接口

```python
def generate(self, config_file, output_file, bus_protocol=None, 
             template_dirs=None, debug=False): ...

@staticmethod
def list_supported_protocols(): ...

@staticmethod
def list_templates(category=None): ...
```

### 测试策略

1. **单元测试**：针对每个模块的核心功能
2. **集成测试**：检验模块间的交互
3. **功能测试**：验证生成结果是否符合预期
4. **向后兼容测试**：确保对之前项目的向后兼容性

## 风险和缓解措施

### 风险1：破坏现有功能

**缓解措施**：
- 全面的测试套件
- 保持原有接口向后兼容
- 逐个模块迁移和测试

### 风险2：模块间依赖关系复杂

**缓解措施**：
- 明确的模块接口定义
- 依赖注入模式
- 避免循环依赖

### 风险3：配置格式改变导致不兼容

**缓解措施**：
- 实现配置转换层
- 保持对旧格式的支持
- 明确文档说明

## 后续增强计划

完成架构重构后，可以考虑以下增强：

1. **图形用户界面**：基于新架构开发GUI
2. **更多总线协议支持**：添加更多协议支持
3. **验证功能**：添加生成验证模型的功能
4. **模板扩展**：支持更多编程语言的模板
5. **与IDE整合**：开发VSCode或PyCharm插件 