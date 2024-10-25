import { walk } from "jsr:@std/fs";

import { walkSync } from "jsr:@std/fs";

// 批量改名

const dir = "C:\\Users\\L\\WPSDrive\\1143379079_2\\WPS云盘\\交易"

for await (const entry of walk(dir)) {
  console.log(entry.path)
  console.log(entry.name)
}
