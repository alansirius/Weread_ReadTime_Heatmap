import json
import os
from datetime import datetime

def process_weread_data():
    """
    处理微信读书的readtiming.json数据，转换时间戳为日期格式
    """
    # 读取原始JSON文件
    input_file = 'readtiming.json'
    output_file = 'processed_readtiming.json'
    
    print(f"开始处理微信读书数据：{input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 处理阅读时间数据
        read_times = data.get('readTimes', {})
        formatted_data = {}
        
        for timestamp_str, seconds in read_times.items():
            # 转换时间戳为日期（YYYY-MM-DD格式）
            try:
                timestamp = int(timestamp_str)
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                formatted_data[date] = seconds
            except ValueError as e:
                print(f"警告：无法解析时间戳 {timestamp_str}: {e}")
        
        # 创建输出数据结构
        output_data = {
            "dailyReadTimes": formatted_data,
            "metadata": {
                "processedAt": datetime.now().isoformat(),
                "totalDays": len(formatted_data),
                "totalReadingSeconds": sum(formatted_data.values())
            }
        }
        
        # 保存处理后的数据
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)
        
        print(f"数据处理完成，已保存到：{output_file}")
        print(f"总计处理了{len(formatted_data)}天的阅读数据")
        
        return True
    
    except Exception as e:
        print(f"处理数据时出错：{e}")
        return False

if __name__ == "__main__":
    process_weread_data()
