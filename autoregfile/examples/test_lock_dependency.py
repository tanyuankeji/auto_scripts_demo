#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试锁定依赖功能

此脚本用于测试锁定依赖功能的实现。它将：
1. 解析Excel配置文件
2. 显示锁定依赖信息
3. 生成并检查包含锁定依赖逻辑的Verilog代码
"""

import os
import sys
import json
import pathlib
from pathlib import Path

# 设置项目根目录
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from autoregfile.parsers import ExcelParser
from autoregfile.generators import VerilogGenerator

# 设置输出目录
output_dir = os.path.join(project_root, "examples", "test")
os.makedirs(output_dir, exist_ok=True)

# 初始化ExcelParser
parser = ExcelParser()

# 解析Excel配置文件
excel_file = os.path.join(project_root, "examples", "configs", "extended_field_test.xlsx")
config = parser.parse(excel_file)

# 显示解析结果
module_name = config.get("module_name", "未知模块")
registers = config.get("registers", [])
fields = config.get("fields", [])
register_count = len(registers)
field_count = len(fields)

print(f"解析Excel文件: {excel_file}")
print(f"模块名称: {module_name}")
print(f"寄存器数量: {register_count}")
print(f"字段数量: {field_count}")

# 显示锁定依赖信息
print("\n锁定依赖信息:")

# 创建寄存器名称到寄存器对象的映射，方便引用
reg_map = {reg.get("name", "未知"): reg for reg in registers}

# 处理字段级锁定依赖
for field in fields:
    reg_name = field.get("register", "未知寄存器")
    field_name = field.get("name", "未知字段")
    
    # 检查字段是否有锁定依赖
    locked_by = field.get("locked_by", [])
    if locked_by and len(locked_by) > 0:
        print(f"字段 {reg_name}.{field_name} 被 {', '.join(locked_by)} 锁定")
    
    # 检查字段是否有魔术数字依赖
    magic_dep = field.get("magic_number_dep", "")
    magic_val = field.get("magic_value", "")
    if magic_dep:
        if magic_val:
            print(f"字段 {reg_name}.{field_name} 依赖魔术数字 {magic_dep} = {magic_val}")
        else:
            print(f"字段 {reg_name}.{field_name} 依赖魔术数字 {magic_dep}")

# 生成Verilog代码
verilog_gen = VerilogGenerator()
verilog_code = verilog_gen.generate(config)

# 将代码分割成行
verilog_lines = verilog_code.split("\n")

# 检查生成的Verilog代码中的锁定和魔术数字依赖逻辑
print("\n生成的锁定和魔术数字依赖Verilog代码片段:")
for i, line in enumerate(verilog_lines):
    if "locked" in line or "magic" in line:
        # 显示前后几行以提供上下文
        start = max(0, i-2)
        end = min(len(verilog_lines), i+3)
        print(f"行 {i+1}: {line}")
        for j in range(i+1, end):
            print(f"行 {j+1}: {verilog_lines[j]}")
        print("")  # 空行分隔不同的片段

# 保存生成的Verilog代码
output_file = os.path.join(output_dir, "lock_test.v")
verilog_gen.save(verilog_code, output_file)
print(f"\n已保存Verilog代码到: {output_file}")

print("\n锁定依赖测试完成!") 