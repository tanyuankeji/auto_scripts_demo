#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有寄存器类型

此脚本用于测试 AutoRegFile 支持的所有寄存器类型，包括：
1. 创建一个包含所有寄存器类型的 Excel 配置文件
2. 使用该配置文件生成 Verilog 代码
3. 测试生成的代码功能
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


def create_all_reg_types_excel(excel_file_path):
    """创建一个包含所有寄存器类型的Excel配置文件"""
    print(f"创建包含所有寄存器类型的Excel配置文件: {excel_file_path}")
    
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'all_reg_types', 32, 10, 'apb', 1, 1, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 支持的所有寄存器类型
    reg_types = [
        'ReadWrite',      # 标准读写寄存器
        'ReadOnly',       # 只读寄存器
        'WriteOnly',      # 只写寄存器
        'Write1Clean',    # 写1清零寄存器
        'Write1Set',      # 写1置位寄存器
        'Write0Clean',    # 写0清零寄存器
        'Write0Set',      # 写0置位寄存器
        'WriteOnce',      # 只能写一次的寄存器
        'WriteOnlyOnce',  # 只能写一次且只写的寄存器
        'ReadClean',      # 读取后自动清零寄存器
        'ReadSet',        # 读取后自动置位寄存器
        'WriteReadClean', # 可写且读取后自动清零寄存器
        'WriteReadSet',   # 可写且读取后自动置位寄存器
        'Write1Pulse',    # 写1产生脉冲寄存器
        'Write0Pulse'     # 写0产生脉冲寄存器
    ]
    
    # 准备数据行
    rows = []
    
    # 为每种寄存器类型创建一个示例寄存器和字段
    for i, reg_type in enumerate(reg_types):
        # 寄存器名和地址
        reg_name = f"{reg_type.upper()}_REG"
        addr = f"0x{i*4:02X}"
        
        # 添加寄存器行
        rows.append({
            'register_name': reg_name,
            'address': addr,
            'register_type': reg_type,
            'register_reset_value': '0x00000000',
            'register_description': f"{reg_type}类型寄存器",
            'sw_access_type': 'READ_WRITE',
            'hw_access_type': '',
            'field_name': '',
            'bit_range': '',
            'field_type': '',
            'field_reset_value': '',
            'field_description': '',
            'field_function': '',
            'field_sw_access_type': '',
            'field_hw_access_type': ''
        })
        
        # 添加一个空行作为分隔
        rows.append({
            'register_name': '',
            'address': '',
            'register_type': '',
            'register_reset_value': '',
            'register_description': '',
            'sw_access_type': '',
            'hw_access_type': '',
            'field_name': '',
            'bit_range': '',
            'field_type': '',
            'field_reset_value': '',
            'field_description': '',
            'field_function': '',
            'field_sw_access_type': '',
            'field_hw_access_type': ''
        })
        
        # 添加寄存器的字段
        rows.append({
            'register_name': '',
            'address': '',
            'register_type': '',
            'register_reset_value': '',
            'register_description': '',
            'sw_access_type': '',
            'hw_access_type': '',
            'field_name': 'VALUE',
            'bit_range': '31:0',
            'field_type': reg_type,
            'field_reset_value': '0x00000000',
            'field_description': f"{reg_type}类型字段",
            'field_function': f"测试{reg_type}功能",
            'field_sw_access_type': 'READ_WRITE',
            'field_hw_access_type': ''
        })
        
        # 为位域类型添加更多的字段
        if reg_type in ['Write1Clean', 'Write1Set', 'Write0Clean', 'Write0Set', 'Write1Pulse', 'Write0Pulse']:
            # 添加一个位字段
            rows.append({
                'register_name': '',
                'address': '',
                'register_type': '',
                'register_reset_value': '',
                'register_description': '',
                'sw_access_type': '',
                'hw_access_type': '',
                'field_name': 'BIT0',
                'bit_range': '0',
                'field_type': reg_type,
                'field_reset_value': '0',
                'field_description': f"{reg_type}位字段",
                'field_function': f"测试{reg_type}位功能",
                'field_sw_access_type': 'READ_WRITE',
                'field_hw_access_type': ''
            })
            
            # 添加一个多位字段
            rows.append({
                'register_name': '',
                'address': '',
                'register_type': '',
                'register_reset_value': '',
                'register_description': '',
                'sw_access_type': '',
                'hw_access_type': '',
                'field_name': 'BITS',
                'bit_range': '4:1',
                'field_type': reg_type,
                'field_reset_value': '0',
                'field_description': f"{reg_type}多位字段",
                'field_function': f"测试{reg_type}多位功能",
                'field_sw_access_type': 'READ_WRITE',
                'field_hw_access_type': ''
            })
    
    # 创建DataFrame
    register_fields_df = pd.DataFrame(rows)
    
    # 创建Excel文件
    try:
        with pd.ExcelWriter(excel_file_path) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            register_fields_df.to_excel(writer, sheet_name='RegisterFields', index=False)
        print(f"成功创建Excel配置文件: {excel_file_path}")
        return True
    except Exception as e:
        print(f"创建Excel文件失败: {str(e)}")
        return False


def generate_verilog_from_excel(excel_file, output_dir):
    """使用Excel配置文件生成Verilog代码"""
    print(f"\n使用Excel配置文件生成Verilog代码: {excel_file}")
    
    if not os.path.exists(excel_file):
        print(f"错误: Excel文件不存在: {excel_file}")
        return False
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 输出文件路径
    verilog_file = os.path.join(output_dir, "all_reg_types.v")
    apb_file = os.path.join(output_dir, "all_reg_types_apb.v")
    header_file = os.path.join(output_dir, "all_reg_types.h")
    doc_file = os.path.join(output_dir, "all_reg_types.md")
    json_file = os.path.join(output_dir, "all_reg_types.json")
    
    try:
        # 1. 解析Excel配置
        print("\n1. 解析Excel配置文件")
        parser = ExcelParser()
        config = parser.parse(excel_file)
        print(f"  成功解析Excel配置文件")
        print(f"  模块名称: {config.get('module_name')}")
        print(f"  寄存器数量: {len(config.get('registers', []))}")
        print(f"  字段数量: {len(config.get('fields', []))}")
        
        # 保存为JSON格式（便于调试和查看）
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"  已保存为JSON格式: {json_file}")
        
        # 2. 生成Verilog文件
        print("\n2. 生成Verilog文件")
        verilog_gen = VerilogGenerator()
        verilog_code = verilog_gen.generate(config)
        verilog_gen.save(verilog_code, verilog_file)
        print(f"  已生成Verilog文件: {verilog_file}")
        
        # 显示生成的文件大小和行数
        file_size = os.path.getsize(verilog_file)
        with open(verilog_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"  文件大小: {file_size} 字节, {line_count} 行")
        
        # 3. 生成APB总线接口文件
        print("\n3. 生成APB总线接口文件")
        # 设置bus_protocol为apb
        config['bus_protocol'] = 'apb'
        
        # 使用临时JSON文件
        temp_json = os.path.join(output_dir, "temp_apb_config.json")
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        # 使用regfile_gen生成APB总线接口
        generate_regfile(temp_json, apb_file, False, 'apb')
        print(f"  已生成APB总线接口文件: {apb_file}")
        
        # 清理临时文件
        os.remove(temp_json)
        
        # 4. 生成C语言头文件
        print("\n4. 生成C语言头文件")
        header_gen = HeaderGenerator()
        header_code = header_gen.generate(config)
        header_gen.save(header_code, header_file)
        print(f"  已生成C语言头文件: {header_file}")
        
        # 5. 生成Markdown文档
        print("\n5. 生成Markdown文档")
        doc_gen = DocGenerator()
        doc_content = doc_gen.generate(config)
        doc_gen.save(doc_content, doc_file)
        print(f"  已生成Markdown文档: {doc_file}")
        
        return True
    except Exception as e:
        print(f"生成代码时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_generated_code(output_dir):
    """测试生成的代码功能"""
    print("\n测试生成的代码功能")
    
    verilog_file = os.path.join(output_dir, "all_reg_types.v")
    if not os.path.exists(verilog_file):
        print(f"错误: Verilog文件不存在: {verilog_file}")
        return False
    
    # 检查生成的代码是否包含所有寄存器类型
    reg_types = [
        'ReadWrite', 'ReadOnly', 'WriteOnly', 'Write1Clean', 'Write1Set',
        'Write0Clean', 'Write0Set', 'WriteOnce', 'WriteOnlyOnce',
        'ReadClean', 'ReadSet', 'WriteReadClean', 'WriteReadSet',
        'Write1Pulse', 'Write0Pulse'
    ]
    
    with open(verilog_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("检查各寄存器类型是否成功生成:")
    for reg_type in reg_types:
        reg_name = f"{reg_type.upper()}_REG"
        if reg_name in content:
            print(f"  ✓ {reg_type} (寄存器名: {reg_name})")
        else:
            print(f"  ✗ {reg_type} (寄存器名: {reg_name})")
    
    return True


def main():
    """主函数"""
    print("测试所有寄存器类型")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    excel_file = configs_dir / "all_reg_types.xlsx"
    
    # 输出目录
    output_dir = current_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 创建Excel配置文件
    if not create_all_reg_types_excel(excel_file):
        return 1
    
    # 2. 生成Verilog代码
    if not generate_verilog_from_excel(excel_file, output_dir):
        return 1
    
    # 3. 测试生成的代码
    if not test_generated_code(output_dir):
        return 1
    
    print("\n成功完成所有测试!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 