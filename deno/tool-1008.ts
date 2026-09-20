
import * as fs from 'node:fs';
import * as readline from 'node:readline';

const filePath = "C:\\Users\\L\\Documents\\词典\\英汉大词典（第2版）\\英汉大词典（第2版）_0.txt";
const filePathNew = "C:\\Users\\L\\Documents\\词典\\英汉大词典（第2版）\\英汉大词典（第2版）.txt";
// 文件内容过大，使用流式读取，一次读取一行
const readStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
const writeStream = fs.createWriteStream(filePathNew, { encoding: 'utf-8' });
// 创建readline接口
const rl = readline.createInterface({
    input: readStream,
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});

// 词头
const hwRegex = /<span.*?class="hw".*?homograph="(.*?)".*?>([^<]*)/
const hw2Regex = /<span.*?class="hw".*?>([^<]*)/
// 词性
const posgRegex = /(<div)( class="(?:se1|subse1)">(?:(?<!class="posg"|class="se1"|class="subse1").)*?<div class="posg">(.*?)<\/div>)/g

const target = /^<link.*?href="ecd.css".*?><div id="topAnchor"><\/div><a href="#topAnchor" style="position:fixed;right:0;bottom:0">回到顶部<\/a>.*?(<div class="e" type="standard">|<span class="hw">)/

for await (let line of rl) {
    let anchorLinks = '<div class="top-anchor-links">'
    let hw = ''
    let hwMatch = line.match(hwRegex)
    if (hwMatch) {
        hw = hwMatch[2] + '_' + hwMatch[1]
    } else {
        hwMatch = line.match(hw2Regex)
        if (hwMatch)
            hw = hwMatch[1]
    }
    if (hw) {
        line = line.replaceAll(posgRegex, (_m, p1, p2, p3, offset) => {
            const id = hw + '_offset-' + offset
            anchorLinks += `<a href="#${id}">${p3}</a>|`
            return `${p1} id="${id}"${p2}`
        })
        if (anchorLinks.endsWith('|')) {
            anchorLinks = anchorLinks.slice(0, -1)
        }
        anchorLinks += '</div>'
    } else {
        // console.log('没有发现词头：', line)
    }
    line = line.replace(target, '<link rel="stylesheet" href="ecd.css" />' + anchorLinks + '$1')
    line = line.replace(/<span class="hw" homograph="(\d+)".*?>[^<]*/g, '$&<sup>$1</sup>')
    writeStream.write(`${line}\n`);
}
console.log('>>> 文件处理完毕。');
