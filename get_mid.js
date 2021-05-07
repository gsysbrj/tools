import axios from 'axios';
import fs from 'fs/promises';
import moment from 'moment';

const re = /\<div class=\"articleCell SG_j_linedot1\"\>.*?<a title="" target=\"_blank\" href="http:\/\/blog.sina.com.cn\/s\/blog_(.*?)\.html\">(.*?)<\/a>.*?<span class=\"atc_tm SG_txtc\">(.*?)<\/span>/isg;

// const root = '/Users/mac/codes/my/chzhshch';
const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';
const catalog = path + '/目录.html'
const catalogByClass = path + '/目录-分类.html'

let catalogContent = await fs.readFile(catalog, 'utf-8')
let catalogByClassContent = await fs.readFile(catalogByClass, 'utf-8')

const lines = [];

for (let i = 1; i <= 20; i++) {
    const p1 = `http://blog.sina.com.cn/s/articlelist_1215172700_0_${i}.html`;
    
    const content = (await axios.get(p1)).data;
    for (const m of content.matchAll(re)) {
        console.log(m[1],m[2],m[3])
        const time = moment(m[3], "YYYY/M/D H:mm").format('YYYYMMDDHHmm')
        lines.push(`${m[1]}--->${m[2]}--->${time}`)
        catalogContent = catalogContent.replace(new RegExp('(缠中说禅博客'+time+'.*?\.html)', 'igs'), '$1?newsid='+m[1]);
        catalogByClassContent = catalogByClassContent.replace(new RegExp('(缠中说禅博客'+time+'.*?\.html)', 'igs'), '$1?newsid='+m[1]);
    }
}

await fs.writeFile('mid.txt', lines.join('\n'));
await fs.writeFile(catalog, catalogContent)
await fs.writeFile(catalogByClass, catalogByClassContent)
