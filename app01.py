import streamlit as st
from ai_chat import get_reply
from mood_tracker import save_mood, get_mood_label
from mood_chart import plot_mood_last_7_days
from tips import random_tip
from safety_check import check_safety

# ---------- 全局样式（来自前端的 app21.py） ----------
st.set_page_config(page_title="心语森林", page_icon="🌿", layout="wide")
st.markdown("""
<style>
.stApp {background-color: #f0f7f4;}
.stChatMessage {border-radius: 15px; padding: 12px; margin: 8px 0;}
.stChatMessage.user {background-color: #e6f4ea;}
.stChatMessage.assistant {background-color: #ffffff; border: 1px solid #d1e7dd;}
</style>
""", unsafe_allow_html=True)

# ---------- 标题 ----------
st.title("🌿 心语森林 — AI心理陪伴与情绪支持助手")
st.caption("我在这里，陪你一起面对所有情绪。无论你是焦虑、难过还是迷茫，都可以在这里倾诉。")

# ---------- 侧边栏 ----------
with st.sidebar:
    st.subheader("📝 今日心情记录")

    # 情绪选项（来自前端的 app23.py + 文档成员的图标设计）
    mood_options = {
        1: "💔😭🙀 裂开了",
        2: "😵🥀🪦 活人微死",
        3: "🧐🍃😹 佛系平稳",
        4: "😌☀️😸 美滋滋",
        5: "🥳🚀😎 爽炸了，起飞"
    }
    selected = st.radio("今天的心情是？", list(mood_options.values()))
    score = {v: k for k, v in mood_options.items()}[selected]
    st.caption("💡 1=彻底崩了 2=半死不活 3=平静无聊 4=偷着乐 5=爽到起飞")

    note = st.text_input("简单记录一句话（可选）", placeholder="今天发生了什么？")

    if st.button("💾 保存今日情绪"):
        ok = save_mood(score, note)
        if ok:
            st.success("✅ 心情已记录，感谢你愿意和我分享～")
        else:
            st.error("❌ 记录失败，请稍后重试")

    st.markdown("---")

    # 小贴士
    st.subheader("💡 今日自助小贴士")
    if st.button("✨ 给我一条今日小技巧"):
        st.info(random_tip())

    st.markdown("---")

    # 趋势图
    st.subheader("📈 近7天情绪变化")
    try:
        fig = plot_mood_last_7_days()
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info("先记录几次情绪，图表就会出现啦～")

# ---------- 主区域：AI 对话 ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🌳"):
        st.markdown(msg["content"])

user_input = st.chat_input("把你的心情告诉我吧...")

if user_input:
    # 显示用户消息
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 安全检测（注意：check_safety 返回 (True, msg) 表示触发预警）
    triggered, help_msg = check_safety(user_input)

    if triggered:
        # 预警信息（来自前端 app26.py + 文档成员的校内外资源）
        with st.chat_message("assistant", avatar="🌳"):
            st.error("⚠️ 我们感受到你正处于极度痛苦中，请一定珍惜自己！")
            st.error("📞 全国心理援助热线：")
            st.error("- 全国统一心理援助热线：12356（24小时，全国通用）")
            st.error("- 希望24热线：400-161-9995（24小时，生命危机干预）")
            st.error("- 青少年心理援助热线：12355（24小时，多地开通）")
            st.error("- 卫建委热线：12320（各地开通，可转接心理援助）")
            st.error("🏫 校内心理咨询预约方式（重庆机电大学）：")
            st.error("- 线上预约：心海系统 https://www.psyc.com.cn/vue/school/68549")
            st.error("- 电话预约：(023) 87388043（工作日 9:00-11:20, 14:00-17:20）")
            st.error("- QQ预约：477276348（工作日 9:00-11:20, 14:00-17:20）")
            st.error("- 线下预约：2栋宿舍旁心理咨询室，现场填写登记表")
        st.session_state.messages.append({"role": "assistant", "content": help_msg})
    else:
        # 正常 AI 回复
        with st.chat_message("assistant", avatar="🌳"):
            with st.spinner("心语森林正在思考..."):
                reply = get_reply(user_input)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- 页脚 ----------
st.divider()
st.caption("⚠️ 本工具为心理陪伴支持，不提供医疗诊断或治疗。如有严重情绪困扰，请拨打全国心理援助热线：400-161-9995")