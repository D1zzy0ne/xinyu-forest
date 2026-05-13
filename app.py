import streamlit as st
from ai_chat import get_reply
from mood_tracker import save_mood, get_mood_label
from mood_chart import plot_mood_last_7_days
from tips import random_tip
from safety_check import check_safety
from tts import text_to_speech

# ---------- 全局样式 ----------
st.set_page_config(page_title="心语森林", page_icon="🌿", layout="wide")
st.markdown("""
<style>
.stApp {background-color: #f0f7f4;}
.stChatMessage {border-radius: 15px; padding: 12px; margin: 8px 0;}
.stChatMessage.user {background-color: #e6f4ea;}
.stChatMessage.assistant {background-color: #ffffff; border: 1px solid #d1e7dd;}
</style>
""", unsafe_allow_html=True)

# ---------- 极简用户系统 ----------
if "user_id" not in st.session_state:
    with st.container():
        st.title("🌿 欢迎来到心语森林")
        nickname = st.text_input("请输入你的昵称", placeholder="给自己取一个名字吧～")
        if st.button("进入心语森林", use_container_width=True):
            if nickname.strip():
                st.session_state.user_id = nickname.strip()
                st.rerun()
            else:
                st.error("请输入一个昵称哦～")
        st.stop()

user_id = st.session_state.user_id
user_name = user_id

# ---------- 标题 ----------
st.title("🌿 心语森林 — AI心理陪伴与情绪支持助手")
st.caption(f"你好，{user_name}！我在这里，陪你一起面对所有情绪。")

# 退出按钮
if st.sidebar.button("🚪 换个昵称"):
    del st.session_state.user_id
    st.rerun()

# ---------- 侧边栏：情绪记录 + 小贴士 + 趋势图 ----------
with st.sidebar:
    st.subheader("📝 今日心情记录")
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
        ok = save_mood(score, note, user_id=user_id)
        if ok:
            st.success("✅ 心情已记录，感谢你愿意和我分享～")
        else:
            st.error("❌ 记录失败，请稍后重试")

    st.markdown("---")
    st.subheader("💡 今日自助小贴士")
    if st.button("✨ 给我一条今日小技巧"):
        st.info(random_tip())

    st.markdown("---")
    st.subheader("📈 近7天情绪变化")
    try:
        fig = plot_mood_last_7_days(user_id=user_id)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info("先记录几次情绪，图表就会出现啦～")

# ---------- 主区域：AI 对话 ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for idx, msg in enumerate(st.session_state.messages):
    avatar = "👤" if msg["role"] == "user" else "🌳"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊 收听回复", key=f"voice_btn_{idx}"):
                with st.spinner("正在合成语音..."):
                    try:
                        audio_bytes = text_to_speech(msg["content"])
                        if audio_bytes and len(audio_bytes) > 0:
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                        else:
                            st.error("❌ 语音生成失败，音频数据为空")
                    except Exception as e:
                        st.error(f"❌ 语音合成出错：{repr(e)}")

user_input = st.chat_input("把你的心情告诉我吧...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    triggered, help_msg = check_safety(user_input)

    if triggered:
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
        with st.chat_message("assistant", avatar="🌳"):
            with st.spinner("心语森林正在思考..."):
                reply = get_reply(user_input)
            st.markdown(reply)

            if st.button("🔊 收听这条回复", key=f"voice_new_{len(st.session_state.messages)}"):
                with st.spinner("正在合成语音..."):
                    try:
                        audio_bytes = text_to_speech(reply)
                        if audio_bytes and len(audio_bytes) > 0:
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                        else:
                            st.error("❌ 语音生成失败，音频数据为空")
                    except Exception as e:
                        st.error(f"❌ 语音合成出错：{repr(e)}")

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- 页脚 ----------
st.divider()
st.caption("⚠️ 本工具为心理陪伴支持，不提供医疗诊断或治疗。如有严重情绪困扰，请拨打全国心理援助热线：400-161-9995")