#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog自动线网声明工具 (Auto Wire Generator)
用途：自动检测Verilog代码中未声明的信号，并生成相应的wire声明
版本：1.3.0
"""

import re
import sys
import os
import json
import argparse
from typing import List, Dict, Set, Tuple, Optional
import traceback

from autowire.core.parser import VerilogParser
from autowire.core.utils import ParseError

def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件
    
    参数:
        config_file: 配置文件路径，如果为None则使用默认路径
        
    返回:
        配置字典
    """
    if config_file is None:
        # 默认配置文件路径
        default_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'auto_wire_config.json'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), 'config', 'auto_wire_config.json'),
            os.path.join(os.getcwd(), 'config', 'auto_wire_config.json')
        ]
        
        for path in default_paths:
            if os.path.exists(path):
                config_file = path
                break
        else:
            return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"警告：无法读取配置文件 {config_file}：{str(e)}")
        return {}

def generate_signal_definitions(undefined_signals: List[str], signal_widths: Dict[str, Optional[str]], default_width: Optional[str] = None) -> List[str]:
    """
    为未定义信号生成wire定义，保持原始顺序
    
    参数:
        undefined_signals: 未定义信号列表
        signal_widths: 信号位宽字典
        default_width: 默认位宽，如果为None则不添加位宽
        
    返回:
        wire定义列表
    """
    definitions = []
    for signal in undefined_signals:
        width = signal_widths.get(signal) if signal_widths else None
        if width is None and default_width:
            # 处理默认位宽，支持[位宽-1:0]格式
            # 如果default_width是数字，则转换为[数字-1:0]格式
            if default_width.isdigit():
                width = f"[{int(default_width)-1}:0]"
            # 如果已经是[x:y]格式，则直接使用
            elif re.match(r'\[\s*\d+\s*:\s*\d+\s*\]', default_width):
                width = default_width
            # 如果是其他格式，尝试提取数字并转换为[数字-1:0]格式
            else:
                match = re.search(r'(\d+)', default_width)
                if match:
                    width = f"[{int(match.group(1))-1}:0]"
                else:
                    # 如果无法解析，使用原始值
                    width = default_width
        
        # 确保位宽格式正确
        if width and not width.startswith('['):
            width = f"[{width}]"
            
        if width:
            definitions.append(f"wire {width} {signal};\n")
        else:
            definitions.append(f"wire {signal};\n")
            
    return definitions

def write_output(file_name: str, definitions: List[str], output_dir: Optional[str] = None) -> str:
    """
    将生成的信号定义写入输出文件
    
    参数:
        file_name: 原始文件名
        definitions: 信号定义列表
        output_dir: 输出目录，如果为None则使用原始文件目录
        
    返回:
        输出文件路径
    """
    base_name = os.path.basename(file_name)
    output_file_name = base_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, output_file_name)
    else:
        output_dir = os.path.dirname(file_name)
        output_file = os.path.join(output_dir, output_file_name)
    
    try:
        with open(output_file, 'w') as file:
            file.writelines(definitions)
        print(f"输出已写入：{output_file}")
        return output_file
    except IOError:
        print(f"错误：无法写入文件 {output_file}")
        sys.exit(1)

def append_to_original(file_name: str, definitions: List[str]) -> None:
    """
    将生成的定义追加到原始文件的模块定义之后
    
    参数:
        file_name: 原始文件名
        definitions: 信号定义列表
    """
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            
        # 查找模块头部结束位置
        module_pattern = re.compile(r'module\s+\w+\s*\([^;]*;', re.DOTALL)
        match = module_pattern.search(content)
        
        if match:
            insert_pos = match.end()
            new_content = content[:insert_pos] + '\n\n// 自动生成的wire声明\n' + ''.join(definitions) + '\n' + content[insert_pos:]
            
            with open(file_name, 'w') as file:
                file.write(new_content)
            print(f"定义已追加到原始文件：{file_name}")
        else:
            print("警告：无法找到模块定义，未能追加到原始文件")
    except IOError:
        print(f"错误：无法修改原始文件 {file_name}")
        sys.exit(1)

def print_help() -> None:
    """打印详细的使用说明"""
    help_text = """
Verilog自动线网声明工具 (Auto Wire Generator)
=============================================

功能说明：
  自动检测Verilog/SystemVerilog代码中未声明的信号，并生成相应的wire声明。
  
主要特点：
  1. 保持信号的原始出现顺序
  2. 自动推断信号位宽
  3. 支持parameter定义的信号
  4. 多种输出模式（独立文件或追加到原文件）
  5. 支持用户自定义排除匹配模式（通过命令行或配置文件）
  6. 增强的模块实例化名称识别（支持常用前缀如u_、i_等）
  7. 支持generate/endgenerate关键字
  8. 支持Verilog数值常量（如1'h0, 8'b00101010等）
  9. 支持多行注释和宏定义
  
用法示例：
  # 基本用法：生成单独的wire声明文件
  autowire my_design.v
  
  # 自动检测位宽
  autowire --width my_design.v
  
  # 应用默认位宽（支持多种格式）
  autowire --default-width "[31:0]" my_design.v  # 直接使用指定位宽
  autowire --default-width "32" my_design.v     # 自动转换为[31:0]格式
  
  # 直接追加到原始文件
  autowire --append my_design.v
  
  # 指定输出目录
  autowire --output-dir ./generated my_design.v
  
  # 排除特定模式的信号（命令行方式）
  autowire --exclude "temp_.*" "debug_.*" my_design.v
  
  # 使用配置文件排除特定模式的信号
  autowire --config ./config/auto_wire_config.json my_design.v
  
配置文件说明：
  配置文件为JSON格式，包含以下字段：
  {
    "exclude_patterns": [
        "temp_.*",
        "debug_.*",
        "test_.*",
        ".*_reg",
        ".*_next"
    ],
    "description": "用户自定义的匹配模式，支持正则表达式",
    "version": "1.0.0"
  }
  
  默认配置文件路径：./config/auto_wire_config.json
    """
    print(help_text)

def main() -> None:
    """主函数：解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(description='Verilog自动线网声明工具')
    parser.add_argument('file', help='Verilog源文件路径')
    parser.add_argument('--width', '-w', action='store_true', help='尝试提取信号位宽')
    parser.add_argument('--default-width', '-d', type=str, help='默认位宽，如 "[7:0]" 或 "8" (会转换为[7:0]格式)')
    parser.add_argument('--append', '-a', action='store_true', help='将定义追加到原始文件')
    parser.add_argument('--output-dir', '-o', type=str, help='输出目录路径')
    parser.add_argument('--exclude', '-e', type=str, nargs='+', help='排除匹配模式列表，支持正则表达式')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--help-detail', action='store_true', help='显示详细使用说明')
    parser.add_argument('--debug', action='store_true', help='启用调试模式，显示详细处理过程')
    
    args = parser.parse_args()
    
    if args.help_detail:
        print_help()
        return
    
    # 加载配置文件
    config = load_config(args.config)
    exclude_patterns = args.exclude or config.get('exclude_patterns', [])
    default_width = args.default_width or config.get('default_width')
    
    if args.debug:
        print(f"处理文件: {args.file}")
        if exclude_patterns:
            print(f"排除模式: {exclude_patterns}")
        if default_width:
            print(f"默认位宽: {default_width}")
    
    try:
        # 解析Verilog文件
        parser = VerilogParser()
        parser.parse_file(args.file)
        
        if args.debug:
            print("\n预处理后的内容:")
            print("="*50)
            print(parser.processed_content[:300] + "..." if len(parser.processed_content) > 300 else parser.processed_content)
            print("="*50)
            print(f"\n检测到已定义信号: {len(parser.defined_signals)}个")
            print(f"检测到模块名: {parser.module_name}")
            
        # 获取未定义信号
        undefined_signals = parser.get_undefined_signals(exclude_patterns)
        
        if undefined_signals:
            if args.verbose or args.debug:
                print(f"\n发现未定义信号: {len(undefined_signals)}个")
                if args.debug:
                    print(f"信号列表: {', '.join(undefined_signals[:20])}{'...' if len(undefined_signals) > 20 else ''}")
            
            # 如果需要提取位宽
            signal_widths = {}
            if args.width:
                signal_widths = parser.get_signal_widths(undefined_signals)
                
                if args.debug:
                    print("\n信号位宽信息:")
                    for signal, width in signal_widths.items():
                        if width:
                            print(f"  {signal}: {width}")
            
            # 生成wire声明
            definitions = generate_signal_definitions(undefined_signals, signal_widths, default_width)
            
            if args.debug:
                print("\n生成的wire声明:")
                for i, definition in enumerate(definitions[:10]):
                    print(f"  {definition.strip()}")
                if len(definitions) > 10:
                    print("  ...")
            
            # 输出或追加声明
            if args.append:
                append_to_original(args.file, definitions)
            else:
                output_file = write_output(args.file, definitions, args.output_dir)
                if args.verbose or args.debug:
                    print(f"\n处理完成。输出文件: {output_file}")
        else:
            print("\n未发现未定义信号。")
            
    except ParseError as e:
        print(f"\n错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n未知错误: {str(e)}")
        if args.debug:
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 