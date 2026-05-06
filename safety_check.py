# 敏感词列表
SENSITIVE_KEYWORDS = [
    "想死", "自杀", "活不下去", "绝望", "一了百了",
    "结束自己", "不想活了", "没有活着的意义", "自残",
]

# 预警后展示的求助资源
HELP_MESSAGE = (
    "🔴 我有点担心你。请相信我，你并不孤单。\n"
    "📞 全国心理援助热线：400-161-9995（24小时）\n"
    "🆘 也可以立刻联系你信任的家人、朋友，或直接前往最近医院急诊科。\n"
    "需要我帮你查找校内心理咨询中心的信息吗？"
)

def check_safety(text: str) -> (bool, str):
    """
    检测用户输入是否包含敏感词
    返回: (是否触发预警, 预警消息)
    """
    if any(word in text for word in SENSITIVE_KEYWORDS):
        return True, HELP_MESSAGE
    return False, ""

if __name__ == "__main__":
    # 测试
    test_input = "我觉得活着好累，想死"
    triggered, msg = check_safety(test_input)
    print("触发预警:", triggered)
    if triggered:
        print("预警消息:\n", msg)