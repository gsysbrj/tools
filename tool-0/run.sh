node to_utf8.js && node rename_article.js && node process_content.js && node fix_nav.js

cd /Users/l/codes/chzhshch/fxgan.com
find *_files -name "*.png" | xargs -J % cp "%" images
find *_files -name "*.gif" | xargs -J % cp "%" images
find *_files -name "*.jpeg" | xargs -J % cp "%" images
find *_files -name "*.jpg" | xargs -J % cp "%" images
rm -rf *_files
