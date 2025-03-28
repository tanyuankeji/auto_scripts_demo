# Verilog自动线网声明工具 (Auto Wire Generator)

自动检测Verilog/SystemVerilog代码中未声明的信号，并生成相应的wire声明。

pip install -e . --force-reinstall
autowire --config .\autowire\config\auto_wire_config.json .\autowire\rtl\i3c_regs.vS

## 主要特点

1. 保持信号的原始出现顺序
2. 自动推断信号位宽
3. 支持parameter定义的信号 
4. 多种输出模式（独立文件或追加到原文件）
5. 支持用户自定义排除匹配模式（通过命令行或配置文件）
6. 增强的模块实例化名称识别（支持常用前缀如u_、i_等）
7. 支持generate/endgenerate关键字
8. 支持Verilog数值常量（如1'h0, 8'b00101010等）
9. 支持多行注释和宏定义

## 安装方法

```bash
# 从源代码安装
pip install .

# 或者直接使用源代码
python -m autowire [参数]
```

## 使用方法

### 基本用法

```bash
# 基本用法：生成单独的wire声明文件
autowire my_design.v

# 自动检测位宽 
autowire --width my_design.v

# 应用默认位宽（支持多种格式）
autowire --default-width "[31:0]" my_design.v  # 直接使用指定位宽
autowire --default-width "32" my_design.v      # 自动转换为[31:0]格式

# 直接追加到原始文件
autowire --append my_design.v

# 指定输出目录
autowire --output-dir ./generated my_design.v

# 排除特定模式的信号（命令行方式）
autowire --exclude "temp_.*" "debug_.*" my_design.v

# 使用配置文件排除特定模式的信号
autowire --config ./config/auto_wire_config.json my_design.v

# 显示详细信息
autowire --verbose my_design.v

# 显示调试信息
autowire --debug my_design.v

# 显示详细帮助
autowire --help-detail
```

### 配置文件

配置文件为JSON格式，包含以下字段：

```json
{
  "exclude_patterns": [
    "temp_.*",
    "debug_.*", 
    "test_.*",
    ".*_reg",
    ".*_next"
  ],
  "default_width": "[7:0]",
  "output_format": "separate",
  "output_dir": "./output",
  "version": "2.0.0"
}
```

默认配置文件路径：`./config/auto_wire_config.json`

## 优势特点

1. **模块化设计**：清晰的代码结构，易于维护和扩展
2. **错误处理完善**：详细的错误信息和异常处理
3. **配置灵活**：支持命令行参数和配置文件
4. **性能优化**：高效的文件处理和信号分析
5. **多编码支持**：自动检测文件编码
6. **位宽推断增强**：更智能的信号位宽推断算法

## 许可证

MIT

可能不需要的文件:

1. autowire/src/auto_wire.py：  这个文件看起来是项目的旧版本代码，现在项目已经重构为使用 core、cli 和 config 模块。src 目录中的这个文件导入了新的模块结构，但似乎没有被其他代码引用，可以考虑删除整个 src 目录。

2. 重复的文档：  docs 目录中已经有了完整的文档，包括中英文的技术文档和用户手册。这些文档内容完整且互不重复，建议保留。

3. build 目录：  build 目录通常包含编译时生成的临时文件，这些文件可以安全删除，因为在需要时可以重新生成。

4. autowire.egg-info 目录：  这个目录是 Python 包安装时生成的元数据，通常可以在需要时重新生成，如果不需要维护包安装状态，可以考虑删除。

5. pycache_ 目录：  这些目录包含 Python 的字节码缓存文件，可以安全删除，在运行代码时会重新生成。

6. 其他脚本工具目录：  项目根目录中还包含 auto_testbench、autoregfile、autosgdc 等目录，这些看起来是其他独立的脚本工具。如果这些工具不是当前项目的一部分，可以根据需要决定是否保留。 

综上所述，可以考虑删除的文件：

1. autowire/src/ 目录：旧版本代码，现已不再使用  

2. build/ 目录：编译临时文件

3. autowire.egg-info/ 目录：包安装元数据，可以重新生成

4. autowire/__pycache__/ 目录：Python 字节码缓存
