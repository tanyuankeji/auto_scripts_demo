# 贡献指南

感谢您考虑为 AutoRegFile 项目做出贡献！本文档将指导您如何参与项目开发。

## 开发环境设置

1. 克隆项目仓库：

```bash
git clone https://github.com/yourusername/autoregfile.git
cd autoregfile
```

2. 创建虚拟环境（可选但推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. 安装开发依赖：

```bash
pip install -e ".[dev]"
```

## 代码风格

本项目遵循以下编码规范：

- 使用 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 所有 Python 代码使用 4 空格缩进
- 所有公共函数、类和方法必须有文档字符串
- 使用类型注解提高代码可读性

我们使用 `flake8` 和 `pylint` 进行代码检查：

```bash
flake8 autoregfile
pylint autoregfile
```

## 提交流程

1. 创建功能分支：

```bash
git checkout -b feature/your-feature-name
```

2. 进行代码修改

3. 添加和提交更改：

```bash
git add .
git commit -m "feat: 添加新功能 X"
```

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 不影响代码含义的更改（空格、格式等）
- `refactor`: 既不修复错误也不添加功能的代码更改
- `perf`: 提高性能的代码更改
- `test`: 添加或修正测试
- `chore`: 对构建过程或辅助工具的更改

4. 推送到 GitHub：

```bash
git push origin feature/your-feature-name
```

5. 创建 Pull Request

## 测试

添加新功能或修复错误时，请确保添加相应的测试：

```bash
pytest tests/
```

测试覆盖率应达到 80% 以上：

```bash
pytest --cov=autoregfile tests/
```

## 项目结构

```
autoregfile/
├── autoregfile/          # 核心包
│   ├── core/             # 核心功能模块
│   ├── generators/       # 代码生成器
│   ├── parsers/          # 配置解析器
│   ├── templates/        # 模板文件
│   └── utils/            # 工具函数
├── docs/                 # 文档
├── examples/             # 示例
├── scripts/              # 脚本工具
├── tests/                # 测试文件
└── setup.py              # 包安装配置
```

添加新功能时，请遵循上述结构，并确保：

1. 将相关功能放在适当的模块中
2. 添加单元测试
3. 更新文档

## 文档

文档使用 Markdown 格式。添加新功能时，请更新相关文档：

- 更新 README.md 中的功能描述
- 在 docs/ 目录中添加详细文档
- 添加示例代码到 examples/ 目录

## 版本控制

我们使用 [Semantic Versioning](https://semver.org/)：

- MAJOR 版本：不兼容的 API 更改
- MINOR 版本：向后兼容的功能添加
- PATCH 版本：向后兼容的问题修复

## 问题报告

报告问题时，请包括：

1. 问题描述
2. 重现步骤
3. 预期行为
4. 实际行为
5. 环境信息（操作系统、Python 版本等）
6. 任何相关日志或错误信息

## 联系方式

如有任何问题，请通过以下方式联系：

- GitHub Issues
- 项目维护者邮箱：example@example.com

感谢您的贡献！ 