import re
import subprocess

mdx_txt = r"C:\Users\gsysb\Documents\词典\ODE 3e 20191231M data\ODE 3e 20191231M.mdx.txt"
mdx_new_txt = r"C:\Users\gsysb\Documents\词典\ODE 3e 20191231M data\ODE 3e 20191231M.mdx.new.txt"
mp3_dir = r'C:\Users\gsysb\Documents\词典\ODE 3e 20191231M data\mp3'

# <img src="pr.png"onclick="o0e.a(this,0,'m/mel/melan/melanesia_1_gb_1')"class="a8e"/>
re_link = re.compile(r'<img src="pr\.png"onclick="o0e\.a\(this,0,\'([^\']*)\'\)"class="a8e"/>')
re_cn = re.compile(r'<span class="xxn">(.*?)</span><p class="cn">(.*?)</p>')

def repl(m: re.Match):
    sound_file_name = m.group(1).split('/')[-1].replace('__', '_');
    # print(sound_file_name)
    return '<a href="sound://' + sound_file_name + '.mp3"><img src="pr.png" class="a8e" /></a>'

with open(mdx_txt, encoding='utf8') as fr, open(mdx_new_txt, mode='w', encoding='utf8') as fw:
    for line in fr:
        line = re_link.sub(repl, line)
        line = line.replace('o0e', 'o0e_') # 避免与其他版本的ode3的js代码冲突
        line = line.replace('<div class="Od3">', '<div class="Od3 bilingual">')
        line = line.replace('<script type="text/javascript"src="o3.js"></script><script>ode();</script></div>', '</div><script defer src="o3.js"></script>')
        line = re_cn.sub(r'<span class="xxn">\1<i class="cn">\2</i></span>', line)
        fw.write(line)

subprocess.run([
    "python", 
    "-m", 
    "mdict_utils", 
    "-a", 
    mdx_new_txt, 
    r"C:\Users\gsysb\Documents\词典\ODE 3e 20191231M\ODE 3e 20191231M.mdx",
])
