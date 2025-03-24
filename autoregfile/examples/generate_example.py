#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本：使用配置文件生成寄存器文件和文档
"""

import os
import sys
import argparse
from typing import Dict, Any

# 确保可以导入autoregfile包
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from autoregfile.parsers.json_parser import JsonParser
from autoregfile.generators.verilog_generator import VerilogGenerator
from autoregfile.generators.header_generator import HeaderGenerator
from autoregfile.generators.doc_generator import DocGenerator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="寄存器文件生成示例")
    
    parser.add_argument("-c", "--config", default="example_config.json",
                       help="配置文件路径 (默认: example_config.json)")
    parser.add_argument("-o", "--output_dir", default="output",
                       help="输出目录 (默认: output)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="显示详细输出")
    
    args = parser.parse_args()
    
    try:
        # 获取配置文件的完整路径
        config_path = os.path.join(script_dir, args.config)
        if not os.path.isfile(config_path):
            print(f"错误: 配置文件不存在: {config_path}", file=sys.stderr)
            return 1
        
        # 创建输出目录
        output_dir = os.path.join(script_dir, args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        if args.verbose:
            print(f"使用配置文件: {config_path}")
            print(f"输出目录: {output_dir}")
        
        # 解析配置
        parser = JsonParser()
        config = parser.parse(config_path)
        
        module_name = config.get("module_name", "regfile")
        verilog_path = os.path.join(output_dir, f"{module_name}.v")
        header_path = os.path.join(output_dir, f"{module_name}.h")
        doc_path = os.path.join(output_dir, f"{module_name}.md")
        
        # 生成Verilog文件
        verilog_gen = VerilogGenerator()
        verilog_code = verilog_gen.generate(config)
        verilog_gen.save(verilog_code, verilog_path)
        if args.verbose:
            print(f"已生成Verilog文件: {verilog_path}")
        
        # 生成C语言头文件
        header_gen = HeaderGenerator()
        header_code = header_gen.generate(config)
        header_gen.save(header_code, header_path)
        if args.verbose:
            print(f"已生成C语言头文件: {header_path}")
        
        # 生成Markdown文档
        doc_gen = DocGenerator()
        doc_content = doc_gen.generate(config)
        doc_gen.save(doc_content, doc_path)
        if args.verbose:
            print(f"已生成Markdown文档: {doc_path}")
        
        print(f"成功生成寄存器文件和文档！输出位置: {output_dir}")
        return 0
    
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 