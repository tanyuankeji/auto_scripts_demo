# analyzer.py
"""
信号分析器模块
负责分析Verilog代码中的信号定义和使用
"""

from typing import List, Dict, Set, Optional
from collections import OrderedDict

from .parser import VerilogParser
from .utils import AnalysisError, format_width

class SignalAnalyzer:
    """信号分析器类"""
    
    def __init__(self):
        """初始化分析器"""
        self.parser = None
        self.undefined_signals = []
        self.signal_widths = {}
        self.default_width = None
        self.exclude_patterns = []
        
    def setup(self, parser: VerilogParser, exclude_patterns: List[str] = None, default_width: Optional[str] = None) -> None:
        """
        设置分析器
        
        参数:
            parser: Verilog解析器实例
            exclude_patterns: 排除模式列表
            default_width: 默认位宽
        """
        self.parser = parser
        self.exclude_patterns = exclude_patterns or []
        self.default_width = default_width
        
    def analyze(self) -> None:
        """
        分析信号
        
        异常:
            AnalysisError: 分析失败
        """
        if not self.parser:
            raise AnalysisError("分析器未设置解析器")
            
        # 获取未定义信号
        self.undefined_signals = self.parser.get_undefined_signals(self.exclude_patterns)
        
        # 提取信号位宽
        self.analyze_signal_widths()
        
    def analyze_signal_widths(self) -> None:
        """分析信号位宽"""
        if not self.parser:
            raise AnalysisError("分析器未设置解析器")
            
        self.signal_widths = self.parser.get_signal_widths(self.undefined_signals)
        
    def get_undefined_signals(self) -> List[str]:
        """
        获取未定义信号列表
        
        返回:
            未定义信号列表
        """
        return self.undefined_signals
        
    def get_signal_width(self, signal: str) -> Optional[str]:
        """
        获取信号位宽
        
        参数:
            signal: 信号名
            
        返回:
            位宽字符串，如果无法确定且无默认值则返回None
        """
        width = self.signal_widths.get(signal)
        if width is None and self.default_width:
            return self._process_default_width()
        return width
        
    def _process_default_width(self) -> str:
        """
        处理默认位宽
        
        返回:
            格式化后的默认位宽
        """
        if not self.default_width:
            return ""
            
        # 处理数字格式 (如 "32" -> "[31:0]")
        if self.default_width.isdigit():
            width = int(self.default_width)
            return f"[{width-1}:0]"
            
        # 处理已有的位宽格式 (如 "[7:0]")
        return format_width(self.default_width)
        
    def get_formatted_signal_widths(self) -> Dict[str, str]:
        """
        获取格式化的信号位宽字典
        
        返回:
            信号名到格式化位宽的字典
        """
        formatted_widths = {}
        for signal in self.undefined_signals:
            width = self.get_signal_width(signal)
            if width:
                formatted_widths[signal] = format_width(width)
            else:
                formatted_widths[signal] = ""
        return formatted_widths
        
    def get_signal_definitions(self) -> Dict[str, str]:
        """
        获取信号定义字典
        
        返回:
            信号名到定义的字典
        """
        definitions = OrderedDict()
        formatted_widths = self.get_formatted_signal_widths()
        
        for signal in self.undefined_signals:
            width = formatted_widths.get(signal, "")
            if width:
                definitions[signal] = f"wire {width} {signal};"
            else:
                definitions[signal] = f"wire {signal};"
                
        return definitions
        
    def get_report(self) -> Dict:
        """
        获取分析报告
        
        返回:
            分析报告字典
        """
        return {
            "total_signals": len(self.undefined_signals),
            "signals_with_width": sum(1 for s in self.signal_widths if self.signal_widths[s] is not None),
            "signals_with_default_width": sum(1 for s in self.signal_widths if self.signal_widths[s] is None and self.default_width),
            "signals_without_width": sum(1 for s in self.signal_widths if self.signal_widths[s] is None and not self.default_width),
            "undefined_signals": self.undefined_signals,
            "signal_widths": self.signal_widths,
        }