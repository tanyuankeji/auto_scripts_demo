#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具模块

提供文件操作相关的实用函数，如路径查找、模板加载等。
"""

import os
import shutil
import tempfile
from typing import List, Optional, Tuple, Set, Union


def find_file(filename: str, search_paths: List[str], file_extensions: Optional[List[str]] = None) -> Optional[str]:
    """
    在指定路径列表中查找文件
    
    Args:
        filename: 要查找的文件名
        search_paths: 要搜索的路径列表
        file_extensions: 可选的文件扩展名列表（如果未指定扩展名）
        
    Returns:
        Optional[str]: 找到的文件的完整路径，未找到则返回None
    """
    # 如果提供了扩展名，确保它们都以.开头
    if file_extensions:
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in file_extensions]
    else:
        extensions = ['']  # 空字符串表示不添加扩展名
    
    # 规范化文件名，移除任何扩展名（以便我们可以尝试提供的扩展名）
    base_filename = os.path.splitext(filename)[0]
    
    # 检查文件是否已经包含扩展名
    has_extension = os.path.splitext(filename)[1] != ''
    
    # 如果文件已有扩展名且未指定扩展名列表，则只查找完整文件名
    if has_extension and not file_extensions:
        for path in search_paths:
            full_path = os.path.join(path, filename)
            if os.path.isfile(full_path):
                return full_path
        return None
    
    # 尝试每个扩展名
    for path in search_paths:
        for ext in extensions:
            if has_extension and ext:
                # 如果文件名已有扩展名，且要尝试的扩展名不为空，跳过
                continue
                
            full_path = os.path.join(path, f"{base_filename}{ext}")
            if os.path.isfile(full_path):
                return full_path
    
    return None


def ensure_dir_exists(directory: str) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
        
    Returns:
        bool: 操作是否成功
    """
    if not directory:
        return False
        
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False


def find_all_files(directory: str, extensions: List[str] = None, recursive: bool = True) -> List[str]:
    """
    查找目录中所有指定扩展名的文件
    
    Args:
        directory: 要搜索的目录
        extensions: 文件扩展名列表，如 ['.txt', '.md']
        recursive: 是否递归搜索子目录
        
    Returns:
        List[str]: 找到的文件的完整路径列表
    """
    result = []
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return result
    
    # 标准化扩展名格式
    if extensions:
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        # 过滤文件
        for file in files:
            # 如果指定了扩展名，检查文件是否匹配
            if extensions:
                ext = os.path.splitext(file)[1].lower()
                if ext not in extensions:
                    continue
            
            # 将文件添加到结果列表
            result.append(os.path.join(root, file))
        
        # 如果不递归搜索，跳出循环
        if not recursive:
            break
    
    return result


def copy_files(source_files: List[str], destination_dir: str, create_missing_dirs: bool = True) -> List[str]:
    """
    将文件复制到目标目录
    
    Args:
        source_files: 源文件路径列表
        destination_dir: 目标目录
        create_missing_dirs: 是否创建缺失的目录结构
        
    Returns:
        List[str]: 成功复制的文件的目标路径列表
    """
    if not source_files:
        return []
    
    # 确保目标目录存在
    if create_missing_dirs:
        ensure_dir_exists(destination_dir)
    elif not os.path.exists(destination_dir):
        return []
    
    copied_files = []
    
    for src_file in source_files:
        if os.path.isfile(src_file):
            # 获取仅文件名
            filename = os.path.basename(src_file)
            dest_file = os.path.join(destination_dir, filename)
            
            try:
                shutil.copy2(src_file, dest_file)
                copied_files.append(dest_file)
            except Exception:
                continue
    
    return copied_files


def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        Optional[str]: 文件内容，读取失败返回None
    """
    if not os.path.isfile(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception:
        try:
            # 尝试使用二进制模式读取
            with open(file_path, 'rb') as f:
                return f.read().decode(encoding, errors='replace')
        except Exception:
            return None


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    写入内容到文件
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
        encoding: 文件编码
        
    Returns:
        bool: 写入是否成功
    """
    # 确保目录存在
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception:
            return False
    
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception:
        return False


def safe_write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    安全地写入内容到文件（先写入临时文件，然后重命名）
    
    这种方法有助于防止在写入过程中发生错误导致文件损坏。
    
    Args:
        file_path: 目标文件路径
        content: 要写入的内容
        encoding: 文件编码
        
    Returns:
        bool: 写入是否成功
    """
    # 确保目录存在
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception:
            return False
    
    try:
        # 创建临时文件
        fd, temp_path = tempfile.mkstemp(dir=directory)
        os.close(fd)
        
        # 写入内容到临时文件
        with open(temp_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        # 如果目标文件已存在，备份它
        if os.path.exists(file_path):
            backup_path = f"{file_path}.bak"
            try:
                os.replace(file_path, backup_path)
            except Exception:
                # 如果无法重命名，直接删除
                os.remove(file_path)
        
        # 重命名临时文件为目标文件
        os.replace(temp_path, file_path)
        
        return True
    except Exception:
        # 清理临时文件
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return False


def get_file_modification_time(file_path: str) -> Optional[float]:
    """
    获取文件的最后修改时间戳
    
    Args:
        file_path: 文件路径
        
    Returns:
        Optional[float]: 最后修改时间戳，获取失败返回None
    """
    if not os.path.isfile(file_path):
        return None
    
    try:
        return os.path.getmtime(file_path)
    except Exception:
        return None


def is_file_newer_than(file_path: str, reference_time: float) -> bool:
    """
    检查文件是否比给定时间更新
    
    Args:
        file_path: 文件路径
        reference_time: 参考时间戳
        
    Returns:
        bool: 文件是否比参考时间更新
    """
    mod_time = get_file_modification_time(file_path)
    if mod_time is None:
        return False
    
    return mod_time > reference_time


def get_relative_path(path: str, base_dir: str) -> str:
    """
    获取相对于基础目录的路径
    
    Args:
        path: 要转换的路径
        base_dir: 基础目录
        
    Returns:
        str: 相对路径
    """
    # 转换为绝对路径
    abs_path = os.path.abspath(path)
    abs_base = os.path.abspath(base_dir)
    
    # 获取相对路径
    try:
        return os.path.relpath(abs_path, abs_base)
    except Exception:
        # 如果无法获取相对路径（例如，在不同驱动器上），返回原始路径
        return path


def normalize_path(path: str) -> str:
    """
    规范化路径（统一分隔符，移除多余分隔符）
    
    Args:
        path: 要规范化的路径
        
    Returns:
        str: 规范化后的路径
    """
    if not path:
        return ""
    
    # 替换Windows路径分隔符为Unix风格
    normalized = path.replace('\\', '/')
    
    # 移除尾部分隔符
    if normalized.endswith('/'):
        normalized = normalized[:-1]
    
    return normalized


if __name__ == "__main__":
    # 测试代码
    print("当前工作目录:", os.getcwd())
    
    # 测试文件查找
    test_paths = ['.', './docs', './examples']
    found = find_file("README.md", test_paths)
    print(f"找到README.md: {found}")
    
    # 测试目录创建
    test_dir = "./test_dir"
    print(f"创建目录: {test_dir}, 结果:", ensure_dir_exists(test_dir))
    
    # 测试文件查找
    all_py_files = find_all_files(".", [".py"])
    print(f"找到的Python文件数量: {len(all_py_files)}")
    if all_py_files:
        print("前5个Python文件:")
        for file in all_py_files[:5]:
            print(f"  {file}")
    
    # 测试路径规范化
    test_path = "dir1\\dir2/dir3\\"
    print(f"规范化路径: {test_path} -> {normalize_path(test_path)}")
    
    # 清理测试目录
    if os.path.exists(test_dir):
        os.rmdir(test_dir) 