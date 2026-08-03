# 写作规范索引（Standards Index）

本目录存放 scholar 各流程中**写作任务的独立规范**，回答「怎么写」的问题。
每个写作任务一份规范文件，相互独立，可单独更新；规范随用户反馈持续成长。

## 规范清单

| 规范文件 | 对应流程 | 写作任务 / 产出文件 |
|----------|----------|----------------------|
| `通用写作规范.md` | 全部流程 | 跨任务底线：反 AI 腔 / 过度声称护栏 / 术语保护 / 完整性（所有写作任务同时执行） |
| `研究方向确认规范.md` | 流程0 | `<主题>/00_研究方向.md` + `00_研究问题卡.md`（v2.0：SMART 问题/证据记录/方法路线/Proposal Readiness Gate） |
| `综述写作规范.md` | 流程一 | `文献综述.md` |
| `解决方案-场景分析与问题剖析.md` | 流程二 | `解决方案/01_场景分析与问题剖析.md` |
| `解决方案-实现逻辑与方案设计.md` | 流程二 | `解决方案/02_实现逻辑与方案设计-方案X.md`（v3.1 方法论：问题类型决策树、资源适配、4 阶段渐进实验、一个方案一篇、逐篇生成） |
| `解决方案-代码架构设计.md` | 流程二 | `解决方案/03_代码架构设计.md`（v3.2 架构层面 + 学术场景适配 + 实现顺序对齐 4 阶段实验 + 评审门禁） |
| `代码实现规范.md` | 流程三 | 按 03 架构生成的代码文件与测试（v1.1：TDD + 编码规范 + 系统化调试 + 验证证据门禁） |
| `论文写作规范.md` | 流程四 | 英文论文 `.tex` + 编译 `.pdf`（v2.0：六步写作顺序 + 六维 review + 主张-证据纪律 + 引用禁编造；历史版本与 review 反馈存档于 `paper/versions/`） |

> 各任务专属规范开头均标注「与 `通用写作规范.md` 同时生效」；只改通用问题（如措辞校准）时更新通用规范，只改某任务写法时更新对应专属规范。

## 成长机制（反馈 → 更新）

1. **每次交付写作任务后，主动询问用户反馈**：哪些地方不满意、哪些写法要保留、哪些要调整。
2. 收到反馈后：
   - 定位对应写作任务的规范文件（跨任务问题定位到 `通用写作规范.md`）；
   - 修改规范内容（结构要求、语言规则、检查清单等）；
   - 在规范文件的「更新记录」表中追加一行（版本、日期、反馈内容、改动）；
   - 版本号 +1。
3. **跨任务/全局性反馈**（如「所有文档都要结论先行」）：记入本索引的「全局备注」，并同步到 `通用写作规范.md` 与各相关规范。
4. 新增写作任务时：按「规范文件模板」新建一份规范，并在上表登记一行。

## 参考来源

以下外部写作类 skill 的规则已被吸收进本库（来源与具体吸收内容见 `通用写作规范.md` §0）：

- academic-writing-skills（paper-audit v6.0）：过度声称护栏 / 术语保护 / 检查清单
- humanize-academic-writing：反 AI 腔改写原则
- writing-anti-ai（本地）：反 AI 腔快速清单
- nature-polishing（本地）：style-guardrails 学术语体与完整性规则
- ml-paper-writing（本地）：核心贡献一句话、方法前置、实验区分竞争假设

若后续发现新的高质量写作规范，按同样方式：吸收 → 记录来源 → 更新对应规范版本。

### 研究方向确认类参考（流程0）

- research-ideation（scholar 内嵌 `references/research-ideation/`）：5W1H 六维度、五类 gap 分析、Research Question Card、Evidence Record、Claim/Proposal 门禁、SMART 问题——已吸收进 v2.0 规范与流程0 工作流。
- agent-research-skills（ref-external）：idea-generation（候选生成/迭代细化/三维评分）、novelty-assessment（≥3 轮检索评估/苛刻审稿）、research-planning（研究计划骨架/输出 schema）、deep-research（阶段门禁/来源质量分级）。
- co-researcher（ref-external）：research-manager（计划先行/状态持久化/决策日志）、hypothesis-testing（H₀/H₁/变量矩阵/证伪标准）。
- ARS（方法已吸收，见 `references/synthesis-guide.md`）：research_architect_agent（问题驱动方法/方法决策树）。

### 软件工程/架构类参考（代码架构设计规范）

- 已下载到项目 `ref-external/`（gstack、superpowers、wondelai-skills、ai-agents-public、claude-software-skills、software_development_skills、qodex-ai-agent-skills、context-engineering-kit、melodic-claude-code-plugins），完整清单见 `ref-external/README.md`。
- 与「代码架构设计」最对口：wondelai/design-code-architecture（8 阶段架构旅程 + ADR）、ai-agents-public/software-architecture-design（模式选型决策树）、qodex/system-design（代码风格硬规则）、superpowers（TDD/验证闭环）、gstack（计划/设计评审）。
- 吸收方式：改写 + 标注来源，更新 `standards/解决方案-代码架构设计.md` 并在更新记录登记。

### 论文写作类参考（论文写作规范 / 流程四）

- 已下载到 `ref-external/`：latex-document-skill（LaTeX 编译工程，已改写为 Python 跨平台脚本）、ai-development-team（多角色分工 + 负面判据）、alirezarezvani-claude-skills（boardroom 多角色讨论架构）、agent-research-skills（latex-formatting 会议模板与投稿检查）。
- 与「论文写作规范」最对口：boardroom（独立立场 → 交叉审阅 → 合成裁决）、ai-development-team（问题未清空不得声称完成）、latex-document-skill（引擎检测/多遍编译/错误解析）。
- 吸收方式：改写 + 标注来源，更新 `standards/论文写作规范.md` 并在更新记录登记。

## 规范文件模板

    # <写作任务>写作规范
    版本：v1.0（YYYY-MM-DD）
    适用：<对应流程 / 产出文件>
    模板：<可选，内容骨架>

    ## 1. 写作目标
    ## 2. 结构要求
    ## 3. 语言与表达
    ## 4. 引用与溯源（禁止编造）
    ## 5. 检查清单
    ## 更新记录

## 全局备注

- 所有文档结论先行；每条观点必须可回溯到文献（MD 文件）。
- 反 AI 腔、过度声称校准、术语保护为全流程底线（见 `通用写作规范.md`）。

（跨任务通用规范记录在这里，随反馈追加）


