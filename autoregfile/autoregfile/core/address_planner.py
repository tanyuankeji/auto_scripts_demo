#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址规划模块

处理寄存器地址的规划、分配和冲突检测。
"""

from typing import Dict, Any, List, Tuple, Optional, Set
import math


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
    """地址规划器类"""
    
    def __init__(self):
        """初始化地址规划器"""
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
    
    def auto_assign_addresses(self, config: Dict[str, Any], block_name: str = "main") -> Dict[str, Any]:
        """
        自动分配地址
        
        参数:
            config: 配置字典
            block_name: 默认地址块名称
            
        返回:
            更新后的配置字典
        """
        # 提取配置信息
        data_width = config.get("data_width", 32)
        addr_width = config.get("addr_width", 8)
        registers = config.get("registers", [])
        
        # 处理地址块配置
        address_blocks = config.get("address_blocks", [])
        
        # 如果没有定义地址块，创建默认地址块
        if not address_blocks:
            # 计算地址块大小
            block_size = 2 ** addr_width * (data_width // 8)
            
            # 创建主地址块
            try:
                main_block = self.add_address_block(block_name, 0, block_size, 
                                                 f"{block_name} 地址空间")
            except ValueError as e:
                # 如果地址块已存在，找到它
                main_block = next((block for block in self.address_blocks if block.name == block_name), None)
                if main_block is None:
                    raise e
        else:
            # 创建配置中定义的所有地址块
            for block_config in address_blocks:
                block_name = block_config.get("name", "block")
                base_addr = block_config.get("base_address", 0)
                size = block_config.get("size", 256)
                description = block_config.get("description", f"{block_name} 地址空间")
                
                # 转换字符串地址
                if isinstance(base_addr, str):
                    if base_addr.startswith("0x") or base_addr.startswith("0X"):
                        base_addr = int(base_addr, 16)
                    else:
                        base_addr = int(base_addr)
                
                try:
                    self.add_address_block(block_name, base_addr, size, description)
                except ValueError as e:
                    print(f"警告: {str(e)}")
        
        # 处理每个寄存器
        for reg in registers:
            if "address" in reg:
                # 使用指定地址
                block_name = reg.get("block", block_name)
                block = next((b for b in self.address_blocks if b.name == block_name), None)
                if block is None:
                    print(f"警告: 寄存器 '{reg['name']}' 引用了未定义的地址块 '{block_name}'，使用默认地址块")
                    block = self.address_blocks[0] if self.address_blocks else None
                    if block is None:
                        raise ValueError(f"无可用地址块用于寄存器 '{reg['name']}'")
                
                try:
                    self.register_address(reg, block)
                except ValueError as e:
                    print(f"警告: {str(e)}")
            else:
                # 自动分配地址
                block_name = reg.get("block", block_name)
                block = next((b for b in self.address_blocks if b.name == block_name), None)
                if block is None:
                    print(f"警告: 寄存器 '{reg['name']}' 引用了未定义的地址块 '{block_name}'，使用默认地址块")
                    block = self.address_blocks[0] if self.address_blocks else None
                    if block is None:
                        raise ValueError(f"无可用地址块用于寄存器 '{reg['name']}'")
                
                addr = block.get_next_available_address(data_width)
                reg["address"] = f"0x{addr:X}"
                try:
                    self.register_address(reg, block)
                except ValueError as e:
                    print(f"警告: {str(e)}")
        
        # 返回更新后的配置
        updated_config = config.copy()
        updated_config["registers"] = registers
        return updated_config
    
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