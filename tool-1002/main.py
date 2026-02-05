# 处理德汉词典

import re

file_path = 'C:\\123pan\\Downloads\\德汉词典\\德汉词典.txt'
file_path_new = 'C:\\123pan\\Downloads\\德汉词典\\德汉词典_new.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    with open(file_path_new, 'w', encoding='utf-8') as f_new:
        keyword = ''
        content = ''
        count = 0
        count_not_empty = 0
        p1 = re.compile(r'\(.*?\)')  
        p2 = re.compile(r'\((.*?)\)') 
        for line in f:
            line = line.strip()
            if line == '</>':
                count += 1
                # 写入文件
                f_new.write(f'{keyword}\n{content}\n{line}\n')

                # 词首可能是包含逗号分隔的多个词，如果是，则添加多个词条LINK
                print('发现多个词首:' + keyword) # 形如 voll|gepackt, ～gepfropft, ～gestopft
                kws = keyword.split(',')
                for kw in kws:
                    if '～' in kw:
                        kw = kw.replace('～', kws[0].split('|')[0].strip())
                    kw = kw.replace('·', '').replace('ˈ', '').replace('ˌ', '').replace('*', '').replace('|', '').strip()
                    if kw != '':
                        kw = kw.replace('()', '')  # 去掉空括号
                        if kw != '' and kw != keyword:
                            f_new.write(f'{kw}\n@@@LINK={keyword}\n{line}\n')
                            if re.search(p1, kw):
                                f_new.write(f'{re.sub(p1, "", kw)}\n@@@LINK={keyword}\n{line}\n') # 去掉括号部分的版本
                                f_new.write(f'{re.sub(p2, r"\1", kw)}\n@@@LINK={keyword}\n{line}\n') # 保留括号内部分的版本

                keyword = ''
                content = ''
                count_not_empty += 1
            elif keyword == '':
                keyword = line
            else:
                content += line # 把多行内容合并为一行
        print(f'处理完成，共处理{count}条词目，其中非空词目{count_not_empty}条。')
