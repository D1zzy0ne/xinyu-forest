# xinyu-forest
心语森林，智能心理助手库
# 心语森林 - AI心理陪伴助手

## 项目简介
面向大学生的 AI 心理陪伴助手，提供情绪记录、共情对话、情绪趋势分析等功能。

## 启动方式
1. 配置 API Key（在代码中替换为环境变量或直接填入）
2. 运行主程序：`python app.py`
3. 情绪记录：`python mood_tracker.py`
4. 生成趋势图：`python mood_chart.py`

## 文件说明
- `app.py`：AI 对话主程序（调用大模型）
- `mood_tracker.py`：记录每日情绪分数
- `mood_chart.py`：生成最近7天情绪趋势图
- `mood_log.csv`：存储情绪记录

## 环境要求
- Python 3.8+
- 安装依赖：`pip install -r requirements.txt`

## 环境配置

本项目使用百度千帆大模型 API，需要配置 API Key。

1. 获取 API Key：登录 [百度千帆平台](https://qianfan.baidu.com/)，在“应用接入”中创建应用，获取 API Key。
2. 设置环境变量：
   - Windows (cmd)：`set BAIDU_API_KEY=你的API_Key`
   - Windows (PowerShell)：`$env:BAIDU_API_KEY="你的API_Key"`
   - macOS / Linux：`export BAIDU_API_KEY="你的API_Key"`

## 安装与运行

1. 安装依赖：`pip install -r requirements.txt`
2. 设置好环境变量后，运行：`streamlit run app.py`