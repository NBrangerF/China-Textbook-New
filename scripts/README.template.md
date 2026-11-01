# China Textbook New · 中小学最新版电子教材

义务教育阶段（小学、初中）各学科的**最新修订版**电子教材 PDF，取自[国家中小学智慧教育平台](https://basic.smartedu.cn/tchMaterial)，每本都和平台记录核对过。

截至 {{DATE}}，共 **{{TOTAL}}** 本（{{SIZE_GB}} GB）：

- ✅ **{{NEW}}** 本是「根据 2022 年版课程标准修订」的新版。
- ⏳ **{{CURRENT}}** 本平台还没有发布修订版，主要是四至六年级、九年级的下册。这些书先放现行版，平台上线新版后替换。
- ⏳ **{{ATLAS}}** 本是初中地理配套图册。平台不提供图册，这几本沿用现有版本。

## 和 ChinaTextbook 有什么不同

[TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 帮了很多人，但义务教育部分已经很久没更新：小学语文、数学停在 2024 年 6 月，初中语文、数学停在 2023 年 3 月。2024 年秋季起陆续换用的新教材，那里大多还是旧印次。

| | ChinaTextbook | 本库 |
|---|---|---|
| 版本 | 旧印次，未标注是否为修订版 | 2022 课标修订版，每本标明 ✅ / ⏳ |
| 来源 | 未逐本注明 | {{PLATFORM}} 本取自国家平台，文件与平台记录的 MD5 逐字节一致，并附平台原页链接；其余 {{LEGACY}} 本（平台暂无新版，或平台不提供）沿用 ChinaTextbook 的现行版并注明 |
| 校验 | 无 | `SHA256SUMS.txt` 和 `catalog.json` 记录每本的 SHA-256、页数、大小 |
| 大文件 | 超过 50 MB 切成 35 MB 的碎片，要下载合并程序 | 只拆超过 95 MB 的 {{SPLIT_COUNT}} 本；表格里的链接直接下载整本 |
| 更新 | 靠人工 | `scripts/check_updates.py` 对照平台清单，列出平台已上线新版的书 |

## 怎么下载

- **单本**：点下面表格里的册名，进入文件页后点右上角的下载按钮。
- **超过 95 MB 的书**：表格链接直接下载整本 PDF（存放在 [Release](https://github.com/NBrangerF/China-Textbook-New/releases/tag/big-files)）。仓库里同时存有分卷（`.pdf.part1`、`.pdf.part2`……），克隆仓库后运行 `python3 scripts/merge_parts.py` 即可合并并校验。也可以手动合并：
  - macOS / Linux：`cat 书名.pdf.part* > 书名.pdf`
  - Windows：`copy /b 书名.pdf.part1+书名.pdf.part2+书名.pdf.part3 书名.pdf`
- **只要某几个学科**（不必下载整个仓库）：

  ```bash
  git clone --filter=blob:none --sparse https://github.com/NBrangerF/China-Textbook-New.git
  cd China-Textbook-New
  git sparse-checkout set 小学/数学 初中/数学
  ```

- **整个仓库**：`git clone https://github.com/NBrangerF/China-Textbook-New.git`，约 {{SIZE_GB}} GB。

## 目录

每个学科先收一套版本。✅ 为 2022 课标修订版，⏳ 为现行版；「平台」链接到国家中小学智慧教育平台上的原页。

{{TABLES}}

## 校验文件

`SHA256SUMS.txt` 列出每本整本 PDF 的 SHA-256（拆分的书要先合并）：

```bash
shasum -a 256 -c SHA256SUMS.txt                   # macOS
sha256sum -c --ignore-missing SHA256SUMS.txt      # Linux，只校验已下载的
```

`catalog.json` 是机器可读的完整目录：学段、学科、年级、册次、版本、修订状态、页数、字节数、SHA-256、平台 MD5、平台原页链接，拆分的书另有分卷列表和整本下载地址。

## 更新

国家平台上线新修订的教材后，本库会替换对应的书，旧版保留在 Git 历史里。维护者可以运行：

```bash
python3 scripts/check_updates.py
```

它读取平台公开的教材清单，列出两种情况：⏳ 的书平台已有同一出版社的修订版；平台在本库快照之后又更新过某本书的文件。

## 来源与版权

- 教材著作权归各出版社及编写者所有。本库只做整理，方便教师、学生和家长学习、备课；文件与国家中小学智慧教育平台免费提供的版本一致。请勿用于商业用途。
- 权利人如有异议，请通过 [Issue](https://github.com/NBrangerF/China-Textbook-New/issues) 联系，我们会尽快处理。

## 相关项目

[课标 kebiao.org](https://www.kebiao.org)：2022 年版义务教育课程标准的结构化索引。本库的教材也是 kebiao.org 的教材底本，在那里可以把教材和课标要求对照着看。
