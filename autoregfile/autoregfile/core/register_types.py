#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寄存器类型定义模块

定义所有支持的寄存器类型及其行为。
"""

from typing import Dict, Any, List, Optional, Union, Callable


class RegisterType:
    """寄存器类型基类"""
    
    def __init__(self, name: str, description: str, readable: bool, writable: bool,
                 special_behaviors: Optional[List[str]] = None):
        """
        初始化寄存器类型
        
        参数:
            name: 类型名称
            description: 类型描述
            readable: 是否可读
            writable: 是否可写
            special_behaviors: 特殊行为列表
        """
        self.name = name
        self.description = description
        self.readable = readable
        self.writable = writable
        self.special_behaviors = special_behaviors or []
    
    def get_write_behavior(self, reg_name: str, data_width: int, 
                           addr: str, data: str, enable: str) -> str:
        """
        获取写行为Verilog代码
        
        参数:
            reg_name: 寄存器名称
            data_width: 数据宽度
            addr: 地址变量名
            data: 数据变量名
            enable: 使能变量名
            
        返回:
            Verilog代码字符串
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def get_read_behavior(self, reg_name: str, data_width: int, 
                          addr: str, data: str) -> str:
        """
        获取读行为Verilog代码
        
        参数:
            reg_name: 寄存器名称
            data_width: 数据宽度
            addr: 地址变量名
            data: 数据变量名
            
        返回:
            Verilog代码字符串
        """
        raise NotImplementedError("子类必须实现此方法")


class RegisterTypeManager:
    """寄存器类型管理器"""
    
    def __init__(self):
        """初始化寄存器类型管理器"""
        self._types: Dict[str, RegisterType] = {}
        self._init_register_types()
    
    def _init_register_types(self):
        """初始化并注册所有支持的寄存器类型"""
        # ReadWrite类型 - 标准读写寄存器
        class ReadWriteRegister(RegisterType):
            def __init__(self):
                super().__init__("ReadWrite", "标准读写寄存器", True, True)
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 标准读写寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # ReadOnly类型 - 只读寄存器
        class ReadOnlyRegister(RegisterType):
            def __init__(self):
                super().__init__("ReadOnly", "只读寄存器，忽略写操作", True, False)
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // {reg_name.upper()} 是只读寄存器，忽略写操作
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # WriteOnly类型 - 只写寄存器
        class WriteOnlyRegister(RegisterType):
            def __init__(self):
                super().__init__("WriteOnly", "只写寄存器，读取时返回0", False, True)
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 只写寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {data_width}'d0; // 只写寄存器，读取返回0
        end
                """
        
        # ReadClean类型 - 读取后自动清零
        class ReadCleanRegister(RegisterType):
            def __init__(self):
                super().__init__("ReadClean", "读取后自动清零的寄存器", True, True,
                              special_behaviors=["read_clean"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 读清零寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
            // 读取后自动清零
            {reg_name.lower()}_reg <= {data_width}'d0;
        end
                """
        
        # Write1Clean类型 - 写1清零对应位
        class Write1CleanRegister(RegisterType):
            def __init__(self):
                super().__init__("Write1Clean", "写1清零对应位，可读", True, True,
                              special_behaviors=["write_1_clean"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 写1清零寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {reg_name.lower()}_reg & ~{data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # Write1Set类型 - 写1置位对应位
        class Write1SetRegister(RegisterType):
            def __init__(self):
                super().__init__("Write1Set", "写1置位对应位，可读", True, True,
                              special_behaviors=["write_1_set"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 写1置位寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {reg_name.lower()}_reg | {data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # WriteOnce类型 - 只写一次寄存器
        class WriteOnceRegister(RegisterType):
            def __init__(self):
                super().__init__("WriteOnce", "只写一次寄存器，写入后不可再修改", True, True,
                              special_behaviors=["write_once"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 只写一次寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()} && !{reg_name.lower()}_written) begin
            {reg_name.lower()}_reg <= {data};
            {reg_name.lower()}_written <= 1'b1; // 设置写标志
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # Write1Pulse类型 - 写1产生一个周期的脉冲，然后自动清零
        class Write1PulseRegister(RegisterType):
            def __init__(self):
                super().__init__("Write1Pulse", "写1产生一个周期的脉冲，然后自动清零",
                              True, True, special_behaviors=["write_1_pulse"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 写1脉冲寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            // 如果数据位为1，生成脉冲
            {reg_name.lower()}_pulse <= {data} & {{({data_width}){{1'b1}}}};
            // 实际寄存器始终保持为0
            {reg_name.lower()}_reg <= {data_width}'d0;
        end else begin
            // 脉冲信号只维持一个周期
            {reg_name.lower()}_pulse <= {data_width}'d0;
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg; // 始终读到0
        end
                """
        
        # Write0Pulse类型 - 写0产生一个周期的脉冲，然后自动清零
        class Write0PulseRegister(RegisterType):
            def __init__(self):
                super().__init__("Write0Pulse", "写0产生一个周期的脉冲，然后自动清零",
                              True, True, special_behaviors=["write_0_pulse"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 写0脉冲寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            // 如果数据位为0，生成脉冲
            {reg_name.lower()}_pulse <= ~{data} & {{({data_width}){{1'b1}}}};
            // 实际寄存器始终保持为0
            {reg_name.lower()}_reg <= {data_width}'d0;
        end else begin
            // 脉冲信号只维持一个周期
            {reg_name.lower()}_pulse <= {data_width}'d0;
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg; // 始终读到0
        end
                """
        
        # LockField类型 - 锁定其他寄存器的修改
        class LockFieldRegister(RegisterType):
            def __init__(self):
                super().__init__("LockField", "锁定字段，用于控制其他寄存器的写保护",
                              True, True, special_behaviors=["lock_field"])
            
            def get_write_behavior(self, reg_name: str, data_width: int, 
                                 addr: str, data: str, enable: str) -> str:
                return f"""
        // 锁定字段寄存器
        if ({enable} && {addr} == ADDR_{reg_name.upper()}) begin
            {reg_name.lower()}_reg <= {data};
        end
                """
            
            def get_read_behavior(self, reg_name: str, data_width: int, 
                                addr: str, data: str) -> str:
                return f"""
        if ({addr} == ADDR_{reg_name.upper()}) begin
            {data} = {reg_name.lower()}_reg;
        end
                """
        
        # 注册所有寄存器类型
        self.register_type(ReadWriteRegister())
        self.register_type(ReadOnlyRegister())
        self.register_type(WriteOnlyRegister())
        self.register_type(ReadCleanRegister())
        self.register_type(Write1CleanRegister())
        self.register_type(Write1SetRegister())
        self.register_type(WriteOnceRegister())
        self.register_type(Write1PulseRegister())
        self.register_type(Write0PulseRegister())
        self.register_type(LockFieldRegister())
        
        # 可以继续添加更多类型...
    
    def register_type(self, reg_type: RegisterType) -> None:
        """
        注册寄存器类型
        
        参数:
            reg_type: 寄存器类型实例
        """
        self._types[reg_type.name] = reg_type
    
    def get_register_type(self, type_name: str) -> RegisterType:
        """
        获取寄存器类型
        
        参数:
            type_name: 类型名称
            
        返回:
            寄存器类型实例
        """
        if type_name not in self._types:
            raise ValueError(f"未知的寄存器类型: {type_name}")
        return self._types[type_name]
    
    def get_all_register_types(self) -> List[str]:
        """
        获取所有支持的寄存器类型名称
        
        返回:
            类型名称列表
        """
        return list(self._types.keys())


# 单例模式，全局寄存器类型管理器
_register_type_manager = None

def get_register_type_manager() -> RegisterTypeManager:
    """
    获取全局寄存器类型管理器实例
    
    返回:
        RegisterTypeManager实例
    """
    global _register_type_manager
    if _register_type_manager is None:
        _register_type_manager = RegisterTypeManager()
    return _register_type_manager 