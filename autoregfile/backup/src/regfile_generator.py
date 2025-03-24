#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Register File Generator

一个用于自动生成Verilog寄存器文件的高级工具，支持多种配置选项和扩展功能。
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

# 导入各个模块
from src.verilog_generator import VerilogGenerator
from src.header_generator import HeaderGenerator
from src.doc_generator import DocumentGenerator


class RegFileGenerator:
    """寄存器文件生成器主类"""
    
    def __init__(self):
        self.verilog_generator = VerilogGenerator()
    
    def generate(self, config: Dict[str, Any]) -> Dict[str, str]:
        """生成所有输出文件"""
        result = {}
        
        # 生成Verilog代码
        verilog_code = self.verilog_generator.generate_regfile(config)
        result['verilog'] = verilog_code
        
        # 生成C语言头文件
        if config.get('gen_header', False):
            header_code = HeaderGenerator.generate(config)
            result['header'] = header_code
        
        # 生成Markdown文档
        if config.get('gen_doc', False):
            doc_content = DocumentGenerator.generate_markdown_doc(config, verilog_code)
            result['doc'] = doc_content
        
        return result
    
    def save_files(self, result: Dict[str, str], config: Dict[str, Any]) -> None:
        """保存生成的文件"""
        output_dir = config.get('output_dir', '')
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存Verilog文件
        verilog_path = os.path.join(output_dir, config.get('output', 'regfile.v'))
        with open(verilog_path, 'w') as f:
            f.write(result['verilog'])
        print(f"Verilog文件已生成: {verilog_path}")
        
        # 保存C语言头文件
        if 'header' in result:
            if config.get('header_output'):
                header_path = os.path.join(output_dir, config.get('header_output'))
            else:
                header_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.h')
            
            with open(header_path, 'w') as f:
                f.write(result['header'])
            print(f"C语言头文件已生成: {header_path}")
        
        # 保存Markdown文档
        if 'doc' in result:
            if config.get('doc_output'):
                doc_path = os.path.join(output_dir, config.get('doc_output'))
            else:
                doc_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.md')
            
            with open(doc_path, 'w') as f:
                f.write(result['doc'])
            print(f"Markdown文档已生成: {doc_path}")


def parse_config_file(config_file: str) -> Dict[str, Any]:
    """解析配置文件 (JSON 或 YAML)"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件不存在: {config_file}")
    
    file_ext = os.path.splitext(config_file)[1].lower()
    
    try:
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
    parser.add_argument("--config", help="从JSON或YAML文件加载配置")
    
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
        'byte_enable': args.byte_enable
    }
    
    return config


def main():
    """主函数"""
    # 解析命令行参数
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 初始化配置
    if args.config:
        # 从配置文件加载
        config = parse_config_file(args.config)
    else:
        # 从命令行参数加载
        config = parse_args_to_config(args)
    
    # 添加输出选项到配置
    config['output'] = args.output
    config['gen_header'] = args.gen_header
    config['header_output'] = args.header_output
    config['output_dir'] = args.output_dir
    config['gen_doc'] = args.gen_doc
    config['doc_output'] = args.doc_output
    
    # 创建生成器并生成文件
    generator = RegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)


if __name__ == "__main__":
    main()