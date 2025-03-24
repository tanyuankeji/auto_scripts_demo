#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析模块

负责解析命令行参数和配置文件，为寄存器文件生成器提供配置参数。
"""

import argparse
import os
import json
import yaml
from typing import Dict, Any

try:
    from excel_parser import ExcelConfigParser
except ImportError:
    from src.excel_parser import ExcelConfigParser


def parse_config_file(config_file: str) -> Dict[str, Any]:
    """解析配置文件 (JSON, YAML 或 Excel)"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件不存在: {config_file}")
    
    file_ext = os.path.splitext(config_file)[1].lower()
    
    try:
        if file_ext in ('.xls', '.xlsx'):
            return ExcelConfigParser.parse(config_file)
        
        with open(config_file, 'r') as f:
            if file_ext == '.json':
                return json.load(f)
            elif file_ext in ('.yml', '.yaml'):
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {file_ext}")
    except Exception as e:
        raise RuntimeError(f"解析配置文件时出错: {str(e)}")


def setup_argument_parser() -> argparse.ArgumentParser:
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description="自动生成Verilog寄存器文件")
    
    # 基本参数
    parser.add_argument("-m", "--module", default="regfile", help="模块名称")
    parser.add_argument("-d", "--data-width", type=int, default=32, help="数据宽度 (位)")
    parser.add_argument("-a", "--addr-width", type=int, default=5, help="地址宽度 (位)")
    parser.add_argument("-wr", "--write-ports", type=int, default=1, help="写端口数量")
    parser.add_argument("-rd", "--read-ports", type=int, default=2, help="读端口数量")
    
    # 复位选项
    parser.add_argument("--sync-reset", action="store_true", help="使用同步复位 (默认为异步复位)")
    parser.add_argument("--reset-value", default="0", help="复位初始化值 (支持十六进制，如0xF)")
    
    # 高级选项
    parser.add_argument("--byte-enable", action="store_true", help="启用字节使能")
    parser.add_argument("--config", help="从JSON, YAML或Excel文件加载配置")
    parser.add_argument("--implementation", choices=["always", "instance"], default="always", 
                       help="实现方式: always块或寄存器例化 (默认: always)")
    parser.add_argument("--default-reg-type", default="ReadWrite", 
                       help="默认寄存器类型 (默认: ReadWrite)")
    
    # 输出选项
    parser.add_argument("-o", "--output", default="regfile.v", help="输出Verilog文件名")
    parser.add_argument("--gen-header", action="store_true", help="生成C语言头文件")
    parser.add_argument("--header-output", help="C语言头文件输出路径 (默认为与Verilog文件同名，扩展名为.h)")
    parser.add_argument("--output-dir", help="输出目录路径")
    parser.add_argument("--gen-doc", action="store_true", help="生成Markdown文档")
    parser.add_argument("--doc-output", help="Markdown文档输出路径 (默认为与Verilog文件同名，扩展名为.md)")
    
    return parser


def parse_args_to_config(args) -> Dict[str, Any]:
    """将命令行参数转换为配置字典"""
    config = {
        'module_name': args.module,
        'data_width': args.data_width,
        'addr_width': args.addr_width,
        'num_write_ports': args.write_ports,
        'num_read_ports': args.read_ports,
        'sync_reset': args.sync_reset,
        'reset_value': args.reset_value,
        'byte_enable': args.byte_enable,
        'implementation': args.implementation,
        'default_reg_type': args.default_reg_type
    }
    
    return config


if __name__ == "__main__":
    # 测试代码
    parser = setup_argument_parser()
    args = parser.parse_args()
    config = parse_args_to_config(args)
    print(config)