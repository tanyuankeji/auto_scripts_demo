#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模板管理器单元测试

测试模板管理器的各项功能，包括模板查找、渲染和目录管理。
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from autoregfile.core.template_manager import get_template_manager, TemplateManager


class TestTemplateManager(unittest.TestCase):
    """测试模板管理器类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建临时测试目录
        self.test_dir = tempfile.mkdtemp()
        
        # 创建测试模板目录和文件
        self.template_dir = os.path.join(self.test_dir, 'templates')
        os.makedirs(self.template_dir, exist_ok=True)
        
        # 创建测试模板文件
        self.test_template = os.path.join(self.template_dir, 'test.j2')
        with open(self.test_template, 'w', encoding='utf-8') as f:
            f.write('Hello, {{ name }}!')
        
        # 初始化模板管理器
        self.template_manager = TemplateManager([self.template_dir])
    
    def tearDown(self):
        """测试后清理工作"""
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_find_template(self):
        """测试查找模板功能"""
        # 测试找到存在的模板
        found_path = self.template_manager.find_template('test.j2')
        self.assertIsNotNone(found_path)
        self.assertEqual(found_path, self.test_template)
        
        # 测试找不到不存在的模板
        not_found_path = self.template_manager.find_template('nonexistent.j2')
        self.assertIsNone(not_found_path)
    
    def test_render_template(self):
        """测试渲染模板功能"""
        # 渲染模板
        context = {'name': 'World'}
        rendered = self.template_manager.render_template('test.j2', context)
        
        # 检查渲染结果
        self.assertEqual(rendered, 'Hello, World!')
    
    def test_add_template_dirs(self):
        """测试添加模板目录功能"""
        # 创建另一个模板目录
        another_dir = os.path.join(self.test_dir, 'another_templates')
        os.makedirs(another_dir, exist_ok=True)
        
        # 在新目录中创建模板
        another_template = os.path.join(another_dir, 'another.j2')
        with open(another_template, 'w', encoding='utf-8') as f:
            f.write('Another {{ value }}!')
        
        # 添加新目录到模板管理器
        self.template_manager.add_template_dirs([another_dir])
        
        # 查找并渲染新目录中的模板
        found_path = self.template_manager.find_template('another.j2')
        self.assertIsNotNone(found_path)
        self.assertEqual(found_path, another_template)
        
        rendered = self.template_manager.render_template('another.j2', {'value': 'template'})
        self.assertEqual(rendered, 'Another template!')
    
    def test_singleton_instance(self):
        """测试单例模式功能"""
        # 获取两个实例，应该是同一个对象
        manager1 = get_template_manager([self.template_dir])
        manager2 = get_template_manager()
        
        self.assertIs(manager1, manager2)
        
        # 添加新目录后应更新现有实例
        another_dir = os.path.join(self.test_dir, 'more_templates')
        os.makedirs(another_dir, exist_ok=True)
        
        manager3 = get_template_manager([another_dir])
        self.assertIs(manager1, manager3)
        
        # 检查目录是否已添加
        self.assertIn(another_dir, manager1.user_template_dirs)


if __name__ == '__main__':
    unittest.main() 