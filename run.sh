node to_utf8.js && node rename_article.js && node process_content.js

cd /Users/l/codes/chzhshch/fxgan.com
find . -name "*_files/*.png" | xargs -J % cp "%" images
find . -name "*_files/*.gif" | xargs -J % cp "%" images
find . -name "*_files/*.jpeg" | xargs -J % cp "%" images
rm -rf *_files
