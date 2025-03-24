#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于Jinja2的寄存器文件生成器

使用Jinja2模板引擎生成Verilog寄存器文件。
"""

import os
import sys
import argparse
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional
import jinja2

# 导入寄存器类型信息
try:
    from register_types_info import get_register_type_info, get_all_register_types
except ImportError:
    from src.register_types_info import get_register_type_info, get_all_register_types

# 导入配置解析器 
try:
    from enhanced_config_parser import ConfigParser, CommandLineParser
except ImportError:
    from src.enhanced_config_parser import ConfigParser, CommandLineParser


class Jinja2RegFileGenerator:
    """基于Jinja2的寄存器文件生成器"""
    
    def __init__(self, templates_dir: str = None):
        """
        初始化生成器
        
        参数:
            templates_dir: 模板目录路径，默认为当前目录下的templates
        """
        if templates_dir is None:
            # 尝试查找模板目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.join(current_dir, 'templates')
            if not os.path.exists(templates_dir):
                templates_dir = os.path.join(os.path.dirname(current_dir), 'templates')
        
        if not os.path.exists(templates_dir):
            raise FileNotFoundError(f"找不到模板目录: {templates_dir}")
        
        # 设置Jinja2环境
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 添加内置函数
        self.env.globals['int'] = int
        
        # 注册自定义过滤器
        self.register_filters()
    
    def register_filters(self):
        """注册自定义过滤器"""
        # 例如，将寄存器名称转换为小写
        self.env.filters['to_lower'] = lambda x: x.lower()
        # 格式化十六进制地址
        self.env.filters['format_hex'] = lambda x, width: f"{width}'h{x:X}"
        # 转换字符串为整数
        self.env.filters['int'] = lambda x, base=10: int(x, base)
        # 字符串startswith方法
        self.env.filters['startswith'] = lambda x, y: str(x).startswith(y)
    
    def generate(self, config: Dict[str, Any]) -> Dict[str, str]:
        """
        生成寄存器文件
        
        参数:
            config: 配置参数
            
        返回:
            包含生成结果的字典
        """
        result = {}
        
        # 准备模板上下文
        context = self._prepare_context(config)
        
        # 生成Verilog代码
        try:
            template = self.env.get_template('regfile_base.v.j2')
            verilog_code = template.render(**context)
            result['verilog'] = verilog_code
        except Exception as e:
            print(f"生成Verilog代码时出错: {str(e)}")
            result['verilog'] = f"// 生成Verilog代码时出错: {str(e)}"
        
        # 生成头文件（如果需要）
        if config.get('gen_header', False):
            try:
                header_template = self.env.get_template('regfile_header.h.j2')
                header_code = header_template.render(**context)
                result['header'] = header_code
            except Exception as e:
                print(f"生成头文件时出错: {str(e)}")
                result['header'] = f"// 生成头文件时出错: {str(e)}"
        
        # 生成文档（如果需要）
        if config.get('gen_doc', False):
            try:
                doc_template = self.env.get_template('regfile_doc.md.j2')
                doc_content = doc_template.render(**context)
                result['doc'] = doc_content
            except Exception as e:
                print(f"生成文档时出错: {str(e)}")
                result['doc'] = f"# 生成文档时出错: {str(e)}"
        
        return result
    
    def _prepare_context(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备模板上下文
        
        参数:
            config: 配置参数
            
        返回:
            模板上下文字典
        """
        context = config.copy()
        
        # 添加时间戳
        context['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 处理寄存器类型信息
        if 'registers' in context:
            for reg in context['registers']:
                reg_type = reg.get('type', context.get('default_reg_type', 'ReadWrite'))
                try:
                    reg['type_info'] = get_register_type_info(reg_type)
                except ValueError:
                    print(f"警告: 未知的寄存器类型 '{reg_type}'，使用 'ReadWrite' 替代")
                    reg['type'] = 'ReadWrite'
                    reg['type_info'] = get_register_type_info('ReadWrite')
        
        # 计算字节使能数量
        if context.get('byte_enable', False):
            context['num_bytes'] = context['data_width'] // 8
        
        return context
    
    def save_files(self, result: Dict[str, str], config: Dict[str, Any]) -> None:
        """
        保存生成的文件
        
        参数:
            result: 生成结果
            config: 配置参数
        """
        output_dir = config.get('output_dir', '')
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存Verilog文件
        output_file = config.get('output', 'regfile.v')
        verilog_path = os.path.join(output_dir, output_file)
        with open(verilog_path, 'w', encoding='utf-8') as f:
            f.write(result['verilog'])
        print(f"Verilog文件已生成: {verilog_path}")
        
        # 保存C语言头文件
        if 'header' in result:
            if config.get('header_output'):
                header_path = os.path.join(output_dir, config.get('header_output'))
            else:
                header_path = os.path.join(output_dir, os.path.splitext(output_file)[0] + '.h')
            
            with open(header_path, 'w', encoding='utf-8') as f:
                f.write(result['header'])
            print(f"C语言头文件已生成: {header_path}")
        
        # 保存Markdown文档
        if 'doc' in result:
            if config.get('doc_output'):
                doc_path = os.path.join(output_dir, config.get('doc_output'))
            else:
                doc_path = os.path.join(output_dir, os.path.splitext(output_file)[0] + '.md')
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(result['doc'])
            print(f"Markdown文档已生成: {doc_path}")


def setup_argument_parser() -> argparse.ArgumentParser:
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description="基于Jinja2的自动寄存器文件生成器")
    
    # 基本参数
    parser.add_argument("-m", "--module", default="regfile", help="模块名称")
    parser.add_argument("-d", "--data-width", type=int, default=32, help="数据宽度 (位)")
    parser.add_argument("-a", "--addr-width", type=int, default=8, help="地址宽度 (位)")
    parser.add_argument("-wr", "--write-ports", type=int, default=1, help="写端口数量")
    parser.add_argument("-rd", "--read-ports", type=int, default=2, help="读端口数量")
    
    # 复位选项
    parser.add_argument("--sync-reset", action="store_true", help="使用同步复位 (默认为异步复位)")
    parser.add_argument("--reset-value", default="0", help="复位初始化值 (支持十六进制，如0xF)")
    
    # 高级选项
    parser.add_argument("--byte-enable", action="store_true", help="启用字节使能")
    parser.add_argument("--config", help="从JSON、YAML或Excel文件加载配置")
    parser.add_argument("--implementation", choices=["always", "instance"], default="instance", 
                       help="实现方式: always块或寄存器例化 (默认: instance)")
    parser.add_argument("--default-reg-type", default="ReadWrite", 
                       help="默认寄存器类型 (默认: ReadWrite)")
    
    # 输出选项
    parser.add_argument("-o", "--output", default="regfile.v", help="输出Verilog文件名")
    parser.add_argument("--gen-header", action="store_true", help="生成C语言头文件")
    parser.add_argument("--header-output", help="C语言头文件输出路径 (默认为与Verilog文件同名，扩展名为.h)")
    parser.add_argument("--output-dir", help="输出目录路径")
    parser.add_argument("--gen-doc", action="store_true", help="生成Markdown文档")
    parser.add_argument("--doc-output", help="Markdown文档输出路径 (默认为与Verilog文件同名，扩展名为.md)")
    parser.add_argument("--templates-dir", help="自定义模板目录路径")
    
    return parser


def main():
    """主函数"""
    # 解析命令行参数
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 初始化配置
    if args.config:
        # 从配置文件加载
        config = ConfigParser.parse_config_file(args.config)
    else:
        # 从命令行参数加载
        config = CommandLineParser.parse_args_to_config(args)
    
    # 创建生成器
    generator = Jinja2RegFileGenerator(args.templates_dir)
    
    # 生成文件
    result = generator.generate(config)
    generator.save_files(result, config)


if __name__ == "__main__":
    main() 