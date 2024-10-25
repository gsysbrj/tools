from pathlib import Path

prefixs = ["_OceanofPDF.com_", "vdoc.pub_"]

for root, dirs, files in Path("C:\\Users\\L\\WPSDrive\\1143379079_2\\WPS云盘\\交易").walk(on_error=print):
    for f in files:
        for prefix in prefixs:
            if f.startswith(prefix):
                old_path = root.joinpath(f)
                new_path = root.joinpath(f.removeprefix(prefix))
                print(old_path, "->", new_path)
                old_path.rename(new_path)
