#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线协议验证器模块

验证总线协议配置是否符合规范，以确保生成的RTL代码符合总线规范。
"""

import logging
from typing import Dict, Any, List, Union, Optional
from .data_model import RegisterFileConfig, Register

# 配置日志
logger = logging.getLogger(__name__)


def validate_bus_protocol(config: Dict[str, Any], protocol_name: str) -> Dict[str, Any]:
    """
    验证总线协议配置
    
    参数:
        config: 配置数据
        protocol_name: 总线协议名称
        
    返回:
        验证结果，包含valid, warnings, errors字段
    """
    result = {
        "valid": True,
        "warnings": [],
        "errors": []
    }
    
    # 验证基本配置
    if not _validate_basic_config(config, result):
        return result
    
    # 根据总线协议类型进行特定验证
    if protocol_name.lower() == "apb":
        _validate_apb_protocol(config, result)
    elif protocol_name.lower() == "axi_lite":
        _validate_axi_lite_protocol(config, result)
    elif protocol_name.lower() == "wishbone":
        _validate_wishbone_protocol(config, result)
    elif protocol_name.lower() == "ocp":
        _validate_ocp_protocol(config, result)
    
    # 验证寄存器类型与总线协议的兼容性
    _validate_register_compatibility(config, protocol_name, result)
    
    # 验证总线配置选项
    _validate_bus_options(config, protocol_name, result)
    
    return result


def validate_model_bus_protocol(config: RegisterFileConfig, protocol_name: Optional[str] = None) -> Dict[str, Any]:
    """
    验证强类型的总线协议配置
    
    参数:
        config: 寄存器文件配置模型
        protocol_name: 总线协议名称，如果为None则使用配置中的协议
        
    返回:
        验证结果，包含valid, warnings, errors字段
    """
    if protocol_name is None:
        protocol_name = config.bus_protocol
    
    result = {
        "valid": True,
        "warnings": [],
        "errors": []
    }
    
    # 验证基本配置
    _validate_model_basic_config(config, result)
    
    if not result["valid"]:
        return result
    
    # 根据总线协议类型进行特定验证
    if protocol_name.lower() == "apb":
        _validate_model_apb_protocol(config, result)
    elif protocol_name.lower() == "axi_lite":
        _validate_model_axi_lite_protocol(config, result)
    elif protocol_name.lower() == "wishbone":
        _validate_model_wishbone_protocol(config, result)
    elif protocol_name.lower() == "ocp":
        _validate_model_ocp_protocol(config, result)
    
    # 验证寄存器类型与总线协议的兼容性
    _validate_model_register_compatibility(config, protocol_name, result)
    
    return result


def _validate_model_basic_config(config: RegisterFileConfig, result: Dict[str, Any]) -> bool:
    """
    验证强类型的基本配置
    
    参数:
        config: 寄存器文件配置模型
        result: 验证结果
        
    返回:
        基本配置是否有效
    """
    # 验证数据宽度
    data_width = config.data_width
    if data_width <= 0:
        result["errors"].append(f"无效的数据宽度: {data_width}，必须是正整数")
        result["valid"] = False
    elif data_width not in [8, 16, 32, 64, 128]:
        result["warnings"].append(f"非标准数据宽度: {data_width}，推荐使用: 8, 16, 32, 64, 128")
    
    # 验证地址宽度
    addr_width = config.addr_width
    if addr_width <= 0:
        result["errors"].append(f"无效的地址宽度: {addr_width}，必须是正整数")
        result["valid"] = False
    
    # 验证寄存器列表
    registers = config.registers
    if len(registers) == 0:
        result["warnings"].append("寄存器列表为空")
    
    return result["valid"]


def _validate_model_apb_protocol(config: RegisterFileConfig, result: Dict[str, Any]) -> None:
    """
    验证APB总线协议配置（强类型版本）
    
    参数:
        config: 配置数据模型
        result: 验证结果
    """
    # APB协议的特定验证
    data_width = config.data_width
    if data_width > 32:
        result["warnings"].append(f"APB协议通常使用32位或更小的数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for reg in config.registers:
        if reg.address % byte_align != 0:
            result["warnings"].append(
                f"寄存器 {reg.name} 的地址 {reg.address_str} 未按照 {byte_align} 字节对齐"
            )


def _validate_model_axi_lite_protocol(config: RegisterFileConfig, result: Dict[str, Any]) -> None:
    """
    验证AXI-Lite总线协议配置（强类型版本）
    
    参数:
        config: 配置数据模型
        result: 验证结果
    """
    # AXI-Lite协议的特定验证
    data_width = config.data_width
    
    # 验证数据宽度
    if data_width not in [32, 64]:
        result["warnings"].append(f"AXI-Lite协议通常使用32位或64位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for reg in config.registers:
        if reg.address % byte_align != 0:
            result["warnings"].append(
                f"寄存器 {reg.name} 的地址 {reg.address_str} 未按照 {byte_align} 字节对齐"
            )


def _validate_model_wishbone_protocol(config: RegisterFileConfig, result: Dict[str, Any]) -> None:
    """
    验证Wishbone总线协议配置（强类型版本）
    
    参数:
        config: 配置数据模型
        result: 验证结果
    """
    # Wishbone协议的特定验证
    data_width = config.data_width
    if data_width not in [8, 16, 32, 64]:
        result["warnings"].append(f"Wishbone协议通常使用8, 16, 32或64位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for reg in config.registers:
        if reg.address % byte_align != 0:
            result["warnings"].append(
                f"寄存器 {reg.name} 的地址 {reg.address_str} 未按照 {byte_align} 字节对齐"
            )


def _validate_model_ocp_protocol(config: RegisterFileConfig, result: Dict[str, Any]) -> None:
    """
    验证OCP总线协议配置（强类型版本）
    
    参数:
        config: 配置数据模型
        result: 验证结果
    """
    # OCP协议的特定验证
    data_width = config.data_width
    if data_width not in [8, 16, 32, 64, 128]:
        result["warnings"].append(f"OCP协议通常使用8, 16, 32, 64或128位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for reg in config.registers:
        if reg.address % byte_align != 0:
            result["warnings"].append(
                f"寄存器 {reg.name} 的地址 {reg.address_str} 未按照 {byte_align} 字节对齐"
            )


def _validate_model_register_compatibility(config: RegisterFileConfig, protocol_name: str, result: Dict[str, Any]) -> None:
    """
    验证寄存器类型与总线协议的兼容性（强类型版本）
    
    参数:
        config: 配置数据模型
        protocol_name: 总线协议名称
        result: 验证结果
    """
    # 检查特定协议不支持的寄存器类型
    protocol_warnings = {}
    
    if protocol_name.lower() == "apb":
        # APB协议可能不完全支持的寄存器类型
        protocol_warnings = {
            "ReadClean": "需要额外逻辑支持",
            "ReadSet": "需要额外逻辑支持",
            "WriteReadClean": "需要额外逻辑支持",
            "WriteReadSet": "需要额外逻辑支持"
        }
    elif protocol_name.lower() == "axi_lite":
        # AXI-Lite协议可能不完全支持的寄存器类型
        protocol_warnings = {
            "Write1Pulse": "需要额外握手逻辑",
            "Write0Pulse": "需要额外握手逻辑"
        }
    
    # 检查每个寄存器的类型
    for reg in config.registers:
        reg_type = reg.type.name
        if reg_type in protocol_warnings:
            result["warnings"].append(
                f"寄存器 {reg.name} 的类型 {reg_type} 在 {protocol_name} 协议下可能需要特殊处理: {protocol_warnings[reg_type]}"
            )
        
        # 检查字段类型
        for field in reg.fields:
            field_type = field.type.name
            if field_type in protocol_warnings:
                result["warnings"].append(
                    f"寄存器 {reg.name} 的字段 {field.name} 的类型 {field_type} 在 {protocol_name} 协议下可能需要特殊处理: {protocol_warnings[field_type]}"
                )


def _parse_address(address: Union[str, int]) -> int:
    """
    解析地址，将字符串地址转换为整数
    
    参数:
        address: 地址（字符串或整数）
        
    返回:
        整数形式的地址
    """
    if isinstance(address, int):
        return address
    
    # 处理十六进制字符串
    if isinstance(address, str):
        addr_str = address.strip().lower()
        
        if addr_str.startswith('0x') or addr_str.startswith('0h'):
            try:
                return int(addr_str.replace('0h', '0x'), 16)
            except ValueError:
                logger.warning(f"无法解析十六进制地址: {address}，使用默认值0")
                return 0
        
        # 尝试作为普通整数
        try:
            return int(addr_str)
        except ValueError:
            logger.warning(f"无法解析地址: {address}，使用默认值0")
            return 0
    
    return 0


def _validate_basic_config(config: Dict[str, Any], result: Dict[str, Any]) -> bool:
    """
    验证基本配置
    
    参数:
        config: 配置数据
        result: 验证结果
        
    返回:
        基本配置是否有效
    """
    # 检查必需的配置字段
    required_fields = ["module_name", "data_width", "addr_width", "registers"]
    for field in required_fields:
        if field not in config:
            result["errors"].append(f"缺少必需的配置字段: {field}")
            result["valid"] = False
    
    if not result["valid"]:
        return False
    
    # 验证数据宽度
    data_width = config["data_width"]
    if not isinstance(data_width, int) or data_width <= 0:
        result["errors"].append(f"无效的数据宽度: {data_width}，必须是正整数")
        result["valid"] = False
    elif data_width not in [8, 16, 32, 64, 128]:
        result["warnings"].append(f"非标准数据宽度: {data_width}，推荐使用: 8, 16, 32, 64, 128")
    
    # 验证地址宽度
    addr_width = config["addr_width"]
    if not isinstance(addr_width, int) or addr_width <= 0:
        result["errors"].append(f"无效的地址宽度: {addr_width}，必须是正整数")
        result["valid"] = False
    
    # 验证寄存器列表
    registers = config["registers"]
    if not isinstance(registers, list):
        result["errors"].append("寄存器配置必须是列表")
        result["valid"] = False
    elif len(registers) == 0:
        result["warnings"].append("寄存器列表为空")
    else:
        # 验证每个寄存器
        for i, reg in enumerate(registers):
            _validate_register(reg, i, result)
    
    return result["valid"]


def _validate_register(reg: Dict[str, Any], index: int, result: Dict[str, Any]) -> None:
    """
    验证单个寄存器配置
    
    参数:
        reg: 寄存器配置
        index: 寄存器索引
        result: 验证结果
    """
    # 检查必需的寄存器字段
    required_fields = ["name", "address", "type"]
    for field in required_fields:
        if field not in reg:
            result["errors"].append(f"寄存器 #{index} 缺少必需的字段: {field}")
            result["valid"] = False
    
    if "type" in reg:
        # 验证寄存器类型
        valid_types = [
            "ReadOnly", "ReadWrite", "WriteOnly", 
            "Write1Clean", "Write0Clean", "Write1Set", "Write0Set",
            "Write1Pulse", "Write0Pulse", "ReadClean", "WriteOnce", "LockField",
            "Write1Clear", "Write0Clear"
        ]
        reg_type = reg["type"]
        if reg_type not in valid_types:
            result["errors"].append(f"寄存器 #{index} ({reg.get('name', '未命名')}) 的类型无效: {reg_type}")
            result["valid"] = False


def _validate_apb_protocol(config: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    验证APB总线协议配置
    
    参数:
        config: 配置数据
        result: 验证结果
    """
    # APB协议的特定验证
    data_width = config["data_width"]
    if data_width > 32:
        result["warnings"].append(f"APB协议通常使用32位或更小的数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            # 解析地址为整数，无论是字符串还是整数格式
            addr_int = _parse_address(reg["address"])
            if addr_int % byte_align != 0:
                result["warnings"].append(
                    f"寄存器 {reg['name']} 的地址 {reg['address']} 未按照 {byte_align} 字节对齐"
                )


def _validate_axi_lite_protocol(config: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    验证AXI-Lite总线协议配置
    
    参数:
        config: 配置数据
        result: 验证结果
    """
    # AXI-Lite协议的特定验证
    data_width = config["data_width"]
    
    # 验证数据宽度
    if data_width not in [32, 64]:
        result["warnings"].append(f"AXI-Lite协议通常使用32位或64位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            # 解析地址为整数，无论是字符串还是整数格式
            addr_int = _parse_address(reg["address"])
            if addr_int % byte_align != 0:
                result["warnings"].append(
                    f"寄存器 {reg['name']} 的地址 {reg['address']} 未按照 {byte_align} 字节对齐"
                )


def _validate_wishbone_protocol(config: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    验证Wishbone总线协议配置
    
    参数:
        config: 配置数据
        result: 验证结果
    """
    # Wishbone协议的特定验证
    data_width = config["data_width"]
    if data_width not in [8, 16, 32, 64]:
        result["warnings"].append(f"Wishbone协议通常使用8, 16, 32或64位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            # 解析地址为整数，无论是字符串还是整数格式
            addr_int = _parse_address(reg["address"])
            if addr_int % byte_align != 0:
                result["warnings"].append(
                    f"寄存器 {reg['name']} 的地址 {reg['address']} 未按照 {byte_align} 字节对齐"
                )


def _validate_ocp_protocol(config: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    验证OCP总线协议配置
    
    参数:
        config: 配置数据
        result: 验证结果
    """
    # OCP协议的特定验证
    data_width = config["data_width"]
    if data_width not in [8, 16, 32, 64, 128]:
        result["warnings"].append(f"OCP协议通常使用8, 16, 32, 64或128位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    byte_align = data_width // 8
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            # 解析地址为整数，无论是字符串还是整数格式
            addr_int = _parse_address(reg["address"])
            if addr_int % byte_align != 0:
                result["warnings"].append(
                    f"寄存器 {reg['name']} 的地址 {reg['address']} 未按照 {byte_align} 字节对齐"
                )


def _validate_register_compatibility(config: Dict[str, Any], protocol_name: str, result: Dict[str, Any]) -> None:
    """
    验证寄存器类型与总线协议的兼容性
    
    参数:
        config: 配置数据
        protocol_name: 总线协议名称
        result: 验证结果
    """
    # 检查特定协议不支持的寄存器类型
    protocol_warnings = {}
    
    if protocol_name.lower() == "apb":
        # APB协议可能不完全支持的寄存器类型
        protocol_warnings = {
            "ReadClean": "需要额外逻辑支持",
            "ReadSet": "需要额外逻辑支持",
            "WriteReadClean": "需要额外逻辑支持",
            "WriteReadSet": "需要额外逻辑支持"
        }
    elif protocol_name.lower() == "axi_lite":
        # AXI-Lite协议可能不完全支持的寄存器类型
        protocol_warnings = {
            "Write1Pulse": "需要额外握手逻辑",
            "Write0Pulse": "需要额外握手逻辑"
        }
    
    # 检查每个寄存器的类型
    for reg in config["registers"]:
        if "type" in reg and reg["type"] in protocol_warnings:
            result["warnings"].append(
                f"寄存器 {reg['name']} 的类型 {reg['type']} 在 {protocol_name} 协议下可能需要特殊处理: {protocol_warnings[reg['type']]}"
            )
        
        # 检查字段类型
        if "fields" in reg:
            for field in reg["fields"]:
                if "type" in field and field["type"] in protocol_warnings:
                    result["warnings"].append(
                        f"寄存器 {reg['name']} 的字段 {field['name']} 的类型 {field['type']} 在 {protocol_name} 协议下可能需要特殊处理: {protocol_warnings[field['type']]}"
                    )


def _validate_bus_options(config: Dict[str, Any], protocol_name: str, result: Dict[str, Any]) -> None:
    """
    验证总线配置选项
    
    参数:
        config: 配置数据
        protocol_name: 总线协议名称
        result: 验证结果
    """
    if "bus_options" not in config:
        return
    
    bus_options = config["bus_options"]
    
    # 检查总线特定选项
    if protocol_name.lower() == "apb":
        # APB特定选项验证
        if "psel_width" in bus_options:
            psel_width = bus_options["psel_width"]
            try:
                psel_width = int(psel_width)
                if psel_width <= 0:
                    result["warnings"].append(f"APB: psel_width应大于0，当前值: {psel_width}")
            except (ValueError, TypeError):
                result["warnings"].append(f"APB: psel_width应为整数，当前值: {psel_width}")
    
    elif protocol_name.lower() == "axi_lite":
        # AXI-Lite特定选项验证
        pass
    
    elif protocol_name.lower() == "wishbone":
        # Wishbone特定选项验证
        if "granularity" in bus_options:
            granularity = bus_options["granularity"]
            if granularity not in ["byte", "word"]:
                result["warnings"].append(f"Wishbone: granularity应为 'byte' 或 'word'，当前值: {granularity}")
    
    elif protocol_name.lower() == "ocp":
        # OCP特定选项验证
        pass 