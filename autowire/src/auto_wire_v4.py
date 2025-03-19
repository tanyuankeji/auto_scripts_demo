import numpy as np
import re
import sys

# Verilog/SystemVerilog保留关键字
VERILOG_KEYWORDS = np.array([
    "module", "endmodule", "input", "output", "inout", "assign", "always", "if",
    "else", "case", "endcase", "begin", "end", "wire", "reg", "logic", "parameter",
    "generate", "endgenerate", "for", "while", "repeat", "posedge", "negedge",
    "include", "define", "ifdef", "ifndef", "endif", "timescale", "initial", "function",
])

def parse_verilog(file_name):
    """解析Verilog文件，提取未定义的信号和模块例化信号"""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        sys.exit(1)

    signals = []
    defined_signals = []
    module_names = []
    instance_signals = []
    module_instance_signals = []
    instance_module_names = []
    declared_signals = []
    undefined_signals = []

    # 定义信号的正则表达式
    signal_pattern = re.compile(r'\b(\w+)\b')
    define_patterns = [
        re.compile(r'\b(?:wire|reg|logic)\s+(\w+)'),  # wire/reg/logic定义
        re.compile(r'\binput\s+(?:\d+:\d+\s+)?(\w+)'),  # input定义
        re.compile(r'\boutput\s+(?:\d+:\d+\s+)?(\w+)'),  # output定义
        re.compile(r'\binout\s+(?:\d+:\d+\s+)?(\w+)')  # inout定义
    ]

    # 模块例化信号的正则表达式
    instance_pattern = re.compile(r'\.(\w+)')
    
    instance_module_pattern = [
        re.compile(r'(\w+)\s+\w+\s\(\.\w+'),
        re.compile(r'\w+\s+(\w+)\s\(\.\w+'),
        re.compile(r'(\w+)\s+(\w+)\s*\(')  # 匹配模块名和例化名
    ]

    # 模块名的正则表达式
    module_pattern = re.compile(r'\bmodule\s+(\w+)')

    # 处理文件行
    for line in lines:
        # 移除注释
        line = re.sub(r'//.*', '', line)  # 单行注释
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)  # 多行注释

        # 提取所有可能的标识符
        signals.append(signal_pattern.findall(line))

        # 提取定义的信号
        for pattern in define_patterns:
            defined_signals.append(pattern.findall(line))

        # 提取模块例化中的信号
        instance_signals = instance_pattern.findall(line)
        module_instance_signals.append(instance_signals)

        # 提取模块例化中的模块名
        for pattern in instance_module_pattern:
            instance_module_names.append(pattern.findall(line))
        
        # 提取模块名
        module_match = module_pattern.search(line)
        if module_match:
            module_names.append(module_match.group(1))

    print(f"instance_module_names: {instance_module_names}")
    flatten_instance_module_names = [item for sublist in instance_module_names for item in sublist]

    print(f"flatten_instance_module_names: {flatten_instance_module_names}")
    # 排除保留关键字和模块名
    signals = np.concatenate(signals)


    flatten_instance_module_names = np.concatenate(flatten_instance_module_names)
    
    print(f"declared_signals: {declared_signals}")
    declared_signals.extend(VERILOG_KEYWORDS)
    declared_signals.extend(module_names)
    declared_signals.extend(flatten_instance_module_names)
    declared_signals.extend(np.concatenate(module_instance_signals))
    declared_signals.extend(np.concatenate(defined_signals))
    print(f"declared_signals: {declared_signals}")
    # 确定未定义的信号

    undefined_signals = np.setdiff1d(signals, declared_signals)
    print(f"undefined_signals: {undefined_signals}")

    undefined_signals = np.setdiff1d(undefined_signals, np.concatenate(module_instance_signals))

    print(f"undefined_signals: {', '.join(undefined_signals)}")

    return undefined_signals

def generate_signal_definitions(undefined_signals):
    """生成未定义信号的自动补全定义"""
    definitions = []
    for signal in undefined_signals:
        definitions.append(f"wire {signal}; \n") # 生成wire定义
    return definitions

def write_output(file_name, definitions):
    """将生成的信号定义写入输出文件"""
    output_file = file_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')
    try:
        with open(output_file, 'w') as file:
            file.writelines(definitions)
        print(f"Output written to {output_file}")
    except IOError:
        print(f"Error: Unable to write to file {output_file}")
        sys.exit(1)

def main():
    """主函数：解析文件并生成自动补全定义"""
    if len(sys.argv) != 2:
        print("Usage: python autogen_signals.py <verilog_file>")
        sys.exit(1)

    file_name = sys.argv[1]
    undefined_signals = parse_verilog(file_name)

    if len(undefined_signals):
        print(f"Found undefined signals: {', '.join(undefined_signals)}")
        definitions = generate_signal_definitions(undefined_signals)
        write_output(file_name, definitions)
    else:
        print("No undefined signals found.")

if __name__ == "__main__":
    main()