#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
自动生成Verilog Testbench脚本

作者: 优化自xiaotu的原始脚本
日期: 2024-05-23
描述: 
    此脚本用于自动分析Verilog设计文件并生成对应的testbench
    支持信号自动驱动、验证环境自动生成
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# 导入自定义模块
from parsers.verilog_parser import VerilogParser
from generators.testbench_generator import TestbenchGenerator
from generators.verification_generator import VerificationGenerator

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def get_args():
    """处理命令行参数"""
    parser = argparse.ArgumentParser(description="自动生成Verilog Testbench工具")
    parser.add_argument('-f', '--file', help='Verilog文件路径或目录')
    parser.add_argument('-o', '--output', help='输出目录', default='.')
    parser.add_argument('-v', '--verification', action='store_true', default=False, 
                        help='生成自动验证环境')
    parser.add_argument('-d', '--debug', action='store_true', default=False, 
                        help='开启调试模式')
    parser.add_argument('--demo', action='store_true', default=False,
                        help='生成演示环境')
    parser.add_argument('-t', '--template', help='指定自定义模板路径')
    
    # 新增参数
    parser.add_argument('--tb-name', help='testbench名称前缀，默认为"testbench"', default='testbench')
    parser.add_argument('--clk-name', help='时钟信号名称，默认为"clk"', default='clk')
    parser.add_argument('--rst-name', help='复位信号名称，默认为"rst_n"', default='rst_n')
    parser.add_argument('--rel-path', help='输出文件的相对路径，默认为"."', default='.')
    parser.add_argument('--ver-path', help='验证环境的生成路径，默认与输出目录相同', default=None)
    
    args = parser.parse_args()
    
    # 如果没有提供文件路径且非demo模式，使用demo模式
    if not args.file and not args.demo:
        args.demo = True
        logger.info("未指定文件路径，自动切换到demo模式")
    
    # 如果没有指定验证环境路径，使用输出目录
    if args.ver_path is None:
        args.ver_path = args.output
    
    return args

def get_top_module_name(file_path):
    """从文件路径提取顶层模块名称"""
    if not file_path:
        return "demo"
    return Path(file_path).stem

def setup_project_paths(args):
    """设置项目路径"""
    # 获取当前脚本所在路径
    script_dir = Path(__file__).parent.absolute()
    
    # 获取工作目录
    work_dir = Path.cwd()
    
    # 设置模板路径
    if args.template:
        template_dir = Path(args.template)
    else:
        template_dir = script_dir / "templates"
    
    # 设置vcs_demo路径 - 用于复制验证环境
    vcs_demo_dir = script_dir / "templates" / "vcs_demo"
    
    # 输出路径
    output_dir = Path(args.output)
    
    # 相对路径
    rel_path = args.rel_path
    
    # 验证环境路径
    ver_path = Path(args.ver_path)
    
    return {
        "script_dir": script_dir,
        "work_dir": work_dir,
        "template_dir": template_dir,
        "vcs_demo_dir": vcs_demo_dir,
        "output_dir": output_dir,
        "rel_path": rel_path,
        "ver_path": ver_path
    }

def main():
    """主函数"""
    # 解析命令行参数
    args = get_args()
    
    # 设置日志级别
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    # 设置项目路径
    paths = setup_project_paths(args)
    
    # 获取顶层模块名
    top_module = get_top_module_name(args.file)
    
    logger.info(f"处理模块: {top_module}")
    
    # 如果是demo模式
    if args.demo:
        logger.info("使用Demo模式")
        tb_generator = TestbenchGenerator(
            None, 
            top_module, 
            paths["template_dir"],
            clk_name=args.clk_name,
            rst_name=args.rst_name
        )
        tb_content = tb_generator.generate_demo_testbench()
        
        # 生成验证环境
        ver_generator = VerificationGenerator(
            top_module, 
            None,
            tb_content, 
            paths["vcs_demo_dir"], 
            paths["output_dir"],
            is_demo=True,
            tb_name=args.tb_name,
            rel_path=paths["rel_path"],
            ver_path=paths["ver_path"]
        )
        ver_generator.generate()
        
    else:
        # 解析Verilog文件
        verilog_file = args.file
        logger.info(f"解析Verilog文件: {verilog_file}")
        
        verilog_parser = VerilogParser(verilog_file, top_module)
        verilog_parser.parse()
        
        # 生成Testbench
        tb_generator = TestbenchGenerator(
            verilog_parser, 
            top_module,
            paths["template_dir"],
            clk_name=args.clk_name,
            rst_name=args.rst_name
        )
        
        tb_content = tb_generator.generate_testbench(
            with_verification=args.verification
        )
        
        # 生成验证环境和简化版testbench
        ver_generator = VerificationGenerator(
            top_module, 
            verilog_parser,
            tb_content, 
            paths["vcs_demo_dir"], 
            paths["output_dir"],
            is_verification=args.verification,
            tb_name=args.tb_name,
            rel_path=paths["rel_path"],
            ver_path=paths["ver_path"]
        )
        ver_generator.generate()
    
    logger.info("生成完成!")

if __name__ == "__main__":
    main() 