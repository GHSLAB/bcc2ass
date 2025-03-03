import pandas as pd
from datetime import timedelta
import json
import sys

def seconds_to_time_string(seconds):
    # 将秒数转换为 timedelta 对象
    time_delta = timedelta(seconds=seconds)
    
    # 使用 strftime 方法将 timedelta 对象格式化为字符串，并保留两位小数
    time_string = time_delta.total_seconds()
    time_string = "{:.2f}".format(time_string)
    
    # 将秒数部分替换为 HH:MM:SS 格式
    hours, remainder = divmod(int(time_string.split('.')[0]), 3600)
    minutes, seconds = divmod(remainder, 60)
    time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{time_string.split('.')[1]}"
    
    return time_string

def df_to_ass(df):
    ass_content = "[Script Info]\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "PlayResX: 1920\n"
    ass_content += "PlayResY: 1080\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "\n"
    ass_content += "[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,36,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,0\n"
    ass_content += "\n"
    ass_content += "[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    for index, row in df.iterrows():
        ass_content += f"Dialogue: 0,{seconds_to_time_string(row['start_time'])},{seconds_to_time_string(row['end_time'])},Default,,0,0,0,,{row['content'].replace('\n', '\\N')}\n"
        
    return ass_content

# 读取BCC文件并解析为DataFrame
def read_bcc_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data['body'])

# 主函数
def main():
    # 检查命令行参数是否正确
    if len(sys.argv) != 5 or sys.argv[1] != '-i' or sys.argv[3] != '-o':
        print("请使用正确的参数格式：python bcc2ass.py -i input_file -o output_file")
        sys.exit(1)
    
    # 获取输入和输出文件路径
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[4]
    
    # 读取BCC文件并解析为DataFrame
    df = read_bcc_file(input_file_path)
    
    # 将DataFrame转换为ASS文件内容
    ass_file_content = df_to_ass(df)
    
    # 将ASS文件内容写入文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(ass_file_content)

# 运行主函数
if __name__ == "__main__":
    main()