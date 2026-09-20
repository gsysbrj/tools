
import * as fs from 'node:fs';
import * as readline from 'node:readline';
import { DOMParser, Element } from "jsr:@b-fuze/deno-dom";

const dictDir = "C:\\Users\\L\\Documents\\词典"
const filePath = dictDir + "\\新世纪英汉大词典\\新世纪英汉大词典\\新世纪英汉大词典.txt"
const tempFile = dictDir + "\\新世纪英汉大词典\\新世纪英汉大词典\\新世纪英汉大词典_temp.txt"
const filePathNew = dictDir + "\\新世纪英汉大词典\\新世纪英汉大词典.txt"

// 创建readline接口
const readLineInterface = readline.createInterface({
    input: fs.createReadStream(filePath, { encoding: 'utf-8' }),
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});
const tempFileWriteStream = fs.createWriteStream(tempFile, { encoding: 'utf-8' });

// 合并相同键的值，并将结果写入新文件
const map = new Map<string, string>();
let k = ''
let v = ''
for await (const line of readLineInterface) {
    if (!k) {
        k = line.toLowerCase(); // 将键转换为小写
        continue;
    }
    if (line === '</>') {
        if (map.has(k)) {
            map.set(k, map.get(k)! + v); // 如果已经存在该键，则将新值追加到原值后面
        } else {
            map.set(k, v);
        }
        k = '';
        v = '';
        continue;
    }
    v += line;
}
for (const [k, v] of map) {
    tempFileWriteStream.write(k + '\n' + v + '\n' + '</>\n');
}


const tempFileReadInterface = readline.createInterface({
    input: fs.createReadStream(tempFile, { encoding: 'utf-8' }),
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});
const writeStream = fs.createWriteStream(filePathNew, { encoding: 'utf-8' });

let key = '';
let value = '';
for await (const line of tempFileReadInterface) {
    if (line.startsWith('<link href="ncecd.css" rel="stylesheet"/>')) {
        value += line;
        continue;
    }
    if (line === '</>') {
        const doc = new DOMParser().parseFromString(value, "text/html");
        const navbar = doc.createElement('div');
        navbar.className = 'navbar';
        const posList = doc.querySelectorAll('.class')
        for (let i = 0; i < posList.length; i++) {
            const pos = posList[i];
            if (pos) {
                const kw = pos.closest('.ncecd_con')?.previousElementSibling?.innerHTML.replace(/\s+/g, '_');
                pos.id = 'XSJYHDCD__' + kw + '__' + pos.innerHTML.replace(/\s+/g, '_')
                const a = doc.createElement('a');
                a.className = 'nav-link';
                a.setAttribute('href', '#' + pos.id);
                a.setAttribute('data-index', i.toString());
                a.innerHTML = pos.innerHTML;
                navbar.appendChild(a);
            }
        }
        doc.body.prepend(navbar); // 将导航栏添加到开头
        writeStream.write(key + '\n' + '<link href="ncecd.css" rel="stylesheet" />' + doc.body.innerHTML + '\n' + '</>\n');
        key = '';
        value = '';
        continue;
    }
    key = line;
}
console.log('>>> 文件处理完毕。');
