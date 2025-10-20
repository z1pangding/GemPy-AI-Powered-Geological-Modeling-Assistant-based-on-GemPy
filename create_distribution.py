"""
用于创建 GemPy AI 地质建模工具分发包的脚本
此脚本包含可执行文件和给同事的必要文档
"""
import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_distribution():
    """创建包含可执行文件和文档的分发包"""
    print("正在创建 GemPy AI 地质建模工具的分发包...")
    
    # 创建分发目录
    dist_dir = Path("distribution")
    dist_dir.mkdir(exist_ok=True)
    
    # 检查可执行文件是否存在 - 可能直接在 dist/ 目录或子目录中
    dist_base_dir = Path("dist")
    exe_file = dist_base_dir / "gempy_gui.exe"
    
    # 首先检查可执行文件是否直接在 dist/ 目录中
    if exe_file.exists():
        print(f"在 dist/ 目录中找到可执行文件: {exe_file}")
        exe_dir = dist_base_dir  # 使用 dist 作为基础目录
    else:
        # 检查是否在子目录中（如 gempy_gui/）
        exe_dir = dist_base_dir / "gempy_gui"
        exe_file = exe_dir / "gempy_gui.exe"
        
        if not exe_file.exists():
            print("错误: 未找到可执行文件！请先运行 build_minimal_exe.py。")
            print(f"查找位置: {dist_base_dir / 'gempy_gui.exe'} 和 {exe_file}")
            return
    
    # 复制可执行文件到分发目录
    dist_exe = dist_dir / "gempy_gui.exe"
    shutil.copy2(exe_file, dist_exe)
    print(f"已复制可执行文件到 {dist_exe}")
    
    # 创建文档
    create_installation_instructions(dist_dir)
    
    # 复制需要与exe一起分发的文件
    # 检查是否有automated_model目录要复制
    src_automated_model = exe_dir / "automated_model"
    if src_automated_model.exists():
        dist_automated_model = dist_dir / "automated_model"
        if dist_automated_model.exists():
            shutil.rmtree(dist_automated_model)
        shutil.copytree(src_automated_model, dist_automated_model)
        print(f"已复制 automated_model 目录到 {dist_automated_model}")
    else:
        print("警告: 未找到 automated_model 目录")
        # 从项目根目录复制CSV模板
        dist_automated_model = dist_dir / "automated_model"
        dist_automated_model.mkdir(exist_ok=True)
        
        # 复制项目中的CSV文件
        csv_files = [
            "automated_model/orientations_template.csv",
            "automated_model/points_template.csv", 
            "automated_model/series_template.csv",
            "automated_model/structure_template.csv",
            "automated_model/onlap_orientations.csv",
            "automated_model/onlap_points.csv",
            "automated_model/onlap_series.csv",
            "automated_model/onlap_structure.csv"
        ]
        
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                dest_file = dist_automated_model / os.path.basename(csv_file)
                shutil.copy2(csv_file, dest_file)
                print(f"已复制 {csv_file} 到 {dest_file}")
    
    # gempy_modeling_prompt.md is now embedded in the code, so no need to copy it separately
    # The AI functionality will work without this external file
    print("AI提示内容已嵌入程序代码中，无需单独分发 gempy_modeling_prompt.md 文件")
    
    # 为分发创建 requirements.txt
    requirements_content = """# GemPy AI geological modeling tool dependencies
# Install using: pip install -r requirements.txt

# Core dependencies
gempy
gempy_viewer
pandas
pyvista
matplotlib
matplotlib-base
PyQt6
numpy
torch
openai
pymupdf
python-docx
httpx[socks]
openpyxl
requests
scipy
fitz
PyMuPDF
pdfplumber
Pillow
pytesseract

# Make sure to install only PyQt6, not PyQt5 or other Qt frameworks
# This is to avoid conflicts during PyInstaller packaging
"""
    
    requirements_file = dist_dir / "requirements.txt"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print(f"已创建 requirements.txt 在 {requirements_file}")
    
    # Create quick start file
    quick_start_content = """GemPy AI Geological Modeling Tool Quick Start Guide

1. Download and install Python 3.10 or higher from https://python.org

2. Install required packages by running the following command in command prompt:
   pip install -r requirements.txt

3. Run the application by double-clicking gempy_gui.exe

4. On first use:
   - To use AI features, you need a ModelScope API key
   - You can also use without AI by manually specifying CSV files

5. If you encounter any problems, check the INSTALLATION_INSTRUCTIONS.txt file for troubleshooting.
"""
    
    quick_start_file = dist_dir / "QUICK_START.txt"
    with open(quick_start_file, 'w', encoding='utf-8') as f:
        f.write(quick_start_content)
    print(f"已创建快速入门指南 {quick_start_file}")
    
    # 创建分发 ZIP 文件
    zip_filename = dist_dir / "gempy_ai_distribution.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加可执行文件
        zipf.write(dist_exe, dist_exe.name)
        
        # 添加依赖项
        zipf.write(requirements_file, requirements_file.name)
        
        # 添加安装说明
        for file in dist_dir.glob("INSTALLATION_INSTRUCTIONS*.txt"):
            zipf.write(file, file.name)
        
        # 添加快速入门
        zipf.write(quick_start_file, quick_start_file.name)
        
        # 添加 automated_model 目录
        for root, dirs, files in os.walk(dist_automated_model):
            for file in files:
                file_path = Path(root) / file
                archive_path = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, archive_path)
        
        # AI提示内容已嵌入代码中，无需添加外部文件
        # The AI functionality will work without external prompt file
    
    print(f"已创建分发包: {zip_filename}")
    print(f"包大小: {zip_filename.stat().st_size / (1024*1024):.2f} MB")
    
    print("\\n分发包创建成功！")
    print(f"可在以下位置找到分发包: {zip_filename}")
    print("\\n分发给同事的方法:")
    print("1. 将 gempy_ai_distribution.zip 文件发送给他们")
    print("2. 让他们将其解压到任意文件夹")
    print("3. 按照 INSTALLATION_INSTRUCTIONS.txt 中的说明操作")

def create_installation_instructions(dist_dir):
    """创建详细的安装说明"""
    instructions = """GEMPY AI 地质建模工具安装说明
================================

重要提示: 此应用程序需要在您的系统上安装 Python 和多个依赖项。

先决条件:
----------
1. Windows 10 或更高版本（64位）
2. 您计算机上的管理员权限（用于安装 Python 和包）

步骤 1: 安装 Python
-------------------
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.10、3.11 或 3.12（64位版本）
3. 运行安装程序
4. 重要提示: 安装过程中勾选"将 Python 添加到 PATH"
5. 点击"立即安装"
6. 如果 Windows SmartScreen 发出警告，点击"更多信息"然后"仍然运行"

步骤 2: 安装依赖项
------------------
1. 解压分发 ZIP 文件到一个文件夹（例如 C:\\gempy_ai）
2. 按住 Shift 键并右键点击文件夹内空白处
3. 选择"在此处打开 PowerShell 窗口"或"在此处打开命令窗口"
4. 在 PowerShell/命令窗口中，运行此命令：
   
   pip install -r requirements.txt
   
5. 等待所有包安装完成（可能需要几分钟）
   注意: 如果出现 pip 错误，请尝试: python -m pip install -r requirements.txt

步骤 3: 运行应用程序
--------------------
1. 双击 gempy_gui.exe 运行应用程序
2. 如果 Windows 出现安全警告，点击"更多信息"然后"仍然运行"

故障排除:
----------
问: 我收到"python 不是内部或外部命令"的提示
答: 未将 Python 添加到 PATH。重新安装 Python 并勾选"将 Python 添加到 PATH"

问: 安装过程中出现权限错误
答: 尝试以管理员身份运行 PowerShell

问: 应用程序无法启动或显示导入错误
答: 确保所有依赖项都已正确安装。尝试:
   python -c "import gempy; print('GemPy 导入成功')"
   如果这失败了，重新安装依赖项: pip install -r requirements.txt

问: 我收到 "No module named PyQt6" 错误
答: 运行: pip install PyQt6

问: AI 功能无法使用
答: 您需要 ModelScope API 密钥。该工具可以在没有 AI 的情况下使用手动 CSV 输入。

问: 性能很慢
答: 确保已安装 CPU (NumPy) 和 GPU (PyTorch) 依赖项。
   该工具可以使用任一后端进行计算。

问: 我收到网络/SSL 错误
答: 某些公司网络会阻止访问。尝试: pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

更新:
-----
如果将来需要更新应用程序:
1. 下载新的分发包
2. 将新的 gempy_gui.exe 覆盖旧文件
3. 使用以下命令更新依赖项: pip install -r requirements.txt --upgrade

技术详情:
--------
此应用程序基于 GemPy v3 地质建模引擎构建，集成了 AI 功能。
它需要大量计算资源进行 3D 建模。
推荐的最低系统配置: 8GB RAM，现代多核处理器。

如需支持，请联系内部 IT 部门或应用程序开发者。

Copyright © 2025 zhengpengding. 保留所有权利。基于 GemPy 技术。
"""
    
    instructions_file = dist_dir / "INSTALLATION_INSTRUCTIONS.txt"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    print(f"已创建安装说明 {instructions_file}")

if __name__ == "__main__":
    create_distribution()