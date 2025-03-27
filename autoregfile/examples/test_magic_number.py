#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试魔术数字依赖功能

此脚本专门测试魔术数字依赖功能的实现。
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到模块搜索路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from autoregfile.parsers.excel_parser import ExcelParser
from autoregfile.generators.verilog_generator import VerilogGenerator

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 配置文件路径
    excel_file = os.path.join(project_root, 'examples', 'configs', 'extended_field_test.xlsx')
    output_dir = os.path.join(project_root, 'examples', 'test')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"解析Excel配置文件: {excel_file}")
    
    # 初始化Excel解析器
    parser = ExcelParser()
    
    # 解析Excel文件
    try:
        config = parser.parse(excel_file)
        
        # 确认解析结果
        print(f"模块名称: {config['module_name']}")
        print(f"寄存器数量: {len(config['registers'])}")
        print(f"字段数量: {len(config['fields'])}")
        
        # 显示魔术数字依赖关系
        print("\n魔术数字依赖关系:")
        for field in config['fields']:
            if 'magic_number_dep' in field:
                print(f"  {field['register']}.{field['name']} 依赖于魔术数字: {field.get('magic_value', '无值')}")
                
        # 生成Verilog代码
        generator = VerilogGenerator()
        verilog_code = generator.generate(config)
        
        # 查找魔术数字验证代码
        print("\n魔术数字验证代码:")
        lines = verilog_code.split('\n')
        in_magic_section = False
        
        for i, line in enumerate(lines):
            if "魔术数字依赖" in line:
                in_magic_section = True
                print("\n=== 魔术数字依赖逻辑 ===")
                
            if in_magic_section and (line.strip() == "" or "硬件访问输出连接" in line):
                in_magic_section = False
                
            if in_magic_section:
                print(f"{i+1:4d}: {line}")
                
            # 查找包含魔术数字验证的写条件
            if "magic_valid" in line and "if" in line and "wr_en" in line:
                print(f"\n=== 字段写入条件中的魔术数字验证 ===")
                for j in range(max(0, i-2), min(i+3, len(lines))):
                    print(f"{j+1:4d}: {lines[j]}")
        
        # 保存Verilog代码
        verilog_file = os.path.join(output_dir, "magic_test.v")
        with open(verilog_file, 'w', encoding='utf-8') as f:
            f.write(verilog_code)
        print(f"\n生成的Verilog代码已保存: {verilog_file}")
        
        print("\n测试完成!")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 