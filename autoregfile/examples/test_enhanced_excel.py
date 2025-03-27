#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强的Excel解析功能

此脚本用于测试我们对Excel解析器的增强功能，包括：
- 单表格格式支持
- 数据验证和错误处理
- 软硬件访问类型和锁定/魔术数字依赖
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


def create_test_excel(excel_file_path):
    """创建一个测试用的Excel配置文件，包含各种增强功能"""
    print(f"开始创建测试Excel文件: {excel_file_path}")
    print(f"文件路径是否存在: {os.path.exists(os.path.dirname(excel_file_path))}")
    
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'enhanced_regfile', 32, 8, 'apb', 1, 2, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器和字段表格，包含增强功能
    register_fields_data = {
        # 寄存器信息列
        'register_name': [
            'CTRL_REG', 'CTRL_REG', 'CTRL_REG',
            'STATUS_REG', 'STATUS_REG',
            'LOCK_REG', 'LOCK_REG',
            'MAGIC_REG'
        ],
        'address': [
            '0x00', '', '',
            '0x04', '',
            '0x08', '',
            '0x0C'
        ],
        'register_type': [
            'ReadWrite', '', '',
            'ReadOnly', '',
            'ReadWrite', '',
            'ReadWrite'
        ],
        'register_reset_value': [
            '0x00000000', '', '',
            '0x00000000', '',
            '0x00000000', '',
            '0xDEADBEEF'
        ],
        'register_description': [
            '控制寄存器', '', '',
            '状态寄存器', '',
            '锁定寄存器', '',
            '魔术数字寄存器'
        ],
        'sw_access_type': [
            'READ_WRITE', '', '',
            'READ', '',
            'READ_WRITE', '',
            'READ_WRITE'
        ],
        'hw_access_type': [
            '', '', '',
            'WRITE', '',
            '', '',
            ''
        ],
        'lock_dependency': [
            '', '', '',
            '', '',
            '', '',
            'LOCK_REG.LOCK_BIT'  # 魔术数字寄存器依赖锁定位
        ],
        'magic_dependency': [
            '', '', 'MAGIC_REG',  # CTRL_REG的START字段依赖魔术数字
            '', '',
            '', '',
            ''
        ],
        
        # 字段信息列
        'field_name': [
            '', 'ENABLE', 'START',
            '', 'BUSY',
            '', 'LOCK_BIT',
            'MAGIC_VALUE'
        ],
        'bit_range': [
            '', '0', '1',
            '', '0',
            '', '0',
            '31:0'
        ],
        'field_type': [
            '', 'ReadWrite', 'ReadWrite',
            '', 'ReadOnly',
            '', 'ReadWrite',
            'ReadWrite'
        ],
        'field_reset_value': [
            '', '0', '0',
            '', '0',
            '', '0',
            '0xDEADBEEF'
        ],
        'field_description': [
            '', '使能位', '启动位',
            '', '忙状态标志',
            '', '锁定位',
            '魔术数字值'
        ],
        'field_function': [
            '', '控制系统工作使能', '启动一次操作，需要魔术数字',
            '', '表示系统当前正在工作中',
            '', '锁定配置，防止意外修改',
            '用于授权访问的魔术数字'
        ],
        'field_sw_access_type': [
            '', 'READ_WRITE', 'WRITE',
            '', 'READ',
            '', 'READ_WRITE',
            'READ_WRITE'
        ],
        'field_hw_access_type': [
            '', '', '',
            '', 'WRITE',
            '', '',
            ''
        ],
        'field_lock_dependency': [
            '', 'LOCK_REG.LOCK_BIT', '',  # ENABLE字段被LOCK_BIT锁定
            '', '',
            '', '',
            ''
        ]
    }
    
    register_fields_df = pd.DataFrame(register_fields_data)
    
    try:
        # 创建Excel文件
        with pd.ExcelWriter(excel_file_path) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            register_fields_df.to_excel(writer, sheet_name='RegisterFields', index=False)
        
        print(f"成功创建测试Excel配置文件: {excel_file_path}")
        print(f"文件是否存在: {os.path.exists(excel_file_path)}")
        print(f"文件大小: {os.path.getsize(excel_file_path) if os.path.exists(excel_file_path) else 0} 字节")
    except Exception as e:
        print(f"创建Excel文件失败: {str(e)}")
        import traceback
        traceback.print_exc()


def test_excel_parser():
    """测试增强的Excel解析器"""
    print("测试增强的Excel解析功能")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    print(f"当前目录: {current_dir}")
    
    # 配置文件路径
    test_dir = current_dir / "test"
    print(f"测试目录: {test_dir}")
    
    # 确保测试目录存在
    os.makedirs(test_dir, exist_ok=True)
    print(f"测试目录已创建: {os.path.exists(test_dir)}")
    
    excel_file = test_dir / "enhanced_excel_test.xlsx"
    print(f"Excel文件路径: {excel_file}")
    
    # 创建测试Excel文件
    create_test_excel(excel_file)
    
    # 检查文件是否已创建
    if not os.path.exists(excel_file):
        print(f"错误: Excel文件未能成功创建: {excel_file}")
        return 1
    
    # 解析Excel文件
    parser = ExcelParser()
    try:
        config = parser.parse(excel_file)
        print(f"\n成功解析Excel配置文件: {excel_file}")
        print(f"模块名称: {config.get('module_name')}")
        print(f"寄存器数量: {len(config.get('registers', []))}")
        print(f"字段数量: {len(config.get('fields', []))}")
        
        # 保存解析结果为JSON（便于查看）
        json_file = test_dir / "enhanced_excel_test.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"已将解析结果保存到: {json_file}")
        print(f"JSON文件是否存在: {os.path.exists(json_file)}")
        
        # 检查关键功能是否正确解析
        print("\n验证增强功能:")
        
        # 1. 检查软硬件访问类型
        print("1. 软硬件访问类型:")
        for reg in config.get('registers', []):
            sw_access = reg.get('sw_access_type', '')
            hw_access = reg.get('hw_access_type', '')
            if sw_access or hw_access:
                print(f"   寄存器 {reg['name']}: 软件访问={sw_access}, 硬件访问={hw_access}")
        
        for field in config.get('fields', []):
            sw_access = field.get('sw_access_type', '')
            hw_access = field.get('hw_access_type', '')
            if sw_access or hw_access:
                print(f"   字段 {field['register']}.{field['name']}: 软件访问={sw_access}, 硬件访问={hw_access}")
        
        # 2. 检查锁定依赖
        print("\n2. 锁定依赖:")
        for reg in config.get('registers', []):
            if 'locked_by' in reg:
                print(f"   寄存器 {reg['name']} 被 {reg['locked_by']} 锁定")
        
        for field in config.get('fields', []):
            if 'locked_by' in field:
                print(f"   字段 {field['register']}.{field['name']} 被 {field['locked_by']} 锁定")
        
        # 3. 检查魔术数字依赖
        print("\n3. 魔术数字依赖:")
        for reg in config.get('registers', []):
            if 'magic_dependency' in reg:
                print(f"   寄存器 {reg['name']} 依赖魔术数字 {reg['magic_dependency']}")
        
        for field in config.get('fields', []):
            reg = next((r for r in config.get('registers', []) if r['name'] == field['register']), None)
            if reg and 'magic_dependency' in reg:
                print(f"   字段 {field['register']}.{field['name']} 依赖魔术数字 {reg['magic_dependency']}")
        
        # 4. 检查字段功能描述
        print("\n4. 字段功能描述:")
        for field in config.get('fields', []):
            if 'function' in field:
                print(f"   字段 {field['register']}.{field['name']}: {field['function']}")
        
        print("\n增强功能测试成功!")
        return 0
    except Exception as e:
        print(f"解析Excel配置失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(test_excel_parser()) 