#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线协议使用示例脚本

该脚本演示了如何使用 AutoRegFile 工具生成不同总线协议的寄存器文件。
"""

import os
import sys
import json
import tempfile
import subprocess

# 添加项目根目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from autoregfile.regfile_gen import generate_regfile


def create_example_config():
    """创建示例配置"""
    config = {
        "module_name": "example_regfile",
        "data_width": 32,
        "addr_width": 8,
        "registers": [
            {
                "name": "CTRL_REG",
                "address": "0x00",
                "type": "ReadWrite",
                "reset_value": "0x00000000",
                "description": "控制寄存器",
                "fields": [
                    {
                        "name": "ENABLE",
                        "bits": "0",
                        "description": "全局使能信号"
                    },
                    {
                        "name": "START",
                        "bits": "1",
                        "description": "启动操作"
                    }
                ]
            },
            {
                "name": "STATUS_REG",
                "address": "0x04",
                "type": "ReadOnly",
                "reset_value": "0x00000000",
                "description": "状态寄存器",
                "fields": [
                    {
                        "name": "BUSY",
                        "bits": "0",
                        "description": "忙状态标志"
                    },
                    {
                        "name": "DONE",
                        "bits": "1",
                        "description": "完成标志"
                    }
                ]
            },
            {
                "name": "INTR_REG",
                "address": "0x08",
                "type": "Write1Clean",
                "reset_value": "0x00000000",
                "description": "中断寄存器",
                "fields": [
                    {
                        "name": "DONE_INT",
                        "bits": "0",
                        "description": "完成中断"
                    },
                    {
                        "name": "ERROR_INT",
                        "bits": "1",
                        "description": "错误中断"
                    }
                ]
            },
            {
                "name": "PULSE_REG",
                "address": "0x0C",
                "type": "Write1Pulse",
                "reset_value": "0x00000000",
                "description": "脉冲寄存器",
                "fields": [
                    {
                        "name": "TRIGGER",
                        "bits": "0",
                        "description": "触发脉冲"
                    }
                ]
            }
        ]
    }
    return config


def generate_for_protocol(protocol, output_dir):
    """为指定协议生成寄存器文件"""
    config = create_example_config()
    
    # 设置总线协议
    config["bus_protocol"] = protocol
    config["module_name"] = f"{protocol}_example"
    
    # 创建配置文件
    config_file = os.path.join(output_dir, f"{protocol}_config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    # 生成寄存器文件
    output_file = os.path.join(output_dir, f"{protocol}_regfile.v")
    generate_regfile(config_file, output_file, False, protocol)
    
    return output_file


def main():
    """主函数"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    print(f"使用临时目录: {temp_dir}")
    
    try:
        # 为每种协议生成寄存器文件
        protocols = ["apb", "axi_lite", "custom"]
        for protocol in protocols:
            output_file = generate_for_protocol(protocol, temp_dir)
            print(f"生成 {protocol} 总线协议寄存器文件: {output_file}")
            
            # 显示前 10 行代码
            with open(output_file, "r") as f:
                lines = f.readlines()[:10]
                print("\n前 10 行代码预览:")
                for line in lines:
                    print(f"  {line.rstrip()}")
                print("  ...")
            
            print("\n")
        
        # 打印输出目录中的文件
        print("生成的文件列表:")
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            file_size = os.path.getsize(file_path)
            print(f"  {filename} ({file_size} 字节)")
        
        # 询问是否保留生成的文件
        if input("\n是否复制生成的文件到当前目录? (y/n): ").lower() == 'y':
            current_dir = os.getcwd()
            for filename in os.listdir(temp_dir):
                if filename.endswith('.v'):
                    src_path = os.path.join(temp_dir, filename)
                    dst_path = os.path.join(current_dir, filename)
                    with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                        dst.write(src.read())
                    print(f"已复制: {dst_path}")
    
    finally:
        # 询问是否删除临时目录
        if input("\n是否删除临时目录? (y/n): ").lower() == 'y':
            import shutil
            shutil.rmtree(temp_dir)
            print(f"已删除临时目录: {temp_dir}")
        else:
            print(f"保留临时目录: {temp_dir}")


if __name__ == "__main__":
    main() 