import numpy as np  # 导入numpy库，用于数值计算
import re  # 导入正则表达式库，用于字符串匹配
import sys  # 导入系统库，用于处理命令行参数和退出程序

# Verilog/SystemVerilog保留关键字集合
VERILOG_KEYWORDS = {
    "module", "endmodule", "input", "output", "inout", "assign", "always", "if",
    "else", "case", "endcase", "begin", "end", "wire", "reg", "logic", "parameter"
}

def parse_verilog(file_name):
    """解析Verilog文件，提取未定义的信号和模块例化信号"""
    try:
        with open(file_name, 'r') as file:  # 尝试打开指定的Verilog文件
            lines = file.readlines()  # 读取文件的所有行
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")  # 文件未找到时输出错误信息
        sys.exit(1)  # 退出程序

    signals = set()  # 存储所有信号的集合
    defined_signals = set()  # 存储已定义信号的集合
    module_names = set()  # 存储模块名的集合
    instance_signals = set()  # 存储实例信号的集合
    module_instance_signals = set()  # 存储模块实例化信号的集合
    instance_module_names = set()  # 存储实例模块名的集合
    test = set()  # 备用集合，未使用

    # 定义信号的正则表达式
    signal_pattern = re.compile(r'\b(\w+)\b')  # 匹配所有单词字符
    define_patterns = [
        re.compile(r'\b(?:wire|reg|logic)\s+(\w+)'),  # 匹配wire/reg/logic定义
        re.compile(r'\binput\s+(?:\d+:\d+\s+)?(\w+)'),  # 匹配input定义
        re.compile(r'\boutput\s+(?:\d+:\d+\s+)?(\w+)'),  # 匹配output定义
        re.compile(r'\binout\s+(?:\d+:\d+\s+)?(\w+)')  # 匹配inout定义
    ]

    # 模块例化信号的正则表达式
    instance_pattern = re.compile(r'\.(\w+)')  # 匹配模块实例化信号

    instance_module_pattern = [
        re.compile(r'(\w+)\s+\w+\s\(\.\w+'),  # 匹配模块名和实例名
        re.compile(r'\w+\s+(\w+)\s\(\.\w+'),  # 匹配实例名和模块名
        re.compile(r'(\w+)\s+(\w+)\s*\(')  # 匹配模块名和实例名
    ]

    # 模块名的正则表达式
    module_pattern = re.compile(r'\bmodule\s+(\w+)')  # 匹配模块定义

    # 处理文件行
    for line in lines:
        # 移除注释
        line = re.sub(r'//.*', '', line)  # 移除单行注释
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)  # 移除多行注释

        # 提取所有可能的标识符
        signals.update(signal_pattern.findall(line))  # 更新信号集合

        # 提取定义的信号
        for pattern in define_patterns:
            defined_signals.update(pattern.findall(line))  # 更新已定义信号集合

        # 提取模块例化中的信号
        instance_signals = instance_pattern.findall(line)  # 查找实例信号
        module_instance_signals.update(instance_signals)  # 更新模块实例信号集合

        # 提取模块例化中的模块名
        for pattern in instance_module_pattern:
            instance_module_names.update(pattern.findall(line))  # 更新实例模块名集合
        
        # 提取模块名
        module_match = module_pattern.search(line)  # 查找模块名
        if module_match:
            module_names.add(module_match.group(1))  # 添加模块名到集合

    # print(f"module_instance_signals: {', '.join(module_instance_signals)}")  # 调试输出
    # print(f"instance_module_names: {instance_module_names}")  # 调试输出

    flatten_instance_module_names = [item for sublist in instance_module_names for item in sublist]  # 扁平化实例模块名
    # print(f"flatten_instance_module_names: {flatten_instance_module_names}")  # 调试输出

    set_flatten_instance_module_names = set(flatten_instance_module_names)  # 转换为集合以去重
    # print(f"set_flatten_instance_module_names: {set_flatten_instance_module_names}")  # 调试输出

    # print(f"signals: {signals}")  # 调试输出
    # 排除保留关键字和模块名
    signals = signals - VERILOG_KEYWORDS - module_names - set_flatten_instance_module_names  # 更新信号集合
    # print(f"signals: {signals}")  # 调试输出

    # 确定未定义的信号
    undefined_signals = signals - defined_signals  # 找到未定义信号

    # print(f"signals: {', '.join(signals)}")  # 调试输出
    # print(f"undefined_signals: {', '.join(undefined_signals)}")  # 调试输出
    # print(f"defined_signals: {', '.join(defined_signals)}")  # 调试输出

    undefined_signals = undefined_signals - module_instance_signals  # 排除模块实例化信号

    # 添加模块实例化中的未定义信号
    undefined_signals.update(undefined_signals)  # 更新未定义信号集合
    # print(f"undefined_signals: {', '.join(undefined_signals)}")  # 调试输出

    return undefined_signals  # 返回未定义信号集合

def generate_signal_definitions(undefined_signals):
    """生成未定义信号的自动补全定义"""
    definitions = []  # 存储生成的定义
    for signal in undefined_signals:
        definitions.append(f"wire {signal}; \n")  # 生成wire定义并添加到列表
    return definitions  # 返回定义列表

def write_output(file_name, definitions):
    """将生成的信号定义写入输出文件"""
    output_file = file_name.replace('.v', '_autogen.v').replace('.sv', '_autogen.sv')  # 生成输出文件名
    try:
        with open(output_file, 'w') as file:  # 尝试打开输出文件
            file.writelines(definitions)  # 写入定义到文件
        print(f"Output written to {output_file}")  # 输出成功信息
    except IOError:
        print(f"Error: Unable to write to file {output_file}")  # 输出错误信息
        sys.exit(1)  # 退出程序

def main():
    """主函数：解析文件并生成自动补全定义"""
    if len(sys.argv) != 2:  # 检查命令行参数数量
        print("Usage: python autogen_signals.py <verilog_file>")  # 输出用法信息
        sys.exit(1)  # 退出程序

    file_name = sys.argv[1]  # 获取文件名参数
    undefined_signals = parse_verilog(file_name)  # 解析Verilog文件

    if undefined_signals:  # 如果找到未定义信号
        print(f"Found undefined signals: {', '.join(undefined_signals)}")  # 输出未定义信号
        definitions = generate_signal_definitions(undefined_signals)  # 生成信号定义
        write_output(file_name, definitions)  # 写入输出文件
    else:
        print("No undefined signals found.")  # 如果没有未定义信号，输出信息

if __name__ == "__main__":
    main()  # 调用主函数