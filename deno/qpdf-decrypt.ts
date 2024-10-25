// 使用qpdf批量解密
// deno run --allow-read --allow-run .\qpdf-decrypt.ts

const dir = "D:\\BaiduNetdiskDownload\\经济与金融"

for await (const dirEntry of Deno.readDir(dir)) {
  const file = dirEntry.name
  console.log(file);

  // console.log(Deno.execPath())
  // qpdf --decrypt "" ""
  if (file.endsWith(".pdf")) {
    const file2 = file.slice(0, -4) + "_.pdf"
    const command = new Deno.Command("C:\\Program Files\\qpdf 11.6.3\\bin\\qpdf.exe", {
      cwd: dir,
      args: [
        "--decrypt",
        file,
        file2,
      ],
    });
    const { code, stdout, stderr } = await command.output();
    console.assert(code === 0);
    console.log(new TextDecoder().decode(stdout));
    console.error(new TextDecoder().decode(stderr));
  }
}

export { };
