# 聊天主界面（只保留这些，其他情绪相关的全删）
import streamlit as st
from pages import app

# 在 chat_ui.py 开头加：
st.set_page_config(page_title="聊天主界面", page_icon="💬")

# 页面配置
st.set_page_config(page_title="心语森林聊天", page_icon="💬")

# 聊天界面的代码（你原来的聊天逻辑，保持不变）
st.title("💬 心语森林聊天")
# ... 你的聊天界面代码 ...
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 去记录心情 → 跳转到 pages/app.py
    if st.button("去聊天"):
        st.switch_page("pages/app.py")

with col2:
    # 2. 查看我的情绪折线图 → 跳转到 pages/mood-chart.py
    if st.button("记录心情"):
        st.switch_page("pages/mood-chart.py")

with col3:
    # 3. （可选）这里可以放其他功能，或者删掉重复的按钮
    pass
