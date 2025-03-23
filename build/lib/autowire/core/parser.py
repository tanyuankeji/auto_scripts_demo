# parser.py
"""
Verilog解析器模块
负责解析Verilog代码并提取基础信息
"""

import re
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import OrderedDict

from .utils import read_file, remove_comments, extract_parameters, ParseError

# Verilog/SystemVerilog保留关键字集合
VERILOG_KEYWORDS = {
    "module", "endmodule", "input", "output", "inout", "assign", "always", "always_ff",
    "always_comb", "always_latch", "if", "else", "case", "endcase", "begin", "end", 
    "wire", "reg", "logic", "parameter", "localparam", "function", "endfunction", "task",
    "endtask", "for", "while", "repeat", "forever", "default", "posedge", "negedge",
    "or", "and", "not", "xor", "nor", "nand", "xnor", "buf", "signed", "unsigned",
    "generate", "endgenerate"
}

# 常用的模块实例化前缀
INSTANCE_PREFIXES = ["u_", "i_", "inst_", "g_", "gen_", "x_", "m_", "s_", "p_", "c_", 
                     "r_", "w_", "dut_", "tb_", "f_", "d_", "l_", "h_", "v_", "n_", 
                     "b_", "a_", "e_"]

class VerilogParser:
    """Verilog解析器类"""
    
    def __init__(self):
        """初始化解析器"""
        self.file_path = ""
        self.content = ""
        self.processed_content = ""
        self.lines = []
        self.module_name = ""
        self.parameters = {}
        self.defined_signals = set()
        self.all_signals = OrderedDict()
        self.module_instances = set()
        self.module_names = set()
        self.instance_module_names = []
        
    def parse_file(self, file_path: str) -> None:
        """
        解析Verilog文件
        
        参数:
            file_path: 文件路径
            
        异常:
            ParseError: 文件解析失败
        """
        self.file_path = file_path
        self.content = read_file(file_path)
        self._preprocess()
        self._extract_signals()
        self._extract_module_info()
        
    def _preprocess(self) -> None:
        """
        预处理文件内容
        - 移除注释
        - 处理宏定义
        """
        # 移除注释
        content = remove_comments(self.content)
        
        # 处理宏定义 (将宏替换为空格以保持行号)
        content = re.sub(r'`\w+', ' ', content)
        
        self.processed_content = content
        self.lines = self.processed_content.splitlines()
        
        # 提取参数定义
        self.parameters = extract_parameters(self.processed_content)
        
    def _extract_signals(self) -> None:
        """
        提取所有信号
        - 已定义信号
        - 所有可能的信号
        """
        # 提取已定义的信号
        self._extract_defined_signals()
        
        # 提取所有可能的信号（保持顺序）
        signal_pattern = re.compile(r'\b(\w+)\b')
        for line in self.lines:
            for signal in signal_pattern.findall(line):
                if signal not in self.all_signals:
                    self.all_signals[signal] = True
    
    def _extract_defined_signals(self) -> None:
        """提取已定义的信号"""
        # 匹配wire声明 - 支持多个信号和位宽
        wire_patterns = [
            # 标准wire声明
            r'\bwire\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            # 参数化位宽wire声明
            r'\bwire\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            # wire数组声明
            r'\bwire\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_]+)\s*\[\s*[\w\d\:\-\+]+\s*\];'
        ]
        
        for pattern in wire_patterns:
            self._extract_signals_by_pattern(pattern)
        
        # 匹配reg声明 - 支持多个信号和位宽
        reg_patterns = [
            # 标准reg声明
            r'\breg\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            # 参数化位宽reg声明
            r'\breg\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            # reg数组声明
            r'\breg\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_]+)\s*\[\s*[\w\d\:\-\+]+\s*\];'
        ]
        
        for pattern in reg_patterns:
            self._extract_signals_by_pattern(pattern)
        
        # 匹配logic声明 (SystemVerilog)
        logic_patterns = [
            r'\blogic\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\blogic\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in logic_patterns:
            self._extract_signals_by_pattern(pattern)
        
        # 匹配input/output/inout声明 - 支持wire/reg类型和位宽
        io_patterns = [
            r'\b(?:input|output|inout)\s+(?:wire|reg|logic)?\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(?:input|output|inout)\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);'
        ]
        
        for pattern in io_patterns:
            self._extract_signals_by_pattern(pattern)
    
    def _extract_signals_by_pattern(self, pattern: str) -> None:
        """
        根据模式提取信号
        
        参数:
            pattern: 正则表达式模式
        """
        matches = re.finditer(pattern, self.processed_content)
        for match in matches:
            signals_group = match.group(1)
            if signals_group:
                signals = signals_group.split(',')
                for signal in signals:
                    signal = signal.strip()
                    if signal:
                        # 处理带有注释或空格的信号名
                        signal_name = re.sub(r'\s*(\w+)\s*.*', r'\1', signal)
                        if signal_name and re.match(r'^[a-zA-Z_]\w*$', signal_name):
                            self.defined_signals.add(signal_name)
    
    def _extract_module_info(self) -> None:
        """
        提取模块相关信息
        - 模块名
        - 模块实例
        - 实例模块名
        """
        # 提取模块名
        module_pattern = re.compile(r'\bmodule\s+(\w+)')
        module_matches = module_pattern.search(self.processed_content)
        if module_matches:
            self.module_name = module_matches.group(1)
            self.module_names.add(self.module_name)
        
        # 提取模块实例化信号
        instance_pattern = re.compile(r'\.(\w+)')
        self.module_instances.update(instance_pattern.findall(self.processed_content))
        
        # 提取实例模块名
        instance_module_patterns = [
            re.compile(r'(\w+)\s+(?:u_|i_|inst_|g_|gen_|x_|m_|s_|p_|c_|r_|w_|dut_|tb_|f_|d_|l_|h_|v_|n_|b_|a_|e_)?(\w+)\s*\(\.'),  # 模块名 [前缀]实例名(.端口
            re.compile(r'(\w+)\s+(\w+)\s*\('),  # 模块名 实例名(
            re.compile(r'(\w+)\s+(?:u_|i_|inst_|g_|gen_|x_|m_|s_|p_|c_|r_|w_|dut_|tb_|f_|d_|l_|h_|v_|n_|b_|a_|e_)(\w+)\s*\('),  # 模块名 前缀实例名(
            re.compile(r'generate\s+.*?\s+(\w+)\s*:'),  # generate块名称
            re.compile(r'//\s*generate\s+.*?\s+(\w+)'),  # generate注释名
            re.compile(r'//.*?generate\s+.*?\s+(\w+)'),  # 更宽松的generate注释名匹配
            re.compile(r'endgenerate\s+.*?\s+(\w+)')  # endgenerate块名称
        ]
        
        for pattern in instance_module_patterns:
            self.instance_module_names.extend(pattern.findall(self.processed_content))
    
    def get_signal_bitwidth(self, signal_name: str) -> Optional[str]:
        """
        获取信号位宽
        
        参数:
            signal_name: 信号名
            
        返回:
            位宽字符串，如"[7:0]"，如果无法确定返回None
        """
        # 查找信号使用位宽的地方
        patterns = [
            # 例如：assign data[7:0] = value;
            re.compile(rf'{signal_name}\s*\[(\d+):(\d+)\]'),
            # 例如：assign data[WIDTH-1:0] = value;
            re.compile(rf'{signal_name}\s*\[(\w+)\s*-\s*1\s*:\s*0\]'),
            # 例如：assign data[WIDTH:0] = value;
            re.compile(rf'{signal_name}\s*\[(\w+)\s*:\s*0\]'),
            # 例如：assign data[0] = value; (单比特)
            re.compile(rf'{signal_name}\s*\[(\d+)\]'),
            # 例如：assign data[WIDTH] = value; (参数索引)
            re.compile(rf'{signal_name}\s*\[(\w+)\]'),
            # 例如：assign data[WIDTH+:8] = value; (增量范围)
            re.compile(rf'{signal_name}\s*\[(\w+)\s*\+\s*:\s*(\d+)\]'),
            # 例如：assign data[WIDTH-:8] = value; (减量范围)
            re.compile(rf'{signal_name}\s*\[(\w+)\s*\-\s*:\s*(\d+)\]'),
            # 例如：assign data[8*i+:8] = value; (表达式增量范围)
            re.compile(rf'{signal_name}\s*\[([\w\d\*\+\-\s]+)\+:(\d+)\]'),
            # 例如：assign data[8*i-:8] = value; (表达式减量范围)
            re.compile(rf'{signal_name}\s*\[([\w\d\*\+\-\s]+)\-:(\d+)\]')
        ]
        
        for pattern in patterns:
            matches = pattern.findall(self.content)
            if matches:
                # 处理第一个匹配
                if len(matches[0]) == 2:  # 范围 [x:y]
                    high, low = matches[0]
                    # 如果是参数，尝试替换
                    if high in self.parameters:
                        try:
                            high_val = int(self.parameters[high])
                            high = str(high_val)
                        except ValueError:
                            # 如果参数值不是简单数字，保留原始参数名
                            pass
                    if low in self.parameters:
                        try:
                            low_val = int(self.parameters[low])
                            low = str(low_val)
                        except ValueError:
                            # 如果参数值不是简单数字，保留原始参数名
                            pass
                    return f"[{high}:{low}]"
                elif len(matches[0]) == 1:  # 单比特 [x]
                    index = matches[0][0]
                    # 如果是参数，尝试替换
                    if index in self.parameters:
                        try:
                            index_val = int(self.parameters[index])
                            return f"[{index_val}:0]"  # 假设是位宽参数
                        except ValueError:
                            return "[0:0]"  # 无法解析参数值，默认为单比特
                    try:
                        # 尝试将索引转换为整数
                        index_val = int(index)
                        return "[0:0]"  # 单比特索引转换为范围格式
                    except ValueError:
                        # 如果不是数字，可能是参数名但未在参数列表中找到
                        return f"[{index}:0]"  # 假设是位宽参数
        
        # 尝试从输入/输出信号定义推断
        type_patterns = [
            # 标准位宽格式 input [7:0] data;
            re.compile(rf'(?:input|output|inout)\s+(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])\s+{signal_name}'),
            # 带类型的位宽格式 input wire [7:0] data;
            re.compile(rf'(?:input|output|inout)\s+(?:wire|reg|logic)\s+(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])\s+{signal_name}'),
            # 参数化位宽 input [WIDTH-1:0] data;
            re.compile(rf'(?:input|output|inout)\s+(?:\[\s*(\w+)\s*-\s*1\s*:\s*0\s*\])\s+{signal_name}')
        ]
        
        for pattern in type_patterns:
            match = pattern.search(self.content)
            if match:
                if match.group(1) and match.group(2):
                    # 标准位宽格式 [x:y]
                    return f"[{match.group(1)}:{match.group(2)}]"
                elif match.group(1):
                    # 参数化位宽 [PARAM-1:0]
                    param_name = match.group(1)
                    if param_name in self.parameters:
                        try:
                            param_val = int(self.parameters[param_name])
                            return f"[{param_val-1}:0]"
                        except ValueError:
                            return f"[{param_name}-1:0]"
                    return f"[{param_name}-1:0]"
        
        return None
    
    def get_undefined_signals(self, exclude_patterns: List[str] = None) -> List[str]:
        """
        获取未定义信号列表
        
        参数:
            exclude_patterns: 排除模式列表
            
        返回:
            未定义信号列表
        """
        # 创建排除集合
        exclude_set = set(VERILOG_KEYWORDS)
        exclude_set.update(self.defined_signals)
        exclude_set.update(self.module_names)
        exclude_set.update(self.module_instances)
        exclude_set.update(self.parameters.keys())
        
        # 排除数字
        number_pattern = re.compile(r'^\d+$')
        exclude_numbers = {signal for signal in self.all_signals if number_pattern.match(signal)}
        exclude_set.update(exclude_numbers)
        
        # 排除Verilog数值常量 (如1'h0, 8'b00101010等)
        verilog_number_pattern = re.compile(r'\d+\'[hbd][\w_]+')
        verilog_numbers = set()
        for line in self.lines:
            for match in verilog_number_pattern.finditer(line):
                verilog_numbers.add(match.group(0))
        exclude_set.update(verilog_numbers)
        
        # 排除带有常用前缀的实例名
        flat_instance_names = [item for sublist in self.instance_module_names for item in (sublist if isinstance(sublist, tuple) else [sublist])]
        prefixed_instances = set()
        for prefix in INSTANCE_PREFIXES:
            for name in flat_instance_names:
                if isinstance(name, str) and name.startswith(prefix):
                    prefixed_instances.add(name)
                # 处理没有前缀的情况，将前缀添加到名称前并排除
                prefixed_name = prefix + name if isinstance(name, str) else ""
                if prefixed_name:
                    prefixed_instances.add(prefixed_name)
        exclude_set.update(prefixed_instances)
        
        # 应用用户自定义排除模式
        if exclude_patterns:
            user_exclude_patterns = []
            for pattern in exclude_patterns:
                try:
                    user_exclude_patterns.append(re.compile(pattern))
                except re.error:
                    print(f"警告：无效的正则表达式模式 '{pattern}'，已忽略")
                    
            for pattern in user_exclude_patterns:
                for signal in list(self.all_signals.keys()):
                    if pattern.search(signal):
                        exclude_set.add(signal)
        
        # 提取未定义信号
        undefined_signals = []
        for signal in self.all_signals:
            if signal not in exclude_set:
                undefined_signals.append(signal)
                
        return undefined_signals
        
    def get_signal_widths(self, signals: List[str]) -> Dict[str, Optional[str]]:
        """
        获取信号位宽字典
        
        参数:
            signals: 信号列表
            
        返回:
            信号名到位宽的字典
        """
        signal_widths = {}
        for signal in signals:
            signal_widths[signal] = self.get_signal_bitwidth(signal)
        return signal_widths