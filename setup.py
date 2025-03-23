"""
安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="autowire",
    version="2.0.0",
    author="ICProject Team",
    author_email="icproject@example.com",
    description="Verilog 自动线网声明工具",
    url="https://github.com/icproject/autowire",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'autowire=autowire.cli.main:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 