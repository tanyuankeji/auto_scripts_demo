#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog代码生成模块

负责生成寄存器文件的Verilog代码。
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Callable
import os

try:
    from register_types import RegisterTypeManager
except ImportError:
    from src.register_types import RegisterTypeManager


class TemplateEngine:
    """模板引擎，用于生成不同部分的Verilog代码"""
    
    def __init__(self):
        self.templates = {
            'module_header': self._gen_module_header,
            'port_declaration': self._gen_port_declaration,
            'register_declaration': self._gen_register_declaration,
            'register_constants': self._gen_register_constants,
            'reset_logic': self._gen_reset_logic,
            'write_logic': self._gen_write_logic,
            'read_logic': self._gen_read_logic,
            'byte_enable_logic': self._gen_byte_enable_logic,
            'register_instances': self._gen_register_instances,
            'module_footer': self._gen_module_footer
        }
        self.reg_type_manager = RegisterTypeManager()
    
    def register_template(self, name: str, generator: Callable) -> None:
        """注册自定义模板生成器"""
        self.templates[name] = generator
    
    def generate(self, template_name: str, params: Dict[str, Any]) -> str:
        """生成指定模板的代码"""
        if template_name not in self.templates:
            raise ValueError(f"未知的模板名称: {template_name}")
        return self.templates[template_name](params)
    
    def _gen_module_header(self, params: Dict[str, Any]) -> str:
        """生成模块头部"""
        return f"""// Auto-generated Register File
// Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Generator Version: 1.0.0

module {params['module_name']} (
    input wire                      clk,
    input wire                      rst_n,"""
    
    def _gen_port_declaration(self, params: Dict[str, Any]) -> str:
        """生成端口声明"""
        ports = []
        
        # 写端口
        for i in range(params['num_write_ports']):
            ports.append(f"    input wire                      wr_en_{i},")
            ports.append(f"    input wire [{params['addr_width']-1}:0]  wr_addr_{i},")
            ports.append(f"    input wire [{params['data_width']-1}:0]  wr_data_{i},")
            
            # 如果启用字节使能
            if params.get('byte_enable', False):
                num_bytes = params['data_width'] // 8
                ports.append(f"    input wire [{num_bytes-1}:0]  wr_be_{i},")
        
        # 读端口
        for i in range(params['num_read_ports']):
            ports.append(f"    input wire [{params['addr_width']-1}:0]  rd_addr_{i},")
            ports.append(f"    output reg [{params['data_width']-1}:0]  rd_data_{i}{'' if i == params['num_read_ports']-1 else ','}")
        
        return '\n'.join(ports) + "\n);"
    
    def _gen_register_constants(self, params: Dict[str, Any]) -> str:
        """生成寄存器地址常量定义"""
        if 'registers' not in params:
            return "// 没有定义特定寄存器\n"
        
        constants = ["\n// 寄存器地址常量定义"]
        
        for reg in params['registers']:
            reg_name = reg['name'].upper()
            constants.append(f"localparam ADDR_{reg_name} = {params['addr_width']}'h{reg['address']:X};")
        
        return '\n'.join(constants) + '\n'
    
    def _gen_register_declaration(self, params: Dict[str, Any]) -> str:
        """生成寄存器声明"""
        if 'implementation' in params and params['implementation'] == 'instance':
            if 'registers' in params:
                declarations = ["\n// 寄存器声明"]
                for reg in params['registers']:
                    reg_name = reg['name'].lower()
                    declarations.append(f"reg [{reg.get('width', params['data_width'])-1}:0] {reg_name}_reg;")
                return '\n'.join(declarations) + '\n'
            else:
                return f"""\n// 寄存器数组声明
reg [{params['data_width']-1}:0] reg_array [0:{2**params['addr_width']-1}];\n"""
        else:
            return f"""\n// 寄存器数组声明
reg [{params['data_width']-1}:0] reg_array [0:{2**params['addr_width']-1}];\n"""
    
    def _gen_reset_logic(self, params: Dict[str, Any]) -> str:
        """生成复位逻辑"""
        reset_type = "posedge clk" if params['sync_reset'] else "posedge clk or negedge rst_n"
        reset_condition = "!rst_n"
        
        if 'implementation' in params and params['implementation'] == 'instance' and 'registers' in params:
            reset_logic = f"""// 复位逻辑
always @({reset_type}) begin
    if ({reset_condition}) begin
"""
            for reg in params['registers']:
                reg_name = reg['name'].lower()
                reset_value = reg.get('reset_value', params['reset_value'])
                reset_logic += f"        {reg_name}_reg <= {reg.get('width', params['data_width'])}'d{reset_value};\n"
            
            reset_logic += "    end\n"
            return reset_logic
        else:
            reset_logic = f"""// 复位和写逻辑
always @({reset_type}) begin
    if ({reset_condition}) begin
        integer i;
        for (i = 0; i < {2**params['addr_width']}; i = i + 1) begin
            reg_array[i] <= {params['data_width']}'d{params['reset_value']};
        end
    end
    else begin
"""
            return reset_logic
    
    def _gen_write_logic(self, params: Dict[str, Any]) -> str:
        """生成写逻辑"""
        if 'implementation' in params and params['implementation'] == 'instance' and 'registers' in params:
            write_logic = ""
            for i in range(params['num_write_ports']):
                write_logic += f"        // 写端口 {i} 逻辑\n"
                
                for reg in params['registers']:
                    reg_name = reg['name'].lower()
                    reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                    reg_type = self.reg_type_manager.get_register_type(reg_type_name)
                    
                    # 生成该寄存器的写行为
                    if params.get('byte_enable', False):
                        # 带字节使能的写逻辑
                        write_logic += f"        // {reg_name} 写逻辑（带字节使能）\n"
                        write_logic += f"        if (wr_en_{i} && wr_addr_{i} == ADDR_{reg_name.upper()}) begin\n"
                        num_bytes = params['data_width'] // 8
                        for b in range(num_bytes):
                            byte_pos = b * 8
                            write_logic += f"            if (wr_be_{i}[{b}]) {reg_name}_reg[{byte_pos+7}:{byte_pos}] <= wr_data_{i}[{byte_pos+7}:{byte_pos}];\n"
                        write_logic += "        end\n"
                    else:
                        # 普通写逻辑
                        write_logic += reg_type.get_write_behavior(
                            reg_name.upper(), 
                            reg.get('width', params['data_width']),
                            f"wr_addr_{i}",
                            f"wr_data_{i}",
                            f"wr_en_{i}"
                        )
                
                write_logic += "\n"
            
            write_logic += "    end\nend\n"
            return write_logic
        else:
            write_logic = ""
            
            for i in range(params['num_write_ports']):
                if params.get('byte_enable', False):
                    write_logic += self._gen_byte_enable_logic(params, i)
                else:
                    write_logic += f"""        if (wr_en_{i}) begin
            reg_array[wr_addr_{i}] <= wr_data_{i};
        end
"""
            
            write_logic += "    end\nend\n"
            return write_logic
    
    def _gen_byte_enable_logic(self, params: Dict[str, Any], port_idx: int) -> str:
        """生成字节使能逻辑"""
        num_bytes = params['data_width'] // 8
        byte_logic = f"""        if (wr_en_{port_idx}) begin
"""
        
        for b in range(num_bytes):
            byte_pos = b * 8
            byte_logic += f"            if (wr_be_{port_idx}[{b}]) reg_array[wr_addr_{port_idx}][{byte_pos+7}:{byte_pos}] <= wr_data_{port_idx}[{byte_pos+7}:{byte_pos}];\n"
        
        byte_logic += "        end\n"
        return byte_logic
    
    def _gen_read_logic(self, params: Dict[str, Any]) -> str:
        """生成读逻辑"""
        if 'implementation' in params and params['implementation'] == 'instance' and 'registers' in params:
            read_logic = ""
            
            for i in range(params['num_read_ports']):
                read_logic += f"""// 读端口 {i} 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_{i} = {params['data_width']}'d0;
    
"""
                for reg in params['registers']:
                    reg_name = reg['name'].lower()
                    reg_type_name = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                    reg_type = self.reg_type_manager.get_register_type(reg_type_name)
                    
                    # 生成该寄存器的读行为
                    read_logic += reg_type.get_read_behavior(
                        reg_name.upper(), 
                        reg.get('width', params['data_width']),
                        f"rd_addr_{i}",
                        f"rd_data_{i}"
                    )
                
                read_logic += "end\n\n"
            
            return read_logic
        else:
            read_logic = ""
            
            for i in range(params['num_read_ports']):
                read_logic += f"""// 读端口 {i} 组合逻辑
always @(*) begin
    rd_data_{i} = reg_array[rd_addr_{i}];
end

"""
            
            return read_logic
    
    def _gen_register_instances(self, params: Dict[str, Any]) -> str:
        """生成寄存器实例化代码（如果使用instance实现方式）"""
        # 此函数暂不使用，仅为将来扩展保留
        return ""
    
    def _gen_module_footer(self, params: Dict[str, Any]) -> str:
        """生成模块尾部"""
        footer = """// 可能的扩展：
// 1. 写冲突检测
// 2. 读写冲突行为控制
// 3. 多时钟域支持

endmodule
"""
        return footer


class ParameterValidator:
    """参数验证器，确保用户输入的参数有效"""
    
    @staticmethod
    def validate_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """验证并处理参数"""
        # 数据宽度必须是8的倍数，如果启用字节使能
        if params.get('byte_enable', False) and params['data_width'] % 8 != 0:
            raise ValueError(f"启用字节使能时，数据宽度必须是8的倍数，当前值: {params['data_width']}")
        
        # 地址宽度不能太大，避免生成过大的寄存器文件
        if params['addr_width'] > 12:  # 4096个寄存器
            print(f"警告: 地址宽度 {params['addr_width']} 将生成 {2**params['addr_width']} 个寄存器，这可能导致综合问题")
        
        # 端口数量检查
        if params['num_read_ports'] < 1 or params['num_write_ports'] < 1:
            raise ValueError("读端口和写端口数量必须至少为1")
        
        # 复位值检查
        if isinstance(params['reset_value'], str):
            # 支持十六进制输入
            try:
                params['reset_value'] = int(params['reset_value'], 0)
            except ValueError:
                raise ValueError(f"无效的复位值: {params['reset_value']}")
        
        # 验证实现方式
        if 'implementation' in params and params['implementation'] not in ['always', 'instance']:
            raise ValueError(f"不支持的实现方式: {params['implementation']}")
        
        # 验证寄存器类型
        if 'registers' in params:
            reg_type_manager = RegisterTypeManager()
            for reg in params['registers']:
                reg_type = reg.get('type', params.get('default_reg_type', 'ReadWrite'))
                if reg_type not in reg_type_manager.get_all_register_types():
                    raise ValueError(f"不支持的寄存器类型: {reg_type}")
        
        return params


class VerilogGenerator:
    """Verilog代码生成器，负责生成寄存器文件的Verilog代码"""
    
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.validator = ParameterValidator()
    
    def generate_regfile(self, params: Dict[str, Any]) -> str:
        """生成完整的寄存器文件Verilog代码"""
        # 验证参数
        params = self.validator.validate_params(params)
        
        # 生成各部分代码
        module_header = self.template_engine.generate('module_header', params)
        port_declaration = self.template_engine.generate('port_declaration', params)
        register_constants = self.template_engine.generate('register_constants', params)
        register_declaration = self.template_engine.generate('register_declaration', params)
        reset_logic = self.template_engine.generate('reset_logic', params)
        write_logic = self.template_engine.generate('write_logic', params)
        read_logic = self.template_engine.generate('read_logic', params)
        module_footer = self.template_engine.generate('module_footer', params)
        
        # 组合完整代码
        verilog_code = f"{module_header}\n{port_declaration}{register_constants}{register_declaration}\n{reset_logic}{write_logic}\n{read_logic}{module_footer}"
        
        return verilog_code

    def save_files(self, result: Dict[str, str], config: Dict[str, Any]) -> None:
        """保存生成的文件"""
        output_dir = config.get('output_dir', '')
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存Verilog文件 - 修改此处，指定UTF-8编码
        verilog_path = os.path.join(output_dir, config.get('output', 'regfile.v'))
        with open(verilog_path, 'w', encoding='utf-8') as f:  # 明确指定UTF-8编码
            f.write(result['verilog'])
        print(f"Verilog文件已生成: {verilog_path}")
        
        # 保存C语言头文件 - 同样修改
        if 'header' in result:
            if config.get('header_output'):
                header_path = os.path.join(output_dir, config.get('header_output'))
            else:
                header_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.h')
            
            with open(header_path, 'w', encoding='utf-8') as f:  # 明确指定UTF-8编码
                f.write(result['header'])
            print(f"C语言头文件已生成: {header_path}")
        
        # 保存Markdown文档 - 同样修改
        if 'doc' in result:
            if config.get('doc_output'):
                doc_path = os.path.join(output_dir, config.get('doc_output'))
            else:
                doc_path = os.path.join(output_dir, os.path.splitext(config.get('output', 'regfile.v'))[0] + '.md')
            
            with open(doc_path, 'w', encoding='utf-8') as f:  # 明确指定UTF-8编码
                f.write(result['doc'])
            print(f"Markdown文档已生成: {doc_path}")


if __name__ == "__main__":
    # 测试代码
    test_params = {
        'module_name': 'test_regfile',
        'data_width': 32,
        'addr_width': 4,  # 16个寄存器
        'num_read_ports': 2,
        'num_write_ports': 1,
        'sync_reset': False,
        'reset_value': 0,
        'byte_enable': False,
        'implementation': 'instance',
        'registers': [
            {
                'name': 'CTRL',
                'address': 0,
                'width': 32,
                'type': 'ReadWrite',
                'reset_value': 0,
                'description': '控制寄存器'
            },
            {
                'name': 'STATUS',
                'address': 4,
                'width': 32,
                'type': 'ReadOnly',
                'reset_value': 0,
                'description': '状态寄存器'
            }
        ]
    }
    
    generator = VerilogGenerator()
    verilog_code = generator.generate_regfile(test_params)
    print(verilog_code)