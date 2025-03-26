#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器文件生成器主模块

提供命令行工具和生成器函数，创建寄存器文件RTL代码。
"""

import os
import sys
import json
import argparse
import time
from typing import Dict, Any, Optional, List

from .core.bus_generator import BusGenerator
from .core.bus_protocols import get_bus_protocol_manager
from .core.template_manager import get_template_manager, TemplateManager
from .core.address_planner import get_address_planner


def generate_regfile(
    config_file: str,
    output_file: str,
    auto_address: bool = False,
    bus_protocol: Optional[str] = None,
    template_dirs: Optional[List[str]] = None,
    custom_template: Optional[str] = None
) -> bool:
    """
    生成寄存器文件
    
    参数:
        config_file: 配置文件路径
        output_file: 输出文件路径
        auto_address: 是否自动分配地址
        bus_protocol: 指定的总线协议，如果为None则使用配置文件中指定的协议
        template_dirs: 自定义模板目录列表
        custom_template: 自定义模板路径
        
    返回:
        生成是否成功
    """
    try:
        print("正在生成寄存器文件...")
        print(f"配置文件: {config_file}")
        print(f"输出文件: {output_file}")
        if bus_protocol:
            print(f"总线协议: {bus_protocol}")
        
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 自动地址分配
        if auto_address:
            planner = get_address_planner()
            config = planner.auto_assign_addresses(config)
        
        # 确定总线协议
        if bus_protocol is None:
            bus_protocol = config.get('bus_protocol', 'custom')
        else:
            # 命令行参数优先级更高，更新配置
            config['bus_protocol'] = bus_protocol
        
        # 处理自定义模板
        if custom_template:
            if 'bus_options' not in config:
                config['bus_options'] = {}
            config['bus_options']['template'] = custom_template
        
        # 生成RTL代码
        if bus_protocol:
            # 使用总线生成器
            generator = BusGenerator(config, template_dirs)
            success = generator.generate(bus_protocol, output_file)
            if not success:
                # 获取错误信息
                print("生成总线接口寄存器文件失败!")
                return False
        else:
            # 使用基本的Verilog生成器
            from .generators.verilog_generator import VerilogGenerator
            generator = VerilogGenerator()
            
            try:
                verilog_code = generator.generate(config)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(verilog_code)
            except Exception as e:
                print(f"生成寄存器文件时出错: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
        
        return True
    
    except Exception as e:
        print(f"生成寄存器文件时出错: {str(e)}")
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        return False


def list_protocols():
    """打印所有支持的总线协议"""
    protocol_manager = get_bus_protocol_manager()
    protocols = protocol_manager.list_protocols()
    
    print("支持的总线协议:")
    for protocol in protocols:
        p = protocol_manager.get_protocol(protocol)
        print(f"  {protocol}: {p.description}")


def list_templates(category: Optional[str] = None):
    """
    列出可用的模板
    
    参数:
        category: 模板类别，如 'bus', 'register' 等，如果为None则列出所有类别
    """
    template_manager = get_template_manager()
    templates = template_manager.list_available_templates(category)
    
    print("可用的模板:")
    for cat, tmpl_list in templates.items():
        print(f"\n== {cat} ==")
        for tmpl in tmpl_list:
            source = tmpl['source']
            name = tmpl['name']
            path = tmpl['path']
            print(f"  {name}  [{source}]")
            print(f"    路径: {path}")


def copy_template(template_path: str, target_dir: Optional[str] = None):
    """
    复制模板到用户目录
    
    参数:
        template_path: 要复制的模板路径
        target_dir: 目标目录，如果为None则使用默认用户目录
    """
    try:
        template_manager = get_template_manager()
        target = template_manager.copy_template(template_path, target_dir)
        print(f"模板已复制到: {target}")
        return True
    except Exception as e:
        print(f"复制模板时出错: {str(e)}")
        return False


def create_template_dir(target_dir: Optional[str] = None):
    """
    创建模板目录
    
    参数:
        target_dir: 目标目录，如果为None则使用默认用户目录
    """
    try:
        template_manager = get_template_manager()
        target = template_manager.create_user_template_dir(target_dir)
        print(f"模板目录已创建: {target}")
        return True
    except Exception as e:
        print(f"创建模板目录时出错: {str(e)}")
        return False


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='生成寄存器文件RTL代码')
    
    # 基本参数
    parser.add_argument('-c', '--config', help='配置文件路径', required=False)
    parser.add_argument('-o', '--output', help='输出文件路径', required=False)
    parser.add_argument('-p', '--bus-protocol', help='总线协议 (apb, axi_lite, wishbone, ocp, custom)')
    parser.add_argument('--auto-address', action='store_true', help='自动分配寄存器地址')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    # 模板相关参数
    parser.add_argument('--template-dir', action='append', help='自定义模板目录路径，可以指定多个')
    parser.add_argument('--custom-template', help='使用自定义总线协议模板')
    
    # 工具命令
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-protocols', action='store_true', help='列出所有支持的总线协议')
    group.add_argument('--list-templates', action='store_true', help='列出所有可用的模板')
    group.add_argument('--list-bus-templates', action='store_true', help='列出所有可用的总线协议模板')
    group.add_argument('--copy-template', help='复制模板到用户目录')
    group.add_argument('--create-template-dir', action='store_true', help='创建用户模板目录')
    
    args = parser.parse_args()
    
    # 处理调试模式
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # 执行工具命令
    if args.list_protocols:
        list_protocols()
        return 0
    elif args.list_templates:
        list_templates()
        return 0
    elif args.list_bus_templates:
        list_templates('verilog/bus')
        return 0
    elif args.copy_template:
        if copy_template(args.copy_template):
            return 0
        else:
            return 1
    elif args.create_template_dir:
        if create_template_dir():
            return 0
        else:
            return 1
    
    # 检查必需参数
    if not args.config:
        parser.error('需要提供配置文件路径 (-c/--config)')
    if not args.output:
        parser.error('需要提供输出文件路径 (-o/--output)')
    
    # 验证文件路径
    if not os.path.exists(args.config):
        print(f"错误: 配置文件不存在: {args.config}")
        return 1
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成寄存器文件
    print(f"正在生成寄存器文件...")
    print(f"配置文件: {args.config}")
    print(f"输出文件: {args.output}")
    if args.bus_protocol:
        print(f"总线协议: {args.bus_protocol}")
    if args.auto_address:
        print("自动地址分配: 启用")
    if args.template_dir:
        print(f"自定义模板目录: {', '.join(args.template_dir)}")
    if args.custom_template:
        print(f"自定义模板: {args.custom_template}")
    
    start_time = time.time()
    
    success = generate_regfile(
        args.config,
        args.output,
        args.auto_address,
        args.bus_protocol,
        args.template_dir,
        args.custom_template
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        print(f"生成完成！用时: {duration:.2f}秒")
        return 0
    else:
        print("生成失败!")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 