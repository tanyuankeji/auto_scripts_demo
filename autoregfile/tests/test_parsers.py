#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析器测试模块
"""

import unittest
import sys
import os
import json
import tempfile

# 添加项目根目录到PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoregfile.parsers.base_parser import detect_parser
from autoregfile.parsers.json_parser import JsonParser
from autoregfile.parsers.yaml_parser import YamlParser


class TestParsers(unittest.TestCase):
    """解析器测试类"""
    
    def test_json_parser(self):
        """测试JSON解析器"""
        # 创建临时JSON配置文件
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as f:
            test_config = {
                "module_name": "test_json",
                "data_width": 32,
                "registers": [
                    {
                        "name": "REG1",
                        "address": "0x00",
                        "type": "ReadWrite"
                    }
                ]
            }
            json.dump(test_config, f)
            f.flush()
            
            # 测试解析
            parser = JsonParser()
            config = parser.parse(f.name)
            
            # 验证结果
            self.assertEqual(config["module_name"], "test_json")
            self.assertEqual(config["data_width"], 32)
            self.assertEqual(len(config["registers"]), 1)
            self.assertEqual(config["registers"][0]["name"], "REG1")
        
        # 删除临时文件
        os.unlink(f.name)
    
    def test_yaml_parser(self):
        """测试YAML解析器"""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML未安装，跳过测试")
            return
            
        # 创建临时YAML配置文件
        with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w+', delete=False) as f:
            f.write("""
module_name: test_yaml
data_width: 32
registers:
  - name: REG1
    address: 0x00
    type: ReadWrite
""")
            f.flush()
            
            # 测试解析
            parser = YamlParser()
            config = parser.parse(f.name)
            
            # 验证结果
            self.assertEqual(config["module_name"], "test_yaml")
            self.assertEqual(config["data_width"], 32)
            self.assertEqual(len(config["registers"]), 1)
            self.assertEqual(config["registers"][0]["name"], "REG1")
        
        # 删除临时文件
        os.unlink(f.name)
    
    def test_detect_parser(self):
        """测试解析器自动检测"""
        # 创建临时JSON配置文件
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as f:
            test_config = {
                "module_name": "test_detect",
                "data_width": 32
            }
            json.dump(test_config, f)
            f.flush()
            
            # 测试自动检测JSON解析器
            parser = detect_parser(f.name)
            self.assertIsInstance(parser, JsonParser)
            
            # 测试解析
            config = parser.parse(f.name)
            self.assertEqual(config["module_name"], "test_detect")
        
        # 删除临时文件
        os.unlink(f.name)
        
        # 测试字符串配置的检测
        json_str = '{"module_name": "test_str"}'
        parser = detect_parser(json_str)
        self.assertIsInstance(parser, JsonParser)


if __name__ == "__main__":
    unittest.main() 