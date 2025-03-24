#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autoregfile包安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README作为长描述
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 获取版本号
about = {}
with open(os.path.join("autoregfile", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="autoregfile",
    version=about["__version__"],
    author="设计自动化团队",
    author_email="example@example.com",
    description="自动生成Verilog寄存器文件的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autoregfile",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "autoregfile": ["templates/**/*"],
    },
    entry_points={
        "console_scripts": [
            "regfile-gen=scripts.generate_regfile:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    python_requires=">=3.6",
    install_requires=[
        "jinja2>=2.11.0",
        "pyyaml>=5.1.0",
        "pandas>=1.0.0",
        "openpyxl>=3.0.0",
    ],
) 