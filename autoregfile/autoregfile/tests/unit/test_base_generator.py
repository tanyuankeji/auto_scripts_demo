#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
总线生成器基类单元测试

测试总线生成器基类的功能，包括配置处理、地址格式化等。
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from autoregfile.core.bus_generators.base_generator import BaseBusGenerator


class TestBaseGenerator(unittest.TestCase):
    """测试总线生成器基类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建测试配置
        self.config = {
            "module_name": "test_regfile",
            "data_width": 32,
            "addr_width": 8,
            "registers": [
                {
                    "name": "control",
                    "address": "0x00",
                    "description": "控制寄存器",
                    "fields": [
                        {
                            "name": "enable",
                            "bit_range": "0:0",
                            "access": "RW",
                            "reset_val": 0,
                            "description": "使能位"
                        },
                        {
                            "name": "status",
                            "bit_range": "1:1",
                            "access": "RO",
                            "reset_val": 0,
                            "description": "状态位"
                        }
                    ]
                },
                {
                    "name": "data",
                    "address": "0x04",
                    "description": "数据寄存器",
                    "bit_range": "7:0"
                }
            ]
        }
        
        # 创建临时测试目录
        self.test_dir = tempfile.mkdtemp()
        
        # 初始化基础生成器
        self.generator = BaseBusGenerator(self.config)
    
    def tearDown(self):
        """测试后清理工作"""
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_init(self):
        """测试初始化功能"""
        # 检查配置是否正确加载
        self.assertEqual(self.generator.module_name, "test_regfile")
        self.assertEqual(self.generator.data_width, 32)
        self.assertEqual(self.generator.addr_width, 8)
        self.assertEqual(len(self.generator.registers), 2)
    
    def test_format_address(self):
        """测试地址格式化功能"""
        # 测试十六进制字符串格式
        addr_hex = self.generator._format_address("0x10")
        self.assertEqual(addr_hex, "0x10")
        
        # 测试十进制整数格式
        addr_int = self.generator._format_address(16)
        self.assertEqual(addr_int, "0x10")
        
        # 测试十进制字符串格式
        addr_dec_str = self.generator._format_address("16")
        self.assertEqual(addr_dec_str, "0x10")
        
        # 测试0h格式
        addr_0h = self.generator._format_address("0h10")
        self.assertEqual(addr_0h, "0x10")
    
    def test_calculate_bit_width(self):
        """测试位宽计算功能"""
        # 测试字符串格式 "high:low"
        width_str = self.generator._calculate_bit_width("7:0")
        self.assertEqual(width_str, 8)
        
        # 测试字典格式 {"high": high, "low": low}
        width_dict = self.generator._calculate_bit_width({"high": 7, "low": 0})
        self.assertEqual(width_dict, 8)
        
        # 测试单比特整数格式
        width_int = self.generator._calculate_bit_width(7)
        self.assertEqual(width_int, 1)
    
    def test_sanitize_registers(self):
        """测试寄存器清理功能"""
        # 创建包含无效寄存器的配置
        invalid_config = {
            "registers": [
                {"name": "reg1", "address": "0x00"},  # 有效寄存器
                {},  # 无效：无名称
                {"address": "0x04"},  # 无效：无名称
                {"name": "reg3"}  # 有效：无地址但有名称
            ]
        }
        
        # 创建临时生成器处理无效配置
        temp_generator = BaseBusGenerator(invalid_config)
        
        # 检查寄存器清理结果
        self.assertEqual(len(temp_generator.registers), 2)  # 应只保留有名称的寄存器
        self.assertEqual(temp_generator.registers[0]["name"], "reg1")
        self.assertEqual(temp_generator.registers[1]["name"], "reg3")
    
    def test_prepare_context(self):
        """测试上下文准备功能"""
        # 获取渲染上下文
        context = self.generator._prepare_context()
        
        # 检查基本上下文信息
        self.assertEqual(context["module_name"], "test_regfile")
        self.assertEqual(context["data_width"], 32)
        self.assertEqual(context["addr_width"], 8)
        self.assertEqual(context["num_registers"], 2)
        self.assertEqual(context["has_registers"], True)
    
    def test_parse_bit_range(self):
        """测试位范围解析功能"""
        # 测试常规范围
        high, low = self.generator._parse_bit_range("7:0")
        self.assertEqual(high, 7)
        self.assertEqual(low, 0)
        
        # 测试单比特
        high, low = self.generator._parse_bit_range("3")
        self.assertEqual(high, 3)
        self.assertEqual(low, 3)
        
        # 测试空范围
        high, low = self.generator._parse_bit_range("")
        self.assertEqual(high, 0)
        self.assertEqual(low, 0)
        
        # 测试无效范围
        high, low = self.generator._parse_bit_range("invalid")
        self.assertEqual(high, 0)
        self.assertEqual(low, 0)


if __name__ == '__main__':
    unittest.main() 