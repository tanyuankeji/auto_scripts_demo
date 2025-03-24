#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Register type definition module

Defines the supported register types and their behavior characteristics.
"""

from typing import Dict, Any, List


class RegisterType:
    """Defines the base class for register types"""
    
    def __init__(self, name: str, description: str, write_behavior: str, read_behavior: str):
        """
        Initialize register type
        
        Parameters:
            name: Register type name
            description: Register type description
            write_behavior: Verilog code template for write behavior
            read_behavior: Verilog code template for read behavior
        """
        self.name = name  # Register type name
        self.description = description  # Register type description
        self.write_behavior = write_behavior  # Verilog code template for write behavior
        self.read_behavior = read_behavior  # Verilog code template for read behavior
    
    def get_write_behavior(self, reg_name: str, data_width: int, 
                           addr: str, data: str, enable: str) -> str:
        """
        Get Verilog code for write behavior
        
        Parameters:
            reg_name: Register name
            data_width: Data width
            addr: Address variable name
            data: Data variable name
            enable: Enable variable name
            
        Returns:
            Verilog code snippet
        """
        # Replace template variables
        code = self.write_behavior.replace("{reg_name}", reg_name)
        code = code.replace("{data_width}", str(data_width))
        code = code.replace("{addr}", addr)
        code = code.replace("{data}", data)
        code = code.replace("{enable}", enable)
        return code
    
    def get_read_behavior(self, reg_name: str, data_width: int, 
                          addr: str, data: str) -> str:
        """
        Get Verilog code for read behavior
        
        Parameters:
            reg_name: Register name
            data_width: Data width
            addr: Address variable name
            data: Data variable name
            
        Returns:
            Verilog code snippet
        """
        # Replace template variables
        code = self.read_behavior.replace("{reg_name}", reg_name)
        code = code.replace("{data_width}", str(data_width))
        code = code.replace("{addr}", addr)
        code = code.replace("{data}", data)
        return code


class RegisterTypeManager:
    """Register type manager"""
    
    def __init__(self):
        """Initialize register type manager"""
        self.register_types = {}
        self._init_register_types()
    
    def _init_register_types(self):
        """Initialize supported register types"""
        
        # Null type register (cannot be read or written)
        self.register_types["Null"] = RegisterType(
            "Null",
            "Empty register, cannot be read or written",
            "// {reg_name} is a Null type register, ignores write operations\n",
            "// {reg_name} is a Null type register, returns 0 when read\n        {data} = {data_width}'d0;\n"
        )
        
        # ReadWrite type register (read-write)
        self.register_types["ReadWrite"] = RegisterType(
            "ReadWrite",
            "Standard read-write register",
            "// {reg_name} is a ReadWrite type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a ReadWrite type register\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # ReadOnly type register (read-only)
        self.register_types["ReadOnly"] = RegisterType(
            "ReadOnly",
            "Read-only register, write operations are ignored",
            "// {reg_name} is a ReadOnly type register, ignores write operations\n",
            "// {reg_name} is a ReadOnly type register\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # ReadClean type register (read-clean)
        self.register_types["ReadClean"] = RegisterType(
            "ReadClean",
            "Register that clears itself after being read",
            "// {reg_name} is a ReadClean type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a ReadClean type register, clears itself after being read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // Clear after read\n        end\n"
        )
        
        # ReadSet type register (read-set)
        self.register_types["ReadSet"] = RegisterType(
            "ReadSet",
            "Register that sets itself to 1 after being read",
            "// {reg_name} is a ReadSet type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a ReadSet type register, sets itself to 1 after being read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'h{data_width}'hFFFFFFFF; // Set to 1 after read\n        end\n"
        )
        
        # WriteReadClean type register
        self.register_types["WriteReadClean"] = RegisterType(
            "WriteReadClean",
            "Writable, clears itself after being read",
            "// {reg_name} is a WriteReadClean type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a WriteReadClean type register, clears itself after being read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'d0; // Clear after read\n        end\n"
        )
        
        # WriteReadSet type register
        self.register_types["WriteReadSet"] = RegisterType(
            "WriteReadSet",
            "Writable, sets itself to 1 after being read",
            "// {reg_name} is a WriteReadSet type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a WriteReadSet type register, sets itself to 1 after being read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // Set to 1 after read\n        end\n"
        )
        
        # WriteOnly type register
        self.register_types["WriteOnly"] = RegisterType(
            "WriteOnly",
            "Write-only register, read operations return 0",
            "// {reg_name} is a WriteOnly type register\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n        end\n",
            "// {reg_name} is a WriteOnly type register, returns 0 when read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteOnlyClean type register
        self.register_types["WriteOnlyClean"] = RegisterType(
            "WriteOnlyClean",
            "Write-only register, clears itself after being written",
            "// {reg_name} is a WriteOnlyClean type register, clears itself after being written\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_reg <= {data_width}'d0; // Clear after write\n        end\n",
            "// {reg_name} is a WriteOnlyClean type register, returns 0 when read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteOnlySet type register
        self.register_types["WriteOnlySet"] = RegisterType(
            "WriteOnlySet",
            "Write-only register, sets itself to 1 after being written",
            "// {reg_name} is a WriteOnlySet type register, sets itself to 1 after being written\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {data};\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // Set to 1 after write\n        end\n",
            "// {reg_name} is a WriteOnlySet type register, returns 0 when read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {data_width}'d0;\n        end\n"
        )
        
        # WriteClean type register
        self.register_types["WriteClean"] = RegisterType(
            "WriteClean",
            "Writing 0 clears the corresponding bit, readable",
            "// {reg_name} is a WriteClean type register, writing 0 clears the corresponding bit\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~({data} & {data});\n        end\n",
            "// {reg_name} is a WriteClean type register\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # WriteCleanReadSet type register
        self.register_types["WriteCleanReadSet"] = RegisterType(
            "WriteCleanReadSet",
            "Writing 0 clears the corresponding bit, sets itself to 1 after being read",
            "// {reg_name} is a WriteCleanReadSet type register, writing 0 clears the corresponding bit\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~({data} & {data});\n        end\n",
            "// {reg_name} is a WriteCleanReadSet type register, sets itself to 1 after being read\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n            {reg_name}_reg <= {data_width}'hFFFFFFFF; // Set to 1 after read\n        end\n"
        )
        
        # Write1Clean type register
        self.register_types["Write1Clean"] = RegisterType(
            "Write1Clean",
            "Writing 1 clears the corresponding bit, readable",
            "// {reg_name} is a Write1Clean type register, writing 1 clears the corresponding bit\n        if ({enable} && {addr} == ADDR_{reg_name}) begin\n            {reg_name}_reg <= {reg_name}_reg & ~{data};\n        end\n",
            "// {reg_name} is a Write1Clean type register\n        if ({addr} == ADDR_{reg_name}) begin\n            {data} = {reg_name}_reg;\n        end\n"
        )
        
        # Add more register types...
        # Only a few types are implemented here, the complete version should implement all types listed in the README
        
    def get_register_type(self, type_name: str) -> RegisterType:
        """Get the register type with the specified name"""
        if type_name not in self.register_types:
            raise ValueError(f"Unsupported register type: {type_name}")
        return self.register_types[type_name]
    
    def get_all_register_types(self) -> List[str]:
        """Get the names of all supported register types"""
        return list(self.register_types.keys())


if __name__ == "__main__":
    # Test code
    manager = RegisterTypeManager()
    print("Supported register types:")
    for reg_type in manager.get_all_register_types():
        reg_obj = manager.get_register_type(reg_type)
        print(f"- {reg_type}: {reg_obj.description}")
    
    # Test code generation
    test_reg = manager.get_register_type("ReadWrite")
    write_code = test_reg.get_write_behavior("TEST_REG", 32, "wr_addr", "wr_data", "wr_en")
    read_code = test_reg.get_read_behavior("TEST_REG", 32, "rd_addr", "rd_data")
    print("\nWrite behavior code:")
    print(write_code)
    print("\nRead behavior code:")
    print(read_code) 