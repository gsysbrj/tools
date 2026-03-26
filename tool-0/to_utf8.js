import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';

// 功能把文件转为utf-8编码

// const path = '/Users/mac/codes/my/chzhshch/fxgan.com/';
const path = '/Users/l/codes/chzhshch/fxgan.com/';
const prefix = '缠中说禅博客'

let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html')
                            && !f.name.startsWith(prefix)
                            && !f.name.startsWith('目录')
                            && !f.name.startsWith('首页')
                    )

for (const file of files) {
    console.log(file.name)
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
