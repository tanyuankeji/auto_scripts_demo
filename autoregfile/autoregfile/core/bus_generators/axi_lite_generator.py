#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXI Lite总线生成器模块

实现AXI Lite总线协议的寄存器文件生成功能。
"""

import os
import logging
from typing import Dict, Any, List, Optional

from .base_generator import BaseBusGenerator

logger = logging.getLogger(__name__)

class AXILiteBusGenerator(BaseBusGenerator):
    """
    AXI Lite总线生成器类
    
    专门用于生成AXI Lite总线接口的寄存器文件。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化AXI Lite总线生成器
        
        参数:
            config: 寄存器配置
            template_dirs: 自定义模板目录
        """
        super().__init__(config, template_dirs)
        self.protocol_name = "axi_lite"
    
    def generate(self, output_file: str) -> bool:
        """
        生成AXI Lite总线接口寄存器文件
        
        参数:
            output_file: 输出文件路径
            
        返回:
            是否生成成功
        """
        try:
            # 验证总线协议配置
            validation_result = self._validate_protocol()
            if not validation_result["valid"]:
                for warning in validation_result["warnings"]:
                    logger.warning(f"警告: {warning}")
                for error in validation_result["errors"]:
                    logger.error(f"错误: {error}")
                if validation_result["errors"]:
                    logger.error("AXI Lite总线协议验证失败，中止生成")
                    return False
            
            # 获取模板路径
            template_path = self._get_template_path()
            
            # 准备模板上下文
            context = self._prepare_axi_lite_context()
            
            # 渲染模板
            output_content = self.template_manager.render_template(template_path, context)
            
            # 写入输出文件，使用UTF-8编码
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            
            logger.info(f"已生成AXI Lite总线接口寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"生成AXI Lite总线接口寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _prepare_axi_lite_context(self) -> Dict[str, Any]:
        """
        准备AXI Lite总线特定的上下文
        
        返回:
            AXI Lite总线上下文数据
        """
        # 获取通用上下文
        context = self._prepare_common_context()
        
        # 添加AXI Lite特定的上下文
        axi_lite_config = self.bus_options.get(self.protocol_name, {})
        
        # AXI Lite时序配置
        if "read_timeout_cycles" in axi_lite_config:
            try:
                context["read_timeout_cycles"] = int(axi_lite_config["read_timeout_cycles"])
            except (ValueError, TypeError):
                context["read_timeout_cycles"] = 16
                
        if "write_timeout_cycles" in axi_lite_config:
            try:
                context["write_timeout_cycles"] = int(axi_lite_config["write_timeout_cycles"])
            except (ValueError, TypeError):
                context["write_timeout_cycles"] = 16
        
        # AXI Lite错误响应配置
        if "error_response" in axi_lite_config:
            context["error_response"] = axi_lite_config["error_response"]
        else:
            # AXI Lite默认错误响应代码
            context["error_response"] = "SLVERR"  # AXI4 slave error response
        
        # AXI Lite延迟配置
        if "read_delay" in axi_lite_config:
            try:
                context["read_delay"] = int(axi_lite_config["read_delay"])
            except (ValueError, TypeError):
                context["read_delay"] = 0
                
        if "write_delay" in axi_lite_config:
            try:
                context["write_delay"] = int(axi_lite_config["write_delay"])
            except (ValueError, TypeError):
                context["write_delay"] = 0
                
        if "response_delay" in axi_lite_config:
            try:
                context["response_delay"] = int(axi_lite_config["response_delay"])
            except (ValueError, TypeError):
                context["response_delay"] = 0
        
        # AXI Lite保护信号处理
        if "check_protection" in axi_lite_config:
            context["check_protection"] = bool(axi_lite_config["check_protection"])
        else:
            context["check_protection"] = False
        
        # 地址对齐检查
        if "check_address_alignment" in axi_lite_config:
            context["check_address_alignment"] = bool(axi_lite_config["check_address_alignment"])
        else:
            context["check_address_alignment"] = True
            
        # 设置总线协议名称（用于注释）
        context["protocol_description"] = "AMBA AXI4-Lite"
        
        return context
    
    def _get_template_path(self) -> str:
        """
        获取AXI Lite总线模板路径
        
        返回:
            模板路径
        """
        # 自定义模板优先
        custom_template = self.bus_options.get("template")
        if custom_template:
            return custom_template
        
        # 协议特定模板其次
        protocol_template = self.bus_options.get(self.protocol_name, {}).get("template")
        if protocol_template:
            return protocol_template
        
        # 默认使用内置AXI Lite模板
        return "verilog/bus/axi_lite.v.j2" 