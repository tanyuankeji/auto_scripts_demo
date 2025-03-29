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
    description="自动寄存器文件生成工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IC Design Tools Team",
    author_email="icdesign@email.com",
    packages=find_packages(exclude=["tests", "backup", "output", "examples.test", "examples.output"]),
    include_package_data=True,
    package_data={
        "autoregfile": [
            "templates/**/*.j2",
            "templates/**/*.md",
            "templates/**/*.txt",
            "templates/**/*.v",
            "templates/**/*.h",
        ],
    },
    entry_points={
        "console_scripts": [
            "autoregfile=autoregfile.regfile_gen:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "jinja2>=2.11.0",
        "pyyaml>=5.1.0",
        "pandas>=1.0.0",
        "openpyxl>=3.0.0",
    ],
) 