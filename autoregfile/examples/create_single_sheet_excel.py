#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建单Sheet Excel配置文件示例

此脚本展示如何创建符合新的单表格格式要求的Excel配置文件，
包含软硬件访问类型和字段功能描述支持。
"""

import os
import pandas as pd
from pathlib import Path


def create_single_sheet_excel(excel_file_path):
    """创建一个示例Excel配置文件（单表格版本）"""
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'single_sheet_regfile', 32, 8, 'apb', 1, 2, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器和字段合并在一个表格中
    register_fields_data = {
        # 寄存器信息列
        'register_name': [
            'CTRL_REG', 'CTRL_REG', 'CTRL_REG', 'CTRL_REG',
            'STATUS_REG', 'STATUS_REG', 'STATUS_REG',
            'INT_FLAGS', 'INT_FLAGS',
            'INT_ENABLE', 'INT_ENABLE'
        ],
        'address': [
            '0x00', '', '', '',
            '0x04', '', '',
            '0x08', '',
            '0x0C', ''
        ],
        'register_type': [
            'ReadWrite', '', '', '',
            'ReadOnly', '', '',
            'Write1Clear', '',
            'ReadWrite', ''
        ],
        'register_reset_value': [
            '0x00000000', '', '', '',
            '0x00000000', '', '',
            '0x00000000', '',
            '0x00000000', ''
        ],
        'register_description': [
            '控制寄存器', '', '', '',
            '状态寄存器', '', '',
            '中断标志寄存器', '',
            '中断使能寄存器', ''
        ],
        'sw_access_type': [
            'READ_WRITE', '', '', '',
            'READ', '', '',
            'READ_WRITE', '',
            'READ_WRITE', ''
        ],
        'hw_access_type': [
            '', '', '', '',
            'WRITE', '', '',
            'WRITE', '',
            '', ''
        ],
        
        # 字段信息列
        'field_name': [
            '', 'ENABLE', 'MODE', 'START', 
            '', 'BUSY', 'ERROR',
            '', 'DATA_READY',
            '', 'DATA_READY_EN'
        ],
        'bit_range': [
            '', '0', '2:1', '3',
            '', '0', '1',
            '', '0',
            '', '0'
        ],
        'field_type': [
            '', 'ReadWrite', 'ReadWrite', 'ReadWrite',
            '', 'ReadOnly', 'ReadOnly',
            '', 'Write1Clear',
            '', 'ReadWrite'
        ],
        'field_reset_value': [
            '', '0', '0', '0',
            '', '0', '0',
            '', '0',
            '', '0'
        ],
        'field_description': [
            '', '使能位', '模式设置', '启动位',
            '', '忙状态标志', '错误标志',
            '', '数据就绪中断',
            '', '数据就绪中断使能'
        ],
        'field_function': [
            '', '控制系统工作使能', '选择工作模式: 00=空闲, 01=低功耗, 10=正常, 11=高性能', '写1启动一次操作',
            '', '表示系统当前正在工作中', '表示系统发生错误',
            '', '数据准备就绪',
            '', '使能数据就绪中断'
        ],
        'field_sw_access_type': [
            '', 'READ_WRITE', 'READ_WRITE', 'WRITE',
            '', 'READ', 'READ',
            '', 'READ_WRITE',
            '', 'READ_WRITE'
        ],
        'field_hw_access_type': [
            '', '', '', '',
            '', 'WRITE', 'WRITE',
            '', 'WRITE',
            '', ''
        ]
    }
    
    register_fields_df = pd.DataFrame(register_fields_data)
    
    # 创建Excel文件
    with pd.ExcelWriter(excel_file_path) as writer:
        config_df.to_excel(writer, sheet_name='Config', index=False)
        register_fields_df.to_excel(writer, sheet_name='RegisterFields', index=False)
    
    print(f"已创建示例Excel配置文件: {excel_file_path}")


def main():
    """主函数"""
    print("创建单表格Excel配置文件示例")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    excel_file = configs_dir / "single_sheet_example.xlsx"
    
    # 创建示例Excel文件
    create_single_sheet_excel(excel_file)
    print(f"\n成功创建单表格Excel示例文件: {excel_file}")


if __name__ == "__main__":
    main() 