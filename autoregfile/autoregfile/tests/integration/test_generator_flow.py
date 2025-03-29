#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成器流程集成测试

测试从配置解析到总线生成的完整流程，验证不同模块的集成。
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from autoregfile.core.bus_generators.factory import BusGeneratorFactory
from autoregfile.core.bus_generators.custom_generator import CustomBusGenerator
from autoregfile.parsers.json_parser import JsonParser


class TestGeneratorFlow(unittest.TestCase):
    """测试生成器流程集成"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建临时测试目录
        self.test_dir = tempfile.mkdtemp()
        
        # 创建测试模板目录
        self.template_dir = os.path.join(self.test_dir, 'templates')
        os.makedirs(os.path.join(self.template_dir, 'verilog', 'bus'), exist_ok=True)
        
        # 创建测试模板文件
        self.template_file = os.path.join(self.template_dir, 'verilog', 'bus', 'custom.v.j2')
        with open(self.template_file, 'w', encoding='utf-8') as f:
            f.write("""
// {{ module_name }} - 生成的寄存器文件
// 生成时间: {{ timestamp }}
// 总线协议: {{ bus_protocol }}

module {{ module_name }} (
    input wire clk,
    input wire rst_n,
    
    // 地址和数据总线
    input wire [{{ addr_width-1 }}:0] addr,
    input wire [{{ data_width-1 }}:0] wdata,
    output reg [{{ data_width-1 }}:0] rdata,
    
    // 控制信号
    input wire write_en,
    input wire read_en,
    output reg ack
);

{% for reg in registers %}
    // {{ reg.name }} - {{ reg.description }}
    reg [{{ reg.width-1 }}:0] {{ reg.name }}_reg;
{% endfor %}

endmodule
            """)
        
        # 创建测试配置文件
        self.config_file = os.path.join(self.test_dir, 'test_config.json')
        test_config = {
            "module_name": "test_regfile",
            "data_width": 32,
            "addr_width": 8,
            "bus_protocol": "custom",
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
                        }
                    ]
                },
                {
                    "name": "status",
                    "address": "0x04",
                    "description": "状态寄存器",
                    "fields": [
                        {
                            "name": "busy",
                            "bit_range": "0:0",
                            "access": "RO",
                            "reset_val": 0,
                            "description": "忙状态位"
                        }
                    ]
                }
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=4)
        
        # 设置输出文件路径
        self.output_file = os.path.join(self.test_dir, 'output_regfile.v')
    
    def tearDown(self):
        """测试后清理工作"""
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_json_to_verilog_flow(self):
        """测试从JSON配置到Verilog生成的流程"""
        # 解析JSON配置
        parser = JsonParser(self.config_file)
        config = parser.parse()
        
        # 验证解析结果
        self.assertIsNotNone(config)
        self.assertEqual(config["module_name"], "test_regfile")
        self.assertEqual(len(config["registers"]), 2)
        
        # 创建总线生成器
        generator = BusGeneratorFactory.create_generator(
            "custom",
            config,
            template_dirs=[self.template_dir]
        )
        
        # 验证生成器
        self.assertIsNotNone(generator)
        self.assertIsInstance(generator, CustomBusGenerator)
        
        # 生成Verilog文件
        result = generator.generate(self.output_file)
        
        # 验证生成结果
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_file))
        
        # 检查生成的文件内容
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 验证文件内容包含预期元素
        self.assertIn("module test_regfile", content)
        self.assertIn("control_reg", content)
        self.assertIn("status_reg", content)
    
    def test_custom_bus_options(self):
        """测试自定义总线选项的处理"""
        # 创建带有自定义总线选项的配置
        config = {
            "module_name": "custom_bus",
            "data_width": 32,
            "addr_width": 8,
            "bus_protocol": "custom",
            "bus_options": {
                "custom": {
                    "enable_handshake": False,
                    "addr_lsb": 4
                }
            },
            "registers": [
                {
                    "name": "config",
                    "address": "0x10",
                    "description": "配置寄存器"
                }
            ]
        }
        
        # 创建自定义总线生成器
        generator = CustomBusGenerator(config, template_dirs=[self.template_dir])
        
        # 准备上下文
        context = generator._prepare_context()
        
        # 验证自定义选项已正确处理
        self.assertFalse(context["enable_handshake"])
        self.assertEqual(context["addr_lsb"], 4)


if __name__ == '__main__':
    unittest.main() 