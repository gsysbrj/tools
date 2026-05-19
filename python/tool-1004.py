# 处理韦氏高阶的音频文件，改名字

import re
import os
from pathlib import Path
import shutil
import urllib.parse
import subprocess
import datetime
import html

file_path = 'C:\\123pan\\Downloads\\韦氏高阶英汉双解词典完美版_data\\maldpe_0.txt'
data_folder = 'C:\\123pan\\Downloads\\韦氏高阶英汉双解词典完美版_data\\data_0'
file_path_new = 'C:\\123pan\\Downloads\\韦氏高阶英汉双解词典完美版_data\\maldpe_new.txt'
data_folder_new = 'C:\\123pan\\Downloads\\韦氏高阶英汉双解词典完美版_data\\maldpe_new.1'

# 处理pronunciations\mp3 目录里的音频
p = re.compile(r'<a class="fa fa-volume-up hpron_icon play_pron" ([^>]*?) data-word="([^"]+)" href="sound://([^"]+)">')
p2 = re.compile(r'^[a-zA-Z]+$') # 匹配单词的正则表达式，要求单词必须是由字母组成的

# 处理idiom_ext目录里的音频 href="sound://idiom_ext/in%20full.spx"
p_idiom_ext = re.compile(r'href="sound://idiom_ext/([^"]+)"')

# 处理idioms目录里的音频 href="sound://idioms/indecent%20exposure.spx"
p_idiom = re.compile(r'href="sound://idioms/([^"]+)"')


# 处理mwcd目录里的音频 href="sound://mwcd/ggjina01.spx"
# <a href="sound://mwcd/ggjina01.spx" class="fa fa-volume-up hpron_icon play_pron" data-word="Jinan" data-dir="g" data-file="ggjina01" data-pron="ˈʤiːˈnɑːn" data-lang="en_us"></a>
p_mwcd = re.compile(r'<a href="sound://mwcd/([^"]+)" class="fa fa-volume-up hpron_icon play_pron" data-word="([^"]+)"([^>]*)></a>')

# WA 目录
# href="sound://WA/Kalahari.spx"
p_WA = re.compile(r'href="sound://WA/([^"]+)"')

# pronunciations/mp3/mw 
# <sup class="homograph"></sup> freaking </span> <span class="hsl"></span> <span class="hpron_word ifont"></span> <a class="fa fa-volume-up hpron_icon play_pron" href="sound://pronunciations/mp3/mw/freaki01.mp3"><img src="/sound.png"></a>
# pronunciations/mp3/number
# <sup class="homograph"></sup> twenty-twenty </span>。。。<span class="v_text">20/20</span> <span class="pron_w ifont">/<span class="smark">ˈ</span>twɛnti<span class="smark">ˈ</span>twɛnti/</span> <a class="fa fa-volume-up pron_i play_pron" data-dir="number" data-file="920_2001" data-lang="en_us" data-pron="ˈtwɛntiˈtwɛnti" data-word="or" href="sound://pronunciations/mp3/number/920_2001.mp3"><img src="/sound.png"></a>
# pronunciations/mp3/gg
# <sup class="homograph"></sup> Tyrian </span> <span class="hsl"></span> <span class="hpron_word ifont">/ˈtirijən/</span> <a class="fa fa-volume-up hpron_icon play_pron" href="sound://pronunciations/mp3/gg/ggtyrt01.mp3"><img src="/sound.png"></a>
# pronunciations/mp3/bix
# <sup class="homograph"></sup> braille </span> <span class="fl">noun</span></div> <div class="hw_vars_d m_hidden"> <span class="v_label">or</span> <span class="v_text">Braille</span> <span class="pron_w ifont">/<span class="smark">ˈ</span>breɪl/</span> <a class="fa fa-volume-up pron_i play_pron" data-dir="bix" data-file="bixbra13" data-lang="en_us" data-pron="ˈbreɪl" data-word="or" href="sound://pronunciations/mp3/bix/bixbra13.mp3"><img src="/sound.png"></a>
p_pron_mp3_mw_number_gg = re.compile(r'<sup class="homograph">(\d*)</sup>([^<]*)</span>((?:.(?!</div>))*.)href="sound://pronunciations/mp3/([^"]*)"><img src="/sound.png"></a>')

# # mp3目录和
# # <div class="hw_vars_d m_hidden"> <span class="v_label">also</span> <span class="v_text">Innuit</span> <span class="pron_w ifont">/<span class="smark">ˈ</span>ɪnjuwət/</span> <span class="pron_w ifont">/<span class="smark">ˈ</span>ɪnuwət/</span> <a class="fa fa-volume-up pron_i play_pron" data-dir="i" data-file="inuit001" data-lang="en_us" data-pron="ˈɪnuwət" data-word="also" href="sound://mp3/inuit001.mp3"><img src="/sound.png"></a></div>
# p_also = re.compile(r'<div class="hw_vars_d m_hidden">((?:.(?!</div>))*?)<span class="v_text">([^<]+)</span>((?:.(?!</div>))*?) href="sound://mp3/([^"]+)"><img src="/sound.png"></a></div>')

p_hw_vars = re.compile(r'<span class="v_text">([^<]*?)</span>((?:.(?!</div>))*.)href="sound://([^"]*)"')

p_traditional_chinese = re.compile(r'<span class="mw_zh traditional">[^<]*</span>')


def ffmpeg_convert(input_path, output_path, bitrate="192k"):
    """
    将音频文件转换格式。

    参数:
        input_path (str): 输入的文件路径。
        output_path (str): 输出的文件路径。
        bitrate (str): 输出 MP3 的比特率，例如 "128k", "192k"。默认 "192k"。
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

def replace_pron(match):
    m2 = match.group(2)
    m2 = m2.replace('/', '-').replace('–', '-') # 将词中的斜杠和破折号替换为连字符，避免文件名中出现非法字符
    m3 = match.group(3)

    old_path = Path(data_folder, m3)
    new_path = Path(data_folder_new, m2 + '_' + old_path.name).with_suffix('.mp3') # 音频文件名为：词_原文件名，避免重名冲突

    if new_path.exists():
        # print(f'文件{new_path}已存在，跳过重命名。')
        return f'<a class="fa fa-volume-up hpron_icon play_pron" {match.group(1)} data-word="{match.group(2)}" href="sound://{new_path.name}">'
    elif old_path.exists():
        # print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3': # 如果不是mp3格式，转换为mp3
            ffmpeg_convert(old_path, new_path) # 如果是spx格式，转换为mp3
        else:
            shutil.copy(old_path, new_path)
        return f'<a class="fa fa-volume-up hpron_icon play_pron" {match.group(1)} data-word="{match.group(2)}" href="sound://{new_path.name}">'
    else:
        # print(f'文件{old_path}不存在！')
        return match.group(0)

def replace_pron_idiom_ext(match):
    m1 = match.group(1)
    m1 = urllib.parse.unquote(m1) # 对URL编码的文件名进行解码
    old_path = Path(data_folder, f'idiom_ext/{m1}')
    new_path = Path(data_folder_new, old_path.name).with_suffix('.mp3') # 将文件扩展名改为mp3

    if new_path.exists():
        # print(f'文件{new_path}已存在，跳过重命名。')
        return f'href="sound://{new_path.name}"'
    elif old_path.exists():
        print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3': # 如果不是mp3格式，转换为mp3
            ffmpeg_convert(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
        return f'href="sound://{new_path.name}"'
    else:
        print(f'文件{old_path}不存在！')
        return match.group(0)

def replace_pron_idiom(match):
    m1 = match.group(1)
    m1 = html.unescape(urllib.parse.unquote(m1)) # 对URL编码的文件名进行解码
    old_path = Path(data_folder, f'idioms/{m1}')
    new_path = Path(data_folder_new, old_path.name).with_suffix('.mp3') # 将文件扩展名改为mp3

    if new_path.exists():
        # print(f'文件{new_path}已存在，跳过重命名。')
        return f'href="sound://{new_path.name}"'
    elif old_path.exists():
        print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3': # 如果不是mp3格式，转换为mp3
            ffmpeg_convert(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
        return f'href="sound://{new_path.name}"'
    else:
        print(f'文件{old_path}不存在！{match.group(1)}')
        return match.group(0)


# def replace_pron_also(match):
#     m2 = match.group(2)
#     m4 = match.group(4)
#     m4 = urllib.parse.unquote(m4)

#     old_path = Path(data_folder, f'mp3/{m4}')
#     new_path = Path(data_folder_new, old_path.name).with_suffix('.mp3')

#     if new_path.exists():
#         # print(f'文件{new_path}已存在，跳过重命名。')
#         return f'<div class="hw_vars_d m_hidden">{match.group(1)}<span class="v_text">{match.group(2)}</span>{match.group(3)} href="sound://{new_path.name}"><img src="/sound.png"></a></div>'
#     elif old_path.exists():
#         print(f'正在处理文件：{old_path}，新文件名：{new_path}')
#         if old_path.suffix != '.mp3': # 如果不是mp3格式，转换为mp3
#             ffmpeg_convert(old_path, new_path) # 如果是spx格式，转换为mp3
#         else:
#             shutil.copy(old_path, new_path)
#         return f'<div class="hw_vars_d m_hidden">{match.group(1)}<span class="v_text">{match.group(2)}</span>{match.group(3)} href="sound://{new_path.name}"><img src="/sound.png"></a></div>'
#     else:
#         print(f'文件{old_path}不存在！')
#         return match.group(0)

def replace_pron_mwcd(match):
    m1 = match.group(1)
    m2 = match.group(2)

    m1 = urllib.parse.unquote(m1) # 对URL编码的文件名进行解码
    old_path = Path(data_folder, f'mwcd/{m1}')
    new_path = Path(data_folder_new, m2 + '_' + old_path.name).with_suffix('.mp3')

    if new_path.exists():
        return f'<a href="sound://{new_path.name}" class="fa fa-volume-up hpron_icon play_pron" data-word="{m2}"{match.group(3)}></a>'
    elif old_path.exists():
        print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3':
            ffmpeg_convert(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
        return f'<a href="sound://{new_path.name}" class="fa fa-volume-up hpron_icon play_pron" data-word="{m2}"{match.group(3)}></a>'
    else:
        print(f'文件{old_path}不存在！')
        return match.group(0)


def replace_pron_WA(match):
    m1 = match.group(1)
    m1 = urllib.parse.unquote(m1)
    old_path = Path(data_folder, f'WA/{m1}')
    new_path = Path(data_folder_new, old_path.name).with_suffix('.mp3')

    if new_path.exists():
        return f'href="sound://{new_path.name}"'
    elif old_path.exists():
        print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3':
            ffmpeg_convert(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
        return f'href="sound://{new_path.name}"'
    else:
        print(f'文件{old_path}不存在！')
        return match.group(0)

def replace_pron_mp3_mw_number_gg(match):
    # 处理 pronunciations/mp3/mw 目录中的音频链接
    m2 = match.group(2).strip()  # 词条文本
    m4 = match.group(4)  # 文件名
    m4 = urllib.parse.unquote(m4)

    old_path = Path(data_folder, f'pronunciations/mp3/{m4}')
    new_path = Path(data_folder_new, m2 + '_' + old_path.name).with_suffix('.mp3')

    if new_path.exists():
        return (f'<sup class="homograph">{match.group(1)}</sup>{match.group(2)}</span>{match.group(3)}href="sound://{new_path.name}"><img src="/sound.png"></a>')
    elif old_path.exists():
        print(f'正在处理文件：{old_path}，新文件名：{new_path}')
        if old_path.suffix != '.mp3':
            ffmpeg_convert(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
        return (f'<sup class="homograph">{match.group(1)}</sup>{match.group(2)}</span>{match.group(3)}href="sound://{new_path.name}"><img src="/sound.png"></a>')
    else:
        print(f'文件{old_path}不存在！')
        return match.group(0)


def process_rest(line):
    """主要具有变体的词头。因为有变体时，主词头的逻辑处理不到这里的情况"""
    def repl(match):
        hw = match.group(1).replace('\\', '-').replace('/', '-').strip() # 去掉会影响目录的字符
        old_path = Path(data_folder, match.group(3))
        new_path = Path(data_folder_new, hw + '_' + old_path.name).with_suffix('.mp3')

        if not old_path.exists():
            print(f'{match.group(1)} 源音频文件{old_path}不存在！ ')
            return match.group(0)
        if not new_path.exists():
            print(f'正在处理 {match.group(1)} {old_path} -> {new_path}')
            if old_path.suffix != new_path.suffix:
                ffmpeg_convert(old_path, new_path)
            else:
                shutil.copy(old_path, new_path)
        return f'<span class="v_text">{match.group(1)}</span>{match.group(2)}href="sound://{new_path.name}"'

    return p_hw_vars.subn(repl, line)

# 收集此类并添加跳转锚点
p_word_class = re.compile(r'(?P<left_part><div class="hw_d hw_(?P<index>\d+) boxy m_hidden"[^>]*)>(?P<right_part>(?:.(?!</div>))*<span class="fl">(?P<class_name>[^<]*)</span>\s*</div>)')
def generate_id(headword, index, class_name):
    id = f'mald-word-class-anchor_{headword}_{index}_{class_name}'.replace(' ', '--') # 空格换成--，以与-做区分
    return id
def add_ids_and_anchors(m, headword, all_anchors):
    index = m.group('index')
    class_name = m.group('class_name')
    id = generate_id(headword, index, class_name)
    return f'{m.group('left_part')} id="{id}">{all_anchors}{m.group('right_part')}'
def add_collected_word_classes(headword, content):
    all_class_matches =  p_word_class.finditer(content)
    all_anchors = '<div class="word-class-anchors">'
    all_class_matches_count = 0
    for m in all_class_matches:
        all_class_matches_count += 1
        index = m.group('index')
        class_name = m.group('class_name')
        id = generate_id(headword, index, class_name)
        anchor = f'<a class="word-class-anchor" href="#{id}">{class_name}</a>'
        all_anchors += anchor + '|'
        # print(anchor)
    if all_class_matches_count <= 1:
        return content
    all_anchors = all_anchors[0:-1] + '</div>'
    # print(all_anchors)
    return p_word_class.sub(lambda m: add_ids_and_anchors(m, headword, all_anchors), content)

with open(file_path, 'r', encoding='utf-8') as f:
    with open(file_path_new, 'w', encoding='utf-8') as f_new:
        count = 0
        t0 = datetime.datetime.now()
        headword = ''
        content = ''
        for line in f:
            line = line.strip()
            if headword == '':
                headword = line
            elif line == '</>':
                count += 1
                if count % 1000 == 0:
                    print(f'正在处理第{count}个: {headword} ')

                content = p_traditional_chinese.sub('', content)                # 去掉繁体中文释义
                content = content.replace('<script src="maldpe-jquery-3.6.0.min.js"></script>', '')
                content = content.replace('<script src="maldpe-crypto-js.min.js"></script>', '')
                content = content.replace('<body>', '')
                content = content.replace('</body>', '')

                content, n = process_rest(content)
                content, n = p.subn(replace_pron, content)
                content, n = p_idiom_ext.subn(replace_pron_idiom_ext, content)
                content, n = p_idiom.subn(replace_pron_idiom, content)
                content, n = p_mwcd.subn(replace_pron_mwcd, content)
                content, n = p_WA.subn(replace_pron_WA, content)
                content, n = p_pron_mp3_mw_number_gg.subn(replace_pron_mp3_mw_number_gg, content)

                # 提取和添加词性类别
                content = add_collected_word_classes(headword, content)

                f_new.write(f'{headword}\n{content}\n</>\n')
                headword = ''
                content = ''
            else:
                content += line

        t1 = datetime.datetime.now()
        print(f'处理完成，共处理{count}条词目, 耗时{t1 - t0}。')
