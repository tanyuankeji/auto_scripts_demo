#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线协议功能测试脚本
"""

import os
import sys
import tempfile
import shutil
import json
import unittest

# 添加项目根目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from autoregfile.regfile_gen import generate_regfile
from autoregfile.core.bus_generator import BusGenerator


class BusProtocolTest(unittest.TestCase):
    """总线协议功能测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.test_dir = tempfile.mkdtemp()
        
        # 示例配置
        self.test_config = {
            "module_name": "test_protocol",
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
            ]
        }
        
        # 创建配置文件
        self.config_file = os.path.join(self.test_dir, "test_config.json")
        with open(self.config_file, "w") as f:
            json.dump(self.test_config, f, indent=2)
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_apb_protocol(self):
        """测试APB总线协议"""
        output_file = os.path.join(self.test_dir, "apb_test.v")
        
        # 生成RTL代码
        generate_regfile(self.config_file, output_file, False, "apb")
        
        # 检查生成的文件是否存在
        self.assertTrue(os.path.exists(output_file))
        
        # 检查文件内容
        with open(output_file, "r") as f:
            content = f.read()
            
            # 检查APB协议特定信号
            self.assertIn("paddr", content)
            self.assertIn("psel", content)
            self.assertIn("penable", content)
            self.assertIn("pwrite", content)
            self.assertIn("pwdata", content)
            self.assertIn("prdata", content)
            self.assertIn("pready", content)
            self.assertIn("pslverr", content)
    
    def test_axi_lite_protocol(self):
        """测试AXI-Lite总线协议"""
        output_file = os.path.join(self.test_dir, "axi_lite_test.v")
        
        # 生成RTL代码
        generate_regfile(self.config_file, output_file, False, "axi_lite")
        
        # 检查生成的文件是否存在
        self.assertTrue(os.path.exists(output_file))
        
        # 检查文件内容
        with open(output_file, "r") as f:
            content = f.read()
            
            # 检查AXI-Lite协议特定信号
            self.assertIn("s_axil_awaddr", content)
            self.assertIn("s_axil_awvalid", content)
            self.assertIn("s_axil_awready", content)
            self.assertIn("s_axil_wdata", content)
            self.assertIn("s_axil_wstrb", content)
            self.assertIn("s_axil_wvalid", content)
            self.assertIn("s_axil_wready", content)
            self.assertIn("s_axil_bresp", content)
            self.assertIn("s_axil_bvalid", content)
            self.assertIn("s_axil_bready", content)
            self.assertIn("s_axil_araddr", content)
            self.assertIn("s_axil_arvalid", content)
            self.assertIn("s_axil_arready", content)
            self.assertIn("s_axil_rdata", content)
            self.assertIn("s_axil_rresp", content)
            self.assertIn("s_axil_rvalid", content)
            self.assertIn("s_axil_rready", content)
    
    def test_custom_protocol(self):
        """测试自定义总线协议"""
        output_file = os.path.join(self.test_dir, "custom_test.v")
        
        # 生成RTL代码
        generate_regfile(self.config_file, output_file, False, "custom")
        
        # 检查生成的文件是否存在
        self.assertTrue(os.path.exists(output_file))
        
        # 检查文件内容
        with open(output_file, "r") as f:
            content = f.read()
            
            # 检查自定义协议特定信号
            self.assertIn("addr", content)
            self.assertIn("chip_select", content)
            self.assertIn("write_en", content)
            self.assertIn("read_en", content)
            self.assertIn("write_data", content)
            self.assertIn("read_data", content)
            self.assertIn("data_valid", content)
    
    def test_pulse_register(self):
        """测试脉冲寄存器在总线协议中的实现"""
        # 修改配置，添加脉冲寄存器
        self.test_config["registers"].append({
            "name": "PULSE_REG",
            "address": "0x08",
            "type": "Write1Pulse",
            "reset_value": "0x00000000",
            "description": "脉冲寄存器"
        })
        
        # 更新配置文件
        with open(self.config_file, "w") as f:
            json.dump(self.test_config, f, indent=2)
        
        output_file = os.path.join(self.test_dir, "pulse_test.v")
        
        # 生成RTL代码
        generate_regfile(self.config_file, output_file, False, "apb")
        
        # 检查生成的文件是否存在
        self.assertTrue(os.path.exists(output_file))
        
        # 检查文件内容
        with open(output_file, "r") as f:
            content = f.read()
            
            # 检查脉冲寄存器输出信号
            self.assertIn("pulse_reg_pulse", content)
    
    def test_locked_register(self):
        """测试锁定寄存器在总线协议中的实现"""
        # 修改配置，添加锁定关系
        self.test_config["registers"][1]["locked_by"] = ["CTRL_REG"]
        
        # 更新配置文件
        with open(self.config_file, "w") as f:
            json.dump(self.test_config, f, indent=2)
        
        output_file = os.path.join(self.test_dir, "lock_test.v")
        
        # 生成RTL代码
        generate_regfile(self.config_file, output_file, False, "axi_lite")
        
        # 检查生成的文件是否存在
        self.assertTrue(os.path.exists(output_file))
        
        # 检查文件内容
        with open(output_file, "r") as f:
            content = f.read()
            
            # 检查锁定逻辑
            self.assertIn("status_reg_locked", content)


if __name__ == "__main__":
    unittest.main() 