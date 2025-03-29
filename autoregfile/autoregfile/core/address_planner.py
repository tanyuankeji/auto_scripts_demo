#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址规划模块

处理寄存器地址的规划、分配和冲突检测。
"""

from typing import Dict, Any, List, Tuple, Optional, Set, Union
import math
import copy

from ..utils import get_logger


class AddressBlock:
    """地址块类，表示一个连续的地址空间"""
    
    def __init__(self, name: str, base_address: int, size: int, description: str = ""):
        """
        初始化地址块
        
        参数:
            name: 地址块名称
            base_address: 基地址
            size: 地址块大小（字节）
            description: 描述信息
        """
        self.name = name
        self.base_address = base_address
        self.size = size
        self.description = description
        self.end_address = base_address + size - 1
        self.registers: List[Dict[str, Any]] = []
        
    def contains_address(self, address: int) -> bool:
        """
        检查地址是否在此地址块范围内
        
        参数:
            address: 要检查的地址
            
        返回:
            如果地址在范围内则返回True，否则返回False
        """
        return self.base_address <= address <= self.end_address
    
    def overlaps_with(self, other: 'AddressBlock') -> bool:
        """
        检查此地址块是否与另一个地址块重叠
        
        参数:
            other: 另一个地址块
            
        返回:
            如果有重叠则返回True，否则返回False
        """
        return not (self.end_address < other.base_address or 
                    self.base_address > other.end_address)
    
    def add_register(self, register: Dict[str, Any]) -> None:
        """
        添加寄存器到地址块
        
        参数:
            register: 寄存器字典
        """
        self.registers.append(register)
        
    def get_next_available_address(self, data_width: int = 32) -> int:
        """
        获取下一个可用地址
        
        参数:
            data_width: 数据宽度（位）
            
        返回:
            下一个可用地址
        """
        if not self.registers:
            return self.base_address
        
        # 计算字节对齐
        alignment = max(4, data_width // 8)
        
        # 获取最后一个寄存器的地址
        last_reg = self.registers[-1]
        last_addr = int(last_reg["address"], 0) if isinstance(last_reg["address"], str) else last_reg["address"]
        
        # 计算下一个对齐的地址
        next_addr = last_addr + alignment
        next_addr = (next_addr + alignment - 1) & ~(alignment - 1)  # 对齐到alignment字节边界
        
        return next_addr


class AddressPlanner:
    """
    地址规划器类
    
    负责对寄存器文件中的寄存器进行自动地址分配，支持多种分配策略。
    """
    
    def __init__(self):
        """初始化地址规划器"""
        self.logger = get_logger("address_planner")
        self.address_blocks: List[AddressBlock] = []
        self.address_map: Dict[int, Tuple[Dict[str, Any], AddressBlock]] = {}
    
    def add_address_block(self, name: str, base_address: int, size: int, 
                          description: str = "") -> AddressBlock:
        """
        添加新的地址块
        
        参数:
            name: 地址块名称
            base_address: 基地址
            size: 大小（字节）
            description: 描述信息
            
        返回:
            添加的地址块
            
        可能引发:
            ValueError: 如果地址块与现有地址块重叠
        """
        new_block = AddressBlock(name, base_address, size, description)
        
        # 检查是否与现有地址块重叠
        for block in self.address_blocks:
            if block.overlaps_with(new_block):
                raise ValueError(f"地址块 '{name}' (0x{base_address:08X} - 0x{new_block.end_address:08X}) "
                                f"与地址块 '{block.name}' (0x{block.base_address:08X} - 0x{block.end_address:08X}) 重叠")
        
        self.address_blocks.append(new_block)
        return new_block
    
    def register_address(self, register: Dict[str, Any], block: AddressBlock) -> None:
        """
        注册寄存器地址
        
        参数:
            register: 寄存器字典
            block: 寄存器所属的地址块
            
        可能引发:
            ValueError: 如果地址已被使用
        """
        # 转换地址格式
        addr = register["address"]
        if isinstance(addr, str):
            if addr.startswith("0x") or addr.startswith("0X"):
                addr_int = int(addr, 16)
            else:
                addr_int = int(addr)
        else:
            addr_int = addr
        
        # 检查地址是否在地址块范围内
        if not block.contains_address(addr_int):
            raise ValueError(f"寄存器 '{register['name']}' 的地址 0x{addr_int:08X} 不在地址块 '{block.name}' 的范围内")
        
        # 检查地址是否已被使用
        if addr_int in self.address_map:
            existing_reg, existing_block = self.address_map[addr_int]
            raise ValueError(f"地址冲突: 寄存器 '{register['name']}' 的地址 0x{addr_int:08X} "
                           f"已被寄存器 '{existing_reg['name']}' 在地址块 '{existing_block.name}' 中使用")
        
        # 注册地址
        self.address_map[addr_int] = (register, block)
        block.add_register(register)
    
    def auto_assign_addresses(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        自动分配寄存器地址
        
        根据配置选项和策略为寄存器分配地址
        
        Args:
            config: 寄存器配置字典
            
        Returns:
            Dict[str, Any]: 更新后的配置字典
        """
        try:
            # 创建配置副本，避免修改原始配置
            new_config = copy.deepcopy(config)
            
            # 获取寄存器列表
            registers = new_config.get('registers', [])
            if not registers:
                self.logger.warning("配置中没有寄存器，无需分配地址")
                return new_config
            
            # 获取数据宽度（字节数）
            data_width = new_config.get('data_width', 32)
            byte_width = data_width // 8
            
            # 获取对齐方式
            alignment = new_config.get('address_alignment', byte_width)
            
            # 获取基地址
            base_address = 0
            if 'base_address' in new_config:
                base_value = new_config['base_address']
                # 解析基地址，可以是整数或十六进制字符串
                if isinstance(base_value, str):
                    if base_value.startswith('0x') or base_value.startswith('0X'):
                        base_address = int(base_value, 16)
                    else:
                        try:
                            base_address = int(base_value)
                        except ValueError:
                            self.logger.warning(f"无法解析基地址: {base_value}，使用默认值0")
                            base_address = 0
                else:
                    base_address = int(base_value)
            
            self.logger.info(f"开始自动分配地址，基地址: 0x{base_address:X}, 对齐方式: {alignment}字节")
            
            # 查找现有的有效地址
            existing_addresses = set()
            for reg in registers:
                if 'address' in reg and reg['address']:
                    addr = self._parse_address(reg['address'])
                    if addr is not None:
                        existing_addresses.add(addr)
            
            # 当前地址
            current_address = base_address
            
            # 为每个没有地址的寄存器分配地址
            for reg in registers:
                if 'address' not in reg or not reg['address']:
                    # 找到下一个可用地址
                    while current_address in existing_addresses:
                        current_address += alignment
                    
                    # 分配地址
                    reg['address'] = f"0x{current_address:X}"
                    existing_addresses.add(current_address)
                    self.logger.debug(f"为寄存器 {reg.get('name', 'unnamed')} 分配地址: {reg['address']}")
                    
                    # 更新下一个地址
                    current_address += alignment
            
            self.logger.info(f"地址分配完成，共分配 {len(registers)} 个寄存器")
            return new_config
            
        except Exception as e:
            self.logger.exception(f"自动分配地址时发生异常: {str(e)}")
            return config
    
    def _parse_address(self, address: Union[str, int]) -> Optional[int]:
        """
        解析地址字符串为整数
        
        Args:
            address: 地址表示，可以是字符串(如"0x10")或整数
            
        Returns:
            Optional[int]: 解析后的整数地址，解析失败返回None
        """
        try:
            if isinstance(address, int):
                return address
                
            if isinstance(address, str):
                address = address.strip().lower()
                if address.startswith('0x'):
                    return int(address, 16)
                elif address.startswith('0b'):
                    return int(address, 2)
                elif address.startswith('0'):
                    return int(address, 8)
                else:
                    return int(address)
                    
            return None
            
        except (ValueError, TypeError):
            self.logger.debug(f"无法解析地址: {address}")
            return None
    
    def validate_addresses(self, config: Dict[str, Any]) -> List[str]:
        """
        验证地址配置
        
        参数:
            config: 配置字典
            
        返回:
            错误消息列表，如果没有错误则为空列表
        """
        errors = []
        registers = config.get("registers", [])
        
        # 检查地址是否唯一
        addr_to_reg = {}
        for reg in registers:
            if "address" in reg:
                addr = reg["address"]
                if isinstance(addr, str):
                    if addr.startswith("0x") or addr.startswith("0X"):
                        addr_int = int(addr, 16)
                    else:
                        addr_int = int(addr)
                else:
                    addr_int = addr
                
                if addr_int in addr_to_reg:
                    errors.append(f"地址冲突: 寄存器 '{reg['name']}' 和 '{addr_to_reg[addr_int]}' "
                                f"使用相同的地址 0x{addr_int:X}")
                else:
                    addr_to_reg[addr_int] = reg['name']
        
        # 检查地址对齐
        data_width = config.get("data_width", 32)
        alignment = max(4, data_width // 8)
        
        for reg in registers:
            if "address" in reg:
                addr = reg["address"]
                if isinstance(addr, str):
                    if addr.startswith("0x") or addr.startswith("0X"):
                        addr_int = int(addr, 16)
                    else:
                        addr_int = int(addr)
                else:
                    addr_int = addr
                
                if addr_int % alignment != 0:
                    errors.append(f"地址未对齐: 寄存器 '{reg['name']}' 的地址 0x{addr_int:X} "
                                f"未对齐到 {alignment} 字节边界")
        
        return errors
    
    def get_address_map(self) -> Dict[str, Dict[str, Any]]:
        """
        获取地址映射
        
        返回:
            地址映射字典，格式为 {寄存器名: {address: 地址, block: 地址块名}}
        """
        address_map = {}
        for addr, (reg, block) in self.address_map.items():
            address_map[reg["name"]] = {
                "address": f"0x{addr:X}",
                "block": block.name,
                "description": reg.get("description", "")
            }
        return address_map
    
    def get_memory_map_markdown(self) -> str:
        """
        生成内存映射的Markdown表格
        
        返回:
            Markdown格式的内存映射表格
        """
        markdown = "# 内存映射\n\n"
        
        for block in self.address_blocks:
            markdown += f"## {block.name}\n\n"
            markdown += f"基地址: 0x{block.base_address:X}\n\n"
            markdown += f"大小: {block.size} 字节\n\n"
            
            if block.description:
                markdown += f"{block.description}\n\n"
            
            markdown += "| 地址偏移 | 地址 | 寄存器名 | 描述 |\n"
            markdown += "|----------|------|----------|------|\n"
            
            sorted_registers = sorted(block.registers, 
                                     key=lambda r: int(r["address"], 16) if isinstance(r["address"], str) 
                                                 else r["address"])
            
            for reg in sorted_registers:
                addr = reg["address"]
                if isinstance(addr, str):
                    if addr.startswith("0x") or addr.startswith("0X"):
                        addr_int = int(addr, 16)
                    else:
                        addr_int = int(addr)
                else:
                    addr_int = addr
                
                offset = addr_int - block.base_address
                markdown += f"| 0x{offset:X} | {reg['address']} | {reg['name']} | {reg.get('description', '')} |\n"
            
            markdown += "\n"
        
        return markdown


# 单例模式，全局地址规划器
_address_planner = None

def get_address_planner() -> AddressPlanner:
    """
    获取全局地址规划器实例
    
    返回:
        AddressPlanner实例
    """
    global _address_planner
    if _address_planner is None:
        _address_planner = AddressPlanner()
    return _address_planner 