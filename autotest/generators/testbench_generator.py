#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Testbench生成器模块

基于解析得到的Verilog模块信息，使用jinja2模板生成testbench文件
支持生成普通testbench和自动验证环境
"""

import os
import logging
from pathlib import Path

# 尝试导入jinja2
try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logging.warning("jinja2未安装，将使用内置的字符串模板")

logger = logging.getLogger(__name__)

class TestbenchGenerator:
    """Testbench生成器类"""
    
    def __init__(self, verilog_parser, top_module, template_dir, clk_name='clk', rst_name='rst_n'):
        """
        初始化生成器
        
        参数:
            verilog_parser: VerilogParser对象实例
            top_module: 顶层模块名
            template_dir: 模板目录路径
            clk_name: 时钟信号名称
            rst_name: 复位信号名称
        """
        self.parser = verilog_parser
        self.top_module = top_module
        self.template_dir = Path(template_dir)
        self.clk_name = clk_name
        self.rst_name = rst_name
        
        # 初始化jinja2环境（如果可用）
        if JINJA2_AVAILABLE:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.template_dir),
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=False
            )
        else:
            self.env = None
    
    def generate_testbench(self, with_verification=False):
        """
        生成testbench代码
        
        参数:
            with_verification: 是否包含自动验证功能
        
        返回:
            生成的testbench代码
        """
        if self.env and os.path.exists(self.template_dir / "testbench.sv.j2"):
            return self._generate_with_jinja2(with_verification)
        else:
            return self._generate_with_string_template(with_verification)
    
    def _generate_with_jinja2(self, with_verification):
        """使用jinja2模板生成testbench"""
        try:
            template = self.env.get_template("testbench.sv.j2")
            
            # 准备模板上下文
            context = {
                "top_module": self.top_module,
                "signals": self.parser.signals if self.parser else [],
                "parameters": self.parser.parameters if self.parser else [],
                "param_dict": self.parser.param_dict if self.parser else {},
                "with_verification": with_verification,
                "clk_name": self.clk_name,
                "rst_name": self.rst_name
            }
            
            # 如果需要验证功能，添加相关数据
            if with_verification and self.parser:
                context.update({
                    "valid_signals": self.parser.valid_signals,
                    "signal_dict": self.parser.signal_dict,
                    "check_valid": self.parser.get_valid_signal_for_verification()
                })
            
            # 渲染模板
            return template.render(**context)
        
        except Exception as e:
            logger.error(f"使用jinja2生成testbench失败: {str(e)}")
            return self._generate_with_string_template(with_verification)
    
    def _generate_with_string_template(self, with_verification):
        """使用字符串模板生成testbench"""
        # 基本testbench结构
        tb = self._generate_testbench_header()
        
        # 参数声明
        tb += self._generate_parameter_declarations()
        
        # 信号声明
        tb += self._generate_signal_declarations()
        
        # 时钟和复位
        tb += self._generate_clock_reset()
        
        # 信号驱动
        tb += self._generate_signal_drivers()
        
        # 模块实例化
        tb += self._generate_module_instantiation()
        
        # 如果需要验证功能
        if with_verification:
            tb += self._generate_verification_code()
        
        # 结束模块
        tb += "endmodule\n"
        
        return tb
    
    def _generate_testbench_header(self):
        """生成testbench头部"""
        header = '''`define DELAY(N, clk) begin \\
	repeat(N) @(posedge clk);\\
	#1ps;\\
end

'''
        # 如果需要验证，添加导入语句
        if self.parser and hasattr(self.parser, 'valid_signals') and self.parser.valid_signals:
            header += f"import {self.top_module}_pkg::*;\n\n"
        
        header += f'''module testbench();

//-------------------------------------{{{{common cfg
timeunit 1ns;
timeprecision 1ps;
initial $timeformat(-9,3,"ns",6);

string tc_name;
int tc_seed;

initial begin
    if(!$value$plusargs("tc_name=%s", tc_name)) $error("no tc_name!");
    else $display("tc name = %0s", tc_name);
    if(!$value$plusargs("ntb_random_seed=%0d", tc_seed)) $error("no tc_seed");
    else $display("tc seed = %0d", tc_seed);
end
//-------------------------------------}}}}

'''
        return header
    
    def _generate_parameter_declarations(self):
        """生成参数声明"""
        if not self.parser or not hasattr(self.parser, 'parameters') or not self.parser.parameters:
            return ""
        
        decl = "//-------------------------------------{{{parameter declare\n"
        for param in self.parser.parameters:
            decl += f"parameter {param} = {self.parser.param_dict[param]};\n"
        decl += "//-------------------------------------}}}\n\n"
        return decl
    
    def _generate_signal_declarations(self):
        """生成信号声明"""
        if not self.parser or not hasattr(self.parser, 'signals') or not self.parser.signals:
            return f"//-------------------------------------{{{{signal declare\nlogic {self.clk_name}, {self.rst_name};\n//-------------------------------------}}}}\n\n"
        
        decl = "//-------------------------------------{{{signal declare\n"
        
        # 首先检查是否已经有与clk_name和rst_name匹配的信号
        has_clk = False
        has_rst = False
        
        for sig in self.parser.signals:
            if sig.name == self.clk_name:
                has_clk = True
            if sig.name == self.rst_name:
                has_rst = True
            decl += f"logic {sig.width} {sig.name};\n"
        
        # 如果没有找到时钟或复位信号，添加它们
        if not has_clk:
            decl += f"logic {self.clk_name};\n"
        if not has_rst:
            decl += f"logic {self.rst_name};\n"
            
        decl += "//-------------------------------------}}}\n\n"
        return decl
    
    def _generate_clock_reset(self):
        """生成时钟和复位代码"""
        return f'''//-------------------------------------{{{{clk/rst cfg
// 初始化时钟和复位信号
initial begin
    {self.clk_name} = 1'b0;
    {self.rst_name} = 1'b0;
end

// 时钟生成
initial forever #5ns {self.clk_name} = ~{self.clk_name};

// 复位控制
initial begin
    {self.rst_name} = 1'b0;
	`DELAY(30, {self.clk_name});
	{self.rst_name} = 1'b1;
end

// 测试超时控制
initial begin
    #100000ns $finish;
end
//-------------------------------------}}}}

'''
    
    def _generate_signal_drivers(self):
        """生成信号驱动代码"""
        if not self.parser or not hasattr(self.parser, 'signals') or not self.parser.signals:
            return f'''//-------------------------------------{{{{other sig assign
initial begin
    `DELAY(50, {self.clk_name});
end
//-------------------------------------}}}}

'''
        
        # 生成valid信号驱动
        valid_force = "//-------------------------------------{{{valid sig assign\n"
        # 生成ready信号驱动
        ready_force = "//-------------------------------------{{{ready sig assign\n"
        # 生成数据信号驱动
        ctrl_sig_force = "//-------------------------------------{{{data sig assign\n"
        # 生成其他信号驱动
        other_force = "//-------------------------------------{{{other sig assign\ninitial begin\n"
        
        for sig in self.parser.signals:
            if sig.port == "input" and sig.name != self.clk_name and sig.name != self.rst_name:
                if sig.valid_en() == 1:
                    valid_force += f"always @(posedge {self.clk_name} or negedge {self.rst_name})begin\n"
                    valid_force += "    if(~"+self.rst_name+")begin\n"
                    valid_force += f"        {sig.name} <= 0;\n"
                    valid_force += "    end\n"
                    valid_force += f"    else if({sig.ready_sig} || ~{sig.name})begin\n"
                    valid_force += f"        {sig.name} <= $urandom;\n"
                    valid_force += "    end\n"
                    valid_force += "end\n\n"
                elif sig.ready_en() == 1:
                    ready_force += f"always @(posedge {self.clk_name} or negedge {self.rst_name})begin\n"
                    ready_force += "    if(~"+self.rst_name+")begin\n"
                    ready_force += f"        {sig.name} <= 0;\n"
                    ready_force += "    end\n"
                    ready_force += "    else begin\n"
                    ready_force += f"        {sig.name} <= $urandom;\n"
                    ready_force += "    end\n"
                    ready_force += "end\n\n"
                elif hasattr(sig, 'find_valid_sig') and sig.find_valid_sig == 1 and hasattr(sig, 'find_ready_sig') and sig.find_ready_sig == 1:
                    ctrl_sig_force += f"always @(posedge {self.clk_name} or negedge {self.rst_name})begin\n"
                    ctrl_sig_force += "    if(~"+self.rst_name+")begin\n"
                    ctrl_sig_force += f"        {sig.name} <= 'x;\n"
                    ctrl_sig_force += "    end\n"
                    ctrl_sig_force += f"    else if({sig.valid_sig} && {sig.ready_sig})begin\n"
                    ctrl_sig_force += f"        {sig.name} <= $urandom;\n"
                    ctrl_sig_force += "    end\n"
                    ctrl_sig_force += f"    else if({sig.valid_sig} == 0)begin\n"
                    ctrl_sig_force += f"        {sig.name} <= $urandom;\n"
                    ctrl_sig_force += "    end\n"
                    ctrl_sig_force += "end\n\n"
                elif hasattr(sig, 'find_valid_sig') and sig.find_valid_sig == 1:
                    ctrl_sig_force += f"always @(posedge {self.clk_name} or negedge {self.rst_name})begin\n"
                    ctrl_sig_force += "    if(~"+self.rst_name+")begin\n"
                    ctrl_sig_force += f"        {sig.name} <= 'x;\n"
                    ctrl_sig_force += "    end\n"
                    ctrl_sig_force += f"    else if({sig.valid_sig} == 0)begin\n"
                    ctrl_sig_force += f"        {sig.name} <= $urandom;\n"
                    ctrl_sig_force += "    end\n"
                    ctrl_sig_force += "end\n\n"
                else:
                    other_force += f"    {sig.name} = $urandom;\n"
        
        valid_force += "//-------------------------------------}}}\n\n"
        ready_force += "//-------------------------------------}}}\n\n"
        ctrl_sig_force += "//-------------------------------------}}}\n\n"
        
        other_force += f"    `DELAY(50, {self.clk_name});\n"
        other_force += "end\n"
        other_force += "//-------------------------------------}}}\n\n"
        
        return valid_force + ready_force + ctrl_sig_force + other_force
    
    def _generate_module_instantiation(self):
        """生成模块实例化代码"""
        if not self.parser or not hasattr(self.parser, 'signals') or not self.parser.signals:
            return ""
        
        inst = f"//-------------------------------------{{{{rtl inst\n"
        
        # 参数实例化
        if not self.parser.parameters:
            inst += f"{self.top_module} u_{self.top_module}(\n"
        else:
            inst += f"{self.top_module} #(\n"
            for i, param in enumerate(self.parser.parameters):
                inst += f"    .{param}({param})"
                if i < len(self.parser.parameters) - 1:
                    inst += ",\n"
            inst += f"\n) \nu_{self.top_module}(\n"
        
        # 端口实例化
        for i, sig in enumerate(self.parser.signals):
            inst += f"    .{sig.name}({sig.name})"
            if i < len(self.parser.signals) - 1:
                inst += ",\n"
        
        inst += "\n);\n"
        inst += "//-------------------------------------}}}\n\n"
        return inst
    
    def _generate_verification_code(self):
        """生成验证代码"""
        if not self.parser or not hasattr(self.parser, 'valid_signals') or not self.parser.valid_signals:
            return ""
        
        ver_code = "//-------------------------------------{{{auto_verification\n"
        
        # 输入队列采集任务
        ver_code += "task in_queue_gain();\n"
        ver_code += "  while(1)begin\n"
        ver_code += f"    @(negedge {self.clk_name});\n"
        
        for valid_name in self.parser.valid_signals:
            valid = self.parser.signal_dict[valid_name]
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0 and valid.port == "input":
                ver_code += f"    if({valid.name} && {valid.ready_sig})begin\n"
                ver_code += f"      {valid.name}_struct {valid.name}_dat;\n"
                for sig in valid.bus_list:
                    ver_code += f"      {valid.name}_dat.{sig.name} = {sig.name};\n"
                ver_code += f"      {valid.name}_bus_q.push_back({valid.name}_dat);\n"
                ver_code += "    end//if-end \n"
        
        ver_code += "  end//while-end \n"
        ver_code += "endtask: in_queue_gain\n\n"
        
        # 输出队列采集任务
        ver_code += "task out_queue_gain();\n"
        ver_code += "  while(1)begin\n"
        ver_code += f"    @(negedge {self.clk_name});\n"
        
        for valid_name in self.parser.valid_signals:
            valid = self.parser.signal_dict[valid_name]
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0 and valid.port == "output":
                ver_code += f"    if({valid.name} && {valid.ready_sig})begin\n"
                ver_code += f"      {valid.name}_struct {valid.name}_dat;\n"
                for sig in valid.bus_list:
                    ver_code += f"      {valid.name}_dat.{sig.name} = {sig.name};\n"
                ver_code += f"      {valid.name}_bus_q.push_back({valid.name}_dat);\n"
                ver_code += "    end//if-end \n"
        
        ver_code += "  end//while-end \n"
        ver_code += "endtask: out_queue_gain\n\n"
        
        # 参考模型队列任务（用户需要实现）
        ver_code += "task rm_queue_gain();\n"
        
        for valid_name in self.parser.valid_signals:
            valid = self.parser.signal_dict[valid_name]
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0:
                ver_code += f"  {valid.name}_struct {valid.name}_dat;\n"
        
        ver_code += "  //while(1)begin\n"
        
        for valid_name in self.parser.valid_signals:
            valid = self.parser.signal_dict[valid_name]
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0 and valid.port == "input":
                ver_code += f"    //wait({valid.name}_bus_q.size > 0);\n"
                ver_code += f"    //{valid.name}_dat = {valid.name}_bus_q.pop_front();\n"
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0 and valid.port == "output":
                ver_code += f"    //rm_q.push_back({valid.name}_dat);\n"
        
        ver_code += "  //end\n"
        ver_code += "endtask: rm_queue_gain\n\n"
        
        # 队列检查任务
        check_valid = self.parser.get_valid_signal_for_verification()
        if check_valid:
            ver_code += "task queue_check();\n"
            ver_code += "  while(1)begin\n"
            ver_code += f"    {check_valid}_struct rm_data;\n"
            ver_code += f"    {check_valid}_struct dual_data;\n"
            ver_code += f"    wait({check_valid}_bus_q.size() > 0);\n"
            ver_code += f"    dual_data = {check_valid}_bus_q.pop_front();\n"
            ver_code += "    if(rm_q.size() == 0) begin\n"
            ver_code += "      $display(\"dual_data = %0p, rm_queue.size = 0\", dual_data);\n"
            ver_code += "      error_cnt += 1;\n"
            ver_code += "    end\n"
            ver_code += "    else begin\n"
            ver_code += "      rm_data = rm_q.pop_front();\n"
            ver_code += "      if(dual_data != rm_data)begin\n"
            ver_code += "        error_cnt += 1;\n"
            ver_code += "        $display(\"dual_data(%0p) != rm_data(%0p) at %t\", dual_data, rm_data, $realtime);\n"
            ver_code += "      end\n"
            ver_code += "      else begin\n"
            ver_code += "        //$display(\"dual_data(%0p) == rm_data(%0p) at %t\", dual_data, rm_data, $realtime);\n"
            ver_code += "      end\n"
            ver_code += "    end\n"
            ver_code += "    if(error_cnt >= ERROR_DEBUG_CNT) begin\n"
            ver_code += "      $display(\"Check Error!!!\");\n"
            ver_code += "      $finish;\n"
            ver_code += "    end\n"
            ver_code += "  end\n"
            ver_code += "endtask: queue_check\n\n"
        
        # 初始化任务
        ver_code += '''initial begin
  fork
    in_queue_gain();
    out_queue_gain();
    rm_queue_gain();
    if(check_en == 1) queue_check();
  join_none
end\n\n'''
        
        ver_code += "//-------------------------------------}}}\n"
        return ver_code
    
    def generate_demo_testbench(self):
        """生成演示用的testbench"""
        return f'''`define DELAY(N, clk) begin \\
	repeat(N) @(posedge clk);\
	#1ps;\
end

module testbench();

//-------------------------------------{{{{common cfg
timeunit 1ns;
timeprecision 1ps;
initial $timeformat(-9,3,"ns",6);

string tc_name;
int tc_seed;

initial begin
    if(!$value$plusargs("tc_name=%s", tc_name)) $error("no tc_name!");
    else $display("tc name = %0s", tc_name);
    if(!$value$plusargs("ntb_random_seed=%0d", tc_seed)) $error("no tc_seed");
    else $display("tc seed = %0d", tc_seed);
end
//-------------------------------------}}}}

//-------------------------------------{{{{clk/rst cfg
logic {self.clk_name}, {self.rst_name};

// 初始化时钟和复位信号
initial begin
    {self.clk_name} = 1'b0;
    {self.rst_name} = 1'b0;
end

// 时钟生成
initial forever #5ns {self.clk_name} = ~{self.clk_name};

// 复位控制
initial begin
    {self.rst_name} = 1'b0;
	`DELAY(30, {self.clk_name});
	{self.rst_name} = 1'b1;
end

// 测试超时控制
initial begin
    #100000ns $finish;
end
//-------------------------------------}}}}

//-------------------------------------{{{{other sig assign
initial begin
    `DELAY(50, {self.clk_name});
end

//-------------------------------------}}}}

endmodule'''
    
    def generate_package(self):
        """生成SystemVerilog包文件"""
        if not self.parser or not hasattr(self.parser, 'valid_signals') or not self.parser.valid_signals:
            return ""
        
        pkg = f"package {self.top_module}_pkg;\n\n"
        pkg += "    parameter ERROR_DEBUG_CNT = 5;\n"
        
        # 添加参数
        for param in self.parser.parameters:
            pkg += f"    parameter {param} = {self.parser.param_dict[param]};\n"
        pkg += "\n"
        
        # 添加验证变量
        pkg += "    int error_cnt = 0;\n"
        pkg += "    bit check_en  = 0;\n\n"
        
        # 为每个valid信号创建结构体
        for valid_name in self.parser.valid_signals:
            valid = self.parser.signal_dict[valid_name]
            if hasattr(valid, 'bus_list') and len(valid.bus_list) != 0:
                pkg += f"    typedef struct{{\n"
                for sig in valid.bus_list:
                    pkg += f"        bit {sig.width} {sig.name};\n"
                pkg += f"    }} {valid.name}_struct;\n"
                
                if valid.port == "output":
                    self.parser.check_valid = valid.name
                    pkg += f"    {valid.name}_struct rm_q[$];\n"
                
                pkg += f"    {valid.name}_struct {valid.name}_bus_q[$];\n\n"
        
        pkg += "endpackage"
        return pkg
    
    def generate_filelist(self, verification=False):
        """生成filelist文件"""
        if not self.parser:
            return "+libext+.v+.sv\n../top/testbench.sv"
        
        verilog_dir = os.path.split(self.parser.file_path)[0]
        
        filelist = "+libext+.v+.sv\n"
        filelist += f"+incdir+{verilog_dir}\n"
        filelist += f"-y {verilog_dir}\n\n"
        
        if verification:
            filelist += f"../ver/{self.top_module}_pkg.sv\n"
        
        filelist += f"{self.parser.file_path}\n"
        filelist += "../top/testbench.sv"
        
        return filelist 