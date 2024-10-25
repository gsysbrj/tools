// 促使云盘下载文件
// deno run --allow-read --allow-run .\download.ts

const dir = "C:\\Users\\Lei\\WPSDrive\\1143379079\\WPS云盘\\经济与金融"

for await (const dirEntry of Deno.readDir(dir)) {
  const file = dirEntry.name
  console.log(file)

  // console.log(Deno.execPath())
  // qpdf --decrypt "" ""
  if (file.endsWith(".pdf")) {
    const f = await Deno.open(dir + "\\" + file)
    f.close()
  }
}

export { };
