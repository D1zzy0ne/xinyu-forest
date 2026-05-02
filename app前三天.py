# -*- coding: utf-8 -*-
import streamlit as st

# 自定义CSS样式：全局背景、后续聊天框样式预设
st.markdown("""
<style>
/* 页面整体背景色：暖心森林浅绿风格 */
.stApp {
    background-color: #f0f7f4;
}

/* 聊天消息框圆角内边距预设 */
.stChatMessage {
    border-radius: 15px;
    padding: 12px;
    margin: 8px 0;
}

/* 用户消息气泡样式 */
.stChatMessage.user {
    background-color: #e6f4ea;
}

/* AI助手消息气泡样式 */
.stChatMessage.assistant {
    background-color: #ffffff;
    border: 1px solid #d1e7dd;
}

/* 底部输入框美化 */
.stChatInputContainer {
    background-color: white;
    border-radius: 20px;
    padding: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.title("🌳 心语森林 - 大学生心理支持助手")
st.caption("在这里,你可以放心倾诉,我会做你温暖的树洞。\n所有对话都会被温柔守护~")

st.divider()
#成员2 第二天代码
#心语森林 - 前端聊天交互开发
#前端开发:成员2
#开发任务:聊天记录存储、历史消息渲染、输入交互、对接后端AI接口

# 初始化会话缓存：保存聊天记录，刷新页面不丢失
#1. 导入成员1的AI回复函数
# --------------------------
from model import get_reply,check_safety
 # --------------------------
 # 2. 初始化会话缓存（刷新页面聊天记录不丢失）
 # --------------------------

if "messages" not in st.session_state:
       st.session_state.messages = []

# 循环渲染所有历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🌳"):
        st.markdown(msg["content"])

# 底部聊天输入框，接收用户倾诉内容
user_input = st.chat_input("把你的心情告诉我吧...")

# 消息发送与AI回复核心逻辑
if user_input:
    # 1. 展示用户发送的消息
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    # 2. 将用户消息存入聊天记录
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 安全预警(严格按成员3的安全规则)
if user_input:
    # 先判断安全等级
    if not check_safety(user_input):
        # 高危场景：只在这里弹出热线
        st.warning("请一定珍惜自己!全国心理援助热线:400-161-9995")
    # 再调用模型回复
    response = get_reply(user_input)

    # 3. 调用成员1的函数,获取AI心理回(只调用一次)
    ai_response = get_reply(user_input)

    # 4. 展示AI助手回复消息
    with st.chat_message("assistant", avatar="🌳"):
        st.markdown(ai_response)

    # 5. 将AI回复存入聊天记录,,完成一次对话交互
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

import pandas as pd
from datetime import datetime
import csv

# --------------------------
# 成员二 第3天：情绪记录UI组件
# 1. 心情分数滑块（1-5分）
# 2. 一句话备注输入框
# 3. 保存按钮
# --------------------------
st.subheader("🌿 今日情绪记录")

# 1. 情绪分数滑块（1-5分，带中文描述）
mood_score = st.slider(
    label="今天心情指数（1很差 → 5很好）",
    min_value=1,
    max_value=5,
    value=3,
    step=1
)

# 分数对应描述（成员三提供）
mood_desc = {
    1: "很差｜低落、疲惫",
    2: "不佳｜烦躁、焦虑",
    3: "一般｜平静普通",
    4: "不错｜轻松愉快",
    5: "很好｜开心满足"
}
st.caption(f"当前选择：{mood_desc[mood_score]}")

# 2. 一句话备注输入框
mood_note = st.text_input(
    label="简单记录一句话（可选）",
    placeholder="今天发生了什么？"
)

# 3. 保存按钮
if st.button("💾 保存今日情绪"):
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构造一行数据
    new_row = [today, mood_score, mood_note]
    
    # 写入 CSV（成员一提供的 save_mood 逻辑）
    with open("mood_log.csv", "a+", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 文件为空则写入表头
        f.seek(0)
        if not f.read(1):
            writer.writerow(["date", "score", "note"])
        writer.writerow(new_row)
    
    st.success("✅ 情绪记录保存成功！")

# --------------------------
# 第3天交付：UI组件可正常显示、点击可保存数据
# --------------------------