#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器类型信息模块

定义所有支持的寄存器类型及其基本信息。
"""

from typing import Dict, Any, List

# 寄存器类型信息
REGISTER_TYPES = {
    "Null": {
        "description": "空寄存器，不可读写",
        "readable": False,
        "writable": False,
        "special_behavior": None,
    },
    "ReadWrite": {
        "description": "标准读写寄存器",
        "readable": True, 
        "writable": True,
        "special_behavior": None,
    },
    "ReadOnly": {
        "description": "只读寄存器，忽略写操作",
        "readable": True,
        "writable": False,
        "special_behavior": None,
    },
    "ReadClean": {
        "description": "读取后自动清零的寄存器",
        "readable": True,
        "writable": True,
        "special_behavior": "read_clean",
    },
    "ReadSet": {
        "description": "读取后自动置位的寄存器",
        "readable": True,
        "writable": True,
        "special_behavior": "read_set",
    },
    "WriteReadClean": {
        "description": "可写，读取后自动清零的寄存器",
        "readable": True,
        "writable": True,
        "special_behavior": "read_clean",
    },
    "WriteReadSet": {
        "description": "可写，读取后自动置位的寄存器",
        "readable": True,
        "writable": True,
        "special_behavior": "read_set",
    },
    "WriteOnly": {
        "description": "只写寄存器，读取时返回0",
        "readable": False,
        "writable": True,
        "special_behavior": None,
    },
    "WriteOnlyClean": {
        "description": "只写寄存器，写入后自动清零",
        "readable": False,
        "writable": True,
        "special_behavior": "write_clean",
    },
    "WriteOnlySet": {
        "description": "只写寄存器，写入后自动置位",
        "readable": False,
        "writable": True,
        "special_behavior": "write_set",
    },
    "WriteClean": {
        "description": "写0清零对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_0_clean",
    },
    "WriteCleanReadSet": {
        "description": "写0清零对应位，读取后自动置位",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_0_clean", "read_set"],
    },
    "Write1Clean": {
        "description": "写1清零对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_1_clean",
    },
    "Write1CleanReadSet": {
        "description": "写1清零对应位，读取后自动置位",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_1_clean", "read_set"],
    },
    "Write0Clean": {
        "description": "写0清零对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_0_clean",
    },
    "Write0CleanReadSet": {
        "description": "写0清零对应位，读取后自动置位",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_0_clean", "read_set"],
    },
    "WriteSet": {
        "description": "写1置位对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_1_set",
    },
    "WriteSetReadClean": {
        "description": "写1置位对应位，读取后自动清零",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_1_set", "read_clean"],
    },
    "Write1Set": {
        "description": "写1置位对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_1_set",
    },
    "Write1SetReadClean": {
        "description": "写1置位对应位，读取后自动清零",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_1_set", "read_clean"],
    },
    "Write0Set": {
        "description": "写0置位对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_0_set",
    },
    "Write0SetReadClean": {
        "description": "写0置位对应位，读取后自动清零",
        "readable": True,
        "writable": True,
        "special_behavior": ["write_0_set", "read_clean"],
    },
    "Write1Toggle": {
        "description": "写1翻转对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_1_toggle",
    },
    "Write0Toggle": {
        "description": "写0翻转对应位，可读",
        "readable": True,
        "writable": True,
        "special_behavior": "write_0_toggle",
    },
    "WriteOnce": {
        "description": "只写一次寄存器，写入后不可再修改",
        "readable": True,
        "writable": True,
        "special_behavior": "write_once",
    },
    "WriteOnlyOnce": {
        "description": "只写一次寄存器，写入后不可再修改，不可读",
        "readable": False,
        "writable": True,
        "special_behavior": "write_once",
    }
}

def get_register_type_info(type_name: str) -> Dict[str, Any]:
    """
    获取指定名称的寄存器类型信息
    
    参数:
        type_name: 寄存器类型名称
        
    返回:
        寄存器类型信息字典
    """
    if type_name not in REGISTER_TYPES:
        raise ValueError(f"不支持的寄存器类型: {type_name}")
    return REGISTER_TYPES[type_name]

def get_all_register_types() -> List[str]:
    """
    获取所有支持的寄存器类型名称
    
    返回:
        寄存器类型名称列表
    """
    return list(REGISTER_TYPES.keys())

if __name__ == "__main__":
    # 测试代码
    print("支持的寄存器类型:")
    for reg_type in get_all_register_types():
        reg_info = get_register_type_info(reg_type)
        print(f"- {reg_type}: {reg_info['description']}")
        print(f"  可读: {reg_info['readable']}, 可写: {reg_info['writable']}")
        if reg_info['special_behavior']:
            print(f"  特殊行为: {reg_info['special_behavior']}") 