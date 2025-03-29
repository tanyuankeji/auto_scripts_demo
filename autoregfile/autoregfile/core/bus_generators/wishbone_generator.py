#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wishbone总线生成器模块

实现Wishbone总线协议的寄存器文件生成功能。
"""

import os
import logging
from typing import Dict, Any, List, Optional

from .base_generator import BaseBusGenerator

logger = logging.getLogger(__name__)

class WishboneBusGenerator(BaseBusGenerator):
    """
    Wishbone总线生成器类
    
    专门用于生成Wishbone总线接口的寄存器文件。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化Wishbone总线生成器
        
        参数:
            config: 寄存器配置
            template_dirs: 自定义模板目录
        """
        super().__init__(config, template_dirs)
        self.protocol_name = "wishbone"
    
    def generate(self, output_file: str) -> bool:
        """
        生成Wishbone总线接口寄存器文件
        
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
                    logger.error("Wishbone总线协议验证失败，中止生成")
                    return False
            
            # 获取模板路径
            template_path = self._get_template_path()
            
            # 准备模板上下文
            context = self._prepare_wishbone_context()
            
            # 渲染模板
            output_content = self.template_manager.render_template(template_path, context)
            
            # 写入输出文件，使用UTF-8编码
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            
            logger.info(f"已生成Wishbone总线接口寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"生成Wishbone总线接口寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _prepare_wishbone_context(self) -> Dict[str, Any]:
        """
        准备Wishbone总线特定的上下文
        
        返回:
            Wishbone总线上下文数据
        """
        # 获取通用上下文
        context = self._prepare_common_context()
        
        # 添加Wishbone特定的上下文
        wishbone_config = self.bus_options.get(self.protocol_name, {})
        
        # Wishbone总线类型
        if "bus_type" in wishbone_config:
            context["bus_type"] = wishbone_config["bus_type"]
        else:
            # 默认经典类型
            context["bus_type"] = "classic"  # 可选：classic, standard
        
        # Wishbone周期类型
        if "cycle_type" in wishbone_config:
            context["cycle_type"] = wishbone_config["cycle_type"]
        else:
            # 默认单一读/写周期
            context["cycle_type"] = "single"  # 可选：single, block, rmw
        
        # Wishbone错误响应配置
        if "error_response" in wishbone_config:
            context["error_response"] = bool(wishbone_config["error_response"])
        else:
            # 默认不生成ERR_O信号
            context["error_response"] = False
        
        # Wishbone总线超时配置
        if "timeout_cycles" in wishbone_config:
            try:
                context["timeout_cycles"] = int(wishbone_config["timeout_cycles"])
            except (ValueError, TypeError):
                context["timeout_cycles"] = 16
        
        # Wishbone地址对齐检查
        if "check_address_alignment" in wishbone_config:
            context["check_address_alignment"] = bool(wishbone_config["check_address_alignment"])
        else:
            context["check_address_alignment"] = True
        
        # Wishbone地址颗粒度
        if "addr_granularity" in wishbone_config:
            context["addr_granularity"] = wishbone_config["addr_granularity"]
        else:
            # 默认8位（字节）地址颗粒度
            context["addr_granularity"] = 8  # 8bit (byte) granularity
        
        # 设置总线协议名称（用于注释）
        context["protocol_description"] = "Wishbone B4"
        
        return context
    
    def _get_template_path(self) -> str:
        """
        获取Wishbone总线模板路径
        
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
        
        # 默认使用内置Wishbone模板
        return "verilog/bus/wishbone.v.j2" 