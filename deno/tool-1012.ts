
import * as fs from 'node:fs';
import * as readline from 'node:readline';
import { DOMParser, Element } from "jsr:@b-fuze/deno-dom@0.1";

const dictDir = "C:\\Users\\L\\Documents\\词典"

const readLineInterface = readline.createInterface({
    input: fs.createReadStream(dictDir + "\\韦氏高阶英汉双解词典完美版\\maldpe\\maldpe.txt", { encoding: 'utf-8' }),
    crlfDelay: Infinity,
});
const writeStream = fs.createWriteStream(dictDir + "\\韦氏高阶英汉双解词典完美版\\maldpe.txt", { encoding: 'utf-8' });

for await (const line of readLineInterface) {
    if (line.startsWith('<link ')) {
        const doc = new DOMParser().parseFromString(line, "text/html");
        const navbar = doc.createElement('div');
        navbar.className = 'navbar';
        const entryList = doc.querySelectorAll('.entry_v2')
        for (let i = 0; i < entryList.length; i++) {
            const entry = entryList[i];
            const hw = entry.querySelector('.hw_txt')?.textContent.trim().replace(/\s+/g, '_');
            const pos = entry.querySelector('.fl')
            if (pos) {
                entry.id = 'MWALECD__' + hw + '__' + pos.textContent.trim().replace(/\s+/g, '_');
                const a = doc.createElement('a');
                a.className = 'nav-link';
                a.setAttribute('href', '#' + entry.id);
                a.setAttribute('data-index', i.toString());
                a.innerHTML = pos.innerHTML;
                navbar.appendChild(a);
            } else {
                const cxs = entry.querySelector('.cxs');
                if (cxs) {
                    entry.id = 'MWALECD__' + hw + '__' + cxs.textContent.trim().replace(/\s+/g, '_');
                    const a = doc.createElement('a');
                    a.className = 'nav-link';
                    a.setAttribute('href', '#' + entry.id);
                    a.setAttribute('data-index', i.toString());
                    
                    a.innerHTML = (cxs.querySelector('.cl')?.textContent || '') + ' ' + (cxs.querySelector('a.cx_link')?.innerHTML || '');
                    console.log(a.innerHTML)
                    navbar.appendChild(a);
                }
            }
        }
        for (let i = 0; i < entryList.length; i++) {
            const entry = entryList[i];
            const navbar_ = navbar.cloneNode(true) as Element;
            const aList = navbar_.querySelectorAll('a');
            for (let j = 0; j < aList.length; j++) {
                const a = aList[j];
                if (a.getAttribute('data-index') === i.toString()) {
                    a.classList.add('active');
                }
            }
            entry.prepend(navbar_); // 将导航栏添加到每个.entry_v2元素的开头
        }
        writeStream.write('<link href="maldpe.css" rel="stylesheet" />' + doc.body.innerHTML + '\n');
    } else {
        writeStream.write(line + '\n');
    }
}
console.log('>>> 文件处理完毕。');
