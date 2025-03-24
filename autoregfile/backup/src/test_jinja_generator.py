#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Jinja2 寄存器文件生成器
"""

import os
import json
from datetime import datetime
from jinja_regfile_generator import Jinja2RegFileGenerator


def main():
    """主测试函数"""
    # 读取 JSON 配置文件
    config_file = os.path.join('..', 'test_output', 'register_config.json')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 设置输出参数
    config['output'] = '../test_output/jinja_custom_regfile.v'
    config['gen_header'] = True
    config['gen_doc'] = True
    
    # 创建生成器
    generator = Jinja2RegFileGenerator()
    
    # 生成文件
    result = generator.generate(config)
    
    # 保存文件
    verilog_path = config['output']
    with open(verilog_path, 'w', encoding='utf-8') as f:
        f.write(result['verilog'])
    print(f"Verilog文件已生成: {verilog_path}")
    
    # 保存C语言头文件
    if 'header' in result:
        header_path = os.path.splitext(verilog_path)[0] + '.h'
        with open(header_path, 'w', encoding='utf-8') as f:
            f.write(result['header'])
        print(f"C语言头文件已生成: {header_path}")
    
    # 保存Markdown文档
    if 'doc' in result:
        doc_path = os.path.splitext(verilog_path)[0] + '.md'
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(result['doc'])
        print(f"Markdown文档已生成: {doc_path}")


if __name__ == "__main__":
    main() 