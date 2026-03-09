# 处理韦氏高阶的音频文件，改名字

import re
import os
from pathlib import Path
import shutil
import urllib.parse
import subprocess
import datetime

file_path_old = 'C:\\123pan\\Downloads\\maldpe_new_data\\maldpe_new_0.txt'
file_path_new = 'C:\\123pan\\Downloads\\maldpe_new_data\\maldpe_new.txt'

with open(file_path_old, 'r', encoding='utf-8') as f:
    with open(file_path_new, 'w', encoding='utf-8') as f_new:
        t0 = datetime.datetime.now()
        count = 0
        for line in f:
            if line.startswith('<link'):
                targets = re.findall(r'id="(maldpe_\d+_[^"_]+_([^"_]+))"', line, flags=re.DOTALL)
                if len(targets) != 0:
                    count += 1
                    anchors = '<div class="fl-anchors">'
                    for g1, g2 in targets:
                        # <a href="#maldpe_1_borne_adjective" class="fl-anchor">adjective</a>|
                        # print(g1, g2)
                        anchors += f'<a href="#{g1}" class="fl-anchor">{g2}</a>|'
                    if anchors.endswith('|'):
                        anchors = anchors[0:-1]
                    anchors += '</div>'
                    # print(anchors)
                    line = re.sub(r'<div class="fl-anchors">.*?</div>', anchors, line)
                f_new.write(f'{line}')
            else:
                f_new.write(f'{line}') 
        t1 = datetime.datetime.now()
        print(f'处理完成，共处理{count}条词目, 耗时{t1 - t0}。')
