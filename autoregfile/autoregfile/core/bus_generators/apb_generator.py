#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APB总线生成器模块

实现APB总线协议的寄存器文件生成功能。
"""

import os
import logging
from typing import Dict, Any, List, Optional

from .base_generator import BaseBusGenerator

logger = logging.getLogger(__name__)

class APBBusGenerator(BaseBusGenerator):
    """
    APB总线生成器类
    
    专门用于生成APB总线接口的寄存器文件。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化APB总线生成器
        
        参数:
            config: 寄存器配置
            template_dirs: 自定义模板目录
        """
        super().__init__(config, template_dirs)
        self.protocol_name = "apb"
    
    def generate(self, output_file: str) -> bool:
        """
        生成APB总线接口寄存器文件
        
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
                    logger.error("APB总线协议验证失败，中止生成")
                    return False
            
            # 获取模板路径
            template_path = self._get_template_path()
            
            # 准备模板上下文
            context = self._prepare_apb_context()
            
            # 渲染模板
            output_content = self.template_manager.render_template(template_path, context)
            
            # 写入输出文件，使用UTF-8编码
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            
            logger.info(f"已生成APB总线接口寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"生成APB总线接口寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _prepare_apb_context(self) -> Dict[str, Any]:
        """
        准备APB总线特定的上下文
        
        返回:
            APB总线上下文数据
        """
        # 获取通用上下文
        context = self._prepare_common_context()
        
        # 添加APB特定的上下文
        apb_config = self.bus_options.get(self.protocol_name, {})
        
        # APB时序配置
        if "timeout_cycles" in apb_config:
            try:
                context["timeout_cycles"] = int(apb_config["timeout_cycles"])
            except (ValueError, TypeError):
                context["timeout_cycles"] = 16
        
        # APB错误响应配置
        if "error_response" in apb_config:
            context["error_response"] = apb_config["error_response"]
        
        # APB延迟配置
        if "pready_delay" in apb_config:
            try:
                context["pready_delay"] = int(apb_config["pready_delay"])
            except (ValueError, TypeError):
                context["pready_delay"] = 0
        
        # 检查是否需要生成PSLVERR信号
        if "generate_pslverr" in apb_config:
            context["generate_pslverr"] = bool(apb_config["generate_pslverr"])
        else:
            context["generate_pslverr"] = True
        
        return context
    
    def _get_template_path(self) -> str:
        """
        获取APB总线模板路径
        
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
        
        # 默认使用内置APB模板
        return "verilog/bus/apb.v.j2" 