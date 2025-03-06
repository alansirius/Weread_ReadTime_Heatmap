import json
from datetime import datetime

# 读取 JSON 文件
with open('/heatmapreadtiming.json', 'r') as f:
    data = json.load(f)

# 转换时间戳为日期，并过滤有效数据
processed_data = {}
for ts, seconds in data['readTimes'].items():
    date = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')
    processed_data[date] = seconds

# 生成 github_heatmap 兼容的 CSV 格式
with open('reading_data.csv', 'w') as f:
    f.write("Date,ReadingTime(seconds)\n")
    for date, seconds in sorted(processed_data.items()):
        f.write(f"{date},{seconds}\n")
