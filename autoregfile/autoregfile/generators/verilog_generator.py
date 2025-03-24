#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog生成器

生成Verilog格式的寄存器文件。
"""

from typing import Dict, Any, List, Optional
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
        
        # 计算字节使能数量
        if context.get('byte_enable', False):
            context['num_bytes'] = context['data_width'] // 8
        
        return context


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