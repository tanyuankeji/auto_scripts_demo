#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用单一模板的寄存器文件生成器
"""

import os
import sys
import json
import yaml
from datetime import datetime
import jinja2

def generate_regfile(config, template_path, output_path):
    """生成寄存器文件"""
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_str = f.read()
    
    # 创建Jinja2环境
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(template_path)),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # 添加内置函数
    env.globals['int'] = int
    
    # 添加过滤器
    env.filters['startswith'] = lambda x, y: str(x).startswith(y)
    
    # 编译模板
    template = env.from_string(template_str)
    
    # 添加时间戳
    config['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 渲染模板
    output = template.render(**config)
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"寄存器文件已生成: {output_path}")


def main():
    """主函数"""
    # 读取配置文件
    config_file = os.path.join('..', 'test_output', 'register_config.json')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 模板文件路径
    template_path = 'all_in_one_template.v.j2'
    
    # 输出文件路径
    output_path = os.path.join('..', 'test_output', 'all_in_one_regfile.v')
    
    # 生成寄存器文件
    generate_regfile(config, template_path, output_path)


if __name__ == "__main__":
    main() 