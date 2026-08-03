# Scholar · 学术研究全流程 Agent Skill

> 一个把「文献 → 综述 → 方案 → 代码 → 论文」串成完整闭环的学术研究 Skill。触发后按流程执行，流程可拆可合；另有科研插图、学习笔记、书籍库管理、知识库检索四个独立工具按需触发。
>
> 适用于 Codex / Claude Code / Cursor 等所有支持 Markdown Skill 的 Coding Agent（要求 agent 能读取目录内 `SKILL.md` 并按说明执行）。

## 功能总览

| 模块 | 说明 |
|------|------|
| 流程0 研究方向确认 | 模糊大方向 → 多轮交互 + 文献验证 → 收敛为可执行方向（产出 `00_研究方向.md`） |
| 流程一 文献检索与综述 | 检索（高质量/高引用/顶会顶刊优先）→ 下载 PDF → MinerU 转 MD → 基于检索内容写文献综述（三步可拆可合） |
| 流程二 解决方案设计 | 基于文献产出三份文档：01 场景分析与问题剖析 / 02 实现逻辑与方案设计（算法+数学，多方案逐篇生成）/ 03 代码架构设计（含学术场景适配） |
| 流程三 代码实现 | 按 03 架构用 TDD 落地实现：系统化调试、验证门禁、回归验证、对齐实验阶段 |
| 流程四 论文写作 | 写（中文）→ 润色 → 翻译 → 再润色 → LaTeX 编译 → 多角色 review 循环（写/润色/翻译/review 分角色）；review 发现问题非写作类则中断返回前流程；历史版本与 review 反馈存档 |
| 工具·科研插图 | 神经网络结构图 / 训练架构图 / 流程图 / 图形摘要（可编辑矢量，draw.io 或 PowerPoint/WPS） |
| 工具·学习笔记 | 论文 → Obsidian 学习笔记（wiki 链接互链，搭建个人知识体系） |
| 工具·书籍库管理 | PDF 教材库骨架 + 增量维护：游离 PDF 归类、转 MD、登记索引 |
| 工具·知识库检索 | **无向量库 RAG**：回答问题时检索本地论文/笔记/书籍/Zotero 缓存并溯源（不做 embedding，`rg` 关键词召回 + 整页读取） |

## 自包含（独立 Skill）

scholar 是**自包含**的：全部流程、规范、脚本、参考文档与第三方工具都内嵌在仓库内（`workflows/`、`standards/`、`references/`、`scripts/`、`tools/`、`plugins/`），不依赖任何其他 Skill 或插件。运行环境只要求系统级工具（Python 3.9+、rg、可选 LaTeX / MinerU CLI / defuddle / draw.io desktop / PowerPoint）。它同时也是**多个 Skill 融合的产物**——融合来源与链接见下文「融合产物」章节。

## 融合产物（多 Skill 融合）

scholar 不是从零编写的单一 Skill，而是**多个公开 Skill / 插件 / 开源项目融合的产物**：把经过筛选的检索、下载、转换、写作、架构、画图等方法论、脚本与定义吸收进一个自包含 Skill。所有被吸收的内容都已**完整内嵌到本仓库**（`scripts/`、`references/`、`standards/`、`tools/`、`plugins/`），运行时不依赖任何外部 Skill 或插件。

### 完整内嵌（脚本 / 插件 / 参考全集）

| 融合来源 | 链接 | 吸收位置 | 吸收内容 |
|----------|------|----------|----------|
| paper-fetch | https://github.com/obra/paper-fetch | `scripts/fetch.py` + `cloak_pdf.py` | 文献 PDF 下载（多源解析 + %PDF 校验） |
| AnySearch | https://github.com/anysearch-ai/anysearch-skill | `scripts/anysearch/` | 实时搜索 CLI（Apache-2.0） |
| scientific-illustrator | https://github.com/icebird1998/scientific-illustrator | `plugins/scientific-illustrator/` | 科研插图 MCP 后端（3 个 server + 6 个子 skill，MIT） |
| MinerU | https://github.com/opendatalab/MinerU | `scripts/mineru/` + `convert_pdf_to_md.py` | PDF→MD 精提取 CLI |
| research-ideation | 本地 skill 生态吸收（无公开链接） | `references/research-ideation/` | 研究方向引导全套：5W1H / gap 分析 / 研究问题 / 方法选择 / 检索策略 / 研究计划 |
| citation-verification / nature-writing / paper-self-review | 本地 skill 生态吸收（无公开链接） | `references/` 对应目录 | 引用核验、Nature 风格写作、论文自查与判定 |

### 方法论与规范吸收（进入 standards / workflows，标注来源改写）

| 融合来源 | 链接 | 吸收内容 |
|----------|------|----------|
| superpowers | https://github.com/obra/superpowers | TDD、系统化调试、验证门禁、代码评审纪律 |
| gstack | https://github.com/garrytan/gstack | 计划评审 / 设计评审 / 文档生成工作流 |
| wondelai/skills | https://github.com/wondelai/skills | design-code-architecture、clean-architecture 依赖规则 |
| co-researcher | https://github.com/poemswe/co-researcher | 系统综述（PRISMA）、研究方法论、批判审查 |
| agent-research-skills | https://github.com/lingzhi227/agent-research-skills | 选题 / 新颖性 / 深研 / 算法设计 / LaTeX 投稿格式 |
| ai-agents-public | https://github.com/vasilyu1983/ai-agents-public | 架构选型决策树、ADR 记录模板 |
| claude-software-skills | https://github.com/miles990/claude-software-skills | 架构模式对比与反模式、测试策略 |
| software_development_skills | https://github.com/yinhunfeixue/software_development_skills | 中文软件生命周期（需求→设计→编码→测试→评审） |
| qodex-ai-agent-skills | https://github.com/qodex-ai/ai-agent-skills | 代码风格硬规则、Clean Architecture 落地 |
| context-engineering-kit | https://github.com/neolabhq/context-engineering-kit | DDD 与 Clean Architecture 规则化 |
| melodic-claude-code-plugins | https://github.com/melodic-software/claude-code-plugins | 架构文档改进流程与模板 |
| everything-claude-code | https://github.com/affaan-m/everything-claude-code | coding-standards 编码规范基线 |
| awesome-copilot | https://github.com/github/awesome-copilot | 编码规范文档结构模板 |
| ai-development-team | https://github.com/olehsvyrydov/ai-development-team | 多角色职责边界、负面判据 |
| alirezarezvani-claude-skills | https://github.com/alirezarezvani/claude-skills | boardroom 多角色隔离评审架构 |
| latex-document-skill | https://github.com/ndpvt-web/latex-document-skill | LaTeX 引擎检测 / 多遍编译（改写为 `scripts/latex/`） |
| langchain-skills | https://github.com/langchain-ai/langchain-skills | 检索→生成两阶段思想（scholar 落地为无向量版） |
| wshobson/agents | https://github.com/wshobson/agents | RAG 生成纪律「有据才答」（反模式对照） |

### 本地生态吸收（已内嵌，无公开链接）

- obsidian-literature-workflow / obsidian-source-ingestion / obsidian-project-kb-core / obsidian-markdown / zotero-obsidian-bridge：Obsidian 知识库结构、wiki 链接互链、Zotero 证据纪律（学习笔记 / 知识库检索工具）。
- ml-paper-writing：主张-证据纪律（Claim Ledger Gate、Claim Audit）（论文写作规范）。

> 「本地 skill 生态吸收」指最初来自本机已安装的 skill，方法论已改写进 scholar 并标注来源；完整吸收映射见 `00_markdown/项目介绍.md`、`ref-external/README.md`（参考源）与各 `standards/` / `references/` 文件内「参考来源」。
## 目录结构

```text
scholar/                     # 仓库根即 Skill 本体（SKILL.md 位于根目录）
├── SKILL.md                 # 路由与总览：流程清单、触发规则、共享资产索引
├── workflows/               # 流程0 + 流程一~四的详细步骤（按需读取）
├── standards/               # 写作规范库（每类写作任务一份，随反馈持续更新）
├── tools/                   # 独立工具（科研插图 / 学习笔记 / 书籍库管理 / 知识库检索）
├── scripts/                 # 共享脚本：下载(fetch) / 转换(MinerU) / 搜索 / 密钥管理 / LaTeX / 书籍库
├── references/              # 共享参考：检索协议、写作模板、Zotero 规则、LaTeX 模板等
├── plugins/                 # 内嵌第三方：scientific-illustrator（科研插图 MCP 后端，MIT）
├── .env.example             # 密钥模板（复制为 .env 后填入）
└── .gitignore
```

## 安装（适用于所有 Agent）

Skill 本体就是本仓库根目录内容。安装 = 把仓库内容放到对应 Agent 的 skills 目录下，目录名 `scholar`。

### 方式一：一键安装脚本（推荐）

```bash
# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/Nieyin345/scholar-skill/main/install.sh | bash -s -- --agent auto
```

```powershell
# Windows（PowerShell 5.1+ / 7+）
irm https://raw.githubusercontent.com/Nieyin345/scholar-skill/main/install.ps1 | iex -Args "--agent", "auto"
```

参数说明（两脚本一致）：

| 参数 | 取值 | 说明 |
|------|------|------|
| `--agent` | `auto`（默认）/ `codex` / `claude` / `cursor` / `custom` | 安装到哪个 Agent；`auto` 自动检测已安装的 Agent 并全部安装 |
| `--target <dir>` | 任意目录 | 与 `--agent custom` 搭配：安装到自定义目录 |
| `--repo <url>` | Git 仓库地址 | 自定义下载源（默认本仓库） |

安装位置：

| Agent | 目录 |
|-------|------|
| Codex | `~/.codex/skills/scholar/` |
| Claude Code | `~/.claude/skills/scholar/` |
| Cursor | `~/.cursor/skills/scholar/`（全局）或项目内 `.cursor/skills/scholar/` |
| 其他 / 自定义 | `--agent custom --target <任意目录>` |

### 方式二：手动安装（git clone）

```bash
# Codex
git clone --depth 1 https://github.com/Nieyin345/scholar-skill.git ~/.codex/skills/scholar

# Claude Code
git clone --depth 1 https://github.com/Nieyin345/scholar-skill.git ~/.claude/skills/scholar

# Cursor（项目级）
git clone --depth 1 https://github.com/Nieyin345/scholar-skill.git .cursor/skills/scholar
```

> 任何只认「目录 + SKILL.md」的 Agent 都可用同一方式：把本仓库 clone/复制到一个 Agent 能读到的 skills 目录即可。更新 = 在对应目录 `git pull`（或重新 clone）。

## 首次使用配置
首次触发由 skill 内建的**状态文件**自动判定：`<skill_dir>/state.json` 不存在或 `setup_complete != true` 即为首次触发，会引导完成一次性配置（密钥 + 本地路径）后写入状态；之后每次触发直接复用，不再询问。可用 `python scripts/setup_state.py status` 查看，`reset` 可重走首次配置。

1. **密钥**（可选项，缺失时触发相关功能会询问一次并保存到 `<skill_dir>/.env`）：
   - `ANYSEARCH_API_KEY` — 实时网络搜索（可选，匿名可用）
   - `MINERU_TOKEN` — PDF→MD 精提取（MinerU `extract` 模式需要；`flash` 模式免认证）
   - `UNPAYWALL_EMAIL` — 文献下载 Unpaywall 源（可选）
2. **本地路径**（首次触发对应功能时确认，确认后记住复用）：
   - Obsidian vault（学习笔记）
   - 书籍库根目录（默认 `~/OB_database/Books`）
   - Zotero 数据目录（知识库检索的 Zotero 缓存，Windows 默认 `%USERPROFILE%\Zotero`，macOS `~/Zotero`）
3. **依赖**：
   - Python 3.9+（脚本）
   - `rg` / ripgrep（知识库检索）
   - LaTeX 引擎（流程四编译；`scripts/latex/detect_engine.py` 会自动检测）
   - MinerU Open API CLI（PDF→MD；`scripts/mineru/install.ps1` 或官方安装命令）
   - draw.io desktop（科研插图工具后端，可选；自动探测或设 `DRAWIO_PATH`）
   - PowerPoint / WPS（科研插图工具可选后端；MCP server 已内嵌于 `plugins/scientific-illustrator/`，注册方式见 `tools/科研插图.md`）

## 工作目录约定

每个研究方向（主题）在工作区内建立独立文件夹，skill 会维护一份 `00_项目导航.md` 作为目录索引 + 文档管理入口（只在文件变动时更新）：

```text
<主题>/
├── 00_项目导航.md           # 目录总表 + 文献/文档位置（导航文档）
├── 00_研究方向.md
├── <论文短名-年>/           # 每篇论文一个文件夹：pdf + md
├── 文献综述.md
├── 解决方案/                # 01 场景分析 / 02 实现逻辑 / 03 代码架构
├── implementation/          # 流程三代码实现 + 实验图 figures/
├── paper/                   # 流程四论文 + versions/（历史版本与 review 反馈）
└── figures/                 # 科研插图工具产出（示意图）
```

## 第三方来源与许可

- Skill 本体（SKILL.md / workflows / standards / tools / references 自研部分）：MIT（见 LICENSE）。
- `scripts/fetch.py`、`scripts/cloak_pdf.py`：源自 [obra/paper-fetch](https://github.com/obra/paper-fetch)，遵循其上游许可证。
- `scripts/anysearch/`：来自 AnySearch，Apache-2.0（目录内附 LICENSE/NOTICE）。
- `plugins/scientific-illustrator/`：来自 [icebird1998/scientific-illustrator](https://github.com/icebird1998/scientific-illustrator)（作者：科研up主:进击的土博），MIT License，已完整内嵌（3 个 MCP server + 6 个子 skill + officejs）。
- `references/` 中部分规范为改写自公开 skill 生态（详见各文件「参考来源」），按「改写 + 标注来源」处理。
- MinerU 为 [opendatalab/MinerU](https://github.com/opendatalab/MinerU) 的 Open API CLI。

## 更新

```bash
# 已安装的 skill 目录内
git pull
```

或重新运行一键安装脚本（覆盖安装）。
