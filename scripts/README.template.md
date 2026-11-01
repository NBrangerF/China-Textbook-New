<div align="center">

# China Textbook New

**一至九年级最新版教材 PDF · 2022 课标修订版**

[![教材]({{BADGE_TOTAL}})](#快速找书)
[![2022 课标修订版]({{BADGE_NEW}})](#快速找书)
[![更新]({{BADGE_DATE}})](#更新)
[![配套网站 kebiao.org]({{BADGE_KEBIAO}})](https://www.kebiao.org)

[快速找书](#快速找书) · [配合 kebiao.org 备课](#配合-kebiaoorg-备课) · [怎么下载](#怎么下载) · [和 ChinaTextbook 有什么不同](#和-chinatextbook-有什么不同) · [English](#english)

</div>

从 2024 年秋天开始，义务教育各科陆续换上了根据 2022 年版课程标准修订的新教材。可网上好找的 PDF 大多还是旧印次，想要新版，只能去[国家中小学智慧教育平台](https://basic.smartedu.cn/tchMaterial)一本本找。

我在做 [kebiao.org](https://www.kebiao.org)，一个帮老师查课标、对教材的网站，本来就得把这套新教材整理一遍。整理好了，干脆放在这里，谁要都能直接拿。

现在有 **{{TOTAL}}** 本，一共 {{SIZE_GB}} GB，{{DATE}} 更新：

- ✅ **{{NEW}}** 本是 2022 课标修订版，直接取自国家平台，和平台上的文件一模一样。
- ⏳ **{{CURRENT}}** 本平台还没出修订版，大多是四到六年级和九年级的下册。先放现行版，新版一出来就换。
- ⏳ 还有 **{{ATLAS}}** 本初中地理图册，平台上没有，用的是现有版本。

## 快速找书

点册名就能下载。带 ⏳ 的是现行版，其余都是修订版。点学科名，能看到这一科每本书的页数、大小，还有去 kebiao.org 和国家平台的链接。

{{OVERVIEW}}

## 配合 kebiao.org 备课

[kebiao.org](https://www.kebiao.org) 用的就是这套教材。打开一本书，你会看到：

- **每一课在教哪几条课标**：AI 逐课读了课文，对着这个年级的课标要点，标出这一课「主要在教」和「也涉及」的，每条都附上课文原话和页码，整本还能导出成 Word。这一步是机器做的，人工核对还在进行，发现不对的地方欢迎告诉我。
- **从某一课开始备课**：AI 照着课标，帮你起一份教案草稿。
- **在线看原书**：懒得下载，就直接在网页上翻。

[![kebiao.org 上的一本书：左边是每一课，右边是它教的课标要点](docs/kebiao-book-page.png)](https://www.kebiao.org/textbooks/ed_006d5ed61c055eb63857)

<sub>上图是 kebiao.org 上的人教版数学七年级上册。金线连着这一课主要在教的课标要点，虚线是也涉及的。</sub>

这里有 {{KEBIAO_COUNT}} 本书在 kebiao.org 上有自己的页面，在[详细目录](#详细目录)里点「课标对应」就能过去。

## 怎么下载

- **下一本**：在上面点册名，进去以后点右上角的下载按钮。
- **超过 95 MB 的 {{SPLIT_COUNT}} 本**：GitHub 不收超过 100 MB 的文件，所以这几本在仓库里拆成了几段（`.pdf.part1`、`.pdf.part2`……）。不过上面的链接下载的是放在 [Release](https://github.com/NBrangerF/China-Textbook-New/releases/tag/big-files) 里的整本，不用自己拼。如果克隆了整个仓库，运行 `python3 scripts/merge_parts.py` 就能拼好，顺便校验。想手动拼也行：
  - macOS / Linux：`cat 书名.pdf.part* > 书名.pdf`
  - Windows：`copy /b 书名.pdf.part1+书名.pdf.part2+书名.pdf.part3 书名.pdf`
- **只要某几科**，不用把整个仓库拉下来：

  ```bash
  git clone --filter=blob:none --sparse https://github.com/NBrangerF/China-Textbook-New.git
  cd China-Textbook-New
  git sparse-checkout set 小学/数学 初中/数学
  ```

- **全都要**：`git clone https://github.com/NBrangerF/China-Textbook-New.git`。大约 {{SIZE_GB}} GB，网慢的话，建议只拿要用的学科。

## 和 ChinaTextbook 有什么不同

[TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 帮过很多人，kebiao 早先的教材也有不少来自那里。只是义务教育这部分很久没更新了：小学语文、数学停在 2024 年 6 月，初中语文、数学停在 2023 年 3 月，大多还是旧印次。

这个仓库只管义务教育这一段，把它换成最新版，另外多做了几件事：

- 每本都标明是修订版（✅）还是现行版（⏳）。
- {{PLATFORM}} 本直接取自国家平台，和平台记录的 MD5 一致，附平台原页链接。另外 {{LEGACY}} 本平台还没有新版，或者平台不提供，沿用 ChinaTextbook 的现行版，也都标了出来。
- 每本的 SHA-256、页数、大小都记在 `SHA256SUMS.txt` 和 `catalog.json` 里。
- 只有超过 95 MB 的 {{SPLIT_COUNT}} 本才拆分，点链接下的还是整本，不用另装合并程序。
- 平台一出新版，`scripts/check_updates.py` 就能查出该换哪几本。
- 每本书都链到 kebiao.org，能看到每一课对应的课标。

## 详细目录

每科先收了一个版本。想要别的版本，[提个 Issue](https://github.com/NBrangerF/China-Textbook-New/issues) 告诉我。✅ 是修订版，⏳ 是现行版。「课标对应」打开这本书在 kebiao.org 上的页面，「平台原页」打开它在国家中小学智慧教育平台上的原页。

{{DETAILS}}

## 校验文件

下载完想确认文件完整、没被改过，可以用 `SHA256SUMS.txt` 核对（拆分的书要先拼好）：

```bash
shasum -a 256 -c SHA256SUMS.txt                   # macOS
sha256sum -c --ignore-missing SHA256SUMS.txt      # Linux，只核对已经下载的
```

`catalog.json` 是给程序读的完整目录：学段、学科、年级、册次、版本、是不是修订版、页数、字节数、SHA-256、平台 MD5、平台原页和 kebiao.org 链接都在里面。拆分的书还列了每一段，以及整本的下载地址。

## 更新

国家平台出了新修订的教材，我会把对应的书换掉，旧版留在 Git 历史里。想自己查，可以运行：

```bash
python3 scripts/check_updates.py
```

它会对照平台公开的教材清单，告诉你两件事：带 ⏳ 的书，平台上是不是已经有同一出版社的修订版；平台在这次整理之后，有没有又更新过哪本书。

## 一起完善

- 发现错版、缺页、链接打不开，或者想要北师大、苏教、沪教、青岛这些版本，[提个 Issue](https://github.com/NBrangerF/China-Textbook-New/issues) 告诉我。
- 觉得有用，点个 ⭐ Star，能让更多老师和家长找到这里。

## 来源与版权

- 教材的著作权属于各出版社和编写者。我做的只是把国家中小学智慧教育平台免费提供的文件整理到一起，方便老师、学生和家长学习、备课。请不要拿去商用。
- 如果你是权利人，觉得哪本书不该放在这里，[开个 Issue](https://github.com/NBrangerF/China-Textbook-New/issues) 告诉我，我会尽快处理。

## English

Since autumn 2024, China's compulsory-education textbooks (grades 1–9) have been switching to new editions revised for the 2022 curriculum standards, but most PDFs you can find online are still old printings. I build [kebiao.org](https://www.kebiao.org), a site that helps teachers look up curriculum standards, and had to collect the new editions anyway, so here they are: {{TOTAL}} PDFs, {{NEW}} of them already revised. {{PLATFORM}} of them come straight from the official [National Smart Education Platform](https://basic.smartedu.cn/tchMaterial), the rest say where they came from, and each book says whether it's revised (✅) or still the current printing (⏳). On kebiao.org, every lesson in these books is mapped to the curriculum points it teaches.
