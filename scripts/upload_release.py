#!/usr/bin/env python3
"""Create (or refresh) the big-files Release with the whole PDFs of split books (maintainers only).

Usage:
  python3 scripts/upload_release.py <release_dir> [--force]

<release_dir> is the folder build_from_kebiao.py copied the whole files into.
GitHub renames non-ASCII asset names to default.pdf, so assets keep ASCII names
and carry the Chinese file name as their label.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
RELEASE_DIR = Path(sys.argv[1])
REPO = 'NBrangerF/China-Textbook-New'
TAG = 'big-files'

books = [b for b in json.loads((REPO_DIR / 'catalog.json').read_text())['books'] if b.get('parts')]
notes = ['仓库里超过 95 MB 的教材以分卷存放；这里是整本 PDF，下载后无需合并。', '',
         '| 教材 | 页数 | 大小 | 文件 | SHA-256 |', '|---|---|---|---|---|']
for b in books:
    notes.append(f"| {b['path']} | {b['pages']} | {b['bytes'] / 2**20:.0f} MiB | `{b['release_asset']}` | `{b['sha256'][:16]}…` |")
notes.append('')
notes.append('完整 SHA-256 见仓库的 SHA256SUMS.txt。')
Path(RELEASE_DIR / 'notes.md').write_text('\n'.join(notes) + '\n', encoding='utf-8')

exists = subprocess.run(['gh', 'release', 'view', TAG, '-R', REPO], capture_output=True).returncode == 0
if not exists:
    subprocess.run(['gh', 'release', 'create', TAG, '-R', REPO, '--target', 'main',
                    '--title', '大文件整本下载', '--notes-file', str(RELEASE_DIR / 'notes.md')], check=True)
else:
    subprocess.run(['gh', 'release', 'edit', TAG, '-R', REPO, '--notes-file', str(RELEASE_DIR / 'notes.md')], check=True)

uploaded = set(subprocess.run(['gh', 'release', 'view', TAG, '-R', REPO, '--json', 'assets', '--jq', '.assets[].name'],
                              capture_output=True, text=True, check=True).stdout.split())
for b in books:
    if b['release_asset'] in uploaded and '--force' not in sys.argv:
        continue
    label = Path(b['path']).name
    path = RELEASE_DIR / b['release_asset']
    for attempt in range(5):
        r = subprocess.run(['gh', 'release', 'upload', TAG, '-R', REPO, '--clobber', f'{path}#{label}'])
        if r.returncode == 0:
            print('uploaded', b['release_asset'], label, flush=True)
            break
    else:
        sys.exit(f'upload failed: {path}')
print('RELEASE DONE')
