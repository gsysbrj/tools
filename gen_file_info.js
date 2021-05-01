import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';

// 生成文件信息
// const root = '/Users/mac/codes/my/chzhshch';
const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';
const catalog = path + '/目录.html'
const catalogByClass = root + '/目录-分类.html'

const reTitle = /<h1>(.*?)<\/h1>/;
const rePubtime = /<span class="pubtime">(.*?)<\/span>/;

const lines = [];
const infoFilePath = root + '/info.txt'
const prefix = '缠中说禅博客'

let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html'))
for (const file of files) {
    if (file.name.startsWith(prefix)) {
        continue
    }
    let filePath = path +'/'+ file.name
    let data = await fs.readFile(filePath)
    let info = jschardet.detect(data)
    if (info.encoding === 'UTF-8') {
        const content = iconv.decode(data, info.encoding);
        const titleMatch = content.match(reTitle)
        if (titleMatch) {
            const title = titleMatch[1]
            const pubtimeMatch = content.match(rePubtime)
            const pubtime = pubtimeMatch[1]
            const time = moment(pubtime, "YYYY/M/D H:mm:ss").format('YYYYMMDDHHmmss')
            const newFileName = prefix + time + '.html'
            const line = `${file.name}--->${newFileName}--->${title}--->（${pubtime}）`;
            console.log(line)
            lines.push(line)
        } else {
            console.log(filePath + ': title not found')
        }
    }
}
await fs.writeFile(infoFilePath, lines.join('\n'));
