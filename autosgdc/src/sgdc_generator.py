#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SGDC生成器模块 - 负责生成SGDC约束文件内容

此模块提供生成SGDC（Synopsys Guidance Design Constraints）文件的功能，包括:
- 创建时钟定义
- 定义异步时钟组
- 生成CDC信号约束
- 配置输入输出延迟
- 生成多周期路径和虚假路径
"""

import os
import re
import logging
import datetime
from typing import List, Dict, Tuple, Set, Optional, Union, Any

from utils import setup_logger
from verilog_parser import VerilogModule

# 设置日志
logger = setup_logger('sgdc_generator')

class ClockConfig:
    """时钟配置类，存储时钟相关信息"""
    
    def __init__(self, name: str, period: float = 10.0):
        """
        初始化时钟配置
        
        参数:
            name: 时钟名称
            period: 时钟周期(ns)
        """
        self.name = name
        self.period = period
        self.uncertainty = round(period * 0.05, 2)  # 默认不确定性为周期的5%
        self.waveform = (0, round(period / 2, 2))   # 默认占空比50%
        self.generated = False                      # 是否为生成的时钟
        self.source = ""                            # 生成时钟的源时钟
        self.divide_by = 1                          # 分频系数
        self.multiply_by = 1                        # 倍频系数
        self.phase = 0.0                            # 相位偏移(度)

class SGDCGenerator:
    """SGDC约束文件生成器"""
    
    def __init__(self, top_module: VerilogModule, clock_signals: List[str], 
                cdc_signals: Dict[str, List[str]], clock_config: Dict[str, Any] = None):
        """
        初始化SGDC生成器
        
        参数:
            top_module: 顶层模块对象
            clock_signals: 时钟信号列表
            cdc_signals: 跨时钟域信号字典，键为"src_clk->dst_clk"，值为信号列表
            clock_config: 时钟配置字典，键为时钟名，值为配置信息
        """
        self.top_module = top_module
        self.clock_signals = clock_signals
        self.cdc_signals = cdc_signals
        self.clock_configs = {}
        
        # 初始化时钟配置
        for clock in clock_signals:
            # 如果提供了配置，使用提供的配置
            if clock_config and clock in clock_config:
                cfg = clock_config[clock]
                clock_cfg = ClockConfig(clock, cfg.get('period', 10.0))
                clock_cfg.uncertainty = cfg.get('uncertainty', clock_cfg.uncertainty)
                clock_cfg.waveform = cfg.get('waveform', clock_cfg.waveform)
                clock_cfg.generated = cfg.get('generated', False)
                clock_cfg.source = cfg.get('source', "")
                clock_cfg.divide_by = cfg.get('divide_by', 1)
                clock_cfg.multiply_by = cfg.get('multiply_by', 1)
                clock_cfg.phase = cfg.get('phase', 0.0)
            else:
                # 否则使用默认配置
                clock_cfg = ClockConfig(clock)
            
            self.clock_configs[clock] = clock_cfg
    
    def configure_clocks_interactive(self) -> None:
        """交互式配置时钟属性"""
        print("\n时钟配置:")
        print("-" * 40)
        
        for clock in self.clock_signals:
            config = self.clock_configs[clock]
            
            # 配置时钟周期
            while True:
                try:
                    period_input = input(f"时钟 {clock} 的周期(ns) [默认: {config.period}]: ")
                    if not period_input:
                        break  # 使用默认值
                        
                    period = float(period_input)
                    if period <= 0:
                        print("错误: 周期必须为正数")
                        continue
                        
                    config.period = period
                    # 更新默认的不确定性和波形
                    config.uncertainty = round(period * 0.05, 2)
                    config.waveform = (0, round(period / 2, 2))
                    break
                    
                except ValueError:
                    print("错误: 请输入有效的数字")
            
            # 配置时钟不确定性
            while True:
                try:
                    uncertainty_input = input(f"时钟 {clock} 的不确定性(ns) [默认: {config.uncertainty}]: ")
                    if not uncertainty_input:
                        break  # 使用默认值
                        
                    uncertainty = float(uncertainty_input)
                    if uncertainty < 0:
                        print("错误: 不确定性必须为非负数")
                        continue
                        
                    config.uncertainty = uncertainty
                    break
                    
                except ValueError:
                    print("错误: 请输入有效的数字")
            
            # 询问是否是生成的时钟
            is_generated = input(f"时钟 {clock} 是生成的时钟吗? (y/n) [默认: {'y' if config.generated else 'n'}]: ")
            if is_generated.lower() == 'y':
                config.generated = True
                
                # 如果是生成的时钟，询问源时钟
                if len(self.clock_signals) > 1:
                    print("可用的源时钟:")
                    for i, src_clock in enumerate(self.clock_signals):
                        if src_clock != clock:
                            print(f"  {i+1}. {src_clock}")
                    
                    while True:
                        try:
                            source_input = input("请选择源时钟 (输入编号或时钟名): ")
                            if not source_input:
                                continue
                                
                            # 检查是否是编号
                            if source_input.isdigit():
                                idx = int(source_input) - 1
                                if 0 <= idx < len(self.clock_signals) and self.clock_signals[idx] != clock:
                                    config.source = self.clock_signals[idx]
                                    break
                            # 检查是否是时钟名
                            elif source_input in self.clock_signals and source_input != clock:
                                config.source = source_input
                                break
                                
                            print("错误: 请输入有效的源时钟")
                            
                        except ValueError:
                            print("错误: 请输入有效的编号")
                
                # 询问分频/倍频系数
                while True:
                    try:
                        divide_input = input(f"分频系数 [默认: {config.divide_by}]: ")
                        if not divide_input:
                            break  # 使用默认值
                            
                        divide_by = int(divide_input)
                        if divide_by <= 0:
                            print("错误: 分频系数必须为正整数")
                            continue
                            
                        config.divide_by = divide_by
                        break
                        
                    except ValueError:
                        print("错误: 请输入有效的整数")
                
                while True:
                    try:
                        multiply_input = input(f"倍频系数 [默认: {config.multiply_by}]: ")
                        if not multiply_input:
                            break  # 使用默认值
                            
                        multiply_by = int(multiply_input)
                        if multiply_by <= 0:
                            print("错误: 倍频系数必须为正整数")
                            continue
                            
                        config.multiply_by = multiply_by
                        break
                        
                    except ValueError:
                        print("错误: 请输入有效的整数")
                
                # 询问相位偏移
                while True:
                    try:
                        phase_input = input(f"相位偏移(度) [默认: {config.phase}]: ")
                        if not phase_input:
                            break  # 使用默认值
                            
                        phase = float(phase_input)
                        if not 0 <= phase < 360:
                            print("错误: 相位必须在0到360度之间")
                            continue
                            
                        config.phase = phase
                        break
                        
                    except ValueError:
                        print("错误: 请输入有效的数字")
            
            # 分隔线
            print("-" * 40)
    
    def configure_clocks_default(self) -> None:
        """使用默认值配置时钟属性"""
        # 对于每个时钟，使用默认配置
        for clock in self.clock_signals:
            config = self.clock_configs[clock]
            # 可以在这里基于频率名称进行一些智能猜测
            
            # 例如: 基于时钟名称推断频率
            if 'mhz' in clock.lower() or 'hz' in clock.lower():
                # 尝试从名称中提取频率
                freq_match = re.search(r'(\d+)(?:m?hz)', clock.lower())
                if freq_match:
                    freq = int(freq_match.group(1))
                    if 'mhz' in clock.lower():
                        # 将MHz转换为ns周期
                        config.period = round(1000 / freq, 2)
                    elif 'hz' in clock.lower():
                        # 将Hz转换为ns周期
                        config.period = round(1e9 / freq, 2)
                    
                    # 更新默认的不确定性和波形
                    config.uncertainty = round(config.period * 0.05, 2)
                    config.waveform = (0, round(config.period / 2, 2))
            
            # 智能判断是否为生成的时钟
            if clock.lower().endswith('_div') or '_div' in clock.lower():
                config.generated = True
                # 尝试推断源时钟和分频系数
                div_match = re.search(r'(\w+)_div(\d*)', clock.lower())
                if div_match:
                    base_clock = div_match.group(1)
                    div_factor = div_match.group(2)
                    
                    # 查找匹配的源时钟
                    for src_clock in self.clock_signals:
                        if src_clock.lower() == base_clock.lower() or src_clock.lower().startswith(base_clock.lower()):
                            config.source = src_clock
                            break
                    
                    # 设置分频系数
                    if div_factor:
                        try:
                            config.divide_by = int(div_factor)
                        except ValueError:
                            pass  # 忽略非数字的后缀
    
    def generate_sgdc(self) -> str:
        """
        生成SGDC约束文件内容
        
        返回:
            SGDC文件内容字符串
        """
        template = []
        
        # 文件头
        template.append("//==============================================================================")
        template.append(f"// Auto-generated SGDC file for Spyglass CDC analysis")
        template.append(f"// Module: {self.top_module.name}")
        template.append(f"// Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        template.append(f"// Generator: AutoSGDC v2.0")
        template.append("//==============================================================================\n")
        
        # 时钟定义
        template.append("//------------------------------------------------------------------------------")
        template.append("// 时钟定义 (Clock Definitions)")
        template.append("//------------------------------------------------------------------------------")
        
        for clock_name, config in self.clock_configs.items():
            if not config.generated:
                # 主时钟定义
                template.append(f"create_clock -name {clock_name} -period {config.period} -waveform {{{config.waveform[0]} {config.waveform[1]}}} [get_ports {clock_name}]")
            else:
                # 生成的时钟
                if config.source:
                    # 如果指定了源时钟
                    source_clock = self.clock_configs.get(config.source)
                    if source_clock:
                        if config.divide_by != 1 or config.multiply_by != 1:
                            # 使用分频/倍频系数
                            period = source_clock.period * config.divide_by / config.multiply_by
                            template.append(f"# 从 {config.source} 生成，分频系数 = {config.divide_by}，倍频系数 = {config.multiply_by}")
                            template.append(f"create_generated_clock -name {clock_name} -source [get_ports {config.source}] -divide_by {config.divide_by} -multiply_by {config.multiply_by} -phase {config.phase} [get_pins <clock_generator_pin>]")
                        else:
                            # 直接使用周期
                            template.append(f"# 从 {config.source} 生成")
                            template.append(f"create_generated_clock -name {clock_name} -source [get_ports {config.source}] -phase {config.phase} [get_pins <clock_generator_pin>]")
                    else:
                        # 源时钟不存在，使用默认形式
                        template.append(f"# 生成的时钟，源时钟未知")
                        template.append(f"create_generated_clock -name {clock_name} -period {config.period} [get_pins <clock_generator_pin>]")
                else:
                    # 没有指定源时钟，使用默认形式
                    template.append(f"# 生成的时钟，无源时钟指定")
                    template.append(f"create_generated_clock -name {clock_name} -period {config.period} [get_pins <clock_generator_pin>]")
        
        # 时钟不确定性
        template.append("\n//------------------------------------------------------------------------------")
        template.append("// 时钟不确定性 (Clock Uncertainty)")
        template.append("//------------------------------------------------------------------------------")
        for clock_name, config in self.clock_configs.items():
            template.append(f"set_clock_uncertainty {config.uncertainty} [get_clocks {clock_name}]")
        
        # 异步时钟组
        if len(self.clock_signals) > 1:
            template.append("\n//------------------------------------------------------------------------------")
            template.append("// 异步时钟组 (Asynchronous Clock Groups)")
            template.append("//------------------------------------------------------------------------------")
            
            # 所有时钟都是异步的情况
            groups = " -group ".join([f"{{{clock}}}" for clock in self.clock_signals])
            template.append(f"set_clock_groups -asynchronous -group {groups}")
            
            # 注释说明
            template.append("\n# 注意: 如果某些时钟是同步的，请移除它们并创建单独的时钟组")
            template.append("# 例如: 如果clk1和clk2是同步的，但与clk3异步:")
            template.append("# set_clock_groups -asynchronous -group {clk1 clk2} -group {clk3}")
        
        # 时钟域交叉约束
        if any(signals for signals in self.cdc_signals.values()):
            template.append("\n//------------------------------------------------------------------------------")
            template.append("// 跨时钟域信号约束 (Clock Domain Crossing Constraints)")
            template.append("//------------------------------------------------------------------------------")
            
            for cdc_path, signals in self.cdc_signals.items():
                if not signals:
                    continue  # 跳过空路径
                    
                src_clock, dst_clock = cdc_path.split("->")
                template.append(f"\n# CDC路径: {src_clock} -> {dst_clock}")
                
                for signal in signals:
                    template.append(f"set_cdc_signal -src_clock {src_clock} -dst_clock {dst_clock} [get_nets {signal}]")
                
                template.append(f"set_cdc_property -type async -from {src_clock} -to {dst_clock}")
                template.append("# 提示: 确认上述信号是否需要同步器")
        else:
            template.append("\n//------------------------------------------------------------------------------")
            template.append("// 跨时钟域信号约束 (Clock Domain Crossing Constraints) - 未检测到CDC")
            template.append("//------------------------------------------------------------------------------")
            template.append("# 未检测到跨时钟域信号，或CDC信号已有同步器")
            
            if len(self.clock_signals) > 1:
                template.append("# 如果您知道存在CDC路径，请手动添加约束:")
                for i, src_clock in enumerate(self.clock_signals):
                    for dst_clock in self.clock_signals[i+1:]:
                        template.append(f"# set_cdc_signal -src_clock {src_clock} -dst_clock {dst_clock} [get_nets <signal_name>]")
                        template.append(f"# set_cdc_property -type async -from {src_clock} -to {dst_clock}")
        
        # 虚假路径排除
        template.append("\n//------------------------------------------------------------------------------")
        template.append("// 虚假路径排除 (False Path Exclusions)")
        template.append("//------------------------------------------------------------------------------")
        if len(self.clock_signals) > 1:
            template.append("# 如果某些跨时钟域路径不需要进行时序分析，可以设置为虚假路径")
            for i, src_clock in enumerate(self.clock_signals):
                for dst_clock in self.clock_signals[i+1:]:
                    template.append(f"# set_false_path -from [get_clocks {src_clock}] -to [get_clocks {dst_clock}]")
                    template.append(f"# set_false_path -from [get_clocks {dst_clock}] -to [get_clocks {src_clock}]")
        else:
            template.append("# 单时钟设计，无需设置虚假路径")
        
        # 多周期路径
        template.append("\n//------------------------------------------------------------------------------")
        template.append("// 多周期路径 (Multicycle Paths)")
        template.append("//------------------------------------------------------------------------------")
        if len(self.clock_signals) > 1:
            # 尝试基于时钟周期比例推荐多周期路径
            for i, clock_a_name in enumerate(self.clock_signals):
                for clock_b_name in self.clock_signals[i+1:]:
                    clock_a = self.clock_configs[clock_a_name]
                    clock_b = self.clock_configs[clock_b_name]
                    
                    # 如果时钟周期差异大，可能需要多周期路径
                    ratio_a_to_b = clock_a.period / clock_b.period
                    ratio_b_to_a = clock_b.period / clock_a.period
                    
                    if ratio_a_to_b >= 1.5:
                        mc_value = max(2, int(ratio_a_to_b))
                        template.append(f"# {clock_a_name}到{clock_b_name}的多周期路径 (周期比约为 {ratio_a_to_b:.1f}:1)")
                        template.append(f"# set_multicycle_path -setup {mc_value} -from [get_clocks {clock_a_name}] -to [get_clocks {clock_b_name}]")
                        template.append(f"# set_multicycle_path -hold {mc_value-1} -from [get_clocks {clock_a_name}] -to [get_clocks {clock_b_name}]")
                    
                    if ratio_b_to_a >= 1.5:
                        mc_value = max(2, int(ratio_b_to_a))
                        template.append(f"# {clock_b_name}到{clock_a_name}的多周期路径 (周期比约为 {ratio_b_to_a:.1f}:1)")
                        template.append(f"# set_multicycle_path -setup {mc_value} -from [get_clocks {clock_b_name}] -to [get_clocks {clock_a_name}]")
                        template.append(f"# set_multicycle_path -hold {mc_value-1} -from [get_clocks {clock_b_name}] -to [get_clocks {clock_a_name}]")
        else:
            template.append("# 单时钟设计，可能仍需要设置多周期路径")
            template.append("# set_multicycle_path -setup <num_cycles> -from [get_pins <source_pin>] -to [get_pins <destination_pin>]")
            template.append("# set_multicycle_path -hold <num_cycles-1> -from [get_pins <source_pin>] -to [get_pins <destination_pin>]")
        
        # 输入输出延迟
        template.append("\n//------------------------------------------------------------------------------")
        template.append("// 输入延迟 (Input Delays)")
        template.append("//------------------------------------------------------------------------------")
        template.append("# 设置相对于时钟的输入延迟")
        if self.clock_signals:
            default_clock = self.clock_signals[0]
            period = self.clock_configs[default_clock].period
            in_delay_max = round(period * 0.3, 2)
            in_delay_min = round(period * 0.1, 2)
            
            template.append(f"# 默认输入延迟: 最大 = {in_delay_max}ns, 最小 = {in_delay_min}ns")
            template.append(f"# set_input_delay -clock {default_clock} -max {in_delay_max} [get_ports <input_port>]")
            template.append(f"# set_input_delay -clock {default_clock} -min {in_delay_min} [get_ports <input_port>]")
            
            # 对每个端口类型提供模板
            template.append("\n# 控制信号输入延迟")
            template.append(f"# set_input_delay -clock {default_clock} -max {in_delay_max} [get_ports {{{self.top_module.name}/control*}}]")
            
            template.append("\n# 数据信号输入延迟")
            template.append(f"# set_input_delay -clock {default_clock} -max {in_delay_max} [get_ports {{{self.top_module.name}/data*}}]")
        
        template.append("\n//------------------------------------------------------------------------------")
        template.append("// 输出延迟 (Output Delays)")
        template.append("//------------------------------------------------------------------------------")
        template.append("# 设置相对于时钟的输出延迟")
        if self.clock_signals:
            default_clock = self.clock_signals[0]
            period = self.clock_configs[default_clock].period
            out_delay_max = round(period * 0.3, 2)
            out_delay_min = round(period * 0.1, 2)
            
            template.append(f"# 默认输出延迟: 最大 = {out_delay_max}ns, 最小 = {out_delay_min}ns")
            template.append(f"# set_output_delay -clock {default_clock} -max {out_delay_max} [get_ports <output_port>]")
            template.append(f"# set_output_delay -clock {default_clock} -min {out_delay_min} [get_ports <output_port>]")
            
            # 对每个端口类型提供模板
            template.append("\n# 控制信号输出延迟")
            template.append(f"# set_output_delay -clock {default_clock} -max {out_delay_max} [get_ports {{{self.top_module.name}/control*}}]")
            
            template.append("\n# 数据信号输出延迟")
            template.append(f"# set_output_delay -clock {default_clock} -max {out_delay_max} [get_ports {{{self.top_module.name}/data*}}]")
        
        # 结束
        template.append("\n//==============================================================================")
        template.append("// 结束 (End of File)")
        template.append("//==============================================================================")
        
        return "\n".join(template)
    
    def generate_report(self) -> str:
        """
        生成配置报告
        
        返回:
            报告字符串
        """
        report = []
        report.append("=" * 80)
        report.append("SGDC配置报告")
        report.append("=" * 80)
        
        # 时钟配置
        report.append("\n时钟配置:")
        report.append("-" * 40)
        
        for clock_name, config in self.clock_configs.items():
            report.append(f"时钟: {clock_name}")
            report.append(f"  周期: {config.period} ns")
            report.append(f"  不确定性: {config.uncertainty} ns")
            report.append(f"  波形: {config.waveform[0]} {config.waveform[1]}")
            
            if config.generated:
                report.append(f"  类型: 生成的时钟")
                if config.source:
                    report.append(f"  源时钟: {config.source}")
                if config.divide_by != 1 or config.multiply_by != 1:
                    report.append(f"  分频系数: {config.divide_by}")
                    report.append(f"  倍频系数: {config.multiply_by}")
                if config.phase != 0:
                    report.append(f"  相位偏移: {config.phase} 度")
            else:
                report.append(f"  类型: 主时钟")
                
            report.append("")
        
        # CDC配置
        report.append("\nCDC约束配置:")
        report.append("-" * 40)
        
        if len(self.clock_signals) <= 1:
            report.append("单时钟设计，无CDC约束")
        else:
            report.append(f"时钟组配置: 全部设置为异步时钟组")
            
            # CDC信号约束
            if any(signals for signals in self.cdc_signals.values()):
                report.append("\nCDC信号约束:")
                for cdc_path, signals in self.cdc_signals.items():
                    if signals:
                        report.append(f"  路径 {cdc_path}: {len(signals)} 个信号")
            else:
                report.append("\n未检测到未同步的CDC信号")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report) 