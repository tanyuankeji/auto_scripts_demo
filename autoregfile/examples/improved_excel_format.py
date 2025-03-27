#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进Excel格式的创建和解析

此脚本实现了三种改进的Excel格式：
1. 层次化设计：单表格，使用row_type区分寄存器和字段
2. 多表分离设计：将寄存器和字段分开存储在不同的表格中
3. 改进层次化设计：单表格，使用register和field两列区分寄存器和字段

这三种设计都旨在使Excel配置文件更加易于编写、查看和修改。
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


def create_hierarchical_excel(excel_file_path):
    """创建使用层次化设计的Excel配置文件"""
    print(f"创建层次化设计的Excel配置文件: {excel_file_path}")
    
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'hierarchical_regfile', 32, 8, 'apb', 1, 1, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器和字段数据（层次化设计）
    hierarchical_data = {
        'row_type': [],          # 行类型：Register 或 Field
        'name': [],              # 寄存器名或字段名
        'address_or_bits': [],   # 寄存器地址或字段位范围
        'type': [],              # 寄存器类型或字段类型
        'reset_value': [],       # 复位值
        'description': [],       # 描述
        'function': [],          # 功能说明（主要用于字段）
        'sw_access': [],         # 软件访问类型
        'hw_access': []          # 硬件访问类型
    }
    
    # 添加示例寄存器和字段
    # 1. 控制寄存器
    hierarchical_data['row_type'].append('Register')
    hierarchical_data['name'].append('CTRL_REG')
    hierarchical_data['address_or_bits'].append('0x00')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('控制寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    
    # CTRL_REG的字段
    # 1.1 使能位
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('ENABLE')
    hierarchical_data['address_or_bits'].append('0')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('使能位')
    hierarchical_data['function'].append('系统使能控制')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    
    # 1.2 模式字段
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('MODE')
    hierarchical_data['address_or_bits'].append('2:1')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('模式选择')
    hierarchical_data['function'].append('00=空闲, 01=低功耗, 10=正常, 11=高性能')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    
    # 1.3 启动位
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('START')
    hierarchical_data['address_or_bits'].append('3')
    hierarchical_data['type'].append('Write1Pulse')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('启动位')
    hierarchical_data['function'].append('写1开始一次操作')
    hierarchical_data['sw_access'].append('WRITE')
    hierarchical_data['hw_access'].append('')
    
    # 2. 状态寄存器
    hierarchical_data['row_type'].append('Register')
    hierarchical_data['name'].append('STATUS_REG')
    hierarchical_data['address_or_bits'].append('0x04')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('状态寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    
    # STATUS_REG的字段
    # 2.1 忙标志
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('BUSY')
    hierarchical_data['address_or_bits'].append('0')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('忙状态标志')
    hierarchical_data['function'].append('指示系统当前是否正在运行')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    
    # 2.2 错误标志
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('ERROR')
    hierarchical_data['address_or_bits'].append('1')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('错误标志')
    hierarchical_data['function'].append('指示系统是否发生错误')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    
    # 3. 中断标志寄存器
    hierarchical_data['row_type'].append('Register')
    hierarchical_data['name'].append('INT_FLAG_REG')
    hierarchical_data['address_or_bits'].append('0x08')
    hierarchical_data['type'].append('Write1Clear')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('中断标志寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('WRITE')
    
    # INT_FLAG_REG的字段
    # 3.1 数据就绪中断
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('DATA_READY')
    hierarchical_data['address_or_bits'].append('0')
    hierarchical_data['type'].append('Write1Clear')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('数据就绪中断')
    hierarchical_data['function'].append('数据准备就绪时置位，软件写1清零')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('WRITE')
    
    # 4. 测试各种寄存器类型
    # 4.1 WriteOnly寄存器
    hierarchical_data['row_type'].append('Register')
    hierarchical_data['name'].append('WRITEONLY_REG')
    hierarchical_data['address_or_bits'].append('0x0C')
    hierarchical_data['type'].append('WriteOnly')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('只写寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['sw_access'].append('WRITE')
    hierarchical_data['hw_access'].append('')
    
    # 4.2 Write1Set寄存器
    hierarchical_data['row_type'].append('Register')
    hierarchical_data['name'].append('WRITE1SET_REG')
    hierarchical_data['address_or_bits'].append('0x10')
    hierarchical_data['type'].append('Write1Set')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('写1置位寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    
    # WRITE1SET_REG的字段
    hierarchical_data['row_type'].append('Field')
    hierarchical_data['name'].append('BIT0')
    hierarchical_data['address_or_bits'].append('0')
    hierarchical_data['type'].append('Write1Set')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('写1置位的位字段')
    hierarchical_data['function'].append('软件写1置位此位')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    
    # 创建DataFrame
    hierarchical_df = pd.DataFrame(hierarchical_data)
    
    # 创建Excel文件
    try:
        with pd.ExcelWriter(excel_file_path) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            hierarchical_df.to_excel(writer, sheet_name='RegisterFields', index=False)
        print(f"成功创建层次化设计的Excel配置文件: {excel_file_path}")
        return True
    except Exception as e:
        print(f"创建Excel文件失败: {str(e)}")
        return False


def create_separated_excel(excel_file_path):
    """创建使用多表分离设计的Excel配置文件"""
    print(f"创建多表分离设计的Excel配置文件: {excel_file_path}")
    
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'separated_regfile', 32, 8, 'apb', 1, 1, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器数据（多表分离设计）
    registers_data = {
        'register_name': [
            'CTRL_REG', 'STATUS_REG', 'INT_FLAG_REG', 'WRITEONLY_REG', 'WRITE1SET_REG'
        ],
        'address': [
            '0x00', '0x04', '0x08', '0x0C', '0x10'
        ],
        'type': [
            'ReadWrite', 'ReadOnly', 'Write1Clear', 'WriteOnly', 'Write1Set'
        ],
        'reset_value': [
            '0x00000000', '0x00000000', '0x00000000', '0x00000000', '0x00000000'
        ],
        'description': [
            '控制寄存器', '状态寄存器', '中断标志寄存器', '只写寄存器', '写1置位寄存器'
        ],
        'sw_access': [
            'READ_WRITE', 'READ', 'READ_WRITE', 'WRITE', 'READ_WRITE'
        ],
        'hw_access': [
            '', 'WRITE', 'WRITE', '', ''
        ]
    }
    registers_df = pd.DataFrame(registers_data)
    
    # 字段数据（多表分离设计）
    fields_data = {
        'register_name': [
            'CTRL_REG', 'CTRL_REG', 'CTRL_REG',
            'STATUS_REG', 'STATUS_REG',
            'INT_FLAG_REG',
            'WRITE1SET_REG'
        ],
        'field_name': [
            'ENABLE', 'MODE', 'START',
            'BUSY', 'ERROR',
            'DATA_READY',
            'BIT0'
        ],
        'bit_range': [
            '0', '2:1', '3',
            '0', '1',
            '0',
            '0'
        ],
        'type': [
            'ReadWrite', 'ReadWrite', 'Write1Pulse',
            'ReadOnly', 'ReadOnly',
            'Write1Clear',
            'Write1Set'
        ],
        'reset_value': [
            '0', '0', '0',
            '0', '0',
            '0',
            '0'
        ],
        'description': [
            '使能位', '模式选择', '启动位',
            '忙状态标志', '错误标志',
            '数据就绪中断',
            '写1置位的位字段'
        ],
        'function': [
            '系统使能控制', '00=空闲, 01=低功耗, 10=正常, 11=高性能', '写1开始一次操作',
            '指示系统当前是否正在运行', '指示系统是否发生错误',
            '数据准备就绪时置位，软件写1清零',
            '软件写1置位此位'
        ],
        'sw_access': [
            'READ_WRITE', 'READ_WRITE', 'WRITE',
            'READ', 'READ',
            'READ_WRITE',
            'READ_WRITE'
        ],
        'hw_access': [
            '', '', '',
            'WRITE', 'WRITE',
            'WRITE',
            ''
        ]
    }
    fields_df = pd.DataFrame(fields_data)
    
    # 创建Excel文件
    try:
        with pd.ExcelWriter(excel_file_path) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            registers_df.to_excel(writer, sheet_name='Registers', index=False)
            fields_df.to_excel(writer, sheet_name='Fields', index=False)
        print(f"成功创建多表分离设计的Excel配置文件: {excel_file_path}")
        return True
    except Exception as e:
        print(f"创建Excel文件失败: {str(e)}")
        return False


def create_improved_hierarchical_excel(excel_file_path):
    """创建使用改进层次化设计的Excel配置文件（register和field两列）"""
    print(f"创建改进层次化设计的Excel配置文件: {excel_file_path}")
    
    # 全局配置
    config_data = {
        'parameter': [
            'module_name', 'data_width', 'addr_width', 'bus_protocol',
            'num_write_ports', 'num_read_ports', 'sync_reset', 'reset_value', 'byte_enable'
        ],
        'value': [
            'improved_hierarchical_regfile', 32, 8, 'apb', 1, 1, False, '0x00000000', True
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # 寄存器和字段数据（改进层次化设计）
    hierarchical_data = {
        'register': [],           # 寄存器名（只在寄存器行填写）
        'field': [],              # 字段名（只在字段行填写）
        'address': [],            # 寄存器地址（只在寄存器行填写）
        'bits': [],               # 字段位范围（只在字段行填写）
        'sw_access': [],          # 软件访问类型
        'hw_access': [],          # 硬件访问类型
        'type': [],               # 寄存器类型或字段类型
        'reset_value': [],        # 复位值
        'description': [],        # 描述
        'function': [],           # 功能说明（主要用于字段）
        'lock': [],               # 锁依赖
        'magic': []               # 魔数依赖
    }
    
    # 添加示例寄存器和字段
    # 1. 控制寄存器
    hierarchical_data['register'].append('CTRL_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x00')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('控制寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # CTRL_REG的字段
    # 1.1 使能位
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('ENABLE')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('0')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('使能位')
    hierarchical_data['function'].append('系统使能控制')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 1.2 模式字段
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('MODE')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('2:1')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('模式选择')
    hierarchical_data['function'].append('00=空闲, 01=低功耗, 10=正常, 11=高性能')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 1.3 启动位
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('START')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('3')
    hierarchical_data['sw_access'].append('WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('Write1Pulse')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('启动位')
    hierarchical_data['function'].append('写1开始一次操作')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 2. 状态寄存器
    hierarchical_data['register'].append('STATUS_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x04')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('状态寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # STATUS_REG的字段
    # 2.1 忙标志
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('BUSY')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('0')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('忙状态标志')
    hierarchical_data['function'].append('指示系统当前是否正在运行')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 2.2 错误标志
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('ERROR')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('1')
    hierarchical_data['sw_access'].append('READ')
    hierarchical_data['hw_access'].append('WRITE')
    hierarchical_data['type'].append('ReadOnly')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('错误标志')
    hierarchical_data['function'].append('指示系统是否发生错误')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 3. 中断标志寄存器
    hierarchical_data['register'].append('INT_FLAG_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x08')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('WRITE')
    hierarchical_data['type'].append('Write1Clear')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('中断标志寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # INT_FLAG_REG的字段
    # 3.1 数据就绪中断
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('DATA_READY')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('0')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('WRITE')
    hierarchical_data['type'].append('Write1Clear')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('数据就绪中断')
    hierarchical_data['function'].append('数据准备就绪时置位，软件写1清零')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 4. 测试各种寄存器类型
    # 4.1 WriteOnly寄存器
    hierarchical_data['register'].append('WRITEONLY_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x0C')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('WriteOnly')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('只写寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 4.2 Write1Set寄存器
    hierarchical_data['register'].append('WRITE1SET_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x10')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('Write1Set')
    hierarchical_data['reset_value'].append('0x00000000')
    hierarchical_data['description'].append('写1置位寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # WRITE1SET_REG的字段
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('BIT0')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('0')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('Write1Set')
    hierarchical_data['reset_value'].append('0')
    hierarchical_data['description'].append('写1置位的位字段')
    hierarchical_data['function'].append('软件写1置位此位')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # 5. 测试锁和魔数依赖
    hierarchical_data['register'].append('LOCK_TEST_REG')
    hierarchical_data['field'].append('')
    hierarchical_data['address'].append('0x14')
    hierarchical_data['bits'].append('')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0x12345678')
    hierarchical_data['description'].append('锁测试寄存器')
    hierarchical_data['function'].append('')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('')
    
    # LOCK_TEST_REG的字段 - 受CTRL_REG.ENABLE控制
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('LOCKED_FIELD')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('7:0')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0x55')
    hierarchical_data['description'].append('受锁控制的字段')
    hierarchical_data['function'].append('只有当CTRL_REG.ENABLE=1时才能修改')
    hierarchical_data['lock'].append('CTRL_REG.ENABLE')
    hierarchical_data['magic'].append('')
    
    # LOCK_TEST_REG的魔数字段 - 需要写入特定值
    hierarchical_data['register'].append('')
    hierarchical_data['field'].append('MAGIC_FIELD')
    hierarchical_data['address'].append('')
    hierarchical_data['bits'].append('15:8')
    hierarchical_data['sw_access'].append('READ_WRITE')
    hierarchical_data['hw_access'].append('')
    hierarchical_data['type'].append('ReadWrite')
    hierarchical_data['reset_value'].append('0xAA')
    hierarchical_data['description'].append('魔数控制的字段')
    hierarchical_data['function'].append('需要先向LOCK_TEST_REG写入0x12345678')
    hierarchical_data['lock'].append('')
    hierarchical_data['magic'].append('LOCK_TEST_REG')
    
    # 创建DataFrame
    hierarchical_df = pd.DataFrame(hierarchical_data)
    
    # 创建Excel文件
    try:
        with pd.ExcelWriter(excel_file_path) as writer:
            config_df.to_excel(writer, sheet_name='Config', index=False)
            hierarchical_df.to_excel(writer, sheet_name='RegisterFields', index=False)
        print(f"成功创建改进层次化设计的Excel配置文件: {excel_file_path}")
        return True
    except Exception as e:
        print(f"创建Excel文件失败: {str(e)}")
        return False


def parse_hierarchical_excel(excel_file):
    """解析层次化设计的Excel配置文件"""
    print(f"解析层次化设计的Excel配置文件: {excel_file}")
    
    # 读取Excel文件的表格
    config_df = pd.read_excel(excel_file, sheet_name='Config')
    register_fields_df = pd.read_excel(excel_file, sheet_name='RegisterFields')
    
    # 处理全局配置
    config = {}
    for _, row in config_df.iterrows():
        if pd.notna(row['parameter']) and pd.notna(row['value']):
            key = str(row['parameter']).strip()
            value = row['value']
            
            # 转换特定类型
            if key in ['data_width', 'addr_width', 'num_write_ports', 'num_read_ports']:
                value = int(value)
            elif key in ['sync_reset', 'byte_enable']:
                value = bool(value) if isinstance(value, (int, float)) else (value.lower() == 'true')
            
            config[key] = value
    
    # 处理寄存器和字段
    registers = []
    fields = []
    current_register = None
    
    for _, row in register_fields_df.iterrows():
        if pd.notna(row['row_type']):
            row_type = str(row['row_type']).strip()
            
            if row_type == 'Register':
                # 添加上一个寄存器（如果存在）
                if current_register is not None:
                    registers.append(current_register)
                
                # 创建新寄存器
                current_register = {
                    'name': str(row['name']).strip(),
                    'address': str(row['address_or_bits']).strip(),
                    'type': str(row['type']).strip() if pd.notna(row['type']) else 'ReadWrite',
                    'reset_value': str(row['reset_value']).strip() if pd.notna(row['reset_value']) else '0x0',
                    'description': str(row['description']).strip() if pd.notna(row['description']) else ''
                }
                
                # 添加可选属性
                if pd.notna(row['sw_access']):
                    current_register['sw_access_type'] = str(row['sw_access']).strip()
                
                if pd.notna(row['hw_access']):
                    current_register['hw_access_type'] = str(row['hw_access']).strip()
            
            elif row_type == 'Field' and current_register is not None:
                # 创建字段
                field = {
                    'register': current_register['name'],
                    'name': str(row['name']).strip(),
                    'bit_range': str(row['address_or_bits']).strip(),
                    'description': str(row['description']).strip() if pd.notna(row['description']) else ''
                }
                
                # 添加可选属性
                if pd.notna(row['type']):
                    field['type'] = str(row['type']).strip()
                
                if pd.notna(row['reset_value']):
                    field['reset_value'] = str(row['reset_value']).strip()
                
                if pd.notna(row['function']):
                    field['function'] = str(row['function']).strip()
                
                if pd.notna(row['sw_access']):
                    field['sw_access_type'] = str(row['sw_access']).strip()
                
                if pd.notna(row['hw_access']):
                    field['hw_access_type'] = str(row['hw_access']).strip()
                
                fields.append(field)
    
    # 添加最后一个寄存器
    if current_register is not None:
        registers.append(current_register)
    
    # 组装最终配置
    config['registers'] = registers
    config['fields'] = fields
    
    return config


def parse_separated_excel(excel_file):
    """解析多表分离设计的Excel配置文件"""
    print(f"解析多表分离设计的Excel配置文件: {excel_file}")
    
    # 读取Excel文件的表格
    config_df = pd.read_excel(excel_file, sheet_name='Config')
    registers_df = pd.read_excel(excel_file, sheet_name='Registers')
    fields_df = pd.read_excel(excel_file, sheet_name='Fields')
    
    # 处理全局配置
    config = {}
    for _, row in config_df.iterrows():
        if pd.notna(row['parameter']) and pd.notna(row['value']):
            key = str(row['parameter']).strip()
            value = row['value']
            
            # 转换特定类型
            if key in ['data_width', 'addr_width', 'num_write_ports', 'num_read_ports']:
                value = int(value)
            elif key in ['sync_reset', 'byte_enable']:
                value = bool(value) if isinstance(value, (int, float)) else (value.lower() == 'true')
            
            config[key] = value
    
    # 处理寄存器
    registers = []
    for _, row in registers_df.iterrows():
        if pd.notna(row['register_name']):
            register = {
                'name': str(row['register_name']).strip(),
                'address': str(row['address']).strip(),
                'type': str(row['type']).strip() if pd.notna(row['type']) else 'ReadWrite',
                'reset_value': str(row['reset_value']).strip() if pd.notna(row['reset_value']) else '0x0',
                'description': str(row['description']).strip() if pd.notna(row['description']) else ''
            }
            
            # 添加可选属性
            if pd.notna(row['sw_access']):
                register['sw_access_type'] = str(row['sw_access']).strip()
            
            if pd.notna(row['hw_access']):
                register['hw_access_type'] = str(row['hw_access']).strip()
            
            registers.append(register)
    
    # 处理字段
    fields = []
    for _, row in fields_df.iterrows():
        if pd.notna(row['field_name']) and pd.notna(row['register_name']):
            field = {
                'register': str(row['register_name']).strip(),
                'name': str(row['field_name']).strip(),
                'bit_range': str(row['bit_range']).strip(),
                'description': str(row['description']).strip() if pd.notna(row['description']) else ''
            }
            
            # 添加可选属性
            if pd.notna(row['type']):
                field['type'] = str(row['type']).strip()
            
            if pd.notna(row['reset_value']):
                field['reset_value'] = str(row['reset_value']).strip()
            
            if pd.notna(row['function']):
                field['function'] = str(row['function']).strip()
            
            if pd.notna(row['sw_access']):
                field['sw_access_type'] = str(row['sw_access']).strip()
            
            if pd.notna(row['hw_access']):
                field['hw_access_type'] = str(row['hw_access']).strip()
            
            fields.append(field)
    
    # 组装最终配置
    config['registers'] = registers
    config['fields'] = fields
    
    return config


def process_excel_file(excel_file, output_dir):
    """处理Excel文件，自动检测格式并生成代码"""
    # 判断Excel文件格式
    format_type = None
    sheets = pd.ExcelFile(excel_file).sheet_names
    
    if 'Config' in sheets and 'RegisterFields' in sheets:
        # 检查RegisterFields表格
        register_fields_df = pd.read_excel(excel_file, sheet_name='RegisterFields')
        columns = register_fields_df.columns.str.lower().tolist()
        
        # 检查是否包含改进的层次化设计所需的列
        if 'register' in columns and 'field' in columns:
            format_type = '改进的层次化设计'
            parser = ExcelParser()
            config = parser.parse(excel_file)
        
        # 检查RegisterFields是否含有row_type列
        elif 'row_type' in register_fields_df.columns:
            format_type = '层次化设计'
            config = parse_hierarchical_excel(excel_file)
        else:
            # 老的单表格格式，使用原有解析器
            format_type = '原有单表格格式'
            parser = ExcelParser()
            config = parser.parse(excel_file)
    
    elif 'Config' in sheets and 'Registers' in sheets and 'Fields' in sheets:
        format_type = '多表分离设计'
        config = parse_separated_excel(excel_file)
    
    else:
        raise ValueError(f"无法识别的Excel文件格式: {excel_file}")
    
    print(f"检测到Excel格式: {format_type}")
    
    # 提取模块名称作为文件名前缀
    module_name = config.get('module_name', 'regfile')
    
    # 输出文件路径
    verilog_file = os.path.join(output_dir, f"{module_name}.v")
    apb_file = os.path.join(output_dir, f"{module_name}_apb.v")
    header_file = os.path.join(output_dir, f"{module_name}.h")
    doc_file = os.path.join(output_dir, f"{module_name}.md")
    json_file = os.path.join(output_dir, f"{module_name}.json")
    
    # 保存为JSON格式（便于调试和查看）
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"已保存为JSON格式: {json_file}")
    
    # 生成Verilog文件
    print("生成Verilog文件...")
    verilog_gen = VerilogGenerator()
    verilog_code = verilog_gen.generate(config)
    verilog_gen.save(verilog_code, verilog_file)
    print(f"已生成Verilog文件: {verilog_file}")
    
    # 生成APB总线接口文件
    print("生成APB总线接口文件...")
    config['bus_protocol'] = 'apb'
    
    # 使用临时JSON文件
    temp_json = os.path.join(output_dir, "temp_apb_config.json")
    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 使用regfile_gen生成APB总线接口
    generate_regfile(temp_json, apb_file, False, 'apb')
    print(f"已生成APB总线接口文件: {apb_file}")
    
    # 清理临时文件
    os.remove(temp_json)
    
    # 生成C语言头文件
    print("生成C语言头文件...")
    header_gen = HeaderGenerator()
    header_code = header_gen.generate(config)
    header_gen.save(header_code, header_file)
    print(f"已生成C语言头文件: {header_file}")
    
    # 生成Markdown文档
    print("生成Markdown文档...")
    doc_gen = DocGenerator()
    doc_content = doc_gen.generate(config)
    doc_gen.save(doc_content, doc_file)
    print(f"已生成Markdown文档: {doc_file}")
    
    return True


def validate_hierarchical_design():
    """验证层次化设计生成的寄存器文件是否符合预期"""
    print("验证层次化设计生成的寄存器文件...")
    
    # 加载生成的JSON配置
    json_file = os.path.join(script_dir, 'output', 'hierarchical_regfile.json')
    if not os.path.exists(json_file):
        print(f"错误：找不到文件 {json_file}")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 验证全局配置
    if config.get('module_name') != 'hierarchical_regfile':
        print(f"错误：模块名称不匹配，期望 'hierarchical_regfile'，实际 '{config.get('module_name')}'")
        return False
    
    # 验证寄存器数量
    if len(config.get('registers', [])) != 5:
        print(f"错误：寄存器数量不匹配，期望 5，实际 {len(config.get('registers', []))}")
        return False
    
    # 验证字段数量
    if len(config.get('fields', [])) != 7:
        print(f"错误：字段数量不匹配，期望 7，实际 {len(config.get('fields', []))}")
        return False
    
    # 验证特定寄存器
    reg_names = [reg['name'] for reg in config.get('registers', [])]
    expected_regs = ['CTRL_REG', 'STATUS_REG', 'INT_FLAG_REG', 'WRITEONLY_REG', 'WRITE1SET_REG']
    for reg_name in expected_regs:
        if reg_name not in reg_names:
            print(f"错误：找不到寄存器 '{reg_name}'")
            return False
    
    # 验证特定字段
    field_names = [(field['register'], field['name']) for field in config.get('fields', [])]
    expected_fields = [
        ('CTRL_REG', 'ENABLE'),
        ('CTRL_REG', 'MODE'),
        ('CTRL_REG', 'START'),
        ('STATUS_REG', 'BUSY'),
        ('STATUS_REG', 'ERROR'),
        ('INT_FLAG_REG', 'DATA_READY'),
        ('WRITE1SET_REG', 'BIT0')
    ]
    for reg_name, field_name in expected_fields:
        if (reg_name, field_name) not in field_names:
            print(f"错误：找不到字段 '{reg_name}.{field_name}'")
            return False
    
    # 验证Verilog文件是否存在
    v_file = os.path.join(script_dir, 'output', 'hierarchical_regfile.v')
    if not os.path.exists(v_file):
        print(f"错误：找不到Verilog文件 {v_file}")
        return False
    
    # 验证APB文件是否存在
    apb_file = os.path.join(script_dir, 'output', 'hierarchical_regfile_apb.v')
    if not os.path.exists(apb_file):
        print(f"错误：找不到APB文件 {apb_file}")
        return False
    
    print("验证层次化设计成功！所有测试都通过了。")
    return True


def validate_separated_excel():
    """验证多表分离设计生成的寄存器文件是否符合预期"""
    print("验证多表分离设计生成的寄存器文件...")
    
    # 加载生成的JSON配置
    json_file = os.path.join(script_dir, 'output', 'separated_regfile.json')
    if not os.path.exists(json_file):
        print(f"错误：找不到文件 {json_file}")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 验证全局配置
    if config.get('module_name') != 'separated_regfile':
        print(f"错误：模块名称不匹配，期望 'separated_regfile'，实际 '{config.get('module_name')}'")
        return False
    
    # 验证寄存器数量
    if len(config.get('registers', [])) != 5:
        print(f"错误：寄存器数量不匹配，期望 5，实际 {len(config.get('registers', []))}")
        return False
    
    # 验证字段数量
    if len(config.get('fields', [])) != 7:
        print(f"错误：字段数量不匹配，期望 7，实际 {len(config.get('fields', []))}")
        return False
    
    # 验证特定寄存器
    reg_names = [reg['name'] for reg in config.get('registers', [])]
    expected_regs = ['CTRL_REG', 'STATUS_REG', 'INT_FLAG_REG', 'WRITEONLY_REG', 'WRITE1SET_REG']
    for reg_name in expected_regs:
        if reg_name not in reg_names:
            print(f"错误：找不到寄存器 '{reg_name}'")
            return False
    
    # 验证特定字段
    field_names = [(field['register'], field['name']) for field in config.get('fields', [])]
    expected_fields = [
        ('CTRL_REG', 'ENABLE'),
        ('CTRL_REG', 'MODE'),
        ('CTRL_REG', 'START'),
        ('STATUS_REG', 'BUSY'),
        ('STATUS_REG', 'ERROR'),
        ('INT_FLAG_REG', 'DATA_READY'),
        ('WRITE1SET_REG', 'BIT0')
    ]
    for reg_name, field_name in expected_fields:
        if (reg_name, field_name) not in field_names:
            print(f"错误：找不到字段 '{reg_name}.{field_name}'")
            return False
    
    # 验证Verilog文件是否存在
    v_file = os.path.join(script_dir, 'output', 'separated_regfile.v')
    if not os.path.exists(v_file):
        print(f"错误：找不到Verilog文件 {v_file}")
        return False
    
    # 验证APB文件是否存在
    apb_file = os.path.join(script_dir, 'output', 'separated_regfile_apb.v')
    if not os.path.exists(apb_file):
        print(f"错误：找不到APB文件 {apb_file}")
        return False
    
    print("验证多表分离设计成功！所有测试都通过了。")
    return True


def validate_improved_hierarchical_design():
    """验证改进层次化设计生成的寄存器文件是否符合预期"""
    print("验证改进层次化设计生成的寄存器文件...")
    
    # 加载生成的JSON配置
    json_file = os.path.join(script_dir, 'output', 'improved_hierarchical_regfile.json')
    if not os.path.exists(json_file):
        print(f"错误：找不到文件 {json_file}")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 验证全局配置
    if config.get('module_name') != 'improved_hierarchical_regfile':
        print(f"错误：模块名称不匹配，期望 'improved_hierarchical_regfile'，实际 '{config.get('module_name')}'")
        return False
    
    # 验证寄存器数量
    if len(config.get('registers', [])) != 6:
        print(f"错误：寄存器数量不匹配，期望 6，实际 {len(config.get('registers', []))}")
        return False
    
    # 验证字段数量
    if len(config.get('fields', [])) != 9:
        print(f"错误：字段数量不匹配，期望 9，实际 {len(config.get('fields', []))}")
        return False
    
    # 验证特定寄存器
    reg_names = [reg['name'] for reg in config.get('registers', [])]
    expected_regs = ['CTRL_REG', 'STATUS_REG', 'INT_FLAG_REG', 'WRITEONLY_REG', 'WRITE1SET_REG', 'LOCK_TEST_REG']
    for reg_name in expected_regs:
        if reg_name not in reg_names:
            print(f"错误：找不到寄存器 '{reg_name}'")
            return False
    
    # 验证特定字段
    field_names = [(field['register'], field['name']) for field in config.get('fields', [])]
    expected_fields = [
        ('CTRL_REG', 'ENABLE'),
        ('CTRL_REG', 'MODE'),
        ('CTRL_REG', 'START'),
        ('STATUS_REG', 'BUSY'),
        ('STATUS_REG', 'ERROR'),
        ('INT_FLAG_REG', 'DATA_READY'),
        ('WRITE1SET_REG', 'BIT0'),
        ('LOCK_TEST_REG', 'LOCKED_FIELD'),
        ('LOCK_TEST_REG', 'MAGIC_FIELD')
    ]
    for reg_name, field_name in expected_fields:
        if (reg_name, field_name) not in field_names:
            print(f"错误：找不到字段 '{reg_name}.{field_name}'")
            return False
    
    # 验证特殊字段属性
    # 验证锁依赖
    locked_field = next((field for field in config.get('fields', []) 
                          if field['register'] == 'LOCK_TEST_REG' and field['name'] == 'LOCKED_FIELD'), None)
    if not locked_field or 'locked_by' not in locked_field or 'CTRL_REG.ENABLE' not in locked_field['locked_by']:
        print("错误：LOCKED_FIELD的锁依赖缺失或不正确")
        return False
    
    # 验证魔数依赖
    magic_field = next((field for field in config.get('fields', []) 
                         if field['register'] == 'LOCK_TEST_REG' and field['name'] == 'MAGIC_FIELD'), None)
    if not magic_field or 'magic_number_dep' not in magic_field or magic_field['magic_number_dep'] != 'LOCK_TEST_REG':
        print("错误：MAGIC_FIELD的魔数依赖缺失或不正确")
        return False
    
    # 验证Verilog文件是否存在
    v_file = os.path.join(script_dir, 'output', 'improved_hierarchical_regfile.v')
    if not os.path.exists(v_file):
        print(f"错误：找不到Verilog文件 {v_file}")
        return False
    
    # 验证APB文件是否存在
    apb_file = os.path.join(script_dir, 'output', 'improved_hierarchical_regfile_apb.v')
    if not os.path.exists(apb_file):
        print(f"错误：找不到APB文件 {apb_file}")
        return False
    
    print("验证改进层次化设计成功！所有测试都通过了。")
    return True


def main():
    """主函数"""
    print("改进Excel格式的创建和解析")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 配置文件路径
    configs_dir = current_dir / "configs"
    os.makedirs(configs_dir, exist_ok=True)
    
    hierarchical_excel = configs_dir / "hierarchical_regfile.xlsx"
    separated_excel = configs_dir / "separated_regfile.xlsx"
    improved_hierarchical_excel = configs_dir / "improved_hierarchical_regfile.xlsx"
    
    # 输出目录
    output_dir = current_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 创建层次化设计的Excel文件
    if not create_hierarchical_excel(hierarchical_excel):
        return 1
    
    # 2. 创建多表分离设计的Excel文件
    if not create_separated_excel(separated_excel):
        return 1
    
    # 3. 创建改进层次化设计的Excel文件
    if not create_improved_hierarchical_excel(improved_hierarchical_excel):
        return 1
    
    # 4. 处理层次化设计的Excel文件
    print("\n===== 处理层次化设计的Excel文件 =====")
    if not process_excel_file(hierarchical_excel, output_dir):
        return 1
    
    # 5. 处理多表分离设计的Excel文件
    print("\n===== 处理多表分离设计的Excel文件 =====")
    if not process_excel_file(separated_excel, output_dir):
        return 1
    
    # 6. 处理改进层次化设计的Excel文件
    print("\n===== 处理改进层次化设计的Excel文件 =====")
    if not process_excel_file(improved_hierarchical_excel, output_dir):
        return 1
    
    # 7. 验证生成的寄存器文件
    print("\n===== 验证生成的寄存器文件 =====")
    hier_valid = validate_hierarchical_design()
    sep_valid = validate_separated_excel()
    imp_hier_valid = validate_improved_hierarchical_design()
    
    if hier_valid and sep_valid and imp_hier_valid:
        print("\n成功完成所有操作!")
    else:
        print("\n验证失败！请检查错误信息。")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 