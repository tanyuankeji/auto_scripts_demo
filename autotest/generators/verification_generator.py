#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
验证环境生成器模块

基于解析和生成的testbench，创建完整的验证环境
支持复制模板文件、生成配置文件等
"""

import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VerificationGenerator:
    """验证环境生成器类"""
    
    def __init__(self, top_module, parser, testbench_content, 
                vcs_demo_dir, output_dir, 
                is_verification=False, is_demo=False,
                tb_name="testbench", rel_path=".", ver_path=None):
        """
        初始化验证环境生成器
        
        参数:
            top_module: 顶层模块名
            parser: VerilogParser对象实例
            testbench_content: 生成的testbench内容
            vcs_demo_dir: vcs_demo模板目录
            output_dir: 输出目录
            is_verification: 是否生成验证环境
            is_demo: 是否demo模式
            tb_name: testbench名称前缀，默认为"testbench"
            rel_path: 输出文件的相对路径，默认为"."
            ver_path: 验证环境的生成路径，默认与output_dir相同
        """
        self.top_module = top_module
        self.parser = parser
        self.testbench_content = testbench_content
        self.vcs_demo_dir = Path(vcs_demo_dir)
        self.output_dir = Path(output_dir)
        self.is_verification = is_verification
        self.is_demo = is_demo
        self.tb_name = tb_name
        self.rel_path = rel_path
        self.ver_path = Path(ver_path) if ver_path else self.output_dir
        
        # 设置验证环境目录
        if is_demo:
            self.verification_dir = self.ver_path / "demo_verification"
        else:
            self.verification_dir = self.ver_path / f"{self.top_module}_verification"
        
        # 创建相对路径目录（用于生成简化版testbench）
        self.rel_dir = Path(self.output_dir) / self.rel_path
        os.makedirs(self.rel_dir, exist_ok=True)
        
        # 如果需要验证环境，则创建验证环境目录
        if self.is_verification or self.is_demo:
            self._create_verification_directories()
    
    def _create_verification_directories(self):
        """创建验证环境目录结构"""
        # 创建验证环境主目录
        os.makedirs(self.verification_dir, exist_ok=True)
        
        # 创建子目录
        for subdir in ["top", "ver", "sim", "cfg"]:
            os.makedirs(self.verification_dir / subdir, exist_ok=True)
    
    def generate(self):
        """生成testbench和验证环境"""
        # 始终生成简化版testbench
        self._generate_simple_testbench()
        
        # 如果不需要验证环境，到此结束
        if not self.is_verification and not self.is_demo:
            logger.info("生成testbench完成！")
            return
            
        # 以下为验证环境生成代码
        # 复制模板文件
        self._copy_template_files()
        
        # 生成verification_dir中的testbench文件
        self._generate_verification_testbench()
        
        # 生成filelist文件
        self._generate_filelist()
        
        # 生成包文件 (如果需要验证环境)
        if self.is_verification and self.parser:
            self._generate_package_file()
            
        # 打印生成信息
        logger.info("生成验证环境完成！")
        logger.info(f"请进入 {self.verification_dir}/sim 目录运行仿真")
    
    def _copy_template_files(self):
        """复制模板文件"""
        if os.path.exists(self.vcs_demo_dir):
            # 复制所有vcs_demo文件到验证环境目录
            for src_path in self.vcs_demo_dir.glob("**/*"):
                if src_path.is_file():
                    # 计算相对路径并创建目标路径
                    rel_path = src_path.relative_to(self.vcs_demo_dir)
                    dst_path = self.verification_dir / rel_path
                    
                    # 确保目标目录存在
                    os.makedirs(dst_path.parent, exist_ok=True)
                    
                    # 复制文件
                    shutil.copy2(src_path, dst_path)
                    
                    # 对脚本文件添加执行权限
                    if src_path.suffix == ".pl" or src_path.suffix == ".sh":
                        os.chmod(dst_path, 0o755)
        else:
            logger.warning(f"模板目录不存在: {self.vcs_demo_dir}")
            # 创建最小的Makefile
            with open(self.verification_dir / "sim" / "Makefile", "w") as f:
                f.write("include ../cfg/cfg.mk\n")
    
    def _generate_verification_testbench(self):
        """在验证环境目录中生成testbench文件"""
        # 生成testbench文件
        tb_filename = f"{self.tb_name}_{self.top_module}.sv"
        try:
            # 使用带BOM的UTF-8编码
            with open(self.verification_dir / "top" / tb_filename, "w", encoding="utf-8-sig") as f:
                f.write(self.testbench_content)
                
            # 为兼容旧代码，也创建一个名为testbench.sv的文件
            with open(self.verification_dir / "top" / "testbench.sv", "w", encoding="utf-8-sig") as f:
                f.write(self.testbench_content)
            
            logger.info(f"生成验证环境testbench: {self.verification_dir}/top/{tb_filename}")
        except Exception as e:
            logger.error(f"生成验证环境testbench失败: {str(e)}")
    
    def _generate_filelist(self):
        """生成filelist文件"""
        from generators.testbench_generator import TestbenchGenerator
        
        # 创建TestbenchGenerator实例来生成filelist
        if self.is_demo:
            filelist = "+libext+.v+.sv\n../top/testbench.sv"
        else:
            tb_generator = TestbenchGenerator(self.parser, self.top_module, "")
            filelist = tb_generator.generate_filelist(self.is_verification)
        
        try:
            with open(self.verification_dir / "cfg" / "tb.f", "w", encoding="utf-8-sig") as f:
                f.write(filelist)
            logger.info(f"生成filelist文件: {self.verification_dir}/cfg/tb.f")
        except Exception as e:
            logger.error(f"生成filelist文件失败: {str(e)}")
    
    def _generate_package_file(self):
        """生成包文件"""
        from generators.testbench_generator import TestbenchGenerator
        
        # 创建TestbenchGenerator实例来生成包文件
        tb_generator = TestbenchGenerator(self.parser, self.top_module, "")
        package_content = tb_generator.generate_package()
        
        try:
            with open(self.verification_dir / "ver" / f"{self.top_module}_pkg.sv", "w", encoding="utf-8-sig") as f:
                f.write(package_content)
            logger.info(f"生成包文件: {self.verification_dir}/ver/{self.top_module}_pkg.sv")
        except Exception as e:
            logger.error(f"生成包文件失败: {str(e)}")
            
    def _generate_simple_testbench(self):
        """在指定的相对路径生成简化版的testbench.v文件"""
        # 生成带模块名的testbench文件名，无论tb_name是什么
        tb_filename = f"{self.tb_name}_{self.top_module}.v"
        simple_tb_path = self.rel_dir / tb_filename
        
        # 提取原始testbench中的必要部分
        try:
            # 简化的testbench内容
            simple_content = f"""// 简化版testbench - 由autotest工具自动生成
// 适用于模块: {self.top_module}

{self.testbench_content}
"""
            if self.is_verification or self.is_demo:
                simple_content = f"""// 简化版testbench - 由autotest工具自动生成
// 适用于模块: {self.top_module}
// 完整版路径: {self.verification_dir}/top/{self.tb_name}_{self.top_module}.sv

{self.testbench_content}
"""
            
            # 使用带BOM的UTF-8编码写入文件
            with open(simple_tb_path, "w", encoding="utf-8-sig") as f:
                f.write(simple_content)
                
            logger.info(f"生成简化版testbench: {simple_tb_path}")
        except Exception as e:
            logger.error(f"生成简化版testbench失败: {str(e)}") 