#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
寄存器类型管理模块

定义和管理不同类型的寄存器，包括读写属性、复位行为、位宽等特性。
支持内置寄存器类型和自定义寄存器类型的扩展。
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass


class AccessType(Enum):
    """寄存器访问类型枚举"""
    READ_WRITE = auto()  # 可读可写
    READ_ONLY = auto()   # 只读
    WRITE_ONLY = auto()  # 只写
    NONE = auto()        # 无访问权限


class ResetBehavior(Enum):
    """寄存器复位行为枚举"""
    SYNC = auto()        # 同步复位
    ASYNC = auto()       # 异步复位
    NONE = auto()        # 无复位行为


@dataclass
class RegTypeInfo:
    """寄存器类型信息数据类"""
    name: str                     # 类型名称
    access: AccessType            # 访问类型
    reset_behavior: ResetBehavior # 复位行为
    default_width: int            # 默认位宽
    description: str              # 描述
    special_handling: bool = False  # 是否需要特殊处理
    hw_access: bool = False       # 是否支持硬件访问
    has_fields: bool = True       # 是否支持子字段
    aliases: List[str] = None     # 类型别名列表


class RegTypeManager:
    """
    寄存器类型管理器
    
    管理所有支持的寄存器类型，包括内置类型和自定义类型。
    提供类型注册、查询和验证功能。
    """
    
    def __init__(self):
        """初始化寄存器类型管理器"""
        self._reg_types: Dict[str, RegTypeInfo] = {}
        self._aliases_map: Dict[str, str] = {}
        
        # 注册内置寄存器类型
        self._register_builtin_types()
    
    def _register_builtin_types(self) -> None:
        """注册内置寄存器类型"""
        # 标准读写寄存器
        self.register_type(
            RegTypeInfo(
                name="RW",
                access=AccessType.READ_WRITE,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="标准读写寄存器",
                aliases=["ReadWrite", "READ_WRITE"]
            )
        )
        
        # 只读寄存器
        self.register_type(
            RegTypeInfo(
                name="RO",
                access=AccessType.READ_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="只读寄存器",
                hw_access=True,
                aliases=["ReadOnly", "READ_ONLY"]
            )
        )
        
        # 只写寄存器
        self.register_type(
            RegTypeInfo(
                name="WO",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="只写寄存器",
                special_handling=True,
                aliases=["WriteOnly", "WRITE_ONLY", "WRITEONLY_REG"]
            )
        )
        
        # 读清零寄存器
        self.register_type(
            RegTypeInfo(
                name="RC",
                access=AccessType.READ_WRITE,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="读清零寄存器，读取后自动清零",
                special_handling=True,
                hw_access=True,
                aliases=["ReadClean", "READ_CLEAN"]
            )
        )
        
        # 写1置位寄存器
        self.register_type(
            RegTypeInfo(
                name="W1S",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="写1置位寄存器，向对应位写1会置位，写0无效",
                special_handling=True,
                aliases=["Write1Set", "WRITE1SET_REG"]
            )
        )
        
        # 写1清零寄存器
        self.register_type(
            RegTypeInfo(
                name="W1C",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="写1清零寄存器，向对应位写1会清零，写0无效",
                special_handling=True,
                aliases=["Write1Clear", "WRITE1CLEAR_REG"]
            )
        )
        
        # 读置位寄存器
        self.register_type(
            RegTypeInfo(
                name="RS",
                access=AccessType.READ_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="读置位寄存器，读取后自动置位",
                special_handling=True,
                hw_access=True,
                aliases=["ReadSet", "READ_SET"]
            )
        )
        
        # 写脉冲寄存器
        self.register_type(
            RegTypeInfo(
                name="WP",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="写脉冲寄存器，写入后产生一个时钟周期的脉冲",
                special_handling=True,
                aliases=["WritePulse", "WRITE_PULSE"]
            )
        )
        
        # 写1脉冲寄存器
        self.register_type(
            RegTypeInfo(
                name="W1P",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="写1脉冲寄存器，向对应位写1会产生脉冲，写0无效",
                special_handling=True,
                aliases=["Write1Pulse", "WRITE1PULSE_REG"]
            )
        )
        
        # 写一次寄存器
        self.register_type(
            RegTypeInfo(
                name="WO1",
                access=AccessType.WRITE_ONLY,
                reset_behavior=ResetBehavior.SYNC,
                default_width=32,
                description="写一次寄存器，只允许写入一次，之后写入无效",
                special_handling=True,
                aliases=["WriteOnce", "WRITE_ONCE"]
            )
        )
    
    def register_type(self, reg_type_info: RegTypeInfo) -> None:
        """
        注册新的寄存器类型
        
        Args:
            reg_type_info: 寄存器类型信息
        """
        self._reg_types[reg_type_info.name] = reg_type_info
        
        # 注册别名
        if reg_type_info.aliases:
            for alias in reg_type_info.aliases:
                self._aliases_map[alias] = reg_type_info.name
    
    def get_type_info(self, type_name: str) -> Optional[RegTypeInfo]:
        """
        获取寄存器类型信息
        
        Args:
            type_name: 寄存器类型名称或别名
            
        Returns:
            Optional[RegTypeInfo]: 寄存器类型信息，如果不存在则返回None
        """
        # 检查是否是别名
        if type_name in self._aliases_map:
            type_name = self._aliases_map[type_name]
        
        # 返回类型信息
        return self._reg_types.get(type_name)
    
    def is_valid_type(self, type_name: str) -> bool:
        """
        检查寄存器类型是否有效
        
        Args:
            type_name: 寄存器类型名称或别名
            
        Returns:
            bool: 类型是否有效
        """
        return self.get_type_info(type_name) is not None
    
    def list_all_types(self) -> List[str]:
        """
        列出所有支持的寄存器类型名称
        
        Returns:
            List[str]: 寄存器类型名称列表
        """
        return list(self._reg_types.keys())
    
    def get_type_by_attributes(self, access: AccessType, 
                              special: bool = False,
                              hw_access: bool = False) -> List[str]:
        """
        根据属性查找匹配的寄存器类型
        
        Args:
            access: 访问类型
            special: 是否需要特殊处理
            hw_access: 是否支持硬件访问
            
        Returns:
            List[str]: 匹配的寄存器类型名称列表
        """
        result = []
        for name, info in self._reg_types.items():
            if (info.access == access and 
                info.special_handling == special and
                info.hw_access == hw_access):
                result.append(name)
        return result
    
    def get_default_width(self, type_name: str) -> int:
        """
        获取寄存器类型的默认位宽
        
        Args:
            type_name: 寄存器类型名称或别名
            
        Returns:
            int: 默认位宽，如果类型不存在则返回32
        """
        type_info = self.get_type_info(type_name)
        return type_info.default_width if type_info else 32


# 创建全局寄存器类型管理器实例
global_reg_type_manager = RegTypeManager()


def get_reg_type_manager() -> RegTypeManager:
    """
    获取全局寄存器类型管理器
    
    Returns:
        RegTypeManager: 全局寄存器类型管理器实例
    """
    return global_reg_type_manager


def is_valid_reg_type(type_name: str) -> bool:
    """
    检查寄存器类型是否有效的便捷函数
    
    Args:
        type_name: 寄存器类型名称或别名
        
    Returns:
        bool: 类型是否有效
    """
    return global_reg_type_manager.is_valid_type(type_name)


def get_reg_type_info(type_name: str) -> Optional[RegTypeInfo]:
    """
    获取寄存器类型信息的便捷函数
    
    Args:
        type_name: 寄存器类型名称或别名
        
    Returns:
        Optional[RegTypeInfo]: 寄存器类型信息
    """
    return global_reg_type_manager.get_type_info(type_name)


def register_custom_reg_type(name: str, 
                            access: AccessType,
                            reset_behavior: ResetBehavior,
                            default_width: int,
                            description: str,
                            special_handling: bool = False,
                            hw_access: bool = False,
                            has_fields: bool = True,
                            aliases: List[str] = None) -> None:
    """
    注册自定义寄存器类型的便捷函数
    
    Args:
        name: 类型名称
        access: 访问类型
        reset_behavior: 复位行为
        default_width: 默认位宽
        description: 描述
        special_handling: 是否需要特殊处理
        hw_access: 是否支持硬件访问
        has_fields: 是否支持子字段
        aliases: 类型别名列表
    """
    reg_type_info = RegTypeInfo(
        name=name,
        access=access,
        reset_behavior=reset_behavior,
        default_width=default_width,
        description=description,
        special_handling=special_handling,
        hw_access=hw_access,
        has_fields=has_fields,
        aliases=aliases
    )
    global_reg_type_manager.register_type(reg_type_info) 