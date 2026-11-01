#!/usr/bin/env python3
"""把拆分的大文件（*.pdf.part1、*.pdf.part2 …）合并回整本 PDF，并按 SHA256SUMS.txt 校验。

用法（在仓库根目录）：
  python3 scripts/merge_parts.py            # 合并整个仓库
  python3 scripts/merge_parts.py 小学/科学   # 只合并某个文件夹
"""
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def nfc(s):
    return unicodedata.normalize('NFC', s)


sums = {}
for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    digest, path = line.split('  ', 1)
    sums[nfc(path)] = digest

base = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
groups = {}
for part in base.rglob('*.pdf.part*'):
    m = re.fullmatch(r'(.+\.pdf)\.part(\d+)', part.name)
    if m and not part.name.startswith('._'):  # skip macOS metadata files on exFAT drives
        groups.setdefault(part.with_name(m[1]), []).append((int(m[2]), part))

if not groups:
    print('没有找到需要合并的文件。')
failed = 0
for whole, parts in sorted(groups.items()):
    digest = hashlib.sha256()
    with open(whole, 'wb') as out:
        for _, part in sorted(parts):
            data = part.read_bytes()
            out.write(data)
            digest.update(data)
    rel = nfc(whole.relative_to(ROOT).as_posix())
    ok = sums.get(rel) == digest.hexdigest()
    failed += not ok
    print(('✅ 已合并 ' if ok else '❌ 校验失败，请重新下载分卷：') + rel)
sys.exit(1 if failed else 0)
