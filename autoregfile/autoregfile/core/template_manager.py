#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板管理器模块

管理和加载模板，包括用户自定义模板
"""

import os
import shutil
import logging
from typing import Dict, Optional, List, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 自定义过滤器
def startswith(value, prefix):
    """检查字符串是否以指定前缀开始"""
    if not value:
        return False
    return str(value).startswith(prefix)


def endswith(value, suffix):
    """检查字符串是否以指定后缀结束"""
    if not value:
        return False
    return str(value).endswith(suffix)


class TemplateManager:
    """
    模板管理器类
    
    负责管理系统和用户自定义模板
    """
    
    def __init__(self, template_dirs: Optional[List[str]] = None):
        """
        初始化模板管理器
        
        参数:
            template_dirs: 自定义模板目录路径列表
        """
        # 获取系统模板目录
        package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.system_template_dir = os.path.join(package_dir, "templates")
        
        # 用户模板目录
        self.user_template_dirs = []
        if template_dirs:
            self.user_template_dirs.extend(template_dirs)
        
        # 用户主目录下的默认模板目录
        user_home = os.path.expanduser("~")
        default_user_template_dir = os.path.join(user_home, ".autoregfile", "templates")
        if os.path.exists(default_user_template_dir):
            self.user_template_dirs.append(default_user_template_dir)
        
        # 当前工作目录下的模板目录
        cwd_template_dir = os.path.join(os.getcwd(), "autoregfile_templates")
        if os.path.exists(cwd_template_dir):
            self.user_template_dirs.append(cwd_template_dir)
        
        # 创建Jinja2环境，包含系统和用户模板目录
        search_dirs = [self.system_template_dir] + self.user_template_dirs
        self.env = Environment(
            loader=FileSystemLoader(search_dirs, encoding='utf-8'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 添加自定义过滤器
        self.env.filters['startswith'] = startswith
        self.env.filters['endswith'] = endswith
        
        logger.info(f"系统模板目录: {self.system_template_dir}")
        logger.info(f"用户模板目录: {self.user_template_dirs}")
    
    def list_available_templates(self, category: str = None) -> Dict[str, List[str]]:
        """
        列出可用的模板文件
        
        参数:
            category: 模板类别，如 'bus', 'register' 等，如果为None则列出所有类别
            
        返回:
            模板列表，按类别分组
        """
        templates = {}
        
        # 搜索系统模板
        sys_templates = self._scan_templates(self.system_template_dir, category, "系统")
        templates.update(sys_templates)
        
        # 搜索用户模板
        for user_dir in self.user_template_dirs:
            user_templates = self._scan_templates(user_dir, category, "用户")
            
            # 合并用户模板到结果中
            for cat, tmpl_list in user_templates.items():
                if cat in templates:
                    templates[cat].extend(tmpl_list)
                else:
                    templates[cat] = tmpl_list
        
        return templates
    
    def _scan_templates(self, base_dir: str, category: Optional[str], source: str) -> Dict[str, List[str]]:
        """
        扫描指定目录中的模板文件
        
        参数:
            base_dir: 基础目录
            category: 模板类别，如 'bus', 'register' 等，如果为None则扫描所有类别
            source: 模板来源标识，如 '系统' 或 '用户'
            
        返回:
            模板列表，按类别分组
        """
        results = {}
        
        if not os.path.exists(base_dir):
            return results
        
        # 确定要扫描的目录
        scan_dir = base_dir
        if category:
            scan_dir = os.path.join(base_dir, category)
            if not os.path.exists(scan_dir):
                return results
        
        # 遍历目录
        for root, dirs, files in os.walk(scan_dir):
            rel_path = os.path.relpath(root, base_dir)
            if rel_path == '.':
                continue
                
            cat = rel_path.replace(os.path.sep, '/')
            templates = [f for f in files if f.endswith(('.j2', '.jinja', '.jinja2'))]
            
            if templates:
                if cat not in results:
                    results[cat] = []
                
                # 添加模板信息
                for tmpl in templates:
                    tmpl_path = os.path.join(rel_path, tmpl)
                    # 添加模板来源信息
                    results[cat].append({
                        "name": os.path.splitext(tmpl)[0],
                        "path": tmpl_path,
                        "source": source
                    })
        
        return results
    
    def get_template(self, template_path: str):
        """
        获取模板对象
        
        参数:
            template_path: 模板相对路径
            
        返回:
            jinja2模板对象
            
        异常:
            jinja2.exceptions.TemplateNotFound: 如果模板未找到
        """
        return self.env.get_template(template_path)
    
    def render_template(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        参数:
            template_path: 模板相对路径
            context: 模板上下文数据
            
        返回:
            渲染后的内容
            
        异常:
            jinja2.exceptions.TemplateNotFound: 如果模板未找到
        """
        template = self.get_template(template_path)
        return template.render(**context)
    
    def create_user_template_dir(self, user_dir: Optional[str] = None) -> str:
        """
        创建用户模板目录
        
        参数:
            user_dir: 自定义用户模板目录，如果为None则创建默认目录
            
        返回:
            创建的模板目录路径
        """
        if user_dir is None:
            user_home = os.path.expanduser("~")
            user_dir = os.path.join(user_home, ".autoregfile", "templates")
        
        # 创建目录
        os.makedirs(user_dir, exist_ok=True)
        
        # 创建子目录结构
        for subdir in ['verilog/bus', 'verilog/register']:
            os.makedirs(os.path.join(user_dir, subdir), exist_ok=True)
        
        logger.info(f"用户模板目录已创建: {user_dir}")
        
        return user_dir
    
    def copy_template(self, template_path: str, target_dir: Optional[str] = None) -> str:
        """
        复制系统模板到用户模板目录
        
        参数:
            template_path: 要复制的模板相对路径
            target_dir: 目标目录，如果为None则使用默认用户目录
            
        返回:
            目标文件路径
            
        异常:
            FileNotFoundError: 如果源模板不存在
        """
        # 获取系统模板完整路径
        src_path = os.path.join(self.system_template_dir, template_path)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"模板不存在: {src_path}")
        
        # 创建用户模板目录
        if target_dir is None:
            user_home = os.path.expanduser("~")
            target_dir = os.path.join(user_home, ".autoregfile", "templates")
        
        # 确保目标目录存在
        target_subdir = os.path.dirname(os.path.join(target_dir, template_path))
        os.makedirs(target_subdir, exist_ok=True)
        
        # 复制模板
        target_path = os.path.join(target_dir, template_path)
        shutil.copy2(src_path, target_path)
        
        logger.info(f"已复制模板 {template_path} 到 {target_path}")
        
        return target_path


# 单例模式，全局模板管理器
_template_manager = None

def get_template_manager(template_dirs: Optional[List[str]] = None) -> TemplateManager:
    """
    获取全局模板管理器实例
    
    参数:
        template_dirs: 自定义模板目录列表
        
    返回:
        模板管理器实例
    """
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager(template_dirs)
    return _template_manager 