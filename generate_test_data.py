import csv
from datetime import date, timedelta
import random

# 直接写入，覆盖旧数据
with open("mood_log.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["日期", "心情分数", "情绪标签", "备注"])

for i in range(7, 0, -1):
    day = date.today() - timedelta(days=i)
    score = random.randint(2, 5)
    labels = {1: "裂开了", 2: "活人微死", 3: "佛系平稳", 4: "美滋滋", 5: "爽炸了，起飞"}
    label = labels.get(score, "")
    note = f"测试数据 - {day.strftime('%m月%d日')}"
    with open("mood_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([day.isoformat(), score, label, note])

print("✅ 已生成最近7天的模拟情绪数据，请刷新页面查看趋势图。")