from openai import OpenAI

# ==================== 配置区 ====================
# 请将下面引号内的内容替换成你的新版 API Key (bce-v3/ALTAK-...)
API_KEY = "please sign in"

# 官方推荐的兼容接口地址
BASE_URL = "https://qianfan.baidubce.com/v2"
# 如果官方地址仍提示模型无效，可尝试以下备选地址：
# BASE_URL = "https://aip.baidubce.com/v2"
# ==============================================

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

system_prompt = (
    "你是一个温暖、耐心、非评判的心理陪伴助手。"
    "你不对用户做医学诊断，不主动建议用药。"
    "你的任务是倾听、共情、引导用户表达情绪，必要时鼓励他们寻求专业帮助。"
    "回答要简短、自然、有温度。"
)

def get_reply(user_message):
    try:
        response = client.chat.completions.create(
            model="ernie-speed-pro-128k",  # 使用确认过的模型ID
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            top_p=0.8,
        )
        return response.choices[0].message.content
    except Exception as e:
        # 捕获并返回更友好的错误信息
        return f"AI助手暂时遇到了一点问题：{e}"

if __name__ == "__main__":
    print("🌳 心语森林 v2.0 正在启动...")
    user_input = input("你：")
    if user_input.strip():
        response = get_reply(user_input)
        print(f"🌳 心语森林：{response}")
    else:
        print("🌳 心语森林：我在这里呢，你想和我聊聊什么？🌿")
