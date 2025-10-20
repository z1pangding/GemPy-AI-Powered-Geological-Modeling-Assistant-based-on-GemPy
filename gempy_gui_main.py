"""
GemPy AI 地质建模工具的主入口点
此脚本将用于创建最小可执行文件
"""
import os
import sys
import json

def main():
    """主应用程序入口点"""
    try:
        # 导入主应用程序
        from automated_model.pyqt_gui_model_builder import main as run_app
        run_app()
    except ImportError as e:
        print(f"导入应用程序时出错: {e}")
        print("\\n请确保已安装所有依赖项。")
        print("运行 'pip install -r requirements.txt' 安装所需包。")
        input("\\n按 Enter 键退出...")
        sys.exit(1)
    except Exception as e:
        print(f"运行应用程序时发生错误: {e}")
        input("\\n按 Enter 键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()