#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的寄存器类型定义模块

定义了所有支持的寄存器类型及其行为特性。
"""

from typing import Dict, Any, List


class RegisterType:
    """定义寄存器类型的基类"""
    
    def __init__(self, name: str, description: str, write_behavior: str, read_behavior: str):
        """
        初始化寄存器类型
        
        参数:
            name: 寄存器类型名称
            description: 寄存器类型描述
            write_behavior: 写行为的Verilog代码模板
            read_behavior: 读行为的Verilog代码模板
        """
        self.name = name  # 寄存器类型名称
        self.description = description  # 寄存器类型描述
        self.write_behavior = write_behavior  # 写行为的Verilog代码模板
        self.read_behavior = read_behavior  # 读行为的Verilog代码模板
    
    def get_write_behavior(self, reg_name: str, data_width: int, 
                           addr: str, data: str, enable: str) -> str:
        """
        获取寄存器写行为的Verilog代码
        
        参数:
            reg_name: 寄存器名称
            data_width: 数据宽度
            addr: 地址变量名
            data: 数据变量名
            enable: 使能变量名
            
        返回:
            Verilog代码片段
        """
        # 替换模板变量
        code = self.write_behavior.replace("{reg_name}", reg_name)
        code = code.replace("{data_width}", str(data_width))
        code = code.replace("{addr}", addr)
        code = code.replace("{data}", data)
        code = code.replace("{enable}", enable)
        return code
    
    def get_read_behavior(self, reg_name: str, data_width: int, 
                          addr: str, data: str) -> str:
        """
        获取寄存器读行为的Verilog代码
        
        参数:
            reg_name: 寄存器名称
            data_width: 数据宽度
            addr: 地址变量名
            data: 数据变量名
            
        返回:
            Verilog代码片段
        """
        # 替换模板变量
        code = self.read_behavior.replace("{reg_name}", reg_name)
        code = code.replace("{data_width}", str(data_width))
        code = code.replace("{addr}", addr)
        code = code.replace("{data}", data)
        return code


class RegisterTypeManager:
    """寄存器类型管理器"""
    
    def __init__(self):
        """初始化寄存器类型管理器"""
        self.register_types = {}
        self._init_register_types()
    
    def _init_register_types(self):
        """初始化支持的寄存器类型"""
        
        # Null 类型寄存器 (不可读写)
        self.register_types["Null"] = RegisterType(
            "Null",
            "空寄存器，不可读写",
            "// {reg_name} 是 Null 类型寄存器，忽略写操作\n",
            "// {reg_name} 是 Null 类型寄存器，读取时返回0\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # ReadWrite 类型寄存器 (读写)
        self.register_types["ReadWrite"] = RegisterType(
            "ReadWrite",
            "标准读写寄存器",
            "// {reg_name} 是 ReadWrite 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 ReadWrite 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # ReadOnly 类型寄存器 (只读)
        self.register_types["ReadOnly"] = RegisterType(
            "ReadOnly",
            "只读寄存器，忽略写操作",
            "// {reg_name} 是 ReadOnly 类型寄存器，忽略写操作\n",
            "// {reg_name} 是 ReadOnly 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # ReadClean 类型寄存器 (读清零)
        self.register_types["ReadClean"] = RegisterType(
            "ReadClean",
            "读取后自动清零的寄存器",
            "// {reg_name} 是 ReadClean 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 ReadClean 类型寄存器，读取后自动清零\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // 读取后清零\n        end\n"
        )
        
        # ReadSet 类型寄存器 (读置位)
        self.register_types["ReadSet"] = RegisterType(
            "ReadSet",
            "读取后自动置位的寄存器",
            "// {reg_name} 是 ReadSet 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 ReadSet 类型寄存器，读取后自动置位\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 读取后置位\n        end\n"
        )
        
        # WriteReadClean 类型寄存器 (可写，读清零)
        self.register_types["WriteReadClean"] = RegisterType(
            "WriteReadClean",
            "可写，读取后自动清零的寄存器",
            "// {reg_name} 是 WriteReadClean 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 WriteReadClean 类型寄存器，读取后自动清零\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // 读取后清零\n        end\n"
        )
        
        # WriteReadSet 类型寄存器 (可写，读置位)
        self.register_types["WriteReadSet"] = RegisterType(
            "WriteReadSet",
            "可写，读取后自动置位的寄存器",
            "// {reg_name} 是 WriteReadSet 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 WriteReadSet 类型寄存器，读取后自动置位\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 读取后置位\n        end\n"
        )
        
        # WriteOnly 类型寄存器 (只写)
        self.register_types["WriteOnly"] = RegisterType(
            "WriteOnly",
            "只写寄存器，读取时返回0",
            "// {reg_name} 是 WriteOnly 类型寄存器\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 WriteOnly 类型寄存器，读取时返回0\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteOnlyClean 类型寄存器 (只写，写后清零)
        self.register_types["WriteOnlyClean"] = RegisterType(
            "WriteOnlyClean",
            "只写寄存器，写入后自动清零",
            "// {reg_name} 是 WriteOnlyClean 类型寄存器，写入后自动清零\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_reg <= {data_width}'d0; // 写入后清零\n        end\n",
            "// {reg_name} 是 WriteOnlyClean 类型寄存器，读取时返回0\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteOnlySet 类型寄存器 (只写，写后置位)
        self.register_types["WriteOnlySet"] = RegisterType(
            "WriteOnlySet",
            "只写寄存器，写入后自动置位",
            "// {reg_name} 是 WriteOnlySet 类型寄存器，写入后自动置位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 写入后置位\n        end\n",
            "// {reg_name} 是 WriteOnlySet 类型寄存器，读取时返回0\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteClean 类型寄存器 (写0清零)
        self.register_types["WriteClean"] = RegisterType(
            "WriteClean",
            "写0清零对应位，可读",
            "// {reg_name} 是 WriteClean 类型寄存器，写0清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & (~({data} & ~{data}));\n        end\n",
            "// {reg_name} 是 WriteClean 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # WriteCleanReadSet 类型寄存器 (写0清零，读后置位)
        self.register_types["WriteCleanReadSet"] = RegisterType(
            "WriteCleanReadSet",
            "写0清零对应位，读取后自动置位",
            "// {reg_name} 是 WriteCleanReadSet 类型寄存器，写0清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & (~({data} & ~{data}));\n        end\n",
            "// {reg_name} 是 WriteCleanReadSet 类型寄存器，读取后自动置位\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 读取后置位\n        end\n"
        )
        
        # Write1Clean 类型寄存器 (写1清零)
        self.register_types["Write1Clean"] = RegisterType(
            "Write1Clean",
            "写1清零对应位，可读",
            "// {reg_name} 是 Write1Clean 类型寄存器，写1清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~{data};\n        end\n",
            "// {reg_name} 是 Write1Clean 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Write1CleanReadSet 类型寄存器 (写1清零，读后置位)
        self.register_types["Write1CleanReadSet"] = RegisterType(
            "Write1CleanReadSet",
            "写1清零对应位，读取后自动置位",
            "// {reg_name} 是 Write1CleanReadSet 类型寄存器，写1清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~{data};\n        end\n",
            "// {reg_name} 是 Write1CleanReadSet 类型寄存器，读取后自动置位\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 读取后置位\n        end\n"
        )
        
        # Write0Clean 类型寄存器 (写0清零)
        self.register_types["Write0Clean"] = RegisterType(
            "Write0Clean",
            "写0清零对应位，可读",
            "// {reg_name} 是 Write0Clean 类型寄存器，写0清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~(~{data});\n        end\n",
            "// {reg_name} 是 Write0Clean 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Write0CleanReadSet 类型寄存器 (写0清零，读后置位)
        self.register_types["Write0CleanReadSet"] = RegisterType(
            "Write0CleanReadSet",
            "写0清零对应位，读取后自动置位",
            "// {reg_name} 是 Write0CleanReadSet 类型寄存器，写0清零对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~(~{data});\n        end\n",
            "// {reg_name} 是 Write0CleanReadSet 类型寄存器，读取后自动置位\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // 读取后置位\n        end\n"
        )
        
        # WriteSet 类型寄存器 (写置位)
        self.register_types["WriteSet"] = RegisterType(
            "WriteSet",
            "写1置位对应位，可读",
            "// {reg_name} 是 WriteSet 类型寄存器，写1置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | {data};\n        end\n",
            "// {reg_name} 是 WriteSet 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # WriteSetReadClean 类型寄存器 (写置位，读后清零)
        self.register_types["WriteSetReadClean"] = RegisterType(
            "WriteSetReadClean",
            "写1置位对应位，读取后自动清零",
            "// {reg_name} 是 WriteSetReadClean 类型寄存器，写1置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | {data};\n        end\n",
            "// {reg_name} 是 WriteSetReadClean 类型寄存器，读取后自动清零\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // 读取后清零\n        end\n"
        )
        
        # Write1Set 类型寄存器 (写1置位)
        self.register_types["Write1Set"] = RegisterType(
            "Write1Set",
            "写1置位对应位，可读",
            "// {reg_name} 是 Write1Set 类型寄存器，写1置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | {data};\n        end\n",
            "// {reg_name} 是 Write1Set 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Write1SetReadClean 类型寄存器 (写1置位，读后清零)
        self.register_types["Write1SetReadClean"] = RegisterType(
            "Write1SetReadClean",
            "写1置位对应位，读取后自动清零",
            "// {reg_name} 是 Write1SetReadClean 类型寄存器，写1置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | {data};\n        end\n",
            "// {reg_name} 是 Write1SetReadClean 类型寄存器，读取后自动清零\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // 读取后清零\n        end\n"
        )
        
        # Write0Set 类型寄存器 (写0置位)
        self.register_types["Write0Set"] = RegisterType(
            "Write0Set",
            "写0置位对应位，可读",
            "// {reg_name} 是 Write0Set 类型寄存器，写0置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | (~{data});\n        end\n",
            "// {reg_name} 是 Write0Set 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Write0SetReadClean 类型寄存器 (写0置位，读后清零)
        self.register_types["Write0SetReadClean"] = RegisterType(
            "Write0SetReadClean",
            "写0置位对应位，读取后自动清零",
            "// {reg_name} 是 Write0SetReadClean 类型寄存器，写0置位对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg | (~{data});\n        end\n",
            "// {reg_name} 是 Write0SetReadClean 类型寄存器，读取后自动清零\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // 读取后清零\n        end\n"
        )
        
        # Write1Toggle 类型寄存器 (写1翻转)
        self.register_types["Write1Toggle"] = RegisterType(
            "Write1Toggle",
            "写1翻转对应位，可读",
            "// {reg_name} 是 Write1Toggle 类型寄存器，写1翻转对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg ^ {data};\n        end\n",
            "// {reg_name} 是 Write1Toggle 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Write0Toggle 类型寄存器 (写0翻转)
        self.register_types["Write0Toggle"] = RegisterType(
            "Write0Toggle",
            "写0翻转对应位，可读",
            "// {reg_name} 是 Write0Toggle 类型寄存器，写0翻转对应位\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg ^ (~{data});\n        end\n",
            "// {reg_name} 是 Write0Toggle 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # WriteOnce 类型寄存器 (只写一次)
        self.register_types["WriteOnce"] = RegisterType(
            "WriteOnce",
            "只写一次寄存器，写入后不可再修改",
            "// {reg_name} 是 WriteOnce 类型寄存器，只写一次\n        if ({enable} && {addr} == ADDR_{reg_name} && !{reg_name}_written) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_written <= 1'b1; // 设置写标志\n        end\n",
            "// {reg_name} 是 WriteOnce 类型寄存器\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # WriteOnlyOnce 类型寄存器 (只写一次，不可读)
        self.register_types["WriteOnlyOnce"] = RegisterType(
            "WriteOnlyOnce",
            "只写一次寄存器，写入后不可再修改，不可读",
            "// {reg_name} 是 WriteOnlyOnce 类型寄存器，只写一次\n        if ({enable} && {addr} == ADDR_{reg_name} && !{reg_name}_written) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_written <= 1'b1; // 设置写标志\n        end\n",
            "// {reg_name} 是 WriteOnlyOnce 类型寄存器，读取时返回0\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # UserDefined 类型寄存器 (用户自定义)
        self.register_types["UserDefined"] = RegisterType(
            "UserDefined",
            "用户自定义寄存器类型",
            "// {reg_name} 是 UserDefined 类型寄存器\n        // 用户需要自定义写逻辑\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            // 示例：标准读写\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} 是 UserDefined 类型寄存器\n        // 用户需要自定义读逻辑\n        if ({addr} == ADDR_{reg_name}) begin\n            // 示例：标准读取\n            {data} = {reg_name}_reg;\n        end\n"
        )
    
    def get_register_type(self, type_name: str) -> RegisterType:
        """获取指定名称的寄存器类型"""
        if type_name not in self.register_types:
            raise ValueError(f"不支持的寄存器类型: {type_name}")
        return self.register_types[type_name]
    
    def get_all_register_types(self) -> List[str]:
        """获取所有支持的寄存器类型名称"""
        return list(self.register_types.keys())


if __name__ == "__main__":
    # 测试代码
    manager = RegisterTypeManager()
    print("支持的寄存器类型:")
    for reg_type in manager.get_all_register_types():
        reg_obj = manager.get_register_type(reg_type)
        print(f"- {reg_type}: {reg_obj.description}")
    
    # 测试代码生成
    test_reg = manager.get_register_type("ReadWrite")
    write_code = test_reg.get_write_behavior("TEST_REG", 32, "wr_addr", "wr_data", "wr_en")
    read_code = test_reg.get_read_behavior("TEST_REG", 32, "rd_addr", "rd_data")
    print("\n写行为代码:")
    print(write_code)
    print("\n读行为代码:")
    print(read_code) 