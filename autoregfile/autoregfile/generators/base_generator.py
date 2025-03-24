#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码生成器基类

定义所有代码生成器的通用接口。
"""

from typing import Dict, Any, List, Optional
import os
import jinja2
from datetime import datetime


class BaseGenerator:
    """代码生成器基类"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化生成器
        
        参数:
            templates_dir: 模板目录，如果为None则使用默认模板目录
        """
        if templates_dir is None:
            # 获取默认模板目录
            import autoregfile
            pkg_dir = os.path.dirname(os.path.abspath(autoregfile.__file__))
            templates_dir = os.path.join(pkg_dir, 'templates')
        
        self.templates_dir = templates_dir
        self.env = self._create_jinja_env()
    
    def _create_jinja_env(self) -> jinja2.Environment:
        """创建Jinja2环境"""
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 添加通用过滤器和全局函数
        env.globals['int'] = int
        env.globals['now'] = datetime.now
        
        env.filters['to_hex'] = lambda x: hex(int(x))
        env.filters['startswith'] = lambda x, y: str(x).startswith(y)
        
        return env
    
    def generate(self, config: Dict[str, Any]) -> str:
        """
        生成代码
        
        参数:
            config: 配置字典
            
        返回:
            生成的代码字符串
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def save(self, content: str, output_path: str) -> None:
        """
        保存生成的内容到文件
        
        参数:
            content: 内容字符串
            output_path: 输出文件路径
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def prepare_context(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备模板上下文
        
        参数:
            config: 配置字典
            
        返回:
            准备好的上下文字典
        """
        context = config.copy()
        
        # 添加时间戳
        context['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 添加版本信息
        try:
            from autoregfile.__version__ import __version__
            context['generator_version'] = __version__
        except ImportError:
            context['generator_version'] = "dev"
        
        return context 