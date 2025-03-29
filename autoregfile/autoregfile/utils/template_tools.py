#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模板工具模块

提供用于管理和操作模板的工具函数，包括创建模板目录、复制模板文件等。
"""

import os
import shutil
import argparse
from typing import List, Optional, Dict, Any

from ..core.template_manager import get_template_manager
from . import get_logger, ensure_dir_exists


def create_template_directory(base_dir: str, protocol_name: Optional[str] = None, force: bool = False) -> bool:
    """
    创建模板目录结构
    
    Args:
        base_dir: 基础目录
        protocol_name: 协议名称，用于复制基础模板
        force: 是否强制覆盖现有文件
        
    Returns:
        bool: 是否成功创建
    """
    logger = get_logger("template_tools")
    
    # 获取模板管理器
    template_manager = get_template_manager()
    
    # 检查目录是否已存在
    if os.path.exists(base_dir) and not force:
        logger.warning(f"目录 {base_dir} 已存在，使用 --force 选项进行覆盖")
        return False
    
    # 使用模板管理器创建目录结构
    return template_manager.create_template_dir(base_dir, protocol_name)


def copy_template_dir(destination: str, force: bool = False) -> bool:
    """
    复制内置模板目录到指定位置
    
    Args:
        destination: 目标目录
        force: 是否强制覆盖现有文件
        
    Returns:
        bool: 是否成功复制
    """
    logger = get_logger("template_tools")
    
    # 检查目录是否已存在
    if os.path.exists(destination) and not force:
        logger.warning(f"目录 {destination} 已存在，使用 --force 选项进行覆盖")
        return False
    
    # 获取模板管理器
    template_manager = get_template_manager()
    
    # 复制模板目录
    return template_manager.copy_template_dir(destination)


def list_available_templates(category: Optional[str] = None) -> List[str]:
    """
    列出可用的模板
    
    Args:
        category: 模板类别，如'bus'、'field'等，如果为None则列出所有模板
        
    Returns:
        List[str]: 模板列表
    """
    # 获取模板管理器
    template_manager = get_template_manager()
    
    # 列出模板
    return template_manager.list_templates(category)


def create_custom_template(output_file: str, base_template: str, replacements: Dict[str, Any]) -> bool:
    """
    创建自定义模板
    
    通过复制和修改现有模板创建新的自定义模板
    
    Args:
        output_file: 输出文件路径
        base_template: 基础模板名称
        replacements: 替换内容字典
        
    Returns:
        bool: 是否成功创建
    """
    logger = get_logger("template_tools")
    
    # 获取模板管理器
    template_manager = get_template_manager()
    
    # 查找基础模板
    base_path = template_manager.find_template(base_template)
    if not base_path:
        logger.error(f"找不到基础模板: {base_template}")
        return False
    
    try:
        # 读取基础模板内容
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用替换
        for key, value in replacements.items():
            content = content.replace(key, str(value))
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not ensure_dir_exists(output_dir):
            logger.error(f"无法创建输出目录: {output_dir}")
            return False
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"已创建自定义模板: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"创建自定义模板时出错: {str(e)}", exc_info=True)
        return False


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description="模板管理工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 创建模板目录命令
    create_parser = subparsers.add_parser("create", help="创建模板目录结构")
    create_parser.add_argument("directory", help="目标目录")
    create_parser.add_argument("-p", "--protocol", help="协议名称，用于复制基础模板")
    create_parser.add_argument("-f", "--force", action="store_true", help="强制覆盖现有文件")
    
    # 复制模板目录命令
    copy_parser = subparsers.add_parser("copy", help="复制内置模板目录")
    copy_parser.add_argument("directory", help="目标目录")
    copy_parser.add_argument("-f", "--force", action="store_true", help="强制覆盖现有文件")
    
    # 列出模板命令
    list_parser = subparsers.add_parser("list", help="列出可用的模板")
    list_parser.add_argument("-c", "--category", help="模板类别，如'bus'、'field'等")
    
    # 创建自定义模板命令
    custom_parser = subparsers.add_parser("custom", help="创建自定义模板")
    custom_parser.add_argument("output", help="输出文件路径")
    custom_parser.add_argument("-b", "--base", required=True, help="基础模板名称")
    custom_parser.add_argument("-r", "--replace", nargs=2, action="append", metavar=("KEY", "VALUE"),
                              help="替换内容，可多次指定")
    
    args = parser.parse_args()
    
    # 处理命令
    if args.command == "create":
        success = create_template_directory(args.directory, args.protocol, args.force)
        return 0 if success else 1
        
    elif args.command == "copy":
        success = copy_template_dir(args.directory, args.force)
        return 0 if success else 1
        
    elif args.command == "list":
        templates = list_available_templates(args.category)
        for template in templates:
            print(template)
        return 0
        
    elif args.command == "custom":
        replacements = {}
        if args.replace:
            for key, value in args.replace:
                replacements[key] = value
                
        success = create_custom_template(args.output, args.base, replacements)
        return 0 if success else 1
        
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    exit(main()) 