#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器文件生成主程序

提供命令行接口用于生成寄存器文件。
"""

import os
import sys
import argparse
from typing import Dict, Any

# 确保可以导入autoregfile包
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from autoregfile.parsers.base_parser import ConfigParser, detect_parser
from autoregfile.generators.verilog_generator import VerilogGenerator
from autoregfile.generators.header_generator import HeaderGenerator
from autoregfile.generators.doc_generator import DocGenerator


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="寄存器文件生成工具")
    
    # 配置输入
    parser.add_argument("-c", "--config", required=True,
                      help="配置文件路径 (支持JSON, YAML, Excel)")
    
    # 输出选项
    parser.add_argument("-o", "--output", required=True,
                      help="输出目录或文件路径")
    parser.add_argument("--verilog", action="store_true", default=True,
                      help="生成Verilog文件 (默认开启)")
    parser.add_argument("--header", action="store_true",
                      help="生成C语言头文件")
    parser.add_argument("--doc", action="store_true",
                      help="生成Markdown文档")
    
    # 高级选项
    parser.add_argument("-t", "--templates", 
                      help="自定义模板目录")
    parser.add_argument("-v", "--verbose", action="store_true",
                      help="显示详细输出")
    
    return parser.parse_args()


def main() -> int:
    """主函数"""
    args = parse_args()
    
    try:
        # 解析配置
        parser = detect_parser(args.config)
        config = parser.parse(args.config)
        
        # 准备输出路径
        if os.path.isdir(args.output):
            output_dir = args.output
            module_name = config.get("module_name", "regfile")
            verilog_path = os.path.join(output_dir, f"{module_name}.v")
            header_path = os.path.join(output_dir, f"{module_name}.h")
            doc_path = os.path.join(output_dir, f"{module_name}.md")
        else:
            output_dir = os.path.dirname(args.output)
            name_base = os.path.splitext(os.path.basename(args.output))[0]
            verilog_path = args.output
            header_path = os.path.join(output_dir, f"{name_base}.h")
            doc_path = os.path.join(output_dir, f"{name_base}.md")
        
        # 生成Verilog文件
        if args.verilog:
            generator = VerilogGenerator(args.templates)
            content = generator.generate(config)
            generator.save(content, verilog_path)
            if args.verbose:
                print(f"已生成Verilog文件: {verilog_path}")
        
        # 生成头文件
        if args.header:
            generator = HeaderGenerator(args.templates)
            content = generator.generate(config)
            generator.save(content, header_path)
            if args.verbose:
                print(f"已生成C语言头文件: {header_path}")
        
        # 生成文档
        if args.doc:
            generator = DocGenerator(args.templates)
            content = generator.generate(config)
            generator.save(content, doc_path)
            if args.verbose:
                print(f"已生成Markdown文档: {doc_path}")
        
        return 0
    
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 