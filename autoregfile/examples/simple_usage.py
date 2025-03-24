#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoRegFile 简单使用示例
展示如何使用新的API生成寄存器文件
"""

from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator

def main():
    """示例主函数"""
    # 配置文件路径
    config_file = "examples/configs/simple_config.json"
    
    # 输出文件路径
    verilog_file = "examples/output/simple_regfile.v"
    header_file = "examples/output/simple_regfile.h"
    doc_file = "examples/output/simple_regfile.md"
    
    # 解析配置
    parser = JsonParser()
    config = parser.parse(config_file)
    
    # 生成Verilog文件
    verilog_gen = VerilogGenerator()
    verilog_code = verilog_gen.generate(config)
    verilog_gen.save(verilog_code, verilog_file)
    print(f"已生成Verilog文件: {verilog_file}")
    
    # 生成C语言头文件
    header_gen = HeaderGenerator()
    header_code = header_gen.generate(config)
    header_gen.save(header_code, header_file)
    print(f"已生成C语言头文件: {header_file}")
    
    # 生成Markdown文档
    doc_gen = DocGenerator()
    doc_content = doc_gen.generate(config)
    doc_gen.save(doc_content, doc_file)
    print(f"已生成Markdown文档: {doc_file}")


if __name__ == "__main__":
    main() 