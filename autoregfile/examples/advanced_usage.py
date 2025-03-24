#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoRegFile 高级使用示例
展示更复杂的工作流程，包括多种输出格式和自定义模板
"""

import os
import sys
from pathlib import Path

from autoregfile.parsers import JsonParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator

def main():
    """高级使用示例主函数"""
    print("AutoRegFile 高级使用示例")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    config_file = current_dir / "configs" / "advanced_config.json"
    
    # 输出文件路径
    output_dir = current_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    verilog_file = output_dir / "advanced_regfile.v"
    header_file = output_dir / "advanced_regfile.h"
    doc_file = output_dir / "advanced_regfile.md"
    
    # 1. 基本使用 - 解析配置
    print("\n1. 解析配置文件")
    parser = JsonParser()
    try:
        config = parser.parse(config_file)
        print(f"  成功解析配置文件: {config_file}")
        print(f"  模块名称: {config.get('module_name')}")
        print(f"  寄存器数量: {len(config.get('registers', []))}")
        print(f"  位域数量: {len(config.get('fields', []))}")
    except Exception as e:
        print(f"  解析配置文件失败: {e}")
        return 1
    
    # 2. 生成Verilog文件
    print("\n2. 生成Verilog文件")
    verilog_gen = VerilogGenerator()
    try:
        verilog_code = verilog_gen.generate(config)
        verilog_gen.save(verilog_code, verilog_file)
        print(f"  已生成Verilog文件: {verilog_file}")
        
        # 显示生成的文件大小和行数
        file_size = os.path.getsize(verilog_file)
        with open(verilog_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"  文件大小: {file_size} 字节, {line_count} 行")
    except Exception as e:
        print(f"  生成Verilog文件失败: {e}")
        return 1
    
    # 3. 生成C语言头文件
    print("\n3. 生成C语言头文件")
    header_gen = HeaderGenerator()
    try:
        header_code = header_gen.generate(config)
        header_gen.save(header_code, header_file)
        print(f"  已生成C语言头文件: {header_file}")
        
        # 显示生成的文件大小和行数
        file_size = os.path.getsize(header_file)
        with open(header_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"  文件大小: {file_size} 字节, {line_count} 行")
    except Exception as e:
        print(f"  生成C语言头文件失败: {e}")
        return 1
    
    # 4. 生成Markdown文档
    print("\n4. 生成Markdown文档")
    doc_gen = DocGenerator()
    try:
        doc_content = doc_gen.generate(config)
        doc_gen.save(doc_content, doc_file)
        print(f"  已生成Markdown文档: {doc_file}")
        
        # 显示生成的文件大小和行数
        file_size = os.path.getsize(doc_file)
        with open(doc_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"  文件大小: {file_size} 字节, {line_count} 行")
    except Exception as e:
        print(f"  生成Markdown文档失败: {e}")
        return 1
    
    # 5. 打印寄存器类型统计
    print("\n5. 寄存器类型统计")
    reg_types = {}
    for reg in config.get('registers', []):
        reg_type = reg.get('type')
        if reg_type in reg_types:
            reg_types[reg_type] += 1
        else:
            reg_types[reg_type] = 1
    
    for reg_type, count in reg_types.items():
        print(f"  {reg_type}: {count}个")
    
    # 6. 打印位域统计
    print("\n6. 位域统计")
    field_counts = {}
    for field in config.get('fields', []):
        reg_name = field.get('register')
        if reg_name in field_counts:
            field_counts[reg_name] += 1
        else:
            field_counts[reg_name] = 1
    
    for reg_name, count in field_counts.items():
        print(f"  {reg_name}: {count}个位域")
    
    print("\n成功完成所有生成工作!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 