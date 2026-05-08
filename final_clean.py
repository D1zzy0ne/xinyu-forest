import json

INPUT_FILE = "xinyu_finetune_clean.jsonl"
OUTPUT_FILE = "xinyu_final.jsonl"

valid_count = 0
skip_too_short = 0
skip_too_long = 0
skip_content_too_long = 0

with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

    for line_num, line in enumerate(fin, 1):
        try:
            data = json.loads(line)
            messages = data.get("messages", [])

            # 规则1：过滤掉少于4轮或多于150轮的对话
            if len(messages) < 4:
                skip_too_short += 1
                continue
            if len(messages) > 150:
                skip_too_long += 1
                continue

            # 规则2：清理每条消息的内容
            cleaned = []
            for msg in messages:
                content = msg.get("content", "")
                # 去除首尾空白和多余换行
                content = content.strip()
                # 限制单条消息最大 800 字符（可自行调整）
                if len(content) > 800:
                    content = content[:800] + "..."
                # 跳过空白消息
                if not content:
                    continue
                # 确保 role 是 user/assistant/system 之一
                role = msg.get("role", "")
                if role not in ("user", "assistant", "system"):
                    continue
                cleaned.append({"role": role, "content": content})

            # 规则3：过滤清理后不足 2 轮的对话
            if len(cleaned) < 2:
                skip_too_short += 1
                continue

            # 规则4（可选）：在第一轮前插入 system 提示（如果你的数据没有）
            # 千帆平台在 Role(user+assistant) 模式下不强制要求 system，但加入可以提高通过率
            # if cleaned[0]["role"] != "system":
            #     cleaned.insert(0, {"role": "system", "content": "你是一个温暖、专业的心理咨询师。"})

            new_data = {"messages": cleaned}
            fout.write(json.dumps(new_data, ensure_ascii=False) + "\n")
            valid_count += 1

        except Exception:
            continue

print(f"结果报告：")
print(f"  ✅ 有效样本数: {valid_count}")
print(f"  ⏩ 跳过过短对话: {skip_too_short}")
print(f"  ⏩ 跳过过长对话: {skip_too_long}")
print(f"  📄 输出文件: {OUTPUT_FILE}")