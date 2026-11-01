#!/usr/bin/env python3
"""Build this repository from a kebiao.org textbook library generation (maintainers only).

Usage:
  python3 scripts/build_from_kebiao.py <asset_manifest.jsonl> <library_root> <release_dir>

Copies each book into 学段/学科/版本/, splits files over SPLIT_AT bytes into parts
(the whole file goes to <release_dir> for the GitHub Release), and writes
catalog.json, SHA256SUMS.txt, .gitignore and the README tables.
"""
import hashlib
import json
import os
import shutil
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
GITHUB = 'https://github.com/NBrangerF/China-Textbook-New'
RELEASE_TAG = 'big-files'
SPLIT_AT = 95_000_000          # GitHub rejects files over 100 MiB
PART_SIZE = 90 * 1024 * 1024
CONTENT_DIRS = ['小学', '初中']

STAGES = {'primary': '小学', 'junior': '初中'}
GRADES = '一二三四五六七八九'
VOLUME_ORDER = {'上册': 0, '下册': 1, '全一册': 2}
VOLUME_SLUG = {'上册': '1', '下册': '2', '全一册': '0'}
STATUS = {
    'new': '2022 课标修订版',
    'current': '现行版（平台尚未发布修订版）',
    'atlas': '现行版（配套图册，平台不提供）',
}
MARK = {'new': '✅', 'current': '⏳', 'atlas': '⏳'}


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


def load_books(manifest):
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
            'source': source_of(row),
            '_status_key': status_of(row),
            '_object': row['object_path'],
            '_asset': f"{row['stage']}-{row['subject_slug']}-g{row['grade']}-{VOLUME_SLUG[row['volume']]}.pdf",
        })
    books.sort(key=lambda b: (b['stage'] != '小学', b['subject'], b['grade'], VOLUME_ORDER[b['volume']]))
    return books


def place(book, library_root, release_dir):
    """Write the book (or its parts) into the repo; return the repo files it owns."""
    src = Path(library_root) / book['_object']
    dest = REPO / book['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    if book['bytes'] <= SPLIT_AT:
        if not (dest.exists() and dest.stat().st_size == book['bytes'] and sha256_of(dest) == book['sha256']):
            shutil.copyfile(src, dest)
        if sha256_of(dest) != book['sha256']:
            sys.exit(f'checksum mismatch after copy: {dest}')
        return [dest]

    whole = Path(release_dir) / book['_asset']
    if not (whole.exists() and whole.stat().st_size == book['bytes']):
        shutil.copyfile(src, whole)
    if sha256_of(whole) != book['sha256']:
        sys.exit(f'checksum mismatch after copy: {whole}')
    parts = []
    with open(whole, 'rb') as f:
        for i, chunk in enumerate(iter(lambda: f.read(PART_SIZE), b''), start=1):
            part = dest.with_name(f'{dest.name}.part{i}')
            if not (part.exists() and part.stat().st_size == len(chunk)):
                part.write_bytes(chunk)
            parts.append(part)
    book['parts'] = [str(p.relative_to(REPO)) for p in parts]
    book['download_url'] = f"{GITHUB}/releases/download/{RELEASE_TAG}/{book['_asset']}"
    book['release_asset'] = book['_asset']
    return parts


def link(path):
    return quote(path)


def cell(book, main_edition):
    mb = book['bytes'] / 1e6
    href = book.get('download_url') or link(book['path'])
    text = f"{MARK[book['_status_key']]} [{book['volume']}]({href}) · {book['pages']} 页 · {mb:.0f} MB"
    if book['edition'] != main_edition:
        text += f"<br><sub>{book['edition']}</sub>"
    if book.get('platform_url'):
        text += f" · [平台]({book['platform_url']})"
    return text


def tables(books):
    out = []
    for stage in ['小学', '初中']:
        out.append(f'### {stage}\n')
        subjects = []
        for b in books:
            if b['stage'] == stage and b['subject'] not in subjects:
                subjects.append(b['subject'])
        for subject in subjects:
            group = [b for b in books if b['stage'] == stage and b['subject'] == subject]
            editions = [b['edition'] for b in group]
            main = max(set(editions), key=editions.count)
            volumes = sorted({b['volume'] for b in group}, key=VOLUME_ORDER.get)
            folder = f'{stage}/{subject}'
            out.append(f'#### {subject} · {main}　<sub>[打开文件夹]({link(folder)})</sub>\n')
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


def stats(books):
    count = {k: sum(1 for b in books if b['_status_key'] == k) for k in MARK}
    total_gb = sum(b['bytes'] for b in books) / 1e9
    return count, total_gb


def write_readme(books, snapshot_date):
    count, total_gb = stats(books)
    split = [b for b in books if b.get('parts')]
    template = (REPO / 'scripts' / 'README.template.md').read_text(encoding='utf-8')
    readme = (template
              .replace('{{DATE}}', snapshot_date)
              .replace('{{TOTAL}}', str(len(books)))
              .replace('{{NEW}}', str(count['new']))
              .replace('{{CURRENT}}', str(count['current']))
              .replace('{{ATLAS}}', str(count['atlas']))
              .replace('{{SIZE_GB}}', f'{total_gb:.1f}')
              .replace('{{SPLIT_COUNT}}', str(len(split)))
              .replace('{{PLATFORM}}', str(sum(1 for b in books if b.get('platform_md5'))))
              .replace('{{LEGACY}}', str(sum(1 for b in books if not b.get('platform_md5'))))
              .replace('{{TABLES}}', tables(books)))
    (REPO / 'README.md').write_text(readme, encoding='utf-8')


def main():
    manifest, library_root, release_dir = sys.argv[1:4]
    Path(release_dir).mkdir(parents=True, exist_ok=True)
    books = load_books(manifest)

    owned = set()
    for b in books:
        owned.update(place(b, library_root, release_dir))

    # Remove books that left the library (e.g. replaced by a new printing).
    # Compare NFC forms: the drive may hand names back decomposed.
    keep = {unicodedata.normalize('NFC', str(p)) for p in owned}
    for d in CONTENT_DIRS:
        for p in (REPO / d).rglob('*'):
            if p.is_file() and not p.name.startswith('._') and unicodedata.normalize('NFC', str(p)) not in keep:
                print('removing', p.relative_to(REPO))
                p.unlink()

    public = [{k: v for k, v in b.items() if not k.startswith('_')} for b in books]
    snapshot = max(json.loads(l)['ingested_at'] for l in open(manifest, encoding='utf-8'))[:10]
    (REPO / 'catalog.json').write_text(
        json.dumps({'snapshot_date': snapshot, 'books': public}, ensure_ascii=False, indent=1) + '\n',
        encoding='utf-8')
    (REPO / 'SHA256SUMS.txt').write_text(
        ''.join(f"{b['sha256']}  {b['path']}\n" for b in books), encoding='utf-8')
    ignore = ['._*', '.DS_Store', '', '# Whole files rebuilt locally from parts (scripts/merge_parts.py)']
    ignore += ['/' + b['path'] for b in books if b.get('parts')]
    (REPO / '.gitignore').write_text('\n'.join(ignore) + '\n', encoding='utf-8')
    write_readme(books, snapshot)

    count, total_gb = stats(books)
    print(f'{len(books)} books, {total_gb:.2f} GB; {count}; split {sum(1 for b in books if b.get("parts"))}')


if __name__ == '__main__':
    main()
