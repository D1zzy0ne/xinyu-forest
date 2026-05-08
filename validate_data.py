import json
import os

INPUT_FILE = "xinyu_finetune_data.jsonl"
OUTPUT_FILE = "xinyu_finetune_clean.jsonl"
ERROR_LOG = "data_errors.txt"

valid_count = 0
errors = []

with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as fout, \
     open(ERROR_LOG, "w", encoding="utf-8") as ferr:

    for line_num, line in enumerate(fin, 1):
        line = line.strip()
        if not line:
            continue
        
        try:
            # 检查是否为合法JSON
            data = json.loads(line)
            
            # 检查是否包含 'messages' 字段，且为列表
            if "messages" not in data or not isinstance(data["messages"], list):
                errors.append(f"Line {line_num}: Missing or invalid 'messages' field.")
                ferr.write(f"{line_num}:{line}\n")
                continue
            
            msgs = data["messages"]
            valid_roles = {"system", "user", "assistant"}
            is_valid = True
            
            # 检查每条消息的格式是否正确，并过滤无效角色
            cleaned_msgs = []
            for msg in msgs:
                if not isinstance(msg, dict):
                    is_valid = False
                    break
                    
                role = msg.get("role", "")
                content = msg.get("content", "")
                
                # 过滤掉 '心理咨询师' 等非标准角色，并替换为标准角色
                if role == "心理咨询师":
                    role = "assistant"
                    msg["role"] = "assistant"
                elif role == "来访者":
                    role = "user"
                    msg["role"] = "user"
                
                # 过滤掉不在有效角色集合的消息
                if role not in valid_roles:
                    continue  # 跳过此无效消息
                    
                cleaned_msgs.append(msg)
                
            # 检查是否有 'user' 和 'assistant' 角色
            has_user = any(msg["role"] == "user" for msg in cleaned_msgs)
            has_assistant = any(msg["role"] == "assistant" for msg in cleaned_msgs)
            
            if not has_user or not has_assistant:
                errors.append(f"Line {line_num}: Missing required 'user' or 'assistant' role.")
                ferr.write(f"{line_num}:{line}\n")
                continue
            
            if is_valid:
                # 重新组织数据，确保格式完全符合要求
                clean_data = {"messages": cleaned_msgs}
                fout.write(json.dumps(clean_data, ensure_ascii=False) + "\n")
                valid_count += 1
            else:
                errors.append(f"Line {line_num}: Invalid message format.")
                ferr.write(f"{line_num}:{line}\n")
                
        except json.JSONDecodeError:
            errors.append(f"Line {line_num}: Invalid JSON format.")
            ferr.write(f"{line_num}:{line}\n")

print(f"✅ 清洗完成！")
print(f"   有效样本: {valid_count}")
print(f"   问题样本: {len(errors)}")
print(f"   问题详情已保存至: {ERROR_LOG}")
print(f"   清洗后数据已保存至: {OUTPUT_FILE}")

if valid_count == 0:
    print("\n⚠️ 警告：未生成任何有效样本，请检查原始数据格式。")