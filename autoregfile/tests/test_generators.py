#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码生成器测试模块
"""

import unittest
import sys
import os
import tempfile

# 添加项目根目录到PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoregfile.generators.verilog_generator import VerilogGenerator
from autoregfile.generators.header_generator import HeaderGenerator
from autoregfile.generators.doc_generator import DocGenerator


class TestGenerators(unittest.TestCase):
    """生成器测试类"""
    
    def setUp(self):
        """准备测试数据"""
        self.test_config = {
            "module_name": "test_gen",
            "data_width": 32,
            "addr_width": 8,
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
            ],
            "fields": [
                {
                    "register": "CTRL_REG",
                    "name": "ENABLE",
                    "bit_range": "0",
                    "description": "使能位"
                },
                {
                    "register": "STATUS_REG",
                    "name": "BUSY",
                    "bit_range": "0",
                    "description": "忙标志"
                }
            ]
        }
    
    def test_verilog_generator(self):
        """测试Verilog生成器"""
        # 生成Verilog代码
        generator = VerilogGenerator()
        verilog_code = generator.generate(self.test_config)
        
        # 检查生成的代码
        self.assertIn("module test_gen", verilog_code)
        self.assertIn("ADDR_CTRL_REG", verilog_code)
        self.assertIn("ADDR_STATUS_REG", verilog_code)
        self.assertIn("ctrl_reg_reg", verilog_code)
        self.assertIn("status_reg_reg", verilog_code)
        
        # 测试保存到文件
        with tempfile.NamedTemporaryFile(suffix='.v', delete=False) as f:
            generator.save(verilog_code, f.name)
            self.assertTrue(os.path.exists(f.name))
            with open(f.name, 'r') as f2:
                saved_code = f2.read()
                self.assertEqual(saved_code, verilog_code)
            
        # 删除临时文件
        os.unlink(f.name)
    
    def test_header_generator(self):
        """测试头文件生成器"""
        # 生成头文件代码
        generator = HeaderGenerator()
        header_code = generator.generate(self.test_config)
        
        # 检查生成的代码
        self.assertIn("TEST_GEN_H", header_code)
        self.assertIn("TEST_GEN_CTRL_REG_ADDR", header_code)
        self.assertIn("TEST_GEN_STATUS_REG_ADDR", header_code)
        self.assertIn("TEST_GEN_CTRL_REG_ENABLE_MASK", header_code)
        self.assertIn("TEST_GEN_STATUS_REG_BUSY_MASK", header_code)
        
        # 测试保存到文件
        with tempfile.NamedTemporaryFile(suffix='.h', delete=False) as f:
            generator.save(header_code, f.name)
            self.assertTrue(os.path.exists(f.name))
            with open(f.name, 'r') as f2:
                saved_code = f2.read()
                self.assertEqual(saved_code, header_code)
            
        # 删除临时文件
        os.unlink(f.name)
    
    def test_doc_generator(self):
        """测试文档生成器"""
        # 生成Markdown文档
        generator = DocGenerator()
        doc_content = generator.generate(self.test_config)
        
        # 检查生成的文档
        self.assertIn("# test_gen 寄存器说明文档", doc_content)
        self.assertIn("| CTRL_REG |", doc_content)
        self.assertIn("| STATUS_REG |", doc_content)
        self.assertIn("| ENABLE |", doc_content)
        self.assertIn("| BUSY |", doc_content)
        
        # 测试保存到文件
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as f:
            generator.save(doc_content, f.name)
            self.assertTrue(os.path.exists(f.name))
            with open(f.name, 'r') as f2:
                saved_content = f2.read()
                self.assertEqual(saved_content, doc_content)
            
        # 删除临时文件
        os.unlink(f.name)


if __name__ == "__main__":
    unittest.main() 