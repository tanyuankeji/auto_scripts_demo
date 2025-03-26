#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：检查总线模板加载和地址转换过程
"""

import os
import sys
import json
import traceback
from autoregfile.core.template_manager import get_template_manager
from autoregfile.core.bus_generator import BusGenerator

def debug_template_and_address():
    """调试总线模板加载和地址转换过程"""
    print("=== 调试总线模板和地址转换 ===")
    
    # 创建测试配置
    config = {
        "module_name": "test_module",
        "data_width": 32,
        "addr_width": 8,
        "registers": [
            {
                "name": "LOCK_REG",
                "address": "0x10",
                "type": "LockField",
                "reset_value": "0x00000000",
                "description": "锁定控制寄存器"
            },
            {
                "name": "DATA_REG",
                "address": "0x14",
                "type": "ReadWrite",
                "reset_value": "0x00000000",
                "description": "数据寄存器"
            }
        ],
        "lock_relations": [
            {
                "locker": "LOCK_REG",
                "locked": "DATA_REG"
            }
        ]
    }
    
    # 设置DATA_REG的locked_by字段
    config["registers"][1]["locked_by"] = ["LOCK_REG"]
    
    # 获取模板管理器
    template_manager = get_template_manager()
    
    # 获取模板目录
    import autoregfile
    pkg_dir = os.path.dirname(os.path.abspath(autoregfile.__file__))
    templates_dir = os.path.join(pkg_dir, 'templates')
    print(f"模板根目录: {templates_dir}")
    
    # 2. 创建总线生成器并测试地址处理
    print("\n2. 测试使用regfile.v.j2主模板:")
    
    # 创建临时目录
    os.makedirs("examples/output", exist_ok=True)
    
    # 准备上下文
    context = {
        "module_name": "test_module",
        "data_width": 32,
        "addr_width": 8,
        "registers": config["registers"],
        "has_locked_registers": True,
        "num_write_ports": 1,
        "num_read_ports": 1,
        "sync_reset": False,
        "byte_enable": True
    }
    
    # 打印寄存器地址信息
    print("\n寄存器地址信息:")
    for reg in context.get("registers", []):
        addr = reg.get("address", "未定义")
        print(f"  寄存器 {reg['name']} 地址: {addr} (类型: {type(addr)})")
    
    # 检查锁定关系
    print("\n锁定关系:")
    for reg in context.get("registers", []):
        if "locked_by" in reg and reg["locked_by"]:
            print(f"  {reg['name']} 被锁定者: {reg['locked_by']}")
    
    # 测试使用主模板直接渲染
    print("\n3. 测试直接渲染主模板 (regfile.v.j2):")
    
    try:
        main_template_path = os.path.join("verilog", "regfile.v.j2")
        main_output = template_manager.render_template(main_template_path, context)
        
        # 保存主模板输出
        main_output_file = "examples/output/debug_main_template.v"
        with open(main_output_file, "w", encoding="utf-8") as f:
            f.write(main_output)
        
        print(f"已生成主模板调试输出: {main_output_file}")
        
        # 提取地址定义行
        address_lines = []
        for line in main_output.split("\n"):
            if "localparam ADDR_" in line:
                address_lines.append(line)
        
        print("\n地址定义行:")
        for line in address_lines:
            print(f"  {line}")
        
    except Exception as e:
        print(f"渲染主模板时出错: {str(e)}")
        traceback.print_exc()
    
    # 4. 测试自定义总线模板
    print("\n4. 测试自定义总线模板 (custom.v.j2):")
    
    # 修复自定义总线模板
    custom_template_path = os.path.join(templates_dir, "verilog", "bus", "custom.v.j2")
    print(f"自定义总线模板路径: {custom_template_path}")
    
    # 读取并打印模板内容
    try:
        with open(custom_template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        print("\n自定义总线模板内容片段:")
        lines = template_content.split("\n")
        for i, line in enumerate(lines):
            if i >= 20 and i <= 30:  # 打印关键部分
                print(f"{i+1}: {line}")
        
        # 尝试修改模板文件
        fixed_content = template_content.replace(
            "// 地址常量定义", 
            """
    // 地址常量定义
    {% for reg in registers %}
    localparam ADDR_{{ reg.name|upper }} = {{ addr_width }}'h{{ '%X' % reg.address|int(0) }};   // {{ reg.description }} ({{ reg.type }}类型)
    {% endfor %}
            """.strip()
        )
        
        # 保存修复后的模板到调试输出目录
        fixed_template_path = "examples/output/custom_fixed.v.j2"
        with open(fixed_template_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        
        print(f"\n已保存修复后的模板到: {fixed_template_path}")
        
        # 尝试使用修复后的模板渲染
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader("examples/output"))
        template = env.get_template("custom_fixed.v.j2")
        fixed_output = template.render(**context)
        
        # 保存修复后的输出
        fixed_output_path = "examples/output/custom_fixed_output.v"
        with open(fixed_output_path, "w", encoding="utf-8") as f:
            f.write(fixed_output)
        
        print(f"已生成修复后的输出: {fixed_output_path}")
        
    except Exception as e:
        print(f"处理自定义总线模板时出错: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_template_and_address() 