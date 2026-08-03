# Zotero 规则与证据记录定义

本文件定义 scholar 使用 Zotero 的规则，以及综述撰写时证据记录（Evidence Record）的标准。

## 1. Zotero 目录与 Markdown 缓存

- Zotero 数据目录：`<zotero-root>`（Windows 默认 `%USERPROFILE%\Zotero`，macOS 默认 `~/Zotero`；首次触发时探测或与用户确认）
- Zotero PDF 转 Markdown 缓存目录：`<zotero-root>\llm-for-zotero-mineru`
- 缓存按 Zotero 附件内部 ID 分文件夹：`<zotero-root>\llm-for-zotero-mineru\<attachmentId>\`
- 每个转换目录通常包含：
  - `full.md` — 论文正文 Markdown
  - `manifest.json` — 章节、图表、公式的解析清单
  - `content_list.json` — 内容索引
  - `_llm_source.json` — 记录 `attachmentId`、`attachmentKey`、`parentItemKey`、源 PDF 文件名
  - `images/` — 论文图片
- 当任务涉及 Zotero 论文查找、阅读、总结、综述或引用核对时，**优先读取缓存中的 `full.md`**；只有缓存不存在或内容不足时，再回退到 PDF、Zotero fulltext 或附件文件。
- 定位规则：用 `_llm_source.json` 中的 `attachmentId`/`attachmentKey`/`parentItemKey`/`sourceFilename` 把 Zotero 条目映射到 Markdown 文件。

## 2. PDF → Markdown 转换

- 转换通过 Zotero 插件 `llm-for-zotero-mineru` 完成，产物写入上述缓存目录。
- scholar 的步骤二（2b）在收到用户提供的转换脚本后，将下载的 PDF 交给转换脚本处理；转换结果（`full.md` 等同内容）复制到对应论文文件夹，命名为 `<论文>.md`。
- 转换脚本未提供前，步骤二 2b 跳过并在结果中标记「待转换」。

## 3. 证据记录（Evidence Record）

综述中每个被采纳的观点/结论都应能回溯到证据记录。证据记录模板：

```md
## Evidence Record

Evidence ID: <唯一编号，如 001>
Source: <论文文件夹名 / Zotero 条目>
Source type: full paper | preprint | dataset | experiment artifact | project note | abstract-only | webpage placeholder
Supports: <支持的观点/结论>
Contradicts: <矛盾的观点/结论（如有）>
Method / dataset / metric: <论文使用的方法/数据/指标>
Limitation: <论文局限性>
Project relevance: <与本次综述主题的相关性>
Claim strength: speculative | observed | supported | strong
```

## 4. 观点提升门槛（Claim Promotion Gate）

综述草稿落定前，逐条检查：

- 每一条被采纳的观点必须指向一个 Evidence Record ID；
- 证据来源类型必须足以支撑该观点（`abstract-only` 和 `webpage placeholder` 不能支撑持久性结论）；
- 表述强度必须与证据强度匹配：证据是 `observed`，就不能写成 `strong`；
- 需要进入论文、稿件或答复的措辞，按“允许的措辞”与“更强的措辞”分开管理；
- 无法回溯到来源笔记/文献内容的综合内容，不允许写入综述。
