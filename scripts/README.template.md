<div align="center">

# China Textbook New

**中小学最新版电子教材 · 2022 年版课程标准修订版**

[![教材]({{BADGE_TOTAL}})](#快速找书)
[![2022 课标修订版]({{BADGE_NEW}})](#快速找书)
[![更新]({{BADGE_DATE}})](#更新)
[![配套网站 kebiao.org]({{BADGE_KEBIAO}})](https://www.kebiao.org)

[快速找书](#快速找书) · [配合 kebiao.org 备课](#配合-kebiaoorg-备课) · [怎么下载](#怎么下载) · [和 ChinaTextbook 的区别](#和-chinatextbook-的区别) · [English](#english)

</div>

小学一年级到初中九年级，各学科**最新修订版**教材的 PDF。全部来自[国家中小学智慧教育平台](https://basic.smartedu.cn/tchMaterial)，每本都和平台记录核对过，并标明是不是 2022 年版课程标准修订后的新版。

截至 {{DATE}}，共 **{{TOTAL}}** 本、{{SIZE_GB}} GB：

- ✅ **{{NEW}}** 本是「根据 2022 年版课程标准修订」的新版。
- ⏳ **{{CURRENT}}** 本平台还没有发布修订版，主要是四至六年级、九年级的下册。先放现行版，平台一上线新版就替换。
- ⏳ **{{ATLAS}}** 本是初中地理配套图册。平台不提供图册，沿用现有版本。

## 快速找书

点册名下载 PDF。带 ⏳ 的是现行版（平台还没发布修订版），其余都是 2022 课标修订版。点学科名可以看这一科每本书的页数、大小，以及到 kebiao.org 和国家平台的链接。

{{OVERVIEW}}

## 配合 kebiao.org 备课

教材下载好了，下一步是备课。[**kebiao.org**](https://www.kebiao.org) 用的就是这套教材，打开一本书就能看到：

- **每一课教哪几条课标**：AI 逐课读了教材原文，对照本年级课标的全部要点，标出这一课「主要在教」和「也涉及」的要点，每条都附教材原话和页码。整本的对应表可以下载成 Word。目前是机器判断，还在人工核验中。
- **用这本书备课**：从书里的某一课开始，AI 按课标帮你起草教案。
- **在线看原书**：不用下载，打开就能读。

[![kebiao.org 上的一本书：左边是每一课，右边是它教的课标要点](docs/kebiao-book-page.png)](https://www.kebiao.org/textbooks/ed_006d5ed61c055eb63857)

<sub>上图：kebiao.org 上的人教版数学七年级上册。金线连着这一课「主要在教」的课标要点，虚线是「也涉及」的。</sub>

本库 {{KEBIAO_COUNT}} 本书在 kebiao.org 上都有自己的页面，[详细目录](#详细目录)里每本书旁边的「课标对应」链接可以直达。

## 怎么下载

- **单本**：在[快速找书](#快速找书)里点册名，进入文件页后点右上角的下载按钮。
- **超过 95 MB 的 {{SPLIT_COUNT}} 本**：链接直接下载整本 PDF（存放在 [Release](https://github.com/NBrangerF/China-Textbook-New/releases/tag/big-files)）。仓库里同时存有分卷（`.pdf.part1`、`.pdf.part2`……），克隆仓库后运行 `python3 scripts/merge_parts.py` 就能合并并校验。也可以手动合并：
  - macOS / Linux：`cat 书名.pdf.part* > 书名.pdf`
  - Windows：`copy /b 书名.pdf.part1+书名.pdf.part2+书名.pdf.part3 书名.pdf`
- **只要某几个学科**，不必下载整个仓库：

  ```bash
  git clone --filter=blob:none --sparse https://github.com/NBrangerF/China-Textbook-New.git
  cd China-Textbook-New
  git sparse-checkout set 小学/数学 初中/数学
  ```

- **整个仓库**：`git clone https://github.com/NBrangerF/China-Textbook-New.git`，约 {{SIZE_GB}} GB。

## 和 ChinaTextbook 的区别

[TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 帮了很多人，但义务教育部分很久没有更新：小学语文、数学停在 2024 年 6 月，初中语文、数学停在 2023 年 3 月。2024 年秋季起各年级陆续换用新教材，那里大多还是旧印次。

| | ChinaTextbook | 本库 |
|---|---|---|
| 版本 | 旧印次，未标注是否为修订版 | 2022 课标修订版，每本标明 ✅ / ⏳ |
| 来源 | 未逐本注明 | {{PLATFORM}} 本取自国家平台，与平台记录的 MD5 逐字节一致，并附平台原页链接；其余 {{LEGACY}} 本（平台暂无新版，或平台不提供）沿用 ChinaTextbook 的现行版并注明 |
| 校验 | 无 | `SHA256SUMS.txt` 和 `catalog.json` 记录每本的 SHA-256、页数、大小 |
| 大文件 | 超过 50 MB 切成 35 MB 的碎片，要另外下载合并程序 | 只拆超过 95 MB 的 {{SPLIT_COUNT}} 本，链接直接下载整本 |
| 更新 | 靠人工 | `scripts/check_updates.py` 对照平台清单，列出平台已上线新版的书 |
| 备课 | — | 每本书链到 kebiao.org，看每一课对应的课标要点 |

## 详细目录

每个学科先收一套版本。✅ 为 2022 课标修订版，⏳ 为现行版。「课标对应」打开这本书在 kebiao.org 上的页面，「平台原页」打开国家中小学智慧教育平台上的原页。

{{DETAILS}}

## 校验文件

`SHA256SUMS.txt` 列出每本整本 PDF 的 SHA-256（拆分的书要先合并）：

```bash
shasum -a 256 -c SHA256SUMS.txt                   # macOS
sha256sum -c --ignore-missing SHA256SUMS.txt      # Linux，只校验已下载的
```

`catalog.json` 是机器可读的完整目录：学段、学科、年级、册次、版本、修订状态、页数、字节数、SHA-256、平台 MD5、平台原页和 kebiao.org 链接；拆分的书另有分卷列表和整本下载地址。

## 更新

国家平台上线新修订的教材后，本库会替换对应的书，旧版留在 Git 历史里。维护者可以运行：

```bash
python3 scripts/check_updates.py
```

它读取平台公开的教材清单，列出两种情况：⏳ 的书平台已有同一出版社的修订版；平台在本库快照之后又更新过某本书的文件。

## 一起完善

- 发现错版、缺页、链接打不开，或者想要其他版本（北师大、苏教、沪教、青岛……）：请[提 Issue](https://github.com/NBrangerF/China-Textbook-New/issues)。
- 觉得有用，点右上角的 ⭐ Star，让更多老师和家长看到。

## 来源与版权

- 教材著作权归各出版社及编写者所有。本库只做整理，方便教师、学生和家长学习、备课；文件与国家中小学智慧教育平台免费提供的版本一致。请勿用于商业用途。
- 权利人如有异议，请通过 [Issue](https://github.com/NBrangerF/China-Textbook-New/issues) 联系，我们会尽快处理。

## English

**China Textbook New** collects the newest editions of China's compulsory-education textbooks (grades 1–9, primary and junior secondary): {{TOTAL}} PDFs, {{NEW}} of them revised for the 2022 national curriculum standards. Every file comes from the official [National Smart Education Platform](https://basic.smartedu.cn/tchMaterial) and is checked against the platform's record; each book is marked as revised (✅) or still the current printing (⏳). The companion site [kebiao.org](https://www.kebiao.org) maps every lesson in these books to the points of the 2022 curriculum standards it teaches, and helps teachers draft lesson plans from them.
