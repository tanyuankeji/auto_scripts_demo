#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoRegFile Excel配置文件使用示例
展示如何使用Excel格式的配置文件生成寄存器文件
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator, HeaderGenerator, DocGenerator


def create_example_excel(excel_file_path):
    """创建一个示例Excel配置文件"""
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'num_write_ports',
            'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'excel_regfile', 32, 8, 1, 2, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器定义
    registers_data = {
        'name': ['CTRL_REG', 'STATUS_REG', 'INT_FLAGS', 'INT_ENABLE'],
        'address': ['0x00', '0x04', '0x08', '0x0C'],
        'type': ['ReadWrite', 'ReadOnly', 'ReadClean', 'ReadWrite'],
        'reset_value': ['0x00000000', '0x00000000', '0x00000000', '0x00000000'],
        'description': ['控制寄存器', '状态寄存器', '中断标志寄存器', '中断使能寄存器']
    }
    registers_df = pd.DataFrame(registers_data)
    
    # 位域定义
    fields_data = {
        'register': [
            'CTRL_REG', 'CTRL_REG', 'CTRL_REG', 
            'STATUS_REG', 'STATUS_REG', 
            'INT_FLAGS', 'INT_FLAGS',
            'INT_ENABLE', 'INT_ENABLE'
        ],
        'name': [
            'ENABLE', 'MODE', 'START',
            'BUSY', 'ERROR',
            'DATA_READY', 'ERROR_FLAG',
            'DATA_READY_EN', 'ERROR_EN'
        ],
        'bit_range': [
            '0', '2:1', '3',
            '0', '1',
            '0', '1',
            '0', '1'
        ],
        'description': [
            '使能位', '模式设置', '启动位',
            '忙状态标志', '错误标志',
            '数据就绪中断', '错误中断',
            '数据就绪中断使能', '错误中断使能'
        ]
    }
    fields_df = pd.DataFrame(fields_data)
    
    # 创建Excel文件
    with pd.ExcelWriter(excel_file_path) as writer:
        config_df.to_excel(writer, sheet_name='Config', index=False)
        registers_df.to_excel(writer, sheet_name='Registers', index=False)
        fields_df.to_excel(writer, sheet_name='Fields', index=False)
    
    print(f"已创建示例Excel配置文件: {excel_file_path}")


def main():
    """Excel配置使用示例主函数"""
    print("AutoRegFile Excel配置文件使用示例")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    excel_file = configs_dir / "example_config.xlsx"
    
    # 创建示例Excel文件
    if not os.path.exists(excel_file):
        print("\n1. 创建示例Excel配置文件")
        create_example_excel(excel_file)
    else:
        print(f"\n1. 使用现有Excel配置文件: {excel_file}")
    
    # 输出文件路径
    output_dir = current_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    verilog_file = output_dir / "excel_regfile.v"
    header_file = output_dir / "excel_regfile.h"
    doc_file = output_dir / "excel_regfile.md"
    json_file = output_dir / "excel_regfile.json"
    
    # 2. 解析Excel配置
    print("\n2. 解析Excel配置文件")
    parser = ExcelParser()
    try:
        config = parser.parse(excel_file)
        print(f"  成功解析Excel配置文件: {excel_file}")
        print(f"  模块名称: {config.get('module_name')}")
        print(f"  寄存器数量: {len(config.get('registers', []))}")
        print(f"  位域数量: {len(config.get('fields', []))}")
        
        # 保存为JSON格式（便于调试和查看）
        with open(json_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"  已保存为JSON格式: {json_file}")
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
    except Exception as e:
        print(f"  生成Verilog文件失败: {e}")
        return 1
    
    # 4. 生成C语言头文件
    print("\n4. 生成C语言头文件")
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
    
    # 5. 生成Markdown文档
    print("\n5. 生成Markdown文档")
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
    
    # 6. Excel与JSON相互转换示例
    print("\n6. Excel与JSON相互转换示例")
    try:
        # 将JSON配置转换回Excel
        reverse_excel_file = output_dir / "reverse_config.xlsx"
        
        # 提取全局配置
        global_config = {k: v for k, v in config.items() if k not in ('registers', 'fields')}
        config_df = pd.DataFrame([(k, v) for k, v in global_config.items()], 
                               columns=['parameter', 'value'])
        
        # 提取寄存器和位域定义
        registers_df = pd.DataFrame(config['registers'])
        fields_df = pd.DataFrame(config['fields'])
        
        # 保存为Excel
        with pd.ExcelWriter(reverse_excel_file) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            registers_df.to_excel(writer, sheet_name='Registers', index=False)
            fields_df.to_excel(writer, sheet_name='Fields', index=False)
        
        print(f"  已将JSON转换回Excel: {reverse_excel_file}")
    except Exception as e:
        print(f"  Excel与JSON相互转换示例失败: {e}")
    
    print("\n成功完成所有生成工作!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 