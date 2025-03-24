#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON格式配置解析器

解析JSON格式的寄存器配置文件。
"""

import os
import json
from typing import Dict, Any

from .base_parser import ConfigParser


class JsonParser(ConfigParser):
    """JSON格式配置解析器"""
    
    @staticmethod
    def parse(config_source: str) -> Dict[str, Any]:
        """
        解析JSON格式的配置
        
        参数:
            config_source: 配置源（文件路径或JSON字符串）
            
        返回:
            解析后的配置字典
        """
        # 确定是文件路径还是JSON字符串
        if os.path.isfile(config_source):
            with open(config_source, 'r', encoding='utf-8') as f:
                config_str = f.read()
        else:
            config_str = config_source
        
        try:
            # 解析JSON
            config = json.loads(config_str)
            
            # 验证配置
            return ConfigParser.validate_config(config)
        except json.JSONDecodeError as e:
            raise ValueError(f"无效的JSON格式: {str(e)}")
        except Exception as e:
            raise ValueError(f"解析JSON配置失败: {str(e)}")


# 测试代码
if __name__ == "__main__":
    # 从字符串解析
    json_str = """
    {
        "module_name": "test_regfile",
        "registers": [
            {
                "name": "CTRL_REG",
                "address": "0x00",
                "type": "ReadWrite"
            }
        ]
    }
    """
    
    parser = JsonParser()
    config = parser.parse(json_str)
    print("从字符串解析的配置:")
    print(json.dumps(config, indent=2)) 