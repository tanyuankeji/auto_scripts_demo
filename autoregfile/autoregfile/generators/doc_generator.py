#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档生成器

生成Markdown格式的寄存器文件文档。
"""

from typing import Dict, Any, List, Optional
import os
import re

from .base_generator import BaseGenerator


class DocGenerator(BaseGenerator):
    """文档生成器"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化文档生成器
        
        参数:
            templates_dir: 模板目录，如果为None则使用默认模板目录下的doc子目录
        """
        if templates_dir is None:
            # 获取默认模板目录
            import autoregfile
            pkg_dir = os.path.dirname(os.path.abspath(autoregfile.__file__))
            templates_dir = os.path.join(pkg_dir, 'templates', 'doc')
        
        super().__init__(templates_dir)
    
    def generate(self, config: Dict[str, Any]) -> str:
        """
        生成文档
        
        参数:
            config: 配置字典
            
        返回:
            生成的文档字符串
        """
        # 准备上下文
        context = self.prepare_context(config)
        
        # 获取模板
        template = self.env.get_template('regfile.md.j2')
        
        # 渲染模板
        return template.render(**context)
    
    def prepare_context(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备文档模板上下文
        
        参数:
            config: 配置字典
            
        返回:
            准备好的上下文字典
        """
        context = super().prepare_context(config)
        
        # 处理寄存器地址，确保地址格式正确
        if 'registers' in context:
            for reg in context['registers']:
                # 确保地址是整数或十六进制字符串
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
                else:
                    # 单个位，如 "0"
                    bit = int(bit_range)
                    field['msb'] = bit
                    field['lsb'] = bit
                    field['width'] = 1
        
        # 组织字段按寄存器分组
        register_fields = {}
        if 'fields' in context:
            for field in context['fields']:
                reg_name = field['register']
                if reg_name not in register_fields:
                    register_fields[reg_name] = []
                register_fields[reg_name].append(field)
        
        context['register_fields'] = register_fields
        
        # 添加内存映射
        if 'memory_map' in config:
            context['memory_map'] = config['memory_map']
        else:
            # 如果没有内存映射，生成一个简单的表格
            memory_map = "# 寄存器内存映射\n\n"
            memory_map += "| 地址 | 寄存器名 | 描述 | 类型 |\n"
            memory_map += "|------|----------|------|------|\n"
            
            if 'registers' in context:
                # 按地址排序寄存器
                for reg in sorted(context['registers'], key=lambda r: r['address_int'] if 'address_int' in r else (int(r['address'], 16) if isinstance(r['address'], str) and r['address'].startswith('0x') else int(r['address']))):
                    addr = reg.get('address_hex', reg['address'])
                    memory_map += f"| {addr} | {reg['name']} | {reg.get('description', '')} | {reg.get('type', 'ReadWrite')} |\n"
            
            context['memory_map'] = memory_map
        
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
    
    generator = DocGenerator()
    doc_content = generator.generate(test_config)
    print(doc_content) 