#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoRegFile 主入口脚本
用于从命令行直接调用寄存器文件生成工具
"""

import sys
from autoregfile.regfile_gen import main

if __name__ == "__main__":
    sys.exit(main()) 