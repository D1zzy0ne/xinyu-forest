import csv
import os
from datetime import date

# 1-5分情绪标签（依据图标.docx）
MOOD_LABELS = {
    1: ("裂开了", "感觉全世界都在跟我作对，做什么都错。"),
    2: ("活人微死", "像行尸走肉，没力气也没兴趣，只想躺着。"),
    3: ("佛系平稳", "没大喜大悲，像喝白开水，平静但有点无聊。"),
    4: ("美滋滋", "有小事让我开心，或者单纯觉得今天顺。"),
    5: ("爽炸了，起飞", "超级爽！快乐到想原地起飞，感觉自己是人生赢家。"),
}


def _get_csv_path(user_id):
    """根据用户ID返回其专属的CSV文件路径"""
    return f"mood_log_{user_id}.csv"


def save_mood(score, note="", user_id="default"):
    """
    保存情绪记录，并返回是否成功和对应的生动标签。
    
    参数:
        score: 1-5 的整数
        note: 备注文字（可选）
        user_id: 用户唯一标识（可选，默认 "default"）
    """
    if not isinstance(score, int) or score < 1 or score > 5:
        print("❌ 心情分数必须是 1-5 的整数")
        return False

    today = date.today().isoformat()
    label, _ = MOOD_LABELS.get(score, ("", ""))
    row = [today, score, label, note]

    csv_file = _get_csv_path(user_id)
    file_exists = os.path.exists(csv_file)
    try:
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["日期", "心情分数", "情绪标签", "备注"])
            writer.writerow(row)
        print(f"✅ 情绪已记录：{today} {score}分 {label} {note} (用户: {user_id})")
        return True
    except Exception as e:
        print(f"❌ 记录失败：{e}")
        return False


def get_mood_label(score):
    """供前端获取分数对应的标签和描述"""
    return MOOD_LABELS.get(score, ("", ""))


if __name__ == "__main__":
    # 测试所有分数
    for s in range(1, 6):
        save_mood(s, "测试标签", user_id="test_user")