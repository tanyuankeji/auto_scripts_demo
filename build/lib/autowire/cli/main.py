"""
命令行入口模块
处理命令行参数解析和程序执行流程
"""

import sys
import os
import argparse
from typing import List, Dict, Optional

from ..core.parser import VerilogParser
from ..core.analyzer import SignalAnalyzer
from ..core.generator import CodeGenerator
from ..core.utils import handle_error, VerilogError
from ..config.config import Config

def parse_arguments(args: List[str] = None) -> argparse.Namespace:
    """
    解析命令行参数
    
    参数:
        args: 命令行参数列表，默认为None使用sys.argv
        
    返回:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(description='Verilog自动线网声明工具')
    parser.add_argument('file', help='Verilog源文件路径')
    parser.add_argument('--width', '-w', action='store_true', help='尝试提取信号位宽')
    parser.add_argument('--default-width', '-d', type=str, help='默认位宽，如 "[7:0]" 或 "8" (会转换为[7:0]格式)')
    parser.add_argument('--append', '-a', action='store_true', help='将定义追加到原始文件')
    parser.add_argument('--output-dir', '-o', type=str, help='输出目录路径')
    parser.add_argument('--exclude', '-e', type=str, nargs='+', help='排除匹配模式列表，支持正则表达式')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--help-detail', action='store_true', help='显示详细使用说明')
    parser.add_argument('--debug', action='store_true', help='启用调试模式，显示中间处理结果')
    
    return parser.parse_args(args)

def print_detailed_help() -> None:
    """打印详细帮助信息"""
    help_text = """
Verilog自动线网声明工具 (Auto Wire Generator) 2.0.0
====================================================

功能说明：
  自动检测Verilog/SystemVerilog代码中未声明的信号，并生成相应的wire声明。
  
主要特点：
  1. 保持信号的原始出现顺序
  2. 自动推断信号位宽
  3. 支持parameter定义的信号
  4. 多种输出模式（独立文件或追加到原文件）
  5. 支持用户自定义排除匹配模式（通过命令行或配置文件）
  6. 增强的模块实例化名称识别（支持常用前缀如u_、i_等）
  7. 支持generate/endgenerate关键字
  8. 支持Verilog数值常量（如1'h0, 8'b00101010等）
  9. 支持多行注释和宏定义
  
用法示例：
  # 基本用法：生成单独的wire声明文件
  python -m autowire.cli.main my_design.v
  
  # 自动检测位宽
  python -m autowire.cli.main --width my_design.v
  
  # 应用默认位宽（支持多种格式）
  python -m autowire.cli.main --default-width "[31:0]" my_design.v  # 直接使用指定位宽
  python -m autowire.cli.main --default-width "32" my_design.v     # 自动转换为[31:0]格式
  
  # 直接追加到原始文件
  python -m autowire.cli.main --append my_design.v
  
  # 指定输出目录
  python -m autowire.cli.main --output-dir ./generated my_design.v
  
  # 排除特定模式的信号（命令行方式）
  python -m autowire.cli.main --exclude "temp_.*" "debug_.*" my_design.v
  
  # 使用配置文件排除特定模式的信号
  python -m autowire.cli.main --config ./config/auto_wire_config.json my_design.v
  
配置文件说明：
  配置文件为JSON格式，包含以下字段：
  {
    "exclude_patterns": [
        "temp_.*",
        "debug_.*",
        "test_.*",
        ".*_reg",
        ".*_next"
    ],
    "default_width": "[7:0]",
    "output_format": "separate",
    "output_dir": "./output",
    "version": "2.0.0"
  }
  
  默认配置文件路径：./config/auto_wire_config.json
    """
    print(help_text)

def run(args: argparse.Namespace) -> int:
    """
    执行主程序
    
    参数:
        args: 解析后的命令行参数
        
    返回:
        执行状态码，0表示成功
    """
    try:
        # 显示详细帮助
        if args.help_detail:
            print_detailed_help()
            return 0
            
        # 初始化配置
        config = Config()
        
        # 加载配置文件
        if args.config:
            config.load_from_file(args.config)
        else:
            # 尝试加载默认配置
            default_config = config.get_default_config_path()
            if os.path.exists(default_config):
                config.load_from_file(default_config)
                
        # 从命令行参数加载配置
        config.load_from_args(args)
        
        # 验证配置
        config.validate()
        
        # 解析文件
        file_path = args.file
        extract_width = args.width
        
        # 创建解析器
        parser = VerilogParser()
        parser.parse_file(file_path)
        
        # 创建分析器
        analyzer = SignalAnalyzer()
        analyzer.setup(
            parser=parser,
            exclude_patterns=config.exclude_patterns,
            default_width=config.default_width
        )
        analyzer.analyze()
        
        # 获取结果
        undefined_signals = analyzer.get_undefined_signals()
        
        # 输出结果
        if undefined_signals:
            if config.verbose or config.debug:
                print(f"\n发现未定义信号：{', '.join(undefined_signals)}")
                
                # 如果提取位宽，显示位宽信息
                if extract_width:
                    print("\n信号位宽信息：")
                    signal_widths = analyzer.signal_widths
                    for signal in undefined_signals:
                        width = signal_widths.get(signal)
                        print(f"  {signal}: {'无位宽信息' if width is None else width}")
            else:
                print(f"\n发现未定义信号：{len(undefined_signals)}个")
                
            # 创建生成器
            generator = CodeGenerator()
            generator.setup(
                analyzer=analyzer,
                file_path=file_path,
                output_dir=config.output_dir,
                append=config.append_to_original
            )
            
            # 生成代码
            generator.generate()
            
            # 输出调试信息
            if config.debug:
                print("\n生成的wire声明：")
                for definition in generator.definitions:
                    print(f"  {definition.strip()}")
                    
            # 写入文件
            output_file = generator.write_to_file()
            
            # 输出摘要
            if config.verbose or config.debug:
                summary = generator.get_summary()
                print(f"\n处理完成。")
                print(f"总共处理信号数量: {summary['total_signals']}")
                print(f"具有自动推断位宽的信号: {summary['signals_with_width']}")
                print(f"使用默认位宽的信号: {summary['signals_with_default_width']}")
                print(f"无位宽信息的信号: {summary['signals_without_width']}")
                print(f"输出模式: {summary['output_mode']}")
                print(f"输出文件: {output_file}")
            else:
                print(f"\n处理完成。{'已追加到原始文件' if config.append_to_original else '输出文件：' + output_file}")
        else:
            print("\n未发现未定义信号。")
            
        return 0
        
    except VerilogError as e:
        handle_error(e, args.debug if hasattr(args, 'debug') else False)
        return 1
    except Exception as e:
        handle_error(e, args.debug if hasattr(args, 'debug') else False)
        return 1

def main() -> int:
    """
    主函数
    
    返回:
        执行状态码，0表示成功
    """
    args = parse_arguments()
    return run(args)

if __name__ == '__main__':
    sys.exit(main())
