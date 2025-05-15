import argparse
import sys
from pathlib import Path
from datetime import datetime


def create_directory_structure(project_name: str, project_path: Path) -> None:
    """创建项目目录结构"""
    # 创建主要目录
    (project_path / "src" / project_name).mkdir(parents=True, exist_ok=True)
    (project_path / "tests").mkdir(parents=True, exist_ok=True)
    (project_path / "docs").mkdir(parents=True, exist_ok=True)

    # 创建基本文件
    (project_path / "src" / project_name / "__init__.py").write_text(f'''"""
{project_name} - 一个使用 create-uv-project 创建的项目
"""

__version__ = "0.1.0"
''')

    # 创建 main.py
    (project_path / "src" / project_name / "main.py").write_text('''"""
主程序入口
"""
import sys


def main():
    """主函数"""
    print("项目启动成功！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')

    # 创建测试文件
    (project_path / "tests" / "__init__.py").touch()
    (project_path / "tests" / "test_main.py").write_text(f'''"""
测试主程序功能
"""
import pytest
from {project_name}.main import main


def test_main():
    """测试主函数"""
    assert main() == 0
''')

    # 创建 pyproject.toml
    (project_path / "pyproject.toml").write_text(f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.8"
license = "MIT"
authors = [
    {{ name = "Your Name", email = "your.email@example.com" }}
]
dependencies = []

[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]
dev = [
    "black>=23.0",
    "ruff>=0.0.290",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
package = true

[project.scripts]
{project_name} = "{project_name}.main:main"

[tool.pytest.ini_options]
addopts = "-ra -q --cov={project_name}"
testpaths = ["tests"]

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.ruff]
line-length = 88
target-version = "py38"
''')

    # 创建 README.md
    current_year = datetime.now().year
    (project_path / "README.md").write_text(f"""# {project_name}

## 描述
这是一个使用 create-uv-project 创建的 Python 项目。

## 功能
- 待添加

## 安装

### 开发环境设置
```bash
# 创建并激活虚拟环境
uv venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 安装开发和测试依赖
uv pip install -e ".[test,dev]"
```

### 可用的开发工具
- **测试工具**
  - `pytest`: 运行单元测试
  - `pytest-cov`: 生成测试覆盖率报告

- **代码质量工具**
  - `black`: Python 代码格式化
  - `ruff`: 快速的 Python 代码检查器

## 开发指南

### 运行测试
```bash
# 运行所有测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov
```

### 代码质量检查
```bash
# 格式化代码
uv run black .

# 运行代码检查
uv run ruff check .
```

## 使用
```bash
# 运行项目
{project_name}
```

## 安装测试环境
```bash
uv pip install -e ".[test,dev]"
```
安装已经完成了！让我解释一下命令的各个部分：
-e 表示以可编辑模式安装当前项目
".[test,dev]" 中的：
. 表示当前目录（项目根目录）
[test,dev] 指定要安装的可选依赖组
现在您已经安装了所有的开发和测试工具：
测试工具：pytest 和 pytest-cov
开发工具：black（代码格式化工具）和 ruff（代码检查工具）
您可以使用这些工具来：
运行测试：uv run pytest
格式化代码：uv run black .
运行代码检查：uv run ruff .



## 许可证
MIT License

Copyright (c) {current_year} Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

    # 创建 .gitignore
    (project_path / ".gitignore").write_text("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.coverage
coverage.xml
htmlcov/

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
""")


def main():
    parser = argparse.ArgumentParser(description="创建 Python 项目结构")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument("--path", default=".", help="项目创建路径，默认为当前目录")

    args = parser.parse_args()

    # 验证项目名称
    if not args.project_name.isidentifier():
        print(f"错误: '{args.project_name}' 不是有效的 Python 包名称", file=sys.stderr)
        sys.exit(1)

    # 创建项目路径
    project_path = Path(args.path) / args.project_name
    if project_path.exists():
        print(f"错误: 目录 '{project_path}' 已存在", file=sys.stderr)
        sys.exit(1)

    try:
        # 创建项目结构
        create_directory_structure(args.project_name, project_path)
        print(f"✨ 项目 '{args.project_name}' 创建成功！")
        print("\n要开始使用项目，请执行以下命令：")
        print(f"cd {args.project_name}")
        print("uv venv")
        print("source .venv/bin/activate  # Windows: .venv\\Scripts\\activate")
        print("uv sync  # 安装开发和测试依赖")
        print(f"{args.project_name}  # 运行项目")
    except Exception as e:
        print(f"错误: 创建项目时发生错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
