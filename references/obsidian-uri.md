# Obsidian 命令行 / URI 控制参考（Advanced URI）

> 场景：scholar 在学习笔记、文献管理、写作跳转中需要「打开指定笔记 / 触发插件命令 / 写入属性」。
> 前提：Obsidian 已打开对应库（vault）；Advanced URI 插件已安装（`learning_space` 已装 v2.0.0）。
> vault 名 = 库文件夹名（如 `learning_space`）；库名统一从 `state.json` 的 `obsidian_vault` 取，未配置时询问用户一次。

## 1. 基础规则

- 入口统一：`obsidian://advanced-uri?<参数>`，参数用 `&` 连接，值需 URL 编码（中文/空格 → `%20`）；
- `vault` 参数必填，放第一位：`vault=learning_space`；
- 触发方式：浏览器地址栏 / PowerShell `Start-Process "obsidian://advanced-uri?vault=..."` / `start obsidian://...`；
- **失败不阻塞**：Obsidian 未开 / 库未加载 / 插件未启用 → URI 静默失败，一律退回直接写 md 文件并提示用户手动打开。

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

## 4. 触发命令（插件功能的关键）

`&commandid=<插件id>:<命令id>` 可执行**任何命令面板命令**——包括其他插件（Templater / Dataview / QuickAdd / obsidian-git…）。命令 id 可在「设置 → 命令面板 → 显示命令 id」里查，或试 `插件id:命令名小写-连字符`。

| 目的 | URI |
|------|------|
| 插入 Templater 模板 | `&filepath=<笔记>&commandid=templater-obsidian:insert-templater` |
| 打开 Dataview 面板 | `&commandid=dataview:dataview-pane-open` |
| 触发 git 推送 | `&commandid=obsidian-git:push` |
| 带参数执行（QuickAdd 等） | `&commandid=quickadd:run-quickadd&commandargs=<json>` |

> 触发命令前先带 `filepath=` 指定目标笔记（命令作用于当前笔记）；命令无反应时核对命令 id 与插件是否启用。

## 5. 与 scholar 的配合

- 学习笔记 / 文献管理等工具**默认直接用 md 文件写入（零依赖、可靠）**；URI 只用于增强：生成后打开笔记供用户查看、触发 Templater 补模板、刷新 Dataview/Bases 视图、推 obsidian-git 等；
- 可选 obsidian-cli（官方 CLI，需加入 PATH，`obsidian --version` 可用时）：`create` / `property:set` / `backlinks` / `search` 批量操作（见 `tools/学习笔记.md`）；
- 所有 URI/CLI 调用失败都不阻塞流程：退回写文件 + 提示用户手动打开。
