#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展字段属性支持测试

测试扩展字段属性的支持，包括：
1. 软件访问类型（READ_WRITE, READ, WRITE）
2. 硬件访问类型（READ, WRITE, READ_WRITE）
3. 字段锁定依赖关系
4. 魔术数字依赖关系
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到模块搜索路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from autoregfile.parsers.excel_parser import ExcelParser
from autoregfile.generators.verilog_generator import VerilogGenerator
from autoregfile.generators.doc_generator import DocGenerator

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
        
        # 显示软件访问类型
        print("\n软件访问类型:")
        for reg in config['registers']:
            if 'sw_access_type' in reg:
                print(f"  {reg['name']}: {reg['sw_access_type']}")
        
        # 显示硬件访问类型
        print("\n硬件访问类型:")
        for field in config['fields']:
            if 'hw_access_type' in field:
                print(f"  {field['register']}.{field['name']}: {field['hw_access_type']}")
        
        # 显示锁定依赖关系
        print("\n锁定依赖关系:")
        for field in config['fields']:
            if 'locked_by' in field and field['locked_by']:
                print(f"  {field['register']}.{field['name']} 被锁定依赖于: {field['locked_by']}")
        
        # 显示魔术数字依赖关系
        print("\n魔术数字依赖关系:")
        for field in config['fields']:
            if 'magic_number_dep' in field:
                print(f"  {field['register']}.{field['name']} 依赖于魔术数字: {field.get('magic_value', '无值')}")
        
        # 保存配置到JSON文件
        json_file = os.path.join(output_dir, 'extended_field_test.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n配置已保存为JSON: {json_file}")
        
        # 生成Verilog代码
        generator = VerilogGenerator()
        verilog_code = generator.generate(config)
        
        # 保存Verilog代码
        verilog_file = os.path.join(output_dir, f"{config['module_name']}.v")
        with open(verilog_file, 'w', encoding='utf-8') as f:
            f.write(verilog_code)
        print(f"生成的Verilog代码已保存: {verilog_file}")
        print(f"代码大小: {len(verilog_code)} 字节, {verilog_code.count(chr(10)) + 1} 行")
        
        # 生成文档
        doc_generator = DocGenerator()
        doc = doc_generator.generate(config)
        
        # 保存文档
        doc_file = os.path.join(output_dir, f"{config['module_name']}.md")
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc)
        print(f"生成的文档已保存: {doc_file}")
        
        print("\n所有生成任务已完成!")
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 