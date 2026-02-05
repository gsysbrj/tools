/**
 * 处理牛津高阶英汉双解词典第10版完美版的oaldpe.txt文件，
 * 将每个单词条目中的英式发音部分放在美式发音部分之后，
 * 并将例句中英式发音放在美式发音之后。
 */
// 使用nodejs读取文本文件全部内容
import * as fs from 'fs';
import * as readline from 'readline';

const filePath = "C:\\123pan\\Downloads\\牛津高阶英汉双解词典第10版完美版\\oaldpe\\oaldpe.txt";
const filePathNew = "C:\\123pan\\Downloads\\牛津高阶英汉双解词典第10版完美版\\oaldpe\\oaldpe_new.txt";
// 文件内容过大，使用流式读取，一次读取一行
const readStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
const writeStream = fs.createWriteStream(filePathNew, { encoding: 'utf-8' });
// 创建readline接口
const rl = readline.createInterface({
    input: readStream,
    crlfDelay: Infinity // 自动识别所有CR/LF换行符
});


const defTagRegex = /<span \s*class="phonetics"\s*>\s*(<div \s*class="phons_br"\s*>.*?<\/div>)\s*(<div \s*class="phons_n_am"\s*>.*?<\/div>)\s*<\/span>/gs;
const defTagRegex2 = /<example-audio>\s*(<a [^<>]*class="audio_uk"[^<>]*?>.*?<\/a>)\s*(<a [^<>]*?class="audio_us"[^<>]*?>.*?<\/a>)\s*<\/example-audio>/gs;

// 使用for await...of循环逐行迭代
try {
    let wordContent = '';
    let count = 0;
    for await (const line of rl) {
        if (line === '</>') {
            count++;
            console.log('>>> count: ', count, '>>> 处理单词: ', wordContent.slice(0, 100));
            wordContent = processContent(wordContent);
            writeStream.write(`${wordContent}${line}\n`);
            wordContent = ''; // 重置wordContent
        } else {
            wordContent += line + '\n'; // 累积wordContent
        }
    }
    console.log('>>> 文件处理完毕。count: ', count);
} catch (err) {
    console.error('>>> 处理文件时发生错误:', err);
}

function processContent(wordContent: string): string {
    // 使用正则表达式替换
    wordContent = wordContent.replace(defTagRegex, '<span class="phonetics">$2$1</span>');
    wordContent = wordContent.replace(defTagRegex2, '<example-audio>$2$1</example-audio>');
    return wordContent;
}
