![gempy自动建模示例](https://github.com/user-attachments/assets/457f6aad-a52c-474b-8bad-ff38b5663e72)
# 基于GemPy的AI地质建模助手 / AI-Powered Geological Modeling Assistant based on GemPy

[**中文**](#中文) | [**English**](#english)

---

## 中文

基于 GemPy v3 的三维地质建模工具，集成 AI 功能，支持通过 AI 对话和文档解析自动生成地质建模所需的数据文件。

### 项目说明

本项目基于 [GemPy](https://github.com/cgre-aachen/gempy) v3 地质建模引擎开发，继承了GemPy强大的三维地质建模能力，并在此基础上增加了AI驱动的数据处理功能。

### 功能特性

#### 1. AI 驱动的地质数据提取
- **对话式 AI 助手**：用户可以直接与 AI 对话，提供地质信息和地层序列关系
- **文档解析**：支持上传 PDF、Word、Excel、TXT 等格式的地质文档，自动解析并生成建模数据
- **双 AI 模型支持**：支持 GLM-4.6 和 DeepSeek-V3.2-Exp 模型，用户可手动选择

#### 2. 传统建模功能
- 基于 GemPy v3 的先进地质建模引擎
- 支持复杂的地质构造（断层、褶皱、不整合面等）
- 八叉树网格和密集网格两种计算模式
- GPU 和 CPU 双计算后端

#### 3. 可视化和输出
- 3D 地质模型可视化
- 2D 剖面图生成
- 多种格式模型导出

### 与 GemPy 的联系

本项目基于 [GemPy](https://github.com/cgre-aachen/gempy) 地质建模引擎构建，继承了其以下核心功能：
- 先进的地质建模算法
- 强大的三维可视化能力
- 灵活的网格系统（八叉树和密集网格）
- GPU 加速计算
- 丰富的地质构造处理能力

本项目在 GemPy 的基础上增加了 AI 数据处理功能，使用户可以通过自然语言或文档自动提取地质建模所需的数据。

### 项目贡献

本项目为 GemPy 生态系统做出以下贡献：
- 提供了 AI 驱动的数据预处理能力
- 简化了地质建模的数据准备流程
- 为中文用户提供了友好的图形界面
- 扩展了 GemPy 的应用场景

### 安装要求

```bash
# 方法一：使用 requirements.txt 文件安装（推荐）
pip install -r requirements.txt

# 方法二：逐个安装依赖库
pip install gempy gempy_viewer pandas pyvista matplotlib PyQt6 numpy pytorch openai pymupdf python-docx httpx[socks] openpyxl
```

### 使用方法

#### 1. 启动 GUI
运行以下脚本启动 GUI 界面：

```bash
python gempy_gui_main.py
```

#### 2. AI 数据生成方式

##### 方式一：文档上传
1. 勾选"使用 AI 生成数据文件"选项
2. 点击"选择文件..."上传地质文档
3. 点击"生成数据文件"让 AI 解析文档
4. 选择保存目录存放生成的 CSV 文件
5. 使用生成的文件进行建模

##### 方式二：对话式 AI 助手
1. 点击"AI 对话助手"按钮
2. 在对话窗口中与 AI 交互，提供地质信息
3. AI 将根据提示生成符合格式的数据
4. 点击"复制提取数据"获取 AI 生成的 CSV 内容
5. 手动保存为 CSV 文件后使用

#### 3. 传统建模方式
1. 取消勾选"使用 AI 生成数据文件"
2. 手动指定所需的四个 CSV 文件：
   - 产状文件 (orientations.csv)
   - 岩性点文件 (points.csv)
   - 序列顺序文件 (series.csv)
   - 构造定义文件 (structure.csv)
3. 设置建模参数后运行建模

### 支持的文件格式

#### 输入文档格式
- PDF 文档
- Word 文档 (.doc, .docx)
- Excel 表格 (.xls, .xlsx)
- 文本文件 (.txt)

---

## English

AI-enhanced 3D geological modeling tool based on GemPy v3, integrating AI capabilities for automatic geological data extraction and model generation through AI conversation and document parsing.

### Project Description

This project is developed based on the [GemPy](https://github.com/cgre-aachen/gempy) v3 geological modeling engine, inheriting GemPy's powerful 3D geological modeling capabilities and adding AI-driven data processing functionality.

### Features

#### 1. AI-Driven Geological Data Extraction
- **Conversational AI Assistant**: Interact directly with AI to provide geological information and stratigraphic sequence relationships
- **Document Parsing**: Upload geological documents in PDF, Word, Excel, and TXT formats for automatic parsing and model data generation
- **Dual AI Model Support**: Supports GLM-4.6 and DeepSeek-V3.2-Exp models with manual selection option

#### 2. Traditional Modeling Capabilities
- Advanced geological modeling engine based on GemPy v3
- Support for complex geological structures (faults, folds, unconformities)
- Both octree grid and dense grid computation modes
- Dual computation backends: GPU and CPU

#### 3. Visualization and Output
- 3D geological model visualization
- 2D cross-section generation
- Multi-format model export

### Relationship to GemPy

This project is built on the [GemPy](https://github.com/cgre-aachen/gempy) geological modeling engine and inherits the following core features:
- Advanced geological modeling algorithms
- Powerful 3D visualization capabilities
- Flexible grid systems (Octree and dense grids)
- GPU-accelerated computing
- Rich geological structure processing capabilities

This project adds AI data processing functionality on top of GemPy, allowing users to automatically extract geological modeling data through natural language or documents.

### Project Contributions

This project contributes to the GemPy ecosystem in the following ways:
- Provides AI-driven data preprocessing capabilities
- Simplifies the data preparation workflow for geological modeling
- Offers a user-friendly graphical interface for Chinese users
- Expands the application scenarios of GemPy

### Installation Requirements

```bash
# Method 1: Using requirements.txt file (recommended)
pip install -r requirements.txt

# Method 2: Install dependencies individually
pip install gempy gempy_viewer pandas pyvista matplotlib PyQt6 numpy pytorch openai pymupdf python-docx httpx[socks] openpyxl
```

### Usage Methods

#### 1. Launch GUI
Run the following script to start the GUI interface:

```bash
python gempy_gui_main.py
```

#### 2. AI Data Generation Modes

##### Method 1: Document Upload
1. Check "Use AI to generate data files" option
2. Click "Select File..." to upload geological documents
3. Click "Generate Data Files" to let AI parse the document
4. Select save directory to store generated CSV files
5. Use generated files for modeling

##### Method 2: Conversational AI Assistant
1. Click "AI Chat Assistant" button
2. Interact with AI in the dialog to provide geological information
3. AI will generate data in the format specified in the prompt
4. Click "Copy Extracted Data" to get AI-generated CSV content
5. Save manually as CSV files for use

#### 3. Traditional Modeling Method
1. Uncheck "Use AI to generate data files"
2. Manually specify the four required CSV files:
   - Orientation file (orientations.csv)
   - Lithological point file (points.csv)
   - Sequence order file (series.csv)
   - Structural definition file (structure.csv)
3. Set modeling parameters and run modeling

### Supported File Formats

#### Input Document Formats
- PDF documents
- Word documents (.doc, .docx)
- Excel spreadsheets (.xls, .xlsx)
- Text files (.txt)
