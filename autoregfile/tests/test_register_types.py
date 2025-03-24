#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器类型测试模块
"""

import unittest
import sys
import os

# 添加项目根目录到PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoregfile.core.register_types import RegisterType, RegisterTypeManager, get_register_type_manager


class TestRegisterTypes(unittest.TestCase):
    """寄存器类型测试类"""
    
    def test_register_type_manager(self):
        """测试寄存器类型管理器"""
        # 获取管理器实例
        manager = get_register_type_manager()
        
        # 测试获取所有类型
        all_types = manager.get_all_register_types()
        self.assertIsInstance(all_types, list)
        self.assertGreater(len(all_types), 0)
        
        # 测试获取特定类型
        rw_type = manager.get_register_type("ReadWrite")
        self.assertEqual(rw_type.name, "ReadWrite")
        self.assertTrue(rw_type.readable)
        self.assertTrue(rw_type.writable)
        
        ro_type = manager.get_register_type("ReadOnly")
        self.assertEqual(ro_type.name, "ReadOnly")
        self.assertTrue(ro_type.readable)
        self.assertFalse(ro_type.writable)
        
        wo_type = manager.get_register_type("WriteOnly")
        self.assertEqual(wo_type.name, "WriteOnly")
        self.assertFalse(wo_type.readable)
        self.assertTrue(wo_type.writable)
        
        # 测试未知类型抛出异常
        with self.assertRaises(ValueError):
            manager.get_register_type("UnknownType")
    
    def test_verilog_generation(self):
        """测试Verilog代码生成"""
        manager = get_register_type_manager()
        
        # 测试ReadWrite类型
        rw_type = manager.get_register_type("ReadWrite")
        write_code = rw_type.get_write_behavior("test_reg", 32, "addr", "data", "wr_en")
        self.assertIn("test_reg_reg <= data", write_code)
        
        read_code = rw_type.get_read_behavior("test_reg", 32, "addr", "data")
        self.assertIn("data = test_reg_reg", read_code)
        
        # 测试ReadOnly类型
        ro_type = manager.get_register_type("ReadOnly")
        write_code = ro_type.get_write_behavior("test_reg", 32, "addr", "data", "wr_en")
        self.assertNotIn("test_reg_reg <=", write_code)
        
        # 测试WriteOnce类型
        wo_type = manager.get_register_type("WriteOnce")
        write_code = wo_type.get_write_behavior("test_reg", 32, "addr", "data", "wr_en")
        self.assertIn("test_reg_written", write_code)
        self.assertIn("!test_reg_written", write_code)


if __name__ == "__main__":
    unittest.main() 