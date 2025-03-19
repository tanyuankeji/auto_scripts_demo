#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog自动线网声明工具 (Auto Wire Generator)
用途：自动检测Verilog代码中未声明的信号，并生成相应的wire声明
作者：AI助手
版本：1.1.0
"""

import re
import sys
import os
import argparse
from typing import List, Dict, Set, Tuple, Optional
from collections import OrderedDict

# Verilog/SystemVerilog保留关键字集合
VERILOG_KEYWORDS = {
    "module", "endmodule", "input", "output", "inout", "assign", "always", "always_ff",
    "always_comb", "always_latch", "if", "else", "case", "endcase", "begin", "end", 
    "wire", "reg", "logic", "parameter", "localparam", "function", "endfunction", "task",
    "endtask", "for", "while", "repeat", "forever", "default", "posedge", "negedge",
    "or", "and", "not", "xor", "nor", "nand", "xnor", "buf", "signed", "unsigned"
}

def remove_comments(line: str) -> str:
    """移除代码中的注释"""
    line = re.sub(r'//.*', '', line)  # 移除单行注释
    line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)  # 移除多行注释
    return line

def extract_bitwidth(file_content: str, signal_name: str) -> Optional[str]:
    """
    从文件内容中提取信号位宽
    
    参数:
        file_content: 文件内容字符串
        signal_name: 需要提取位宽的信号名
        
    返回:
        位宽字符串，如"[7:0]"，如果无法确定返回None
    """
    # 查找参数定义，如 parameter WIDTH = 8
    param_pattern = re.compile(r'parameter\s+(\w+)\s*=\s*(\d+)')
    params = {name: value for name, value in param_pattern.findall(file_content)}
    
    # 查找信号使用位宽的地方
    patterns = [
        # 例如：assign data[7:0] = value;
        re.compile(rf'{signal_name}\s*\[(\d+):(\d+)\]'),
        # 例如：assign data[WIDTH-1:0] = value;
        re.compile(rf'{signal_name}\s*\[(\w+)\s*-\s*1\s*:\s*0\]'),
        # 例如：assign data[0] = value; (单比特)
        re.compile(rf'{signal_name}\s*\[(\d+)\]')
    ]
    
    for pattern in patterns:
        matches = pattern.findall(file_content)
        if matches:
            # 处理第一个匹配
            if len(matches[0]) == 2:  # 范围 [x:y]
                high, low = matches[0]
                # 如果是参数，尝试替换
                if high in params:
                    high = params[high]
                if low in params:
                    low = params[low]
                return f"[{high}:{low}]"
            elif len(matches[0]) == 1:  # 单比特 [x]
                return "[0:0]"  # 转换为范围格式
    
    # 尝试从输入信号定义推断
    input_pattern = re.compile(rf'input\s+(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])?\s*{signal_name}')
    output_pattern = re.compile(rf'output\s+(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])?\s*{signal_name}')
    
    for pattern in [input_pattern, output_pattern]:
        match = pattern.search(file_content)
        if match and match.group(1) and match.group(2):
            return f"[{match.group(1)}:{match.group(2)}]"
    
    return None

def parse_verilog(file_name: str, extract_width: bool = False) -> Tuple[List[str], Dict[str, Optional[str]]]:
    """
    解析Verilog文件，提取未定义的信号，保持出现顺序
    
    参数:
        file_name: Verilog文件路径
        extract_width: 是否提取信号位宽
        
    返回:
        未定义信号列表和信号位宽字典的元组
    """
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            lines = content.splitlines()
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_name}")
        sys.exit(1)

    # 使用OrderedDict保持信号出现的顺序
    signals_ordered = OrderedDict()
    defined_signals = set()
    module_names = set()
    module_instance_signals = set()
    instance_module_names = []
    parameter_values = {}  # 存储parameter定义值

    # 定义正则表达式
    signal_pattern = re.compile(r'\b(\w+)\b')
    
    # 信号定义模式
    define_patterns = [
        re.compile(r'\b(?:wire|reg|logic)\s+(?:\[\s*[\w\d\-\+:\s]+\])?\s*(\w+)'),
        re.compile(r'\binput\s+(?:\[\s*[\w\d\-\+:\s]+\])?\s*(\w+)'),
        re.compile(r'\boutput\s+(?:\[\s*[\w\d\-\+:\s]+\])?\s*(\w+)'),
        re.compile(r'\binout\s+(?:\[\s*[\w\d\-\+:\s]+\])?\s*(\w+)')
    ]
    
    # 参数定义模式
    param_pattern = re.compile(r'\b(?:parameter|localparam)\s+(\w+)\s*=\s*([^,;]+)')
    
    # 模块实例化模式
    instance_pattern = re.compile(r'\.(\w+)')
    module_pattern = re.compile(r'\bmodule\s+(\w+)')
    
    instance_module_patterns = [
        re.compile(r'(\w+)\s+\w+\s\(\.\w+'),
        re.compile(r'\w+\s+(\w+)\s\(\.\w+'),
        re.compile(r'(\w+)\s+(\w+)\s*\(')
    ]

    # 处理每一行
    for line in lines:
        line = remove_comments(line)
        
        # 1. 收集所有可能的标识符，保持顺序
        for signal in signal_pattern.findall(line):
            # 将每个信号添加到OrderedDict，键为信号名，值不重要
            if signal not in signals_ordered:
                signals_ordered[signal] = True
        
        # 2. 识别已定义的信号
        for pattern in define_patterns:
            defined_signals.update(pattern.findall(line))
        
        # 3. 收集模块实例化信号
        module_instance_signals.update(instance_pattern.findall(line))
        
        # 4. 识别模块名和实例模块名
        for pattern in instance_module_patterns:
            instance_module_names.extend(pattern.findall(line))
            
        module_match = module_pattern.search(line)
        if module_match:
            module_names.add(module_match.group(1))
            
        # 5. 收集参数定义
        for name, value in param_pattern.findall(line):
            parameter_values[name] = value.strip()

    # 6. 处理实例模块名（扁平化并去重）
    flat_instance_names = [item for sublist in instance_module_names for item in (sublist if isinstance(sublist, tuple) else [sublist])]
    set_instance_names = set(flat_instance_names)
    
    # 7. 按照原始顺序筛选未定义信号
    undefined_signals = []
    exclude_set = VERILOG_KEYWORDS | defined_signals | module_names | set_instance_names | module_instance_signals | set(parameter_values.keys())
    
    # 更新排除集合，添加数字
    number_pattern = re.compile(r'^\d+$')
    exclude_numbers = {signal for signal in signals_ordered if number_pattern.match(signal)}
    exclude_set.update(exclude_numbers)
    
    for signal in signals_ordered:
        if signal not in exclude_set:
            undefined_signals.append(signal)
    
    # 8. 提取位宽信息（如果需要）
    signal_widths = {}
    if extract_width:
        for signal in undefined_signals:
            signal_widths[signal] = extract_bitwidth(content, signal)
    
    return undefined_signals, signal_widths

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
            width = default_width
            
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
  
用法示例：
  # 基本用法：生成单独的wire声明文件
  python auto_wire.py my_design.v
  
  # 自动检测位宽
  python auto_wire.py --width my_design.v
  
  # 应用默认位宽
  python auto_wire.py --default-width "[31:0]" my_design.v
  
  # 直接追加到原始文件
  python auto_wire.py --append my_design.v
  
  # 指定输出目录
  python auto_wire.py --output-dir ./generated my_design.v
    """
    print(help_text)

def main() -> None:
    """主函数：解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(description='Verilog自动线网声明工具')
    parser.add_argument('file', help='Verilog源文件路径')
    parser.add_argument('--width', '-w', action='store_true', help='尝试提取信号位宽')
    parser.add_argument('--default-width', '-d', type=str, help='默认位宽，如 "[7:0]"')
    parser.add_argument('--append', '-a', action='store_true', help='将定义追加到原始文件')
    parser.add_argument('--output-dir', '-o', type=str, help='输出目录路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--help-detail', action='store_true', help='显示详细使用说明')

    args = parser.parse_args()
    
    if args.help_detail:
        print_help()
        return

    file_name = args.file
    extract_width = args.width
    default_width = args.default_width
    
    # 解析Verilog文件
    undefined_signals, signal_widths = parse_verilog(file_name, extract_width)

    if undefined_signals:
        if args.verbose:
            print(f"发现未定义信号：{', '.join(undefined_signals)}")
            if extract_width:
                for signal in undefined_signals:
                    width = signal_widths.get(signal)
                    print(f"  {signal}: {'无位宽信息' if width is None else width}")
        else:
            print(f"发现未定义信号：{len(undefined_signals)}个")
        
        # 生成定义
        definitions = generate_signal_definitions(undefined_signals, signal_widths, default_width)
        
        # 输出定义
        if args.append:
            append_to_original(file_name, definitions)
        else:
            write_output(file_name, definitions, args.output_dir)
    else:
        print("未发现未定义信号。")

if __name__ == "__main__":
    main()