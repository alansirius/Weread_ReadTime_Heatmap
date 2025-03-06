import json
from datetime import datetime

# 读取原始数据
with open('heatmapreadtiming.json', 'r') as f:
    data = json.load(f)

# 转换时间戳为日期，并提取阅读时间（单位：分钟）
output_data = []
for ts, seconds in data["readTimes"].items():
    date = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
    minutes = seconds // 60  # 转换为分钟
    output_data.append({"date": date, "value": minutes})

# 生成目标JSON格式
with open('processed_data.json', 'w') as f:
    json.dump(output_data, f, indent=2)
