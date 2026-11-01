#!/usr/bin/env python3
"""Build this repository from a kebiao.org textbook library generation (maintainers only).

Usage:
  python3 scripts/build_from_kebiao.py <asset_manifest.jsonl> <library_root> <release_dir>

Copies each book into 学段/学科/版本/, splits files over SPLIT_AT bytes into parts
(the whole file goes to <release_dir> for the GitHub Release), and writes
catalog.json, SHA256SUMS.txt, .gitignore and README.md.
"""
import hashlib
import json
import shutil
import sys
import unicodedata
import urllib.request
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
GITHUB = 'https://github.com/NBrangerF/China-Textbook-New'
KEBIAO = 'https://www.kebiao.org'
RELEASE_TAG = 'big-files'
SPLIT_AT = 95_000_000          # GitHub rejects files over 100 MiB
PART_SIZE = 90 * 1024 * 1024
CONTENT_DIRS = ['小学', '初中']

STAGES = {'primary': '小学', 'junior': '初中'}
GRADES = '一二三四五六七八九'
SUBJECT_ORDER = ['语文', '数学', '英语', '道德与法治', '科学', '历史', '地理', '地理图册',
                 '物理', '化学', '生物学', '体育与健康', '音乐', '美术']
VOLUME_ORDER = {'上册': 0, '下册': 1, '全一册': 2}
VOLUME_SLUG = {'上册': '1', '下册': '2', '全一册': '0'}
VOLUME_SHORT = {'上册': '上', '下册': '下', '全一册': '全一册'}
STATUS = {
    'new': '2022 课标修订版',
    'current': '现行版（平台尚未发布修订版）',
    'atlas': '现行版（配套图册，平台不提供）',
}
MARK = {'new': '✅', 'current': '⏳', 'atlas': '⏳'}


def nfc(s):
    return unicodedata.normalize('NFC', str(s))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def status_of(row):
    if row['revision_status'] == 'current_2022_revision':
        return 'new'
    return 'atlas' if row['resource_type'] == 'student_companion' else 'current'


def source_of(row):
    if row.get('source_kind') == 'local_platform_pdf':
        return '国家中小学智慧教育平台'
    return 'TapXWorld/ChinaTextbook（平台尚无新版时沿用）'


def kebiao_editions():
    """Edition ids that have a book page on kebiao.org right now."""
    ids, offset = set(), 0
    while True:
        with urllib.request.urlopen(f'{KEBIAO}/api/v1/textbooks?limit=200&offset={offset}', timeout=60) as r:
            body = json.load(r)
        ids.update(item['edition_id'] for item in body['data'])
        offset += len(body['data'])
        if not body['data'] or offset >= body['meta']['total']:
            return ids


def load_books(manifest, live):
    books = []
    for line in open(manifest, encoding='utf-8'):
        row = json.loads(line)
        # Only official books; skip unofficial early copies of future terms.
        if row['revision_status'].startswith('future_candidate'):
            continue
        stage = STAGES[row['stage']]
        grade = f"{GRADES[row['grade'] - 1]}年级"
        edition = row['edition_name']
        name = f"{row['subject']}{grade}{row['volume']}·{edition}.pdf"
        books.append({
            'path': f"{stage}/{row['subject']}/{edition}/{name}",
            'stage': stage,
            'subject': row['subject'],
            'grade': row['grade'],
            'volume': row['volume'],
            'edition': edition,
            'status': STATUS[status_of(row)],
            'pages': row['pages'],
            'bytes': row['bytes'],
            'sha256': row['sha256'],
            'platform_md5': row.get('source_md5'),
            'platform_url': row.get('source_url'),
            'kebiao_url': f"{KEBIAO}/textbooks/{row['edition_id']}" if row['edition_id'] in live else None,
            'source': source_of(row),
            '_status_key': status_of(row),
            '_object': row['object_path'],
            '_asset': f"{row['stage']}-{row['subject_slug']}-g{row['grade']}-{VOLUME_SLUG[row['volume']]}.pdf",
        })
    rank = {s: i for i, s in enumerate(SUBJECT_ORDER)}
    books.sort(key=lambda b: (b['stage'] != '小学', rank.get(b['subject'], len(rank)), b['subject'],
                              b['grade'], VOLUME_ORDER[b['volume']]))
    return books


def place(book, library_root, release_dir, verified):
    """Write the book (or its parts) into the repo; return the repo files it owns.

    `verified` maps path -> sha256 from the previous SHA256SUMS.txt, which is only
    written after every file was checked, so matching sizes there skip re-hashing.
    """
    src = Path(library_root) / book['_object']
    dest = REPO / book['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    known = verified.get(nfc(book['path'])) == book['sha256']

    if book['bytes'] <= SPLIT_AT:
        if not (known and dest.exists() and dest.stat().st_size == book['bytes']):
            shutil.copyfile(src, dest)
            if sha256_of(dest) != book['sha256']:
                sys.exit(f'checksum mismatch after copy: {dest}')
        return [dest]

    whole = Path(release_dir) / book['_asset']
    count = -(-book['bytes'] // PART_SIZE)
    parts = [dest.with_name(f'{dest.name}.part{i}') for i in range(1, count + 1)]
    sizes_ok = (whole.exists() and whole.stat().st_size == book['bytes']
                and all(p.exists() for p in parts) and sum(p.stat().st_size for p in parts) == book['bytes'])
    if not (known and sizes_ok):
        shutil.copyfile(src, whole)
        if sha256_of(whole) != book['sha256']:
            sys.exit(f'checksum mismatch after copy: {whole}')
        with open(whole, 'rb') as f:
            for part in parts:
                part.write_bytes(f.read(PART_SIZE))
    book['parts'] = [str(p.relative_to(REPO)) for p in parts]
    book['download_url'] = f"{GITHUB}/releases/download/{RELEASE_TAG}/{book['_asset']}"
    book['release_asset'] = book['_asset']
    return parts


def link(path):
    return quote(path)


def badge(label, message, color):
    def esc(s):
        return quote(str(s).replace('-', '--').replace('_', '__').replace(' ', '_'))
    return f'https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color}'


def subjects_of(books, stage):
    out = []
    for b in books:
        if b['stage'] == stage and b['subject'] not in out:
            out.append(b['subject'])
    return out


def main_edition(group):
    editions = [b['edition'] for b in group]
    return max(dict.fromkeys(editions), key=editions.count)


def overview(books):
    """学科 × 年级 grid: one screen to find any book."""
    out = []
    for stage, grades in (('小学', range(1, 7)), ('初中', range(7, 10))):
        out.append(f'**{stage}**\n')
        out.append('| 学科 | ' + ' | '.join(f'{GRADES[g - 1]}年级' for g in grades) + ' |')
        out.append('|---|' + '---|' * len(grades))
        for subject in subjects_of(books, stage):
            group = [b for b in books if b['stage'] == stage and b['subject'] == subject]
            row = [f"[{subject}](#{quote(stage + subject)})"]
            for g in grades:
                links = []
                for b in sorted((b for b in group if b['grade'] == g), key=lambda b: VOLUME_ORDER[b['volume']]):
                    href = b.get('download_url') or link(b['path'])
                    mark = '' if b['_status_key'] == 'new' else '⏳'
                    links.append(f"[{VOLUME_SHORT[b['volume']]}]({href}){mark}")
                row.append(' · '.join(links) or '')
            out.append('| ' + ' | '.join(row) + ' |')
        out.append('')
    return '\n'.join(out)


def cell(book, main):
    href = book.get('download_url') or link(book['path'])
    text = f"{MARK[book['_status_key']]} [{book['volume']}]({href}) · {book['pages']} 页 · {book['bytes'] / 1e6:.0f} MB"
    if book['edition'] != main:
        text += f"<br><sub>{book['edition']}</sub>"
    extra = []
    if book.get('kebiao_url'):
        extra.append(f"[课标对应]({book['kebiao_url']})")
    if book.get('platform_url'):
        extra.append(f"[平台原页]({book['platform_url']})")
    if extra:
        text += '<br>' + ' · '.join(extra)
    return text


def details(books):
    out = []
    for stage in ['小学', '初中']:
        out.append(f'### {stage}\n')
        for subject in subjects_of(books, stage):
            group = [b for b in books if b['stage'] == stage and b['subject'] == subject]
            main = main_edition(group)
            volumes = sorted({b['volume'] for b in group}, key=VOLUME_ORDER.get)
            # The anchor overview() links to: a hidden <a name> keeps it stable across headings.
            out.append(f'<a name="{stage}{subject}"></a>\n')
            out.append(f'#### {stage}{subject} · {main}　<sub>[打开文件夹]({link(stage + "/" + subject)})</sub>\n')
            out.append('| 年级 | ' + ' | '.join(volumes) + ' |')
            out.append('|---|' + '---|' * len(volumes))
            for grade in sorted({b['grade'] for b in group}):
                row = [f'{GRADES[grade - 1]}年级']
                for v in volumes:
                    hit = [b for b in group if b['grade'] == grade and b['volume'] == v]
                    row.append(cell(hit[0], main) if hit else '—')
                out.append('| ' + ' | '.join(row) + ' |')
            out.append('')
    return '\n'.join(out)


def write_readme(books, snapshot):
    count = {k: sum(1 for b in books if b['_status_key'] == k) for k in MARK}
    values = {
        'DATE': snapshot,
        'TOTAL': len(books),
        'NEW': count['new'],
        'CURRENT': count['current'],
        'ATLAS': count['atlas'],
        'SIZE_GB': f"{sum(b['bytes'] for b in books) / 1e9:.1f}",
        'SPLIT_COUNT': sum(1 for b in books if b.get('parts')),
        'PLATFORM': sum(1 for b in books if b.get('platform_md5')),
        'LEGACY': sum(1 for b in books if not b.get('platform_md5')),
        'KEBIAO_COUNT': sum(1 for b in books if b.get('kebiao_url')),
        'BADGE_TOTAL': badge('教材', f'{len(books)} 本', '2f4f4f'),
        'BADGE_NEW': badge('2022 课标修订版', f"{count['new']} 本", 'c9a227'),
        'BADGE_DATE': badge('更新', snapshot, '555555'),
        'BADGE_KEBIAO': badge('配套网站', 'kebiao.org', '1f2937'),
        'OVERVIEW': overview(books),
        'DETAILS': details(books),
    }
    readme = (REPO / 'scripts' / 'README.template.md').read_text(encoding='utf-8')
    for key, value in values.items():
        readme = readme.replace('{{' + key + '}}', str(value))
    if '{{' in readme:
        sys.exit('unfilled placeholder in README template')
    (REPO / 'README.md').write_text(readme, encoding='utf-8')


def main():
    manifest, library_root, release_dir = sys.argv[1:4]
    Path(release_dir).mkdir(parents=True, exist_ok=True)
    books = load_books(manifest, kebiao_editions())

    verified = {}
    sums = REPO / 'SHA256SUMS.txt'
    if sums.exists():
        for line in sums.read_text(encoding='utf-8').splitlines():
            digest, path = line.split('  ', 1)
            verified[nfc(path)] = digest

    owned = set()
    for b in books:
        owned.update(place(b, library_root, release_dir, verified))

    # Remove books that left the library (e.g. replaced by a new printing).
    # Compare NFC forms: the drive may hand names back decomposed.
    keep = {nfc(p) for p in owned}
    for d in CONTENT_DIRS:
        for p in (REPO / d).rglob('*'):
            if p.is_file() and not p.name.startswith('._') and nfc(p) not in keep:
                print('removing', p.relative_to(REPO))
                p.unlink()

    public = [{k: v for k, v in b.items() if not k.startswith('_')} for b in books]
    snapshot = max(json.loads(l)['ingested_at'] for l in open(manifest, encoding='utf-8'))[:10]
    (REPO / 'catalog.json').write_text(
        json.dumps({'snapshot_date': snapshot, 'books': public}, ensure_ascii=False, indent=1) + '\n',
        encoding='utf-8')
    sums.write_text(''.join(f"{b['sha256']}  {b['path']}\n" for b in books), encoding='utf-8')
    ignore = ['._*', '.DS_Store', '', '# Whole files rebuilt locally from parts (scripts/merge_parts.py)']
    ignore += ['/' + b['path'] for b in books if b.get('parts')]
    (REPO / '.gitignore').write_text('\n'.join(ignore) + '\n', encoding='utf-8')
    write_readme(books, snapshot)

    print(f"{len(books)} books; kebiao pages {sum(1 for b in books if b.get('kebiao_url'))}; "
          f"split {sum(1 for b in books if b.get('parts'))}")


if __name__ == '__main__':
    main()
