"""
配置管理模块
包含配置加载和管理功能
"""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..core.utils import ConfigError

class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        self.exclude_patterns: List[str] = []
        self.default_width: Optional[str] = None
        self.output_format: str = "separate"
        self.output_dir: Optional[str] = None
        self.debug: bool = False
        self.verbose: bool = False
        self.append_to_original: bool = False
        
    def load_from_file(self, file_path: str) -> None:
        """
        从文件加载配置
        
        参数:
            file_path: 配置文件路径
            
        异常:
            ConfigError: 配置文件加载失败
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            if not isinstance(config_data, dict):
                raise ConfigError("配置文件格式错误：必须是JSON对象")
                
            # 加载排除模式
            if 'exclude_patterns' in config_data:
                patterns = config_data['exclude_patterns']
                if not isinstance(patterns, list):
                    raise ConfigError("exclude_patterns必须是列表")
                self.exclude_patterns.extend(patterns)
                
            # 加载默认位宽
            if 'default_width' in config_data:
                self.default_width = str(config_data['default_width'])
                
            # 加载输出格式
            if 'output_format' in config_data:
                self.output_format = str(config_data['output_format'])
                
            # 加载输出目录
            if 'output_dir' in config_data:
                self.output_dir = str(config_data['output_dir'])
                
        except json.JSONDecodeError as e:
            raise ConfigError(f"配置文件JSON格式错误：{str(e)}")
        except Exception as e:
            raise ConfigError(f"加载配置文件失败：{str(e)}")
            
    def load_from_args(self, args: Any) -> None:
        """
        从命令行参数加载配置
        
        参数:
            args: 命令行参数对象
        """
        # 加载排除模式
        if hasattr(args, 'exclude') and args.exclude:
            self.exclude_patterns.extend(args.exclude)
            
        # 加载默认位宽
        if hasattr(args, 'default_width') and args.default_width:
            self.default_width = args.default_width
            
        # 加载输出目录
        if hasattr(args, 'output_dir') and args.output_dir:
            self.output_dir = args.output_dir
            
        # 加载调试和详细输出选项
        if hasattr(args, 'debug'):
            self.debug = args.debug
        if hasattr(args, 'verbose'):
            self.verbose = args.verbose
            
        # 加载追加模式选项
        if hasattr(args, 'append'):
            self.append_to_original = args.append
            
    def get_default_config_path(self) -> str:
        """
        获取默认配置文件路径
        
        返回:
            默认配置文件路径
        """
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'auto_wire_config.json')
        
    def save_to_file(self, file_path: str) -> None:
        """
        保存配置到文件
        
        参数:
            file_path: 配置文件路径
            
        异常:
            ConfigError: 配置文件保存失败
        """
        config_data = {
            'exclude_patterns': self.exclude_patterns,
            'default_width': self.default_width,
            'output_format': self.output_format,
            'output_dir': self.output_dir,
            'version': '2.0.0'
        }
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            raise ConfigError(f"保存配置文件失败：{str(e)}")
            
    def validate(self) -> None:
        """
        验证配置有效性
        
        异常:
            ConfigError: 配置无效
        """
        # 验证输出格式
        if self.output_format not in ['separate', 'append']:
            raise ConfigError("输出格式必须是 'separate' 或 'append'")
            
        # 验证默认位宽格式
        if self.default_width:
            if not self.default_width.startswith('['):
                try:
                    width = int(self.default_width)
                    if width <= 0:
                        raise ValueError
                except ValueError:
                    raise ConfigError("默认位宽必须是正整数或[x:y]格式")
                    
        # 验证排除模式
        for pattern in self.exclude_patterns:
            try:
                import re
                re.compile(pattern)
            except re.error:
                raise ConfigError(f"无效的排除模式：{pattern}")