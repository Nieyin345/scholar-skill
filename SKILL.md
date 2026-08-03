---
name: scholar
description: |
  学术场景通用 Skill，多流程结构。已实现流程0「研究方向确认」（模糊方向 → 多轮交互 + 文献验证收敛为可执行方向）、流程一「文献检索与文献综述」（三步可拆可合）、流程二「解决方案设计」（基于文献产出场景分析/实现逻辑/代码架构三份文档，多方案逐篇生成）、流程三「代码实现」（按代码架构用 TDD 落地实现）与流程四「论文写作」（写→润色→翻译→再润色→review 循环，LaTeX 编译，历史版本与 review 反馈存档）。
  触发词：「确定研究方向」「帮我选题」「方向太模糊」「brainstorm」「检索文献」「下载论文」「找文献」「做文献综述」「review the literature」「summarize papers」「文献调研」「写论文」「paper writing」「latex 写作」「画图」「科研插图」「graphical abstract」「整理文件」「导入教材」「书籍入库」「检索我的知识库」「参考我的笔记」「根据我的文档回答」「rag」「retrieve」等。
  触发时先判断属于哪个流程，再读取 workflows/ 下对应流程文件执行。
---

# Scholar · 学术工作流

面向学术研究场景的通用 Skill，采用**多流程结构**：每个流程独立，可整体或分步执行。

- 本文件（SKILL.md）是**路由与总览**，只包含流程清单、触发规则和共享资产索引。
- 每个流程的详细步骤存放在 `workflows/` 目录，**按需读取**，避免上下文臃肿。
- 共享脚本（`scripts/`）与参考文档（`references/`）由所有流程复用，只有一份。

## 流程总览

| 流程 | 名称 | 触发要点 | 状态 |
|------|------|----------|------|
| 流程0 | 研究方向确认 | 确定研究方向 / 帮我选题 / 方向太模糊 / brainstorm | ✅ 已实现 |
| 流程一 | 文献检索与文献综述 | 检索文献 / 下载论文 / 文献综述 | ✅ 已实现 |
| 流程二 | 解决方案设计 | 方案设计 / 技术方案 / 怎么实现 / 架构设计 | ✅ 已实现 |
| 流程三 | 代码实现 | 写代码 / 实现 / 落地 / 把方案做成 | ✅ 已实现 |
| 流程四 | 论文写作 | 写论文 / paper writing / latex 写作 / 把结果写成论文 | ✅ 已实现 |

## 触发路由规则

1. 触发时先判断用户需求属于哪个流程；无法判断时，询问用户要执行哪个流程。
2. **方向太模糊时，任何流程都不直接开始**：先走流程0（与用户交互 + 文献验证收敛方向），产出 `00_研究方向.md` 后再进入对应流程。
3. 确定流程后，读取对应文件并执行：
   - 流程0 → `workflows/流程0-研究方向确认.md`
   - 流程一 → `workflows/流程一-文献检索与综述.md`
   - 流程二 → `workflows/流程二-解决方案设计.md`
   - 流程三 → `workflows/流程三-代码实现.md`
   - 流程四 → `workflows/流程四-论文写作.md`
4. 流程内的步骤可拆可合：完整执行、只走前几步、或单独执行某一步（见对应流程文件的「触发模式」）。
5. 所有流程共用密钥规则与共享脚本；流程文件内的路径相对于 skill 根目录。
6. 写作任务交付后主动询问用户反馈，反馈用于更新 `standards/` 对应规范（成长机制见 `standards/_INDEX.md`）；所有写作任务同时遵循 `standards/通用写作规范.md`（反 AI 腔、过度声称护栏、术语保护、完整性底线）。

## 项目导航文档（强制）

每个研究主题（项目）维护一份 `00_项目导航.md`，作为**目录索引 + 文档管理入口**：定义文件结构、文献（PDF/MD）与各类文档的位置，并随文件变动持续更新。模板：`references/project-navigation-template.md`（项目根目录下的 `AGENTS.md` 若存在，以其中的规则为准）。

1. **触发时（任何流程第一步）**：检查 `<主题>/00_项目导航.md` 是否存在：不存在 → 确认项目根目录后立即按模板生成；存在 → 读取并复用，确认根目录无变化后继续。**不读导航文档不开工**；
2. **文件变动时更新（铁律）**：**只有文件发生变动才更新**导航文档（创建 / 删除 / 重命名 / 移动 / 转换完成）：§文件结构（新增/移动文件）、§文档索引（状态变化）、§文献库索引（新下载/转换的论文及位置）、§当前状态、§更新记录（只增不删）；无文件变动的轮次不重写导航；
3. **位置变更必须同步**：任何文件被重命名/移动时，同步更新导航文档——不允许「文件在但导航没更新」；
4. 导航文档始终反映最新状态，历史保留在更新记录中。
5. **三库导航体系**：论文库导航 `00_项目导航.md`（本文件）、书籍库导航 `<Books>/00_索引.md`（书籍库管理工具维护）、笔记库导航 `<vault>/Research/<项目短名>/00-导航.md`（学习笔记工具维护）——各管各库、互不替代，统一「文件变动时才更新」纪律。


## 密钥获取与保存规则

- 密钥**首次获取后保存到本地**，之后触发自动读取，不再反复询问用户。
- 保存位置：`<skill_dir>/.env`（已被 `.gitignore` 排除，**不会上传到 GitHub**）。
- 管理命令：`python scripts/manage_keys.py set <KEY> <value>` 保存；`get` / `list` / `delete` 读取、查看、删除。
- anysearch：触发时若无 `ANYSEARCH_API_KEY` 则询问用户，提供后保存；之后每次自动使用。用户没有 key 则匿名访问。
- MinerU：`flash` 免认证；`extract` 需要 `MINERU_TOKEN`——转换脚本自动从 `.env` 读取并传 `--token`；缺失时提示用户保存后再跑。
- paper-fetch：`UNPAYWALL_EMAIL` 缺失时询问用户；提供后保存，之后不再问。
- 密钥失效/更新：`delete` 删除后重新 `set`。

## 共享脚本索引

| 脚本 | 用途 |
|------|------|
| `scripts/fetch.py` + `scripts/cloak_pdf.py` | 文献 PDF 下载（paper-fetch，多源解析 + %PDF 校验） |
| `scripts/convert_pdf_to_md.py` | PDF→MD 转换（MinerU Open API CLI 封装） |
| `scripts/mineru/install.ps1` | MinerU 官方安装器（随 Skill 分发） |
| `scripts/manage_keys.py` | 密钥管理（set/get/list/delete） |
| `scripts/anysearch/` | 实时搜索 CLI（anysearch） |
| `scripts/arxiv_search.py` | arXiv/bioRxiv 搜索脚本 |
| `scripts/citation-verification/` | 引用核验脚本 |
| `scripts/latex/` | LaTeX 引擎检测 + 编译脚本（流程四） |
| `scripts/books_ingest.py` | 书籍库维护：ensure-skeleton / list-orphan-pdfs / ingest（归类+转换+登记索引） |

## 共享参考文档

| 文档 | 内容 |
|------|------|
| `references/zotero-rules.md` | Zotero 目录/缓存规则、Evidence Record 模板、Claim Promotion Gate |
| `references/citation-verification/` | 引用核验规则与 API 用法 |
| `references/paper-self-review/` | 综述/论文自查清单与最终判定 |
| `references/nature-writing/` | Nature 风格写作规范（精选章节） |
| `references/web-extraction.md` | defuddle 网页提取用法 |
| `references/search-protocols/` | 检索 API 协议（OpenAlex/Crossref/arXiv） |
| `references/search-quality/` | 检索质量标准（质量评分/关键词） |
| `references/synthesis-guide.md` | 检索三关筛选、布尔式、滚雪球、综合方法 |
| `references/literature-review-template.md` | 文献综述结构化模板 |
| `references/solution-templates/` | 解决方案三文档模板（场景分析/实现逻辑/代码架构） |
| `references/latex-template/` | 默认论文格式模板（main.tex + references.bib，仅格式） |
| `references/project-navigation-template.md` | 项目导航文档模板（`00_项目导航.md`：文件结构 / 文档索引 / 文献库索引 / 当前状态 / 更新记录） |
| `references/vault-navigation-template.md` | 笔记库导航模板（`00-导航.md`：vault 项目知识库结构 / 命名规则 / 论文笔记注册表 / 当前状态 / 维护铁律） |
| `standards/` | 写作规范库（`通用写作规范.md` 跨任务底线 + 每个写作任务一份规范，随反馈持续更新；索引见 `standards/_INDEX.md`） |

## 工具索引（不在流程内，按需触发）

| 工具 | 用途 | 触发要点 | 文档 | 依赖 |
|------|------|----------|------|------|
| 科研插图 | 神经网络结构图 / 训练与推理架构图 / 流程图 / 图形摘要 / 机理图（可编辑矢量，draw.io 或 PowerPoint/WPS） | 画图 / 插图 / 结构图 / 架构图 / 流程图 / neural network diagram / graphical abstract | `tools/科研插图.md` | scientific-illustrator 插件（可选；未装时按文档降级路径处理） |
| 学习笔记 | 把论文提炼为个人学习笔记，写入 Obsidian vault（wiki 链接互链/跳转，搭建个人知识体系） | 学习笔记 / 知识笔记 / 论文笔记 / 搭建知识体系 / 放进 Obsidian / knowledge note | `tools/学习笔记.md` | Obsidian vault（默认 `OB_database`，可选） |
| 书籍库管理 | 书籍库（PDF 教材）骨架创建 + 增量维护：游离 PDF 归类、MD 转换、`00_索引.md` 登记 | 导入教材 / 书籍入库 / 整理教材 / 检查新 pdf / 分类教材 / books / textbook | `tools/书籍库管理.md` | 可选（`scripts/books_ingest.py`） |
| 知识库检索 | 无向量 RAG 问答：回答问题时检索本地论文/笔记/书籍/Zotero 缓存并溯源（`rg` 关键词召回 + LLM 相关性 + 整页读取，不做 embedding） | 检索我的知识库 / 参考我的笔记 / 根据我的文档回答 / 查一下我之前记的 / rag / retrieve / grounded answer | `tools/知识库检索.md` | 无（`rg` 已具备，无需脚本与密钥） |

- 工具不是流程步骤：由用户在任意流程中按需触发，或流程三/四需要图表素材时调用；
- 工具产出（`<主题>/figures/`，示意图目录）是流程四论文素材；实验数据图在 `implementation/figures/`（流程三按 03 §4 产出），两类图不混放；
- 新增工具时在此表登记一行，并在 `tools/` 下新建对应文档。


## 新增流程规范

新增流程时：

1. 在「流程总览」登记一行（名称、触发要点、状态）；
2. 在 `workflows/` 下新建 `流程N-名称.md`，内容包含：触发条件、触发模式（可拆可合）、步骤、输入输出、依赖的共享脚本/参考文档；
3. 在「触发路由规则」中补充该流程的文件映射；
4. 流程内如有写作任务，在 `standards/` 下新建对应写作规范（见 `standards/_INDEX.md` 模板）并登记；
5. 共用 `scripts/` 与 `references/`，不复制脚本，不修改其他流程文件。

