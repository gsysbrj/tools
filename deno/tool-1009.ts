
import * as fs from 'node:fs';
import * as readline from 'node:readline';
import { DOMParser, Element } from "jsr:@b-fuze/deno-dom";

const dictDir = "C:\\Users\\L\\Documents\\词典"
const filePath = dictDir + "\\牛津高阶英汉双解词典第10版完美版\\oaldpe\\oaldpe.txt"
const filePathNew = dictDir + "\\牛津高阶英汉双解词典第10版完美版\\oaldpe.txt"
// 文件内容过大，使用流式读取，一次读取一行
const readStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
const writeStream = fs.createWriteStream(filePathNew, { encoding: 'utf-8' });
// 创建readline接口
const rl = readline.createInterface({
    input: readStream,
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});

for await (const line of rl) {
    if (line.startsWith('<link ')) {
        const doc = new DOMParser().parseFromString(line, "text/html");
        const navbar = doc.createElement('div');
        navbar.className = 'navbar';
        const oaldList = doc.querySelectorAll('.oald')
        for (let i = 0; i < oaldList.length; i++) {
            const oald = oaldList[i];
            const hw = oald.querySelector('.headword')
            const pos = oald.querySelector('.pos')
            if (pos) {
                oald.id = 'oald_' + hw?.id + '_' + pos.innerHTML.replace(/\s+/g, '-').toLowerCase();
                const a = doc.createElement('a');
                a.className = 'nav-link';
                a.setAttribute('href', '#' + oald.id);
                a.setAttribute('data-index', i.toString());
                a.innerHTML = pos.innerHTML;
                navbar.appendChild(a);
            }
        }
        for (let i = 0; i < oaldList.length; i++) {
            const oald = oaldList[i];
            const navbar_ = navbar.cloneNode(true) as Element;
            const aList = navbar_.querySelectorAll('a');
            for (let j = 0; j < aList.length; j++) {
                const a = aList[j];
                if (a.getAttribute('data-index') === i.toString()) {
                    a.classList.add('active');
                }
            }
            oald.prepend(navbar_); // 将导航栏添加到每个.oald元素的开头
        }
        writeStream.write('<link href="oaldpe.css" rel="stylesheet"><script src="oaldpe.js"></script>' + doc.body.innerHTML + '\n');
    } else {
        writeStream.write(line + '\n');
    }
}
console.log('>>> 文件处理完毕。');
