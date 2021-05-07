import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';

// const root = '/Users/mac/codes/my/chzhshch';
const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';
const catalog = path + '/目录.html'
const catalogByClass = path + '/目录-分类.html'

const reLink = /<li class="liText"><a href="(.*?)" target="_blank">(.*?)\((.*?)\)<\/a><\/li>/isg;

const prefix = '缠中说禅博客'

async function process (path) {
    let content = await fs.readFile(path, 'utf-8')
    content = content.replace(reLink, function(match, fileName, title, pubtime) {
        const time = moment(pubtime, "YYYY/M/D H:mm:ss").format('YYYYMMDDHHmmss')
        pubtime = moment(pubtime, "YYYY/M/D H:mm:ss").format('YYYY/M/D H:mm:ss') // 消除其中的换行等空白
        const newFileName = prefix + time + '.html'
        const replacement = `<li class="liText"><a href="${newFileName}" target="_blank">${title}(${pubtime})</a></li>`
        console.log(replacement)
        return replacement;
    });
    console.log(content)
    await fs.writeFile(path, content);  
}

process(catalog)
process(catalogByClass)
