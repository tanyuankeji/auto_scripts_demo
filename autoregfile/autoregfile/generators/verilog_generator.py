#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog生成器

生成Verilog格式的寄存器文件。
"""

from typing import Dict, Any, List, Optional, Tuple
import os
import re

from ..core.register_types import get_register_type_manager
from .base_generator import BaseGenerator


class VerilogGenerator(BaseGenerator):
    """Verilog生成器"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化Verilog生成器
        
        参数:
            templates_dir: 模板目录，如果为None则使用默认模板目录下的verilog子目录
        """
        if templates_dir is None:
            # 获取默认模板目录
            import autoregfile
            pkg_dir = os.path.dirname(os.path.abspath(autoregfile.__file__))
            templates_dir = os.path.join(pkg_dir, 'templates', 'verilog')
        
        super().__init__(templates_dir)
        
        # 获取寄存器类型管理器
        self.reg_type_manager = get_register_type_manager()
    
    def generate(self, config: Dict[str, Any]) -> str:
        """
        生成Verilog代码
        
        参数:
            config: 配置字典
            
        返回:
            生成的Verilog代码字符串
        """
        # 准备上下文
        context = self.prepare_context(config)
        
        # 获取模板
        template = self.env.get_template('regfile.v.j2')
        
        # 渲染模板
        return template.render(**context)
    
    def prepare_context(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备Verilog模板上下文
        
        参数:
            config: 配置字典
            
        返回:
            准备好的上下文字典
        """
        context = super().prepare_context(config)
        
        # 检查是否存在脉冲寄存器类型
        has_pulse_registers = False
        # 检查是否存在锁定关系的寄存器
        has_locked_registers = False
        # 检查是否存在硬件接口的寄存器和字段
        has_hw_interfaces = False
        # 检查是否存在魔术数字依赖
        has_magic_deps = False
        
        # 处理寄存器类型信息
        if 'registers' in context:
            for reg in context['registers']:
                reg_type = reg.get('type', context.get('default_reg_type', 'ReadWrite'))
                try:
                    reg_type_obj = self.reg_type_manager.get_register_type(reg_type)
                    reg['type_info'] = {
                        'name': reg_type_obj.name,
                        'description': reg_type_obj.description,
                        'readable': reg_type_obj.readable,
                        'writable': reg_type_obj.writable,
                        'special_behaviors': reg_type_obj.special_behaviors
                    }
                    
                    # 检查是否为脉冲类型寄存器
                    if reg_type in ['Write1Pulse', 'Write0Pulse']:
                        has_pulse_registers = True
                    
                    # 检查是否存在锁定关系
                    if reg.get('locked_by') and len(reg['locked_by']) > 0:
                        has_locked_registers = True
                    
                    # 检查是否有硬件接口
                    if reg.get('hw_access_type') in ['READ', 'WRITE', 'READ_WRITE']:
                        has_hw_interfaces = True
                        
                    # 检查是否有魔术数字依赖
                    if reg.get('magic_dependency'):
                        has_magic_deps = True
                        
                except ValueError:
                    print(f"警告: 未知的寄存器类型 '{reg_type}'，使用 'ReadWrite' 替代")
                    reg['type'] = 'ReadWrite'
                    reg_type_obj = self.reg_type_manager.get_register_type('ReadWrite')
                    reg['type_info'] = {
                        'name': reg_type_obj.name,
                        'description': reg_type_obj.description,
                        'readable': reg_type_obj.readable,
                        'writable': reg_type_obj.writable,
                        'special_behaviors': reg_type_obj.special_behaviors
                    }
        
        # 处理字段类型和访问类型信息
        if 'fields' in context:
            for field in context['fields']:
                # 检查是否有硬件接口
                if field.get('hw_access_type') in ['READ', 'WRITE', 'READ_WRITE']:
                    has_hw_interfaces = True
                
                # 获取关联的寄存器
                register = next((r for r in context['registers'] if r['name'] == field['register']), None)
                if not register:
                    continue
                
                field_type = field.get('type', register.get('type', context.get('default_reg_type', 'ReadWrite')))
                try:
                    field_type_obj = self.reg_type_manager.get_register_type(field_type)
                    field['type_info'] = {
                        'name': field_type_obj.name,
                        'description': field_type_obj.description,
                        'readable': field_type_obj.readable,
                        'writable': field_type_obj.writable,
                        'special_behaviors': field_type_obj.special_behaviors
                    }
                except ValueError:
                    print(f"警告: 未知的字段类型 '{field_type}'，使用 'ReadWrite' 替代")
                    field['type'] = 'ReadWrite'
                    field_type_obj = self.reg_type_manager.get_register_type('ReadWrite')
                    field['type_info'] = {
                        'name': field_type_obj.name,
                        'description': field_type_obj.description,
                        'readable': field_type_obj.readable,
                        'writable': field_type_obj.writable,
                        'special_behaviors': field_type_obj.special_behaviors
                    }
                
                # 处理依赖关系
                if field.get('locked_by'):
                    has_locked_registers = True
                
                # 处理魔术数字依赖
                if field.get('magic_number_dep'):
                    has_magic_deps = True
                    field['has_magic_dep'] = True
                    # 确保魔术数字值是正确格式
                    if 'magic_value' in field:
                        magic_value = field['magic_value']
                        if isinstance(magic_value, str) and magic_value.startswith('0x'):
                            # 保持十六进制格式
                            pass
                        else:
                            # 转换为整数再转回字符串
                            field['magic_value'] = str(int(magic_value))
                    else:
                        field['magic_value'] = "0"
        
        # 设置脉冲寄存器标志
        context['has_pulse_registers'] = has_pulse_registers
        # 设置锁定寄存器标志
        context['has_locked_registers'] = has_locked_registers
        # 设置硬件接口标志
        context['has_hw_interfaces'] = has_hw_interfaces
        # 设置魔术数字依赖标志
        context['has_magic_deps'] = has_magic_deps
        
        # 计算字节使能数量
        if context.get('byte_enable', False):
            context['num_bytes'] = context['data_width'] // 8
        
        # 添加辅助函数到上下文
        context['get_bit_width'] = self.get_bit_width
        context['get_bit_range'] = self.get_bit_range
        context['get_field_reset_value'] = self.get_field_reset_value
        context['get_register_by_name'] = self.get_register_by_name
        context['max'] = max
        context['min'] = min
        
        return context
    
    @staticmethod
    def get_bit_width(bit_range: str) -> int:
        """
        获取位宽度
        
        参数:
            bit_range: 位范围字符串，如 "7:0" 或 "0"
            
        返回:
            位宽度
        """
        if ':' in bit_range:
            high, low = map(int, bit_range.split(':'))
            return high - low + 1
        else:
            return 1
    
    @staticmethod
    def get_bit_range(bit_range: str) -> Tuple[int, int]:
        """
        获取位范围
        
        参数:
            bit_range: 位范围字符串，如 "7:0" 或 "0"
            
        返回:
            (低位, 高位) 元组
        """
        if ':' in bit_range:
            high_str, low_str = bit_range.split(':')
            high = int(high_str.strip())
            low = int(low_str.strip())
            return low, high
        else:
            bit = int(bit_range.strip())
            return bit, bit
    
    @staticmethod
    def get_field_reset_value(reset_value: str, width: int) -> str:
        """
        获取字段复位值
        
        参数:
            reset_value: 复位值字符串，如 "0x3" 或 "0"
            width: 字段宽度
            
        返回:
            格式化后的复位值
        """
        # 如果reset_value是十六进制字符串
        if isinstance(reset_value, str) and reset_value.startswith('0x'):
            return reset_value
        # 如果是数字
        try:
            return str(int(reset_value))
        except:
            return f"0"
    
    @staticmethod
    def get_register_by_name(registers: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
        """
        根据名称获取寄存器
        
        参数:
            registers: 寄存器列表
            name: 寄存器名称
            
        返回:
            寄存器字典，如果未找到则返回空字典
        """
        for reg in registers:
            if reg['name'] == name:
                return reg
        return {}


# 测试代码
if __name__ == "__main__":
    import json
    import sys
    
    # 测试配置
    test_config = {
        "module_name": "test_regfile",
        "data_width": 32,
        "addr_width": 8,
        "num_write_ports": 1,
        "num_read_ports": 1,
        "registers": [
            {
                "name": "CTRL_REG",
                "address": "0x00",
                "type": "ReadWrite",
                "reset_value": "0x00000000",
                "description": "控制寄存器"
            },
            {
                "name": "STATUS_REG",
                "address": "0x04",
                "type": "ReadOnly",
                "reset_value": "0x00000000",
                "description": "状态寄存器"
            }
        ]
    }
    
    generator = VerilogGenerator()
    verilog_code = generator.generate(test_config)
    print(verilog_code) 