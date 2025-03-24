#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的配置解析模块

负责解析不同格式的配置文件，支持从Excel, JSON, YAML等文件中加载寄存器配置。
"""

import os
import json
import yaml
import pandas as pd
from typing import Dict, Any, List, Optional


class ConfigParser:
    """配置文件解析器基类"""
    
    @staticmethod
    def parse_config_file(config_file: str) -> Dict[str, Any]:
        """
        解析配置文件
        
        参数:
            config_file: 配置文件路径
            
        返回:
            包含配置信息的字典
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        file_ext = os.path.splitext(config_file)[1].lower()
        
        try:
            if file_ext in ('.xls', '.xlsx'):
                return ExcelConfigParser.parse(config_file)
            
            with open(config_file, 'r', encoding='utf-8') as f:
                if file_ext == '.json':
                    return JsonConfigParser.parse(f.read())
                elif file_ext in ('.yml', '.yaml'):
                    return YamlConfigParser.parse(f.read())
                else:
                    raise ValueError(f"不支持的配置文件格式: {file_ext}")
        except Exception as e:
            raise RuntimeError(f"解析配置文件时出错: {str(e)}")


class JsonConfigParser:
    """JSON格式配置文件解析器"""
    
    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        """
        解析JSON配置内容
        
        参数:
            content: JSON格式的字符串内容
            
        返回:
            包含配置信息的字典
        """
        try:
            return json.loads(content)
        except Exception as e:
            raise ValueError(f"解析JSON配置内容时出错: {str(e)}")


class YamlConfigParser:
    """YAML格式配置文件解析器"""
    
    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        """
        解析YAML配置内容
        
        参数:
            content: YAML格式的字符串内容
            
        返回:
            包含配置信息的字典
        """
        try:
            return yaml.safe_load(content)
        except Exception as e:
            raise ValueError(f"解析YAML配置内容时出错: {str(e)}")


class ExcelConfigParser:
    """Excel格式配置文件解析器"""
    
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
                        if isinstance(param_value, str):
                            param_value = param_value.lower() in ("true", "yes", "1")
                        else:
                            param_value = bool(param_value)
                    elif param_name == "reset_value" and isinstance(param_value, str):
                        # 支持十六进制值
                        if param_value.startswith("0x"):
                            param_value = param_value
                        else:
                            try:
                                int(param_value, 0)  # 尝试解析数字
                                param_value = param_value
                            except ValueError:
                                pass  # 保持字符串
                    
                    config[param_name] = param_value
            
            # 读取寄存器定义表格
            registers_df = pd.read_excel(excel_file, sheet_name="Registers")
            registers = []
            
            # 解析寄存器定义
            for index, row in registers_df.iterrows():
                if pd.notna(row["Name"]):
                    # 处理地址值，支持十六进制
                    if isinstance(row["Address"], str):
                        address_value = int(row["Address"], 0)
                    else:
                        address_value = int(row["Address"])
                    
                    # 处理复位值，支持十六进制
                    if pd.notna(row["Reset Value"]):
                        if isinstance(row["Reset Value"], str) and row["Reset Value"].startswith("0x"):
                            reset_value = row["Reset Value"]
                        else:
                            reset_value = row["Reset Value"]
                    else:
                        reset_value = 0
                    
                    register = {
                        "name": row["Name"].strip(),
                        "address": address_value,
                        "width": int(row["Width"]) if pd.notna(row["Width"]) else config.get("data_width", 32),
                        "type": row["Type"].strip() if pd.notna(row["Type"]) else "ReadWrite",
                        "reset_value": reset_value,
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
                        # 处理复位值，支持十六进制
                        if pd.notna(row["Reset Value"]):
                            if isinstance(row["Reset Value"], str) and row["Reset Value"].startswith("0x"):
                                reset_value = row["Reset Value"]
                            else:
                                reset_value = row["Reset Value"]
                        else:
                            reset_value = 0
                        
                        field = {
                            "register": row["Register"].strip(),
                            "name": row["Name"].strip(),
                            "bit_range": row["Bit Range"].strip() if pd.notna(row["Bit Range"]) else "",
                            "type": row["Type"].strip() if pd.notna(row["Type"]) else "ReadWrite",
                            "reset_value": reset_value,
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


class CommandLineParser:
    """命令行参数解析器"""
    
    @staticmethod
    def parse_args_to_config(args) -> Dict[str, Any]:
        """
        将命令行参数转换为配置字典
        
        参数:
            args: 命令行参数对象
            
        返回:
            包含配置信息的字典
        """
        config = {
            'module_name': args.module,
            'data_width': args.data_width,
            'addr_width': args.addr_width,
            'num_write_ports': args.write_ports,
            'num_read_ports': args.read_ports,
            'sync_reset': args.sync_reset,
            'reset_value': args.reset_value,
            'byte_enable': args.byte_enable,
            'implementation': args.implementation,
            'default_reg_type': args.default_reg_type,
            'output': args.output,
            'gen_header': args.gen_header,
            'gen_doc': args.gen_doc,
        }
        
        if hasattr(args, 'header_output') and args.header_output:
            config['header_output'] = args.header_output
            
        if hasattr(args, 'doc_output') and args.doc_output:
            config['doc_output'] = args.doc_output
            
        if hasattr(args, 'output_dir') and args.output_dir:
            config['output_dir'] = args.output_dir
        
        return config


if __name__ == "__main__":
    # 测试代码
    try:
        # 测试JSON
        json_config = """
        {
            "module_name": "test_regfile",
            "data_width": 32,
            "addr_width": 8,
            "registers": [
                {
                    "name": "CTRL",
                    "address": "0x00",
                    "type": "ReadWrite"
                }
            ]
        }
        """
        json_result = JsonConfigParser.parse(json_config)
        print("JSON配置解析结果:")
        print(json_result)
        
        # 测试YAML
        yaml_config = """
        module_name: test_regfile
        data_width: 32
        addr_width: 8
        registers:
          - name: CTRL
            address: 0x00
            type: ReadWrite
        """
        yaml_result = YamlConfigParser.parse(yaml_config)
        print("\nYAML配置解析结果:")
        print(yaml_result)
        
        # 测试Excel
        excel_file = "example_config.xlsx"
        if os.path.exists(excel_file):
            excel_result = ExcelConfigParser.parse(excel_file)
            print("\nExcel配置解析结果:")
            print(excel_result)
        else:
            print(f"\nExcel文件不存在: {excel_file}")
    
    except Exception as e:
        print(f"错误: {str(e)}") 