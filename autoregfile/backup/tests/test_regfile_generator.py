#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器文件生成器测试

测试不同寄存器类型和实现方式的生成效果。
"""

import os
import sys
import json
import argparse
from pathlib import Path
# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.regfile_generator import RegFileGenerator
from src.register_types import RegisterTypeManager


def test_with_json_config():
    """测试使用JSON配置文件生成寄存器文件"""
    # 创建一个简单的JSON配置
    config = {
        'module_name': 'json_test_regfile',
        'data_width': 32,
        'addr_width': 4,
        'num_read_ports': 2,
        'num_write_ports': 1,
        'sync_reset': False,
        'reset_value': 0,
        'byte_enable': False,
        'implementation': 'instance',
        'default_reg_type': 'ReadWrite',
        'registers': [
            {
                'name': 'CTRL',
                'address': 0,
                'width': 32,
                'type': 'ReadWrite',
                'reset_value': 0,
                'description': '控制寄存器'
            },
            {
                'name': 'STATUS',
                'address': 4,
                'width': 32,
                'type': 'ReadOnly',
                'reset_value': 0,
                'description': '状态寄存器'
            },
            {
                'name': 'IRQ_STATUS',
                'address': 8,
                'width': 32,
                'type': 'ReadClean',
                'reset_value': 0,
                'description': '中断状态寄存器，读取后清零'
            }
        ],
        'output': 'json_test_regfile.v',
        'gen_header': True,
        'gen_doc': True
    }
    
    # 保存为临时文件
    with open('temp_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # 创建生成器并生成文件
    generator = RegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)
    
    print(f"已生成 JSON 配置测试文件: {config['output']}")
    
    # 删除临时文件
    os.remove('temp_config.json')


def test_always_block_implementation():
    """测试使用always块实现方式生成寄存器文件"""
    config = {
        'module_name': 'always_test_regfile',
        'data_width': 32,
        'addr_width': 4,
        'num_read_ports': 1,
        'num_write_ports': 1,
        'sync_reset': True,  # 测试同步复位
        'reset_value': 0xFF,
        'byte_enable': True,  # 测试字节使能
        'implementation': 'always',
        'output': 'always_test_regfile.v',
        'gen_doc': True
    }
    
    generator = RegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)
    
    print(f"已生成 always 实现方式测试文件: {config['output']}")


def test_instance_implementation():
    """测试使用例化实现方式生成寄存器文件"""
    config = {
        'module_name': 'instance_test_regfile',
        'data_width': 32,
        'addr_width': 3,
        'num_read_ports': 2,
        'num_write_ports': 1,
        'sync_reset': False,  # 测试异步复位
        'reset_value': 0,
        'byte_enable': False,
        'implementation': 'instance',
        'default_reg_type': 'ReadWrite',
        'registers': [
            {
                'name': 'VERSION',
                'address': 0,
                'width': 32,
                'type': 'ReadOnly',
                'reset_value': 0x00010001,
                'description': '版本寄存器'
            },
            {
                'name': 'CONTROL',
                'address': 4,
                'width': 32,
                'type': 'ReadWrite',
                'reset_value': 0,
                'description': '控制寄存器'
            },
            {
                'name': 'IRQ_ENABLE',
                'address': 8,
                'width': 32,
                'type': 'ReadWrite',
                'reset_value': 0,
                'description': '中断使能寄存器'
            },
            {
                'name': 'IRQ_STATUS',
                'address': 12,
                'width': 32,
                'type': 'Write1Clean',
                'reset_value': 0,
                'description': '中断状态寄存器，写1清零'
            },
            {
                'name': 'IRQ_RAW',
                'address': 16,
                'width': 32,
                'type': 'ReadClean',
                'reset_value': 0,
                'description': '原始中断状态，读取后清零'
            }
        ],
        'output': 'instance_test_regfile.v',
        'gen_header': True,
        'gen_doc': True
    }
    
    generator = RegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)
    
    print(f"已生成 instance 实现方式测试文件: {config['output']}")


def test_all_register_types():
    """测试所有支持的寄存器类型"""
    # 获取所有支持的寄存器类型
    reg_type_manager = RegisterTypeManager()
    reg_types = reg_type_manager.get_all_register_types()
    
    # 创建测试配置
    registers = []
    addr = 0
    
    for reg_type in reg_types:
        registers.append({
            'name': f"{reg_type}_REG",
            'address': addr,
            'width': 32,
            'type': reg_type,
            'reset_value': 0,
            'description': f"{reg_type}类型寄存器测试"
        })
        addr += 4
    
    config = {
        'module_name': 'all_types_test_regfile',
        'data_width': 32,
        'addr_width': 8,  # 足够大的地址空间
        'num_read_ports': 1,
        'num_write_ports': 1,
        'sync_reset': False,
        'reset_value': 0,
        'byte_enable': False,
        'implementation': 'instance',
        'registers': registers,
        'output': 'all_types_test_regfile.v',
        'gen_header': True,
        'gen_doc': True
    }
    
    generator = RegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)
    
    print(f"已生成所有寄存器类型测试文件: {config['output']}")
    print(f"测试了 {len(reg_types)} 种寄存器类型")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="测试寄存器文件生成器")
    parser.add_argument("--test", choices=["json", "always", "instance", "all_types", "all"], 
                       default="all", help="指定要运行的测试 (默认: 运行所有测试)")
    
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 切换到输出目录
    os.chdir(output_dir)
    
    if args.test in ["json", "all"]:
        test_with_json_config()
    
    if args.test in ["always", "all"]:
        test_always_block_implementation()
    
    if args.test in ["instance", "all"]:
        test_instance_implementation()
    
    if args.test in ["all_types", "all"]:
        test_all_register_types()


if __name__ == "__main__":
    main() 