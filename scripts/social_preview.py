"""Write the 1280x640 GitHub social preview HTML for China-Textbook-New from catalog.json.

Usage:
  python3 -I scripts/social_preview.py catalog.json /tmp/social.html
  npx -y playwright@1.61.1 screenshot --channel chrome --viewport-size=1280,640 \
    file:///tmp/social.html docs/social-preview.png
Then upload docs/social-preview.png in the repo's Settings → Social preview.

The coverage grid on the right is drawn from the catalog: one block per book,
gold = 2022 revision, outlined = current printing.
"""
import json
import sys

SUBJECTS = ['语文', '数学', '英语', '道德与法治', '科学', '历史', '地理', '地理图册',
            '物理', '化学', '生物学', '体育与健康', '音乐', '美术']
GRADES = range(1, 10)
CELL, GAP, LABEL_W, ROW_H = 28, 6, 96, 30

catalog = json.load(open(sys.argv[1], encoding='utf-8'))
books = catalog['books']
total = len(books)
revised = sum(1 for b in books if b['status'].startswith('2022'))
by_cell = {}
for b in books:
    by_cell.setdefault((b['subject'], b['grade']), []).append(b)

order = {'上册': 0, '下册': 1, '全一册': 0}
rects = []
for row, subject in enumerate(SUBJECTS):
    y = row * ROW_H
    rects.append(f'<text x="{LABEL_W - 12}" y="{y + CELL / 2 + 5}" class="lab">{subject}</text>')
    for col, grade in enumerate(GRADES):
        x = LABEL_W + col * (CELL + GAP)
        cell = sorted(by_cell.get((subject, grade), []), key=lambda b: order[b['volume']])
        if not cell:
            rects.append(f'<rect x="{x + CELL / 2 - 1.5}" y="{y + CELL / 2 - 1.5}" width="3" height="3" class="none"/>')
            continue
        w = (CELL - 3) / 2 if len(cell) == 2 else CELL
        for i, b in enumerate(cell):
            cls = 'new' if b['status'].startswith('2022') else 'cur'
            rects.append(f'<rect x="{x + i * (w + 3):.1f}" y="{y + 2}" width="{w:.1f}" height="{CELL - 4}" rx="2" class="{cls}"/>')
for col, grade in enumerate(GRADES):
    x = LABEL_W + col * (CELL + GAP) + CELL / 2
    rects.append(f'<text x="{x}" y="{len(SUBJECTS) * ROW_H + 16}" class="grade">{grade}</text>')

grid_w = LABEL_W + 9 * (CELL + GAP)
grid_h = len(SUBJECTS) * ROW_H + 24

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin: 0; box-sizing: border-box; }}
body {{ width: 1280px; height: 640px; background: #07080c; color: #eceff4; font-family: 'PingFang SC', sans-serif; overflow: hidden; }}
.wrap {{ position: relative; height: 100%; padding: 64px 72px; display: grid; grid-template-columns: 1fr {grid_w}px; gap: 56px; align-items: center;
  background: radial-gradient(900px 520px at 18% 0%, rgba(233,200,135,.10), transparent 60%); }}
.eyebrow {{ font-family: Menlo, monospace; font-size: 17px; letter-spacing: .22em; color: #e9c887; }}
h1 {{ margin-top: 22px; font-family: 'Songti SC', serif; font-weight: 900; font-size: 64px; line-height: 1.18; letter-spacing: .02em; }}
.en {{ margin-top: 14px; font-size: 26px; color: #c3cad6; letter-spacing: .01em; }}
.stats {{ margin-top: 34px; display: flex; gap: 34px; }}
.stats b {{ display: block; font-family: 'Songti SC', serif; font-size: 44px; font-weight: 900; color: #e9c887; line-height: 1; }}
.stats span {{ display: block; margin-top: 8px; font-size: 17px; color: #c3cad6; }}
.foot {{ margin-top: 40px; display: flex; align-items: center; gap: 12px; font-size: 18px; color: #8b94a2; }}
.foot svg {{ width: 30px; height: 30px; }}
.foot em {{ font-style: normal; color: #eceff4; }}
.grid text {{ font-size: 14px; fill: #8b94a2; }}
.grid .lab {{ text-anchor: end; }}
.grid .grade {{ text-anchor: middle; font-family: Menlo, monospace; font-size: 12px; }}
.grid .new {{ fill: #e9c887; }}
.grid .cur {{ fill: none; stroke: #e9c887; stroke-width: 1.4; opacity: .75; }}
.grid .none {{ fill: rgba(222,228,238,.18); }}
.legend {{ margin-top: 10px; padding-left: {LABEL_W}px; display: flex; gap: 18px; font-size: 13px; color: #8b94a2; }}
.legend i {{ display: inline-block; width: 11px; height: 11px; margin-right: 6px; border-radius: 2px; vertical-align: -1px; }}
</style></head><body><div class="wrap">
<div>
  <div class="eyebrow">CHINA TEXTBOOK NEW</div>
  <h1>中小学最新版<br>电子教材</h1>
  <div class="en">Newest K–9 textbooks of China · 2022 revision</div>
  <div class="stats">
    <div><b>{total}</b><span>本 PDF，一至九年级</span></div>
    <div><b>{revised}</b><span>本 2022 课标修订版</span></div>
    <div><b>逐本</b><span>核对国家平台原文件</span></div>
  </div>
  <div class="foot">
    <svg viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#11131a"/><g transform="translate(2.88 4.46) scale(0.22621)"><path d="M0 33L15 33L15 91L23 84M30.75 0L30.75 46M45 0L45 100M59.25 0L59.25 46M26 4.75L64 4.75M26 23L64 23M26 41.25L64 41.25M23 59L111.5 59M43 64L26 94M47 64L57 81M78 33L102 33M90 59L90 100M77.5 69L68.5 85M102.5 69L111.5 85" fill="none" stroke="#eceff4" stroke-width="9.5"/><circle cx="8.5" cy="9" r="7.6" fill="#e9c887"/></g></svg>
    <span>每一课教哪几条课标，见 <em>kebiao.org</em></span>
  </div>
</div>
<div>
  <svg class="grid" width="{grid_w}" height="{grid_h}" viewBox="0 0 {grid_w} {grid_h}">{''.join(rects)}</svg>
  <div class="legend"><span><i style="background:#e9c887"></i>修订版</span><span><i style="border:1.4px solid #e9c887"></i>现行版</span><span>年级 →</span></div>
</div>
</div></body></html>'''
open(sys.argv[2], 'w', encoding='utf-8').write(html)
print(f'{total} books, {revised} revised, grid {grid_w}x{grid_h}')
