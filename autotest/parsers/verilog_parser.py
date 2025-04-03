#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Verilog解析器模块

此模块用于解析Verilog设计文件，提取模块接口、参数和信号信息
支持通过pyverilog进行解析（若安装）以及通过正则表达式进行基本解析
"""

import os
import re
import logging
import difflib
from pathlib import Path

# 尝试导入pyverilog
try:
    import pyverilog
    from pyverilog.vparser.parser import parse
    PYVERILOG_AVAILABLE = True
except ImportError:
    PYVERILOG_AVAILABLE = False
    logging.warning("pyverilog未安装，将使用内置的正则表达式解析器")

logger = logging.getLogger(__name__)

class Signal:
    """表示Verilog中的信号"""
    
    name_width = 1  # 最长信号名宽度（用于格式化输出）
    width_width = 1  # 最长位宽描述宽度
    
    def __init__(self, name, signal_type="wire", port="none", width=""):
        """
        初始化信号对象
        
        参数:
            name: 信号名称
            signal_type: 信号类型 (wire/reg)
            port: 端口类型 (input/output/inout/none)
            width: 位宽描述 (如 [7:0])
        """
        self.name = name
        self.type = signal_type
        self.port = port
        self.width = width
        self.ctrl_sig = 0  # 是否为控制信号
        self.find_valid_sig = 0  # 是否找到对应的valid信号
        self.find_ready_sig = 0  # 是否找到对应的ready信号
        self.bus_list = []  # 相关的总线信号列表
        
        # 更新类的静态变量
        Signal.name_width = max(Signal.name_width, len(name))
        Signal.width_width = max(Signal.width_width, len(width))
    
    def __str__(self):
        """字符串表示"""
        result = "信号: {}\n".format(self.name)
        result += "  类型: {}\n".format(self.type)
        result += "  端口: {}\n".format(self.port)
        result += "  位宽: {}\n".format(self.width)
        return result
    
    def valid_en(self):
        """检查是否为valid信号"""
        if re.search(r"valid$", self.name):
            self.ctrl_sig = 1
            return 1
        return 0
    
    def ready_en(self):
        """检查是否为ready信号"""
        if re.search(r"ready$", self.name):
            self.ctrl_sig = 1
            return 1
        return 0
    
    def org_valid_sig(self):
        """获取对应的valid信号名"""
        if self.ready_en() == 1:
            self.valid_sig = re.sub(r"ready$", "valid", self.name)
        else:
            self.valid_sig = self.name + "_valid"
        return self.valid_sig
    
    def org_ready_sig(self):
        """获取对应的ready信号名"""
        if self.valid_en() == 1:
            self.ready_sig = re.sub(r"valid$", "ready", self.name)
        else:
            self.ready_sig = self.name + "_ready"
        return self.ready_sig
    
    def set_valid_sig(self, sig):
        """设置对应的valid信号"""
        self.valid_sig = sig
        self.find_valid_sig = 1
    
    def set_ready_sig(self, sig):
        """设置对应的ready信号"""
        self.ready_sig = sig
        self.find_ready_sig = 1
    
    def valid_get_bus(self, sig):
        """将信号添加到valid信号的总线列表中"""
        self.bus_list.append(sig)


class VerilogParser:
    """Verilog解析器类"""
    
    def __init__(self, file_path, top_module=None):
        """
        初始化解析器
        
        参数:
            file_path: Verilog文件路径
            top_module: 顶层模块名，如果为None则从文件名推断
        """
        self.file_path = file_path
        self.top_module = top_module or Path(file_path).stem
        
        # 信号相关
        self.signals = []  # 所有信号列表
        self.signal_dict = {}  # 信号名到Signal对象的映射
        self.valid_signals = []  # valid信号列表
        self.ready_signals = []  # ready信号列表
        
        # 参数相关
        self.parameters = []  # 参数名列表
        self.param_dict = {}  # 参数名到参数值的映射
        
        # 用于验证的信号
        self.check_valid = ""  # 用于检查的valid信号
        
    def parse(self):
        """解析Verilog文件"""
        if not os.path.exists(self.file_path):
            logger.error(f"文件不存在: {self.file_path}")
            return False
        
        # 如果pyverilog可用，优先使用pyverilog解析
        if PYVERILOG_AVAILABLE:
            return self._parse_with_pyverilog()
        else:
            return self._parse_with_regex()
    
    def _parse_with_pyverilog(self):
        """使用pyverilog解析Verilog文件"""
        try:
            ast, _ = parse([self.file_path])
            
            # 遍历AST查找顶层模块
            for module in ast.description.definitions:
                if module.name == self.top_module:
                    # 解析端口列表
                    self._parse_module_ports(module)
                    # 解析参数列表
                    self._parse_module_params(module)
                    # 解析模块内部信号
                    self._parse_module_signals(module)
                    break
            
            # 查找valid和ready信号之间的关系
            self._find_valid_ready_relationships()
            
            return True
        except Exception as e:
            logger.error(f"pyverilog解析出错: {str(e)}")
            logger.info("回退到正则表达式解析")
            return self._parse_with_regex()
    
    def _parse_module_ports(self, module):
        """从pyverilog的AST中解析模块端口"""
        # 实现从AST解析端口的逻辑
        pass
    
    def _parse_module_params(self, module):
        """从pyverilog的AST中解析模块参数"""
        # 实现从AST解析参数的逻辑
        pass
    
    def _parse_module_signals(self, module):
        """从pyverilog的AST中解析模块内部信号"""
        # 实现从AST解析信号的逻辑
        pass
    
    def _parse_with_regex(self):
        """使用正则表达式解析Verilog文件"""
        try:
            with open(self.file_path, "r") as f:
                content = f.readlines()
            
            # 移除注释
            content = self._remove_comments(content)
            
            # 提取模块定义
            module_lines = self._extract_module_definition(content)
            
            # 解析信号和参数
            self._parse_signals_and_params(module_lines)
            
            # 查找valid和ready信号之间的关系
            self._find_valid_ready_relationships()
            
            return True
        except Exception as e:
            logger.error(f"正则表达式解析出错: {str(e)}")
            return False
    
    def _remove_comments(self, lines):
        """移除Verilog注释"""
        result = []
        in_multiline_comment = False
        
        for line in lines:
            # 处理多行注释
            if in_multiline_comment:
                if "*/" in line:
                    line = line[line.find("*/") + 2:]
                    in_multiline_comment = False
                else:
                    continue
            
            # 处理行内的多行注释
            while "/*" in line and not in_multiline_comment:
                comment_start = line.find("/*")
                if "*/" in line[comment_start:]:
                    comment_end = line.find("*/", comment_start) + 2
                    line = line[:comment_start] + line[comment_end:]
                else:
                    line = line[:comment_start]
                    in_multiline_comment = True
            
            # 处理单行注释
            if "//" in line:
                line = line[:line.find("//")]
            
            # 添加非空行
            if line.strip():
                result.append(line)
        
        return result
    
    def _extract_module_definition(self, lines):
        """提取模块定义"""
        module_lines = []
        in_module = False
        module_depth = 0
        
        for line in lines:
            if re.search(r"^\s*module\s+" + self.top_module + r"\b", line):
                in_module = True
                module_depth = 1
                module_lines.append(line)
            elif in_module:
                module_lines.append(line)
                
                # 处理嵌套模块
                if "module" in line:
                    module_depth += 1
                if "endmodule" in line:
                    module_depth -= 1
                    if module_depth == 0:
                        break
        
        return module_lines
    
    def _parse_signals_and_params(self, module_lines):
        """解析信号和参数"""
        for line in module_lines:
            # 解析参数
            param_match = re.search(r"^\s*(parameter|localparam)\s+(\w+)\s*=\s*([\$\(\)\w\']+)", line)
            if param_match:
                param_name = param_match.group(2)
                param_value = param_match.group(3)
                self.parameters.append(param_name)
                self.param_dict[param_name] = param_value
                continue
            
            # 解析端口和信号
            signal_match = re.search(r"^\s*(input|output|inout|wire|reg)(\s+wire|\s+reg)?\s+(\[.*\])?\s*([\s,\w]+)\s*", line)
            if signal_match:
                signal_type = "wire"
                port_type = "none"
                width = ""
                
                if signal_match.group(3):
                    width = signal_match.group(3).strip()
                
                if signal_match.group(1) in ["input", "output", "inout"]:
                    port_type = signal_match.group(1).strip()
                else:
                    signal_type = signal_match.group(1).strip()
                
                if signal_match.group(2):
                    signal_type = signal_match.group(2).strip()
                
                # 分割多个信号名
                for sig_name in signal_match.group(4).split(","):
                    name = sig_name.strip()
                    if name:
                        signal = Signal(name, signal_type, port_type, width)
                        
                        if port_type in ["input", "output", "inout"]:
                            if signal.valid_en():
                                self.valid_signals.append(name)
                            elif signal.ready_en():
                                self.ready_signals.append(name)
                            
                            self.signals.append(signal)
                            self.signal_dict[name] = signal
    
    def _find_valid_ready_relationships(self):
        """查找valid和ready信号之间的关系"""
        # 查找valid信号对应的ready信号
        self._find_valid_ready_pairs()
        
        # 查找数据信号对应的valid/ready信号
        self._find_signal_valid_ready_pairs()
        
        # 将数据信号关联到valid信号
        self._associate_signals_to_valid()
    
    def _find_valid_ready_pairs(self):
        """根据命名相似度查找valid和ready信号对之间的关系"""
        for signal in self.signals:
            if signal.valid_en():
                ratio_threshold = 0.4
                ready_sig = signal.org_ready_sig()
                
                for ready in self.ready_signals:
                    if self.signal_dict[ready].port == signal.port:
                        continue
                    
                    similarity = self._similarity_ratio(signal.name, ready)
                    if similarity > ratio_threshold:
                        ratio_threshold = similarity
                        signal.set_ready_sig(ready)
    
    def _find_signal_valid_ready_pairs(self):
        """查找数据信号对应的valid和ready信号"""
        for signal in self.signals:
            if not signal.valid_en() and not signal.ready_en():
                # 查找ready信号
                ratio = 0.4
                ready_sig = signal.org_ready_sig()
                
                for ready in self.ready_signals:
                    if self.signal_dict[ready].port == signal.port:
                        continue
                    
                    similarity = self._similarity_ratio(signal.name, ready)
                    if similarity > ratio:
                        ratio = similarity
                        signal.set_ready_sig(ready)
                
                # 查找valid信号
                ratio = 0.5
                valid_sig = signal.org_valid_sig()
                
                for valid in self.valid_signals:
                    if self.signal_dict[valid].port != signal.port:
                        continue
                    
                    similarity = self._similarity_ratio(signal.name, valid)
                    if similarity > ratio:
                        ratio = similarity
                        signal.set_valid_sig(valid)
    
    def _associate_signals_to_valid(self):
        """将数据信号关联到对应的valid信号"""
        for signal in self.signals:
            if signal.find_valid_sig:
                valid = self.signal_dict[signal.valid_sig]
                valid.valid_get_bus(signal)
    
    def _similarity_ratio(self, str1, str2):
        """计算两个字符串的相似度"""
        return difflib.SequenceMatcher(None, str1, str2).ratio()
    
    def get_valid_signal_for_verification(self):
        """获取用于验证的valid信号"""
        for valid_name in self.valid_signals:
            valid = self.signal_dict[valid_name]
            if len(valid.bus_list) > 0 and valid.port == "output":
                return valid_name
        return "" 