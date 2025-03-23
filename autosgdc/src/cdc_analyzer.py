#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CDC分析器模块 - 负责检测跨时钟域信号

此模块提供检测跨时钟域信号的功能，包括:
- 根据时钟域划分分析信号流向
- 检测信号跨时钟域传输
- 识别常见的CDC同步结构
- 提供CDC分析报告
"""

import re
import logging
from typing import List, Dict, Tuple, Set, Optional, Union, Any

from utils import setup_logger, is_synchronizer
from verilog_parser import VerilogModule

# 设置日志
logger = setup_logger('cdc_analyzer')

class CDCAnalyzer:
    """CDC分析器，用于检测跨时钟域信号"""
    
    def __init__(self, modules: Dict[str, VerilogModule], top_module_name: str):
        """
        初始化CDC分析器
        
        参数:
            modules: 所有解析到的模块字典，键为模块名
            top_module_name: 顶层模块名称
        """
        self.modules = modules
        self.top_module_name = top_module_name
        
        # 确保顶层模块存在
        if top_module_name not in modules:
            logger.error(f"指定的顶层模块 {top_module_name} 未找到")
            raise ValueError(f"模块 {top_module_name} 未找到")
            
        self.top_module = modules[top_module_name]
        
        # 初始化时钟域字典和跨时钟域信号字典
        self.clock_domains = {}      # 时钟域，键为时钟名，值为信号集合
        self.cdc_signals = {}        # 跨时钟域信号，键为"src_clk->dst_clk"，值为信号列表
        self.synchronizers = {}      # 已识别的同步器，键为目标时钟，值为同步器信号列表
    
    def detect_cdc(self) -> Dict[str, List[str]]:
        """
        检测跨时钟域信号
        
        返回:
            字典，键为"src_clk->dst_clk"，值为跨时钟域信号列表
        """
        # 首先识别所有时钟信号
        clocks = self.top_module.identify_clock_signals()
        
        if len(clocks) <= 1:
            logger.info("只检测到一个或零个时钟，无需CDC分析")
            return {}
        
        # 对每个时钟构建时钟域
        logger.debug("开始构建时钟域...")
        self._build_clock_domains(clocks)
        
        # 检测跨时钟域信号
        logger.debug("开始检测跨时钟域信号...")
        self._detect_cdc_signals()
        
        # 识别同步器
        logger.debug("开始识别同步器...")
        self._identify_synchronizers()
        
        return self.cdc_signals
    
    def _build_clock_domains(self, clocks: List[str]) -> None:
        """
        构建每个时钟的时钟域
        
        参数:
            clocks: 时钟信号列表
        """
        # 初始化时钟域
        for clock in clocks:
            self.clock_domains[clock] = set()
        
        # 从顶层模块开始，递归分析每个模块的时钟域
        self._analyze_module_clock_domains(self.top_module)
    
    def _analyze_module_clock_domains(self, module: VerilogModule) -> None:
        """
        分析单个模块的时钟域
        
        参数:
            module: 要分析的模块
        """
        # 获取模块内的时钟域划分
        module_domains = module.find_clock_domains()
        
        # 合并到全局时钟域
        for clock, signals in module_domains.items():
            if clock in self.clock_domains:
                # 对于顶层模块中的信号，直接添加
                for signal in signals:
                    self.clock_domains[clock].add(f"{module.name}.{signal}")
        
        # 递归分析实例化的子模块
        for instance in module.instances:
            inst_module_name = instance.module_name
            if inst_module_name in self.modules:
                # 递归分析子模块
                inst_module = self.modules[inst_module_name]
                self._analyze_module_clock_domains(inst_module)
    
    def _detect_cdc_signals(self) -> None:
        """检测跨时钟域信号"""
        # 检查每个时钟域中的信号
        for src_clock, src_signals in self.clock_domains.items():
            for dst_clock, dst_signals in self.clock_domains.items():
                if src_clock != dst_clock:  # 不同时钟域
                    # 寻找潜在的CDC信号
                    cdc_key = f"{src_clock}->{dst_clock}"
                    self.cdc_signals[cdc_key] = []
                    
                    # 分析从源时钟域流向目标时钟域的信号
                    self._analyze_signal_flow(src_clock, dst_clock, src_signals, dst_signals)
    
    def _analyze_signal_flow(self, src_clock: str, dst_clock: str, 
                            src_signals: Set[str], dst_signals: Set[str]) -> None:
        """
        分析从源时钟域到目标时钟域的信号流
        
        参数:
            src_clock: 源时钟名称
            dst_clock: 目标时钟名称
            src_signals: 源时钟域中的信号集合
            dst_signals: 目标时钟域中的信号集合
        """
        # 遍历每个目标时钟域中的信号，检查其是否使用了源时钟域的信号
        # 这里采用简化的方法：检查模块内容中是否存在源信号流向目标信号的赋值
        for src_module_signal in src_signals:
            # 提取模块名和信号名
            if '.' in src_module_signal:
                src_module, src_signal = src_module_signal.split('.', 1)
            else:
                continue  # 跳过不完整的信号引用
                
            # 检查该源信号是否被目标时钟域使用
            for dst_module_signal in dst_signals:
                if '.' in dst_module_signal:
                    dst_module, dst_signal = dst_module_signal.split('.', 1)
                else:
                    continue  # 跳过不完整的信号引用
                
                # 如果源模块和目标模块相同，检查信号赋值关系
                if src_module == dst_module and src_module in self.modules:
                    module = self.modules[src_module]
                    
                    # 检查是否有从源信号到目标信号的赋值
                    # 注意：这是一个简化的检查，实际上需要更复杂的数据流分析
                    if self._check_signal_assignment(module, src_signal, dst_signal):
                        cdc_key = f"{src_clock}->{dst_clock}"
                        if src_signal not in self.cdc_signals[cdc_key]:
                            self.cdc_signals[cdc_key].append(src_signal)
    
    def _check_signal_assignment(self, module: VerilogModule, 
                                src_signal: str, dst_signal: str) -> bool:
        """
        检查模块中是否存在从源信号到目标信号的赋值
        
        参数:
            module: 要检查的模块
            src_signal: 源信号名
            dst_signal: 目标信号名
            
        返回:
            如果存在赋值关系则返回True
        """
        # 简化的检查：查找是否有类似 dst_signal = ... src_signal ... 的语句
        # 这里仅做基本检查，实际上需要更完整的解析器
        assignment_pattern = fr'{dst_signal}\s*(?:=|<=)\s*[^;]*\b{src_signal}\b'
        return bool(re.search(assignment_pattern, module.content))
    
    def _identify_synchronizers(self) -> None:
        """识别常见的CDC同步器结构"""
        # 对每个跨时钟域路径
        for cdc_path, signals in self.cdc_signals.items():
            src_clock, dst_clock = cdc_path.split('->')
            
            # 同步器集合，键为同步信号输入，值为同步器链中的所有信号
            synchronizers = {}
            
            # 对于每个潜在的CDC信号，检查是否有同步器
            for signal in signals[:]:  # 创建副本以便在迭代时修改
                # 在目标时钟域中查找可能是同步器的信号
                sync_candidates = self._find_sync_candidates(signal, dst_clock)
                
                if sync_candidates and len(sync_candidates) >= 2:
                    # 检查这些信号是否构成同步器
                    if self._check_synchronizer_structure(sync_candidates, signal, dst_clock):
                        # 找到了同步器，记录下来
                        synchronizers[signal] = sync_candidates
                        
                        # 从CDC信号列表中移除这个信号，因为它已被同步
                        self.cdc_signals[cdc_path].remove(signal)
            
            # 记录识别到的同步器
            if synchronizers:
                self.synchronizers[dst_clock] = synchronizers
    
    def _find_sync_candidates(self, signal: str, dst_clock: str) -> List[str]:
        """
        查找可能是同步器的信号
        
        参数:
            signal: 输入信号名
            dst_clock: 目标时钟域
            
        返回:
            可能构成同步器的信号列表
        """
        # 常见的同步器命名模式
        # 例如: signal_sync, signal_sync1, signal_sync2, ...
        sync_candidates = []
        
        # 在目标时钟域中的所有信号中查找
        for dom_signal in self.clock_domains.get(dst_clock, set()):
            if '.' in dom_signal:
                module_name, signal_name = dom_signal.split('.', 1)
            else:
                continue
                
            # 检查是否匹配同步器命名模式
            if (signal_name.startswith(f"{signal}_sync") or 
                signal_name == f"{signal}_meta" or
                (signal_name.startswith(signal) and signal_name.endswith("_sync"))):
                sync_candidates.append(signal_name)
        
        return sorted(sync_candidates)
    
    def _check_synchronizer_structure(self, sync_candidates: List[str], 
                                     input_signal: str, dst_clock: str) -> bool:
        """
        检查信号列表是否构成同步器结构
        
        参数:
            sync_candidates: 候选同步器信号列表
            input_signal: 输入信号
            dst_clock: 目标时钟域
            
        返回:
            如果构成同步器则返回True
        """
        # 检查是否至少有2个触发器
        if len(sync_candidates) < 2:
            return False
        
        # 找到包含这些信号的模块
        containing_module = None
        for module in self.modules.values():
            all_found = True
            for sig in sync_candidates:
                if sig not in module.signals:
                    all_found = False
                    break
            if all_found:
                containing_module = module
                break
        
        if not containing_module:
            return False
        
        # 使用辅助函数检查是否构成同步器
        return is_synchronizer(sync_candidates, containing_module.content)
    
    def get_report(self) -> str:
        """
        生成CDC分析报告
        
        返回:
            格式化的CDC分析报告字符串
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("CDC分析报告")
        report_lines.append("=" * 80)
        
        # 报告时钟域
        report_lines.append("\n时钟域信息:")
        report_lines.append("-" * 40)
        for clock, signals in self.clock_domains.items():
            report_lines.append(f"时钟 {clock}: {len(signals)} 个信号")
        
        # 报告同步器
        report_lines.append("\n识别到的同步器:")
        report_lines.append("-" * 40)
        if self.synchronizers:
            for dst_clock, sync_dict in self.synchronizers.items():
                report_lines.append(f"目标时钟域 {dst_clock}:")
                for input_signal, sync_signals in sync_dict.items():
                    report_lines.append(f"  输入信号 {input_signal} -> 同步器: {', '.join(sync_signals)}")
        else:
            report_lines.append("未检测到同步器")
        
        # 报告未同步的CDC信号
        report_lines.append("\n未同步的跨时钟域信号:")
        report_lines.append("-" * 40)
        if any(signals for signals in self.cdc_signals.values()):
            for cdc_path, signals in self.cdc_signals.items():
                if signals:  # 只报告非空的路径
                    report_lines.append(f"路径 {cdc_path}: {len(signals)} 个信号")
                    for signal in signals:
                        report_lines.append(f"  - {signal}")
        else:
            report_lines.append("未检测到未同步的跨时钟域信号")
        
        report_lines.append("\n" + "=" * 80)
        return "\n".join(report_lines) 