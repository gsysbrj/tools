import re
import subprocess

mdx_txt = r"D:\\词典\\韦氏高阶英汉双解词典完美版\\mdx\\maldpe.mdx.txt"
mdx_new_txt = r"D:\\词典\\韦氏高阶英汉双解词典完美版\\mdx\\maldpe.mdx.new.txt"

re_link = re.compile(r'<a class="dx_link" href="entry://([^"#]*)">\s*<sup>(\d+)</sup>([^<]*)</a>')

with open(mdx_txt, encoding='utf8') as fr, open(mdx_new_txt, mode='w', encoding='utf8') as fw:
    for line in fr:
        line = re_link.sub(r'<a class="dx_link" href="entry://\1#\1_\2__q"><sup>\2</sup>\3</a>', line)
        line = re.sub(r'>\s*<', '><', line)
        # 添加libs.css和libs.js引用
        line = line.replace(
            '<link href="maldpe.css" rel="stylesheet" type="text/css">',
            '<link href="libs.css" rel="stylesheet" type="text/css"><link href="maldpe.css" rel="stylesheet" type="text/css">',
        )
        line = line.replace(
            '<script src="maldpe-jquery-3.6.0.min.js"></script>',
            '<script src="libs.js"></script>',
        )
        line = line.replace(
            '<script src="maldpe-crypto-js.min.js"></script>',
            '',
        )

        fw.write(line)

subprocess.run([
    "python", 
    "-m", 
    "mdict_utils", 
    "-a", 
    r"D:\\词典\\韦氏高阶英汉双解词典完美版\\mdx\\maldpe.mdx.new.txt", 
    r"D:\\词典\\韦氏高阶英汉双解词典完美版\\maldpe.mdx",
])
