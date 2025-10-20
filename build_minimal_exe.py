"""
用于构建 GemPy AI 地质建模工具的最小可执行文件
此脚本使用 PyInstaller 创建一个小型可执行文件，需要外部依赖
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_minimal_exe():
    """使用 PyInstaller 构建最小可执行文件"""
    print("正在构建 GemPy AI 地质建模工具的最小可执行文件...")
    
    # 检查是否安装了 PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("未安装 PyInstaller。正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 主脚本路径
    main_script = "gempy_gui_main.py"
    
    if not os.path.exists(main_script):
        print(f"错误: 未找到 {main_script}！")
        return
    
    # PyInstaller 命令用于构建最小可执行文件
    # 我们将使用 spec 文件方法以更好地控制输出大小
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{main_script}'],
    pathex=[],
    binaries=[],
    datas=[
        ('automated_model/*.csv', 'automated_model'),
        ('automated_model/gui_config.json', 'automated_model'),
        # gempy_modeling_prompt.md is now embedded in the code, so no need to include it as a separate file
    ],
    hiddenimports=[
        'requests', 
        'urllib3', 
        'certifi', 
        'ssl', 
        'urllib3.util.ssl_', 
        'urllib3.contrib.pyopenssl', 
        'urllib3.packages.ssl_match_hostname',
        'urllib3.util.retry',
        'urllib3.connectionpool',
        'urllib3.connection',
        'urllib3.response',
        'urllib3.fields',
        'urllib3.filepost',
        'urllib3.poolmanager',
        'urllib3.request',
        'urllib3.util',
        'urllib3.util.connection',
        'urllib3.util.request',
        'urllib3.util.response',
        'urllib3.util.retry',
        'urllib3.util.ssl_',
        'urllib3.util.timeout',
        'urllib3.util.url',
        # SciPy and related dependencies to fix fftpack issue
        'scipy',
        'scipy.fft',
        'scipy.fftpack',
        'scipy.spatial',
        'scipy.spatial.distance',
        'scipy.interpolate',
        'scipy.integrate',
        'scipy.linalg',
        'scipy.special',
        'scipy.ndimage',
        'numpy',
        # Additional common dependencies
        'sklearn',
        'pandas',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt4agg',
        'matplotlib.backends.backend_agg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'matplotlib.patches',
        'matplotlib.path',
        'matplotlib.cbook',
        'matplotlib.colors',
        'matplotlib.collections',
        'matplotlib.patches',
        'matplotlib.text',
        'matplotlib.font_manager',
        'matplotlib.transforms',
        'matplotlib.lines',
        'matplotlib.image',
        'matplotlib.dates',
        'matplotlib.units',
        'matplotlib.container',
        'pyvista',
        'gempy',
        'gempy_viewer',
        'torch',  # PyTorch renamed from pytorch
    ],
    hookspath=['.'],  # Look for hooks in the current directory
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['PyQt5', 'PySide2', 'PySide6', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],  # 排除其他Qt绑定以避免冲突，仅保留PyQt6
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gempy_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""
    
    # 写入 spec 文件
    spec_file = "gempy_gui.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("已创建 PyInstaller 的 spec 文件...")
    
    # 使用 spec 文件运行 PyInstaller
    try:
        print("正在运行 PyInstaller 构建可执行文件...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller", 
            spec_file, 
            "--clean",
            "--noconfirm"  # 添加覆盖选项
        ]
        
        # 先删除可能存在的旧文件以避免权限错误
        exe_path = Path("dist/gempy_gui.exe")
        if exe_path.exists():
            try:
                exe_path.unlink()
            except PermissionError:
                print(f"警告: 无法删除旧的可执行文件 {exe_path}，可能正在运行中")
                print("请关闭任何正在运行的 gempy_gui.exe 进程，然后重试")
                return
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 检查是否是权限错误
        if "PermissionError: [WinError 32]" in result.stderr:
            print("权限错误: 另一个程序正在使用输出文件。")
            print("请确保没有正在运行的 gempy_gui.exe 进程，然后重试")
            return
        elif result.returncode != 0:
            print(f"PyInstaller 运行失败. 输出: {result.stdout}")
            print(f"错误: {result.stderr}")
            # 检查是否生成了exe文件但没有目录（这是PyInstaller的另一种输出模式）
            exe_files = list(Path("dist").glob("*.exe"))
            if exe_files:
                print(f"找到直接在dist目录的exe文件: {exe_files}")
            return
        
        # 检查可执行文件是否存在
        dist_dir = Path("dist")
        exe_dir = dist_dir / "gempy_gui"
        
        # 检查 if the executable exists directly in the dist directory
        direct_exe = dist_dir / "gempy_gui.exe"
        if direct_exe.exists():
            print(f"找到直接在 dist 目录的可执行文件: {direct_exe}")
            exe_dir = dist_dir  # 更新exe_dir指向dist目录
        
        # 验证exe目录是否存在
        if not exe_dir.exists():
            print(f"警告: {exe_dir} 不存在，PyInstaller 可能构建失败")
            # 检查是否有其他可能的输出目录
            possible_dirs = [d for d in dist_dir.iterdir() if d.is_dir() and d.name.startswith("gemp")]
            if possible_dirs:
                exe_dir = possible_dirs[0]  # 使用找到的第一个目录
                print(f"使用找到的目录: {exe_dir}")
            else:
                print("未找到构建输出目录")
                # 检查是否直接生成了exe文件而不是目录
                exe_files = list(dist_dir.glob("*.exe"))
                if exe_files:
                    print(f"找到直接在dist目录的exe文件: {exe_files}")
                    print("构建可能已部分完成，但没有目录结构")
                    # 更新exe_dir指向dist
                    exe_dir = dist_dir
                else:
                    print("在dist目录中未找到任何exe文件")
                    return
        
        # 如果不存在则创建 automated_model 子目录
        automated_model_dir = exe_dir / "automated_model"
        automated_model_dir.mkdir(exist_ok=True)
        
        # 复制 CSV 模板
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
                dest_file = automated_model_dir / os.path.basename(csv_file)
                shutil.copy2(csv_file, dest_file)
                print(f"已复制 {csv_file} 到 {dest_file}")
        
        # 复制 GUI 配置文件（如果存在）
        if os.path.exists("automated_model/gui_config.json"):
            shutil.copy2("automated_model/gui_config.json", automated_model_dir / "gui_config.json")
            print(f"已复制 automated_model/gui_config.json 到 {automated_model_dir / 'gui_config.json'}")
        
        print("可执行文件构建成功！")
        exe_file = exe_dir / "gempy_gui.exe"
        if exe_file.exists():
            print(f"可在以下位置找到您的可执行文件: {exe_file}")
        else:
            # 如果 exe_dir 是 dist 目录，查找 exe 文件
            exe_file_dist = Path("dist") / "gempy_gui.exe"
            if exe_file_dist.exists():
                print(f"可在以下位置找到您的可执行文件: {exe_file_dist}")
            else:
                print(f"警告: 可执行文件未在预期位置找到: {exe_file}")
                # 查找exe文件
                exe_files = list(exe_dir.rglob("*.exe"))
                if exe_files:
                    print(f"找到的可执行文件: {exe_files}")
        
        # 清理构建文件
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("已清理 build 目录")
        
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"已清理 {spec_file}")
            
        if os.path.exists("gempy_gui.spec"):
            os.remove("gempy_gui.spec")
            print("已清理 gempy_gui.spec")
        
    except subprocess.CalledProcessError as e:
        print(f"运行 PyInstaller 时出错: {e}")
        # 即使 PyInstaller 报错，我们也检查是否已生成了部分文件
        dist_dir = Path("dist")
        exe_dir = dist_dir / "gempy_gui"
        if exe_dir.exists():
            print(f"警告: 虽然遇到错误，但目录 {exe_dir} 已存在")
            exe_file = exe_dir / "gempy_gui.exe"
            if exe_file.exists():
                print(f"可执行文件已成功创建: {exe_file}")
            else:
                print(f"目录 {exe_dir} 存在，但可执行文件可能未完成创建")
        return
    except Exception as e:
        print(f"发生错误: {e}")
        return

if __name__ == "__main__":
    build_minimal_exe()