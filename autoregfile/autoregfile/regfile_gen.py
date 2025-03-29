#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
寄存器文件生成主入口

提供命令行接口和向后兼容性支持。
"""

import os
import sys
import argparse
import logging
from typing import List, Dict, Any, Optional

from .register_factory import get_register_factory
from .utils import configure_global_logging


def main():
    """主入口函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="寄存器文件生成工具")
    parser.add_argument("-c", "--config", dest="config_file", required=True, help="配置文件路径")
    parser.add_argument("-o", "--output", dest="output_file", help="输出文件路径")
    parser.add_argument("-p", "--protocol", dest="bus_protocol", help="总线协议")
    parser.add_argument("-t", "--template-dir", dest="template_dir", action="append", help="模板目录路径")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="启用调试模式")
    parser.add_argument("--log-file", dest="log_file", help="日志文件路径")
    
    args = parser.parse_args()
    
    # 检查必要参数
    if not args.config_file:
        parser.print_help()
        sys.exit(1)
    
    # 设置日志
    log_level = logging.DEBUG if args.debug else logging.INFO
    configure_global_logging(
        level=log_level,
        log_file=args.log_file,
        file_handler_enabled=args.log_file is not None
    )
    
    # 如果未指定输出文件，根据配置文件名生成
    if not args.output_file:
        base_name = os.path.splitext(os.path.basename(args.config_file))[0]
        args.output_file = f"{base_name}_output.v"
    
    # 获取寄存器工厂
    factory = get_register_factory(args.debug, args.log_file)
    
    # 添加模板目录
    if args.template_dir:
        for template_dir in args.template_dir:
            factory.add_template_dir(template_dir)
    
    # 生成寄存器文件
    success = factory.generate_regfile(
        config_file=args.config_file,
        output_file=args.output_file,
        bus_protocol=args.bus_protocol
    )
    
    # 根据结果设置退出码
    sys.exit(0 if success else 1)


# 命令行执行入口
if __name__ == "__main__":
    main() 