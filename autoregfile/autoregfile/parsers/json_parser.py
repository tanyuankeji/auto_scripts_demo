#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSON格式配置解析器

解析JSON格式的寄存器配置文件。
"""

import os
import json
import copy
from typing import Dict, Any, List, Optional

from ..utils import get_logger
from .parser_base import ParserBase, ParserFactory


class JsonParser(ParserBase):
    """
    JSON格式配置解析器
    
    支持解析符合预定义结构的JSON格式配置文件
    """
    
    def __init__(self):
        """初始化JSON解析器"""
        super().__init__()
        self.logger = get_logger("JsonParser")
    
    def parse(self, config_file: str) -> Dict[str, Any]:
        """
        解析JSON配置文件
        
        Args:
            config_file: JSON配置文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        self.logger.info(f"开始解析JSON配置文件: {config_file}")
        
        # 检查文件是否存在
        if not os.path.exists(config_file):
            self.logger.error(f"配置文件不存在: {config_file}")
            return {}
        
        # 检查文件扩展名
        _, ext = os.path.splitext(config_file)
        if ext.lower() != '.json':
            self.logger.error(f"不支持的文件格式: {ext}，需要.json格式")
            return {}
        
        # 解析JSON文件
        try:
            # 尝试使用不同的编码打开文件
            try:
                # 首先尝试使用UTF-8编码
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except UnicodeDecodeError:
                # 如果UTF-8失败，尝试其他编码
                try:
                    self.logger.warning("UTF-8编码读取失败，尝试使用GBK编码...")
                    with open(config_file, 'r', encoding='gbk') as f:
                        config_data = json.load(f)
                except UnicodeDecodeError:
                    try:
                        self.logger.warning("GBK编码读取失败，尝试使用CP936编码...")
                        with open(config_file, 'r', encoding='cp936') as f:
                            config_data = json.load(f)
                    except UnicodeDecodeError:
                        try:
                            self.logger.warning("CP936编码读取失败，尝试使用latin-1编码...")
                            with open(config_file, 'r', encoding='latin-1') as f:
                                config_data = json.load(f)
                        except Exception as e:
                            self.logger.error(f"无法解析JSON文件: {str(e)}，请检查文件编码")
                            return {}
            
            # 合并默认配置与解析的配置
            config = copy.deepcopy(self.config)
            self._update_config(config, config_data)
            
            # 验证并修复配置
            validated_config = self.validate_config(config)
            self.logger.info(f"验证配置完成，包含 {len(validated_config.get('registers', []))} 个寄存器")
            
            return validated_config
            
        except Exception as e:
            self.logger.error(f"解析JSON配置文件失败: {str(e)}", exc_info=True)
            return {}
    
    def _update_config(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """
        更新配置，支持递归更新嵌套字典
        
        Args:
            target: 目标配置字典
            source: 源配置字典
        """
        for key, value in source.items():
            # 确保寄存器列表完整替换，而不是合并
            if key == "registers":
                target[key] = value
            # 处理嵌套字典
            elif isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._update_config(target[key], value)
            else:
                target[key] = value
    
    def _sanitize_register(self, register: Dict[str, Any]) -> Dict[str, Any]:
        """
        清理和规范化寄存器数据
        
        Args:
            register: 寄存器数据字典
            
        Returns:
            Dict[str, Any]: 清理后的寄存器数据
        """
        sanitized = copy.deepcopy(register)
        
        # 确保必要字段存在
        if "name" not in sanitized or not sanitized["name"]:
            self.logger.warning("寄存器缺少名称，将被跳过")
            return {}
        
        # 处理地址
        if "address" in sanitized:
            if isinstance(sanitized["address"], str):
                # 处理十六进制地址
                if sanitized["address"].startswith("0x") or sanitized["address"].startswith("0X"):
                    try:
                        sanitized["address"] = int(sanitized["address"], 16)
                    except ValueError:
                        self.logger.warning(f"寄存器 {sanitized['name']} 的地址格式无效: {sanitized['address']}")
                else:
                    try:
                        sanitized["address"] = int(sanitized["address"])
                    except ValueError:
                        self.logger.warning(f"寄存器 {sanitized['name']} 的地址格式无效: {sanitized['address']}")
        else:
            self.logger.warning(f"寄存器 {sanitized['name']} 缺少地址")
        
        # 确保字段列表存在
        if "fields" not in sanitized:
            sanitized["fields"] = []
        
        # 清理字段
        sanitized_fields = []
        for field in sanitized["fields"]:
            if "name" not in field or not field["name"]:
                self.logger.warning(f"寄存器 {sanitized['name']} 的字段缺少名称，将被跳过")
                continue
                
            if "bit_range" not in field:
                self.logger.warning(f"寄存器 {sanitized['name']} 的字段 {field['name']} 缺少bit_range")
                continue
                
            sanitized_fields.append(field)
        
        sanitized["fields"] = sanitized_fields
        
        return sanitized


# 注册JSON解析器
ParserFactory.register_parser("json", JsonParser)


# 测试代码
if __name__ == "__main__":
    # 从字符串解析
    json_str = """
    {
        "module_name": "test_regfile",
        "registers": [
            {
                "name": "CTRL_REG",
                "address": "0x00",
                "type": "ReadWrite"
            }
        ]
    }
    """
    
    parser = JsonParser()
    config = parser.parse(json_str)
    print("从字符串解析的配置:")
    print(json.dumps(config, indent=2)) 