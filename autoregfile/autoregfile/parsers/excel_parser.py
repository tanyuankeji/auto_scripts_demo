#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Excel解析器模块

实现对Excel格式配置文件的解析，支持多种Excel格式结构。
"""

import os
import copy
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Union, Tuple

from ..utils import get_logger
from .parser_base import ParserBase, ParserFactory


class ExcelParser(ParserBase):
    """
    Excel格式配置文件解析器
    
    支持多种Excel格式：
    1. 改进的层次结构设计（单工作表模式）
    2. 层次结构设计（单工作表模式）
    3. 分离式设计（多工作表模式）
    4. 原始设计（分离式多工作表模式）
    """
    
    def __init__(self):
        """初始化Excel解析器"""
        super().__init__()
        self.logger = get_logger("ExcelParser")
    
    def parse(self, config_file: str) -> Dict[str, Any]:
        """
        解析Excel配置文件
        
        Args:
            config_file: Excel配置文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info(f"开始解析Excel配置文件: {config_file}")
        
        # 检查文件是否存在
        if not os.path.exists(config_file):
            self.logger.error(f"配置文件不存在: {config_file}")
            return {}
        
        # 检测Excel格式
        excel_format = self._detect_excel_format(config_file)
        self.logger.info(f"检测到Excel格式: {excel_format}")
        
        # 根据格式解析Excel
        try:
            if excel_format == "improved_hierarchical":
                config = self._parse_improved_hierarchical_excel(config_file)
            elif excel_format == "hierarchical":
                config = self._parse_hierarchical_excel(config_file)
            elif excel_format == "separated":
                config = self._parse_separated_excel(config_file)
            elif excel_format == "original":
                config = self._parse_original_excel(config_file)
            else:
                self.logger.error(f"不支持的Excel格式: {excel_format}")
                return {}
                
            # 验证并修复配置
            validated_config = self.validate_config(config)
            self.logger.info(f"验证配置完成，包含 {len(validated_config.get('registers', []))} 个寄存器")
            
            return validated_config
            
        except Exception as e:
            self.logger.error(f"解析Excel配置文件失败: {str(e)}", exc_info=True)
            return {}
    
    def _detect_excel_format(self, excel_file: str) -> str:
        """
        检测Excel文件的格式
        
        Args:
            excel_file: Excel文件路径
            
        Returns:
            str: Excel格式类型，可能的值：
                - improved_hierarchical: 改进的层次结构设计
                - hierarchical: 层次结构设计
                - separated: 分离式设计
                - original: 原始设计
                - unknown: 未知格式
        """
        try:
            # 使用openpyxl引擎，这样不需要处理编码问题
            self.logger.info("使用openpyxl引擎检测Excel格式...")
            xl = pd.ExcelFile(excel_file, engine='openpyxl')
            sheet_names = xl.sheet_names
            
            # 检查是否包含RegisterFields表
            if "RegisterFields" in sheet_names:
                # 读取RegisterFields表
                df = pd.read_excel(excel_file, sheet_name="RegisterFields", engine='openpyxl', nrows=5)
                columns = [col.lower() for col in df.columns]
                
                # 改进的层次结构设计需要包含bits列
                if "bits" in columns:
                    return "improved_hierarchical"
                # 普通层次结构设计
                elif "register" in columns and "field" in columns and "address" in columns:
                    return "hierarchical"
                elif "row_type" in columns:
                    return "hierarchical"
            
            # 检查是否包含Registers和Fields表
            if "Registers" in sheet_names and "Fields" in sheet_names:
                return "separated"
            
            # 检查是否包含Headers表（原始设计）
            if "Headers" in sheet_names:
                return "original"
            
            # 默认为未知格式
            return "unknown"
            
        except Exception as e:
            self.logger.error(f"检测Excel格式失败: {str(e)}")
            return "unknown"
    
    def _parse_improved_hierarchical_excel(self, excel_file: str) -> Dict[str, Any]:
        """
        解析改进的层次结构Excel
        
        Args:
            excel_file: Excel文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info("使用改进的层次结构格式解析Excel")
        
        try:
            # 读取RegisterFields表
            df = pd.read_excel(excel_file, sheet_name="RegisterFields", engine='openpyxl')
            
            # 初始化配置
            config = copy.deepcopy(self.config)
            
            # 读取全局配置（如果存在）
            if "GlobalConfig" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="GlobalConfig", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            elif "Config" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="Config", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            
            # 处理寄存器和字段
            registers = []
            current_reg = None
            
            # 填充空白值
            df = df.fillna("")
            
            # 标准化列名（转为小写）
            df.columns = [col.lower() for col in df.columns]
            
            # 遍历每一行
            for _, row in df.iterrows():
                register_name = row.get("register", "")
                if isinstance(register_name, float) and pd.isna(register_name):
                    register_name = ""
                
                if not register_name:
                    continue
                
                # 如果当前行有地址，表示这是一个新寄存器
                address = row.get("address", "")
                if address:
                    # 如果存在当前处理的寄存器，保存它
                    if current_reg:
                        registers.append(current_reg)
                    
                    # 创建新寄存器
                    current_reg = {
                        "name": register_name,
                        "address": address,
                        "fields": []
                    }
                    
                    # 添加其他寄存器属性
                    if "type" in row and row["type"]:
                        current_reg["type"] = row["type"]
                    if "reset_value" in row and row["reset_value"]:
                        current_reg["reset_value"] = row["reset_value"]
                    if "description" in row and row["description"]:
                        current_reg["description"] = row["description"]
                    
                    # 处理位宽信息（针对无子字段寄存器）
                    if "bits" in row and row["bits"]:
                        current_reg["bits"] = row["bits"]
                    
                # 处理字段信息
                field_name = row.get("field", "")
                if isinstance(field_name, float) and pd.isna(field_name):
                    field_name = ""
                
                if field_name and current_reg:
                    field = {
                        "name": field_name
                    }
                    
                    # 获取位范围
                    if "bit_range" in row and row["bit_range"]:
                        field["bit_range"] = row["bit_range"]
                    elif "bits" in row and row["bits"]:
                        field["bit_range"] = row["bits"]
                    else:
                        self.logger.warning(f"寄存器 {register_name} 的字段 {field_name} 缺少位范围信息")
                        continue
                    
                    # 添加其他字段属性
                    if "type" in row and row["type"]:
                        field["type"] = row["type"]
                    if "reset_value" in row and row["reset_value"]:
                        field["reset_value"] = row["reset_value"]
                    if "description" in row and row["description"]:
                        field["description"] = row["description"]
                    
                    current_reg["fields"].append(field)
            
            # 保存最后一个寄存器
            if current_reg:
                registers.append(current_reg)
            
            # 更新配置
            config["registers"] = registers
            return config
            
        except Exception as e:
            self.logger.error(f"解析改进的层次结构Excel失败: {str(e)}", exc_info=True)
            return {}
    
    def _parse_hierarchical_excel(self, excel_file: str) -> Dict[str, Any]:
        """
        解析层次结构Excel
        
        Args:
            excel_file: Excel文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info("使用层次结构格式解析Excel")
        
        try:
            # 读取RegisterFields表
            df = pd.read_excel(excel_file, sheet_name="RegisterFields", engine='openpyxl')
            
            # 初始化配置
            config = copy.deepcopy(self.config)
            
            # 读取全局配置（如果存在）
            if "GlobalConfig" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="GlobalConfig", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            elif "Config" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="Config", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            
            # 处理寄存器和字段
            registers = []
            current_reg = None
            
            # 填充空白值
            df = df.fillna("")
            
            # 标准化列名（转为小写）
            df.columns = [col.lower() for col in df.columns]
            
            # 检查是否使用row_type列
            if "row_type" in df.columns:
                # 按row_type区分寄存器和字段
                for _, row in df.iterrows():
                    row_type = str(row.get("row_type", "")).strip().lower()
                    
                    if row_type == "register":
                        # 保存上一个寄存器
                        if current_reg:
                            registers.append(current_reg)
                        
                        # 创建新寄存器
                        current_reg = {
                            "name": row.get("name", ""),
                            "address": row.get("address", ""),
                            "fields": []
                        }
                        
                        # 添加其他寄存器属性
                        if "type" in row and row["type"]:
                            current_reg["type"] = row["type"]
                        if "reset_value" in row and row["reset_value"]:
                            current_reg["reset_value"] = row["reset_value"]
                        if "description" in row and row["description"]:
                            current_reg["description"] = row["description"]
                    
                    elif row_type == "field" and current_reg:
                        field = {
                            "name": row.get("name", ""),
                            "bit_range": row.get("bit_range", "")
                        }
                        
                        # 添加其他字段属性
                        if "type" in row and row["type"]:
                            field["type"] = row["type"]
                        if "reset_value" in row and row["reset_value"]:
                            field["reset_value"] = row["reset_value"]
                        if "description" in row and row["description"]:
                            field["description"] = row["description"]
                        
                        current_reg["fields"].append(field)
            else:
                # 遍历每一行，按register和field列区分
                for _, row in df.iterrows():
                    register_name = row.get("register", "")
                    if isinstance(register_name, float) and pd.isna(register_name):
                        register_name = ""
                    
                    if not register_name:
                        continue
                    
                    # 如果当前行有地址，表示这是一个新寄存器
                    address = row.get("address", "")
                    if address:
                        # 如果存在当前处理的寄存器，保存它
                        if current_reg:
                            registers.append(current_reg)
                        
                        # 创建新寄存器
                        current_reg = {
                            "name": register_name,
                            "address": address,
                            "fields": []
                        }
                        
                        # 添加其他寄存器属性
                        if "type" in row and row["type"]:
                            current_reg["type"] = row["type"]
                        if "reset_value" in row and row["reset_value"]:
                            current_reg["reset_value"] = row["reset_value"]
                        if "description" in row and row["description"]:
                            current_reg["description"] = row["description"]
                    
                    # 处理字段信息
                    field_name = row.get("field", "")
                    if isinstance(field_name, float) and pd.isna(field_name):
                        field_name = ""
                    
                    if field_name and current_reg:
                        field = {
                            "name": field_name,
                            "bit_range": row.get("bit_range", "")
                        }
                        
                        # 添加其他字段属性
                        if "type" in row and row["type"]:
                            field["type"] = row["type"]
                        if "reset_value" in row and row["reset_value"]:
                            field["reset_value"] = row["reset_value"]
                        if "description" in row and row["description"]:
                            field["description"] = row["description"]
                        
                        current_reg["fields"].append(field)
            
            # 保存最后一个寄存器
            if current_reg:
                registers.append(current_reg)
            
            # 更新配置
            config["registers"] = registers
            return config
            
        except Exception as e:
            self.logger.error(f"解析层次结构Excel失败: {str(e)}", exc_info=True)
            return {}
    
    def _parse_separated_excel(self, excel_file: str) -> Dict[str, Any]:
        """
        解析分离式Excel
        
        Args:
            excel_file: Excel文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info("使用分离式格式解析Excel")
        
        try:
            # 读取Registers和Fields表
            registers_df = pd.read_excel(excel_file, sheet_name="Registers", engine='openpyxl')
            fields_df = pd.read_excel(excel_file, sheet_name="Fields", engine='openpyxl')
            
            # 初始化配置
            config = copy.deepcopy(self.config)
            
            # 读取全局配置（如果存在）
            if "GlobalConfig" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="GlobalConfig", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            elif "Config" in pd.ExcelFile(excel_file).sheet_names:
                global_df = pd.read_excel(excel_file, sheet_name="Config", engine='openpyxl')
                if not global_df.empty:
                    self._parse_global_config(global_df, config)
            
            # 填充空白值
            registers_df = registers_df.fillna("")
            fields_df = fields_df.fillna("")
            
            # 标准化列名（转为小写）
            registers_df.columns = [col.lower() for col in registers_df.columns]
            fields_df.columns = [col.lower() for col in fields_df.columns]
            
            # 处理寄存器
            registers = []
            
            for _, reg_row in registers_df.iterrows():
                reg_name = reg_row.get("name", "")
                if isinstance(reg_name, float) and pd.isna(reg_name):
                    reg_name = ""
                
                if not reg_name:
                    continue
                
                # 创建寄存器
                register = {
                    "name": reg_name,
                    "address": reg_row.get("address", ""),
                    "fields": []
                }
                
                # 添加其他寄存器属性
                if "type" in reg_row and reg_row["type"]:
                    register["type"] = reg_row["type"]
                if "reset_value" in reg_row and reg_row["reset_value"]:
                    register["reset_value"] = reg_row["reset_value"]
                if "description" in reg_row and reg_row["description"]:
                    register["description"] = reg_row["description"]
                
                # 处理位宽信息（针对无子字段寄存器）
                if "bits" in reg_row and reg_row["bits"]:
                    register["bits"] = reg_row["bits"]
                
                # 查找该寄存器的所有字段
                reg_fields = fields_df[fields_df["register"].str.lower() == reg_name.lower()]
                
                for _, field_row in reg_fields.iterrows():
                    field_name = field_row.get("name", "")
                    if isinstance(field_name, float) and pd.isna(field_name):
                        field_name = ""
                    
                    if not field_name:
                        continue
                    
                    # 创建字段
                    field = {
                        "name": field_name,
                        "bit_range": field_row.get("bit_range", "")
                    }
                    
                    # 添加其他字段属性
                    if "type" in field_row and field_row["type"]:
                        field["type"] = field_row["type"]
                    if "reset_value" in field_row and field_row["reset_value"]:
                        field["reset_value"] = field_row["reset_value"]
                    if "description" in field_row and field_row["description"]:
                        field["description"] = field_row["description"]
                    
                    register["fields"].append(field)
                
                registers.append(register)
            
            # 更新配置
            config["registers"] = registers
            return config
            
        except Exception as e:
            self.logger.error(f"解析分离式Excel失败: {str(e)}", exc_info=True)
            return {}
    
    def _parse_original_excel(self, excel_file: str) -> Dict[str, Any]:
        """
        解析原始设计Excel
        
        Args:
            excel_file: Excel文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info("使用原始格式解析Excel")
        
        try:
            # 初始化配置
            config = copy.deepcopy(self.config)
            
            # 读取Headers表以获取全局配置
            headers_df = pd.read_excel(excel_file, sheet_name="Headers", engine='openpyxl')
            if not headers_df.empty:
                headers_df.columns = [col.lower() for col in headers_df.columns]
                for _, row in headers_df.iterrows():
                    key = row.get("key", "")
                    value = row.get("value", "")
                    if key == "module_name":
                        config["module_name"] = value
                    elif key == "bus_protocol":
                        config["bus_protocol"] = value
                    elif key == "addr_width":
                        try:
                            config["addr_width"] = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == "data_width":
                        try:
                            config["data_width"] = int(value)
                        except (ValueError, TypeError):
                            pass
            
            # 读取Registers表
            registers_df = pd.read_excel(excel_file, sheet_name="Registers", engine='openpyxl')
            registers_df.columns = [col.lower() for col in registers_df.columns]
            
            # 处理寄存器
            registers = []
            
            for _, reg_row in registers_df.iterrows():
                reg_name = reg_row.get("name", "")
                if isinstance(reg_name, float) and pd.isna(reg_name):
                    reg_name = ""
                
                if not reg_name:
                    continue
                
                # 创建寄存器
                register = {
                    "name": reg_name,
                    "address": reg_row.get("offset", ""),
                    "fields": []
                }
                
                # 添加其他寄存器属性
                if "access" in reg_row and reg_row["access"]:
                    register["type"] = self._map_access_to_type(reg_row["access"])
                if "reset" in reg_row and reg_row["reset"]:
                    register["reset_value"] = reg_row["reset"]
                if "description" in reg_row and reg_row["description"]:
                    register["description"] = reg_row["description"]
                
                # 检查是否有对应的子字段表
                sheet_names = pd.ExcelFile(excel_file).sheet_names
                if reg_name in sheet_names:
                    # 读取字段表
                    fields_df = pd.read_excel(excel_file, sheet_name=reg_name, engine='openpyxl')
                    fields_df.columns = [col.lower() for col in fields_df.columns]
                    
                    for _, field_row in fields_df.iterrows():
                        field_name = field_row.get("name", "")
                        if isinstance(field_name, float) and pd.isna(field_name):
                            field_name = ""
                        
                        if not field_name:
                            continue
                        
                        # 获取位范围
                        bit_high = field_row.get("bit_high", 0)
                        bit_low = field_row.get("bit_low", 0)
                        if bit_high == bit_low:
                            bit_range = f"{bit_high}"
                        else:
                            bit_range = f"{bit_high}:{bit_low}"
                        
                        # 创建字段
                        field = {
                            "name": field_name,
                            "bit_range": bit_range
                        }
                        
                        # 添加其他字段属性
                        if "access" in field_row and field_row["access"]:
                            field["type"] = self._map_access_to_type(field_row["access"])
                        if "reset" in field_row and field_row["reset"]:
                            field["reset_value"] = field_row["reset"]
                        if "description" in field_row and field_row["description"]:
                            field["description"] = field_row["description"]
                        
                        register["fields"].append(field)
                
                registers.append(register)
            
            # 更新配置
            config["registers"] = registers
            return config
            
        except Exception as e:
            self.logger.error(f"解析原始Excel失败: {str(e)}", exc_info=True)
            return {}
    
    def _parse_global_config(self, df: pd.DataFrame, config: Dict[str, Any]) -> None:
        """
        解析全局配置信息
        
        Args:
            df: 全局配置DataFrame
            config: 配置字典（会被修改）
        """
        # 标准化列名（转为小写）
        df.columns = [col.lower() for col in df.columns]
        
        # 尝试不同的列名格式
        key_col = next((c for c in ["key", "name", "parameter"] if c in df.columns), None)
        value_col = next((c for c in ["value", "setting"] if c in df.columns), None)
        
        if not key_col or not value_col:
            self.logger.warning("全局配置表格式不正确，找不到键值列")
            return
        
        for _, row in df.iterrows():
            key = row.get(key_col, "")
            value = row.get(value_col, "")
            
            if not key:
                continue
                
            key = str(key).lower()
            
            if key == "module_name":
                config["module_name"] = value
            elif key == "bus_protocol":
                config["bus_protocol"] = value
            elif key == "addr_width":
                try:
                    config["addr_width"] = int(value)
                except (ValueError, TypeError):
                    pass
            elif key == "data_width":
                try:
                    config["data_width"] = int(value)
                except (ValueError, TypeError):
                    pass
            
            # 处理总线选项
            elif key.startswith("bus_options."):
                option_key = key[len("bus_options."):]
                if "bus_options" not in config:
                    config["bus_options"] = {}
                
                # 处理子选项（如bus_options.apb.timeout_cycles）
                if "." in option_key:
                    bus_type, bus_option = option_key.split(".", 1)
                    if bus_type not in config["bus_options"]:
                        config["bus_options"][bus_type] = {}
                    config["bus_options"][bus_type][bus_option] = value
                else:
                    config["bus_options"][option_key] = value
    
    def _map_access_to_type(self, access: str) -> str:
        """
        将访问类型映射到寄存器类型
        
        Args:
            access: 访问类型字符串
            
        Returns:
            str: 对应的寄存器类型
        """
        access_map = {
            "RW": "ReadWrite",
            "RO": "ReadOnly",
            "WO": "WriteOnly",
            "RC": "ReadClean",
            "RS": "ReadSet",
            "W1C": "Write1Clean",
            "W1S": "Write1Set",
            "WP": "WritePulse",
            "W1P": "Write1Pulse",
            "WO1": "WriteOnce"
        }
        
        if isinstance(access, str):
            return access_map.get(access.upper(), "ReadWrite")
        return "ReadWrite"


# 注册Excel解析器
ParserFactory.register_parser("excel", ExcelParser) 