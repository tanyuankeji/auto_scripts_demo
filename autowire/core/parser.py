# parser.py
"""
Verilog解析器模块
负责解析Verilog代码并提取基础信息
"""

import re
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import OrderedDict

from .utils import read_file, remove_comments, extract_parameters, ParseError, is_common_constant

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
        self.original_content = ""  # 保存原始内容用于位宽推断
        self.processed_content = ""
        self.lines = []
        self.module_name = ""
        self.parameters = {}
        self.defined_signals = set()
        self.port_signals = set()    # 端口信号
        self.wire_signals = set()    # wire类型信号
        self.reg_signals = set()     # reg类型信号
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
        # 保存原始内容以备信号位宽推断
        self.original_content = self.content
        
        # 移除注释
        self.processed_content = remove_comments(self.content)
        
        # 处理宏定义
        self._process_macros()
        
        # 分割为行
        self.lines = self.processed_content.splitlines()
        
        # 提取参数定义
        self.parameters = extract_parameters(self.processed_content)
    
    def _process_macros(self) -> None:
        """处理Verilog宏定义"""
        # 替换宏定义，保留空格以保持行号一致
        self.processed_content = re.sub(r'`\w+', ' ', self.processed_content)
        
        # 特殊处理include语句
        self.processed_content = re.sub(r'`include\s+["<].*?[">]', ' ', self.processed_content)
        
        # 处理条件编译指令
        conditional_pattern = re.compile(r'`(ifdef|ifndef|else|endif|elsif|define|undef).*?$', re.MULTILINE)
        self.processed_content = conditional_pattern.sub(' ', self.processed_content)
        
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
            self._extract_signals_by_pattern(pattern, signal_set=self.wire_signals)
        self.defined_signals.update(self.wire_signals)
        
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
            self._extract_signals_by_pattern(pattern, signal_set=self.reg_signals)
        self.defined_signals.update(self.reg_signals)
        
        # 匹配logic声明 (SystemVerilog)
        logic_patterns = [
            r'\blogic\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\blogic\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in logic_patterns:
            self._extract_signals_by_pattern(pattern)
        
        # 匹配input/output/inout声明
        # 首先提取模块声明中的端口列表
        self._extract_port_signals_from_module_declaration()
        
        # 然后匹配模块内的input/output/inout声明 - 支持wire/reg类型和位宽
        io_patterns = [
            r'\b(?:input|output|inout)\s+(?:wire|reg|logic)?\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(?:input|output|inout)\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            # 新增：匹配参数化位宽
            r'\b(?:input|output|inout)\s+(?:wire|reg|logic)?\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            r'\b(?:input|output|inout)\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in io_patterns:
            self._extract_signals_by_pattern(pattern, signal_set=self.port_signals)
        self.defined_signals.update(self.port_signals)
        
        # 检查并排除端口信号和内部使用的相同名称信号
        self._exclude_port_signal_wire_declaration()
    
    def _extract_signals_by_pattern(self, pattern: str, signal_set: Optional[Set[str]] = None) -> None:
        """
        使用指定模式提取信号
        
        参数:
            pattern: 正则表达式模式
            signal_set: 如果提供，将提取的信号添加到此集合
        """
        pattern_obj = re.compile(pattern)
        
        for match in pattern_obj.finditer(self.processed_content):
            signals_str = match.group(1)
            # 处理逗号分隔的多个信号情况
            for signal in re.split(r'\s*,\s*', signals_str):
                signal = signal.strip()
                if signal and re.match(r'^[a-zA-Z_]\w*$', signal):
                    self.defined_signals.add(signal)
                    if signal_set is not None:
                        signal_set.add(signal)
    
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
        
        # 使用原始内容进行匹配，以便正确处理位宽
        content_to_search = self.original_content
        
        for pattern in patterns:
            matches = pattern.findall(content_to_search)
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
            match = pattern.search(content_to_search)
            if match:
                # 确保在访问前检查捕获组的数量和存在性
                groups = match.groups()
                if len(groups) >= 2 and groups[0] is not None and groups[1] is not None:
                    # 标准位宽格式 [x:y]
                    return f"[{groups[0]}:{groups[1]}]"
                elif len(groups) >= 1 and groups[0] is not None:
                    # 参数化位宽 [PARAM-1:0]
                    param_name = groups[0]
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
        
        # 强制排除所有输入/输出信号 - 这是一个额外的保障措施
        input_output_signals = set()
        io_patterns = [
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in io_patterns:
            matches = re.finditer(pattern, self.original_content)
            for match in matches:
                signal_group = match.group(2)
                if signal_group:
                    for signal in re.split(r'\s*,\s*', signal_group):
                        signal = signal.strip()
                        if signal and re.match(r'^[a-zA-Z_]\w*$', signal):
                            input_output_signals.add(signal)
        
        # 将所有输入/输出信号添加到排除集合中
        exclude_set.update(input_output_signals)
        
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
        
        # 排除常量名称
        exclude_constants = {signal for signal in self.all_signals if is_common_constant(signal)}
        exclude_set.update(exclude_constants)
        
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

    def _extract_port_signals_from_module_declaration(self) -> None:
        """从模块声明中提取端口信号"""
        # 匹配模块声明及其端口列表
        module_pattern = re.compile(r'\bmodule\s+\w+\s*#?\s*\(.*?\)\s*\(([\s\S]*?)\);', re.DOTALL)
        match = module_pattern.search(self.original_content)
        
        if match:
            port_list = match.group(1)
            # 找出所有端口名称
            port_pattern = re.compile(r'\b(\w+)(?:\s*,|\s*\)|\s*$)')
            ports = port_pattern.findall(port_list)
            
            # 将这些端口名称添加到端口信号集合中
            for port in ports:
                if port and re.match(r'^[a-zA-Z_]\w*$', port) and port not in VERILOG_KEYWORDS:
                    self.port_signals.add(port)
                    # 直接将所有端口信号添加到已定义信号集合中
                    self.defined_signals.add(port)
        
        # 显式匹配input/output/inout声明
        io_patterns = [
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in io_patterns:
            pattern_obj = re.compile(pattern)
            matches = pattern_obj.finditer(self.original_content)
            for match in matches:
                signal_group = match.group(2)
                if signal_group:
                    for signal in re.split(r'\s*,\s*', signal_group):
                        signal = signal.strip()
                        if signal and re.match(r'^[a-zA-Z_]\w*$', signal):
                            self.port_signals.add(signal)
                            self.defined_signals.add(signal)
                    
    def _exclude_port_signal_wire_declaration(self) -> None:
        """排除端口信号与内部信号同名的情况，这些信号不需要wire声明"""
        # 首先，确保所有端口信号都被标记为已定义
        for port_signal in self.port_signals:
            self.defined_signals.add(port_signal)
        
        # 匹配input/output/inout声明
        io_patterns = [
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:\[\s*[\w\d\:\-\+]+\s*\])?\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);',
            r'\b(input|output|inout)\s+\[\s*[\w\d_]+\s*(?:[\-\+]\s*[\w\d_]+)?\s*:\s*[\w\d_]+\s*\]\s*([\w\d_,\s]+);'
        ]
        
        for pattern in io_patterns:
            matches = re.finditer(pattern, self.original_content)
            for match in matches:
                signal_group = match.group(2)
                if signal_group:
                    for signal in re.split(r'\s*,\s*', signal_group):
                        signal = signal.strip()
                        if signal:
                            self.defined_signals.add(signal)
                            self.port_signals.add(signal)
        
        # 下面是原有的额外检查逻辑，保留以确保完全排除所有端口信号
        # 对于模块内部直接使用但与端口同名的信号，可能需要额外处理
        for port_signal in self.port_signals:
            # 排除简单赋值：assign port_signal = xxx; 或 xxx = port_signal;
            assignment_patterns = [
                re.compile(f'assign\\s+{port_signal}\\s*='),
                re.compile(f'=\\s*{port_signal}\\b')
            ]
            
            for pattern in assignment_patterns:
                if pattern.search(self.processed_content):
                    # 如果端口信号在赋值中使用，则标记为已定义
                    self.defined_signals.add(port_signal)
                    
            # 排除在always块内使用
            always_pattern = re.compile(f'always\\s+@.*?{port_signal}')
            if always_pattern.search(self.processed_content):
                self.defined_signals.add(port_signal)
                
            # 排除在实例化端口连接中使用
            port_connection_pattern = re.compile(f'\\.\\w+\\s*\\(\\s*{port_signal}\\s*\\)')
            if port_connection_pattern.search(self.processed_content):
                self.defined_signals.add(port_signal)
                
            # 排除在case语句中使用
            case_pattern = re.compile(f'case\\s*\\(.*?{port_signal}|{port_signal}\\s*:')
            if case_pattern.search(self.processed_content):
                self.defined_signals.add(port_signal)
                
            # 排除在if条件中使用
            if_pattern = re.compile(f'if\\s*\\(.*?{port_signal}')
            if if_pattern.search(self.processed_content):
                self.defined_signals.add(port_signal)