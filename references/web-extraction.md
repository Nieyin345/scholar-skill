# 网页内容提取（Defuddle）

来源：defuddle skill（Anthropic，CLI 工具）。

用于从网页（论文主页、新闻、博客等）提取干净正文，减少噪音和 token 消耗。优先于直接读取整页 HTML。

## 安装

```bash
npm install -g defuddle
```

## 用法

```bash
# 提取正文为 Markdown
defuddle parse <url> --md

# 保存到文件
defuddle parse <url> --md -o content.md

# 提取元数据
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## 在 scholar 中的用途

- 步骤一：从检索结果/论文主页提取摘要与关键信息，用于构建 `01_检索结果.md`；
- 步骤二：提取期刊主页的下载链接或元数据（配合 DOI 解析失败时的补充手段）。
