"""
代码生成器模块
负责生成wire声明代码并处理输出
"""

import os
import re
from typing import List, Dict, Optional, Any
from pathlib import Path

from .analyzer import SignalAnalyzer
from .utils import write_file, ensure_dir, ParseError

class CodeGenerator:
    """代码生成器类"""
    
    def __init__(self):
        """初始化生成器"""
        self.analyzer = None
        self.file_path = ""
        self.output_dir = None
        self.append_mode = False
        self.definitions = []
        
    def setup(self, analyzer: SignalAnalyzer, file_path: str, 
              output_dir: Optional[str] = None, append: bool = False) -> None:
        """
        设置生成器
        
        参数:
            analyzer: 信号分析器实例
            file_path: 源文件路径
            output_dir: 输出目录
            append: 是否追加到原始文件
        """
        self.analyzer = analyzer
        self.file_path = file_path
        self.output_dir = output_dir
        self.append_mode = append
        
    def generate(self) -> List[str]:
        """
        生成代码
        
        返回:
            生成的代码行列表
            
        异常:
            ParseError: 代码生成失败
        """
        if not self.analyzer:
            raise ParseError("生成器未设置分析器")
            
        # 获取信号定义
        definitions_dict = self.analyzer.get_signal_definitions()
        
        # 组织输出内容
        output_lines = ["// 自动生成的wire声明\n"]
        
        # 添加信号定义
        for signal, definition in definitions_dict.items():
            output_lines.append(f"{definition}\n")
            
        self.definitions = output_lines
        return output_lines
        
    def write_to_file(self) -> str:
        """
        将生成的代码写入文件
        
        返回:
            输出文件路径
            
        异常:
            ParseError: 文件写入失败
        """
        if not self.definitions:
            raise ParseError("未生成代码，请先调用generate()")
            
        if self.append_mode:
            return self._append_to_original()
        else:
            return self._write_to_new_file()
            
    def _write_to_new_file(self) -> str:
        """
        写入新文件
        
        返回:
            输出文件路径
        """
        # 确定输出文件名
        base_name = os.path.basename(self.file_path)
        output_file_name = base_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')
        
        if self.output_dir:
            output_file = os.path.join(self.output_dir, output_file_name)
        else:
            output_dir = os.path.dirname(self.file_path)
            output_file = os.path.join(output_dir, output_file_name)
        
        # 确保输出目录存在
        ensure_dir(output_file)
        
        # 写入文件
        content = ''.join(self.definitions)
        write_file(output_file, content)
        
        return output_file
        
    def _append_to_original(self) -> str:
        """
        追加到原始文件
        
        返回:
            输出文件路径
        """
        # 读取原始文件内容
        with open(self.file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
            
        # 查找模块头部结束位置
        module_pattern = re.compile(r'module\s+\w+\s*\([^;]*;', re.DOTALL)
        match = module_pattern.search(original_content)
        
        if match:
            insert_pos = match.end()
            
            # 组合新内容
            new_content = (
                original_content[:insert_pos] + 
                '\n\n' + 
                ''.join(self.definitions) + 
                '\n' + 
                original_content[insert_pos:]
            )
            
            # 写入文件
            write_file(self.file_path, new_content)
            
            return self.file_path
        else:
            raise ParseError("无法找到模块定义位置，无法追加到原始文件")
            
    def get_summary(self) -> Dict[str, Any]:
        """
        获取生成摘要
        
        返回:
            生成摘要字典
        """
        if not self.analyzer:
            return {"status": "未初始化"}
            
        report = self.analyzer.get_report()
        
        return {
            "status": "成功",
            "total_signals": report["total_signals"],
            "signals_with_width": report["signals_with_width"],
            "signals_with_default_width": report["signals_with_default_width"],
            "signals_without_width": report["signals_without_width"],
            "output_mode": "追加到原始文件" if self.append_mode else "独立文件",
            "output_file": self.file_path if self.append_mode else self._get_expected_output_path()
        }
        
    def _get_expected_output_path(self) -> str:
        """
        获取预期的输出文件路径
        
        返回:
            输出文件路径
        """
        base_name = os.path.basename(self.file_path)
        output_file_name = base_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')
        
        if self.output_dir:
            return os.path.join(self.output_dir, output_file_name)
        else:
            output_dir = os.path.dirname(self.file_path)
            return os.path.join(output_dir, output_file_name)