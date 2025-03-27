#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单表格Excel配置和硬件访问类型使用示例

展示如何使用单表格Excel格式定义寄存器和字段，并使用软硬件访问类型生成带有字段级别注释的Verilog代码。
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

# 确保能够导入autoregfile包
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# 导入autoregfile包
from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator
from autoregfile.regfile_gen import generate_regfile

# 首先导入创建单表格Excel的函数
from create_single_sheet_excel import create_single_sheet_excel


def main():
    """单表格Excel配置和硬件访问类型使用示例主函数"""
    print("单表格Excel配置和硬件访问类型使用示例")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    excel_file = configs_dir / "single_sheet_example.xlsx"
    
    # 如果Excel文件不存在，则创建
    if not os.path.exists(excel_file):
        print("\n1. 创建单表格Excel配置文件")
        create_single_sheet_excel(excel_file)
    else:
        print(f"\n1. 使用现有单表格Excel配置文件: {excel_file}")
    
    # 输出文件路径
    output_dir = current_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    verilog_file = output_dir / "single_sheet_regfile.v"
    header_file = output_dir / "single_sheet_regfile.h"
    doc_file = output_dir / "single_sheet_regfile.md"
    json_file = output_dir / "single_sheet_regfile.json"
    
    # 2. 解析Excel配置
    print("\n2. 解析单表格Excel配置文件")
    parser = ExcelParser()
    try:
        config = parser.parse(excel_file)
        print(f"  成功解析Excel配置文件: {excel_file}")
        print(f"  模块名称: {config.get('module_name')}")
        print(f"  寄存器数量: {len(config.get('registers', []))}")
        print(f"  位域数量: {len(config.get('fields', []))}")
        
        # 打印软硬件访问类型信息
        print("\n  软硬件访问类型信息:")
        for reg in config.get('registers', []):
            sw_access = reg.get('sw_access_type', 'READ_WRITE')
            hw_access = reg.get('hw_access_type', '-')
            print(f"  寄存器 {reg['name']}: 软件访问={sw_access}, 硬件访问={hw_access}")
        
        print("\n  字段级别硬件接口信息:")
        for field in config.get('fields', []):
            hw_access = field.get('hw_access_type', '-')
            if hw_access in ['READ', 'WRITE', 'READ_WRITE']:
                print(f"  字段 {field['register']}.{field['name']}: 硬件访问={hw_access}")
        
        # 保存为JSON格式（便于调试和查看）
        with open(json_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n  已保存为JSON格式: {json_file}")
    except Exception as e:
        print(f"  解析Excel配置文件失败: {e}")
        return 1
    
    # 3. 生成Verilog文件
    print("\n3. 生成Verilog文件")
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
        
        # 输出文件的前50行内容预览
        print("\n  Verilog文件内容预览 (前50行):")
        with open(verilog_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:50]
            for i, line in enumerate(lines, 1):
                print(f"    {i:3d}: {line.rstrip()}")
            print("    ...")
    except Exception as e:
        print(f"  生成Verilog文件失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 4. 生成文档
    print("\n4. 生成文档")
    doc_gen = DocGenerator()
    try:
        doc_content = doc_gen.generate(config)
        doc_gen.save(doc_content, doc_file)
        print(f"  已生成Markdown文档: {doc_file}")
    except Exception as e:
        print(f"  生成文档失败: {e}")
    
    print("\n成功完成所有生成工作!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 