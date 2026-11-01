#!/usr/bin/env python3
"""对照国家中小学智慧教育平台的公开教材清单，列出需要更新的书（维护者用）。

  python3 scripts/check_updates.py

报告两种情况：
  1. ⏳ 现行版的书，平台已经上线了同一出版社的「根据2022年版课程标准修订」版本；
  2. 平台在本库快照日期之后又更新过某本书的文件。
"""
import json
import sys
import urllib.request
from pathlib import Path

LIST = 'https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/version/data_version.json'
GRADES = '一二三四五六七八九'
REVISED = '根据2022年版课程标准修订'


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def tags(record):
    out = {}
    for t in record.get('tag_list') or []:
        out.setdefault(t['tag_dimension_id'], t['tag_name'])
    return out


catalog = json.loads((Path(__file__).resolve().parent.parent / 'catalog.json').read_text(encoding='utf-8'))
records = []
for url in fetch(LIST)['urls'].split(','):
    records += fetch(url)
by_id = {r['id']: r for r in records}

found = 0
for book in catalog['books']:
    if book['status'].startswith('现行版') and book['subject'] != '地理图册':
        publisher = book['edition'][:2]          # 统编 / 人教 / 人美 / 人音 / 教科 …
        want = (book['stage'], book['subject'], f"{GRADES[book['grade'] - 1]}年级", book['volume'])
        for r in records:
            t = tags(r)
            if ((t.get('zxxxd'), t.get('zxxxk'), t.get('zxxnj'), t.get('zxxcc')) == want
                    and (t.get('zxxbb') or '').startswith(publisher) and REVISED in r['title']):
                found += 1
                print(f"新版已上线：{book['path']}\n  → {r['title']}（{t.get('zxxbb')}，{r['update_time'][:10]}）")
    url = book.get('platform_url') or ''
    if 'contentId=' in url:
        record = by_id.get(url.split('contentId=')[1].split('&')[0])
        if record and record['update_time'][:10] > catalog['snapshot_date']:
            found += 1
            print(f"平台更新过文件：{book['path']}（{record['update_time'][:10]}）")

print(f'共 {found} 处需要更新。' if found else f"没有需要更新的书（快照 {catalog['snapshot_date']}）。")
sys.exit(1 if found else 0)
