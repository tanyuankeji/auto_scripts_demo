import re
import sys

# Verilog/SystemVerilog保留关键字
VERILOG_KEYWORDS = {
    "module", "endmodule", "input", "output", "inout", "assign", "always", "if",
    "else", "case", "endcase", "begin", "end", "wire", "reg", "logic", "parameter"
}

def parse_verilog(file_name):
    """解析Verilog文件，提取未定义的信号"""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        sys.exit(1)

    signals = set()
    defined_signals = set()
    module_names = set()

    # 定义信号的正则表达式
    signal_pattern = re.compile(r'\b(\w+)\b')
    define_patterns = [
        re.compile(r'\b(?:wire|reg|logic)\s+(\w+)'),  # wire/reg/logic定义
        re.compile(r'\binput\s+(?:\d+:\d+\s+)?(\w+)'),  # input定义
        re.compile(r'\boutput\s+(?:\d+:\d+\s+)?(\w+)'),  # output定义
        re.compile(r'\binout\s+(?:\d+:\d+\s+)?(\w+)')  # inout定义
    ]

    # 模块名的正则表达式
    module_pattern = re.compile(r'\bmodule\s+(\w+)')

    # 处理文件行
    for line in lines:
        # 移除注释
        line = re.sub(r'//.*', '', line)  # 单行注释
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)  # 多行注释

        # 提取所有可能的标识符
        signals.update(signal_pattern.findall(line))

        # 提取定义的信号
        for pattern in define_patterns:
            defined_signals.update(pattern.findall(line))

        # 提取模块名
        module_match = module_pattern.search(line)
        if module_match:
            module_names.add(module_match.group(1))

    # 排除保留关键字和模块名
    signals = signals - VERILOG_KEYWORDS - module_names

    # 确定未定义的信号
    undefined_signals = signals - defined_signals

    return undefined_signals

def generate_signal_definitions(undefined_signals):
    """生成未定义信号的自动补全定义"""
    definitions = []
    for signal in undefined_signals:
        definitions.append(f"wire {signal}; // Automatically added\n")
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
    if undefined_signals:
        print(f"Found undefined signals: {', '.join(undefined_signals)}")
        definitions = generate_signal_definitions(undefined_signals)
        write_output(file_name, definitions)
    else:
        print("No undefined signals found.")

if __name__ == "__main__":
    main()