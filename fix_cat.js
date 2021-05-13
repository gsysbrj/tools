import fs from 'fs/promises';
import jschardet from "jschardet";
import iconv from 'iconv-lite';
import moment from 'moment';

// 目录-分类添加 from=cat
const root = '/Users/mac/codes/my/chzhshch';
// const root = '/Users/l/codes/chzhshch';
const path = root + '/fxgan.com';
const catalog = path + '/目录.html'
const catalogByClass = path + '/目录-分类.html'

const reLink = /"(缠中说禅.*?\.html.*?)"/isg;

let content = await fs.readFile(catalogByClass, 'utf-8')
content = content.replace(reLink, function(match, url) {
    if (url.endsWith('.html')) {
        url += '?'
    } else {
        url += '&'
    }
    url += 'from=cat'
    const replacement = `"${url}"`
    return replacement;
});
await fs.writeFile(catalogByClass, content);
