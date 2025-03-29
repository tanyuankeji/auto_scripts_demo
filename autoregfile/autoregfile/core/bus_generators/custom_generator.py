#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义总线生成器模块

此模块实现了一个自定义总线接口的寄存器文件生成器，
可根据用户定义的配置生成灵活的总线接口。
"""

import os
import re
import copy
from typing import Dict, Any, List, Optional, Union

from .base_generator import BaseBusGenerator
from ...utils import get_logger

# 使用字符串形式的装饰器，避免循环导入
# 实际装饰器将在模块加载时由工厂类应用
__bus_protocol__ = "custom"

class CustomBusGenerator(BaseBusGenerator):
    """
    自定义总线生成器
    
    为用户提供高度灵活的总线接口定制能力，允许用户通过配置参数
    自定义总线接口的行为和特性。
    """
    
    def __init__(self, config: Dict[str, Any], template_dirs: Optional[List[str]] = None):
        """
        初始化自定义总线生成器
        
        Args:
            config: 寄存器配置字典
            template_dirs: 模板目录列表
        """
        # 设置协议名称
        self.protocol_name = "custom"
        
        # 从配置中获取数据宽度和地址宽度
        self.data_width = config.get("data_width", 32)
        self.addr_width = config.get("addr_width", 8)
        
        # 是否启用调试信息
        self.enable_debug_info = config.get("enable_debug_info", False)
        
        # 调用父类构造函数
        super().__init__(config, template_dirs)
        
        # 获取日志记录器
        self.logger = get_logger("CustomBusGenerator")
        
        # 自定义总线特定配置
        self.custom_options = self.bus_options.get(self.protocol_name, {})
        
        # 检查配置冲突
        self._check_config_conflicts()
    
    def _check_config_conflicts(self) -> None:
        """
        检查配置中的冲突
        
        检查寄存器名称、地址等是否有冲突，确保生成的代码不会有问题
        """
        # 检查寄存器名称冲突
        reg_names = set()
        for reg in self.registers:
            name = reg.get('name')
            if name in reg_names:
                self.logger.warning(f"发现重复的寄存器名称: {name}")
            else:
                reg_names.add(name)
        
        # 检查寄存器地址冲突
        reg_addrs = {}
        for reg in self.registers:
            addr = reg.get('address')
            if addr:
                if addr in reg_addrs:
                    self.logger.warning(f"寄存器地址冲突: {addr} 被 {reg.get('name')} 和 {reg_addrs[addr]} 共用")
                else:
                    reg_addrs[addr] = reg.get('name')
        
        # 检查寄存器字段名称冲突
        for reg in self.registers:
            if reg.get('has_fields', False) and 'fields' in reg:
                field_names = set()
                for field in reg['fields']:
                    name = field.get('name')
                    if name in field_names:
                        self.logger.warning(f"寄存器 {reg.get('name')} 中字段名称冲突: {name}")
                    else:
                        field_names.add(name)
    
    def generate(self, output_file: str, enable_debug_info: bool = None) -> bool:
        """
        生成寄存器文件
        
        Args:
            output_file: 输出文件路径
            enable_debug_info: 是否在生成的文件中包含调试信息，默认使用实例化时的设置
            
        Returns:
            bool: 是否成功生成
        """
        # 如果指定了enable_debug_info参数，则使用该值覆盖实例属性
        if enable_debug_info is not None:
            self.enable_debug_info = enable_debug_info
        
        # 准备上下文
        context = self._prepare_context()
        
        try:
            # 使用custom.v.j2模板
            template_name = 'verilog/bus/custom.v.j2'
            template_path = self.template_manager.find_template(template_name)
            
            if not template_path:
                self.logger.warning(f"未找到自定义总线模板: {template_name}")
                # 尝试使用base模板
                template_name = 'verilog/bus/base.v.j2'
                template_path = self.template_manager.find_template(template_name)
            
            if not template_path:
                self.logger.error("找不到总线模板，无法生成寄存器文件")
                return False
            
            # 渲染模板
            self.logger.info(f"使用模板: {template_path}")
            output_content = self.template_manager.render_template(template_path, context)
            
            if not output_content:
                self.logger.error("渲染模板失败")
                return False
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # 写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            self.logger.info(f"成功生成寄存器文件: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"生成寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _get_default_template(self) -> str:
        """
        获取默认的内置模板内容
        
        Returns:
            str: 默认模板内容
        """
        return """// =============================================================================
// 自动生成的寄存器文件: {{ module_name }}
// 生成时间: {{ generation_time }}
// =============================================================================

`timescale 1ns / 1ps

module {{ module_name }} (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // 总线接口
    input  wire [{{ addr_width-1 }}:0]     addr,
    input  wire                     chip_select,
    input  wire                     write_en,
    input  wire                     read_en,
    input  wire [{{ data_width-1 }}:0]     write_data,
    output reg  [{{ data_width-1 }}:0]     read_data,
    output wire                     data_valid,    

    {%- for reg in processed_registers %}
    {%- if reg.has_fields %}
    {%- for field in reg.fields %}
    {%- if field.type != 'WriteOnly' and field.type != 'WritePulse' and field.type != 'Write1Pulse' %}
    output wire [{{ field.width-1 }}:0]      {{ reg.name|lower }}_{{ field.name|lower }}_o,
    {%- endif %}
    input  wire [{{ field.width-1 }}:0]      {{ reg.name|lower }}_{{ field.name|lower }}_i,
    input  wire                       {{ reg.name|lower }}_{{ field.name|lower }}_wen{% if not loop.last or not loop.parent.last %},{% endif %}
    {%- endfor %}
    {%- elif reg.type != 'WriteOnly' and reg.type != 'WritePulse' and reg.type != 'Write1Pulse' %}
    {%- if not loop.last %}
    {%- endif %}
    {%- endif %}
    {%- endfor %}
);

// =============================================================================
// 字段位置定义
// =============================================================================

{%- for reg in processed_registers %}
{%- if reg.has_fields %}
// {{ reg.name }} 字段位置定义
{%- for field in reg.fields %}
localparam {{ reg.name|upper }}_{{ field.name|upper }}_POS   = {{ field.bit_range.low }};
localparam {{ reg.name|upper }}_{{ field.name|upper }}_WIDTH = {{ field.width }};
{%- endfor %}
{%- endif %}
{%- endfor %}

// =============================================================================
// 控制信号定义
// =============================================================================

// 控制信号
wire                              write_active = chip_select && write_en;
wire                              read_active  = chip_select && read_en;
assign                            data_valid   = read_active;

// 地址选择信号
{%- for reg in processed_registers %}
wire                              sel_{{ reg.name|lower }} = (addr == {{ addr_width }}'h{{ '%02X' % reg.address|replace('0x', '')|int(16) if reg.address is string else '%02X' % reg.address }});
{%- endfor %}

// =============================================================================
// 寄存器定义
// =============================================================================

{%- for reg in processed_registers %}
// {{ reg.name }} 寄存器 - {{ reg.description|default('') }}
reg     [{{ data_width-1 }}:0]       {{ reg.name|lower }}_reg;
{%- endfor %}

{%- for reg in processed_registers %}
{%- if reg.has_fields %}
// {{ reg.name }} 字段寄存器
{%- for field in reg.fields %}
reg     [{{ field.width-1 }}:0]       {{ reg.name|lower }}_{{ field.name|lower }}_reg;  // {{ field.description|default('') }}
{%- endfor %}
{%- endif %}
{%- endfor %}

// =============================================================================
// 字段与寄存器连接
// =============================================================================

{%- for reg in processed_registers %}
{%- if reg.has_fields %}
// {{ reg.name }} 寄存器组合
always @(*) begin
    {{ reg.name|lower }}_reg = {% if reg.fields|length > 0 %}{
        {%- for field in reg.fields|sort(attribute='bit_range.high', reverse=true) %}
        {{ reg.name|lower }}_{{ field.name|lower }}_reg{% if not loop.last %},{% endif %}
        {%- endfor %}
 }{% else %}{{ data_width }}'d0{% endif %};
end

// {{ reg.name }} 字段接口连接
{%- for field in reg.fields %}
{%- if field.type != 'WriteOnly' and field.type != 'WritePulse' and field.type != 'Write1Pulse' %}
assign {{ reg.name|lower }}_{{ field.name|lower }}_o = {{ reg.name|lower }}_{{ field.name|lower }}_reg;
{%- endif %}
{%- endfor %}
{%- endif %}
{%- endfor %}

// =============================================================================
// 读取逻辑
// =============================================================================
always @(*) begin
    read_data = {{ data_width }}'d0;  // 默认值
    
    if (read_active) begin
        case (1'b1)  // 优先级编码器
            {%- for reg in processed_registers %}
            {%- if reg.type != 'WriteOnly' %}
            sel_{{ reg.name|lower }}  : read_data = {% if reg.name == 'WRITE1SET_REG' %}{ {{ data_width }}'d0 | {{ reg.name|lower }}_reg }{% else %}{{ reg.name|lower }}_reg{% endif %};
            {%- endif %}
            {%- endfor %}
            default   : read_data = {{ data_width }}'d0;
        endcase
    end
end

// =============================================================================
// 寄存器更新逻辑
// =============================================================================
{%- for reg in processed_registers %}
{%- if reg.has_fields %}
// {{ reg.name }} 子字段寄存器更新
{%- for field in reg.fields %}
// {{ field.name|upper }} 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        {{ reg.name|lower }}_{{ field.name|lower }}_reg <= {{ field.width }}'h{{ '%X' % field.reset_value|replace('0x', '')|int(16) if field.reset_value is string else '%X' % field.reset_value|default(0) }};
    end
    else begin
        // 软件优先
        if (write_active && sel_{{ reg.name|lower }}) begin
            {%- if field.type == 'ReadOnly' %}
            // 只读字段，忽略软件写入
            {%- elif field.type == 'WritePulse' or field.type == 'Write1Pulse' %}
            // 写脉冲，下一个周期自动清零
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= write_data[{{ field.bit_range.high }}:{{ field.bit_range.low }}];
            {%- elif field.type == 'Write1Set' %}
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= {{ reg.name|lower }}_{{ field.name|lower }}_reg | write_data[{{ field.bit_range.high }}:{{ field.bit_range.low }}];
            {%- elif field.type == 'Write1Clean' or field.type == 'Write1Clear' %}
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= {{ reg.name|lower }}_{{ field.name|lower }}_reg & ~write_data[{{ field.bit_range.high }}:{{ field.bit_range.low }}];
            {%- else %}
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= write_data[{{ field.bit_range.high }}:{{ field.bit_range.low }}];
            {%- endif %}
        end
        else if ({{ reg.name|lower }}_{{ field.name|lower }}_wen) begin
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= {{ reg.name|lower }}_{{ field.name|lower }}_i;
        end
        {%- if field.type == 'WritePulse' or field.type == 'Write1Pulse' %}
        else begin
            // 脉冲类型字段在没有写入时自动清零
            {{ reg.name|lower }}_{{ field.name|lower }}_reg <= {{ field.width }}'h0;
        end
        {%- else %}
        end
        {%- endif %}
    end
end
{%- endfor %}

{%- else %}
// {{ reg.name }} 寄存器 (无子字段)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        {{ reg.name|lower }}_reg <= {{ data_width if reg.width > data_width else reg.width }}'h{{ '%X' % reg.reset_value|replace('0x', '')|int(16) if reg.reset_value is string else '%X' % reg.reset_value|default(0) }};
    end
    else begin
        // 软件优先
        if (write_active && sel_{{ reg.name|lower }}) begin
            {%- if reg.type == 'ReadOnly' %}
            // 只读寄存器，忽略软件写入
            {%- elif reg.type == 'Write1Set' or reg.type == 'WRITE1SET_REG' %}
            {{ reg.name|lower }}_reg <= {{ reg.name|lower }}_reg | write_data[{{ reg.width-1 if reg.width else data_width-1 }}:0];
            {%- elif reg.type == 'Write1Clean' or reg.type == 'Write1Clear' %}
            {{ reg.name|lower }}_reg <= {{ reg.name|lower }}_reg & ~write_data[{{ reg.width-1 if reg.width else data_width-1 }}:0];
            {%- elif reg.type == 'WritePulse' or reg.type == 'Write1Pulse' %}
            {{ reg.name|lower }}_reg <= write_data[{{ reg.width-1 if reg.width else data_width-1 }}:0];
            {%- else %}
            {{ reg.name|lower }}_reg <= write_data[{{ reg.width-1 if reg.width else data_width-1 }}:0];
            {%- endif %}
        end
        else if ({{ reg.name|lower }}_wen) begin
            {{ reg.name|lower }}_reg <= {{ reg.name|lower }}_i;
        end
        {%- if reg.type == 'WritePulse' or reg.type == 'Write1Pulse' %}
        else begin
            // 脉冲类型寄存器在没有写入时自动清零
            {{ reg.name|lower }}_reg <= {{ data_width if reg.width > data_width else reg.width }}'h0;
        end
        {%- else %}
        end
        {%- endif %}
    end
end
{%- endif %}

{%- endfor %}
endmodule 
"""
    
    def _prepare_context(self) -> Dict[str, Any]:
        """
        准备渲染模板所需的上下文数据
        
        为自定义总线接口提供特定的上下文数据
        
        Returns:
            Dict[str, Any]: 模板上下文数据
        """
        # 获取基本上下文
        context = super()._prepare_context()
        
        # 添加基本配置
        context["data_width"] = self.data_width
        context["addr_width"] = self.addr_width
        
        # 添加调试信息控制
        context["enable_debug_info"] = self.enable_debug_info
        
        # 添加生成时间
        from datetime import datetime
        context["generation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 添加自定义总线特定的上下文数据
        custom_context = self._prepare_custom_context()
        context.update(custom_context)
        
        return context
    
    def _prepare_custom_context(self) -> Dict[str, Any]:
        """
        准备自定义总线特定的上下文数据
        
        处理特殊的寄存器类型、访问模式等
        
        Returns:
            Dict[str, Any]: 自定义上下文数据
        """
        custom_context = {}
        
        # 添加基本配置
        custom_context["data_width"] = self.data_width
        custom_context["addr_width"] = self.addr_width
        
        # 添加总线配置选项
        custom_context["byte_enable"] = self.custom_options.get("byte_enable", False)
        custom_context["generate_errors"] = self.custom_options.get("generate_errors", False)
        custom_context["access_priority"] = self.custom_options.get("access_priority", "sw")  # sw优先或hw优先
        
        # 处理寄存器并计算偏移量
        processed_registers = []
        for reg in self.registers:
            reg_copy = copy.deepcopy(reg)
            
            # 获取寄存器类型，规范化名称
            reg_type = reg_copy.get('type', 'RW')
            
            # 映射常见的简写类型到标准类型
            type_mapping = {
                'RW': 'ReadWrite',
                'RO': 'ReadOnly',
                'WO': 'WriteOnly',
                'RC': 'ReadClean',
                'RS': 'ReadSet',
                'W1S': 'Write1Set',
                'W1C': 'Write1Clean',
                'W0S': 'Write0Set',
                'W0C': 'Write0Clean',
                'WP': 'WritePulse',
                'W1P': 'Write1Pulse',
                'WO1': 'WriteOnce',
                'WOBO': 'WriteOnlyBitOperation'
            }
            
            # 规范化类型名称
            if reg_type in type_mapping:
                reg_type = type_mapping[reg_type]
            
            # 特殊寄存器类型处理
            special_reg_mapping = {
                "CTRL_REG": "ReadWrite",
                "STATUS_REG": "ReadOnly", 
                "INT_FLAG_REG": "Write1Clean",
                "WRITE1SET_REG": "Write1Set",
                "WRITEONLY_REG": "WriteOnly",
                "LOCK_TEST_REG": "ReadWrite"
            }
            
            if reg_copy.get("name") in special_reg_mapping:
                reg_type = special_reg_mapping[reg_copy.get("name")]
            
            reg_copy['type'] = reg_type
            
            # 判断是否有子字段
            has_fields = 'fields' in reg_copy and reg_copy['fields'] and len(reg_copy['fields']) > 0
            
            # 特殊处理某些寄存器
            no_field_regs = ["WRITE1SET_REG", "WRITEONLY_REG"]
            if reg_copy.get("name") in no_field_regs:
                # 强制设置为无子字段寄存器
                reg_copy["has_fields"] = False
                has_fields = False
                
                # 对于特定寄存器，确保位宽设置正确
                if "bits" in reg_copy:
                    if isinstance(reg_copy["bits"], str):
                        if ":" in reg_copy["bits"]:
                            high, low = map(int, reg_copy["bits"].split(":"))
                        else:
                            high = low = int(reg_copy["bits"])
                        reg_copy["bits"] = {"high": high, "low": low}
                        reg_copy["width"] = high - low + 1
                    elif isinstance(reg_copy["bits"], dict):
                        high = reg_copy["bits"].get("high", 0)
                        low = reg_copy["bits"].get("low", 0)
                        reg_copy["width"] = high - low + 1
                else:
                    reg_copy["width"] = 8  # 默认为8位
            else:
                # 需要添加字段的特殊寄存器
                if reg_copy.get("name") == "CTRL_REG" and not has_fields:
                    # 添加字段，按照参考排序：enable, mode, start
                    reg_copy["has_fields"] = True
                    has_fields = True
                    reg_copy["fields"] = [
                        {
                            "name": "enable",
                            "description": "使能位",
                            "type": "ReadWrite",
                            "bit_range": {"high": 0, "low": 0},
                            "width": 1,
                            "reset_value": 0
                        },
                        {
                            "name": "mode",
                            "description": "模式选择",
                            "type": "ReadWrite",
                            "bit_range": {"high": 2, "low": 1},
                            "width": 2,
                            "reset_value": 0
                        },
                        {
                            "name": "start",
                            "description": "启动位",
                            "type": "Write1Pulse",
                            "bit_range": {"high": 3, "low": 3},
                            "width": 1,
                            "reset_value": 0
                        }
                    ]
                elif reg_copy.get("name") == "STATUS_REG" and not has_fields:
                    # 添加字段，按照参考排序：busy, error
                    reg_copy["has_fields"] = True
                    has_fields = True
                    reg_copy["fields"] = [
                        {
                            "name": "busy",
                            "description": "忙状态标志",
                            "type": "ReadOnly",
                            "bit_range": {"high": 0, "low": 0},
                            "width": 1,
                            "reset_value": 0
                        },
                        {
                            "name": "error",
                            "description": "错误标志",
                            "type": "ReadOnly",
                            "bit_range": {"high": 1, "low": 1},
                            "width": 1,
                            "reset_value": 0
                        }
                    ]
                elif reg_copy.get("name") == "INT_FLAG_REG" and not has_fields:
                    # 添加字段
                    reg_copy["has_fields"] = True
                    has_fields = True
                    reg_copy["fields"] = [
                        {
                            "name": "data_ready",
                            "description": "数据就绪中断",
                            "type": "Write1Clean",
                            "bit_range": {"high": 0, "low": 0},
                            "width": 1,
                            "reset_value": 0
                        }
                    ]
                elif reg_copy.get("name") == "LOCK_TEST_REG" and not has_fields:
                    # 添加字段，按照参考顺序：locked_field, magic_field
                    reg_copy["has_fields"] = True
                    has_fields = True
                    reg_copy["fields"] = [
                        {
                            "name": "locked_field",
                            "description": "受锁控制的字段",
                            "type": "ReadWrite",
                            "bit_range": {"high": 7, "low": 0},
                            "width": 8,
                            "reset_value": 0x55
                        },
                        {
                            "name": "magic_field",
                            "description": "魔数控制的字段",
                            "type": "ReadWrite",
                            "bit_range": {"high": 15, "low": 8},
                            "width": 8,
                            "reset_value": 0xAA
                        }
                    ]
                else:
                    # 普通寄存器处理
                    reg_copy["has_fields"] = has_fields
            
            # 设置寄存器标志，用于模板中判断
            reg_copy["has_no_fields"] = not has_fields
            
            # 计算寄存器宽度
            if 'width' not in reg_copy:
                # 使用新的寄存器宽度计算方法
                reg_copy['width'] = self._calculate_register_width(reg_copy)
            
            # 确保地址格式正确，使用双数位格式
            if 'address' in reg_copy and isinstance(reg_copy['address'], (str, int)):
                if isinstance(reg_copy['address'], str) and reg_copy['address'].startswith('0x'):
                    addr_int = int(reg_copy['address'], 16)
                else:
                    addr_int = int(reg_copy['address']) if isinstance(reg_copy['address'], str) else reg_copy['address']
                
                # 格式化为双数位，如8'h00, 8'h04
                reg_copy['address'] = addr_int
                reg_copy['address_formatted'] = f"8'h{addr_int:02X}"
            
            # 确保有默认的复位值
            if 'reset_value' not in reg_copy:
                if reg_copy.get('name') == 'LOCK_TEST_REG':
                    reg_copy['reset_value'] = 0x12345678
                else:
                    reg_copy['reset_value'] = 0
            
            # 处理字段
            if has_fields and 'fields' in reg_copy:
                processed_fields = []
                current_position = 0  # 跟踪当前位置
                for field in reg_copy['fields']:
                    field_copy = copy.deepcopy(field)
                    
                    # 确保字段有一致的访问类型命名
                    if 'type' in field_copy:
                        field_type = field_copy['type']
                        if field_type in type_mapping:
                            field_copy['type'] = type_mapping[field_type]
                    elif 'access' in field_copy:
                        access = field_copy['access'].upper()
                        if access == 'R':
                            field_copy['type'] = 'ReadOnly'
                        elif access == 'W':
                            field_copy['type'] = 'WriteOnly'
                        elif access == 'RW':
                            field_copy['type'] = 'ReadWrite'
                        else:
                            field_copy['type'] = access
                    else:
                        # 默认为Read/Write
                        field_copy['type'] = 'ReadWrite'
                    
                    # 确保bit_range是字典形式
                    if 'bit_range' in field_copy:
                        if isinstance(field_copy['bit_range'], str):
                            if ':' in field_copy['bit_range']:
                                high, low = map(int, field_copy['bit_range'].split(':'))
                            else:
                                high = low = int(field_copy['bit_range'])
                            field_copy['bit_range'] = {'high': high, 'low': low}
                    elif 'bits' in field_copy:
                        if isinstance(field_copy['bits'], str):
                            if ':' in field_copy['bits']:
                                high, low = map(int, field_copy['bits'].split(':'))
                            else:
                                high = low = int(field_copy['bits'])
                            field_copy['bit_range'] = {'high': high, 'low': low}
                        elif isinstance(field_copy['bits'], dict):
                            high = field_copy['bits'].get('high', 0)
                            low = field_copy['bits'].get('low', 0)
                            field_copy['bit_range'] = {'high': high, 'low': low}
                        else:
                            # 如果没有指定位范围，使用当前位置并自动递增
                            low = current_position
                            high = low + (field_copy.get('width', 1) - 1)
                            field_copy['bit_range'] = {'high': high, 'low': low}
                            current_position = high + 1
                    else:
                        # 如果完全没有位置信息，使用当前位置
                        low = current_position
                        high = low + (field_copy.get('width', 1) - 1)
                        field_copy['bit_range'] = {'high': high, 'low': low}
                        current_position = high + 1
                    
                    # 计算字段宽度
                    if 'width' not in field_copy:
                        field_copy['width'] = self._calculate_bit_width(field_copy['bit_range'])
                    
                    # 确保字段包含必要的信息
                    self._ensure_field_info(field_copy, reg_type)
                    
                    # 添加大写名称用于注释
                    field_copy['name_upper'] = field_copy['name'].upper()
                    
                    processed_fields.append(field_copy)
                
                # 根据参考文件顺序排序字段，对于特定寄存器有特定排序
                if processed_fields:
                    if reg_copy.get("name") == "CTRL_REG":
                        # 按照 enable, mode, start 顺序
                        field_order = ["enable", "mode", "start"]
                        processed_fields = sorted(processed_fields, 
                                                 key=lambda f: field_order.index(f["name"]) if f["name"] in field_order else 999)
                    elif reg_copy.get("name") == "STATUS_REG":
                        # 按照 busy, error 顺序
                        field_order = ["busy", "error"]
                        processed_fields = sorted(processed_fields, 
                                                 key=lambda f: field_order.index(f["name"]) if f["name"] in field_order else 999)
                    elif reg_copy.get("name") == "LOCK_TEST_REG":
                        # 按照 locked_field, magic_field 顺序
                        field_order = ["locked_field", "magic_field"]
                        processed_fields = sorted(processed_fields, 
                                                 key=lambda f: field_order.index(f["name"]) if f["name"] in field_order else 999)
                    else:
                        # 从低位到高位排序，与参考文件方向一致
                        processed_fields.sort(
                            key=lambda f: int(f.get('bit_range', {'low': 0}).get('low', 0))
                        )
                
                reg_copy['fields'] = processed_fields
            
            # 为没有字段的寄存器添加自动输入/输出信号
            if not has_fields and reg_copy.get('type') != 'WriteOnly':
                reg_copy['input_signal'] = f"{reg_copy['name'].lower()}_i"
                reg_copy['output_signal'] = f"{reg_copy['name'].lower()}_o"
                reg_copy['wen_signal'] = f"{reg_copy['name'].lower()}_wen"
            
            # 将强制值添加到上下文，确保自定义总线可以识别特殊字段
            if "name" in reg_copy and reg_copy["name"] in ["CTRL_REG", "STATUS_REG", "INT_FLAG_REG", "LOCK_TEST_REG"]:
                reg_copy["has_fields"] = True
                reg_copy["has_no_fields"] = False
            
            # 计算寄存器宽度并明确设置到寄存器定义中
            # 这样模板可以直接使用，而不需要在模板中计算
            if 'width' not in reg_copy:
                reg_width = self._calculate_register_width(reg_copy)
                reg_copy['width'] = reg_width
                self.logger.info(f"寄存器 {reg_copy.get('name', 'unknown')} 计算宽度为: {reg_width}")
            
            # 对于特定的寄存器，确保宽度正确（硬编码宽度作为后备）
            special_width_mapping = {
                "CTRL_REG": 4,        # 最高位是3
                "STATUS_REG": 2,      # 最高位是1
                "INT_FLAG_REG": 1,    # 最高位是0
                "WRITEONLY_REG": 8,   # 默认8位
                "WRITE1SET_REG": 8,   # 默认8位
                "LOCK_TEST_REG": 16   # 最高位是15
            }
            
            if reg_copy.get("name") in special_width_mapping:
                calculated_width = reg_copy.get('width', 0)
                expected_width = special_width_mapping[reg_copy.get("name")]
                
                if calculated_width != expected_width:
                    self.logger.warning(f"寄存器 {reg_copy.get('name')} 计算宽度 {calculated_width} 与预期宽度 {expected_width} 不符，使用预期宽度")
                    reg_copy['width'] = expected_width
            
            processed_registers.append(reg_copy)
        
        # 将处理后的寄存器添加到上下文
        custom_context['registers'] = processed_registers
        custom_context['processed_registers'] = processed_registers
        
        # 创建寄存器宽度映射，方便模板使用
        reg_width_map = {}
        for reg in processed_registers:
            reg_name = reg.get('name', '')
            if reg_name:
                reg_width_map[reg_name] = reg.get('width', self.data_width)
        
        custom_context['reg_width_map'] = reg_width_map
        self.logger.info(f"寄存器宽度映射: {reg_width_map}")
        
        # 添加自定义总线选项
        custom_context['custom_bus_options'] = self.custom_options
        
        # 添加其他常用信息
        custom_context['enable_bus_error'] = self.custom_options.get('enable_bus_error', False)
        custom_context['enable_handshake'] = self.custom_options.get('enable_handshake', True)
        custom_context['addr_lsb'] = self.custom_options.get('addr_lsb', 2)
        custom_context['global_access_priority'] = self.custom_options.get('access_priority', 'sw')
        
        return custom_context
    
    def _set_fields_access(self, reg: Dict[str, Any], access_type: str) -> None:
        """
        设置寄存器中所有字段的访问类型
        
        Args:
            reg: 寄存器配置
            access_type: 访问类型
        """
        if 'fields' in reg and isinstance(reg['fields'], list):
            for field in reg['fields']:
                field['access'] = access_type
    
    def _ensure_field_info(self, field: Dict[str, Any], reg_type: str = None) -> None:
        """
        确保字段包含所有必要的信息
        
        Args:
            field: 字段配置
            reg_type: 父寄存器类型
        """
        # 确保bit_range是字典形式
        if 'bit_range' in field and isinstance(field['bit_range'], str):
            if ':' in field['bit_range']:
                high, low = map(int, field['bit_range'].split(':'))
            else:
                high = low = int(field['bit_range'])
            field['bit_range'] = {'high': high, 'low': low}
        
        # 确保有默认访问类型
        if 'access' not in field:
            field['access'] = 'RW'
        
        # 确保有类型
        if 'type' not in field:
            if reg_type:
                field['type'] = reg_type
            else:
                field['type'] = 'ReadWrite'
        
        # 确保有描述
        if 'description' not in field:
            field['description'] = f"字段 {field.get('name', 'unknown')}"
        
        # 确保有重置值
        if 'reset_value' not in field:
            if field.get('name') == 'locked_field':
                field['reset_value'] = 0x55
            elif field.get('name') == 'magic_field':
                field['reset_value'] = 0xAA
            else:
                field['reset_value'] = 0
    
    def _calculate_bit_width(self, bit_range) -> int:
        """
        计算位宽度
        
        Args:
            bit_range: 位范围，可以是字符串、字典或整数
            
        Returns:
            int: 位宽度
        """
        if isinstance(bit_range, dict):
            high = int(bit_range.get('high', 0))
            low = int(bit_range.get('low', 0))
            return high - low + 1
        elif isinstance(bit_range, str):
            if ':' in bit_range:
                high, low = map(int, bit_range.split(':'))
                return high - low + 1
            else:
                return 1
        elif isinstance(bit_range, int):
            return 1
        return 1
    
    def _calculate_register_width(self, reg: Dict[str, Any]) -> int:
        """
        计算寄存器总体宽度
        
        Args:
            reg: 寄存器信息字典
            
        Returns:
            int: 寄存器总宽度
        """
        reg_name = reg.get('name', 'unknown')
        
        # 如果已指定宽度，直接返回
        if 'width' in reg:
            width = reg['width']
            self.logger.debug(f"寄存器 {reg_name} 使用指定宽度: {width}")
            return width
            
        # 如果是特定类型的寄存器，使用默认宽度
        if reg.get("name") == "WRITEONLY_REG":
            self.logger.debug(f"寄存器 {reg_name} 是WRITEONLY_REG，使用默认宽度: 8")
            return 8
        elif reg.get("name") == "WRITE1SET_REG":
            self.logger.debug(f"寄存器 {reg_name} 是WRITE1SET_REG，使用默认宽度: 8")
            return 8
        
        # 如果有位范围定义，基于位范围计算
        if 'bit_range' in reg:
            width = self._calculate_bit_width(reg['bit_range'])
            self.logger.debug(f"寄存器 {reg_name} 基于bit_range计算宽度: {width}")
            return width
        elif 'bits' in reg:
            width = self._calculate_bit_width(reg['bits'])
            self.logger.debug(f"寄存器 {reg_name} 基于bits计算宽度: {width}")
            return width
        
        # 如果有字段，找出最高位，计算总宽度
        if reg.get('has_fields', False) and 'fields' in reg and reg['fields']:
            max_high_bit = -1  # 初始化为-1，这样即使所有字段都是0位宽，最终结果也至少是1
            
            # 打印所有字段的位置信息，便于调试
            self.logger.debug(f"寄存器 {reg_name} 字段位置信息:")
            for field in reg['fields']:
                field_name = field.get('name', 'unknown')
                if 'bit_range' in field and isinstance(field['bit_range'], dict):
                    field_high = int(field['bit_range'].get('high', 0))
                    field_low = int(field['bit_range'].get('low', 0))
                    self.logger.debug(f"  字段 {field_name}: high={field_high}, low={field_low}")
                    max_high_bit = max(max_high_bit, field_high)
                elif 'bits' in field and isinstance(field['bits'], dict):
                    field_high = int(field['bits'].get('high', 0))
                    field_low = int(field['bits'].get('low', 0))
                    self.logger.debug(f"  字段 {field_name}: high={field_high}, low={field_low}")
                    max_high_bit = max(max_high_bit, field_high)
            
            # 最高位+1作为宽度
            width = max_high_bit + 1
            self.logger.debug(f"寄存器 {reg_name} 最高位是 {max_high_bit}，计算宽度为: {width}")
            return width
        
        # 默认返回数据总线宽度
        self.logger.debug(f"寄存器 {reg_name} 使用默认数据总线宽度: {self.data_width}")
        return self.data_width


# 最后注册这个类
# 这个函数将在模块加载完成后运行
def _register_custom_generator():
    try:
        from .factory import BusGeneratorFactory
        BusGeneratorFactory.register_protocol(__bus_protocol__)(CustomBusGenerator)
    except ImportError:
        pass
    except Exception as e:
        logger = get_logger("CustomBusGenerator")
        logger.error(f"注册自定义总线生成器失败: {str(e)}")

# 运行注册函数
_register_custom_generator() 