import re
import sys
from typing import Set, List, Tuple

# Verilog/SystemVerilog保留关键字集合
VERILOG_KEYWORDS = {
    "module", "endmodule", "input", "output", "inout", "assign", "always", "if",
    "else", "case", "endcase", "begin", "end", "wire", "reg", "logic", "parameter"
}

def remove_comments(line: str) -> str:
    """移除代码中的注释"""
    line = re.sub(r'//.*', '', line)  # 移除单行注释
    line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)  # 移除多行注释
    return line

def parse_verilog(file_name: str) -> Set[str]:
    """解析Verilog文件，提取未定义的信号"""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_name}")
        sys.exit(1)

    # 初始化集合
    signals = set()  # 所有信号
    defined_signals = set()  # 已定义信号
    module_names = set()  # 模块名
    module_instance_signals = set()  # 模块实例化信号
    instance_module_names = []  # 实例模块名

    # 定义正则表达式
    signal_pattern = re.compile(r'\b(\w+)\b')  # 匹配所有单词
    
    # 信号定义模式
    define_patterns = [
        re.compile(r'\b(?:wire|reg|logic)\s+(?:\[\d+:\d+\])?\s*(\w+)'),  # 匹配wire/reg/logic定义
        re.compile(r'\binput\s+(?:\[\d+:\d+\])?\s*(\w+)'),  # 匹配input定义
        re.compile(r'\boutput\s+(?:\[\d+:\d+\])?\s*(\w+)'),  # 匹配output定义
        re.compile(r'\binout\s+(?:\[\d+:\d+\])?\s*(\w+)')  # 匹配inout定义
    ]
    
    # 模块实例化模式
    instance_pattern = re.compile(r'\.(\w+)')  # 匹配模块实例化信号
    module_pattern = re.compile(r'\bmodule\s+(\w+)')  # 匹配模块定义
    
    instance_module_patterns = [
        re.compile(r'(\w+)\s+\w+\s\(\.\w+'),
        re.compile(r'\w+\s+(\w+)\s\(\.\w+'),
        re.compile(r'(\w+)\s+(\w+)\s*\(')
    ]

    # 处理每一行
    for line in lines:
        line = remove_comments(line)
        
        # 1. 收集所有可能的标识符
        signals.update(signal_pattern.findall(line))
        
        # 2. 识别已定义的信号
        for pattern in define_patterns:
            defined_signals.update(pattern.findall(line))
        
        # 3. 收集模块实例化信号
        module_instance_signals.update(instance_pattern.findall(line))
        
        # 4. 识别模块名和实例模块名
        for pattern in instance_module_patterns:
            instance_module_names.extend(pattern.findall(line))
            
        module_match = module_pattern.search(line)
        if module_match:
            module_names.add(module_match.group(1))

    # 5. 处理实例模块名（扁平化并去重）
    flat_instance_names = [item for sublist in instance_module_names for item in (sublist if isinstance(sublist, tuple) else [sublist])]
    set_instance_names = set(flat_instance_names)
    
    # 6. 确定未定义信号
    # 排除关键字、模块名和实例名
    signals -= VERILOG_KEYWORDS | module_names | set_instance_names
    # 排除已定义信号和模块实例化信号
    undefined_signals = signals - defined_signals - module_instance_signals

    return undefined_signals

def generate_signal_definitions(undefined_signals: Set[str]) -> List[str]:
    """为未定义信号生成wire定义"""
    return [f"wire {signal};\n" for signal in sorted(undefined_signals)]

def write_output(file_name: str, definitions: List[str]) -> None:
    """将生成的信号定义写入输出文件"""
    output_file = file_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')
    try:
        with open(output_file, 'w') as file:
            file.writelines(definitions)
        print(f"输出已写入：{output_file}")
    except IOError:
        print(f"错误：无法写入文件 {output_file}")
        sys.exit(1)

def main() -> None:
    """主函数：解析Verilog文件并生成自动补全定义"""
    if len(sys.argv) != 2:
        print("用法：python auto_wire.py <verilog文件>")
        sys.exit(1)

    file_name = sys.argv[1]
    undefined_signals = parse_verilog(file_name)

    if undefined_signals:
        print(f"发现未定义信号：{', '.join(sorted(undefined_signals))}")
        definitions = generate_signal_definitions(undefined_signals)
        write_output(file_name, definitions)
    else:
        print("未发现未定义信号。")

if __name__ == "__main__":
    main()