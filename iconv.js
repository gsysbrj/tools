
import fs from 'fs/promises';
import iconv from 'iconv-lite';

const path = '/Users/mac/codes/my/chzhshch/fxgan.com/';

const files = await fs.readdir(path, {
    withFileTypes: true,
});
for (const file of files) {
    if (file.isFile()) {
        console.log(file.name)
        let content = await fs.readFile(path + file.name, {
            // encoding: 'GBK',
        })
        // console.log(content)
        // 若是GBK编码，则以gbk解码
        if (content.includes('charset=GBK', 0, 'UTF8')) {
            content = iconv.decode(content, 'gbk');
            content = content.replace('charset=GBK', 'charset=UTF8')
        } else {
            content = iconv.decode(content, 'UTF8');
        }
        // 添加适配移动设备的meta
        if (!content.includes('device-width')) {
            content = content.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n');
        }

        // 以utf8编码写入
        fs.writeFile(path + file.name, content, {
            encoding: 'utf8',
        });
    }
}
