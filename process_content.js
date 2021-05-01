import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';

// 生成文件信息
// const root = '/Users/mac/codes/my/chzhshch';
const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';

const prefix = '缠中说禅博客'
let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html') && f.name.startsWith(prefix))

for (const file of files) {
    let filePath = path +'/'+ file.name
    let content = await fs.readFile(filePath, 'utf-8')
    // 添加适配移动设备的meta
    if (!content.includes('device-width')) {
        content = content.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n');
    }
    // --- 替换html5的doctype
    content = content.replace(/<!DOCTYPE html .*?>/si, '<!DOCTYPE html>');
    // --- 删除hm.js和jquery-1.11.0.min.js引用
    content = content.replace(/<script src=\".*?_files\/hm.js\"><\/script>/igs, '');
    content = content.replace(/<script type="text\/javascript" src=".\/.*?_files\/jquery-1.11.0.min.js"><\/script>/igs, '');
    content = content.replace(/<script type="text\/javascript">window.onerror.*?<\/script>/igs, '');
    // --- 引入a.js和a.css
    if (!content.includes('src="a.js"')) {
        content = content.replace('</head>', '\n<script type="text/javascript" src="a.js"></script>\n<link href="a.css" rel="stylesheet">\n</head>');
    }
    // 修复一些链接
    content = content.replace(/<a href="http:\/\/fxgan.com\/chan_time.*?">回目录<\/a>/ig, '<a href="目录.html">回目录</a>')

    // 以utf8编码写入
    await fs.writeFile(path + '/' + file.name, content);
}
