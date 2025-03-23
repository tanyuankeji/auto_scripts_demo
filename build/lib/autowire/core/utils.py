"""
工具模块
包含错误处理和通用工具函数
"""

import re
from typing import List, Dict, Optional, Set
from pathlib import Path

class VerilogError(Exception):
    """Verilog相关错误基类"""
    pass

class ParseError(VerilogError):
    """解析错误"""
    pass

class AnalysisError(VerilogError):
    """分析错误"""
    pass

class ConfigError(VerilogError):
    """配置错误"""
    pass

def handle_error(error: Exception, debug: bool = False) -> None:
    """
    统一的错误处理函数
    
    参数:
        error: 异常对象
        debug: 是否显示调试信息
    """
    if debug:
        import traceback
        traceback.print_exc()
    else:
        print(f"\n错误：{str(error)}")

def read_file(file_path: str) -> str:
    """
    读取文件内容，支持多种编码
    
    参数:
        file_path: 文件路径
        
    返回:
        文件内容字符串
        
    异常:
        ParseError: 文件读取失败
    """
    encodings = ['utf-8', 'latin-1', 'gbk']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise ParseError(f"无法读取文件 {file_path}：{str(e)}")
    raise ParseError(f"无法使用支持的编码读取文件 {file_path}")

def write_file(file_path: str, content: str) -> None:
    """
    写入文件内容
    
    参数:
        file_path: 文件路径
        content: 要写入的内容
        
    异常:
        ParseError: 文件写入失败
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise ParseError(f"无法写入文件 {file_path}：{str(e)}")

def ensure_dir(file_path: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    参数:
        file_path: 文件路径
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

def remove_comments(content: str) -> str:
    """
    移除Verilog代码中的注释
    
    参数:
        content: 文件内容字符串
        
    返回:
        移除注释后的内容
    """
    # 移除单行注释
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    # 移除多行注释
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return content

def extract_parameters(content: str) -> Dict[str, str]:
    """
    提取Verilog代码中的参数定义
    
    参数:
        content: 文件内容字符串
        
    返回:
        参数名和值的字典
    """
    params = {}
    pattern = re.compile(r'\b(?:parameter|localparam)\s+(\w+)\s*=\s*([^,;]+)')
    for name, value in pattern.findall(content):
        params[name] = value.strip()
    return params

def is_valid_identifier(name: str) -> bool:
    """
    检查是否为有效的Verilog标识符
    
    参数:
        name: 标识符名称
        
    返回:
        是否为有效标识符
    """
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))

def format_width(width: str) -> str:
    """
    格式化位宽字符串
    
    参数:
        width: 位宽字符串
        
    返回:
        格式化后的位宽字符串
    """
    if not width:
        return ""
    if not width.startswith('['):
        width = f"[{width}]"
    return width.strip()

class WidthInferrer:
    """位宽推断类"""
    def __init__(self):
        self.parameter_values = {}
        self.width_patterns = [
            r'\[(\d+):(\d+)\]',  # [7:0]
            r'\[(\w+)\s*-\s*1\s*:\s*0\]',  # [WIDTH-1:0]
            r'\[(\d+)\]'  # [0]
        ]
        
    def infer_width(self, signal: str, context: str) -> Optional[str]:
        """推断信号位宽"""
        pass

class CodeFormatter:
    """代码格式化类"""
    def __init__(self):
        self.indent_size = 4
        self.max_line_length = 80
        
    def format_wire_definition(self, signal: str, width: Optional[str]) -> str:
        """格式化wire定义"""
        pass
        
    def format_file(self, content: str) -> str:
        """格式化整个文件"""
        pass