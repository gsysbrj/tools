import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';

// 功能把文件转为utf-8编码

// const path = '/Users/mac/codes/my/chzhshch/fxgan.com/';
const path = '/Users/l/codes/chzhshch/fxgan.com/';

let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html'))
for (const file of files) {
    let filePath = path + file.name
    let content = await fs.readFile(filePath)
    let info = jschardet.detect(content)
    if (info.encoding !== 'UTF-8') {
        console.log(file.name, info)
        content = iconv.decode(content, info.encoding);
        content = content.replace(/<meta.*?charset.*?>/i, '<meta charset="utf-8">')
        await fs.writeFile(filePath, content)
    }
}
