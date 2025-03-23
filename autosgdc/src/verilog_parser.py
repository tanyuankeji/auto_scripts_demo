#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verilog解析器模块 - 负责解析Verilog文件并提取关键信息

此模块提供用于解析Verilog文件的类和方法，包括:
- 解析模块定义和端口
- 提取信号和时钟
- 分析信号连接和层次结构
- 支持包含文件和多文件分析
"""

import os
import re
import logging
from typing import List, Dict, Tuple, Set, Optional, Union, Any
from dataclasses import dataclass, field

from utils import setup_logger, is_clock_name, is_reset_name, remove_comments

# 设置日志
logger = setup_logger('verilog_parser')

@dataclass
class VerilogPort:
    """Verilog端口定义"""
    name: str                        # 端口名称
    direction: str                   # 方向(input/output/inout)
    width: str = ""                  # 位宽，如[7:0]
    is_reg: bool = False             # 是否为reg类型
    is_wire: bool = False            # 是否为wire类型
    is_clock: bool = False           # 是否可能是时钟
    is_reset: bool = False           # 是否可能是复位
    
    def __post_init__(self):
        """初始化后检查端口名称是否是时钟或复位"""
        self.is_clock = is_clock_name(self.name)
        self.is_reset = is_reset_name(self.name)

@dataclass
class VerilogSignal:
    """Verilog内部信号定义"""
    name: str                        # 信号名称
    type: str                        # 类型(reg/wire)
    width: str = ""                  # 位宽
    is_clock: bool = False           # 是否可能是时钟
    is_reset: bool = False           # 是否可能是复位
    
    def __post_init__(self):
        """初始化后检查信号名称是否是时钟或复位"""
        self.is_clock = is_clock_name(self.name)
        self.is_reset = is_reset_name(self.name)

@dataclass
class ModuleInstance:
    """模块实例化信息"""
    module_name: str                 # 模块名称
    instance_name: str               # 实例名称
    port_connections: Dict[str, str] = field(default_factory=dict)  # 端口连接

@dataclass
class VerilogModule:
    """Verilog模块定义"""
    name: str                        # 模块名称
    file_path: str                   # 文件路径
    content: str                     # 模块内容
    ports: Dict[str, VerilogPort] = field(default_factory=dict)  # 端口
    signals: Dict[str, VerilogSignal] = field(default_factory=dict)  # 内部信号
    instances: List[ModuleInstance] = field(default_factory=list)  # 模块实例
    is_instantiated: bool = False    # 是否被其他模块实例化
    
    def identify_clock_signals(self) -> List[str]:
        """识别模块中的时钟信号"""
        clock_signals = []
        
        # 检查端口中的时钟
        for name, port in self.ports.items():
            if port.is_clock and port.direction == 'input':
                clock_signals.append(name)
        
        # 检查内部信号中的时钟
        for name, signal in self.signals.items():
            if signal.is_clock and signal.type == 'wire':
                # 内部生成的时钟信号，通常来自时钟缓冲器或分频器
                clock_signals.append(name)
        
        return sorted(list(set(clock_signals)))
    
    def find_clock_domains(self) -> Dict[str, Set[str]]:
        """
        识别模块中的时钟域和属于每个时钟域的信号
        
        返回:
            字典，键为时钟名，值为这个时钟域中的信号集合
        """
        clock_domains = {}
        
        # 识别所有时钟信号
        clocks = self.identify_clock_signals()
        
        # 为每个时钟创建一个域
        for clock in clocks:
            clock_domains[clock] = set()
        
        # 解析always块，确定信号所属的时钟域
        # 移除注释，避免干扰
        content_no_comments = remove_comments(self.content)
        
        # 提取always块和敏感列表
        always_blocks = re.finditer(
            r'always\s*@\s*\((.*?)\)(.*?)(?=always|endmodule|$)', 
            content_no_comments, 
            re.DOTALL
        )
        
        for match in always_blocks:
            sensitivity = match.group(1)  # 敏感列表
            block_content = match.group(2)  # always块内容
            
            # 确定这个always块使用的时钟
            block_clock = None
            for clock in clocks:
                # 检查时钟是否在敏感列表中
                if re.search(rf'\b{re.escape(clock)}\b', sensitivity):
                    # 确认是在上升沿或下降沿
                    if re.search(rf'pos\w*\s*\(\s*{re.escape(clock)}\s*\)', sensitivity) or \
                       re.search(rf'neg\w*\s*\(\s*{re.escape(clock)}\s*\)', sensitivity):
                        block_clock = clock
                        break
            
            # 如果找到了时钟，提取这个always块中赋值的信号
            if block_clock:
                # 查找非阻塞赋值 (<=)
                assignments = re.findall(r'(\w+)\s*<=', block_content)
                
                # 添加到对应的时钟域
                for signal in assignments:
                    if signal in self.signals and self.signals[signal].type == 'reg':
                        clock_domains[block_clock].add(signal)
        
        return clock_domains

class VerilogParser:
    """Verilog文件解析器"""
    
    def __init__(self, verilog_files: Union[str, List[str]], include_dirs: List[str] = None):
        """
        初始化解析器
        
        参数:
            verilog_files: 单个Verilog文件路径或文件路径列表
            include_dirs: 包含目录列表，用于查找include文件
        """
        if isinstance(verilog_files, str):
            self.verilog_files = [verilog_files]
        else:
            self.verilog_files = verilog_files
            
        self.include_dirs = include_dirs or []
        self.modules = {}  # 所有解析到的模块
    
    def parse_all(self) -> Dict[str, VerilogModule]:
        """
        解析所有指定的Verilog文件
        
        返回:
            字典，键为模块名，值为模块对象
        """
        # 首先解析所有文件中的模块
        for file_path in self.verilog_files:
            self._parse_file(file_path)
        
        # 然后构建模块实例化关系
        self._build_instance_relationships()
        
        return self.modules
    
    def _parse_file(self, file_path: str) -> None:
        """
        解析单个Verilog文件
        
        参数:
            file_path: Verilog文件路径
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 处理包含文件
            content = self._process_includes(content, os.path.dirname(file_path))
            
            # 提取模块定义
            self._extract_modules(content, file_path)
            
        except Exception as e:
            logger.error(f"解析文件 {file_path} 时出错: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
    
    def _process_includes(self, content: str, base_dir: str) -> str:
        """
        处理Verilog文件中的include指令
        
        参数:
            content: 文件内容
            base_dir: 基础目录，用于相对路径
            
        返回:
            处理后的内容
        """
        def replace_include(match):
            include_file = match.group(1).strip('"\'')
            
            # 查找include文件
            include_path = None
            
            # 首先检查相对于当前文件的路径
            rel_path = os.path.join(base_dir, include_file)
            if os.path.exists(rel_path):
                include_path = rel_path
            else:
                # 然后检查include目录
                for inc_dir in self.include_dirs:
                    inc_path = os.path.join(inc_dir, include_file)
                    if os.path.exists(inc_path):
                        include_path = inc_path
                        break
            
            if include_path:
                try:
                    with open(include_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    logger.warning(f"读取包含文件 {include_path} 时出错: {str(e)}")
                    return f"// ERROR: 无法读取包含文件 {include_file}"
            else:
                logger.warning(f"找不到包含文件: {include_file}")
                return f"// ERROR: 找不到包含文件 {include_file}"
        
        # 替换所有`include指令
        return re.sub(r'`include\s+(["\']\S+["\'])', replace_include, content)
    
    def _extract_modules(self, content: str, file_path: str) -> None:
        """
        从内容中提取所有模块定义
        
        参数:
            content: 文件内容
            file_path: 文件路径
        """
        # 移除注释
        content_no_comments = remove_comments(content)
        
        # 查找所有模块定义
        # 模式: 从module开始到endmodule结束
        module_pattern = r'module\s+(\w+)[\s\S]*?endmodule'
        
        for match in re.finditer(module_pattern, content_no_comments):
            module_content = match.group(0)
            module_name = match.group(1)
            
            logger.debug(f"在文件 {file_path} 中找到模块: {module_name}")
            
            # 创建模块对象
            module = VerilogModule(
                name=module_name,
                file_path=file_path,
                content=module_content
            )
            
            # 提取端口
            self._extract_ports(module)
            
            # 提取内部信号
            self._extract_signals(module)
            
            # 提取模块实例化
            self._extract_instances(module)
            
            # 添加到模块字典
            self.modules[module_name] = module
    
    def _extract_ports(self, module: VerilogModule) -> None:
        """
        提取模块的端口定义
        
        参数:
            module: 模块对象
        """
        # 查找端口列表
        # 假设端口列表在module关键字后的括号内
        port_list_match = re.search(r'module\s+\w+\s*\((.*?)\)', module.content, re.DOTALL)
        
        if port_list_match:
            port_list = port_list_match.group(1).strip()
            
            # 提取所有端口名称
            port_names = []
            for port in re.split(r',\s*', port_list):
                port = port.strip()
                if port:
                    port_names.append(port)
            
            # 查找端口方向和类型定义
            port_defs = {}
            
            # 查找输入端口
            input_matches = re.finditer(
                r'input\s+(reg|wire)?\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s*(\w+(?:\s*,\s*\w+)*)',
                module.content
            )
            for match in input_matches:
                type_str = match.group(1) or ""
                width_str = match.group(2) or ""
                names_str = match.group(3)
                
                for name in re.split(r',\s*', names_str):
                    name = name.strip()
                    port_defs[name] = {
                        'direction': 'input',
                        'type': type_str,
                        'width': width_str
                    }
            
            # 查找输出端口
            output_matches = re.finditer(
                r'output\s+(reg|wire)?\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s*(\w+(?:\s*,\s*\w+)*)',
                module.content
            )
            for match in output_matches:
                type_str = match.group(1) or ""
                width_str = match.group(2) or ""
                names_str = match.group(3)
                
                for name in re.split(r',\s*', names_str):
                    name = name.strip()
                    port_defs[name] = {
                        'direction': 'output',
                        'type': type_str,
                        'width': width_str
                    }
            
            # 查找双向端口
            inout_matches = re.finditer(
                r'inout\s+(reg|wire)?\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s*(\w+(?:\s*,\s*\w+)*)',
                module.content
            )
            for match in inout_matches:
                type_str = match.group(1) or ""
                width_str = match.group(2) or ""
                names_str = match.group(3)
                
                for name in re.split(r',\s*', names_str):
                    name = name.strip()
                    port_defs[name] = {
                        'direction': 'inout',
                        'type': type_str,
                        'width': width_str
                    }
            
            # 创建端口对象
            for name in port_names:
                if name in port_defs:
                    port_def = port_defs[name]
                    port = VerilogPort(
                        name=name,
                        direction=port_def['direction'],
                        width=port_def['width'],
                        is_reg=port_def['type'].lower() == 'reg',
                        is_wire=port_def['type'].lower() == 'wire'
                    )
                    module.ports[name] = port
                else:
                    # 如果找不到定义，假设是线型输入
                    logger.warning(f"模块 {module.name} 中的端口 {name} 未找到定义，假设为wire input")
                    port = VerilogPort(
                        name=name,
                        direction='input',
                        is_wire=True
                    )
                    module.ports[name] = port
    
    def _extract_signals(self, module: VerilogModule) -> None:
        """
        提取模块内部信号定义
        
        参数:
            module: 模块对象
        """
        # 提取wire信号
        wire_matches = re.finditer(
            r'\bwire\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s*(\w+(?:\s*,\s*\w+)*)',
            module.content
        )
        for match in wire_matches:
            width_str = match.group(1) or ""
            names_str = match.group(2)
            
            for name in re.split(r',\s*', names_str):
                name = name.strip()
                # 避免重复添加端口信号
                if name not in module.ports:
                    signal = VerilogSignal(
                        name=name,
                        type='wire',
                        width=width_str
                    )
                    module.signals[name] = signal
        
        # 提取reg信号
        reg_matches = re.finditer(
            r'\breg\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s*(\w+(?:\s*,\s*\w+)*)',
            module.content
        )
        for match in reg_matches:
            width_str = match.group(1) or ""
            names_str = match.group(2)
            
            for name in re.split(r',\s*', names_str):
                name = name.strip()
                # 避免重复添加端口信号
                if name not in module.ports:
                    signal = VerilogSignal(
                        name=name,
                        type='reg',
                        width=width_str
                    )
                    module.signals[name] = signal
    
    def _extract_instances(self, module: VerilogModule) -> None:
        """
        提取模块实例化
        
        参数:
            module: 模块对象
        """
        # 查找模块实例化
        # 基本模式: module_name instance_name ( ... );
        instance_pattern = r'(\w+)\s+(\w+)\s*\(([\s\S]*?)\)\s*;'
        
        for match in re.finditer(instance_pattern, module.content):
            inst_module = match.group(1)
            inst_name = match.group(2)
            ports_text = match.group(3)
            
            # 跳过可能是Verilog原语的情况
            if inst_module in ('and', 'or', 'not', 'xor', 'nand', 'nor', 'xnor', 'buf'):
                continue
            
            # 创建实例对象
            instance = ModuleInstance(
                module_name=inst_module,
                instance_name=inst_name
            )
            
            # 提取端口连接
            # 可能的格式:
            # .port_name(signal_name) - 命名连接
            # signal_name - 位置连接
            port_connections = {}
            
            # 处理命名连接
            named_connections = re.finditer(r'\.(\w+)\s*\(\s*([^)]+)\s*\)', ports_text)
            for conn_match in named_connections:
                port_name = conn_match.group(1)
                signal_name = conn_match.group(2).strip()
                port_connections[port_name] = signal_name
            
            # 如果没有命名连接，尝试位置连接
            if not port_connections:
                positional_signals = re.split(r',\s*', ports_text)
                for i, signal in enumerate(positional_signals):
                    signal = signal.strip()
                    if signal:
                        # 使用索引作为临时端口名
                        port_connections[f"PORT_{i}"] = signal
            
            instance.port_connections = port_connections
            module.instances.append(instance)
    
    def _build_instance_relationships(self) -> None:
        """构建模块间的实例化关系"""
        # 重置所有模块的实例化状态
        for module in self.modules.values():
            module.is_instantiated = False
        
        # 标记被实例化的模块
        for module in self.modules.values():
            for instance in module.instances:
                inst_module_name = instance.module_name
                if inst_module_name in self.modules:
                    self.modules[inst_module_name].is_instantiated = True
                
        # 计算可能的顶层模块
        top_candidates = [m.name for m in self.modules.values() if not m.is_instantiated]
        if top_candidates:
            logger.debug(f"可能的顶层模块: {', '.join(top_candidates)}") 