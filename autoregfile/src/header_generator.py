#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C语言头文件生成模块

负责生成用于软件访问寄存器的C语言头文件。
"""

from datetime import datetime
from typing import Dict, Any


class HeaderGenerator:
    """C语言头文件生成器"""
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> str:
        """生成C语言头文件，用于软件访问寄存器"""
        module_name = params['module_name'].upper()
        header = f"""/**
 * Auto-generated C Header for {params['module_name']} Register File
 * Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

#ifndef {module_name}_REGS_H
#define {module_name}_REGS_H

#include <stdint.h>

// Register addresses
"""
        
        # 生成寄存器地址定义
        registers = []
        for i in range(2**params['addr_width']):
            registers.append(f"#define {module_name}_REG_{i} 0x{i * (params['data_width'] // 8):08X}")
        
        footer = f"""

// Data type for {params['data_width']}-bit registers
typedef {'uint64_t' if params['data_width'] > 32 else 'uint32_t' if params['data_width'] > 16 else 'uint16_t' if params['data_width'] > 8 else 'uint8_t'} {module_name}_reg_t;

#endif // {module_name}_REGS_H
"""
        
        return header + '\n'.join(registers) + footer


if __name__ == "__main__":
    # 测试代码
    test_params = {
        'module_name': 'test_regfile',
        'data_width': 32,
        'addr_width': 4,  # 16个寄存器
    }
    
    header_content = HeaderGenerator.generate(test_params)
    print(header_content)