#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模板管理器模块

此模块提供了模板管理器类，用于管理和渲染模板文件。
支持从多个模板目录查找模板，加载和渲染模板文件。
"""

import os
import re
import shutil
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import datetime
import json
import jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from ..utils import get_logger, ensure_dir_exists

# 模板管理器单例
_template_manager_instance = None


def get_template_manager(template_dirs: Optional[List[str]] = None) -> 'TemplateManager':
    """
    获取模板管理器实例
    
    如果实例不存在，则创建一个新的模板管理器实例
    
    Args:
        template_dirs: 模板目录列表
        
    Returns:
        TemplateManager: 模板管理器实例
    """
    global _template_manager_instance
    if _template_manager_instance is None:
        _template_manager_instance = TemplateManager(template_dirs)
    elif template_dirs:
        # 如果提供了新的模板目录，更新现有实例
        _template_manager_instance.add_template_dirs(template_dirs)
    
    return _template_manager_instance


class TemplateManager:
    """
    模板管理器类
    
    用于管理和渲染模板文件。支持从多个模板目录查找模板，
    加载和渲染模板文件，以及创建模板目录。
    """
    
    def __init__(self, template_dirs: Optional[List[str]] = None):
        """
        初始化模板管理器
        
        Args:
            template_dirs: 用户定义的模板目录列表
        """
        self.logger = get_logger("TemplateManager")
        
        # 内置模板目录
        self.builtin_template_dir = self._get_builtin_template_dir()
        
        # 用户模板目录
        self.user_template_dirs = []
        if template_dirs:
            self.add_template_dirs(template_dirs)
        
        # 创建Jinja2环境
        self.jinja_env = self._create_jinja_env()
        
        self.logger.debug(f"模板管理器初始化完成，内置模板目录: {self.builtin_template_dir}")
        self.logger.debug(f"用户模板目录: {self.user_template_dirs}")
    
    def _get_builtin_template_dir(self) -> str:
        """
        获取内置模板目录的路径
        
        Returns:
            str: 内置模板目录的路径
        """
        # 内置模板目录相对于当前模块的路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        package_dir = os.path.dirname(current_dir)
        builtin_template_dir = os.path.join(package_dir, "templates")
        
        if not os.path.isdir(builtin_template_dir):
            self.logger.warning(f"内置模板目录不存在: {builtin_template_dir}")
        
        return builtin_template_dir
    
    def add_template_dirs(self, template_dirs: List[str]) -> None:
        """
        添加用户模板目录
        
        Args:
            template_dirs: 要添加的模板目录列表
        """
        for template_dir in template_dirs:
            if os.path.isdir(template_dir):
                if template_dir not in self.user_template_dirs:
                    self.user_template_dirs.append(template_dir)
                    self.logger.debug(f"添加用户模板目录: {template_dir}")
            else:
                self.logger.warning(f"模板目录不存在: {template_dir}")
        
        # 更新Jinja2环境
        self.jinja_env = self._create_jinja_env()
    
    def _create_jinja_env(self) -> Environment:
        """
        创建Jinja2环境
        
        Returns:
            Environment: 配置好的Jinja2环境
        """
        # 构建搜索路径，优先使用用户模板目录
        search_paths = self.user_template_dirs.copy()
        
        # 添加内置模板目录
        if os.path.isdir(self.builtin_template_dir):
            search_paths.append(self.builtin_template_dir)
        
        # 创建Jinja2环境
        env = Environment(
            loader=FileSystemLoader(search_paths),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 添加自定义过滤器
        env.filters['hex'] = lambda x: hex(x) if isinstance(x, int) else x
        env.filters['upper'] = lambda x: x.upper() if isinstance(x, str) else x
        env.filters['lower'] = lambda x: x.lower() if isinstance(x, str) else x
        env.filters['width_to_hex_chars'] = lambda width: max(2, (width + 3) // 4)
        
        return env
    
    def find_template(self, template_path: str) -> Optional[str]:
        """
        查找模板文件
        
        按照以下顺序查找模板:
        1. 如果是绝对路径且存在，直接返回
        2. 在用户模板目录中查找
        3. 在内置模板目录中查找
        
        Args:
            template_path: 模板路径
            
        Returns:
            Optional[str]: 模板的绝对路径，如果未找到则返回None
        """
        # 1. 检查是否是绝对路径
        if os.path.isabs(template_path) and os.path.isfile(template_path):
            return template_path
        
        # 2. 在用户模板目录中查找
        for template_dir in self.user_template_dirs:
            abs_path = os.path.join(template_dir, template_path)
            if os.path.isfile(abs_path):
                return abs_path
        
        # 3. 在内置模板目录中查找
        builtin_path = os.path.join(self.builtin_template_dir, template_path)
        if os.path.isfile(builtin_path):
            return builtin_path
        
        # 未找到模板
        self.logger.warning(f"未找到模板: {template_path}")
        return None
    
    def render_template(self, template_path: str, context: Dict[str, Any]) -> Optional[str]:
        """
        渲染模板
        
        Args:
            template_path: 模板路径
            context: 渲染上下文
            
        Returns:
            Optional[str]: 渲染后的内容，如果渲染失败则返回None
        """
        try:
            # 尝试直接在Jinja环境中查找模板
            template = None
            
            # 检查是否是绝对路径
            if os.path.isabs(template_path):
                # 尝试直接加载文件
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                template = self.jinja_env.from_string(template_content)
                self.logger.debug(f"从绝对路径加载模板: {template_path}")
            else:
                # 尝试通过Jinja环境加载
                try:
                    template = self.jinja_env.get_template(template_path)
                    self.logger.debug(f"通过Jinja环境加载模板: {template_path}")
                except jinja2.exceptions.TemplateNotFound:
                    # 如果Jinja环境找不到模板，尝试手动查找
                    full_path = self.find_template(template_path)
                    if full_path:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            template_content = f.read()
                        template = self.jinja_env.from_string(template_content)
                        self.logger.debug(f"手动查找并加载模板: {full_path}")
            
            # 若模板仍未找到，报错并返回
            if template is None:
                self.logger.error(f"找不到模板: {template_path}")
                return None
            
            # 添加标准上下文变量
            full_context = context.copy()
            full_context.update({
                'current_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'generator': 'autoregfile'
            })
            
            # 渲染模板
            rendered = template.render(**full_context)
            return rendered
            
        except Exception as e:
            self.logger.error(f"渲染模板 {template_path} 失败: {str(e)}", exc_info=True)
            return None
    
    def copy_template_dir(self, destination: str) -> bool:
        """
        复制内置模板目录到指定位置
        
        Args:
            destination: 目标目录
            
        Returns:
            bool: 是否复制成功
        """
        try:
            if not os.path.isdir(self.builtin_template_dir):
                self.logger.error(f"内置模板目录不存在: {self.builtin_template_dir}")
                return False
            
            # 确保目标目录存在
            if not ensure_dir_exists(destination):
                self.logger.error(f"无法创建目标目录: {destination}")
                return False
            
            # 复制模板文件
            for root, dirs, files in os.walk(self.builtin_template_dir):
                # 计算相对路径
                rel_path = os.path.relpath(root, self.builtin_template_dir)
                target_dir = os.path.join(destination, rel_path)
                
                # 创建目标目录
                if rel_path != '.' and not ensure_dir_exists(target_dir):
                    self.logger.error(f"无法创建目录: {target_dir}")
                    return False
                
                # 复制文件
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_dir, file)
                    shutil.copy2(src_file, dst_file)
            
            self.logger.info(f"内置模板目录已复制到: {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"复制模板目录时出错: {str(e)}", exc_info=True)
            return False
    
    def create_template_dir(self, template_dir: str, base_template: Optional[str] = None) -> bool:
        """
        创建自定义模板目录结构
        
        Args:
            template_dir: 要创建的模板目录
            base_template: 基础模板名称，如果指定，将复制该模板作为起点
            
        Returns:
            bool: 是否创建成功
        """
        try:
            # 创建目录结构
            dirs_to_create = [
                template_dir,
                os.path.join(template_dir, "verilog"),
                os.path.join(template_dir, "verilog", "bus"),
                os.path.join(template_dir, "verilog", "common"),
                os.path.join(template_dir, "verilog", "field"),
                os.path.join(template_dir, "systemverilog")
            ]
            
            for directory in dirs_to_create:
                if not ensure_dir_exists(directory):
                    self.logger.error(f"无法创建目录: {directory}")
                    return False
            
            # 如果指定了基础模板，复制它
            if base_template:
                base_template_path = self.find_template(f"verilog/bus/{base_template}.v.j2")
                if base_template_path:
                    target_path = os.path.join(template_dir, "verilog", "bus", "custom.v.j2")
                    shutil.copy2(base_template_path, target_path)
                    self.logger.info(f"已复制基础模板 {base_template} 到 {target_path}")
            
            # 创建README文件
            readme_path = os.path.join(template_dir, "README.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("# 自定义模板目录\n\n")
                f.write("此目录包含自定义模板文件，用于生成寄存器文件。\n\n")
                f.write("## 目录结构\n\n")
                f.write("- `verilog/bus/`: 总线协议模板\n")
                f.write("- `verilog/common/`: 通用模板片段\n")
                f.write("- `verilog/field/`: 字段相关模板\n")
                f.write("- `systemverilog/`: SystemVerilog模板\n")
            
            self.logger.info(f"已创建自定义模板目录: {template_dir}")
            
            # 将新目录添加到搜索路径
            self.add_template_dirs([template_dir])
            
            return True
            
        except Exception as e:
            self.logger.error(f"创建模板目录时出错: {str(e)}", exc_info=True)
            return False
    
    def list_templates(self, category: Optional[str] = None) -> List[str]:
        """
        列出可用的模板
        
        Args:
            category: 模板类别，如'bus'、'field'等，如果为None则列出所有模板
            
        Returns:
            List[str]: 模板列表
        """
        templates = []
        
        # 构建搜索路径
        search_paths = self.user_template_dirs.copy()
        if os.path.isdir(self.builtin_template_dir):
            search_paths.append(self.builtin_template_dir)
        
        # 过滤路径的模式
        if category:
            pattern = f"**/{'*/' if category else ''}{category}/*.j2"
        else:
            pattern = "**/*.j2"
        
        # 在所有目录中搜索
        for path in search_paths:
            if not os.path.isdir(path):
                continue
                
            for template_file in Path(path).glob(pattern):
                rel_path = os.path.relpath(template_file, path)
                if rel_path not in templates:
                    templates.append(rel_path)
        
        return sorted(templates)
    
    def render_string(self, template_content: str, context: Dict[str, Any]) -> Optional[str]:
        """
        渲染字符串模板
        
        Args:
            template_content: 模板内容字符串
            context: 渲染上下文
            
        Returns:
            Optional[str]: 渲染后的内容，如果渲染失败则返回None
        """
        try:
            # 创建模板
            template = self.jinja_env.from_string(template_content)
            
            # 添加标准上下文变量
            full_context = context.copy()
            full_context.update({
                'current_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'generation_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tool_version': '1.0.0',
                'generator': 'autoregfile'
            })
            
            # 渲染模板
            rendered = template.render(**full_context)
            return rendered
            
        except Exception as e:
            self.logger.error(f"渲染字符串模板失败: {str(e)}", exc_info=True)
            return None 