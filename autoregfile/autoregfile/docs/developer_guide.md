# AutoRegFile 开发者指南

## 简介

本文档面向希望扩展或修改AutoRegFile的开发者，详细介绍了项目架构、关键组件和扩展方法。

## 项目架构

AutoRegFile采用模块化设计，主要组件包括：

```
autoregfile/
├── cli/                 # 命令行界面
├── core/                # 核心功能模块
│   ├── config/          # 配置管理
│   ├── template_manager.py # 模板管理器
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
├── utils/               # 工具函数
└── register_factory.py  # 主接口
```

## 核心组件

### 1. 总线生成器系统

#### 基类: `BaseBusGenerator`

总线生成器的基础类，定义了生成器的公共接口和功能。

```python
class BaseBusGenerator:
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        # 初始化生成器
        
    def _set_config_defaults(self) -> None:
        # 设置配置默认值
        
    def _cleanup_config(self) -> None:
        # 清理配置，确保格式正确
        
    def _get_template_path(self) -> Optional[str]:
        # 获取模板路径
        
    def _prepare_context(self) -> Dict[str, Any]:
        # 准备渲染上下文
        
    def generate(self, output_file: str) -> bool:
        # 生成寄存器文件
```

#### 工厂: `BusGeneratorFactory`

管理和创建总线生成器实例的工厂类。

```python
class BusGeneratorFactory:
    @classmethod
    def register_protocol(cls, protocol_name: str) -> Callable:
        # 注册总线协议生成器
        
    @classmethod
    def create_generator(cls, bus_protocol: str, config: Dict[str, Any], 
                         template_dirs: Optional[List[str]] = None,
                         external_generator_dirs: Optional[List[str]] = None) -> Optional[BaseBusGenerator]:
        # 创建总线生成器实例
        
    @classmethod
    def list_supported_protocols(cls) -> List[str]:
        # 列出支持的总线协议
```

### 2. 解析器系统

#### 基类: `ParserBase`

配置解析器的基础类，定义了解析器的公共接口。

```python
class ParserBase:
    def __init__(self, config_file: str):
        # 初始化解析器
        
    def parse(self) -> Dict[str, Any]:
        # 解析配置文件
        
    def validate(self, config: Dict[str, Any]) -> bool:
        # 验证配置是否有效
```

#### 具体实现

- `ExcelParser`: 解析Excel格式的配置文件
- `JsonParser`: 解析JSON格式的配置文件
- `YamlParser`: 解析YAML格式的配置文件

### 3. 模板管理系统

#### 模板管理器: `TemplateManager`

管理和渲染模板文件的类。

```python
class TemplateManager:
    def __init__(self, template_dirs: Optional[List[str]] = None):
        # 初始化模板管理器
        
    def add_template_dirs(self, template_dirs: List[str]) -> None:
        # 添加模板目录
        
    def find_template(self, template_path: str) -> Optional[str]:
        # 查找模板文件
        
    def render_template(self, template_path: str, context: Dict[str, Any]) -> Optional[str]:
        # 渲染模板
```

### 4. 主接口: `register_factory.py`

提供统一的对外接口，整合解析器和生成器功能。

```python
def generate_register_file(config_file: Optional[str] = None,
                          config_dict: Optional[Dict[str, Any]] = None,
                          output_file: str = "regfile.v",
                          bus_protocol: str = "custom",
                          template_dirs: Optional[List[str]] = None) -> bool:
    # 生成寄存器文件的主函数
```

## 扩展指南

### 添加新的总线协议生成器

1. 创建继承自`BaseBusGenerator`的新类
2. 实现必要的方法，尤其是`_prepare_context`
3. 使用装饰器注册协议

```python
from autoregfile.core.bus_generators.base_generator import BaseBusGenerator
from autoregfile.core.bus_generators.factory import register_bus_generator

@register_bus_generator("mynewbus")
class MyNewBusGenerator(BaseBusGenerator):
    def __init__(self, config, template_dirs=None):
        self.protocol_name = "mynewbus"
        super().__init__(config, template_dirs)
        
    def _prepare_context(self):
        context = super()._prepare_context()
        # 添加特定于新总线的上下文数据
        return context
```

4. 创建对应的模板文件: `templates/verilog/bus/mynewbus.v.j2`

### 添加新的配置文件解析器

1. 创建继承自`ParserBase`的新类
2. 实现`parse`和`validate`方法

```python
from autoregfile.parsers.parser_base import ParserBase

class MyNewParser(ParserBase):
    def __init__(self, config_file):
        super().__init__(config_file)
        
    def parse(self):
        # 实现解析逻辑
        return parsed_config
        
    def validate(self, config):
        # 实现验证逻辑
        return is_valid
```

3. 在`parsers/__init__.py`中注册解析器

```python
from .mynew_parser import MyNewParser

def get_parser(config_file):
    # 根据文件扩展名选择解析器
    if config_file.endswith(".mynew"):
        return MyNewParser(config_file)
    # ...
```

## 项目开发流程

### 代码风格

- 遵循PEP 8编码规范
- 使用类型注解增加代码可读性
- 添加详细的文档字符串
- 使用英文编写代码和注释

### 测试

- 单元测试: 测试单个组件的功能
- 集成测试: 测试多个组件的协同工作
- 测试命令: `python -m unittest discover autoregfile/tests`

### 贡献流程

1. Fork项目仓库
2. 创建功能分支: `git checkout -b feature/my-new-feature`
3. 提交更改: `git commit -am 'Add some feature'`
4. 推送到分支: `git push origin feature/my-new-feature`
5. 提交Pull Request

## 高级主题

### 模板开发

模板使用Jinja2模板引擎，支持:

- 条件: `{% if condition %}...{% endif %}`
- 循环: `{% for item in items %}...{% endfor %}`
- 过滤器: `{{ value|filter }}`
- 包含: `{% include 'template.j2' %}`

自定义过滤器示例:

```python
# 在模板管理器中添加
env.filters['my_filter'] = lambda x: some_transformation(x)

# 在模板中使用
{{ value|my_filter }}
```

### 插件系统

AutoRegFile支持通过动态加载外部目录来扩展功能:

```python
# 加载外部总线生成器
BusGeneratorFactory.create_generator(
    "custom",
    config,
    external_generator_dirs=["/path/to/external/generators"]
)
```

## 故障排除

### 常见开发问题

1. **模板未找到**
   - 检查模板路径是否正确
   - 确认模板目录已添加到模板管理器

2. **配置解析错误**
   - 验证配置文件格式是否正确
   - 检查解析器对应的文件扩展名

3. **总线生成器注册失败**
   - 确保装饰器正确应用
   - 检查协议名称是否唯一

### 调试技巧

- 使用`logger`输出调试信息
- 检查生成的上下文数据
- 启用详细日志: `get_logger("component", level=logging.DEBUG)`

## API参考

### 核心类

- `BaseBusGenerator`: 总线生成器基类
- `BusGeneratorFactory`: 总线生成器工厂
- `ParserBase`: 解析器基类
- `TemplateManager`: 模板管理器

### 实用工具

- `get_logger`: 获取日志记录器
- `safe_write_file`: 安全写入文件
- `ensure_dir_exists`: 确保目录存在

### 主要函数

- `generate_register_file`: 生成寄存器文件的主函数
- `get_template_manager`: 获取模板管理器实例 