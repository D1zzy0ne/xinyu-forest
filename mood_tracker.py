import csv
import os
from datetime import date

# CSV 文件路径（与当前脚本同目录）
CSV_FILE = "mood_log.csv"

def save_mood(score, note=""):
    """
    保存一条情绪记录到 CSV 文件。

    参数:
        score: 心情分数，1-5 的整数
        note:  备注文字（可选）
    返回:
        True  记录成功
        False 记录失败
    """
    # 检查分数是否合法
    if not isinstance(score, int) or score < 1 or score > 5:
        print("❌ 心情分数必须是 1-5 的整数")
        return False

    # 获取今天日期，格式：2026-05-02
    today = date.today().isoformat()
    row = [today, score, note]

    # 判断文件是否已存在（用来决定要不要写表头）
    file_exists = os.path.exists(CSV_FILE)

    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["日期", "心情分数", "备注"])
            writer.writerow(row)
        print(f"✅ 情绪已记录：{today} 心情{score}分 {note}")
        return True
    except Exception as e:
        print(f"❌ 记录失败：{e}")
        return False


# ---------- 测试代码 ----------
if __name__ == "__main__":
    # 模拟三次情绪记录
    save_mood(3, "考试压力有点大")
    save_mood(4, "今天和室友一起吃饭")
    save_mood(2)  # 不写备注
    print("测试完成，请打开 mood_log.csv 查看结果。")