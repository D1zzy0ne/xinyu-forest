import os
import json
import glob

data_dir = "cpsycoun_data"           # 原始 txt 文件夹
output_file = "xinyu_finetune_data.jsonl"

total_dialogues = 0

with open(output_file, "w", encoding="utf-8") as f_out:
    for filepath in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
        with open(filepath, "r", encoding="utf-8") as f_in:
            lines = [line.strip() for line in f_in if line.strip()]
            if not lines:
                continue

            messages = []
            i = 0
            while i < len(lines):
                line = lines[i]

                # 识别说话人（支持“来访者：”和“心理咨询师：”）
                if line.startswith("来访者：") or line.startswith("来访者:"):
                    role = "user"
                    content = line.split("：", 1)[-1] if "：" in line else line.split(":", 1)[-1]
                    i += 1
                    # 合并连续的非角色行（同一个人说的话可能分多行）
                    while i < len(lines) and not (lines[i].startswith("来访者：") or lines[i].startswith("来访者:") or lines[i].startswith("心理咨询师：") or lines[i].startswith("心理咨询师:")):
                        content += "\n" + lines[i]
                        i += 1
                    messages.append({"role": role, "content": content.strip()})

                elif line.startswith("心理咨询师：") or line.startswith("心理咨询师:"):
                    role = "assistant"
                    content = line.split("：", 1)[-1] if "：" in line else line.split(":", 1)[-1]
                    i += 1
                    while i < len(lines) and not (lines[i].startswith("来访者：") or lines[i].startswith("来访者:") or lines[i].startswith("心理咨询师：") or lines[i].startswith("心理咨询师:")):
                        content += "\n" + lines[i]
                        i += 1
                    messages.append({"role": role, "content": content.strip()})
                else:
                    i += 1

            # 只保存至少有一问一答的对话
            if len(messages) >= 2:
                f_out.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
                total_dialogues += 1

print(f"✅ 转换完成！共处理 {total_dialogues} 组有效对话")
print(f"训练数据已保存到：{output_file}")