#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线生成器基类模块

定义总线生成器的基础接口和共享功能，为不同类型的总线生成器提供统一的基础实现。
"""

import os
import re
import logging
import json
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime

from ...utils import get_logger, safe_write_file, ensure_dir_exists
from ..template_manager import get_template_manager
from ..bus_validator import validate_bus_protocol

logger = logging.getLogger(__name__)

class BaseBusGenerator:
    """
    总线生成器基类
    
    为所有总线生成器提供基础功能，包括配置处理、模板渲染和文件生成等。
    这是一个抽象基类，具体的总线生成器应该继承它并实现特定的方法。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化总线生成器
        
        Args:
            config: 寄存器配置字典
            template_dirs: 模板目录列表
        """
        self.logger = get_logger("BaseBusGenerator")
        self.config = config.copy() if config else {}
        self.template_dirs = template_dirs or []
        
        # 获取总线配置选项
        self.bus_options = self.config.get('bus_options', {})
        self.protocol_name = "base"  # 将在子类中覆盖
        
        # 设置模板管理器
        self.template_manager = get_template_manager(self.template_dirs)
        
        # 设置配置默认值
        self._set_config_defaults()
        
        # 清理配置，确保值的有效性
        self._cleanup_config()
        
        # 提取常用配置
        self.module_name = self.config.get("module_name", "regfile")
        self.data_width = self.config.get("data_width", 32)
        self.addr_width = self.config.get("addr_width", 8)
        self.registers = self.config.get("registers", [])
    
    def _set_config_defaults(self) -> None:
        """设置配置默认值"""
        defaults = {
            'data_width': 32,
            'addr_width': 8,
            'module_name': 'regfile',
            'bus_protocol': 'custom',
            'registers': []
        }
        
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
    
    def _cleanup_config(self) -> None:
        """
        清理配置，确保所有值的格式和类型正确
        
        这个方法会检查和修正配置中可能的问题，如地址格式、位宽等
        """
        # 确保数值参数是整数
        for param in ['data_width', 'addr_width']:
            try:
                self.config[param] = int(self.config[param])
            except (ValueError, TypeError):
                self.logger.warning(f"无效的{param}: {self.config[param]}，使用默认值")
                self.config[param] = 32 if param == 'data_width' else 8
        
        # 清理寄存器配置
        self._sanitize_registers()
    
    def _sanitize_registers(self) -> None:
        """
        清理寄存器配置，确保所有寄存器属性格式正确
        """
        sanitized_registers = []
        
        for reg in self.config.get('registers', []):
            try:
                # 跳过无名称的寄存器
                if 'name' not in reg or not reg['name']:
                    self.logger.warning("跳过无名称的寄存器")
                    continue
                
                # 创建寄存器的副本
                reg_copy = reg.copy()
                
                # 格式化地址
                if 'address' in reg_copy:
                    reg_copy['address'] = self._format_address(reg_copy['address'])
                
                # 处理位宽信息
                if 'bits' in reg_copy:
                    reg_copy['width'] = self._calculate_bit_width(reg_copy['bits'])
                elif 'bit_range' in reg_copy:
                    reg_copy['width'] = self._calculate_bit_width(reg_copy['bit_range'])
                else:
                    reg_copy['width'] = self.data_width
                
                # 处理字段
                has_fields = 'fields' in reg_copy and isinstance(reg_copy['fields'], list) and len(reg_copy['fields']) > 0
                reg_copy['has_fields'] = has_fields
                
                if has_fields:
                    sanitized_fields = []
                    for field in reg_copy['fields']:
                        field_copy = field.copy()
                        
                        # 确保字段有名称
                        if 'name' not in field_copy or not field_copy['name']:
                            self.logger.warning(f"寄存器 {reg_copy['name']} 中跳过无名称的字段")
                            continue
                        
                        # 处理位宽信息
                        if 'bit_range' in field_copy:
                            field_copy['width'] = self._calculate_bit_width(field_copy['bit_range'])
                        elif 'bits' in field_copy:
                            field_copy['bit_range'] = field_copy['bits']
                            field_copy['width'] = self._calculate_bit_width(field_copy['bits'])
                        
                        sanitized_fields.append(field_copy)
                    
                    reg_copy['fields'] = sanitized_fields
                
                # 添加到清理后的列表
                sanitized_registers.append(reg_copy)
                
            except Exception as e:
                self.logger.error(f"清理寄存器 {reg.get('name', 'unnamed')} 时出错: {str(e)}")
        
        self.config['registers'] = sanitized_registers
    
    def _format_address(self, address) -> str:
        """
        格式化地址为十六进制字符串
        
        Args:
            address: 地址值，可以是整数或字符串
            
        Returns:
            str: 格式化的十六进制地址
        """
        try:
            if isinstance(address, str):
                # 处理十六进制字符串
                if address.lower().startswith('0x'):
                    addr_int = int(address, 16)
                elif address.lower().startswith('0h'):
                    addr_int = int(address[2:], 16)
                else:
                    # 尝试作为十进制解析
                    addr_int = int(address)
            else:
                # 直接使用整数值
                addr_int = int(address)
            
            return f"0x{addr_int:X}"
        except (ValueError, TypeError) as e:
            self.logger.warning(f"无法格式化地址 '{address}': {str(e)}")
            return str(address)
    
    def _calculate_bit_width(self, bit_range: Union[str, Dict[str, int], int]) -> int:
        """
        计算位宽
        
        Args:
            bit_range: 位范围，可以是字符串(如"7:0")、字典(如{"high": 7, "low": 0})或整数
            
        Returns:
            int: 位宽
        """
        try:
            if isinstance(bit_range, dict):
                # 字典格式: {"high": high, "low": low}
                high = bit_range.get("high", 0)
                low = bit_range.get("low", 0)
                return high - low + 1
                
            elif isinstance(bit_range, str):
                # 字符串格式: "high:low"
                if ":" in bit_range:
                    parts = bit_range.split(":")
                    high = int(parts[0].strip())
                    low = int(parts[1].strip())
                    return high - low + 1
                else:
                    # 单比特: "bit"
                    return 1
                    
            elif isinstance(bit_range, int):
                # 整数格式: bit
                return 1
                
            else:
                # 默认宽度
                self.logger.warning(f"无法识别的位宽格式: {bit_range}，使用默认值1")
                return 1
                
        except Exception as e:
            self.logger.error(f"计算位宽时出错: {str(e)}")
            return 1
    
    def _get_template_path(self) -> Optional[str]:
        """
        获取模板路径
        
        默认情况下，使用基于协议名称的模板路径。子类可以覆盖此方法以提供自定义的模板路径。
        
        Returns:
            Optional[str]: 模板路径，如果找不到则返回None
        """
        # 检查是否在bus_options中指定了模板
        if self.protocol_name in self.bus_options:
            template_path = self.bus_options[self.protocol_name].get("template")
            if template_path:
                if os.path.isfile(template_path):
                    return template_path
                else:
                    # 尝试使用模板管理器查找
                    resolved_path = self.template_manager.find_template(template_path)
                    if resolved_path:
                        return resolved_path
        
        # 使用默认模板路径
        template_name = f"verilog/bus/{self.protocol_name}.v.j2"
        template_path = self.template_manager.find_template(template_name)
        
        if not template_path:
            self.logger.error(f"找不到{self.protocol_name}协议的模板")
            
        return template_path
    
    def _prepare_context(self) -> Dict[str, Any]:
        """
        准备渲染模板所需的上下文数据
        
        子类可以覆盖此方法以提供额外的上下文数据。
        
        Returns:
            Dict[str, Any]: 模板上下文数据
        """
        # 创建基本上下文
        context = {
            "module_name": self.module_name,
            "data_width": self.data_width,
            "addr_width": self.addr_width,
            "registers": self.registers,
            "bus_protocol": self.protocol_name,
            "bus_options": self.bus_options.get(self.protocol_name, {}),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "generator": f"{self.__class__.__name__} ({self.protocol_name})"
        }
        
        # 添加其他可能有用的信息
        context.update({
            "num_registers": len(self.registers),
            "has_registers": len(self.registers) > 0
        })
        
        return context
    
    def generate(self, output_file: str) -> bool:
        """
        生成总线接口寄存器文件
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            bool: 是否成功生成
        """
        try:
            # 获取模板路径
            template_path = self._get_template_path()
            if not template_path:
                self.logger.error(f"没有找到适用于 {self.protocol_name} 协议的模板")
                return False
            
            # 准备渲染上下文
            context = self._prepare_context()
            
            # 渲染模板
            self.logger.info(f"使用模板 {template_path} 生成寄存器文件")
            rendered_content = self.template_manager.render_template(template_path, context)
            
            if not rendered_content:
                self.logger.error("渲染模板失败")
                return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir and not ensure_dir_exists(output_dir):
                self.logger.error(f"无法创建输出目录: {output_dir}")
                return False
            
            # 写入输出文件
            if not safe_write_file(output_file, rendered_content):
                self.logger.error(f"写入文件失败: {output_file}")
                return False
            
            self.logger.info(f"成功生成寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"生成寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _validate_bus_protocol(self, expected_protocol: str) -> bool:
        """
        验证配置中的总线协议是否与预期的协议匹配。
        
        参数:
            expected_protocol: 预期的总线协议名称
            
        返回:
            bool: 如果匹配返回True，否则返回False
        """
        bus_protocol = self.config.get("bus_protocol", "").lower()
        
        if not bus_protocol:
            self.logger.error("No bus_protocol specified in configuration")
            return False
            
        if bus_protocol != expected_protocol:
            self.logger.warning(f"Expected bus protocol '{expected_protocol}', got '{bus_protocol}'")
            return False
            
        return True
    
    def _parse_bit_range(self, bit_range: str) -> Tuple[int, int]:
        """
        解析位范围
        
        参数:
            bit_range: 位范围字符串，如 "7:0" 或 "0"
            
        返回:
            (高位, 低位) 元组
        """
        if not bit_range:
            return (0, 0)
            
        bit_range = str(bit_range)
        
        if ':' in bit_range:
            parts = bit_range.split(':')
            if len(parts) == 2:
                try:
                    high = int(parts[0].strip())
                    low = int(parts[1].strip())
                    return (high, low)
                except (ValueError, TypeError):
                    return (0, 0)
        else:
            try:
                bit = int(bit_range.strip())
                return (bit, bit)
            except (ValueError, TypeError):
                return (0, 0)
        
        return (0, 0)
    
    def _validate_protocol(self) -> Dict[str, Any]:
        """
        验证总线协议配置
        
        返回:
            验证结果字典
        """
        return validate_bus_protocol(self.config, self.protocol_name) 