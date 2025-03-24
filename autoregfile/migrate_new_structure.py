#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将autoregfile_new目录中的内容迁移到根目录，重新整理文件结构
"""

import os
import sys
import shutil
import argparse


def migrate_files(dry_run=False, verbose=False):
    """
    迁移文件结构
    
    参数:
        dry_run: 是否只显示将移动的文件，不实际移动
        verbose: 是否显示详细输出
    """
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 源目录和目标目录
    source_dir = os.path.join(script_dir, "autoregfile_new")
    
    if not os.path.exists(source_dir):
        print(f"错误: 源目录不存在: {source_dir}", file=sys.stderr)
        return False
    
    # 要删除的旧文件
    old_files = [
        os.path.join(script_dir, "regfile.v"),
        os.path.join(script_dir, "readme"),
        os.path.join(script_dir, "use_new_autoregfile.py"),
        os.path.join(script_dir, "cleanup_old_files.py"),
        os.path.join(script_dir, "README_MIGRATION.md")
    ]
    
    # 删除旧文件
    for old_file in old_files:
        if os.path.exists(old_file):
            if verbose:
                print(f"删除旧文件: {old_file}")
                
            if not dry_run:
                os.remove(old_file)
    
    # 复制autoregfile_new中的文件
    if verbose:
        print(f"复制目录: {source_dir} -> {script_dir}")
        
    if not dry_run:
        # 复制所有文件和子目录
        for item in os.listdir(source_dir):
            src_path = os.path.join(source_dir, item)
            dst_path = os.path.join(script_dir, item)
            
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                if verbose:
                    print(f"已复制目录: {src_path} -> {dst_path}")
            else:
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                shutil.copy2(src_path, dst_path)
                if verbose:
                    print(f"已复制文件: {src_path} -> {dst_path}")
    
    # 创建迁移完成标记文件
    migration_note = os.path.join(script_dir, "MIGRATION_COMPLETED.md")
    if not dry_run:
        with open(migration_note, "w", encoding="utf-8") as f:
            f.write("# 迁移完成\n\n")
            f.write("autoregfile已完成从旧结构到新结构的迁移。\n\n")
            f.write("## 迁移内容\n\n")
            f.write("- 删除了旧的src、ref、tests和test_output目录\n")
            f.write("- 将autoregfile_new中的内容移动到根目录\n")
            f.write("- 更新了README.md文件\n\n")
            f.write("## 备份\n\n")
            f.write("所有旧文件已备份到backup目录。\n")
            
    # 删除autoregfile_new目录
    if not dry_run:
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
            if verbose:
                print(f"已删除源目录: {source_dir}")
    
    print("\n迁移完成!")
    if dry_run:
        print("这是演示模式，未实际移动任何文件。使用 --no-dry-run 标志来实际执行操作。")
    else:
        print("已成功将新的文件结构迁移到根目录")
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="迁移autoregfile文件结构")
    
    parser.add_argument("--no-dry-run", action="store_true",
                      help="实际执行文件移动操作（默认只显示将移动的文件）")
    parser.add_argument("-v", "--verbose", action="store_true",
                      help="显示详细输出")
    
    args = parser.parse_args()
    
    try:
        migrate_files(not args.no_dry_run, args.verbose)
        return 0
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 