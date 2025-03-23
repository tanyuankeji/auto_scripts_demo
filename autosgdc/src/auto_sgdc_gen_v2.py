#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动SGDC生成工具 (Auto SGDC Generator) V2.0

本工具用于自动分析Verilog文件并生成用于Spyglass CDC分析的SGDC约束文件。
主要功能包括：
1. 自动识别时钟信号和时钟域
2. 检测跨时钟域信号
3. 生成完整的SGDC约束文件
4. 支持交互式配置时钟属性

作者：Auto SGDC Generator Team
"""

import os
import re
import sys
import argparse
import logging
from typing import List, Dict, Tuple, Set, Optional, Union

# 导入自定义模块
from verilog_parser import VerilogParser
from cdc_analyzer import CDCAnalyzer
from sgdc_generator import SGDCGenerator
from utils import setup_logger

# 设置默认日志
logger = setup_logger()

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="自动生成用于Spyglass CDC分析的SGDC约束文件",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("verilog_files", nargs='+', help="Verilog源文件路径，支持多个文件")
    parser.add_argument("-o", "--output", help="输出SGDC文件名 (默认为<top_module>.sgdc)")
    parser.add_argument("-t", "--top", help="顶层模块名称 (默认自动检测)")
    parser.add_argument("-i", "--include", nargs='+', help="包含的目录路径，用于查找其他模块文件")
    parser.add_argument("-c", "--clock-file", help="时钟配置文件路径，用于预设时钟属性")
    parser.add_argument("-n", "--non-interactive", action="store_true", help="非交互模式，使用默认时钟周期")
    parser.add_argument("-s", "--skip-cdc", action="store_true", help="跳过CDC检测分析")
    parser.add_argument("-r", "--report", action="store_true", help="生成详细分析报告")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志")
    return parser.parse_args()

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # 检查文件存在
        for vfile in args.verilog_files:
            if not os.path.exists(vfile):
                logger.error(f"找不到文件: {vfile}")
                return 1
        
        logger.info(f"开始处理 {len(args.verilog_files)} 个Verilog文件...")
        
        # 解析所有Verilog文件
        parser = VerilogParser(args.verilog_files, include_dirs=args.include)
        modules = parser.parse_all()
        
        if not modules:
            logger.error("未能成功解析任何模块！")
            return 1
        
        # 确定顶层模块
        top_module = None
        if args.top:
            # 用户指定顶层模块
            if args.top in modules:
                top_module = modules[args.top]
                logger.info(f"使用用户指定的顶层模块: {args.top}")
            else:
                logger.error(f"指定的顶层模块 {args.top} 未找到！")
                return 1
        else:
            # 自动推断顶层模块
            top_candidates = [m for name, m in modules.items() if not m.is_instantiated]
            if len(top_candidates) == 1:
                top_module = top_candidates[0]
                logger.info(f"自动检测到顶层模块: {top_module.name}")
            elif len(top_candidates) > 1:
                # 多个候选，选择最复杂的一个作为顶层
                top_module = max(top_candidates, key=lambda m: len(m.instances))
                logger.warning(f"检测到多个可能的顶层模块，选择最复杂的一个: {top_module.name}")
            else:
                # 如果所有模块都被实例化，选择包含最多实例的模块作为顶层
                top_module = max(modules.values(), key=lambda m: len(m.instances))
                logger.warning(f"未检测到明确的顶层模块，选择包含最多实例的模块: {top_module.name}")
        
        # 检测时钟信号
        logger.info("正在识别时钟信号...")
        clock_signals = top_module.identify_clock_signals()
        
        if not clock_signals:
            logger.warning("未检测到时钟信号！请检查信号命名或手动添加时钟约束。")
        else:
            logger.info(f"检测到 {len(clock_signals)} 个时钟信号: {', '.join(clock_signals)}")
        
        # 加载时钟配置
        clock_config = {}
        if args.clock_file and os.path.exists(args.clock_file):
            logger.info(f"从配置文件加载时钟属性: {args.clock_file}")
            # TODO: 实现时钟配置文件加载
        
        # CDC分析
        cdc_signals = {}
        if not args.skip_cdc and len(clock_signals) > 1:
            logger.info("开始CDC分析...")
            analyzer = CDCAnalyzer(modules, top_module.name)
            cdc_signals = analyzer.detect_cdc()
            
            if cdc_signals:
                logger.info(f"检测到 {sum(len(signals) for signals in cdc_signals.values())} 个可能的跨时钟域信号")
                for path, signals in cdc_signals.items():
                    logger.debug(f"  {path}: {', '.join(signals)}")
            else:
                logger.info("未检测到跨时钟域信号")
        elif args.skip_cdc:
            logger.info("已跳过CDC分析")
        elif len(clock_signals) <= 1:
            logger.info("只有一个时钟域，跳过CDC分析")
        
        # 生成SGDC文件
        logger.info("正在生成SGDC约束文件...")
        sgdc_gen = SGDCGenerator(
            top_module=top_module,
            clock_signals=clock_signals,
            cdc_signals=cdc_signals,
            clock_config=clock_config
        )
        
        # 设置时钟属性
        if not args.non_interactive:
            sgdc_gen.configure_clocks_interactive()
        else:
            sgdc_gen.configure_clocks_default()
        
        # 生成SGDC内容
        sgdc_content = sgdc_gen.generate_sgdc()
        
        # 确定输出文件名
        if args.output:
            output_file = args.output
        else:
            output_file = f"{top_module.name}.sgdc"
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sgdc_content)
        
        logger.info(f"SGDC约束文件已生成: {output_file}")
        
        # 生成报告
        if args.report:
            report_file = f"{top_module.name}_cdc_report.txt"
            logger.info(f"生成CDC分析报告: {report_file}")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(sgdc_gen.generate_report())
            logger.info(f"CDC分析报告已生成: {report_file}")
        
        return 0
        
    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main()) 