#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML格式配置解析器

解析YAML格式的寄存器配置文件。
"""

import os
import yaml
from typing import Dict, Any

from .base_parser import ConfigParser


class YamlParser(ConfigParser):
    """YAML格式配置解析器"""
    
    @staticmethod
    def parse(config_source: str) -> Dict[str, Any]:
        """
        解析YAML格式的配置
        
        参数:
            config_source: 配置源（文件路径或YAML字符串）
            
        返回:
            解析后的配置字典
        """
        # 确定是文件路径还是YAML字符串
        if os.path.isfile(config_source):
            with open(config_source, 'r', encoding='utf-8') as f:
                config_str = f.read()
        else:
            config_str = config_source
        
        try:
            # 解析YAML
            config = yaml.safe_load(config_str)
            
            # 验证配置
            return ConfigParser.validate_config(config)
        except yaml.YAMLError as e:
            raise ValueError(f"无效的YAML格式: {str(e)}")
        except Exception as e:
            raise ValueError(f"解析YAML配置失败: {str(e)}")


# 测试代码
if __name__ == "__main__":
    # 从字符串解析
    yaml_str = """
    module_name: test_regfile
    registers:
      - name: CTRL_REG
        address: 0x00
        type: ReadWrite
    """
    
    parser = YamlParser()
    config = parser.parse(yaml_str)
    print("从字符串解析的配置:")
    import json
    print(json.dumps(config, indent=2)) 