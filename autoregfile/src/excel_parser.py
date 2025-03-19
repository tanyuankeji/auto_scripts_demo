#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel配置文件解析模块

负责解析Excel格式的寄存器配置文件。
"""

import os
import pandas as pd
from typing import Dict, Any, List


class ExcelConfigParser:
    """Excel配置文件解析器"""
    
    @staticmethod
    def parse(excel_file: str) -> Dict[str, Any]:
        """
        解析Excel配置文件
        
        参数:
            excel_file: Excel文件路径
            
        返回:
            包含配置信息的字典
        """
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"Excel配置文件不存在: {excel_file}")
        
        try:
            # 读取基本配置表格
            config_df = pd.read_excel(excel_file, sheet_name="Config")
            config = {}
            
            # 解析基本配置
            for index, row in config_df.iterrows():
                if pd.notna(row["Parameter"]) and pd.notna(row["Value"]):
                    param_name = row["Parameter"].strip()
                    param_value = row["Value"]
                    
                    # 转换特定类型
                    if param_name in ["data_width", "addr_width", "num_read_ports", "num_write_ports"]:
                        param_value = int(param_value)
                    elif param_name in ["sync_reset", "byte_enable", "gen_header", "gen_doc"]:
                        param_value = bool(param_value)
                    
                    config[param_name] = param_value
            
            # 读取寄存器定义表格
            registers_df = pd.read_excel(excel_file, sheet_name="Registers")
            registers = []
            
            # 解析寄存器定义
            for index, row in registers_df.iterrows():
                if pd.notna(row["Name"]):
                    register = {
                        "name": row["Name"].strip(),
                        "address": int(row["Address"], 0) if isinstance(row["Address"], str) else int(row["Address"]),
                        "width": int(row["Width"]) if pd.notna(row["Width"]) else config.get("data_width", 32),
                        "type": row["Type"].strip() if pd.notna(row["Type"]) else "ReadWrite",
                        "reset_value": row["Reset Value"] if pd.notna(row["Reset Value"]) else 0,
                        "description": row["Description"].strip() if pd.notna(row["Description"]) else ""
                    }
                    registers.append(register)
            
            # 添加寄存器定义到配置
            config["registers"] = registers
            
            # 读取字段定义表格（如果存在）
            try:
                fields_df = pd.read_excel(excel_file, sheet_name="Fields")
                fields = []
                
                # 解析字段定义
                for index, row in fields_df.iterrows():
                    if pd.notna(row["Register"]) and pd.notna(row["Name"]):
                        field = {
                            "register": row["Register"].strip(),
                            "name": row["Name"].strip(),
                            "bit_range": row["Bit Range"].strip() if pd.notna(row["Bit Range"]) else "",
                            "type": row["Type"].strip() if pd.notna(row["Type"]) else "ReadWrite",
                            "reset_value": row["Reset Value"] if pd.notna(row["Reset Value"]) else 0,
                            "description": row["Description"].strip() if pd.notna(row["Description"]) else ""
                        }
                        fields.append(field)
                
                # 添加字段定义到配置
                config["fields"] = fields
            except Exception as e:
                # 字段定义是可选的
                pass
            
            return config
        
        except Exception as e:
            raise RuntimeError(f"解析Excel配置文件时出错: {str(e)}")


if __name__ == "__main__":
    # 测试代码
    try:
        config = ExcelConfigParser.parse("example_config.xlsx")
        print("基本配置:")
        for key, value in config.items():
            if key not in ["registers", "fields"]:
                print(f"  {key}: {value}")
        
        print("\n寄存器定义:")
        for reg in config.get("registers", []):
            print(f"  {reg['name']} @ 0x{reg['address']:08X} 类型: {reg['type']}")
        
        if "fields" in config:
            print("\n字段定义:")
            for field in config["fields"]:
                print(f"  {field['register']}.{field['name']} {field['bit_range']} 类型: {field['type']}")
    except Exception as e:
        print(f"错误: {str(e)}")