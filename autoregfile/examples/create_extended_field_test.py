#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建扩展字段属性测试Excel配置文件

此脚本创建一个测试Excel配置文件，包含扩展的字段属性：
1. 软件访问类型（READ_WRITE, READ, WRITE）
2. 硬件访问类型（READ, WRITE, READ_WRITE）
3. 字段锁定依赖关系
4. 魔术数字依赖关系
"""

import os
import pandas as pd
from pathlib import Path


def create_extended_field_test_excel(excel_file_path):
    """创建一个测试Excel配置文件，包含扩展的字段属性"""
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'extended_field_regfile', 32, 8, 'apb', 1, 2, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器和字段表格
    register_fields_data = {
        # 寄存器信息列
        'register_name': [
            'CTRL_REG', 'CTRL_REG', 'CTRL_REG',
            'STATUS_REG', 'STATUS_REG',
            'LOCK_REG', 'LOCK_REG',
            'MAGIC_REG', 'MAGIC_REG'
        ],
        'address': [
            '0x00', '', '',
            '0x04', '',
            '0x08', '',
            '0x0C', ''
        ],
        'register_type': [
            'ReadWrite', '', '',
            'ReadOnly', '',
            'ReadWrite', '',
            'ReadWrite', ''
        ],
        'register_reset_value': [
            '0x00000000', '', '',
            '0x00000000', '',
            '0x00000000', '',
            '0xDEADBEEF', ''
        ],
        'register_description': [
            '控制寄存器', '', '',
            '状态寄存器', '',
            '锁定寄存器', '',
            '魔术数字寄存器', ''
        ],
        'sw_access_type': [
            'READ_WRITE', '', '',
            'READ', '',
            'READ_WRITE', '',
            'READ_WRITE', ''
        ],
        'hw_access_type': [
            '', '', '',
            'WRITE', '',
            '', '',
            '', ''
        ],
        
        # 字段信息列
        'field_name': [
            '', 'ENABLE', 'START',
            '', 'BUSY',
            '', 'LOCK_BIT',
            '', 'MAGIC_VALUE'
        ],
        'bit_range': [
            '', '0', '1',
            '', '0',
            '', '0',
            '', '31:0'
        ],
        'field_type': [
            '', 'ReadWrite', 'ReadWrite',
            '', 'ReadOnly',
            '', 'ReadWrite',
            '', 'ReadWrite'
        ],
        'field_reset_value': [
            '', '0', '0',
            '', '0',
            '', '0',
            '', '0xDEADBEEF'
        ],
        'field_description': [
            '', '使能位', '启动位',
            '', '忙状态标志',
            '', '锁定位',
            '', '魔术数字值'
        ],
        'field_function': [
            '', '控制系统工作使能', '启动一次操作，需要验证魔术数字',
            '', '表示系统当前正在工作中',
            '', '锁定配置，防止意外修改',
            '', '用于授权访问的魔术数字'
        ],
        'field_sw_access_type': [
            '', 'READ_WRITE', 'WRITE',
            '', 'READ',
            '', 'READ_WRITE',
            '', 'READ_WRITE'
        ],
        'field_hw_access_type': [
            '', '', '',
            '', 'WRITE',
            '', '',
            '', ''
        ],
        # 这里添加锁定依赖和魔术数字依赖
        'field_lock_dependency': [
            '', 'LOCK_REG.LOCK_BIT', '',
            '', '',
            '', '',
            '', ''
        ],
        'magic_dependency': [
            '', '', 'MAGIC_REG',
            '', '',
            '', '',
            '', ''
        ]
    }
    
    register_fields_df = pd.DataFrame(register_fields_data)
    
    # 创建Excel文件
    with pd.ExcelWriter(excel_file_path) as writer:
        config_df.to_excel(writer, sheet_name='Config', index=False)
        register_fields_df.to_excel(writer, sheet_name='RegisterFields', index=False)
    
    print(f"已创建扩展字段属性测试Excel配置文件: {excel_file_path}")


def main():
    """主函数"""
    print("创建扩展字段属性测试Excel配置文件")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    excel_file = configs_dir / "extended_field_test.xlsx"
    
    # 创建测试Excel文件
    create_extended_field_test_excel(excel_file)
    print(f"\n成功创建扩展字段属性测试Excel文件: {excel_file}")


if __name__ == "__main__":
    main() 