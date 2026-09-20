
import * as fs from 'node:fs';
import * as readline from 'node:readline';
import { DOMParser, Element } from "jsr:@b-fuze/deno-dom";

const dictDir = "C:\\Users\\L\\Documents\\词典"
const filePath = dictDir + "\\21世纪大英汉词典\\21世纪大英汉词典\\21世纪大英汉词典.txt"
const filePathNew = dictDir + "\\21世纪大英汉词典\\21世纪大英汉词典.txt"
// 文件内容过大，使用流式读取，一次读取一行
const readStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
const writeStream = fs.createWriteStream(filePathNew, { encoding: 'utf-8' });
// 创建readline接口
const rl = readline.createInterface({
    input: readStream,
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});

for await (const line of rl) {
    if (line.startsWith('<span class="word">')) {
        const doc = new DOMParser().parseFromString(line, "text/html");
        const hw = doc.querySelector('.return-phrase .l .i')?.innerHTML.replace(/\s+/g, '_');
        const navbar = doc.createElement('div');
        navbar.className = 'navbar';
        const oaldList = doc.querySelectorAll('.trs')
        for (let i = 0; i < oaldList.length; i++) {
            const oald = oaldList[i];
            const pos = oald.querySelector('.pos')
            if (pos) {
                oald.id = '21SJDYHCD__' + hw + '__' + pos.innerHTML.replace(/\s+/g, '_').toLowerCase();
                const a = doc.createElement('a');
                a.className = 'nav-link';
                a.setAttribute('href', '#' + oald.id);
                a.setAttribute('data-index', i.toString());
                a.innerHTML = pos.innerHTML;
                navbar.appendChild(a);
            }
        }
        doc.querySelector('.word')?.prepend(navbar); // 将导航栏添加到.word元素的开头
        writeStream.write(doc.body.innerHTML + '\n');
    } else {
        writeStream.write(line + '\n');
    }
}
console.log('>>> 文件处理完毕。');
