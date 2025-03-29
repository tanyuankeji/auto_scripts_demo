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
            config_source: 配置源（YAML文件路径）
            
        返回:
            解析后的配置字典
        """
        if not os.path.isfile(config_source):
            raise ValueError(f"文件不存在: {config_source}")
        
        _, ext = os.path.splitext(config_source)
        if ext.lower() not in ['.yml', '.yaml']:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        # 尝试使用不同的编码打开文件
        try:
            # 首先尝试使用UTF-8编码
            with open(config_source, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试其他编码
            try:
                print("UTF-8编码读取失败，尝试使用GBK编码...")
                with open(config_source, 'r', encoding='gbk') as f:
                    config = yaml.safe_load(f)
            except UnicodeDecodeError:
                try:
                    print("GBK编码读取失败，尝试使用CP936编码...")
                    with open(config_source, 'r', encoding='cp936') as f:
                        config = yaml.safe_load(f)
                except UnicodeDecodeError:
                    try:
                        print("CP936编码读取失败，尝试使用latin-1编码...")
                        with open(config_source, 'r', encoding='latin-1') as f:
                            config = yaml.safe_load(f)
                    except Exception as e:
                        raise ValueError(f"无法解析YAML文件: {str(e)}，请检查文件编码")
        except yaml.YAMLError as e:
            raise ValueError(f"无效的YAML格式: {str(e)}")
        except Exception as e:
            raise ValueError(f"解析YAML文件时出错: {str(e)}")
        
        return config


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