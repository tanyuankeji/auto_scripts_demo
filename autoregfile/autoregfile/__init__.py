#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autoregfile - 自动寄存器文件生成器包

用于自动生成Verilog寄存器文件及相关文档的工具包。
"""

# 版本信息
from .__version__ import __version__

# 导入主要组件
from .core.register_types import RegisterType, RegisterTypeManager
from .parsers.base_parser import ConfigParser
from .generators.base_generator import BaseGenerator
from .generators.verilog_generator import VerilogGenerator
from .generators.header_generator import HeaderGenerator
from .generators.doc_generator import DocGenerator

# 公开的API
__all__ = [
    "__version__",
    "RegisterType",
    "RegisterTypeManager",
    "ConfigParser",
    "BaseGenerator",
    "VerilogGenerator",
    "HeaderGenerator",
    "DocGenerator",
] 