#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线协议验证器模块

验证总线协议配置是否符合规范，以确保生成的RTL代码符合总线规范。
"""

from typing import Dict, Any, List


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
            "Write1Pulse", "Write0Pulse", "ReadClean", "WriteOnce", "LockField"
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
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            addr = reg["address"]
            if isinstance(addr, str) and addr.startswith("0x"):
                addr_int = int(addr, 16)
                if addr_int % (data_width // 8) != 0:
                    result["warnings"].append(
                        f"寄存器 {reg['name']} 的地址 {addr} 未按照 {data_width//8} 字节对齐"
                    )


def _validate_axi_lite_protocol(config: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    验证AXI-Lite总线协议配置
    
    参数:
        config: 配置数据
        result: 验证结果
    """
    # AXI-Lite协议的特定验证
    addr_width = config["addr_width"]
    data_width = config["data_width"]
    
    # 验证数据宽度
    if data_width not in [32, 64]:
        result["warnings"].append(f"AXI-Lite协议通常使用32位或64位数据宽度，当前: {data_width}")
    
    # 验证地址对齐
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            addr = reg["address"]
            if isinstance(addr, str) and addr.startswith("0x"):
                addr_int = int(addr, 16)
                if addr_int % (data_width // 8) != 0:
                    result["warnings"].append(
                        f"寄存器 {reg['name']} 的地址 {addr} 未按照 {data_width//8} 字节对齐"
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
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            addr = reg["address"]
            if isinstance(addr, str) and addr.startswith("0x"):
                addr_int = int(addr, 16)
                if addr_int % (data_width // 8) != 0:
                    result["warnings"].append(
                        f"寄存器 {reg['name']} 的地址 {addr} 未按照 {data_width//8} 字节对齐"
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
    for i, reg in enumerate(config["registers"]):
        if "address" in reg:
            addr = reg["address"]
            if isinstance(addr, str) and addr.startswith("0x"):
                addr_int = int(addr, 16)
                if addr_int % (data_width // 8) != 0:
                    result["warnings"].append(
                        f"寄存器 {reg['name']} 的地址 {addr} 未按照 {data_width//8} 字节对齐"
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
    unsupported_types = {}
    
    if protocol_name.lower() == "apb":
        # APB协议可能不完全支持的寄存器类型
        unsupported_types = {
            "ReadClear": "需要额外逻辑支持"
        }
    elif protocol_name.lower() == "custom":
        # 自定义协议可能需要特殊处理的寄存器类型
        unsupported_types = {
            "Write1Pulse": "需要确保自定义协议支持脉冲寄存器",
            "Write0Pulse": "需要确保自定义协议支持脉冲寄存器"
        }
    
    # 检查每个寄存器类型是否受支持
    for reg in config["registers"]:
        reg_type = reg.get("type")
        if reg_type in unsupported_types:
            result["warnings"].append(
                f"寄存器 {reg['name']} 的类型 '{reg_type}' 在 {protocol_name} 协议中{unsupported_types[reg_type]}"
            )


def _validate_bus_options(config: Dict[str, Any], protocol_name: str, result: Dict[str, Any]) -> None:
    """
    验证总线配置选项
    
    参数:
        config: 配置数据
        protocol_name: 总线协议名称
        result: 验证结果
    """
    # 获取总线配置选项
    bus_options = config.get("bus_options", {})
    if not bus_options:
        return
    
    # 验证特定协议的配置选项
    protocol_config = bus_options.get(protocol_name.lower(), {})
    common_config = bus_options.get("common", {})
    
    # 合并配置
    all_config = {}
    all_config.update(common_config)
    all_config.update(protocol_config)
    
    # 验证超时配置
    if "timeout" in all_config:
        timeout = all_config["timeout"]
        if not isinstance(timeout, dict):
            result["errors"].append("超时配置必须是字典类型")
            result["valid"] = False
        else:
            if "enable" in timeout and not isinstance(timeout["enable"], bool):
                result["errors"].append("超时启用标志必须是布尔类型")
                result["valid"] = False
            
            if "cycles" in timeout:
                cycles = timeout["cycles"]
                if not isinstance(cycles, int) or cycles <= 0:
                    result["errors"].append(f"超时周期数 {cycles} 无效，必须是正整数")
                    result["valid"] = False
            
            if "action" in timeout:
                action = timeout["action"]
                valid_actions = ["error", "reset", "interrupt"]
                if action not in valid_actions:
                    result["errors"].append(f"超时动作 '{action}' 无效，有效值: {', '.join(valid_actions)}")
                    result["valid"] = False
    
    # 验证延迟配置
    if "delay" in all_config:
        delay = all_config["delay"]
        if not isinstance(delay, dict):
            result["errors"].append("延迟配置必须是字典类型")
            result["valid"] = False
        else:
            for key in ["read", "write", "response"]:
                if key in delay:
                    value = delay[key]
                    if not isinstance(value, int) or value < 0:
                        result["errors"].append(f"{key}延迟值 {value} 无效，必须是非负整数")
                        result["valid"] = False
    
    # 验证错误处理配置
    if "error_handling" in all_config:
        error_config = all_config["error_handling"]
        if not isinstance(error_config, dict):
            result["errors"].append("错误处理配置必须是字典类型")
            result["valid"] = False
        else:
            if "response" in error_config:
                response = error_config["response"]
                valid_responses = ["default", "error", "busy", "timeout"]
                if response not in valid_responses:
                    result["errors"].append(f"错误响应类型 '{response}' 无效，有效值: {', '.join(valid_responses)}")
                    result["valid"] = False
    
    # 验证特定协议的特殊配置选项
    if protocol_name.lower() == "axi_lite":
        if "write_strobes" in all_config and not isinstance(all_config["write_strobes"], bool):
            result["errors"].append("AXI-Lite写选通标志必须是布尔类型")
            result["valid"] = False
    
    elif protocol_name.lower() == "wishbone":
        if "classic_cycle" in all_config and not isinstance(all_config["classic_cycle"], bool):
            result["errors"].append("Wishbone经典周期标志必须是布尔类型")
            result["valid"] = False
    
    # 验证自定义模板
    if "template" in bus_options:
        template = bus_options["template"]
        if not isinstance(template, str):
            result["errors"].append("自定义模板路径必须是字符串类型")
            result["valid"] = False
        # 注意：不检查模板文件是否存在，这将在生成时由模板管理器处理 