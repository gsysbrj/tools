import axios from 'axios';
import fs from 'fs/promises';
import moment from 'moment';

const root = '/Users/mac/codes/my/chzhshch';
// const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';
const catalog = path + '/目录.html'
const catalogByClass = path + '/目录-分类.html'
const prefix = '缠中说禅博客'

const catalogContent = await fs.readFile(catalog, 'utf-8')
const catalogByClassContent = await fs.readFile(catalogByClass, 'utf-8')
const times = [];
const cats = [];
const reLink = /<li class="liText"><a href="(.*?)" target="_blank">(.*?)\(.*?\)<\/a><\/li>/isg;
for (const m of catalogContent.matchAll(reLink)) {
    times.push({
        url: m[1],
        title: m[2],
    })
}
for (const m of catalogByClassContent.matchAll(reLink)) {
    cats.push({
        url: m[1],
        title: m[2],
    })
}
console.log(`times: ${times.length} cats: ${cats.length}`)

let files = await fs.readdir(path, {
    withFileTypes: true,
});
files = files.filter(f => f.isFile() && f.name.endsWith('.html') && f.name.startsWith(prefix))

for (const file of files) {
    const filePath = path +'/'+ file.name
    let content = await fs.readFile(filePath, 'utf-8')
    const index = times.findIndex(item => item.url.startsWith(file.name))
    const indexCat = cats.findIndex(item => item.url.startsWith(file.name))
    content = content.replace(/<a href=".*?">(上一篇.*?)<\/a>/ig, `<a class="page-prev time" href="${times[index-1]?.url}">上一篇 ${times[index-1]?.title}</a>
<a class="page-prev cat" href="${cats[indexCat-1]?.url}">上一篇 ${cats[indexCat-1]?.title}</a>`)
    content = content.replace(/<a href=".*?">(下一篇.*?)<\/a>/ig, `<a class="page-next time" href="${times[index+1]?.url}">下一篇 ${times[index+1]?.title}</a>
<a class="page-next cat" href="${cats[indexCat+1]?.url}">下一篇 ${cats[indexCat+1]?.title}</a>`)

    // 以utf8编码写入
    await fs.writeFile(filePath, content);
}
