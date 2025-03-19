import re
import os
import argparse
import logging
from typing import List, Dict, Tuple, Set, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VerilogParser:
    """Verilog文件解析器，提取时钟和跨时钟域信号"""
    
    def __init__(self, verilog_content: str):
        self.content = self._preprocess_content(verilog_content)
        self.module_name = self._extract_module_name()
        self.input_signals = self._extract_input_signals()
        self.output_signals = self._extract_output_signals()
        self.reg_signals = self._extract_reg_signals()
        self.wire_signals = self._extract_wire_signals()
        self.clocks = self._identify_clock_signals()
        
    def _preprocess_content(self, content: str) -> str:
        """预处理Verilog内容，移除注释"""
        # 移除单行注释
        content = re.sub(r'//.*', '', content)
        # 移除多行注释
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content
    
    def _extract_module_name(self) -> str:
        """提取模块名称"""
        match = re.search(r'module\s+(\w+)', self.content)
        if match:
            return match.group(1)
        return "unknown_module"
    
    def _extract_input_signals(self) -> List[str]:
        """提取所有输入信号"""
        input_signals = []
        # 匹配输入声明，支持多种格式
        input_decls = re.findall(r'\binput\s+(?:reg|wire)?\s*(?:\[.*?\])?\s*([^;]+)', self.content, re.IGNORECASE)
        for decl in input_decls:
            signals = re.split(r',\s*', decl.strip())
            for sig in signals:
                # 处理可能的位宽声明
                clean_sig = sig.split()[-1] if ' ' in sig else sig
                # 移除任何剩余的位宽信息
                clean_sig = re.sub(r'\[.*?\]', '', clean_sig).strip()
                # 检查信号名是否有效
                if re.match(r'^[a-zA-Z0-9_]+$', clean_sig):
                    input_signals.append(clean_sig)
                else:
                    logger.warning(f"跳过无效输入信号名: {clean_sig}")
        return sorted(list(set(input_signals)))
    
    def _extract_output_signals(self) -> List[str]:
        """提取所有输出信号"""
        output_signals = []
        output_decls = re.findall(r'\boutput\s+(?:reg|wire)?\s*(?:\[.*?\])?\s*([^;]+)', self.content, re.IGNORECASE)
        for decl in output_decls:
            signals = re.split(r',\s*', decl.strip())
            for sig in signals:
                clean_sig = sig.split()[-1] if ' ' in sig else sig
                clean_sig = re.sub(r'\[.*?\]', '', clean_sig).strip()
                output_signals.append(clean_sig)
        return sorted(list(set(output_signals)))
    
    def _extract_reg_signals(self) -> List[str]:
        """提取所有reg类型信号"""
        reg_signals = []
        reg_decls = re.findall(r'\breg\s+(?:\[.*?\])?\s*([^;]+)', self.content, re.IGNORECASE)
        for decl in reg_decls:
            signals = re.split(r',\s*', decl.strip())
            for sig in signals:
                clean_sig = sig.split()[-1] if ' ' in sig else sig
                clean_sig = re.sub(r'\[.*?\]', '', clean_sig).strip()
                reg_signals.append(clean_sig)
        return sorted(list(set(reg_signals)))
    
    def _extract_wire_signals(self) -> List[str]:
        """提取所有wire类型信号"""
        wire_signals = []
        wire_decls = re.findall(r'\bwire\s+(?:\[.*?\])?\s*([^;]+)', self.content, re.IGNORECASE)
        for decl in wire_decls:
            signals = re.split(r',\s*', decl.strip())
            for sig in signals:
                clean_sig = sig.split()[-1] if ' ' in sig else sig
                clean_sig = re.sub(r'\[.*?\]', '', clean_sig).strip()
                wire_signals.append(clean_sig)
        return sorted(list(set(wire_signals)))
    
    def _identify_clock_signals(self) -> List[str]:
        """识别时钟信号"""
        clocks = []
        # 扩展时钟识别模式
        clock_patterns = [
            r'clk\w*', r'clock\w*',  # 基本时钟名称
            r'\w*_clk\w*', r'\w*_clock\w*',  # 前缀_clk
            r'\w*clk_\w*', r'\w*clock_\w*',  # clk_后缀
        ]
        
        # 合并所有模式为一个正则表达式
        combined_pattern = '|'.join(f'({pattern})' for pattern in clock_patterns)
        clock_regex = re.compile(combined_pattern, re.IGNORECASE)
        
        for sig in self.input_signals:
            if clock_regex.fullmatch(sig):
                clocks.append(sig)
        
        return sorted(list(set(clocks)))
    
    def detect_cdc_signals(self) -> Dict[str, List[str]]:
        """检测可能的跨时钟域信号"""
        if len(self.clocks) <= 1:
            return {}
            
        # 提取always块和时钟敏感列表
        always_blocks = re.findall(r'always\s*@\s*\((.*?)\)(.*?)(?=always|endmodule|$)', 
                                  self.content, re.DOTALL)
        
        # 映射时钟到其控制的信号
        clock_to_signals = {clock: [] for clock in self.clocks}
        
        for sensitivity, block_content in always_blocks:
            # 确定这个always块使用的时钟
            block_clock = None
            for clock in self.clocks:
                if re.search(rf'\b{re.escape(clock)}\b', sensitivity):
                    block_clock = clock
                    break
            
            if block_clock:
                # 提取这个always块中赋值的信号
                assignments = re.findall(r'(\w+)\s*<=', block_content)
                for signal in assignments:
                    if signal in self.reg_signals and signal not in clock_to_signals[block_clock]:
                        clock_to_signals[block_clock].append(signal)
        
        # 检测跨时钟域信号
        cdc_signals = {}
        for clock1 in self.clocks:
            for clock2 in self.clocks:
                if clock1 != clock2:
                    # 检查clock1域的信号是否在clock2域中使用
                    for signal in clock_to_signals[clock1]:
                        # 简单检查：如果信号在另一个时钟域的always块中被读取
                        for _, block_content in always_blocks:
                            if re.search(rf'\b{re.escape(clock2)}\b', block_content) and \
                               re.search(rf'\b{re.escape(signal)}\b', block_content):
                                cdc_key = f"{clock1}->{clock2}"
                                if cdc_key not in cdc_signals:
                                    cdc_signals[cdc_key] = []
                                if signal not in cdc_signals[cdc_key]:
                                    cdc_signals[cdc_key].append(signal)
        
        return cdc_signals

# 修改SGDCGenerator类的初始化方法
class SGDCGenerator:
    """SGDC约束文件生成器"""
    
    def __init__(self, clocks: List[str], module_name: str, cdc_signals: Dict[str, List[str]],
                 input_signals: List[str] = None, output_signals: List[str] = None):
        self.clocks = clocks
        self.module_name = module_name
        self.cdc_signals = cdc_signals
        self.input_signals = input_signals or []
        self.output_signals = output_signals or []
        self.clock_periods = {}
        self.clock_uncertainties = {}
    
    def set_clock_periods(self, interactive: bool = True):
        """设置时钟周期，可以交互式或使用默认值"""
        if interactive:
            print("\n设置时钟周期:")
            for clock in self.clocks:
                while True:
                    try:
                        period = input(f"请输入时钟 {clock} 的周期(ns)，或按Enter使用默认值(10ns): ")
                        if period == "":
                            self.clock_periods[clock] = 10.0
                            # 默认时钟不确定性为周期的5%
                            self.clock_uncertainties[clock] = 0.5
                            break
                        period_float = float(period)
                        if period_float <= 0:
                            print("周期必须为正数，请重新输入")
                            continue
                        self.clock_periods[clock] = period_float
                        # 默认时钟不确定性为周期的5%
                        self.clock_uncertainties[clock] = round(period_float * 0.05, 2)
                        break
                    except ValueError:
                        print("无效输入，请输入一个数字")
                
                # 可选设置时钟不确定性
                while True:
                    try:
                        uncertainty = input(f"请输入时钟 {clock} 的不确定性(ns)，或按Enter使用默认值({self.clock_uncertainties[clock]}ns): ")
                        if uncertainty == "":
                            break
                        uncertainty_float = float(uncertainty)
                        if uncertainty_float < 0:
                            print("不确定性必须为非负数，请重新输入")
                            continue
                        self.clock_uncertainties[clock] = uncertainty_float
                        break
                    except ValueError:
                        print("无效输入，请输入一个数字")
        else:
            # 使用默认值
            for clock in self.clocks:
                self.clock_periods[clock] = 10.0
                self.clock_uncertainties[clock] = 0.5
    
    def _categorize_signals(self):
        """根据信号名称推断信号所属的时钟域"""
        signal_to_clock = {}
        
        # 根据命名规则推断信号所属的时钟域
        for signal in self.input_signals + self.output_signals:
            # 跳过时钟信号本身
            if signal in self.clocks:
                continue
                
            assigned_clock = None
            
            # 尝试通过信号名称匹配时钟域
            for clock in self.clocks:
                # 提取时钟名称的特征部分（去除clk, clock等通用词）
                clock_feature = re.sub(r'_?clk|_?clock', '', clock, flags=re.IGNORECASE).strip('_')
                if clock_feature and clock_feature in signal:
                    assigned_clock = clock
                    break
            
            # 如果没有匹配到，则分配给第一个时钟
            if not assigned_clock and self.clocks:
                assigned_clock = self.clocks[0]
                
            signal_to_clock[signal] = assigned_clock
        
        return signal_to_clock
    
    def _generate_delay_constraints(self):
        """生成输入输出延迟约束"""
        signal_to_clock = self._categorize_signals()
        
        # 为每个时钟域设置默认延迟值
        default_delays = {}
        for clock in self.clocks:
            period = self.clock_periods.get(clock, 10.0)
            # 输入延迟默认为时钟周期的30%
            default_delays[clock] = {
                'input_max': round(period * 0.3, 2),
                'input_min': round(period * 0.1, 2),
                'output_max': round(period * 0.3, 2),
                'output_min': round(period * 0.1, 2)
            }
        
        # 生成输入延迟约束
        input_constraints = []
        for signal in self.input_signals:
            # 跳过时钟信号本身
            if signal in self.clocks:
                continue
                
            # 检查信号名是否有效，避免特殊字符导致语法错误
            if not re.match(r'^[a-zA-Z0-9_]+$', signal):
                logger.warning(f"跳过无效信号名: {signal}")
                continue
                
            clock = signal_to_clock.get(signal)
            if clock:
                delays = default_delays.get(clock, default_delays[self.clocks[0]] if self.clocks else None)
                if delays:
                    input_constraints.append(f"set_input_delay -clock {clock} -max {delays['input_max']} [get_ports {signal}]")
                    input_constraints.append(f"set_input_delay -clock {clock} -min {delays['input_min']} [get_ports {signal}]")
        
        # 生成输出延迟约束
        output_constraints = []
        for signal in self.output_signals:
            # 检查信号名是否有效
            if not re.match(r'^[a-zA-Z0-9_]+$', signal):
                logger.warning(f"跳过无效信号名: {signal}")
                continue
                
            clock = signal_to_clock.get(signal)
            if clock:
                delays = default_delays.get(clock, default_delays[self.clocks[0]] if self.clocks else None)
                if delays:
                    output_constraints.append(f"set_output_delay -clock {clock} -max {delays['output_max']} [get_ports {signal}]")
                    output_constraints.append(f"set_output_delay -clock {clock} -min {delays['output_min']} [get_ports {signal}]")
        
        return input_constraints, output_constraints
    
    def _generate_multicycle_path_templates(self):
        """生成多周期路径模板"""
        templates = []
        
        if len(self.clocks) > 1:
            # 为不同时钟域之间的路径生成多周期路径模板
            for i, clock_a in enumerate(self.clocks):
                for clock_b in self.clocks[i+1:]:
                    period_a = self.clock_periods.get(clock_a, 10.0)
                    period_b = self.clock_periods.get(clock_b, 10.0)
                    
                    # 如果时钟周期差异大，可能需要多周期路径
                    if period_a > 1.5 * period_b:
                        ratio = int(period_a / period_b)
                        templates.append(f"# {clock_a}到{clock_b}的多周期路径 (周期比约为 {ratio}:1)")
                        templates.append(f"# set_multicycle_path -setup {ratio} -from [get_clocks {clock_a}] -to [get_clocks {clock_b}]")
                        templates.append(f"# set_multicycle_path -hold {ratio-1} -from [get_clocks {clock_a}] -to [get_clocks {clock_b}]")
                    elif period_b > 1.5 * period_a:
                        ratio = int(period_b / period_a)
                        templates.append(f"# {clock_b}到{clock_a}的多周期路径 (周期比约为 {ratio}:1)")
                        templates.append(f"# set_multicycle_path -setup {ratio} -from [get_clocks {clock_b}] -to [get_clocks {clock_a}]")
                        templates.append(f"# set_multicycle_path -hold {ratio-1} -from [get_clocks {clock_b}] -to [get_clocks {clock_a}]")
        
        # 添加通用的多周期路径模板
        if not templates:
            templates.append("# 对于需要多个时钟周期完成的路径，可以设置多周期路径约束")
            templates.append("# set_multicycle_path -setup <num_cycles> -from [get_pins <source_pin>] -to [get_pins <destination_pin>]")
            templates.append("# set_multicycle_path -hold <num_cycles-1> -from [get_pins <source_pin>] -to [get_pins <destination_pin>]")
            templates.append("# 例如: 需要2个时钟周期的路径")
            templates.append("# set_multicycle_path -setup 2 -from [get_pins reg_slow/Q] -to [get_pins reg_fast/D]")
            templates.append("# set_multicycle_path -hold 1 -from [get_pins reg_slow/Q] -to [get_pins reg_fast/D]")
        
        return templates
    
    def generate_sgdc(self) -> str:
        """生成SGDC约束文件内容"""
        template = []
        
        # 文件头说明
        template.append("//=============================================================================")
        template.append(f"// Auto-generated SGDC file for CDC analysis of module: {self.module_name}")
        template.append("// Generated by auto_sgdc_gen.py")
        template.append("// 注意: 请根据实际设计需求验证和修改以下约束")
        template.append("//=============================================================================\n")
        
        # 时钟定义
        template.append("//-----------------------------------------------------------------------------")
        template.append("// 时钟定义 (Clock Definitions)")
        template.append("//-----------------------------------------------------------------------------")
        for clock in self.clocks:
            period = self.clock_periods.get(clock, 10.0)
            template.append(f"create_clock -name {clock} -period {period} [get_ports {clock}]")
        
        # 时钟不确定性
        template.append("\n//-----------------------------------------------------------------------------")
        template.append("// 时钟不确定性 (Clock Uncertainty)")
        template.append("//-----------------------------------------------------------------------------")
        for clock in self.clocks:
            uncertainty = self.clock_uncertainties.get(clock, 0.5)
            template.append(f"set_clock_uncertainty {uncertainty} [get_clocks {clock}]")
        
        # 时钟组约束
        if len(self.clocks) > 1:
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// 时钟组约束 (Clock Group Constraints)")
            template.append("//-----------------------------------------------------------------------------")
            groups = " -group ".join([f"{{{clock}}}" for clock in self.clocks])
            template.append(f"set_clock_groups -asynchronous -group {groups}")
        
        # CDC信号约束
        if self.cdc_signals:
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// CDC信号约束 (CDC Signal Constraints) - 自动检测，请验证")
            template.append("//-----------------------------------------------------------------------------")
            for cdc_path, signals in self.cdc_signals.items():
                src_clock, dst_clock = cdc_path.split("->")
                template.append(f"# CDC从 {src_clock} 到 {dst_clock}:")
                for signal in signals:
                    template.append(f"set_cdc_signal -src_clock {src_clock} -dst_clock {dst_clock} [get_nets {signal}]")
                template.append(f"set_cdc_property -type async -from {src_clock} -to {dst_clock}")
                template.append("# 注意: 请确认上述CDC信号是否需要同步器")
        else:
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// CDC信号约束 (CDC Signal Constraints) - 请手动添加")
            template.append("//-----------------------------------------------------------------------------")
            if len(self.clocks) > 1:
                for i, clock_a in enumerate(self.clocks):
                    for clock_b in self.clocks[i+1:]:
                        template.append(f"# CDC从 {clock_a} 到 {clock_b}:")
                        template.append(f"# set_cdc_signal -src_clock {clock_a} -dst_clock {clock_b} [get_nets <net_name>]")
                        template.append(f"# set_cdc_property -type async -from {clock_a} -to {clock_b}")
                        template.append("")
                        template.append(f"# CDC从 {clock_b} 到 {clock_a}:")
                        template.append(f"# set_cdc_signal -src_clock {clock_b} -dst_clock {clock_a} [get_nets <net_name>]")
                        template.append(f"# set_cdc_property -type async -from {clock_b} -to {clock_a}")
            else:
                template.append("# set_cdc_signal -src_clock <src_clock> -dst_clock <dst_clock> [get_nets <net_name>]")
                template.append("# set_cdc_property -type async -from <src_clock> -to <dst_clock>")
        
        # 虚假路径排除
        template.append("\n//-----------------------------------------------------------------------------")
        template.append("// 虚假路径排除 (False Path Exceptions)")
        template.append("//-----------------------------------------------------------------------------")
        if len(self.clocks) > 1:
            for i, clock_a in enumerate(self.clocks):
                for clock_b in self.clocks[i+1:]:
                    template.append(f"# 如果{clock_a}和{clock_b}之间的路径不需要时序分析，可以设置为false path")
                    template.append(f"set_false_path -from [get_clocks {clock_a}] -to [get_clocks {clock_b}]")
                    template.append(f"set_false_path -from [get_clocks {clock_b}] -to [get_clocks {clock_a}]")
        else:
            template.append("# set_false_path -from [get_clocks <clock_a>] -to [get_clocks <clock_b>]")
        
        # 多周期路径
        template.append("\n//-----------------------------------------------------------------------------")
        template.append("// 多周期路径 (Multicycle Path)")
        template.append("//-----------------------------------------------------------------------------")
        multicycle_templates = self._generate_multicycle_path_templates()
        template.extend(multicycle_templates)
        
        # 在generate_sgdc方法中修复输出延迟部分的条件判断
        # 找到输入输出延迟部分
        
        # 输入输出延迟
        input_constraints, output_constraints = self._generate_delay_constraints()
        
        if input_constraints:
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// 输入延迟 (Input Delays)")
            template.append("//-----------------------------------------------------------------------------")
            template.append("# 以下是自动生成的输入延迟约束，请根据实际情况修改")
            template.extend(input_constraints)
        else:
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// 输入延迟 (Input Delays)")
            template.append("//-----------------------------------------------------------------------------")
            template.append("# 未检测到输入信号或无法确定时钟域")
            if self.clocks:
                default_clock = self.clocks[0]
                template.append(f"# set_input_delay -clock {default_clock} -max <delay_ns> [get_ports <port_name>]")
                template.append(f"# set_input_delay -clock {default_clock} -min <delay_ns> [get_ports <port_name>]")
        
            template.append("\n//-----------------------------------------------------------------------------")
            template.append("// 输出延迟 (Output Delays)")
            template.append("//-----------------------------------------------------------------------------")
            if output_constraints:
                template.append("# 以下是自动生成的输出延迟约束，请根据实际情况修改")
                template.extend(output_constraints)
            else:
                template.append("# 未检测到输出信号或无法确定时钟域")
                if self.clocks:
                    default_clock = self.clocks[0]
                    template.append(f"# set_output_delay -clock {default_clock} -max <delay_ns> [get_ports <port_name>]")
                    template.append(f"# set_output_delay -clock {default_clock} -min <delay_ns> [get_ports <port_name>]")
        
        return "\n".join(template)

# 修改main函数，传递输入输出信号
def main():
    parser = argparse.ArgumentParser(description="生成SGDC模板从Verilog模块")
    parser.add_argument("verilog_file", help="Verilog源文件路径")
    parser.add_argument("-o", "--output", help="输出SGDC文件名 (默认为<module_name>.sgdc)")
    parser.add_argument("-n", "--non-interactive", action="store_true", help="非交互模式，使用默认时钟周期")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志")
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # 读取Verilog文件
        logger.info(f"正在读取Verilog文件: {args.verilog_file}")
        with open(args.verilog_file, 'r') as f:
            content = f.read()
        
        # 解析Verilog文件
        logger.info("正在解析Verilog文件...")
        parser = VerilogParser(content)
        
        # 提取模块名和时钟信号
        module_name = parser.module_name
        clocks = parser.clocks
        input_signals = parser.input_signals
        output_signals = parser.output_signals
        
        if not clocks:
            logger.warning("未检测到时钟信号！请检查信号命名或手动添加时钟约束。")
        else:
            logger.info(f"检测到 {len(clocks)} 个时钟信号: {', '.join(clocks)}")
        
        logger.info(f"检测到 {len(input_signals)} 个输入信号")
        logger.info(f"检测到 {len(output_signals)} 个输出信号")
        
        # 检测跨时钟域信号
        logger.info("正在检测跨时钟域信号...")
        cdc_signals = parser.detect_cdc_signals()
        
        if cdc_signals:
            logger.info(f"检测到 {sum(len(signals) for signals in cdc_signals.values())} 个可能的跨时钟域信号")
            for path, signals in cdc_signals.items():
                logger.debug(f"  {path}: {', '.join(signals)}")
        else:
            logger.info("未检测到跨时钟域信号，或只有一个时钟域")
        
        # 生成SGDC文件
        logger.info("正在生成SGDC约束文件...")
        sgdc_gen = SGDCGenerator(clocks, module_name, cdc_signals, input_signals, output_signals)
        
        # 设置时钟周期
        sgdc_gen.set_clock_periods(not args.non_interactive)
        
        # 生成SGDC内容
        sgdc_content = sgdc_gen.generate_sgdc()
        
        # 确定输出文件名
        if args.output:
            output_file = args.output
        else:
            output_file = f"{module_name}.sgdc"
        
        # 写入文件
        # 修改文件写入部分，添加编码指定
        # 在main函数中找到写入文件的部分
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sgdc_content)
        
        logger.info(f"SGDC约束文件已生成: {output_file}")
        
    except FileNotFoundError:
        logger.error(f"找不到文件: {args.verilog_file}")
    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())

if __name__ == "__main__":
    main()