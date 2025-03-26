#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：测试锁定寄存器功能的解析和处理
"""

import os
import sys
import json
from autoregfile.parsers.json_parser import JsonParser
from autoregfile.generators.verilog_generator import VerilogGenerator

def debug_lock_relations():
    """调试锁定关系的解析和处理"""
    print("=== 调试锁定寄存器功能 ===")
    
    # 测试配置文件路径
    config_file = "examples/lock_test_fix.json"
    
    # 1. 打印原始配置文件内容
    print(f"\n1. 原始配置文件内容 ({config_file}):")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    # 2. 解析配置
    print("\n2. 解析后的配置:")
    parser = JsonParser()
    parsed_config = parser.parse(config_file)
    print("锁定关系:")
    if "lock_relations" in parsed_config:
        for lock_rel in parsed_config["lock_relations"]:
            print(f"  - {lock_rel['locker']} 锁定 {lock_rel['locked']}")
    else:
        print("  无锁定关系")
    
    print("\n寄存器锁定信息:")
    for reg in parsed_config["registers"]:
        print(f"  - {reg['name']} 被锁定者: {reg.get('locked_by', [])}")
    
    # 3. 生成Verilog前的上下文准备
    print("\n3. 生成Verilog前的上下文准备:")
    generator = VerilogGenerator()
    context = generator.prepare_context(parsed_config)
    
    print(f"has_locked_registers 标志: {context.get('has_locked_registers', False)}")
    print("寄存器地址:")
    for reg in context.get('registers', []):
        print(f"  - {reg['name']}: {reg.get('address', 'N/A')}")
    
    # 4. 检查生成的Verilog代码
    print("\n4. 生成的Verilog代码片段:")
    verilog_code = generator.generate(parsed_config)
    
    # 提取锁定逻辑相关部分
    lock_logic_lines = []
    lock_pattern = "// 锁定逻辑"
    assign_pattern = "assign"
    found_lock_section = False
    
    for line in verilog_code.split("\n"):
        if lock_pattern in line:
            found_lock_section = True
            lock_logic_lines.append(line)
        elif found_lock_section and (assign_pattern in line or len(line.strip()) == 0):
            lock_logic_lines.append(line)
        elif found_lock_section and len(line.strip()) > 0 and assign_pattern not in line:
            found_lock_section = False
    
    if lock_logic_lines:
        print("\n锁定逻辑片段:")
        for line in lock_logic_lines:
            print(line)
    else:
        print("\n未找到锁定逻辑片段")
    
    # 5. 检查写逻辑中的锁定条件
    write_logic_lines = []
    for line in verilog_code.split("\n"):
        if "_locked" in line and "if (" in line:
            write_logic_lines.append(line)
    
    if write_logic_lines:
        print("\n写逻辑中的锁定条件:")
        for line in write_logic_lines:
            print(line)
    else:
        print("\n未找到写逻辑中的锁定条件")
    
    # 6. 检查地址定义
    address_lines = []
    for line in verilog_code.split("\n"):
        if "localparam ADDR_" in line:
            address_lines.append(line)
    
    if address_lines:
        print("\n地址定义:")
        for line in address_lines:
            print(line)
    else:
        print("\n未找到地址定义")

if __name__ == "__main__":
    debug_lock_relations() 