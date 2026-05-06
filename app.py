"""
心语森林 —— AI心理陪伴与情绪支持助手
主入口文件：整合所有功能模块
"""

import streamlit as st
from ai_chat import get_reply
from mood_tracker import save_mood, get_mood_label
from mood_chart import plot_mood_last_7_days
from tips import random_tip
from safety_check import check_safety

# ---------- 页面设置 ----------
st.set_page_config(
    page_title="心语森林",
    page_icon="🌳",
    layout="wide"
)

# ---------- 标题 ----------
st.title("🌳 心语森林 —— AI心理陪伴与情绪支持助手")
st.caption("这里没有评判，只有倾听。你可以放心说出任何心事。")

# ---------- 侧边栏：情绪记录 + 小贴士 + 趋势图 ----------
with st.sidebar:
    st.header("📝 情绪记录")
    score = st.slider("今日心情分数", 1, 5, 3)
    label, desc = get_mood_label(score)
    st.caption(f"**{label}** —— {desc}")
    note = st.text_input("备注（可选）")
    if st.button("记录今日心情"):
        ok = save_mood(score, note)
        if ok:
            st.success("✅ 情绪已记录")
        else:
            st.error("❌ 记录失败，请稍后重试")

    st.divider()

    st.header("💡 今日小贴士")
    if st.button("给我一条小贴士"):
        st.info(random_tip())

    st.divider()

    st.header("📊 情绪趋势")
    try:
        fig = plot_mood_last_7_days()
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"图表加载失败：{e}")

# ---------- 主区域：AI 对话 ----------
st.header("💬 对话心语森林")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用户输入
user_input = st.chat_input("说说你的心事...")

if user_input:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 安全检测
    triggered, help_msg = check_safety(user_input)
    if triggered:
        with st.chat_message("assistant"):
            st.error(help_msg)
        st.session_state.messages.append({"role": "assistant", "content": help_msg})
    else:
        # 调用AI获取回复
        with st.chat_message("assistant"):
            with st.spinner("心语森林正在思考..."):
                reply = get_reply(user_input)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- 页脚 ----------
st.divider()
st.caption("⚠️ 本工具为心理陪伴支持，不提供医疗诊断或治疗。如有严重情绪困扰，请拨打全国心理援助热线：400-161-9995")