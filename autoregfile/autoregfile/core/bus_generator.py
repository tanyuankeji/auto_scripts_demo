#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线生成器模块

负责生成不同总线协议的寄存器文件RTL代码。
"""

import os
import time
from typing import Dict, Any, List, Optional

from .bus_protocols import get_bus_protocol_manager
from .template_manager import get_template_manager
from .bus_validator import validate_bus_protocol


class BusGenerator:
    """
    总线生成器类
    
    用于生成不同总线协议的寄存器文件RTL代码。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化总线生成器
        
        参数:
            config: 寄存器配置
            template_dirs: 自定义模板目录
        """
        # 清理配置，修复可能的问题
        self.config = self._cleanup_config(config)
        self.module_name = self.config.get("module_name", "regfile")
        self.data_width = self.config.get("data_width", 32)
        self.addr_width = self.config.get("addr_width", 8)
        self.registers = self.config.get("registers", [])
        
        # 获取总线协议管理器和模板管理器
        self.bus_protocol_manager = get_bus_protocol_manager()
        self.template_manager = get_template_manager(template_dirs)
        
        # 总线协议配置
        self.bus_options = self.config.get("bus_options", {})
    
    def _cleanup_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        清理配置，修复常见问题
        
        参数:
            config: 原始配置
            
        返回:
            清理后的配置
        """
        # 创建配置的副本，避免修改原始配置
        clean_config = config.copy()
        
        # 确保基本字段存在
        if "data_width" not in clean_config:
            clean_config["data_width"] = 32
        if "addr_width" not in clean_config:
            clean_config["addr_width"] = 8
        if "module_name" not in clean_config:
            clean_config["module_name"] = "regfile"
        if "registers" not in clean_config:
            clean_config["registers"] = []
            
        # 清理寄存器配置
        if "registers" in clean_config:
            clean_registers = []
            for reg in clean_config["registers"]:
                # 创建寄存器副本
                clean_reg = {}
                # 复制基本属性（避免重复）
                for key in ["name", "address", "type", "reset_value", "description"]:
                    if key in reg:
                        clean_reg[key] = reg[key]
                
                # 复制其他属性
                for key, value in reg.items():
                    if key not in clean_reg:
                        clean_reg[key] = value
                
                # 处理'Undefined'值
                for key, value in clean_reg.items():
                    if isinstance(value, str) and value.lower() == 'undefined':
                        if key == "type":
                            clean_reg[key] = "ReadWrite"
                        elif key == "reset_value":
                            clean_reg[key] = "0x0"
                        elif key == "address":
                            clean_reg[key] = "0x0"
                
                clean_registers.append(clean_reg)
            
            clean_config["registers"] = clean_registers
        
        # 清理字段配置
        if "fields" in clean_config:
            clean_fields = []
            for field in clean_config["fields"]:
                # 创建字段副本
                clean_field = {}
                # 复制基本属性（避免重复）
                for key in ["register", "name", "bit_range", "description"]:
                    if key in field:
                        clean_field[key] = field[key]
                
                # 复制其他属性
                for key, value in field.items():
                    if key not in clean_field:
                        clean_field[key] = value
                
                # 处理'Undefined'值
                for key, value in clean_field.items():
                    if isinstance(value, str) and value.lower() == 'undefined':
                        if key == "type":
                            clean_field[key] = "ReadWrite"
                        elif key == "reset_value":
                            clean_field[key] = "0x0"
                        elif key == "bit_range":
                            clean_field[key] = "0"
                
                clean_fields.append(clean_field)
            
            clean_config["fields"] = clean_fields
        
        return clean_config
    
    def generate(self, bus_protocol: str, output_file: str) -> bool:
        """
        生成总线接口寄存器文件
        
        参数:
            bus_protocol: 总线协议名称
            output_file: 输出文件路径
            
        返回:
            是否生成成功
        """
        try:
            # 获取总线协议
            protocol = self.bus_protocol_manager.get_protocol(bus_protocol)
            
            # 准备模板上下文
            context = self._prepare_context(protocol.name)
            
            # 获取模板路径
            template_path = protocol.get_interface_template()
            
            # 检查是否有自定义模板
            user_template = self.bus_options.get("template", None)
            if user_template:
                # 使用用户指定的模板
                template_path = user_template
            
            # 验证总线协议配置
            validation_result = validate_bus_protocol(self.config, protocol.name)
            if not validation_result["valid"]:
                for warning in validation_result["warnings"]:
                    print(f"警告: {warning}")
                for error in validation_result["errors"]:
                    print(f"错误: {error}")
                if validation_result["errors"]:
                    print("总线协议验证失败，中止生成")
                    return False
            
            # 渲染模板
            output_content = self.template_manager.render_template(template_path, context)
            
            # 写入输出文件，使用UTF-8编码
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            
            print(f"已生成总线接口寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            print(f"生成总线接口寄存器文件时出错: {str(e)}")
            return False
    
    def _prepare_context(self, protocol_name: str) -> Dict[str, Any]:
        """
        准备模板渲染上下文
        
        参数:
            protocol_name: 总线协议名称
            
        返回:
            模板上下文数据
        """
        # 基本上下文
        context = {
            "module_name": str(self.module_name),
            "data_width": int(self.data_width),
            "addr_width": int(self.addr_width),
            "registers": self._sanitize_registers(self.registers),
            "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "bus_protocol": str(protocol_name)
        }
        
        # 确保所有值都是正确的类型
        print(f"DEBUG: data_width 类型: {type(context['data_width'])}, 值: {context['data_width']}")
        print(f"DEBUG: addr_width 类型: {type(context['addr_width'])}, 值: {context['addr_width']}")
        
        if not isinstance(context["data_width"], int):
            try:
                print(f"DEBUG: 尝试将 data_width 值 '{context['data_width']}' (类型: {type(context['data_width'])}) 转换为整数")
                context["data_width"] = int(context["data_width"])
                print(f"DEBUG: 转换后 data_width: {context['data_width']}")
            except (ValueError, TypeError) as e:
                print(f"ERROR: 无法将 data_width 转换为整数: {str(e)}")
                context["data_width"] = 32
                print(f"DEBUG: 使用默认 data_width: {context['data_width']}")
                
        if not isinstance(context["addr_width"], int):
            try:
                print(f"DEBUG: 尝试将 addr_width 值 '{context['addr_width']}' (类型: {type(context['addr_width'])}) 转换为整数")
                context["addr_width"] = int(context["addr_width"])
                print(f"DEBUG: 转换后 addr_width: {context['addr_width']}")
            except (ValueError, TypeError) as e:
                print(f"ERROR: 无法将 addr_width 转换为整数: {str(e)}")
                context["addr_width"] = 8
                print(f"DEBUG: 使用默认 addr_width: {context['addr_width']}")
        
        # 添加num_write_ports和num_read_ports到上下文
        if 'num_write_ports' in self.config:
            try:
                context['num_write_ports'] = int(self.config['num_write_ports'])
                print(f"DEBUG: num_write_ports: {context['num_write_ports']}")
            except (ValueError, TypeError) as e:
                print(f"ERROR: 无法将 num_write_ports 转换为整数: {str(e)}")
                context['num_write_ports'] = 1
                print(f"DEBUG: 使用默认 num_write_ports: {context['num_write_ports']}")
        else:
            context['num_write_ports'] = 1
            print(f"DEBUG: 使用默认 num_write_ports: {context['num_write_ports']}")
            
        if 'num_read_ports' in self.config:
            try:
                context['num_read_ports'] = int(self.config['num_read_ports'])
                print(f"DEBUG: num_read_ports: {context['num_read_ports']}")
            except (ValueError, TypeError) as e:
                print(f"ERROR: 无法将 num_read_ports 转换为整数: {str(e)}")
                context['num_read_ports'] = 1
                print(f"DEBUG: 使用默认 num_read_ports: {context['num_read_ports']}")
        else:
            context['num_read_ports'] = 1
            print(f"DEBUG: 使用默认 num_read_ports: {context['num_read_ports']}")
            
        if 'byte_enable' in self.config:
            try:
                context['byte_enable'] = bool(self.config['byte_enable'])
                print(f"DEBUG: byte_enable: {context['byte_enable']}")
            except (ValueError, TypeError) as e:
                print(f"ERROR: 无法将 byte_enable 转换为布尔值: {str(e)}")
                context['byte_enable'] = False
                print(f"DEBUG: 使用默认 byte_enable: {context['byte_enable']}")
        
        # 处理自动创建的寄存器输出端口
        register_outputs = []
        for reg in context["registers"]:
            # 添加脉冲类型寄存器的输出端口
            if reg.get("type") in ["Write1Pulse", "Write0Pulse"]:
                reg_name = reg["name"].lower()
                register_outputs.append({
                    "name": f"{reg_name}_pulse",
                    "width": context["data_width"],
                    "direction": "output wire",
                    "description": f"{reg['description']} 脉冲信号"
                })
            
            # 为寄存器字段添加输出端口
            for field in reg.get("fields", []):
                if "output" in field:
                    # 计算字段宽度
                    bit_range = field.get("bits", "0")
                    width = 1
                    if isinstance(bit_range, str) and "-" in bit_range:
                        try:
                            high, low = map(int, bit_range.split("-"))
                            width = high - low + 1
                        except (ValueError, TypeError):
                            width = 1
                    
                    register_outputs.append({
                        "name": field["output"],
                        "width": width,
                        "direction": "output wire",
                        "description": field.get("description", "")
                    })
        
        context["register_outputs"] = register_outputs
        
        # 添加总线配置选项
        bus_config = self.bus_options.get(protocol_name, {})
        bus_config.update(self.bus_options.get("common", {}))
        
        # 超时配置
        timeout_config = bus_config.get("timeout", {})
        if timeout_config:
            context["timeout_enable"] = bool(timeout_config.get("enable", False))
            try:
                context["timeout_cycles"] = int(timeout_config.get("cycles", 16))
            except (ValueError, TypeError):
                context["timeout_cycles"] = 16
            context["timeout_action"] = str(timeout_config.get("action", "error"))
        
        # 延迟配置
        delay_config = bus_config.get("delay", {})
        if delay_config:
            try:
                context["read_delay"] = int(delay_config.get("read", 0))
            except (ValueError, TypeError):
                context["read_delay"] = 0
                
            try:
                context["write_delay"] = int(delay_config.get("write", 0))
            except (ValueError, TypeError):
                context["write_delay"] = 0
                
            try:
                context["response_delay"] = int(delay_config.get("response", 0))
            except (ValueError, TypeError):
                context["response_delay"] = 0
        
        # 错误处理配置
        error_config = bus_config.get("error_handling", {})
        if error_config:
            context["error_response"] = str(error_config.get("response", "default"))
            context["error_reporting"] = bool(error_config.get("reporting", True))
        
        # 附加配置项
        for key, value in bus_config.items():
            if key not in ["timeout", "delay", "error_handling"]:
                # 确保数值类型正确
                if key.endswith('_cycles') or key.endswith('_count') or key.endswith('_width'):
                    try:
                        context[key] = int(value)
                    except (ValueError, TypeError):
                        context[key] = 0
                else:
                    context[key] = value
        
        return context
    
    def _sanitize_registers(self, registers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        清理并规范化寄存器配置，确保所有值都是合适的类型
        
        参数:
            registers: 原始寄存器列表
            
        返回:
            清理后的寄存器列表
        """
        sanitized_registers = []
        
        for i, reg in enumerate(registers):
            # 创建寄存器的深拷贝，避免修改原始数据
            sanitized_reg = {}
            
            # 确保名称有效
            if "name" not in reg or not reg["name"] or reg["name"] == "Undefined":
                sanitized_reg["name"] = f"REG_{i}"
            else:
                sanitized_reg["name"] = str(reg["name"])
            
            # 确保地址有效
            if "address" not in reg or not reg["address"] or reg["address"] == "Undefined":
                sanitized_reg["address"] = f"0x{i*4:X}"
            elif isinstance(reg["address"], str):
                # 处理字符串地址
                if reg["address"].lower() == "undefined":
                    sanitized_reg["address"] = f"0x{i*4:X}"
                else:
                    # 尝试将地址转换为标准的十六进制格式
                    try:
                        if reg["address"].startswith("0x"):
                            addr_int = int(reg["address"], 16)
                        else:
                            addr_int = int(reg["address"], 0)
                        sanitized_reg["address"] = f"0x{addr_int:X}"
                    except (ValueError, TypeError):
                        sanitized_reg["address"] = f"0x{i*4:X}"
            elif isinstance(reg["address"], int):
                # 处理整数地址
                sanitized_reg["address"] = f"0x{reg['address']:X}"
            else:
                # 其他情况，使用默认地址
                sanitized_reg["address"] = f"0x{i*4:X}"
            
            # 确保类型有效
            if "type" not in reg or not reg["type"] or reg["type"] == "Undefined":
                sanitized_reg["type"] = "ReadWrite"
            elif isinstance(reg["type"], str) and reg["type"].lower() == "undefined":
                sanitized_reg["type"] = "ReadWrite"
            else:
                sanitized_reg["type"] = str(reg["type"])
            
            # 确保复位值有效
            if "reset_value" not in reg or not reg["reset_value"] or reg["reset_value"] == "Undefined":
                sanitized_reg["reset_value"] = "0x0"
            elif isinstance(reg["reset_value"], str):
                # 处理字符串复位值
                if reg["reset_value"].lower() == "undefined":
                    sanitized_reg["reset_value"] = "0x0"
                else:
                    # 尝试将复位值转换为标准的十六进制格式
                    try:
                        if reg["reset_value"].startswith("0x"):
                            reset_int = int(reg["reset_value"], 16)
                        else:
                            reset_int = int(reg["reset_value"], 0)
                        sanitized_reg["reset_value"] = f"0x{reset_int:X}"
                    except (ValueError, TypeError):
                        sanitized_reg["reset_value"] = "0x0"
            elif isinstance(reg["reset_value"], int):
                # 处理整数复位值
                sanitized_reg["reset_value"] = f"0x{reg['reset_value']:X}"
            else:
                # 其他情况，使用默认复位值
                sanitized_reg["reset_value"] = "0x0"
            
            # 确保描述有效
            if "description" not in reg or not reg["description"] or reg["description"] == "Undefined":
                sanitized_reg["description"] = f"寄存器 {sanitized_reg['name']}"
            else:
                sanitized_reg["description"] = str(reg["description"])
            
            # 处理字段
            sanitized_reg["fields"] = []
            if "fields" in reg and isinstance(reg["fields"], list):
                for j, field in enumerate(reg["fields"]):
                    sanitized_field = {}
                    
                    # 确保字段名称有效
                    if "name" not in field or not field["name"] or field["name"] == "Undefined":
                        sanitized_field["name"] = f"FIELD_{j}"
                    else:
                        sanitized_field["name"] = str(field["name"])
                    
                    # 确保位范围有效
                    bit_range_key = None
                    bit_range_value = None
                    
                    # 查找可用的位范围定义
                    for key in ["bit_range", "bits"]:
                        if key in field and field[key] is not None and field[key] != "Undefined":
                            bit_range_key = key
                            bit_range_value = field[key]
                            break
                    
                    # 如果没有找到有效的位范围定义，则使用默认值
                    if bit_range_key is None or bit_range_value is None:
                        sanitized_field["bit_range"] = "0"
                        sanitized_field["bits"] = "0"
                    else:
                        sanitized_field[bit_range_key] = str(bit_range_value)
                        # 确保另一个键也存在
                        other_key = "bits" if bit_range_key == "bit_range" else "bit_range"
                        sanitized_field[other_key] = sanitized_field[bit_range_key]
                    
                    # 确保类型有效
                    if "type" not in field or not field["type"] or field["type"] == "Undefined":
                        sanitized_field["type"] = sanitized_reg["type"]
                    else:
                        sanitized_field["type"] = str(field["type"])
                    
                    # 确保复位值有效
                    if "reset_value" not in field or not field["reset_value"] or field["reset_value"] == "Undefined":
                        sanitized_field["reset_value"] = "0x0"
                    elif isinstance(field["reset_value"], str):
                        # 处理字符串复位值
                        if field["reset_value"].lower() == "undefined":
                            sanitized_field["reset_value"] = "0x0"
                        else:
                            # 尝试将复位值转换为标准的十六进制格式
                            try:
                                if field["reset_value"].startswith("0x"):
                                    reset_int = int(field["reset_value"], 16)
                                else:
                                    reset_int = int(field["reset_value"], 0)
                                sanitized_field["reset_value"] = f"0x{reset_int:X}"
                            except (ValueError, TypeError):
                                sanitized_field["reset_value"] = "0x0"
                    elif isinstance(field["reset_value"], int):
                        # 处理整数复位值
                        sanitized_field["reset_value"] = f"0x{field['reset_value']:X}"
                    else:
                        # 其他情况，使用默认复位值
                        sanitized_field["reset_value"] = "0x0"
                    
                    # 确保描述有效
                    if "description" not in field or not field["description"] or field["description"] == "Undefined":
                        sanitized_field["description"] = f"字段 {sanitized_field['name']}"
                    else:
                        sanitized_field["description"] = str(field["description"])
                    
                    # 复制其他属性
                    for key, value in field.items():
                        if key not in sanitized_field and value is not None and value != "Undefined":
                            sanitized_field[key] = value
                    
                    sanitized_reg["fields"].append(sanitized_field)
            
            # 复制其他属性
            for key, value in reg.items():
                if key not in sanitized_reg and value is not None and value != "Undefined":
                    sanitized_reg[key] = value
            
            sanitized_registers.append(sanitized_reg)
        
        return sanitized_registers 