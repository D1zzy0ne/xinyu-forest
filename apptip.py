import random
# ----------------------
# 小贴士库（可扩展）
# ----------------------
TIPS = []
# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------
# 侧边栏：小贴士
# ----------------------
with st.sidebar:
    st.subheader("💡 今日小贴士")
    if "tip" not in st.session_state:
        st.session_state.tip = random.choice(TIPS)
    
    if st.button("🔄 换一条"):
        st.session_state.tip = random.choice(TIPS)
    
    st.success(st.session_state.tip)

# ----------------------
# 显示聊天历史
# ----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------
# 用户输入
# ----------------------
user_input = st.chat_input("说点什么吧...")

if user_input:
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. AI回复（这里先用模拟回复，你后面替换成API）
    ai_reply = f"我听到啦：{user_input}，别担心，我一直都在陪着你。"

    # 3. 显示AI消息
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
    # ----------------------
    st.components.v1.html(f"""
    <script>
        const text = `{ai_reply}`;
        const synth = window.speechSynthesis;
        synth.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 1.0;
        synth.speak(u);
    </script>
    """, height=0)