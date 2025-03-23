#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版寄存器文件生成器

一个用于自动生成Verilog寄存器文件的高级工具，支持所有寄存器类型和各种配置选项。
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional

# 导入增强的模块
try:
    from enhanced_register_types import RegisterTypeManager
    from enhanced_config_parser import ConfigParser, CommandLineParser
except ImportError:
    from src.enhanced_register_types import RegisterTypeManager
    from src.enhanced_config_parser import ConfigParser, CommandLineParser


class RegFileTemplateEngine:
    """寄存器文件模板引擎"""
    
    def __init__(self):
        """初始化模板引擎"""
        self.reg_type_manager = RegisterTypeManager()
    
    def generate_module_header(self, params: Dict[str, Any]) -> str:
        """生成模块头部"""
        module_header = f"""// 自动生成的寄存器文件
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// 生成器版本: 2.0.0

module {params['module_name']} (
    input wire                      clk,
    input wire                      rst_n,
"""
        return module_header
    
    def generate_port_declaration(self, params: Dict[str, Any]) -> str:
        """生成端口声明"""
        ports = []
        
        # 写端口
        for i in range(params['num_write_ports']):
            ports.append(f"    // 写端口 {i}")
            ports.append(f"    input wire                      wr_en_{i},")
            ports.append(f"    input wire [{params['addr_width']-1}:0]  wr_addr_{i},")
            ports.append(f"    input wire [{params['data_width']-1}:0]  wr_data_{i},")
            
            # 如果启用字节使能
            if params.get('byte_enable', False):
                num_bytes = params['data_width'] // 8
                ports.append(f"    input wire [{num_bytes-1}:0]  wr_be_{i},")
        
        # 读端口
        for i in range(params['num_read_ports']):
            if i == 0 and params['num_write_ports'] > 0:
                ports.append(f"    // 读端口 {i}")
            
            if i < params['num_read_ports'] - 1:
                ports.append(f"    input wire [{params['addr_width']-1}:0]  rd_addr_{i},")
                ports.append(f"    output reg [{params['data_width']-1}:0]  rd_data_{i},")
            else:
                ports.append(f"    input wire [{params['addr_width']-1}:0]  rd_addr_{i},")
                ports.append(f"    output reg [{params['data_width']-1}:0]  rd_data_{i}")
        
        return '\n'.join(ports) + "\n);"
    
    def generate_register_constants(self, params: Dict[str, Any]) -> str:
        """生成寄存器地址常量定义"""
        if 'registers' not in params:
            return "\n// 未定义特定寄存器\n"
        
        constants = ["\n// 寄存器地址常量定义"]
        
        for reg in params['registers']:
            reg_name = reg['name'].upper()
            description = reg['description'] if 'description' in reg else ""
            reg_type = reg['type'] if 'type' in reg else params.get('default_reg_type', 'ReadWrite')
            
            if description:
                constants.append(f"localparam ADDR_{reg_name} = {params['addr_width']}'h{reg['address']:X};   // {description} ({reg_type}类型)")
            else:
                constants.append(f"localparam ADDR_{reg_name} = {params['addr_width']}'h{reg['address']:X};   // {reg_type}类型")
        
        return '\n'.join(constants) + '\n'
    
    def generate_register_declaration(self, params: Dict[str, Any]) -> str:
        """生成寄存器声明"""
        if 'registers' not in params:
            return "\n// 未定义特定寄存器\n"
        
        declarations = ["\n// 寄存器声明"]
        
        for reg in params['registers']:
            reg_name = reg['name'].lower()
            width = reg.get('width', params['data_width'])
            description = reg.get('description', "")
            
            if description:
                declarations.append(f"reg [{width-1}:0] {reg_name}_reg;{' ' * (30 - len(reg_name))} // {description}")
            else:
                declarations.append(f"reg [{width-1}:0] {reg_name}_reg;")
            
            # 为需要写标志的寄存器类型添加写标志寄存器
            reg_type = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
            if reg_type in ['WriteOnce', 'WriteOnlyOnce']:
                declarations.append(f"reg {reg_name}_written;{' ' * (30 - len(reg_name))} // {reg_name} 写标志")
        
        return '\n'.join(declarations) + '\n'
    
    def generate_reset_logic(self, params: Dict[str, Any]) -> str:
        """生成复位逻辑"""
        reset_type = "posedge clk" if params.get('sync_reset', False) else "posedge clk or negedge rst_n"
        reset_condition = "rst_n == 1'b0" if params.get('sync_reset', False) else "!rst_n"
        
        reset_logic = f"""
// 复位逻辑
always @({reset_type}) begin
    if ({reset_condition}) begin
"""
        
        if 'registers' in params:
            for reg in params['registers']:
                reg_name = reg['name'].lower()
                width = reg.get('width', params['data_width'])
                reset_value = reg.get('reset_value', params.get('reset_value', '0'))
                
                # 处理复位值格式
                if isinstance(reset_value, str) and reset_value.startswith('0x'):
                    reset_logic += f"        {reg_name}_reg <= {width}'h{reset_value[2:]};\n"
                else:
                    reset_logic += f"        {reg_name}_reg <= {width}'d{reset_value};\n"
                
                # 为需要写标志的寄存器类型添加写标志寄存器复位
                reg_type = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                if reg_type in ['WriteOnce', 'WriteOnlyOnce']:
                    reset_logic += f"        {reg_name}_written <= 1'b0;\n"
        
        reset_logic += "    end\n    else begin\n"
        return reset_logic
    
    def generate_write_logic(self, params: Dict[str, Any]) -> str:
        """生成写逻辑"""
        write_logic = ""
        
        if 'registers' in params:
            for reg in params['registers']:
                reg_name = reg['name']
                reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                
                # 获取寄存器类型对象
                try:
                    reg_type = self.reg_type_manager.get_register_type(reg_type_name)
                except ValueError:
                    # 如果不支持的类型，使用ReadWrite作为默认
                    reg_type = self.reg_type_manager.get_register_type("ReadWrite")
                
                # 生成每个写端口的写逻辑
                for i in range(params['num_write_ports']):
                    # 检查是否支持字节使能
                    if params.get('byte_enable', False):
                        # 带字节使能的写逻辑，需要特殊处理
                        if reg_type_name == "ReadOnly":
                            # 只读寄存器不支持写入
                            write_logic += f"        // {reg_name} 是只读寄存器，忽略写操作\n"
                        elif reg_type_name == "Null":
                            # Null类型寄存器忽略写操作
                            write_logic += f"        // {reg_name} 是Null类型寄存器，忽略写操作\n"
                        elif reg_type_name in ["WriteOnce", "WriteOnlyOnce"]:
                            # 只写一次的寄存器需要检查写标志
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，只写一次
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()} && !{reg_name.lower()}_written) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= wr_data_{i}[7:0];
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= wr_data_{i}[15:8];
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= wr_data_{i}[23:16];
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= wr_data_{i}[31:24];
            {reg_name.lower()}_written <= 1'b1; // 设置写标志
        end
"""
                        elif reg_type_name == "Write1Clean":
                            # Write1Clean 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写1清零对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] & ~wr_data_{i}[7:0];
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] & ~wr_data_{i}[15:8];
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] & ~wr_data_{i}[23:16];
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] & ~wr_data_{i}[31:24];
        end
"""
                        elif reg_type_name == "Write1Set":
                            # Write1Set 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写1置位对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] | wr_data_{i}[7:0];
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] | wr_data_{i}[15:8];
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] | wr_data_{i}[23:16];
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] | wr_data_{i}[31:24];
        end
"""
                        elif reg_type_name == "Write0Clean":
                            # Write0Clean 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写0清零对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] & ~(~wr_data_{i}[7:0]);
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] & ~(~wr_data_{i}[15:8]);
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] & ~(~wr_data_{i}[23:16]);
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] & ~(~wr_data_{i}[31:24]);
        end
"""
                        elif reg_type_name == "Write0Set":
                            # Write0Set 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写0置位对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] | (~wr_data_{i}[7:0]);
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] | (~wr_data_{i}[15:8]);
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] | (~wr_data_{i}[23:16]);
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] | (~wr_data_{i}[31:24]);
        end
"""
                        elif reg_type_name == "Write1Toggle":
                            # Write1Toggle 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写1翻转对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] ^ wr_data_{i}[7:0];
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] ^ wr_data_{i}[15:8];
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] ^ wr_data_{i}[23:16];
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] ^ wr_data_{i}[31:24];
        end
"""
                        elif reg_type_name == "Write0Toggle":
                            # Write0Toggle 类型特殊处理
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器，写0翻转对应位
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= {reg_name.lower()}_reg[7:0] ^ (~wr_data_{i}[7:0]);
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= {reg_name.lower()}_reg[15:8] ^ (~wr_data_{i}[15:8]);
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= {reg_name.lower()}_reg[23:16] ^ (~wr_data_{i}[23:16]);
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= {reg_name.lower()}_reg[31:24] ^ (~wr_data_{i}[31:24]);
        end
"""
                        else:
                            # 其他类型使用标准写逻辑
                            write_logic += f"""        // {reg_name} 是{reg_type_name}类型寄存器
        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin
            if (wr_be_{i}[0]) {reg_name.lower()}_reg[7:0] <= wr_data_{i}[7:0];
            if (wr_be_{i}[1]) {reg_name.lower()}_reg[15:8] <= wr_data_{i}[15:8];
            if (wr_be_{i}[2]) {reg_name.lower()}_reg[23:16] <= wr_data_{i}[23:16];
            if (wr_be_{i}[3]) {reg_name.lower()}_reg[31:24] <= wr_data_{i}[31:24];
        end
"""
                    else:
                        # 不带字节使能的写逻辑，直接使用寄存器类型的写行为
                        write_logic += reg_type.get_write_behavior(
                            reg_name.upper(), 
                            reg.get('width', params['data_width']),
                            f"wr_addr_{i}",
                            f"wr_data_{i}",
                            f"wr_en_{i}"
                        )
        
        # 添加读操作触发的特殊逻辑
        if 'registers' in params:
            read_triggered_logic = ""
            for reg in params['registers']:
                reg_name = reg['name']
                reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                
                # 对于ReadClean和类似类型的寄存器，需要在读取后清零
                if reg_type_name in ["ReadClean", "WriteReadClean"]:
                    read_ports_check = []
                    for i in range(params['num_read_ports']):
                        read_ports_check.append(f"rd_addr_{i} == ADDR_{reg_name.upper()}")
                    
                    read_triggered_logic += f"""        // 如果读端口读取了{reg_name}，则清零（{reg_type_name}类型）
        if ({' || '.join(read_ports_check)}) begin
"""
                    for i in range(params['num_read_ports']):
                        read_triggered_logic += f"            if (rd_addr_{i} == ADDR_{reg_name.upper()}) \n                {reg_name.lower()}_reg <= {reg.get('width', params['data_width'])}'d0;\n"
                    
                    read_triggered_logic += "        end\n"
                
                # 对于ReadSet和类似类型的寄存器，需要在读取后置位
                elif reg_type_name in ["ReadSet", "WriteReadSet"]:
                    read_ports_check = []
                    for i in range(params['num_read_ports']):
                        read_ports_check.append(f"rd_addr_{i} == ADDR_{reg_name.upper()}")
                    
                    read_triggered_logic += f"""        // 如果读端口读取了{reg_name}，则置位（{reg_type_name}类型）
        if ({' || '.join(read_ports_check)}) begin
"""
                    for i in range(params['num_read_ports']):
                        read_triggered_logic += f"            if (rd_addr_{i} == ADDR_{reg_name.upper()}) \n                {reg_name.lower()}_reg <= {reg.get('width', params['data_width'])}'hFFFFFFFF;\n"
                    
                    read_triggered_logic += "        end\n"
            
            if read_triggered_logic:
                write_logic += "\n        // 读操作触发的特殊逻辑\n" + read_triggered_logic
        
        write_logic += "    end\nend\n"
        return write_logic
    
    def generate_read_logic(self, params: Dict[str, Any]) -> str:
        """生成读逻辑"""
        read_logic = ""
        
        for i in range(params['num_read_ports']):
            read_logic += f"""
// 读端口{i} 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_{i} = {params['data_width']}'d0;
    
"""
            if 'registers' in params:
                if len(params['registers']) <= 8:
                    # 对于寄存器数量较少的情况，使用if-else结构
                    for reg in params['registers']:
                        reg_name = reg['name']
                        reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                        
                        # 获取寄存器类型对象
                        try:
                            reg_type = self.reg_type_manager.get_register_type(reg_type_name)
                        except ValueError:
                            # 如果不支持的类型，使用ReadWrite作为默认
                            reg_type = self.reg_type_manager.get_register_type("ReadWrite")
                        
                        # 生成该寄存器的读行为
                        read_logic += reg_type.get_read_behavior(
                            reg_name.upper(), 
                            reg.get('width', params['data_width']),
                            f"rd_addr_{i}",
                            f"rd_data_{i}"
                        )
                else:
                    # 对于寄存器数量较多的情况，使用case结构
                    read_logic += "    case (rd_addr_" + str(i) + ")\n"
                    
                    for reg in params['registers']:
                        reg_name = reg['name']
                        reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                        
                        # 根据寄存器类型确定读取行为
                        if reg_type_name in ["Null", "WriteOnly", "WriteOnlyClean", "WriteOnlySet", "WriteOnlyOnce"]:
                            # 这些类型的寄存器读取时返回0
                            read_logic += f"        ADDR_{reg_name.upper()}: rd_data_{i} = {params['data_width']}'d0;  // {reg_type_name} 类型\n"
                        else:
                            # 其他类型的寄存器返回寄存器值
                            read_logic += f"        ADDR_{reg_name.upper()}: rd_data_{i} = {reg_name.lower()}_reg;  // {reg_type_name} 类型\n"
                    
                    read_logic += f"        default: rd_data_{i} = {params['data_width']}'d0;  // 未知地址返回0\n"
                    read_logic += "    endcase\n"
            
            read_logic += "end\n"
        
        return read_logic
    
    def generate_module_footer(self, params: Dict[str, Any]) -> str:
        """生成模块尾部"""
        return "\nendmodule"
    
    def generate_regfile(self, params: Dict[str, Any]) -> str:
        """生成完整的寄存器文件Verilog代码"""
        verilog_code = ""
        
        # 生成各部分代码
        verilog_code += self.generate_module_header(params)
        verilog_code += self.generate_port_declaration(params)
        verilog_code += self.generate_register_constants(params)
        verilog_code += self.generate_register_declaration(params)
        verilog_code += self.generate_reset_logic(params)
        verilog_code += self.generate_write_logic(params)
        verilog_code += self.generate_read_logic(params)
        verilog_code += self.generate_module_footer(params)
        
        return verilog_code


class EnhancedRegFileGenerator:
    """增强的寄存器文件生成器主类"""
    
    def __init__(self):
        """初始化生成器"""
        self.template_engine = RegFileTemplateEngine()
    
    def generate(self, config: Dict[str, Any]) -> Dict[str, str]:
        """生成所有输出文件"""
        result = {}
        
        # 生成Verilog代码
        verilog_code = self.template_engine.generate_regfile(config)
        result['verilog'] = verilog_code
        
        # 生成C语言头文件（未实现，仅占位）
        if config.get('gen_header', False):
            # TODO: 实现头文件生成
            header_code = "// TODO: 实现头文件生成\n"
            result['header'] = header_code
        
        # 生成Markdown文档（未实现，仅占位）
        if config.get('gen_doc', False):
            # TODO: 实现文档生成
            doc_content = "# 寄存器文件文档\n\n// TODO: 实现文档生成\n"
            result['doc'] = doc_content
        
        return result
    
    def save_files(self, result: Dict[str, str], config: Dict[str, Any]) -> None:
        """保存生成的文件"""
        output_dir = config.get('output_dir', '')
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存Verilog文件
        verilog_path = os.path.join(output_dir, config.get('output', 'regfile.v'))
        with open(verilog_path, 'w', encoding='utf-8') as f:
            f.write(result['verilog'])
        print(f"Verilog文件已生成: {verilog_path}")
        
        # 保存C语言头文件
        if 'header' in result:
            if config.get('header_output'):
                header_path = os.path.join(output_dir, config.get('header_output'))
            else:
                header_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.h')
            
            with open(header_path, 'w', encoding='utf-8') as f:
                f.write(result['header'])
            print(f"C语言头文件已生成: {header_path}")
        
        # 保存Markdown文档
        if 'doc' in result:
            if config.get('doc_output'):
                doc_path = os.path.join(output_dir, config.get('doc_output'))
            else:
                doc_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.md')
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(result['doc'])
            print(f"Markdown文档已生成: {doc_path}")


def setup_argument_parser() -> argparse.ArgumentParser:
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description="自动生成Verilog寄存器文件")
    
    # 基本参数
    parser.add_argument("-m", "--module", default="regfile", help="模块名称")
    parser.add_argument("-d", "--data-width", type=int, default=32, help="数据宽度 (位)")
    parser.add_argument("-a", "--addr-width", type=int, default=8, help="地址宽度 (位)")
    parser.add_argument("-wr", "--write-ports", type=int, default=1, help="写端口数量")
    parser.add_argument("-rd", "--read-ports", type=int, default=2, help="读端口数量")
    
    # 复位选项
    parser.add_argument("--sync-reset", action="store_true", help="使用同步复位 (默认为异步复位)")
    parser.add_argument("--reset-value", default="0", help="复位初始化值 (支持十六进制，如0xF)")
    
    # 高级选项
    parser.add_argument("--byte-enable", action="store_true", help="启用字节使能")
    parser.add_argument("--config", help="从JSON、YAML或Excel文件加载配置")
    parser.add_argument("--implementation", choices=["always", "instance"], default="instance", 
                       help="实现方式: always块或寄存器例化 (默认: instance)")
    parser.add_argument("--default-reg-type", default="ReadWrite", 
                       help="默认寄存器类型 (默认: ReadWrite)")
    
    # 输出选项
    parser.add_argument("-o", "--output", default="regfile.v", help="输出Verilog文件名")
    parser.add_argument("--gen-header", action="store_true", help="生成C语言头文件")
    parser.add_argument("--header-output", help="C语言头文件输出路径 (默认为与Verilog文件同名，扩展名为.h)")
    parser.add_argument("--output-dir", help="输出目录路径")
    parser.add_argument("--gen-doc", action="store_true", help="生成Markdown文档")
    parser.add_argument("--doc-output", help="Markdown文档输出路径 (默认为与Verilog文件同名，扩展名为.md)")
    
    return parser


def main():
    """主函数"""
    # 解析命令行参数
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 初始化配置
    if args.config:
        # 从配置文件加载
        config = ConfigParser.parse_config_file(args.config)
    else:
        # 从命令行参数加载
        config = CommandLineParser.parse_args_to_config(args)
    
    # 创建生成器并生成文件
    generator = EnhancedRegFileGenerator()
    result = generator.generate(config)
    generator.save_files(result, config)


if __name__ == "__main__":
    main() 