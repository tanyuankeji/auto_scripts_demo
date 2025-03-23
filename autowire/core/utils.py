"""
工具函数模块
提供各种辅助函数
"""

import os
import re
import sys
import traceback
from typing import Dict, Optional, Any

class VerilogError(Exception):
    """Verilog错误异常基类"""
    pass

class ParseError(VerilogError):
    """解析错误异常类"""
    pass

class AnalysisError(VerilogError):
    """分析错误异常类"""
    pass

class ConfigError(VerilogError):
    """配置错误异常类"""
    pass

def handle_error(error: Exception, debug: bool = False) -> None:
    """
    处理异常并打印错误信息
    
    参数:
        error: 捕获的异常
        debug: 是否打印完整堆栈跟踪
    """
    if isinstance(error, VerilogError):
        print(f"\n错误: {str(error)}", file=sys.stderr)
    else:
        print(f"\n发生未知错误: {str(error)}", file=sys.stderr)
    
    if debug:
        print("\n堆栈跟踪:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

def read_file(file_path: str) -> str:
    """
    读取文件内容
    
    参数:
        file_path: 文件路径
        
    返回:
        文件内容
        
    异常:
        IOError: 文件读取失败
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # 尝试使用其他编码
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise IOError(f"无法读取文件 {file_path}: {str(e)}")
    except Exception as e:
        raise IOError(f"无法读取文件 {file_path}: {str(e)}")

def write_file(file_path: str, content: str) -> None:
    """
    写入文件内容
    
    参数:
        file_path: 文件路径
        content: 要写入的内容
        
    异常:
        IOError: 文件写入失败
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise IOError(f"无法写入文件 {file_path}: {str(e)}")

def ensure_dir(directory: str) -> None:
    """
    确保目录存在，不存在则创建
    
    参数:
        directory: 目录路径
        
    异常:
        IOError: 创建目录失败
    """
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            raise IOError(f"无法创建目录 {directory}: {str(e)}")

def remove_comments(content: str) -> str:
    """
    移除Verilog代码中的注释
    
    参数:
        content: 原始代码内容
        
    返回:
        移除注释后的代码内容
    """
    # 移除多行注释 /* ... */
    content = re.sub(r'/\*[\s\S]*?\*/', ' ', content)
    
    # 移除单行注释 // ...
    content = re.sub(r'//.*?$', ' ', content, flags=re.MULTILINE)
    
    return content

def format_width(width: str) -> str:
    """
    格式化信号位宽
    
    参数:
        width: 原始位宽表示
        
    返回:
        格式化后的位宽表示
    """
    # 如果width是数字，则转换为[数字-1:0]格式
    if width.isdigit():
        return f"[{int(width)-1}:0]"
    # 如果已经是[x:y]格式，则直接使用
    elif re.match(r'\[\s*\d+\s*:\s*\d+\s*\]', width):
        return width
    # 如果是其他格式，尝试提取数字并转换为[数字-1:0]格式
    else:
        match = re.search(r'(\d+)', width)
        if match:
            return f"[{int(match.group(1))-1}:0]"
        else:
            # 如果无法解析，使用原始值
            return width

def extract_parameters(content: str) -> Dict[str, str]:
    """
    提取Verilog代码中的参数定义
    
    参数:
        content: 代码内容
        
    返回:
        参数名到参数值的字典
    """
    # 匹配参数定义，如parameter WIDTH = 8
    param_pattern = re.compile(r'parameter\s+(\w+)\s*=\s*([^,;]+)')
    
    # 查找所有匹配项
    params = {}
    for name, value in param_pattern.findall(content):
        params[name] = value.strip()
    
    # 匹配localparam定义
    localparam_pattern = re.compile(r'localparam\s+(\w+)\s*=\s*([^,;]+)')
    for name, value in localparam_pattern.findall(content):
        params[name] = value.strip()
    
    return params

def is_common_constant(signal: str) -> bool:
    """
    检查信号名是否是常见常量名
    
    参数:
        signal: 信号名
        
    返回:
        如果是常见常量名则返回True，否则返回False
    """
    # 常见常量名模式
    constant_patterns = [
        r'^[A-Z][A-Z0-9_]*$',        # 全大写
        r'^[A-Z][A-Z0-9_]*_[a-z]+$', # 全大写加小写后缀
        r'^e_\w+$',                  # e_前缀
        r'^c_\w+$',                  # c_前缀
        r'^k_\w+$',                  # k_前缀
        r'^PARAM_\w+$',              # PARAM_前缀
        r'^CONST_\w+$',              # CONST_前缀
        r'^[0-9]+$',                 # 纯数字
    ]
    
    for pattern in constant_patterns:
        if re.match(pattern, signal):
            return True
    return False