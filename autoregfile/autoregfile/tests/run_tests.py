#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoRegFile 测试运行脚本

运行单元测试和集成测试，并生成测试报告。
"""

import os
import sys
import unittest
import argparse
from typing import List, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def run_tests(test_type: Optional[str] = None, verbose: bool = False) -> bool:
    """
    运行测试
    
    Args:
        test_type: 测试类型，可选值为'unit', 'integration', None(全部)
        verbose: 是否显示详细输出
        
    Returns:
        bool: 测试是否全部通过
    """
    # 设置测试发现的起始目录
    start_dir = os.path.dirname(__file__)
    
    if test_type == 'unit':
        start_dir = os.path.join(start_dir, 'unit')
    elif test_type == 'integration':
        start_dir = os.path.join(start_dir, 'integration')
    
    # 创建测试加载器和测试套件
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # 运行测试
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # 返回是否全部通过
    return result.wasSuccessful()


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='运行AutoRegFile测试')
    parser.add_argument('-t', '--type', choices=['unit', 'integration', 'all'],
                        default='all', help='要运行的测试类型')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细输出')
    args = parser.parse_args()
    
    # 确定测试类型
    test_type = None if args.type == 'all' else args.type
    
    # 打印测试标题
    test_name = '全部测试' if test_type is None else f'{test_type}测试'
    print(f"===== 运行{test_name} =====")
    
    # 运行测试
    success = run_tests(test_type, args.verbose)
    
    # 返回状态码
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main()) 