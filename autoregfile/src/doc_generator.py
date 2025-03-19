#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档生成模块

负责生成寄存器文件的Markdown文档。
"""

from datetime import datetime
from typing import Dict, Any


class DocumentGenerator:
    """文档生成器，用于生成寄存器文件的文档"""
    
    @staticmethod
    def generate_markdown_doc(params: Dict[str, Any], verilog_code: str = None) -> str:
        """生成Markdown格式的文档"""
        doc = f"""# {params['module_name']} 寄存器文件

## 概述

这是一个自动生成的寄存器文件模块，用于SoC设计。

## 参数

- 数据宽度: {params['data_width']} 位
- 地址宽度: {params['addr_width']} 位 (共 {2**params['addr_width']} 个寄存器)
- 读端口数量: {params['num_read_ports']}
- 写端口数量: {params['num_write_ports']}
- 复位类型: {'同步' if params['sync_reset'] else '异步'}
- 复位值: {params['reset_value']}
- 字节使能: {'启用' if params.get('byte_enable', False) else '禁用'}

## 接口

### 全局信号
- `clk`: 时钟信号
- `rst_n`: 低有效复位信号

### 写端口
"""
        
        # 写端口描述
        for i in range(params['num_write_ports']):
            doc += f"#### 写端口 {i}\n"
            doc += f"- `wr_en_{i}`: 写使能信号\n"
            doc += f"- `wr_addr_{i}`: 写地址，宽度 {params['addr_width']} 位\n"
            doc += f"- `wr_data_{i}`: 写数据，宽度 {params['data_width']} 位\n"
            
            if params.get('byte_enable', False):
                num_bytes = params['data_width'] // 8
                doc += f"- `wr_be_{i}`: 字节使能信号，宽度 {num_bytes} 位\n"
            
            doc += "\n"
        
        # 读端口描述
        doc += "### 读端口\n\n"
        for i in range(params['num_read_ports']):
            doc += f"#### 读端口 {i}\n"
            doc += f"- `rd_addr_{i}`: 读地址，宽度 {params['addr_width']} 位\n"
            doc += f"- `rd_data_{i}`: 读数据，宽度 {params['data_width']} 位\n\n"
        
        # 寄存器映射
        doc += "## 寄存器映射\n\n"
        doc += "| 地址 | 偏移量 | 描述 |\n"
        doc += "|------|--------|------|\n"
        
        for i in range(min(16, 2**params['addr_width'])):
            doc += f"| {i} | 0x{i * (params['data_width'] // 8):08X} | 寄存器 {i} |\n"
        
        if 2**params['addr_width'] > 16:
            doc += "| ... | ... | ... |\n"
        
        # 生成时间
        doc += f"\n\n---\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return doc


if __name__ == "__main__":
    # 测试代码
    test_params = {
        'module_name': 'test_regfile',
        'data_width': 32,
        'addr_width': 4,  # 16个寄存器
        'num_read_ports': 2,
        'num_write_ports': 1,
        'sync_reset': False,
        'reset_value': 0,
        'byte_enable': False
    }
    
    doc_content = DocumentGenerator.generate_markdown_doc(test_params)
    print(doc_content)