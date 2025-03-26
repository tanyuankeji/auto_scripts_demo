#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：检查寄存器地址转换问题
"""

import os
import sys
import json
import re
from autoregfile.parsers.json_parser import JsonParser
from autoregfile.generators.verilog_generator import VerilogGenerator

def debug_address_conversion():
    """调试地址解析和转换问题"""
    print("=== 调试寄存器地址解析与转换 ===")
    
    # 测试配置文件路径
    config_file = "examples/lock_test_address.json"
    
    # 1. 打印原始配置文件内容
    print(f"\n1. 原始配置文件内容 ({config_file}):")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    for reg in config.get("registers", []):
        addr = reg.get("address", "未定义")
        print(f"  寄存器 {reg['name']} 地址: {addr} (类型: {type(addr)})")
    
    # 2. 解析配置
    print("\n2. 解析后的配置:")
    parser = JsonParser()
    parsed_config = parser.parse(config_file)
    
    for reg in parsed_config.get("registers", []):
        addr = reg.get("address", "未定义")
        print(f"  寄存器 {reg['name']} 地址: {addr} (类型: {type(addr)})")
    
    # 3. 生成Verilog前的上下文准备
    print("\n3. 生成Verilog前的上下文准备:")
    generator = VerilogGenerator()
    context = generator.prepare_context(parsed_config)
    
    for reg in context.get("registers", []):
        addr = reg.get("address", "未定义")
        print(f"  寄存器 {reg['name']} 地址: {addr} (类型: {type(addr)})")
    
    # 4. 生成Verilog代码
    print("\n4. 生成的Verilog地址定义:")
    verilog_code = generator.generate(parsed_config)
    
    # 提取地址定义行
    addr_pattern = r"localparam\s+ADDR_([A-Z0-9_]+)\s*=\s*([^;]+);"
    addr_matches = re.findall(addr_pattern, verilog_code)
    
    for reg_name, addr_value in addr_matches:
        print(f"  ADDR_{reg_name} = {addr_value.strip()}")
    
    # 5. 仔细检查地址转换逻辑
    print("\n5. 检查地址转换逻辑:")
    
    # 模拟模板中的地址转换逻辑
    for reg in parsed_config.get("registers", []):
        reg_name = reg["name"]
        addr_hex = reg["address"]
        
        # 尝试自己转换地址格式
        if isinstance(addr_hex, str) and addr_hex.startswith("0x"):
            addr_int = int(addr_hex, 16)
        else:
            addr_int = int(addr_hex)
        
        addr_width = parsed_config.get("addr_width", 8)
        expected_verilog = f"{addr_width}'h{addr_int:X}"
        
        print(f"  {reg_name}: 原始值={addr_hex}, 转换后={expected_verilog}")
    
    # 6. 检查模板中的地址格式化方式
    template_segment = """
    示例代码片段：
    {% for reg in registers %}
    localparam ADDR_{{ reg.name|upper }} = {{ addr_width }}'h{{ '%X' % reg.address|int(0) }};
    {% endfor %}
    """
    print(f"\n6. 模板地址格式化方式:\n{template_segment}")
    
    # 7. 保存原始Verilog代码到文件
    output_file = "examples/output/debug_addr_convert.v"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(verilog_code)
    
    print(f"\n已保存完整Verilog代码到: {output_file}")

if __name__ == "__main__":
    debug_address_conversion() 