import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';
import fixNav from './fix_nav.js'

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
    console.log(file.name);
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
    content = content.replace(/<script type="text\/javascript">.*?<\/script>/igs, '');
    // --- 删除style
    content = content.replace(/<style.*?>.*?<\/style>/igs, '');

    // --- 引入a.js和a.css
    if (!content.includes('src="a.js"')) {
        content = content.replace('</head>', '\n<link href="a.css" rel="stylesheet">\n</head>');
        content = content.replace('</body>', '\n<script src="a.js"></script>\n<script src="b.js"></script>\n</body>');
    }
    // 修复一些链接
    content = content.replace(/<a href="http:\/\/fxgan.com\/chan_time.*?">回目录<\/a>/ig, '<a href="目录.html">回目录</a>')
    // 选中“只展示缠师回复”
    content = content.replace(/<input type="checkbox" onclick="toggleGuestReply\(\)">/ig, '<input type="checkbox" checked >')
    // 替换图片路径
    content = content.replace(/\/.*?_files\/(?=.*?\.(gif|jpe?g|png))/ig, '/images/')
    // 添加最新回复
    // if (!content.includes('\"divReply2\"')){
    //     content = content.replace("<div id=\"divReply\">", `<div id="divReply2">
    //     <h2>最新回复</h2>
    //     <reply-item v-for="reply in replyList" :reply="reply" :key="reply.mid"></reply-item>
    // </div>
    // <div id="divReply">`);
    // }
    // 修复上一篇和下一篇链接
    content = fixNav(file.name, content)

    // 以utf8编码写入
    await fs.writeFile(path + '/' + file.name, content);
}
