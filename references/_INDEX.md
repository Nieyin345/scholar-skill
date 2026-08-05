# 参考文档检索索引（references/_INDEX.md）

> 用途：在 scholar 内查找「某个问题该读哪个参考文件」。需要参考某类内容时**先读本索引定位，再打开对应文件**；不要整目录扫读、不要整篇读大文件。
> 通用规则：多文件目录一律先读入口（`GUIDE.md`），再按需打开子文件；大文件（>8KB）先用 `rg "<关键词>" <文件>` 定位小节再读；引用路径时写文件本身（`.md`），不只写目录名。

## 按任务 / 场景速查

| 任务 / 场景 | 读哪个（优先级从上到下） |
|-------------|--------------------------|
| 流程0：澄清研究方向 | `research-ideation/GUIDE.md` → `research-ideation/references/5w1h-framework.md` → `gap-analysis-guide.md` |
| 流程0：候选拆分 / gap 验证 | `research-ideation/references/gap-analysis-guide.md` |
| 流程0：写研究问题卡 / 研究契约 | `research-ideation/references/research-question-formulation.md` + `research-contract.md` |
| 流程0：方法初选 | `research-ideation/references/method-selection-guide.md` |
| 流程0：研究计划骨架 | `research-ideation/references/research-planning.md` |
| 流程一：检索策略 / 数据源 | `search-protocols/`（按数据源选读）+ `research-ideation/references/literature-search-strategies.md` + `synthesis-guide.md` |
| 流程一：质量筛选 / 关键词 | `search-quality/quality-criteria.md` + `search-quality/keywords.md` |
| 综述写作结构 | `literature-review-template.md`（结构模板）+ `standards/综述写作规范.md`（写法规则） |
| 引用核验（写任何含引用文档时） | `citation-verification/GUIDE.md` → `citation-verification/references/verification-rules.md` → `common-errors.md` → `api-usage.md` |
| 流程二：解决方案三文档 | `solution-templates/01_场景分析与问题剖析.md` / `02_实现逻辑与方案设计.md` / `03_代码架构设计.md`（按步骤对照） |
| 流程四：Nature 风格写作 | `nature-writing/GUIDE.md`（自带「When to open extra files」表，按章节选子文件） |
| 流程四：论文自查 | `paper-self-review/GUIDE.md` → `paper-self-review/references/SECTION-CHECKLIST.md` → `FINAL-VERDICT.md` |
| 流程四：默认 LaTeX 模板 | `latex-template/`（`main.tex` + `IEEEcsmag.cls`；`README.md` 说明使用方式） |
| Obsidian URI / 插件命令控制 | `obsidian-uri.md` |
| 网页提取（defuddle） | `web-extraction.md` |
| Zotero 目录 / 缓存规则 | `zotero-rules.md` |
| 密钥获取（用 key 时才读） | `key-setup-guide.md` |
| 导航文档模板 | `project-navigation-template.md`（主题级）/ `vault-navigation-template.md`（笔记库级） |

## 多文件目录子文件速查

### research-ideation/（流程0 主参考）

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `GUIDE.md` | 入口：5W1H / 文献综述 / gap / 研究问题 / 方法 / 计划 全流程 | 流程0 启动 |
| `references/5w1h-framework.md` | 5W1H 六维度头脑风暴 | 澄清 / brainstorm |
| `references/gap-analysis-guide.md` | 五类研究 gap | 候选拆分 / 验证 |
| `references/research-question-formulation.md` | 研究问题卡（SMART） | 写问题卡 |
| `references/research-contract.md` | 问题 / 假设 / 证据 / 证伪标准 | 研究契约 |
| `references/method-selection-guide.md` | 方法选择 | 方法初选 |
| `references/literature-search-strategies.md` | 检索策略 | 流程一 |
| `references/research-planning.md` | 研究计划骨架 | 计划产出 |
| `references/zotero-integration-guide.md` | Zotero 集成 | 需要 Zotero 时 |
| `examples/example-research-proposal.md` / `example-literature-review.md` | 完整示例 | 需要样例 |

### citation-verification/（引用核验）

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `GUIDE.md` | 入口：核验原则与核心问题 | 引用核验启动 |
| `references/verification-rules.md` | 逐条核验规则（最常用） | 逐条核验引用 |
| `references/common-errors.md` | 常见引用错误模式 | 自查引用 |
| `references/api-usage.md` | 核验 API 用法 | 配合 `scripts/citation-verification/` |

### nature-writing/（Nature 风格写作）

- 入口 `GUIDE.md` 自带「When to open extra files」表；写具体章节时按表打开：`abstract.md`（摘要）/ `introduction.md`（引言）/ `related-work.md`（相关工作）/ `conclusion.md`（结论）/ `paragraph-flow.md`（段落流）/ `article-architecture.md`（结构）/ `paper-review.md`（审稿视角）/ `chinese-author-workflow.md`（中文→英文写作流程）。

### paper-self-review/（论文自查）

| 文件 | 内容 |
|------|------|
| `GUIDE.md` | 入口：结构 / 逻辑 / 引用 / 主张审计 |
| `references/SECTION-CHECKLIST.md` | 分节自查清单 |
| `references/FINAL-VERDICT.md` | 最终判定规则 |
| `examples/example-self-review.md` | 自查示例 |

### search-protocols/（检索 API 协议）

- `openalex_api_protocol.md` / `crossref_api_protocol.md` / `arxiv_api_protocol.md` —— 按检索数据源选读（OpenAlex / Crossref / arXiv）。

### search-quality/（检索质量）

- `quality-criteria.md`：质量评分 / 顶刊高引用优先标准；`keywords.md`：关键词构建与检索式。

### solution-templates/（流程二三文档模板）

- `01_场景分析与问题剖析.md` / `02_实现逻辑与方案设计.md` / `03_代码架构设计.md` —— 流程二按步骤生成时对照（与 `standards/解决方案-*.md` 配套：模板管结构，规范管写法）。

### latex-template/（默认论文格式模板）

- `main.tex` + `IEEEcsmag.cls`（IEEE CS Magazine 官方格式，仅格式不限定写作风格）；流程四自动复制到 `论文/<主题>/thesis/`；`README.md` 说明编译与使用。

## 检索技巧

- 定位内容优先 `rg`：全库 `rg "关键词" references/`；单个大文件 `rg "<小节名>" references/nature-writing/introduction.md`；
- 只读需要的子文件，不整目录 / 整文件扫读（上下文是公共资源）；
- 融合子 skill（research-ideation / citation-verification / nature-writing / paper-self-review）入口都是 `GUIDE.md`，其内部子文件路径相对于各自目录；
- 不确定读哪个 → 先读本索引，再按「按任务速查」定位。
