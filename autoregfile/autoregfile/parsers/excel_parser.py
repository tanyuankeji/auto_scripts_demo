#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel格式配置解析器

解析Excel格式的寄存器配置文件。
支持四种Excel格式：
1. 原有单表格格式
2. 层次化设计（单表格，使用row_type区分寄存器和字段）
3. 多表分离设计（寄存器和字段分开存储在不同的表格中）
4. 改进层次化设计（单表格，使用register和field两列区分寄存器和字段）
"""

import os
import pandas as pd
from typing import Dict, Any, List, Optional

from .base_parser import ConfigParser


class ExcelParser(ConfigParser):
    """Excel格式配置解析器"""
    
    @staticmethod
    def parse(config_source: str) -> Dict[str, Any]:
        """
        解析Excel格式的配置
        
        参数:
            config_source: 配置源（Excel文件路径）
            
        返回:
            解析后的配置字典
        """
        if not os.path.isfile(config_source):
            raise ValueError(f"文件不存在: {config_source}")
        
        _, ext = os.path.splitext(config_source)
        if ext.lower() not in ['.xls', '.xlsx']:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        # 检测Excel文件格式
        excel_format = ExcelParser._detect_excel_format(config_source)
        
        if excel_format == 'hierarchical':
            return ExcelParser._parse_hierarchical_excel(config_source)
        elif excel_format == 'separated':
            return ExcelParser._parse_separated_excel(config_source)
        elif excel_format == 'improved_hierarchical':
            return ExcelParser._parse_improved_hierarchical_excel(config_source)
        else:
            # 默认使用原有格式解析
            return ExcelParser._parse_original_excel(config_source)
    
    @staticmethod
    def _detect_excel_format(excel_file: str) -> str:
        """
        检测Excel文件格式
        
        参数:
            excel_file: Excel文件路径
            
        返回:
            文件格式: 'hierarchical'、'separated'、'improved_hierarchical' 或 'original'
        """
        try:
            sheets = pd.ExcelFile(excel_file).sheet_names
            
            if 'Config' in sheets and 'RegisterFields' in sheets:
                # 读取RegisterFields表
                register_fields_df = pd.read_excel(excel_file, sheet_name='RegisterFields')
                
                # 检查是否包含改进的层次化设计所需的列
                columns = register_fields_df.columns.str.lower().tolist()
                if 'register' in columns and 'field' in columns:
                    print(f"检测到Excel格式: 改进的层次化设计")
                    return 'improved_hierarchical'  # 改进的层次化设计
                
                # 检查RegisterFields是否含有row_type列
                elif 'row_type' in register_fields_df.columns:
                    print(f"检测到Excel格式: 层次化设计")
                    return 'hierarchical'  # 层次化设计
                else:
                    print(f"检测到Excel格式: 原有单表格格式")
                    return 'original'  # 原有单表格格式
            
            elif 'Config' in sheets and 'Registers' in sheets and 'Fields' in sheets:
                print(f"检测到Excel格式: 多表分离设计")
                return 'separated'  # 多表分离设计
            
            else:
                print(f"检测到Excel格式: 原有单表格格式")
                return 'original'  # 默认使用原有格式
        
        except Exception as e:
            print(f"检测Excel格式时出错: {str(e)}")
            return 'original'  # 出错时默认使用原有格式
    
    @staticmethod
    def _parse_improved_hierarchical_excel(excel_file: str) -> Dict[str, Any]:
        """
        解析改进的层次化设计的Excel配置文件（使用register和field两列代替row_type）
        
        参数:
            excel_file: Excel文件路径
            
        返回:
            解析后的配置字典
        """
        print(f"解析改进的层次化设计Excel配置文件: {excel_file}")
        
        # 读取Excel文件的表格
        config_df = pd.read_excel(excel_file, sheet_name='Config')
        register_fields_df = pd.read_excel(excel_file, sheet_name='RegisterFields')
        
        # 创建列名的小写映射，以便大小写不敏感查找
        columns = {col.lower(): col for col in register_fields_df.columns}
        
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
            # 通过小写列名查找
            reg_col = columns.get('register')
            field_col = columns.get('field')
            addr_col = columns.get('address')
            bits_col = columns.get('bits')
            desc_col = columns.get('description')
            type_col = columns.get('type')
            reset_col = columns.get('reset_value')
            function_col = columns.get('function')
            sw_access_col = columns.get('sw_access')
            hw_access_col = columns.get('hw_access')
            lock_col = columns.get('lock')
            magic_col = columns.get('magic')
            
            # 判断是否为寄存器行（register列有值）
            if reg_col and pd.notna(row[reg_col]):
                # 添加上一个寄存器（如果存在）
                if current_register is not None:
                    registers.append(current_register)
                
                # 创建新寄存器
                current_register = {
                    'name': str(row[reg_col]).strip(),
                    'address': str(row[addr_col]).strip() if addr_col and pd.notna(row[addr_col]) else '0x0',
                    'type': str(row[type_col]).strip() if type_col and pd.notna(row[type_col]) else 'ReadWrite',
                    'reset_value': str(row[reset_col]).strip() if reset_col and pd.notna(row[reset_col]) else '0x0',
                    'description': str(row[desc_col]).strip() if desc_col and pd.notna(row[desc_col]) else ''
                }
                
                # 添加可选属性
                if sw_access_col and pd.notna(row[sw_access_col]):
                    current_register['sw_access_type'] = str(row[sw_access_col]).strip()
                
                if hw_access_col and pd.notna(row[hw_access_col]):
                    current_register['hw_access_type'] = str(row[hw_access_col]).strip()
                
                # 添加锁依赖和魔数依赖（如果有）
                if lock_col and pd.notna(row[lock_col]):
                    current_register['locked_by'] = [dep.strip() for dep in str(row[lock_col]).split(',')]
                
                if magic_col and pd.notna(row[magic_col]):
                    current_register['magic_dependency'] = [dep.strip() for dep in str(row[magic_col]).split(',')]
            
            # 判断是否为字段行（field列有值）
            if field_col and pd.notna(row[field_col]):
                if current_register is None:
                    raise ValueError(f"字段定义必须位于寄存器定义之后: {row[field_col]}")
                
                # 创建字段
                field = {
                    'register': current_register['name'],
                    'name': str(row[field_col]).strip(),
                    'bit_range': str(row[bits_col]).strip() if bits_col and pd.notna(row[bits_col]) else '0',
                    'description': str(row[desc_col]).strip() if desc_col and pd.notna(row[desc_col]) else ''
                }
                
                # 添加可选属性
                if type_col and pd.notna(row[type_col]):
                    field['type'] = str(row[type_col]).strip()
                
                if reset_col and pd.notna(row[reset_col]):
                    field['reset_value'] = str(row[reset_col]).strip()
                
                if function_col and pd.notna(row[function_col]):
                    field['function'] = str(row[function_col]).strip()
                
                if sw_access_col and pd.notna(row[sw_access_col]):
                    field['sw_access_type'] = str(row[sw_access_col]).strip()
                
                if hw_access_col and pd.notna(row[hw_access_col]):
                    field['hw_access_type'] = str(row[hw_access_col]).strip()
                
                # 添加锁依赖和魔数（如果有）
                if lock_col and pd.notna(row[lock_col]):
                    field['locked_by'] = [dep.strip() for dep in str(row[lock_col]).split(',')]
                
                if magic_col and pd.notna(row[magic_col]):
                    field['magic_number_dep'] = str(row[magic_col]).strip()
                    # 默认魔术数字值
                    magic_reg_name = field['magic_number_dep'].split('.')[0] if '.' in field['magic_number_dep'] else field['magic_number_dep']
                    magic_reg = next((r for r in registers if r['name'] == magic_reg_name), None)
                    if magic_reg and 'reset_value' in magic_reg:
                        field['magic_value'] = magic_reg['reset_value']
                    else:
                        field['magic_value'] = '0xDEADBEEF'
                
                fields.append(field)
        
        # 添加最后一个寄存器
        if current_register is not None:
            registers.append(current_register)
        
        # 组装最终配置
        config['registers'] = registers
        config['fields'] = fields
        
        return config
    
    @staticmethod
    def _parse_hierarchical_excel(excel_file: str) -> Dict[str, Any]:
        """
        解析层次化设计的Excel配置文件
        
        参数:
            excel_file: Excel文件路径
            
        返回:
            解析后的配置字典
        """
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
    
    @staticmethod
    def _parse_separated_excel(excel_file: str) -> Dict[str, Any]:
        """
        解析多表分离设计的Excel配置文件
        
        参数:
            excel_file: Excel文件路径
            
        返回:
            解析后的配置字典
        """
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
                if pd.notna(row.get('sw_access')):
                    register['sw_access_type'] = str(row['sw_access']).strip()
                
                if pd.notna(row.get('hw_access')):
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
                if pd.notna(row.get('type')):
                    field['type'] = str(row['type']).strip()
                
                if pd.notna(row.get('reset_value')):
                    field['reset_value'] = str(row['reset_value']).strip()
                
                if pd.notna(row.get('function')):
                    field['function'] = str(row['function']).strip()
                
                if pd.notna(row.get('sw_access')):
                    field['sw_access_type'] = str(row['sw_access']).strip()
                
                if pd.notna(row.get('hw_access')):
                    field['hw_access_type'] = str(row['hw_access']).strip()
                
                fields.append(field)
        
        # 组装最终配置
        config['registers'] = registers
        config['fields'] = fields
        
        return config
    
    @staticmethod
    def _parse_original_excel(config_source: str) -> Dict[str, Any]:
        """
        解析原有格式的Excel配置
        
        参数:
            config_source: 配置源（Excel文件路径）
            
        返回:
            解析后的配置字典
        """
        try:
            # 读取Excel文件的多个表格
            config = {}
            
            # 读取基本配置表
            try:
                config_df = pd.read_excel(config_source, sheet_name='Config')
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
            except ValueError:
                # Config表可能不存在
                pass
                
            # 尝试使用新的单表格方式读取寄存器和字段
            # 如果单表格存在，则使用它；否则，回退到旧的双表格方式
            registers = []
            fields = []
            
            try:
                # 新的单表格方式: 寄存器和字段在同一个表格
                reg_field_df = pd.read_excel(config_source, sheet_name='RegisterFields')
                
                # 验证必要的列存在
                required_reg_columns = ['register_name', 'address']
                required_field_columns = ['field_name', 'bit_range']
                
                missing_columns = []
                for col in required_reg_columns + required_field_columns:
                    if col not in reg_field_df.columns:
                        missing_columns.append(col)
                
                if missing_columns:
                    raise ValueError(f"RegisterFields表格缺少必要列: {', '.join(missing_columns)}")
                
                # 处理当前寄存器
                current_reg = None
                current_reg_name = None
                
                for idx, row in reg_field_df.iterrows():
                    # 判断是否为寄存器行（检查register_name字段是否存在，是否非空）
                    if 'register_name' in reg_field_df.columns and pd.notna(row.get('register_name')):
                        register_name = str(row['register_name']).strip()
                        
                        # 如果是新寄存器，则创建并添加
                        if register_name != current_reg_name:
                            if current_reg is not None:
                                registers.append(current_reg)
                            
                            # 创建新寄存器
                            current_reg = {
                                'name': register_name,
                                'address': str(row.get('address', '0x0')).strip()
                            }
                            
                            # 验证地址格式
                            try:
                                int(current_reg['address'], 0)  # 尝试将地址转换为整数
                            except ValueError:
                                raise ValueError(f"第{idx+2}行: 寄存器 '{register_name}' 的地址 '{current_reg['address']}' 格式无效")
                            
                            current_reg_name = register_name
                            
                            # 可选字段
                            if 'register_type' in reg_field_df.columns and pd.notna(row.get('register_type')):
                                current_reg['type'] = str(row['register_type']).strip()
                                
                            if 'register_reset_value' in reg_field_df.columns and pd.notna(row.get('register_reset_value')):
                                reset_value = str(row['register_reset_value']).strip()
                                # 验证复位值格式
                                try:
                                    if reset_value.startswith('0x'):
                                        int(reset_value, 16)
                                    else:
                                        # 尝试转换为整数，如果失败但是格式看起来像浮点数，则截断为整数
                                        try:
                                            int(reset_value, 0)
                                        except ValueError:
                                            # 可能是浮点数格式，尝试转换并截断
                                            try:
                                                float_val = float(reset_value)
                                                reset_value = str(int(float_val))
                                            except ValueError:
                                                raise ValueError(f"第{idx+2}行: 寄存器 '{register_name}' 的复位值 '{reset_value}' 格式无效")
                                except ValueError:
                                    raise ValueError(f"第{idx+2}行: 寄存器 '{register_name}' 的复位值 '{reset_value}' 格式无效")
                                current_reg['reset_value'] = reset_value
                                
                            if 'register_description' in reg_field_df.columns and pd.notna(row.get('register_description')):
                                current_reg['description'] = str(row['register_description']).strip()
                                
                            # 新增: 软件/硬件访问类型
                            if 'sw_access_type' in reg_field_df.columns and pd.notna(row.get('sw_access_type')):
                                sw_access = str(row['sw_access_type']).strip().upper()
                                if sw_access not in ['READ_WRITE', 'READ', 'WRITE']:
                                    print(f"警告: 第{idx+2}行: 寄存器 '{register_name}' 的软件访问类型 '{sw_access}' 无效，使用 'READ_WRITE' 替代")
                                    sw_access = 'READ_WRITE'
                                current_reg['sw_access_type'] = sw_access
                                
                            if 'hw_access_type' in reg_field_df.columns and pd.notna(row.get('hw_access_type')):
                                hw_access = str(row['hw_access_type']).strip().upper()
                                if hw_access not in ['READ_WRITE', 'READ', 'WRITE', '']:
                                    print(f"警告: 第{idx+2}行: 寄存器 '{register_name}' 的硬件访问类型 '{hw_access}' 无效，将被忽略")
                                    hw_access = ''
                                current_reg['hw_access_type'] = hw_access
                                
                            # 锁定依赖和魔术数字支持
                            if 'lock_dependency' in reg_field_df.columns and pd.notna(row.get('lock_dependency')):
                                current_reg['locked_by'] = [dep.strip() for dep in str(row['lock_dependency']).split(',')]
                                
                            if 'magic_dependency' in reg_field_df.columns and pd.notna(row.get('magic_dependency')):
                                current_reg['magic_dependency'] = [dep.strip() for dep in str(row['magic_dependency']).split(',')]
                    
                    # 处理字段行 (如果有field_name栏位)
                    if 'field_name' in reg_field_df.columns and pd.notna(row.get('field_name')):
                        if current_reg_name is None:
                            raise ValueError(f"第{idx+2}行: 字段定义必须位于寄存器定义之后")
                        
                        field_name = str(row['field_name']).strip()
                        bit_range = str(row.get('bit_range', '0')).strip()
                        
                        # 验证位范围格式
                        try:
                            if ':' in bit_range:
                                high, low = map(int, bit_range.split(':'))
                                if high < low:
                                    raise ValueError(f"第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的位范围 '{bit_range}' 无效，高位应大于等于低位")
                            else:
                                int(bit_range)  # 尝试将位值转换为整数
                        except ValueError as e:
                            if "高位应大于等于低位" in str(e):
                                raise e
                            raise ValueError(f"第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的位范围 '{bit_range}' 格式无效")
                        
                        field = {
                            'register': current_reg_name,
                            'name': field_name,
                            'bit_range': bit_range
                        }
                        
                        # 可选字段
                        if 'field_type' in reg_field_df.columns and pd.notna(row.get('field_type')):
                            field['type'] = str(row['field_type']).strip()
                            
                        if 'field_reset_value' in reg_field_df.columns and pd.notna(row.get('field_reset_value')):
                            reset_value = str(row['field_reset_value']).strip()
                            # 验证复位值格式
                            try:
                                if reset_value.startswith('0x'):
                                    int(reset_value, 16)
                                else:
                                    # 尝试转换为整数，如果失败但是格式看起来像浮点数，则截断为整数
                                    try:
                                        int(reset_value, 0)
                                    except ValueError:
                                        # 可能是浮点数格式，尝试转换并截断
                                        try:
                                            float_val = float(reset_value)
                                            reset_value = str(int(float_val))
                                        except ValueError:
                                            raise ValueError(f"第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的复位值 '{reset_value}' 格式无效")
                            except ValueError:
                                raise ValueError(f"第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的复位值 '{reset_value}' 格式无效")
                            field['reset_value'] = reset_value
                            
                        if 'field_description' in reg_field_df.columns and pd.notna(row.get('field_description')):
                            field['description'] = str(row['field_description']).strip()

                        # 新增: 软件/硬件访问类型 (字段级别)
                        if 'field_sw_access_type' in reg_field_df.columns and pd.notna(row.get('field_sw_access_type')):
                            sw_access = str(row['field_sw_access_type']).strip().upper()
                            if sw_access not in ['READ_WRITE', 'READ', 'WRITE']:
                                print(f"警告: 第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的软件访问类型 '{sw_access}' 无效，使用 'READ_WRITE' 替代")
                                sw_access = 'READ_WRITE'
                            field['sw_access_type'] = sw_access
                            
                        if 'field_hw_access_type' in reg_field_df.columns and pd.notna(row.get('field_hw_access_type')):
                            hw_access = str(row['field_hw_access_type']).strip().upper()
                            if hw_access not in ['READ_WRITE', 'READ', 'WRITE', '']:
                                print(f"警告: 第{idx+2}行: 字段 '{current_reg_name}.{field_name}' 的硬件访问类型 '{hw_access}' 无效，将被忽略")
                                hw_access = ''
                            field['hw_access_type'] = hw_access
                            
                        # 新增: 字段功能描述
                        if 'field_function' in reg_field_df.columns and pd.notna(row.get('field_function')):
                            field['function'] = str(row['field_function']).strip()
                            
                        # 锁定依赖
                        if 'field_lock_dependency' in reg_field_df.columns and pd.notna(row.get('field_lock_dependency')):
                            field['locked_by'] = [dep.strip() for dep in str(row['field_lock_dependency']).split(',')]
                        
                        # 魔术数字依赖
                        if 'magic_dependency' in reg_field_df.columns and pd.notna(row.get('magic_dependency')):
                            field['magic_number_dep'] = str(row['magic_dependency']).strip()
                            # 默认魔术数字值
                            magic_reg_name = field['magic_number_dep'].split('.')[0]
                            magic_reg = next((r for r in registers if r['name'] == magic_reg_name), None)
                            if magic_reg and 'reset_value' in magic_reg:
                                field['magic_value'] = magic_reg['reset_value']
                            else:
                                field['magic_value'] = '0xDEADBEEF'

                        fields.append(field)
                
                # 添加最后一个寄存器
                if current_reg is not None:
                    registers.append(current_reg)
                
            except ValueError as e:
                if "RegisterFields表格缺少必要列" in str(e):
                    # 旧的双表格方式: 寄存器和字段分开
                    try:
                        registers_df = pd.read_excel(config_source, sheet_name='Registers')
                        fields_df = pd.read_excel(config_source, sheet_name='Fields')
                        
                        # 处理寄存器
                        for idx, row in registers_df.iterrows():
                            if pd.notna(row.get('name')):
                                register = {
                                    'name': str(row['name']).strip(),
                                    'address': str(row.get('address', '0x0')).strip()
                                }
                                
                                # 验证地址格式
                                try:
                                    int(register['address'], 0)  # 尝试将地址转换为整数
                                except ValueError:
                                    raise ValueError(f"寄存器表第{idx+2}行: 寄存器 '{register['name']}' 的地址 '{register['address']}' 格式无效")
                                
                                # 可选字段
                                if pd.notna(row.get('type')):
                                    register['type'] = str(row['type']).strip()
                                
                                if pd.notna(row.get('reset_value')):
                                    reset_value = str(row['reset_value']).strip()
                                    # 验证复位值格式
                                    try:
                                        if reset_value.startswith('0x'):
                                            int(reset_value, 16)
                                        else:
                                            int(reset_value, 0)
                                    except ValueError:
                                        raise ValueError(f"寄存器表第{idx+2}行: 寄存器 '{register['name']}' 的复位值 '{reset_value}' 格式无效")
                                    register['reset_value'] = reset_value
                                
                                if pd.notna(row.get('description')):
                                    register['description'] = str(row['description']).strip()
                                
                                registers.append(register)
                        
                        # 处理字段
                        for idx, row in fields_df.iterrows():
                            if pd.notna(row.get('register')) and pd.notna(row.get('name')):
                                field = {
                                    'register': str(row['register']).strip(),
                                    'name': str(row['name']).strip(),
                                    'bit_range': str(row.get('bit_range', '0')).strip()
                                }
                                
                                # 验证位范围格式
                                try:
                                    if ':' in field['bit_range']:
                                        high, low = map(int, field['bit_range'].split(':'))
                                        if high < low:
                                            raise ValueError(f"字段表第{idx+2}行: 字段 '{field['register']}.{field['name']}' 的位范围 '{field['bit_range']}' 无效，高位应大于等于低位")
                                    else:
                                        int(field['bit_range'])  # 尝试将位值转换为整数
                                except ValueError as e:
                                    if "高位应大于等于低位" in str(e):
                                        raise e
                                    raise ValueError(f"字段表第{idx+2}行: 字段 '{field['register']}.{field['name']}' 的位范围 '{field['bit_range']}' 格式无效")
                                
                                # 可选字段
                                if pd.notna(row.get('type')):
                                    field['type'] = str(row['type']).strip()
                                
                                if pd.notna(row.get('reset_value')):
                                    reset_value = str(row['reset_value']).strip()
                                    # 验证复位值格式
                                    try:
                                        if reset_value.startswith('0x'):
                                            int(reset_value, 16)
                                        else:
                                            int(reset_value, 0)
                                    except ValueError:
                                        raise ValueError(f"字段表第{idx+2}行: 字段 '{field['register']}.{field['name']}' 的复位值 '{reset_value}' 格式无效")
                                    field['reset_value'] = reset_value
                                
                                if pd.notna(row.get('description')):
                                    field['description'] = str(row['description']).strip()
                                
                                fields.append(field)
                    
                    except Exception as e2:
                        raise ValueError(f"解析Excel格式失败: {str(e)}; 尝试旧格式也失败: {str(e2)}")
                else:
                    raise e
            
            # 组装最终配置
            config['registers'] = registers
            config['fields'] = fields
            
            return config
            
        except Exception as e:
            if "解析Excel格式失败" in str(e):
                raise e
            raise ValueError(f"解析Excel格式失败: {str(e)}")


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        parser = ExcelParser()
        config = parser.parse(sys.argv[1])
        print("从Excel文件解析的配置:")
        import json
        print(json.dumps(config, indent=2))
    else:
        print("用法: python excel_parser.py <excel_file>") 