#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器配置的数据模型

定义强类型的数据模型，用于替代原有的字典结构，提供类型安全和数据验证功能。
"""

from typing import Dict, List, Any, Optional, Union, Set
from enum import Enum, auto
import re


class RegType:
    """
    寄存器类型类
    
    定义各种寄存器类型及其特性，替代原始的枚举类型实现。
    """
    
    # 基本类型
    ReadOnly = "ReadOnly"       # 只读寄存器
    ReadWrite = "ReadWrite"     # 读写寄存器
    WriteOnly = "WriteOnly"     # 只写寄存器
    
    # 特殊类型
    Write1Clean = "Write1Clean"    # 写1清零寄存器
    Write0Clean = "Write0Clean"    # 写0清零寄存器
    Write1Set = "Write1Set"        # 写1置位寄存器
    Write0Set = "Write0Set"        # 写0置位寄存器
    WriteOnce = "WriteOnce"        # 只能写一次的寄存器
    WriteOnlyOnce = "WriteOnlyOnce"  # 只能写一次且只写的寄存器
    ReadClean = "ReadClean"        # 读取后自动清零寄存器
    ReadSet = "ReadSet"            # 读取后自动置位寄存器
    WriteReadClean = "WriteReadClean"  # 可写且读取后自动清零寄存器
    WriteReadSet = "WriteReadSet"    # 可写且读取后自动置位寄存器
    Write1Pulse = "Write1Pulse"    # 写1产生脉冲寄存器
    Write0Pulse = "Write0Pulse"    # 写0产生脉冲寄存器
    
    # 类型属性定义
    _TYPE_ATTRIBUTES = {
        # 类型: (默认位宽, 描述, 特殊处理标志, 是否可读, 是否可写, 读特性, 写特性)
        ReadOnly: (32, "只读寄存器，硬件可写入，软件只能读取", False, True, False, None, None),
        ReadWrite: (32, "读写寄存器，硬件和软件都可读写", False, True, True, None, None),
        WriteOnly: (8, "只写寄存器，软件可写入但读回为0", True, False, True, None, None),
        Write1Clean: (32, "写1清零寄存器，软件写1清除对应位", False, True, True, None, "write1clear"),
        Write0Clean: (32, "写0清零寄存器，软件写0清除对应位", False, True, True, None, "write0clear"),
        Write1Set: (8, "写1置位寄存器，软件写1置位对应位", True, True, True, None, "write1set"),
        Write0Set: (32, "写0置位寄存器，软件写0置位对应位", False, True, True, None, "write0set"),
        WriteOnce: (32, "只能写一次的寄存器，写入后锁定", True, True, True, None, "writeonce"),
        WriteOnlyOnce: (32, "只能写一次且只写的寄存器", True, False, True, None, "writeonce"),
        ReadClean: (32, "读取后自动清零寄存器", True, True, False, "readclear", None),
        ReadSet: (32, "读取后自动置位寄存器", True, True, False, "readset", None),
        WriteReadClean: (32, "可写且读取后自动清零寄存器", True, True, True, "readclear", None),
        WriteReadSet: (32, "可写且读取后自动置位寄存器", True, True, True, "readset", None),
        Write1Pulse: (32, "写1产生脉冲寄存器，写入1后自动在下一周期清零", True, True, True, None, "write1pulse"),
        Write0Pulse: (32, "写0产生脉冲寄存器，写入0后自动在下一周期清零", True, True, True, None, "write0pulse"),
    }
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """
        获取所有寄存器类型
        
        Returns:
            List[str]: 所有支持的寄存器类型列表
        """
        return list(cls._TYPE_ATTRIBUTES.keys())
    
    @classmethod
    def is_valid_type(cls, reg_type: str) -> bool:
        """
        检查是否是有效的寄存器类型
        
        Args:
            reg_type: 要检查的寄存器类型
            
        Returns:
            bool: 是否是有效的寄存器类型
        """
        return reg_type in cls._TYPE_ATTRIBUTES
    
    @classmethod
    def get_default_width(cls, reg_type: str) -> int:
        """
        获取寄存器类型的默认宽度
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            int: 默认宽度
        """
        if not cls.is_valid_type(reg_type):
            return 32  # 默认返回32位
        return cls._TYPE_ATTRIBUTES[reg_type][0]
    
    @classmethod
    def get_description(cls, reg_type: str) -> str:
        """
        获取寄存器类型的描述
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            str: 类型描述
        """
        if not cls.is_valid_type(reg_type):
            return "未知类型寄存器"
        return cls._TYPE_ATTRIBUTES[reg_type][1]
    
    @classmethod
    def needs_special_handling(cls, reg_type: str) -> bool:
        """
        检查是否需要特殊处理
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            bool: 是否需要特殊处理
        """
        if not cls.is_valid_type(reg_type):
            return False
        return cls._TYPE_ATTRIBUTES[reg_type][2]
    
    @classmethod
    def is_read_accessible(cls, reg_type: str) -> bool:
        """
        检查是否可读
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            bool: 是否可读
        """
        if not cls.is_valid_type(reg_type):
            return True  # 默认可读
        return cls._TYPE_ATTRIBUTES[reg_type][3]
    
    @classmethod
    def is_write_accessible(cls, reg_type: str) -> bool:
        """
        检查是否可写
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            bool: 是否可写
        """
        if not cls.is_valid_type(reg_type):
            return True  # 默认可写
        return cls._TYPE_ATTRIBUTES[reg_type][4]
    
    @classmethod
    def get_read_behavior(cls, reg_type: str) -> Optional[str]:
        """
        获取读取行为
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            Optional[str]: 读取行为，如果没有特殊行为则返回None
        """
        if not cls.is_valid_type(reg_type):
            return None
        return cls._TYPE_ATTRIBUTES[reg_type][5]
    
    @classmethod
    def get_write_behavior(cls, reg_type: str) -> Optional[str]:
        """
        获取写入行为
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            Optional[str]: 写入行为，如果没有特殊行为则返回None
        """
        if not cls.is_valid_type(reg_type):
            return None
        return cls._TYPE_ATTRIBUTES[reg_type][6]
    
    @classmethod
    def get_attributes(cls, reg_type: str) -> Dict[str, Any]:
        """
        获取寄存器类型的所有属性
        
        Args:
            reg_type: 寄存器类型
            
        Returns:
            Dict[str, Any]: 属性字典
        """
        if not cls.is_valid_type(reg_type):
            # 返回默认属性
            return {
                "default_width": 32,
                "description": "未知类型寄存器",
                "needs_special_handling": False,
                "is_readable": True,
                "is_writable": True,
                "read_behavior": None,
                "write_behavior": None
            }
        
        attrs = cls._TYPE_ATTRIBUTES[reg_type]
        return {
            "default_width": attrs[0],
            "description": attrs[1],
            "needs_special_handling": attrs[2],
            "is_readable": attrs[3],
            "is_writable": attrs[4],
            "read_behavior": attrs[5],
            "write_behavior": attrs[6]
        }


class BitRange:
    """位范围表示，可以处理单个位或位范围（例如 "3:0"）"""
    
    def __init__(self, bit_range_str: Union[str, int]):
        """
        初始化位范围
        
        参数:
            bit_range_str: 位范围字符串（如 "3:0"）或单个位（如 "5"或5）
        """
        self.high: int = 0
        self.low: int = 0
        
        # 转换输入为字符串
        if isinstance(bit_range_str, int):
            bit_range_str = str(bit_range_str)
        
        # 清理字符串
        bit_range_str = bit_range_str.strip()
        
        # 解析位范围
        if ':' in bit_range_str:
            # 范围格式 "high:low"
            try:
                parts = bit_range_str.split(':')
                if len(parts) != 2:
                    raise ValueError(f"无效的位范围格式: {bit_range_str}")
                
                self.high = int(parts[0].strip())
                self.low = int(parts[1].strip())
                
                if self.high < self.low:
                    # 自动交换高低位
                    self.high, self.low = self.low, self.high
            except ValueError:
                raise ValueError(f"无法解析位范围: {bit_range_str}")
        else:
            # 单个位
            try:
                bit = int(bit_range_str)
                self.high = bit
                self.low = bit
            except ValueError:
                raise ValueError(f"无效的位值: {bit_range_str}")
    
    @property
    def width(self) -> int:
        """位宽"""
        return self.high - self.low + 1
    
    def __str__(self) -> str:
        """字符串表示"""
        if self.high == self.low:
            return str(self.high)
        return f"{self.high}:{self.low}"
    
    def __repr__(self) -> str:
        """调试表示"""
        return f"BitRange({self.high}:{self.low})"


class Field:
    """寄存器字段"""
    
    def __init__(self, 
                 name: str, 
                 bit_range: Union[str, int, BitRange],
                 field_type: Union[str, RegType] = RegType.ReadWrite,
                 reset_value: Union[str, int] = 0,
                 description: str = "",
                 function: str = "",
                 lock_dependency: Optional[List[str]] = None,
                 magic_dependency: Optional[List[str]] = None,
                 sw_access: str = "",
                 hw_access: str = ""):
        """
        初始化寄存器字段
        
        参数:
            name: 字段名称
            bit_range: 位范围（如 "3:0" 或 5）
            field_type: 字段类型
            reset_value: 复位值
            description: 描述
            function: 功能描述
            lock_dependency: 锁依赖
            magic_dependency: 魔数依赖
            sw_access: 软件访问类型
            hw_access: 硬件访问类型
        """
        self.name = name.strip()
        
        # 位范围处理
        if isinstance(bit_range, BitRange):
            self.bit_range = bit_range
        else:
            self.bit_range = BitRange(bit_range)
        
        # 类型处理
        if isinstance(field_type, RegType):
            self.type = field_type
        else:
            self.type = RegType.ReadWrite
        
        # 复位值处理
        self.reset_value_str = str(reset_value).strip()
        self.reset_value = self._parse_value(reset_value)
        
        self.description = description
        self.function = function
        self.lock_dependency = lock_dependency or []
        self.magic_dependency = magic_dependency or []
        self.sw_access = sw_access
        self.hw_access = hw_access
    
    def _parse_value(self, value: Union[str, int]) -> int:
        """解析复位值，转换为整数"""
        if isinstance(value, int):
            return value
        
        value_str = str(value).strip().lower()
        
        # 处理十六进制
        if value_str.startswith('0x') or value_str.startswith('0h'):
            try:
                return int(value_str.replace('0h', '0x'), 16)
            except ValueError:
                return 0
        
        # 处理二进制
        elif value_str.startswith('0b'):
            try:
                return int(value_str[2:], 2)
            except ValueError:
                return 0
        
        # 尝试作为普通整数
        try:
            return int(value_str)
        except ValueError:
            return 0
    
    def get_mask(self) -> int:
        """计算此字段的掩码"""
        mask = 0
        for i in range(self.bit_range.low, self.bit_range.high + 1):
            mask |= (1 << i)
        return mask
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name}[{self.bit_range}]"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示，兼容原有代码"""
        return {
            'name': self.name,
            'bit_range': str(self.bit_range),
            'bits': str(self.bit_range),  # 兼容性字段
            'type': self.type,
            'reset_value': self.reset_value_str,
            'description': self.description,
            'function': self.function,
            'lock_dependency': self.lock_dependency,
            'magic_dependency': self.magic_dependency,
            'sw_access': self.sw_access,
            'hw_access': self.hw_access
        }


class Register:
    """寄存器定义"""
    
    def __init__(self,
                 name: str,
                 address: Union[str, int],
                 reg_type: Union[str, RegType] = RegType.ReadWrite,
                 reset_value: Union[str, int] = 0,
                 description: str = "",
                 fields: Optional[List[Field]] = None,
                 lock_dependency: Optional[List[str]] = None,
                 magic_dependency: Optional[List[str]] = None,
                 sw_access: str = "",
                 hw_access: str = ""):
        """
        初始化寄存器
        
        参数:
            name: 寄存器名称
            address: 寄存器地址（整数或十六进制字符串）
            reg_type: 寄存器类型
            reset_value: 复位值
            description: 描述
            fields: 字段列表
            lock_dependency: 锁依赖
            magic_dependency: 魔数依赖
            sw_access: 软件访问类型
            hw_access: 硬件访问类型
        """
        self.name = name.strip()
        
        # 地址处理 - 保存原始字符串和解析后的整数值
        self.address_str = str(address).strip()
        self.address = self._parse_address(address)
        
        # 类型处理
        if isinstance(reg_type, RegType):
            self.type = reg_type
        else:
            self.type = RegType.ReadWrite
        
        # 复位值处理
        self.reset_value_str = str(reset_value).strip()
        self.reset_value = self._parse_value(reset_value)
        
        self.description = description
        self.fields = fields or []
        self.lock_dependency = lock_dependency or []
        self.magic_dependency = magic_dependency or []
        self.sw_access = sw_access
        self.hw_access = hw_access
        
        # 验证字段
        self._validate_fields()
    
    def _parse_address(self, address: Union[str, int]) -> int:
        """解析地址，转换为整数"""
        if isinstance(address, int):
            return address
        
        addr_str = str(address).strip().lower()
        
        # 处理十六进制
        if addr_str.startswith('0x') or addr_str.startswith('0h'):
            try:
                return int(addr_str.replace('0h', '0x'), 16)
            except ValueError:
                return 0
        
        # 尝试作为普通整数
        try:
            return int(addr_str)
        except ValueError:
            return 0
    
    def _parse_value(self, value: Union[str, int]) -> int:
        """解析复位值，转换为整数"""
        if isinstance(value, int):
            return value
        
        value_str = str(value).strip().lower()
        
        # 处理十六进制
        if value_str.startswith('0x') or value_str.startswith('0h'):
            try:
                return int(value_str.replace('0h', '0x'), 16)
            except ValueError:
                return 0
        
        # 处理二进制
        elif value_str.startswith('0b'):
            try:
                return int(value_str[2:], 2)
            except ValueError:
                return 0
        
        # 尝试作为普通整数
        try:
            return int(value_str)
        except ValueError:
            return 0
    
    def _validate_fields(self) -> None:
        """验证字段是否有重叠或其他问题"""
        used_bits: Set[int] = set()
        
        for field in self.fields:
            # 检查字段位是否重叠
            for bit in range(field.bit_range.low, field.bit_range.high + 1):
                if bit in used_bits:
                    raise ValueError(f"寄存器 {self.name} 中的字段 {field.name} 与其他字段位重叠")
                used_bits.add(bit)
    
    def add_field(self, field: Field) -> None:
        """添加字段"""
        # 检查是否与现有字段重叠
        for bit in range(field.bit_range.low, field.bit_range.high + 1):
            for existing_field in self.fields:
                if bit >= existing_field.bit_range.low and bit <= existing_field.bit_range.high:
                    raise ValueError(
                        f"字段 {field.name} 的位 {bit} 与现有字段 {existing_field.name} 重叠"
                    )
        
        self.fields.append(field)
    
    def get_field_by_name(self, name: str) -> Optional[Field]:
        """通过名称获取字段"""
        for field in self.fields:
            if field.name.lower() == name.lower():
                return field
        return None
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} @ {self.address_str}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示，兼容原有代码"""
        return {
            'name': self.name,
            'address': self.address_str,
            'type': self.type,
            'reset_value': self.reset_value_str,
            'description': self.description,
            'fields': [field.to_dict() for field in self.fields],
            'locked_by': self.lock_dependency,
            'magic_dependency': self.magic_dependency,
            'sw_access_type': self.sw_access,
            'hw_access_type': self.hw_access
        }


class RegisterFileConfig:
    """寄存器文件配置"""
    
    def __init__(self,
                 module_name: str = "regfile",
                 data_width: int = 32,
                 addr_width: int = 8,
                 bus_protocol: str = "apb",
                 registers: Optional[List[Register]] = None,
                 sync_reset: bool = True,
                 byte_enable: bool = True,
                 num_write_ports: int = 1,
                 num_read_ports: int = 1,
                 bus_options: Optional[Dict[str, Any]] = None):
        """
        初始化寄存器文件配置
        
        参数:
            module_name: 模块名称
            data_width: 数据宽度
            addr_width: 地址宽度
            bus_protocol: 总线协议
            registers: 寄存器列表
            sync_reset: 是否使用同步复位
            byte_enable: 是否启用字节使能
            num_write_ports: 写端口数量
            num_read_ports: 读端口数量
            bus_options: 总线选项
        """
        self.module_name = module_name
        self.data_width = data_width
        self.addr_width = addr_width
        self.bus_protocol = bus_protocol
        self.registers = registers or []
        self.sync_reset = sync_reset
        self.byte_enable = byte_enable
        self.num_write_ports = num_write_ports
        self.num_read_ports = num_read_ports
        self.bus_options = bus_options or {}
    
    def add_register(self, register: Register) -> None:
        """添加寄存器"""
        # 检查地址是否重复
        for reg in self.registers:
            if reg.address == register.address:
                raise ValueError(f"寄存器 {register.name} 的地址 {register.address_str} 与 {reg.name} 重复")
        
        self.registers.append(register)
    
    def get_register_by_name(self, name: str) -> Optional[Register]:
        """通过名称获取寄存器"""
        for reg in self.registers:
            if reg.name.lower() == name.lower():
                return reg
        return None
    
    def get_register_by_address(self, address: Union[str, int]) -> Optional[Register]:
        """通过地址获取寄存器"""
        # 如果传入的是字符串，解析为整数
        if isinstance(address, str):
            addr_int = Register("temp", address)._parse_address(address)
        else:
            addr_int = address
            
        for reg in self.registers:
            if reg.address == addr_int:
                return reg
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示，兼容原有代码"""
        return {
            'module_name': self.module_name,
            'data_width': self.data_width,
            'addr_width': self.addr_width,
            'bus_protocol': self.bus_protocol,
            'registers': [reg.to_dict() for reg in self.registers],
            'sync_reset': self.sync_reset,
            'byte_enable': self.byte_enable,
            'num_write_ports': self.num_write_ports,
            'num_read_ports': self.num_read_ports,
            'bus_options': self.bus_options
        } 