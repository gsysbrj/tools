# 处理美国传统词典第5版的音频文件，改名字

import re
import os
from pathlib import Path
import shutil
import urllib.parse
import subprocess
import datetime

file_path_old = 'C:\\123pan\\Downloads\\AHD52017_old\\AHD52017.txt'
data_folder_old = 'C:\\123pan\\Downloads\\AHD52017_old\\data'
file_path_new = 'C:\\123pan\\Downloads\\AHD52017_new\\AHD52017_new.txt'
data_folder_new = 'C:\\123pan\\Downloads\\AHD52017_new\\data'


def ffmpeg_convert(input_path, output_path, bitrate="192k"):
    """
    将音频文件转换为格式。

    参数:
        input_path (str): 输入文件路径。
        output_path (str): 输出文件路径。
        bitrate (str): 输出比特率，例如 "128k", "192k"。默认 "192k"。
    """
    # 检查输入文件是否存在
    # if not os.path.exists(input_path):
    #     print(f"错误：输入文件不存在 - {input_path}")
    #     return False

    # 确保输出文件的目录存在
    # os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 构建 FFmpeg 命令
    # -i: 指定输入文件
    # -ab: 设置音频比特率
    # -ac: 设置音频通道数（2 为立体声）
    # -ar: 设置音频采样率（44100 Hz 为 CD 音质）
    # -y: 如果输出文件已存在，则直接覆盖，不再询问
    command = [
        'ffmpeg',
        '-i', input_path,
        '-ab', bitrate,
        '-ac', '2',          # 转换为立体声
        '-ar', '44100',       # 设置采样率为 44100 Hz
        '-y',                 # 覆盖输出文件
        output_path
    ]

    try:
        # 执行命令，并等待其完成
        # 设置 timeout 可以防止进程卡死，可根据文件大小调整
        result = subprocess.run(command, check=True, capture_output=True, timeout=60)
        # print(f"转换成功：{input_path} -> {output_path}")
        # print('FFmpeg 的标准输出信息:', result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 执行失败：{e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("转换超时，请检查文件大小或 FFmpeg 配置。")
        return False
    except Exception as e:
        print(f"发生未知错误：{e}")
        return False

# <div class="rtseg">...<a class="sound" href="sound:///wavs/A0281100.wav" >...</div>
p_pron = re.compile(r'<div class="rtseg">((?:.(?!</div>))*?)<a class="sound" href="sound:///([^"]*?)" >')

def process(headword, line):
    """
    复制和转换格式
    """

    def replace_pron(match):
        headword_ = headword.replace('\\', '-').replace('/', '-')
        old_path = Path(data_folder_old, match.group(2))
        new_path = Path(data_folder_new, headword_ + '_' + old_path.name).with_suffix('.mp3') # 采用兼容性最好的mp3格式
        if not old_path.exists():
            print(f'文件{old_path}不存在！{headword}')
            return match.group(0)
        if not new_path.exists():
            if old_path.suffix != new_path.suffix: # 如果格式不同，则进行转换
                ffmpeg_convert(old_path, new_path)
            else:
                shutil.copy(old_path, new_path)
        return f'<div class="rtseg">{match.group(1)}<a class="sound" href="sound:///{new_path.name}" >'
    
    return p_pron.subn(replace_pron, line)

with open(file_path_old, 'r', encoding='utf-8') as f:
    with open(file_path_new, 'w', encoding='utf-8') as f_new:
        t0 = datetime.datetime.now()
        count = 0
        headword = ''
        for line in f:
            if line.startswith('<link'):
                count += 1
                # print(f"count = {count}")
                if count % 100 == 0:
                    print(f'正在处理第{count}个: {headword}')
                line, n = process(headword, line)
                f_new.write(f'{line}')
            else:
                headword = line.strip()
                f_new.write(f'{line}') 
        t1 = datetime.datetime.now()
        print(f'处理完成，共处理{count}条词目, 耗时{t1 - t0}。')
