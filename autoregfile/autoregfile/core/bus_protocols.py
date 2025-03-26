#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总线协议模块

定义不同总线协议的接口和信号。
"""

from typing import Dict, Any, List, Optional, Set
import os


class BusProtocol:
    """总线协议基类"""
    
    def __init__(self, name: str, description: str):
        """
        初始化总线协议
        
        参数:
            name: 协议名称
            description: 协议描述
        """
        self.name = name
        self.description = description
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """
        获取总线输入端口列表
        
        返回:
            输入端口列表，每个端口是一个字典，包含name, width, description等字段
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """
        获取总线输出端口列表
        
        返回:
            输出端口列表，每个端口是一个字典，包含name, width, description等字段
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def get_interface_template(self) -> str:
        """
        获取总线接口模板文件路径
        
        返回:
            模板文件路径
        """
        raise NotImplementedError("子类必须实现此方法")


class APBProtocol(BusProtocol):
    """AMBA APB协议"""
    
    def __init__(self):
        """初始化APB协议"""
        super().__init__("apb", "AMBA APB (Advanced Peripheral Bus) Protocol")
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """获取APB协议输入端口列表"""
        return [
            {"name": "paddr", "width": "addr_width", "description": "APB 地址信号"},
            {"name": "psel", "width": 1, "description": "APB 片选信号"},
            {"name": "penable", "width": 1, "description": "APB 使能信号"},
            {"name": "pwrite", "width": 1, "description": "APB 写使能信号 (1:写, 0:读)"},
            {"name": "pwdata", "width": "data_width", "description": "APB 写数据信号"}
        ]
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """获取APB协议输出端口列表"""
        return [
            {"name": "prdata", "width": "data_width", "description": "APB 读数据信号"},
            {"name": "pready", "width": 1, "description": "APB 就绪信号"},
            {"name": "pslverr", "width": 1, "description": "APB 从机错误信号"}
        ]
    
    def get_interface_template(self) -> str:
        """获取APB接口模板文件路径"""
        return "verilog/bus/apb.v.j2"


class AXILiteProtocol(BusProtocol):
    """AMBA AXI4-Lite协议"""
    
    def __init__(self):
        """初始化AXI-Lite协议"""
        super().__init__("axi_lite", "AMBA AXI4-Lite Protocol")
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """获取AXI-Lite协议输入端口列表"""
        return [
            # 写地址通道
            {"name": "s_axi_awaddr", "width": "addr_width", "description": "AXI4-Lite 写地址"},
            {"name": "s_axi_awprot", "width": 3, "description": "AXI4-Lite 写保护类型"},
            {"name": "s_axi_awvalid", "width": 1, "description": "AXI4-Lite 写地址有效信号"},
            
            # 写数据通道
            {"name": "s_axi_wdata", "width": "data_width", "description": "AXI4-Lite 写数据"},
            {"name": "s_axi_wstrb", "width": "data_width/8", "description": "AXI4-Lite 写数据字节选通"},
            {"name": "s_axi_wvalid", "width": 1, "description": "AXI4-Lite 写数据有效信号"},
            
            # 写响应通道
            {"name": "s_axi_bready", "width": 1, "description": "AXI4-Lite 写响应就绪信号"},
            
            # 读地址通道
            {"name": "s_axi_araddr", "width": "addr_width", "description": "AXI4-Lite 读地址"},
            {"name": "s_axi_arprot", "width": 3, "description": "AXI4-Lite 读保护类型"},
            {"name": "s_axi_arvalid", "width": 1, "description": "AXI4-Lite 读地址有效信号"},
            
            # 读数据通道
            {"name": "s_axi_rready", "width": 1, "description": "AXI4-Lite 读数据就绪信号"}
        ]
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """获取AXI-Lite协议输出端口列表"""
        return [
            # 写地址通道
            {"name": "s_axi_awready", "width": 1, "description": "AXI4-Lite 写地址就绪信号"},
            
            # 写数据通道
            {"name": "s_axi_wready", "width": 1, "description": "AXI4-Lite 写数据就绪信号"},
            
            # 写响应通道
            {"name": "s_axi_bresp", "width": 2, "description": "AXI4-Lite 写响应"},
            {"name": "s_axi_bvalid", "width": 1, "description": "AXI4-Lite 写响应有效信号"},
            
            # 读地址通道
            {"name": "s_axi_arready", "width": 1, "description": "AXI4-Lite 读地址就绪信号"},
            
            # 读数据通道
            {"name": "s_axi_rdata", "width": "data_width", "description": "AXI4-Lite 读数据"},
            {"name": "s_axi_rresp", "width": 2, "description": "AXI4-Lite 读响应"},
            {"name": "s_axi_rvalid", "width": 1, "description": "AXI4-Lite 读数据有效信号"}
        ]
    
    def get_interface_template(self) -> str:
        """获取AXI-Lite接口模板文件路径"""
        return "verilog/bus/axi_lite.v.j2"


class WishboneProtocol(BusProtocol):
    """Wishbone总线协议"""
    
    def __init__(self):
        """初始化Wishbone协议"""
        super().__init__("wishbone", "Wishbone B4 Protocol")
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """获取Wishbone协议输入端口列表"""
        return [
            {"name": "wb_adr_i", "width": "addr_width", "description": "Wishbone 地址输入"},
            {"name": "wb_dat_i", "width": "data_width", "description": "Wishbone 数据输入"},
            {"name": "wb_we_i", "width": 1, "description": "Wishbone 写使能输入"},
            {"name": "wb_sel_i", "width": "data_width/8", "description": "Wishbone 字节选择输入"},
            {"name": "wb_stb_i", "width": 1, "description": "Wishbone 选通输入"},
            {"name": "wb_cyc_i", "width": 1, "description": "Wishbone 周期输入"}
        ]
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """获取Wishbone协议输出端口列表"""
        return [
            {"name": "wb_dat_o", "width": "data_width", "description": "Wishbone 数据输出"},
            {"name": "wb_ack_o", "width": 1, "description": "Wishbone 应答输出"},
            {"name": "wb_err_o", "width": 1, "description": "Wishbone 错误输出"}
        ]
    
    def get_interface_template(self) -> str:
        """获取Wishbone接口模板文件路径"""
        return "verilog/bus/wishbone.v.j2"


class OCPProtocol(BusProtocol):
    """Open Core Protocol (OCP)"""
    
    def __init__(self):
        """初始化OCP协议"""
        super().__init__("ocp", "Open Core Protocol")
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """获取OCP协议输入端口列表"""
        return [
            {"name": "MAddr", "width": "addr_width", "description": "OCP 主地址"},
            {"name": "MCmd", "width": 3, "description": "OCP 主命令 (0:空闲, 1:写, 2:读)"},
            {"name": "MData", "width": "data_width", "description": "OCP 主写数据"},
            {"name": "MByteEn", "width": "data_width/8", "description": "OCP 主字节使能"},
            {"name": "MRespAccept", "width": 1, "description": "OCP 主响应接收"}
        ]
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """获取OCP协议输出端口列表"""
        return [
            {"name": "SData", "width": "data_width", "description": "OCP 从读数据"},
            {"name": "SResp", "width": 2, "description": "OCP 从响应 (0:空闲, 1:完成, 2:错误)"},
            {"name": "SCmdAccept", "width": 1, "description": "OCP 从命令接收"}
        ]
    
    def get_interface_template(self) -> str:
        """获取OCP接口模板文件路径"""
        return "verilog/bus/ocp.v.j2"


class CustomBusProtocol(BusProtocol):
    """自定义总线协议"""
    
    def __init__(self):
        """初始化自定义总线协议"""
        super().__init__("custom", "Custom Bus Protocol")
    
    def get_input_ports(self) -> List[Dict[str, Any]]:
        """获取自定义总线协议输入端口列表"""
        return [
            {"name": "addr", "width": "addr_width", "description": "地址输入"},
            {"name": "wdata", "width": "data_width", "description": "写数据输入"},
            {"name": "wr_en", "width": 1, "description": "写使能输入"},
            {"name": "rd_en", "width": 1, "description": "读使能输入"},
            {"name": "byte_en", "width": "data_width/8", "description": "字节使能输入"},
            {"name": "req", "width": 1, "description": "请求信号输入"}
        ]
    
    def get_output_ports(self) -> List[Dict[str, Any]]:
        """获取自定义总线协议输出端口列表"""
        return [
            {"name": "rdata", "width": "data_width", "description": "读数据输出"},
            {"name": "ack", "width": 1, "description": "应答信号输出"},
            {"name": "err", "width": 1, "description": "错误信号输出"}
        ]
    
    def get_interface_template(self) -> str:
        """获取自定义总线接口模板文件路径"""
        return "verilog/bus/custom.v.j2"


class BusProtocolManager:
    """总线协议管理器"""
    
    def __init__(self):
        """初始化总线协议管理器"""
        self.protocols = {}
        self._register_protocols()
    
    def _register_protocols(self):
        """注册内置总线协议"""
        self.register_protocol(APBProtocol())
        self.register_protocol(AXILiteProtocol())
        self.register_protocol(WishboneProtocol())
        self.register_protocol(OCPProtocol())
        self.register_protocol(CustomBusProtocol())
    
    def register_protocol(self, protocol: BusProtocol):
        """
        注册总线协议
        
        参数:
            protocol: 总线协议对象
        """
        self.protocols[protocol.name] = protocol
    
    def get_protocol(self, name: str) -> BusProtocol:
        """
        获取总线协议
        
        参数:
            name: 协议名称
            
        返回:
            总线协议对象
            
        异常:
            ValueError: 如果协议名称未知
        """
        if name.lower() in self.protocols:
            return self.protocols[name.lower()]
        
        # 如果找不到匹配的协议，尝试使用自定义协议作为后备选项
        if "custom" in self.protocols:
            print(f"警告: 未知的总线协议 '{name}'，使用自定义总线协议替代")
            return self.protocols["custom"]
        
        raise ValueError(f"未知的总线协议: {name}")
    
    def list_protocols(self) -> List[str]:
        """
        获取所有已注册的总线协议名称
        
        返回:
            协议名称列表
        """
        return list(self.protocols.keys())


_bus_protocol_manager = None

def get_bus_protocol_manager() -> BusProtocolManager:
    """
    获取全局总线协议管理器实例
    
    返回:
        总线协议管理器对象
    """
    global _bus_protocol_manager
    if _bus_protocol_manager is None:
        _bus_protocol_manager = BusProtocolManager()
    return _bus_protocol_manager 