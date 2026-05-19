# 处理韦氏大学词典11版的音频文件，改名字

import re
import os
from pathlib import Path
import shutil
import urllib.parse
import subprocess
import datetime

data_path_old = 'C:\\123pan\\Downloads\\WMCD11_data\\WMCD11_0.txt'
data_path_new = 'C:\\123pan\\Downloads\\WMCD11_data\\WMCD11.txt'

sound_dir_old = 'C:\\123pan\\Downloads\\WMCD11_data\\data_0'
sound_dir_new = 'C:\\123pan\\Downloads\\WMCD11_data\\WMCD11.1'

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

def clear_headword(word):
    return word.replace('\\', '').replace('/', '--').replace('·', '').replace('?', '')

def convert_or_copy(word, sound_file_name):
    headword_ = clear_headword(word)
    old_path = Path(sound_dir_old, sound_file_name)
    new_path = Path(sound_dir_new, headword_ + '_' + old_path.name).with_suffix('.mp3') # 采用兼容性最好的mp3格式
    if not old_path.exists():
        print(f'文件{old_path}不存在！{word}')
        return False, sound_file_name
    if not new_path.exists():
        if old_path.suffix != new_path.suffix: # 如果格式不同，则进行转换
            print(f'正在处理{old_path} -> {new_path}')
            success = ffmpeg_convert(old_path, new_path)
            if not success:
                return False, sound_file_name
        else:
            shutil.copy(old_path, new_path)
    return True, new_path.name


# <font style="font-weight:bold;">([^<]*)</font>(<br>|<table(?:.(?!</table>))*?.</table>)<a href="sound://([^"]*)"><img src="Sound.png" border="0"></a>
pattern1 = re.compile(r'<font style="font-weight:bold;">(?P<word>[^<]*)</font>(<br>|<table(?:.(?!</table>))*?.</table>)<a href="sound://(?P<sound_file_name>[^"]*)"><img src="Sound.png" border="0"></a>')
def replace1(m, new_sound_name):
    return f'<font style="font-weight:bold;">{m.group("word").replace('\\', '')}</font>{m.group(2)}<a href="sound://{new_sound_name}"><img src="Sound.png" border="0"></a>'


# 底部派生词
pattern2 = re.compile(r'• <b>(?P<word>[^<]*)</b> <a href="sound://(?P<sound_file_name>[^"]*)"><img src="Sound.png" border="0"></a>')
def replace2(m, new_sound_name):
    # print(f"正在处理{m.group("word")}")
    return f'• <b>{m.group("word")}</b> <a href="sound://{new_sound_name}"><img src="Sound.png" border="0"></a>'


# 不同词形
pattern3 = re.compile(r'<i>also</i> <b>(?P<word>[^<]*)</b> <a href="sound://(?P<sound_file_name>[^"]*)"><img src="Sound.png" border="0"></a>')
def replace3(m, new_sound_name):
    return f'<i>also</i> <b>{m.group("word")}</b> <a href="sound://{new_sound_name}"><img src="Sound.png" border="0"></a>'


# or 的一种情况 主词或派生词的变形之一
pattern4 = re.compile(r'<i>or</i> <b>(?P<word>[^<]*)</b> <a href="sound://(?P<sound_file_name>[^"]*)"><img src="Sound.png" border="0"></a>')
def replace4(m, new_sound_name):
    return f'<i>or</i> <b>{m.group("word")}</b> <a href="sound://{new_sound_name}"><img src="Sound.png" border="0"></a>'


#TODO also 或 or， 比如 boogy，remove 以及其他带 or 或者 also 的情况 比如 polyphonic 等. 
# 不过，只要是具备独立词形的词头都已经具有了至少一个发音文件。


# def process_replace(line, pattern, replace_func):
#     def repl(m):
#         success, new_sound_name = convert_or_copy(m.group("word"), m.group('sound_file_name'))
#         if not success:
#             return m.group(0)
#         return replace_func(m, new_sound_name)

#     return pattern.sub(repl, line)

def process_replace(m, replace_func):
    success, new_sound_name = convert_or_copy(m.group("word"), m.group('sound_file_name'))
    if not success:
        return m.group(0)
    return replace_func(m, new_sound_name)

def process_content(content):
    # print(content)
    # content = process_replace(content, pattern1, replace1)
    # content = process_replace(content, pattern2, replace2)
    # content = process_replace(content, pattern3, replace3)
    # content = process_replace(content, pattern4, replace4)

    content = pattern1.sub(lambda m: process_replace(m, replace1), content)
    content = pattern2.sub(lambda m: process_replace(m, replace2), content)
    content = pattern3.sub(lambda m: process_replace(m, replace3), content)
    content = pattern4.sub(lambda m: process_replace(m, replace4), content)
    return content

with open(data_path_old, 'r', encoding='utf-8') as f:
    with open(data_path_new, 'w', encoding='utf-8') as f_new:
        t0 = datetime.datetime.now()
        count = 0
        word = ''
        item_end = False
        content = ''
        for line in f:
            if line.startswith('</>'):
                count += 1
                if count % 100 == 0:
                    print(f'正在处理第{count}个: {word}')
                content = process_content(content)
                f_new.write(f'{content}\n{line}')
                item_end = True
                content = ''
                continue
 
            # 词头
            if item_end:
                item_end = False
                f_new.write(f'{line}')
                word = line.strip()
                continue

            # 内容
            content += line.strip()

  
        t1 = datetime.datetime.now()
        print(f'处理完成，共处理{count}条词目, 耗时{t1 - t0}。')
