import datetime
from pathlib import Path
import re
import sys
from typing import List, Tuple

# 合并词典文件，给美国传统词典添加韦氏词典的发音
filepath = Path(r"C:/123pan/Downloads/美国传统英语词典英汉双解第3版_完善进行中/美国传统英语词典英汉双解第3版.txt")
filepath_new = Path(r"C:/123pan/Downloads/美国传统英语词典英汉双解第3版_完善进行中/美国传统英语词典英汉双解第3版_new.txt")
filepath2 = Path(r"C:/123pan/Downloads/WMCD11/WMCD11/WMCD11.txt")
filepath3 = Path(r"C:/123pan/Downloads/AHD5/AHD52017/AHD52017.txt")



def build_mapping(path: Path) -> List[Tuple[str, str]]:
    '''读取词典文件，构建条目列表'''
    entries: List[Tuple[str, str]] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        lines = [line.strip() for line in f]

    key = ""
    value = ""
    for line in lines:
        if line == "</>":
            entries.append((key, value))
            key = ""
            value = ""
        elif key == "":
            key = line
        else:
            value += line
    return entries


process_pattern1 = re.compile(r'(<link rel="stylesheet" href="ahd3af.css" />|<hr>)<b>([^<]*?)</b>((?:(?<!<font class=PoS>).)*?)<font class=PoS><b>([^<]*?)</b>((?:(?<!</font>).)*?)</font>', flags=re.DOTALL)
process_pattern2 = re.compile(r'<br><b>([^<]*?)</b>\s*<font class=PoS><b>([^<]*?)</b>([^<]*?)</font>', flags=re.DOTALL)
process_pattern3 = re.compile(r'<font class="PoS" data-kw="([^"]*?)" id="AHD3-PoS-([^_]*?)_([^"]*?)">((?:(?<!</font>).)*?)</font>((?:(?<!<font class=PoS>).)*?)<font class=PoS><b>([^<]*?)</b>((?:(?<!</font>).)*?)</font>', flags=re.DOTALL)
process_pattern4 = re.compile(r'data-kw="([^"]*?)" id="AHD3-PoS-([^_]*?)_([^"]*?)"', flags=re.DOTALL)
def process(v: str) -> str:
    # 对 v 进行加工处理的函数

    # 先处理多个词头和与其紧挨着的词性标志
    v = re.sub(process_pattern1, 
                lambda m: f'{m.group(1)}<b>{m.group(2)}</b>{m.group(3)}<font class="PoS" data-kw="{m.group(2)}" id="AHD3-PoS-{m.group(2).replace(" ", "")}_{m.group(4).replace(" ", "")}"><b>{m.group(4)}</b>{m.group(5)}</font>',
               v
            )

    # # # 先处理继承用法里派生词 <br><b>liʹcensable</b> <font class=PoS><b>adj.</b>（形容词）</font>
    v = re.sub(process_pattern2, 
            lambda m: f'<br><b>{m.group(1)}</b><font class="PoS" data-kw="{m.group(1)}" id="AHD3-PoS-{m.group(1).replace(" ", "")}_{m.group(2).replace(" ", "")}"><b>{m.group(2)}</b>{m.group(3)}</font>',
               v)
    # 处理多个词性的情况，上面的正则一次处理不了全部
    while True:
        mp = process_pattern3.search(v)
        if not mp:
            break

        # print(f"找到多个词性匹配: {mp.group(0)!r}")
        v_new = process_pattern3.sub(
            lambda m: f'<font class="PoS" data-kw="{m.group(1)}" id="AHD3-PoS-{m.group(2)}_{m.group(3)}">{m.group(4)}</font>{m.group(5)}<font class="PoS" data-kw="{m.group(1)}" id="AHD3-PoS-{m.group(2)}_{m.group(6).replace(" ", "")}"><b>{m.group(6)}</b>{m.group(7)}</font>',
            v)
        if v_new == v:
            break
        v = v_new

    # 添加锚点
    ids = re.findall(process_pattern4, v)
    links = "<div id='AHD3-TopLinks'>"
    for id_ in ids:
        links += f'<a href="#AHD3-PoS-{id_[1]}_{id_[2]}">{id_[0]} {id_[2]}</a>' + '|'
    if links.endswith('|'):
        links = links[:-1]
    links += "</div>"
    return links + v


def main() -> int:
    if not filepath.exists():
        print(f"文件不存在: {filepath}", file=sys.stderr)
        return 1

    try:
        entries = build_mapping(filepath)
    except Exception as e:
        print(f"读取或解析文件 {filepath} 出错: {e}", file=sys.stderr)
        return 2

    try:
        entries2 = build_mapping(filepath2)
    except Exception as e:
        print(f"读取或解析文件 {filepath2} 出错: {e}", file=sys.stderr)
        return 3
    
    try:
        entries3 = build_mapping(filepath3) # 未使用  
    except Exception as e:
        print(f"读取或解析文件 {filepath3} 出错: {e}", file=sys.stderr)
        return 4

    print(f"文件: {filepath} -> 已构建条目列表，条目数: {len(entries)}")
    print(f"文件: {filepath2} -> 已构建条目列表，条目数: {len(entries2)}")
    print(f"文件: {filepath3} -> 已构建条目列表，条目数: {len(entries3)}")

    # 构建第二个文件的 key -> 发音
    pronunciation_map2 = {}
    pattern1 = re.compile(r'((?:\([^)]*?|•[^•]*?)?<a href="sound:[^\\]*?\\\\[^\\]+?\\\\(?:(?<!<br>).|(?<!<div ).|(?<!$).)*?)(?:<br>|<div |$)') # 发音部分
    pattern2 = re.compile(r'<font style="font-weight:bold;">[^<]*?</font>') # 带音节划分的词头
    for k, v1 in entries2:
        # 提取发音部分,可能有多个
        m1 = re.findall(pattern1, v1)
        if not m1:
            # print(f"警告: 第二个文件中条目缺少发音部分，已跳过: {k!r}, {v1!r}")
            continue
        for part in m1:
            if k in pronunciation_map2:
                pronunciation_map2[k] += "<br>" + part
            else:
                pronunciation_map2[k] = part

        # 添加音节划分词头。
        m2 = re.search(pattern2, v1)
        if m2:
            pronunciation_map2[k] = m2.group(0) + pronunciation_map2[k]

    print(f"第二个文件发音映射条目数: {len(pronunciation_map2)}")
    # 打印前 10 条示例
    # for i, (k, pron) in enumerate(list(pronunciation_map2.items())[:10]):
    #     print(f"[{i+1}] {k!r} -> {pron!r}")
    
    # 构建第三个文件的 key -> 发音
    pronunciation_map3 = {}
    pattern3 = re.compile(r'<div class="rtseg">((?:(?<!<a ).)*?<a \s*class="sound" \s*href=(?:(?<!</div>).)*?)</div>') # 发音部分
    pattern4 = re.compile(r'<div class="pseg"><i>([^<]*?)</i>') # 词性部分
    for k, v1 in entries3:
        m1 = re.search(pattern3, v1)
        if not m1:
            # print(f"警告: 第三个文件中条目缺少发音部分，已跳过: {k!r}, {v1!r}")
            continue
        pron = m1.group(1) 

        m2 = re.search(pattern4, v1)
        if m2:
            pron += "<i class='word-class'>" + m2.group(1) + "</i>"
            # if k == 'ear' or True:
            #     print(f"找到第三个文件中 key 的词性信息: {k!r} -> {m2.group(1)!r}")

        # 处理重复 key
        if k not in pronunciation_map3:
            pronunciation_map3[k] = pron
        else:
            pronunciation_map3[k] += "<br>" + pron
            # if k == 'ear':
            #     print(f"警告: 第三个文件中 key 重复出现:，已合并发音: {k!r} -> {pronunciation_map3[k]!r}")
    print(f"第三个文件发音映射条目数: {len(pronunciation_map3)}")
    # 打印前 10 条示例
    # for i, (k, pron) in enumerate(list(pronunciation_map3.items())[:10]):
    #     print(f"[{i+1}] {k!r} -> {pron!r}")
    
    # 合并发音到第一个文件的条目中
    for i, (k, v) in enumerate(entries):
        pronunciation2 = pronunciation_map2.get(k, "")
        pronunciation3 = pronunciation_map3.get(k, "")
        # print(f"处理条目 {i+1}/{len(entries)}: {k!r}，发音 WMCD11: {pronunciation2!r}，AHD5: {pronunciation3!r}")
        if not pronunciation2 and not pronunciation3:
            continue
        text_to_add = ""
        if pronunciation2:
            text_to_add += f'<span class="wmcd11-pron">WMCD11: {pronunciation2}</span><br>'
        if pronunciation3:
            text_to_add += f'<span class="ahd5-pron">AHD5: {pronunciation3}</span><br>'
        insert_pos = v.find(r'<br>')
        if insert_pos != -1:
            insert_pos += 4
            v = v[:insert_pos] + text_to_add + v[insert_pos:]
            entries[i] = (k, v)
        # # 插入第三个文件的发音（未使用
        # if k in pronunciation_map3:
        #     pron3 = pronunciation_map3[k]
        #     if not pron3:
        #         continue
        #     # 插入发音到 v 的适当位置
        #     insert_pos = v.find(r'<br>')
        #     if insert_pos != -1:
        #         v = v[:insert_pos + 4] + '<span class="ahd5-pron">AHD5: ' + pron3 + '</span>' + v[insert_pos:]
        #     entries[i] = (k, v)
        # # 插入第二个文件的发音
        # if k in pronunciation_map2:
        #     pron = pronunciation_map2[k]
        #     if not pron:
        #         continue
        #     # 插入发音到 v 的适当位置
        #     insert_pos = v.find(r'<br>')
        #     if insert_pos != -1:
        #         v = v[:insert_pos + 4] + '<span class="wmcd11-pron">WMCD11: ' + pron + '</span>' + v[insert_pos:]
        #     entries[i] = (k, v)

    print(f"合并发音后，条目数: {len(entries)}")
    # 写回合并后的文件
    # 打印前 10 条示例
    # print("合并发音后，前 10 条示例:")
    # for i, (k, v) in enumerate(entries[:10]):
    #     print(f"[{i+1}] {k!r} -> {v!r}")

    # 记录执行消耗时间
    t1 = datetime.datetime.now()
    with filepath_new.open("w", encoding="utf-8", errors="replace") as f:
        f.writelines([f"{k}\n{process(v)}\n</>\n" for k, v in entries])
    t2 = datetime.datetime.now()
    print(f"已写入合并后的文件: {filepath_new}。其中，匹配和添加词性导航链接耗时: {t2 - t1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())