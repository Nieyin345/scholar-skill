# Obsidian 命令行 / URI 控制参考（Advanced URI）

> 场景：scholar 在学习笔记、文献管理、写作跳转中需要「打开指定笔记 / 触发插件命令 / 写入属性」。
> 前提：Obsidian 已打开对应库（vault）；Advanced URI 插件已安装（是否已装**用时探测**：读 `<vault>/.obsidian/community-plugins.json`，含 `obsidian-advanced-uri` 即已启用；不预先维护清单）。
> vault 名 = 库文件夹名；库名统一从 `state.json` 的 `obsidian_vault` 取，未配置时询问用户一次。

## 1. 基础规则

- 入口统一：`obsidian://advanced-uri?<参数>`，参数用 `&` 连接，值需 URL 编码（中文/空格 → `%20`）；
- `vault` 参数必填，放第一位：`vault=learning_space`；
- 触发方式：浏览器地址栏 / PowerShell `Start-Process "obsidian://advanced-uri?vault=..."` / `start obsidian://...`；
- **失败不阻塞**：Obsidian 未开 / 库未加载 / 插件未启用 → URI 静默失败，一律退回直接写 md 文件并提示用户手动打开。
- **不维护清单**：本文件是**用法参考**，不是插件清单；插件与命令 id 一律用时探测，装/卸插件无需改本文件。
- **未装 Advanced URI 时提醒安装（必做）**：需要 URI 功能而 `<vault>/.obsidian/community-plugins.json` 里没有 `obsidian-advanced-uri` → **先提醒用户安装**：Obsidian → 设置 → 第三方插件（Community plugins）→ 浏览 → 搜索「Advanced URI」→ 安装并启用；手动安装：到 https://github.com/Vinzent03/obsidian-advanced-uri/releases 下载对应版本，解压到 `<vault>/.obsidian/plugins/obsidian-advanced-uri/`，然后在「第三方插件」里启用。装完重试 URI；用户暂时不装 → 退回直接写 md 文件（不阻塞）。

## 2. 打开与定位（核心）

| 目的 | URI（`obsidian://advanced-uri?vault=<库>` 后拼接） |
|------|------|
| 打开笔记 | `&filepath=<路径>` |
| 定位到行 | `&filepath=<路径>&line=<行号>` |
| 定位到标题 | `&filepath=<路径>&heading=<标题>` |
| 定位到块 | `&filepath=<路径>&block=<块id>` |
| 打开时搜索 | `&filepath=<路径>&search=<关键词>` |
| 阅读/源码模式 | `&mode=preview|source|live` |
| 新标签打开 | `&openmode=true` |

## 3. 新建 / 写入

| 目的 | URI |
|------|------|
| 新建笔记并写内容 | `&new=<路径>&data=<内容>`（`\n` 表示换行） |
| 用剪贴板内容新建 | `&new=<路径>&clipBoard=true` |
| 设置属性 | `&filepath=<笔记>&property=<键>&value=<值>`（按需加 `propertytype=number|boolean|date|checkbox`） |

## 4. 触发命令（插件功能的关键，命令 id 用时直接探测）

`&commandid=<插件id>:<命令id>` 可执行**任何命令面板命令**——包括其他插件（Templater / Dataview / QuickAdd / obsidian-git…）。

**不维护静态命令清单**：需要触发某个插件的命令时，现场直接探测（30 秒内）：

1. 读 `<vault>/.obsidian/community-plugins.json` → 已启用插件列表（再看 `plugins/` 目录确认已装）；
2. 在目标插件 `main.js` 里搜索 `id:"<本地命令id>"`（命令注册处），插件 id 见该插件 `manifest.json` 的 `id` 字段；
3. 完整命令 id = `<插件id>:<本地命令id>`（如 Templater 的 `id:"insert-templater"` + 插件 id `templater-obsidian` → `templater-obsidian:insert-templater`）；
4. 拼 URI 执行；不确定就先在目标笔记上试一次（命令无反应= id 不对或插件未启用）。

已核验示例（本机 Templater 2.16.4 / obsidian-git 2.38.6 / QuickAdd 2.9.4 实测提取）：

| 目的 | 命令 id（完整） |
|------|------|
| 插入 Templater 模板 | `templater-obsidian:insert-templater` |
| 新建笔记套模板 | `templater-obsidian:create-new-note-from-template` |
| git 推送 | `obsidian-git:push` |
| git 拉取 | `obsidian-git:pull` |
| git 提交（默认消息） | `obsidian-git:commit` |
| QuickAdd 执行 | `quickadd:runQuickAdd` |

> 触发命令前先带 `filepath=` 指定目标笔记（命令作用于当前笔记）；以现场探测到的 id 为准，上面的示例只作参考。

## 5. 与 scholar 的配合

- 学习笔记 / 文献管理等工具**默认直接用 md 文件写入（零依赖、可靠）**；URI 只用于增强：生成后打开笔记供用户查看、触发 Templater 补模板、刷新 Dataview/Bases 视图、推 obsidian-git 等；
- 可选 obsidian-cli（官方 CLI，需加入 PATH，`obsidian --version` 可用时）：`create` / `property:set` / `backlinks` / `search` 批量操作（见 `tools/学习笔记.md`）；
- 所有 URI/CLI 调用失败都不阻塞流程：退回写文件 + 提示用户手动打开。
