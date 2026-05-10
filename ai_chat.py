import requests

# 你的千帆 API Key
API_KEY = "bce-v3/ALTAK-oJp8a8jKurluJ3mlNDIen/9537ae4bf219b387196d1a9bf0200f2cab6df656"

# 千帆 OpenAI 兼容接口地址（微调模型同样使用此地址）
BASE_URL = "https://qianfan.baidubce.com/v2/chat/completions"

# 终版系统提示词（来自文档人员）
SYSTEM_PROMPT = (
    "你是「心语森林」AI心理陪伴助手，面向大学生群体，提供温暖、中立、非评判的情绪陪伴与倾听服务。"
    "你是“心语森林”，一个专门陪伴大学生的AI心理支持助手。"
    "【你的性格】"
    "- 温暖、耐心、不评判。像一位愿意倾听的朋友。"
    "- 不主动给出建议，不诊断疾病，不替代专业心理咨询师。"
    #"- 用简短、自然的中文回复，每句话不超过150字。"
    "【敏感话题处理规则】"
    "性取向、性别认同：不得说“性取向是个人的选择”或“可以改变”。应表达：性取向是与生俱来的自然特质，完全值得尊重。"
    "【安全机制】"
    "如果用户的话里明确提到：想死、自杀、活不下去、绝望、一了百了"
    "你必须先共情，然后立即建议寻求专业帮助。回复格式："
    "“我有点担心你。请相信我，你并不孤单。我建议你立刻联系心理援助热线：400-161-9995。需要我帮你找更多资源吗？”"
    "（不要额外加任何其他内容）"
)

def get_reply(user_message):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "ig7w5it1_d1zzy0ne",   # 已替换为你的微调模型接入点ID
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.9,
        "top_p": 0.8,
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "🌳 心语森林的思绪飘得有点远，请再呼唤我一次好吗？"
    except requests.exceptions.ConnectionError:
        return "🌳 心语森林暂时迷路了，网络好像不太稳定……"
    except Exception as e:
        return f"🌳 心语森林打了个盹：{repr(e)}"

if __name__ == "__main__":
    print("🌳 心语森林 v2.0 正在启动...")
    user_input = input("你：")
    if user_input.strip():
        response = get_reply(user_input)
        print(f"🌳 心语森林：{response}")
    else:
        print("🌳 心语森林：我在这里呢，你想和我聊聊什么？🌿")