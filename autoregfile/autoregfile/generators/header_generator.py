#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C语言头文件生成器

生成C语言头文件，包含寄存器地址定义和位域定义。
"""

from typing import Dict, Any, List, Optional
import os
import re

from .base_generator import BaseGenerator


class HeaderGenerator(BaseGenerator):
    """C语言头文件生成器"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化C语言头文件生成器
        
        参数:
            templates_dir: 模板目录，如果为None则使用默认模板目录下的header子目录
        """
        if templates_dir is None:
            # 获取默认模板目录
            import autoregfile
            pkg_dir = os.path.dirname(os.path.abspath(autoregfile.__file__))
            templates_dir = os.path.join(pkg_dir, 'templates', 'header')
        
        super().__init__(templates_dir)
    
    def generate(self, config: Dict[str, Any]) -> str:
        """
        生成C语言头文件
        
        参数:
            config: 配置字典
            
        返回:
            生成的C语言头文件字符串
        """
        # 准备上下文
        context = self.prepare_context(config)
        
        # 获取模板
        template = self.env.get_template('regfile.h.j2')
        
        # 渲染模板
        return template.render(**context)
    
    def prepare_context(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备C语言头文件模板上下文
        
        参数:
            config: 配置字典
            
        返回:
            准备好的上下文字典
        """
        context = super().prepare_context(config)
        
        # 处理寄存器地址，确保地址格式正确
        if 'registers' in context:
            for reg in context['registers']:
                # 确保地址是整数格式
                if isinstance(reg['address'], str):
                    if reg['address'].startswith('0x'):
                        reg['address_hex'] = reg['address'].upper()
                        reg['address_int'] = int(reg['address'], 16)
                    else:
                        # 尝试解析为整数
                        try:
                            addr_int = int(reg['address'])
                            reg['address_int'] = addr_int
                            reg['address_hex'] = f"0x{addr_int:X}"
                        except ValueError:
                            print(f"警告: 无法解析寄存器地址: {reg['address']}")
                            reg['address_int'] = 0
                            reg['address_hex'] = "0x0"
                else:
                    # 已经是整数
                    reg['address_int'] = reg['address']
                    reg['address_hex'] = f"0x{reg['address']:X}"
        
        # 处理位域信息
        if 'fields' in context:
            for field in context['fields']:
                # 解析位域范围
                bit_range = field['bit_range']
                if ':' in bit_range:
                    # 范围格式，如 "7:0"
                    msb, lsb = map(int, bit_range.split(':'))
                    field['msb'] = msb
                    field['lsb'] = lsb
                    field['width'] = msb - lsb + 1
                    field['mask'] = ((1 << field['width']) - 1) << lsb
                else:
                    # 单个位，如 "0"
                    bit = int(bit_range)
                    field['msb'] = bit
                    field['lsb'] = bit
                    field['width'] = 1
                    field['mask'] = 1 << bit
        
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
        "registers": [
            {
                "name": "CTRL_REG",
                "address": "0x00",
                "type": "ReadWrite",
                "description": "控制寄存器"
            },
            {
                "name": "STATUS_REG",
                "address": "0x04",
                "type": "ReadOnly",
                "description": "状态寄存器"
            }
        ],
        "fields": [
            {
                "register": "CTRL_REG",
                "name": "ENABLE",
                "bit_range": "0",
                "description": "使能位"
            },
            {
                "register": "CTRL_REG",
                "name": "MODE",
                "bit_range": "2:1",
                "description": "模式选择"
            },
            {
                "register": "STATUS_REG",
                "name": "BUSY",
                "bit_range": "0",
                "description": "忙标志"
            }
        ]
    }
    
    generator = HeaderGenerator()
    header_code = generator.generate(test_config)
    print(header_code) 