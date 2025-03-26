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
        self.config = config
        self.module_name = config.get("module_name", "regfile")
        self.data_width = config.get("data_width", 32)
        self.addr_width = config.get("addr_width", 8)
        self.registers = config.get("registers", [])
        
        # 获取总线协议管理器和模板管理器
        self.bus_protocol_manager = get_bus_protocol_manager()
        self.template_manager = get_template_manager(template_dirs)
        
        # 总线协议配置
        self.bus_options = config.get("bus_options", {})
    
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
            "module_name": self.module_name,
            "data_width": self.data_width,
            "addr_width": self.addr_width,
            "registers": self.registers,
            "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "bus_protocol": protocol_name
        }
        
        # 处理自动创建的寄存器输出端口
        register_outputs = []
        for reg in self.registers:
            # 添加脉冲类型寄存器的输出端口
            if reg.get("type") in ["Write1Pulse", "Write0Pulse"]:
                reg_name = reg["name"].lower()
                register_outputs.append({
                    "name": f"{reg_name}_pulse",
                    "width": self.data_width,
                    "direction": "output wire",
                    "description": f"{reg['description']} 脉冲信号"
                })
            
            # 为寄存器字段添加输出端口
            for field in reg.get("fields", []):
                if "output" in field:
                    # 计算字段宽度
                    bit_range = field["bits"]
                    width = 1
                    if "-" in bit_range:
                        high, low = map(int, bit_range.split("-"))
                        width = high - low + 1
                    
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
            context["timeout_enable"] = timeout_config.get("enable", False)
            context["timeout_cycles"] = timeout_config.get("cycles", 16)
            context["timeout_action"] = timeout_config.get("action", "error")
        
        # 延迟配置
        delay_config = bus_config.get("delay", {})
        if delay_config:
            context["read_delay"] = delay_config.get("read", 0)
            context["write_delay"] = delay_config.get("write", 0)
            context["response_delay"] = delay_config.get("response", 0)
        
        # 错误处理配置
        error_config = bus_config.get("error_handling", {})
        if error_config:
            context["error_response"] = error_config.get("response", "default")
            context["error_reporting"] = error_config.get("reporting", True)
        
        # 附加配置项
        for key, value in bus_config.items():
            if key not in ["timeout", "delay", "error_handling"]:
                context[key] = value
        
        return context 