from pathlib import Path

for root, dirs, files in Path("C:\\Users\\L\\WPSDrive\\1143379079_2\\WPS云盘\\交易书籍").walk(on_error=print):
    for f in files:
        if "_" in f:
            print(f)
            new_name = f.replace("_", " ")
            print(new_name)
            old_path = root.joinpath(f)
            new_path = root.joinpath(new_name)
            print(old_path, "->", new_path)
            old_path.rename(new_path)
