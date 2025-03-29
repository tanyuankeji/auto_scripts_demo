# AutoRegFile API参考

## 概述

本文档提供了AutoRegFile项目的API详细说明，包括核心类、方法和函数的接口定义。

## 主接口

### 寄存器文件生成

```python
from autoregfile.register_factory import generate_register_file

generate_register_file(
    config_file: Optional[str] = None,
    config_dict: Optional[Dict[str, Any]] = None,
    output_file: str = "regfile.v",
    bus_protocol: str = "custom",
    template_dirs: Optional[List[str]] = None,
    verbose: bool = False
) -> bool:
    """
    生成寄存器文件
    
    参数:
        config_file: 配置文件路径
        config_dict: 配置字典，当config_file为None时使用
        output_file: 输出文件路径
        bus_protocol: 总线协议名称
        template_dirs: 自定义模板目录列表
        verbose: 是否显示详细日志
        
    返回:
        bool: 是否成功生成
    """
```

### 支持的总线协议

```python
from autoregfile.core.bus_generators.factory import BusGeneratorFactory

# 获取支持的总线协议列表
protocols = BusGeneratorFactory.list_supported_protocols()
```

## 总线生成器API

### 基类: `BaseBusGenerator`

```python
from autoregfile.core.bus_generators.base_generator import BaseBusGenerator

class BaseBusGenerator:
    """总线生成器基类"""
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化总线生成器
        
        参数:
            config: 寄存器配置字典
            template_dirs: 模板目录列表
        """
        
    def generate(self, output_file: str) -> bool:
        """
        生成总线接口寄存器文件
        
        参数:
            output_file: 输出文件路径
            
        返回:
            bool: 是否成功生成
        """
```

### 工厂: `BusGeneratorFactory`

```python
from autoregfile.core.bus_generators.factory import BusGeneratorFactory

class BusGeneratorFactory:
    """总线生成器工厂类"""
    
    @classmethod
    def register_protocol(cls, protocol_name: str) -> Callable:
        """
        注册总线协议生成器的装饰器
        
        参数:
            protocol_name: 总线协议名称
            
        返回:
            装饰器函数
        """
        
    @classmethod
    def create_generator(cls, bus_protocol: str, config: Dict[str, Any], 
                        template_dirs: Optional[List[str]] = None,
                        external_generator_dirs: Optional[List[str]] = None) -> Optional[BaseBusGenerator]:
        """
        创建总线生成器实例
        
        参数:
            bus_protocol: 总线协议名称
            config: 配置字典
            template_dirs: 模板目录列表
            external_generator_dirs: 外部总线生成器目录列表
            
        返回:
            总线生成器实例，如果未找到则返回None
        """
        
    @classmethod
    def list_supported_protocols(cls) -> List[str]:
        """
        列出所有支持的总线协议
        
        返回:
            支持的总线协议列表
        """
```

### 装饰器: `register_bus_generator`

```python
from autoregfile.core.bus_generators.factory import register_bus_generator

@register_bus_generator("protocol_name")
class MyBusGenerator(BaseBusGenerator):
    """自定义总线生成器"""
    pass
```

### 自定义总线生成器: `CustomBusGenerator`

```python
from autoregfile.core.bus_generators.custom_generator import CustomBusGenerator

class CustomBusGenerator(BaseBusGenerator):
    """自定义总线生成器"""
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化自定义总线生成器
        
        参数:
            config: 寄存器配置字典
            template_dirs: 模板目录列表
        """
```

## 解析器API

### 基类: `ParserBase`

```python
from autoregfile.parsers.parser_base import ParserBase

class ParserBase:
    """解析器基类"""
    
    def __init__(self, config_file: str):
        """
        初始化解析器
        
        参数:
            config_file: 配置文件路径
        """
        
    def parse(self) -> Dict[str, Any]:
        """
        解析配置文件
        
        返回:
            配置字典
        """
        
    def validate(self, config: Dict[str, Any]) -> bool:
        """
        验证配置是否有效
        
        参数:
            config: 配置字典
            
        返回:
            bool: 是否有效
        """
```

### Excel解析器: `ExcelParser`

```python
from autoregfile.parsers.excel_parser import ExcelParser

class ExcelParser(ParserBase):
    """Excel配置文件解析器"""
    
    def __init__(self, config_file: str):
        """
        初始化Excel解析器
        
        参数:
            config_file: Excel配置文件路径
        """
```

### JSON解析器: `JsonParser`

```python
from autoregfile.parsers.json_parser import JsonParser

class JsonParser(ParserBase):
    """JSON配置文件解析器"""
    
    def __init__(self, config_file: str):
        """
        初始化JSON解析器
        
        参数:
            config_file: JSON配置文件路径
        """
```

### 解析器工厂

```python
from autoregfile.parsers import get_parser

# 根据文件扩展名获取解析器
parser = get_parser("config.xlsx")  # 返回ExcelParser实例
config = parser.parse()
```

## 模板管理API

### 模板管理器: `TemplateManager`

```python
from autoregfile.core.template_manager import TemplateManager, get_template_manager

class TemplateManager:
    """模板管理器类"""
    
    def __init__(self, template_dirs: Optional[List[str]] = None):
        """
        初始化模板管理器
        
        参数:
            template_dirs: 用户定义的模板目录列表
        """
        
    def add_template_dirs(self, template_dirs: List[str]) -> None:
        """
        添加用户模板目录
        
        参数:
            template_dirs: 要添加的模板目录列表
        """
        
    def find_template(self, template_path: str) -> Optional[str]:
        """
        查找模板文件
        
        参数:
            template_path: 模板路径
            
        返回:
            Optional[str]: 模板的绝对路径，如果未找到则返回None
        """
        
    def render_template(self, template_path: str, context: Dict[str, Any]) -> Optional[str]:
        """
        渲染模板
        
        参数:
            template_path: 模板路径
            context: 渲染上下文
            
        返回:
            Optional[str]: 渲染后的内容，如果渲染失败则返回None
        """
        
    def copy_template_dir(self, destination: str) -> bool:
        """
        复制内置模板目录到指定位置
        
        参数:
            destination: 目标目录
            
        返回:
            bool: 是否复制成功
        """
        
    def create_template_dir(self, template_dir: str, base_template: Optional[str] = None) -> bool:
        """
        创建自定义模板目录结构
        
        参数:
            template_dir: 要创建的模板目录
            base_template: 基础模板名称，如果指定，将复制该模板作为起点
            
        返回:
            bool: 是否创建成功
        """
        
    def list_templates(self, category: Optional[str] = None) -> List[str]:
        """
        列出可用的模板
        
        参数:
            category: 模板类别，如'bus'、'field'等，如果为None则列出所有模板
            
        返回:
            List[str]: 模板列表
        """

# 获取单例实例
template_manager = get_template_manager(template_dirs)
```

## 工具函数API

### 日志工具

```python
from autoregfile.utils import get_logger

# 获取日志记录器
logger = get_logger("component_name", level=logging.INFO)
logger.info("日志消息")
```

### 文件工具

```python
from autoregfile.utils import safe_write_file, ensure_dir_exists

# 安全写入文件
success = safe_write_file("/path/to/file.txt", "文件内容")

# 确保目录存在
exists = ensure_dir_exists("/path/to/directory")
```

### 模板工具

```python
from autoregfile.utils.template_tools import create_template_directory, copy_template_dir, list_available_templates

# 创建模板目录
create_template_directory("/path/to/templates", protocol_name="apb")

# 复制内置模板
copy_template_dir("/path/to/destination")

# 列出可用模板
templates = list_available_templates(category="bus")
```

## 配置数据结构

### 全局配置

```python
config = {
    "module_name": "my_regfile",     # 模块名称
    "data_width": 32,                # 数据位宽
    "addr_width": 8,                 # 地址位宽
    "bus_protocol": "custom",        # 总线协议
    "registers": [...]               # 寄存器列表
}
```

### 寄存器配置

```python
register = {
    "name": "control",              # 寄存器名称
    "address": "0x00",              # 寄存器地址
    "description": "控制寄存器",     # 寄存器描述
    "type": "RW",                   # 寄存器类型
    "fields": [...]                 # 字段列表
}
```

### 字段配置

```python
field = {
    "name": "enable",              # 字段名称
    "bit_range": "0:0",            # 位范围
    "access": "RW",                # 访问类型
    "reset_val": 0,                # 复位值
    "description": "使能位"         # 字段描述
}
```

## 返回值和异常

大多数API函数和方法返回布尔值表示操作成功或失败，或者返回相应的对象或None。错误情况通常通过记录日志而不是抛出异常来处理，以提高健壮性。

## 版本信息

```python
from autoregfile import __version__

print(f"AutoRegFile 版本: {__version__}")
``` 