import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';

// 生成文件信息
// const root = '/Users/mac/codes/my/chzhshch';
const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';

const reTitle = /<h1>(.*?)<\/h1>/;
const rePubtime = /<span class="pubtime">(.*?)<\/span>/;

const prefix = '缠中说禅博客'
const lines = []
let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html')
                            && !f.name.startsWith(prefix)
                            && !f.name.startsWith('目录')
                            && !f.name.startsWith('首页')
                    )
for (const file of files) {
    let filePath = path +'/'+ file.name
    let content = await fs.readFile(filePath, 'utf-8')
    const titleMatch = content.match(reTitle)
    if (titleMatch) {
        const title = titleMatch[1]
        const pubtimeMatch = content.match(rePubtime)
        const pubtime = pubtimeMatch[1]
        const time = moment(pubtime, "YYYY/M/D H:mm:ss").format('YYYYMMDDHHmmss')
        const newFileName = prefix + time + '.html'
        const oldFilesDirName = file.name.slice(0, -5) + '_files'
        const neweFilesDirName = prefix + time + '_files'
        const line = `${oldFilesDirName}--->${neweFilesDirName}--->${newFileName}--->（${pubtime}）`;
        // 替换文件内容中的目录名
        content = content.split(oldFilesDirName).join(neweFilesDirName);
        console.log(line)
        // 替换完写回内容
        await fs.writeFile(filePath, content)
        // 新文件名若存在删除之
        await fs.rm(path + '/' + newFileName, {
            force: true,
            recursive: true,
        })
        await fs.rm(path + '/' + neweFilesDirName, {
            force: true,
            recursive: true,
        })
        // 重命名
        await fs.rename(filePath, path + '/' + newFileName)
        await fs.rename(path + '/' + oldFilesDirName, path + '/' + neweFilesDirName)
        lines.push(line)
    } else {
        console.log(filePath + ': title not found')
    }
}

await fs.writeFile('info.txt', lines.join('\n'))
