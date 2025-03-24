#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel格式配置解析器

解析Excel格式的寄存器配置文件。
"""

import os
import pandas as pd
from typing import Dict, Any, List

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
                
            # 读取寄存器表
            registers = []
            try:
                reg_df = pd.read_excel(config_source, sheet_name='Registers')
                for _, row in reg_df.iterrows():
                    if pd.notna(row['name']):
                        reg = {
                            'name': str(row['name']).strip(),
                            'address': str(row['address']).strip()
                        }
                        
                        # 可选字段
                        if 'type' in reg_df.columns and pd.notna(row['type']):
                            reg['type'] = str(row['type']).strip()
                            
                        if 'reset_value' in reg_df.columns and pd.notna(row['reset_value']):
                            reg['reset_value'] = str(row['reset_value']).strip()
                            
                        if 'description' in reg_df.columns and pd.notna(row['description']):
                            reg['description'] = str(row['description']).strip()
                            
                        registers.append(reg)
            except ValueError:
                # Registers表可能不存在
                pass
                
            config['registers'] = registers
            
            # 读取字段表
            fields = []
            try:
                field_df = pd.read_excel(config_source, sheet_name='Fields')
                for _, row in field_df.iterrows():
                    if pd.notna(row['register']) and pd.notna(row['name']) and pd.notna(row['bit_range']):
                        field = {
                            'register': str(row['register']).strip(),
                            'name': str(row['name']).strip(),
                            'bit_range': str(row['bit_range']).strip()
                        }
                        
                        # 可选字段
                        if 'type' in field_df.columns and pd.notna(row['type']):
                            field['type'] = str(row['type']).strip()
                            
                        if 'reset_value' in field_df.columns and pd.notna(row['reset_value']):
                            field['reset_value'] = str(row['reset_value']).strip()
                            
                        if 'description' in field_df.columns and pd.notna(row['description']):
                            field['description'] = str(row['description']).strip()
                            
                        fields.append(field)
            except ValueError:
                # Fields表可能不存在
                pass
                
            if fields:
                config['fields'] = fields
            
            # 验证配置
            return ConfigParser.validate_config(config)
        except Exception as e:
            raise ValueError(f"解析Excel配置失败: {str(e)}")


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