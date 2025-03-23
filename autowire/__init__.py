"""
Verilog自动线网声明工具 (Auto Wire Generator)
用途：自动检测Verilog代码中未声明的信号，并生成相应的wire声明
版本：2.0.0
"""

from .core.parser import VerilogParser
from .core.analyzer import SignalAnalyzer
from .core.generator import CodeGenerator
from .config.config import Config
from .cli.main import main

__version__ = "2.0.0"
__all__ = ['VerilogParser', 'SignalAnalyzer', 'CodeGenerator', 'Config', 'main']
