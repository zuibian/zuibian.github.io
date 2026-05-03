import re
import os
import sys
import hashlib
from urllib.parse import urlparse
from urllib.request import urlopen

html_path = 'index.html'
res_dir = 'res'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

urls = re.findall(r'src="(https?://[^"]+)"', html)
urls = list(dict.fromkeys(urls))
print(f'Found {len(urls)} unique external image URL(s).')

for url in urls:
    print(url)

print('\nDownloading...')
for url in urls:
    try:
        data = urlopen(url, timeout=30).read()
    except Exception as e:
        print('ERROR downloading', url, e, file=sys.stderr)
        continue
    ext = os.path.splitext(urlparse(url).path)[1]
    if len(ext) > 5 or ext == '':
        ext = '.jpg'
    h = hashlib.sha256(url.encode('utf-8')).hexdigest()[:8]
    local_name = f'external-{h}{ext}'
    local_path = os.path.join(res_dir, local_name)
    with open(local_path, 'wb') as f:
        f.write(data)
    print('Saved', local_name)
    html = html.replace(url, f'res/{local_name}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html with local image paths.')
