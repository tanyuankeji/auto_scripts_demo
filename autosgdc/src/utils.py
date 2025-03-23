#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具类模块 - 提供日志设置和辅助函数

此模块包含工具程序所需的通用工具函数，如日志配置、文件读写、
字符串处理等辅助功能。
"""

import os
import re
import logging
from typing import List, Dict, Tuple, Set, Optional, Any

def setup_logger(name: str = 'autosgdc', level: int = logging.INFO) -> logging.Logger:
    """
    设置和配置日志器
    
    参数:
        name: 日志器名称
        level: 日志级别
        
    返回:
        配置好的日志器对象
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 如果已经有处理器，则不再添加
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 设置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志器
    logger.addHandler(console_handler)
    
    return logger

def is_clock_name(signal_name: str) -> bool:
    """
    判断信号名是否可能是时钟
    
    参数:
        signal_name: 信号名称
        
    返回:
        如果信号名可能是时钟则返回True
    """
    # 常见的时钟命名模式
    clock_patterns = [
        r'^clk\w*$',                  # 以clk开头
        r'^clock\w*$',                # 以clock开头
        r'^\w*_clk\w*$',              # 包含_clk
        r'^\w*_clock\w*$',            # 包含_clock
        r'^\w*clk_\w*$',              # 包含clk_
        r'^\w*clock_\w*$',            # 包含clock_
        r'^clk$', r'^clock$',         # 精确匹配clk或clock
        r'.*_clk$', r'.*_clock$',     # 以_clk或_clock结尾
        r'^gclk\w*$', r'^gclk$',      # 全局时钟
        r'^pclk\w*$', r'^pclk$',      # 外设时钟
        r'^sclk\w*$', r'^sclk$',      # 系统时钟
        r'^aclk\w*$', r'^aclk$',      # AXI时钟
        r'^mclk\w*$', r'^mclk$',      # 主时钟
    ]
    
    # 将所有模式合并为一个正则表达式，不区分大小写
    combined_pattern = '|'.join(clock_patterns)
    return bool(re.match(combined_pattern, signal_name, re.IGNORECASE))

def is_reset_name(signal_name: str) -> bool:
    """
    判断信号名是否可能是复位
    
    参数:
        signal_name: 信号名称
        
    返回:
        如果信号名可能是复位则返回True
    """
    # 常见的复位命名模式
    reset_patterns = [
        r'^rst\w*$',                  # 以rst开头
        r'^reset\w*$',                # 以reset开头
        r'^\w*_rst\w*$',              # 包含_rst
        r'^\w*_reset\w*$',            # 包含_reset
        r'^\w*rst_\w*$',              # 包含rst_
        r'^\w*reset_\w*$',            # 包含reset_
        r'^rst$', r'^reset$',         # 精确匹配rst或reset
        r'.*_rst$', r'.*_reset$',     # 以_rst或_reset结尾
        r'^resetn\w*$', r'^rstn\w*$', # 低电平有效复位
        r'^arst\w*$', r'^areset\w*$', # 异步复位
        r'^srst\w*$', r'^sreset\w*$', # 同步复位
    ]
    
    # 将所有模式合并为一个正则表达式，不区分大小写
    combined_pattern = '|'.join(reset_patterns)
    return bool(re.match(combined_pattern, signal_name, re.IGNORECASE))

def extract_module_name(content: str) -> str:
    """
    从Verilog内容中提取模块名称
    
    参数:
        content: Verilog文件内容
        
    返回:
        模块名称，如果未找到则返回空字符串
    """
    # 移除注释，避免干扰
    content_no_comments = remove_comments(content)
    
    # 匹配模块声明
    module_match = re.search(r'module\s+(\w+)', content_no_comments)
    if module_match:
        return module_match.group(1)
    return ""

def remove_comments(content: str) -> str:
    """
    移除Verilog内容中的注释
    
    参数:
        content: 包含注释的Verilog代码
        
    返回:
        移除注释后的Verilog代码
    """
    # 移除单行注释
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    
    # 移除多行注释
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    return content

def is_synchronizer(signals: List[str], content: str) -> bool:
    """
    检测给定信号列表是否构成同步器
    
    参数:
        signals: 信号列表
        content: Verilog代码内容
        
    返回:
        如果信号构成同步器则返回True
    """
    # 同步器通常包含2个或以上连续的触发器
    if len(signals) < 2:
        return False
    
    # 检查信号命名模式，同步器通常命名为xx_sync, xx_sync1, xx_sync2等
    base_name = None
    for i, signal in enumerate(signals):
        # 尝试提取基本名称
        sync_match = re.match(r'^(.+?)_sync\d*$', signal)
        if sync_match:
            current_base = sync_match.group(1)
            if base_name is None:
                base_name = current_base
            elif base_name != current_base:
                return False
        else:
            # 如果不匹配同步器命名模式，检查数字后缀
            digits_match = re.match(r'^(.+?)(\d+)$', signal)
            if digits_match:
                current_base = digits_match.group(1)
                if base_name is None:
                    base_name = current_base
                elif base_name != current_base:
                    return False
            else:
                # 如果没有数字后缀，则不太可能是同步器
                return False
    
    # 检查信号之间是否有直接连接关系
    for i in range(len(signals) - 1):
        # 检查是否有类似 assign signals[i+1] = signals[i]; 的语句
        assignment_pattern = fr'{signals[i+1]}\s*<=\s*{signals[i]}'
        if not re.search(assignment_pattern, content):
            # 如果没有找到直接赋值，可能不是同步器
            return False
    
    return True

def get_module_instantiations(content: str) -> Dict[str, List[str]]:
    """
    提取模块中的所有实例化
    
    参数:
        content: Verilog代码内容
        
    返回:
        字典，键为模块名，值为实例名列表
    """
    # 移除注释
    content_no_comments = remove_comments(content)
    
    # 查找模块实例化
    instances = {}
    
    # 匹配模式: module_name instance_name ( ... );
    instance_pattern = r'(\w+)\s+(\w+)\s*\('
    for match in re.finditer(instance_pattern, content_no_comments):
        module_name = match.group(1)
        instance_name = match.group(2)
        
        if module_name not in instances:
            instances[module_name] = []
        
        instances[module_name].append(instance_name)
    
    return instances

def is_clock_buffer(module_name: str) -> bool:
    """
    判断模块是否可能是时钟缓冲器
    
    参数:
        module_name: 模块名称
        
    返回:
        如果模块可能是时钟缓冲器则返回True
    """
    # 常见的时钟缓冲器/生成器名称
    clock_buffer_patterns = [
        r'BUFG', r'BUFH', r'BUFR',    # Xilinx缓冲器
        r'BUFGCE', r'BUFHCE',         # Xilinx使能缓冲器
        r'MMCM', r'PLL',              # 时钟管理器
        r'IBUFDS',                    # 差分输入缓冲器
        r'clk_div', r'clock_div',     # 时钟分频器
        r'clk_gen', r'clock_gen',     # 时钟生成器
        r'clk_buf', r'clock_buf',     # 通用时钟缓冲器
        r'CLK\w*BUF',                 # 任何类型的时钟缓冲器
    ]
    
    combined_pattern = '|'.join(clock_buffer_patterns)
    return bool(re.match(combined_pattern, module_name, re.IGNORECASE)) 