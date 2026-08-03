# 检索筛选与综述综合指南

来源：改编自 ARS（academic-research-suite）的 literature_strategist_agent 与 synthesis_agent；v2.0 增补自 co-researcher（systematic-review / research-synthesis / literature-review）与 agent-research-skills（deep-research / literature-review）。

## 1. 检索三关通用门槛（UNIVERSAL GATES）

任何文献进入候选清单前，必须通过三关，任何情况都不放宽：

| 门槛 | 检查内容 | 不通过则 |
|------|----------|----------|
| 相关性（relevance_to_RQ） | 摘要是否直接回应研究问题/主题 | 剔除 |
| 方法学（methodology_not_fatally_flawed） | 有无致命设计缺陷、结论是否可信 | 剔除 |
| 非掠夺性/非伪造（not_predatory_or_fabricated） | 来源期刊是否掠夺性、数据/引用是否伪造 | 剔除 |

注意：允许放宽的只有「是否同行评审 / 是否预印本 / 是否较老经典文献 / 时间窗」；绝不允许放宽上表三关。

## 2. 布尔检索式

用 AND / OR / NOT 组合关键词，先宽后窄：

    ("概念A" OR "概念B" OR "同义词") AND ("核心概念C") NOT ("排除词D")

- 每个概念先列同义词/上下位词再合并（含领域术语：方法词、应用词、评估指标词）；
- 结果过多则加 AND 收紧，结果过少则删 NOT / 加 OR 放宽；
- **迭代检索协议**：第 1 轮核心布尔式 → 分析高引论文关键词/标题模式 → 优化检索式（加同义词、领域术语）→ 第 2 轮补检；最多 2–3 轮防发散；
- 每个数据源记录：检索式、检索日期、命中数（写入 `02_检索日志.md`）。

### 2.1 检索陷阱（OpenAlex）

- 裸 `search` + `sort=cited_by_count:desc` 按「名气」而非「相关性」排序，可能混入只含关键词的经典论文（如搜「LLM 摘要筛选」返回 PRISMA Statement / Rayyan）；
- 正确姿势：先用子主题/概念过滤（`filter=topics.id:T<id>` 或 `concepts.id:C<id>`）收窄到领域切片，再在切片内按引用排序；
- 引用排序只在已收窄的主题过滤内使用。

## 3. 纳入 / 排除标准（Inclusion / Exclusion）

- 检索前先定纳入标准（直接回应研究问题、时间窗、文献类型）与排除标准（偏离主题、预印本中的低质内容、掠夺性期刊）——**方案卡锁死后不中途放水**；
- 按「标题 → 摘要 → 全文」三级扫描；
- 剔除的文献在 `01_检索结果.md` 中记录**剔除原因（excluded_reason）**，不允许静默排除；
- 候选池 > 50 篇时，先随机试筛 ~20 篇校准标准，再批量筛（Pilot screening）。

## 3.1 跨库去重（Deduplication）

多源检索（Semantic Scholar / Crossref / OpenAlex / arXiv）必然重复：

1. 先按 **DOI** 去重；
2. 剩余按「归一化标题 + 第一作者姓氏 + 年份」去重；
3. 去重后数量写入 `01_检索结果.md` 与 `02_检索日志.md`（PRISMA Identification 数）。

## 3.2 来源质量分级（Source Quality Tiers）

每条纳入文献标注来源等级（参考 deep-research）：

| 等级 | 类型 | 处理 |
|------|------|------|
| 1 | 顶会（NeurIPS/ICML/ICLR/ACL/CVPR/AAAI/KDD 等） | 正常纳入，优先 |
| 2 | 同行评审期刊（JMLR/TACL/Nature/Science 等） | 正常纳入，优先 |
| 3 | Workshop（有评审、门槛低） | 可纳入，标注 |
| 4 | 高引 arXiv 预印本 | 可纳入，标注 `(preprint)` |
| 5 | 近期 arXiv 预印本（<3 个月） | 谨慎，仅作补充证据，标注 `(preprint)` |

- preprint 用途：补充最新结果、尚无同行评审版本的方向；不作为持久性结论的唯一依据；
- 引用时对非同行评审工作标注 `(preprint)`。

## 4. 滚雪球引用追踪（Snowballing）

- 向后追溯（backward）：从综述/关键论文的参考文献列表中找回源文献（seed DOIs）；
- 向前追踪（forward）：用 OpenAlex cited_by_api_url 或 Semantic Scholar citations 接口追踪高引论文的被引文献；
- 每轮滚雪球最多 1–2 轮，防止发散；新增文献同样过三关、记录 reason 与来源等级。

## 5. 综述综合方法（Synthesis Methods）

综合 ≠ 逐篇摘要。综合是跨文献建立新理解：连接观点、识别模式与矛盾、映射收敛与分歧、指出知识空白。

### 5.1 主题综合（Thematic Synthesis）
- 从文献中识别反复出现的主题，给发现编码到主题；
- 建立「主题 × 文献」映射（文献矩阵），统计每个主题的证据强度；
- 每个主题下先讲共识，再讲分歧，再给该主题小结。

### 5.2 叙述综合（Narrative Synthesis）
- 按时间线或概念脉络组织叙述，说明研究如何演进；
- 适合主题较发散、证据不统一的情况。

### 5.3 框架综合（Framework Synthesis）
- 用预先定义的分析框架（如理论模型、分类体系）作为骨架，把文献归入框架各维度；
- 适合有明确分析框架的研究问题。

### 5.4 跨源对比与分歧溯源（v2.0，参考 research-synthesis）
- **Agreement Mapping**：识别哪些结论是多个来源一致支持的（共识区）；
- **Disagreement Analysis**：对矛盾结论溯源——差异来自**方法、人群/数据集，还是情境**（例如「方法 A 有效」在某数据集成立、另一数据集不成立，不是矛盾而是边界条件）；
- **Evidence-First**：每条综合声明列出支持来源（「A、B 一致支持，C 有分歧」）。

### 5.5 证据加权与置信度标注（v2.0）
- **证据加权**：同行评审、大样本、多数据集、严格统计的研究权重更高；预印本与增量工作降权；
- **置信度标注**：用校准语言区分——
  - `共识（consensus）`：多来源一致、证据强；
  - `新兴（emerging）`：方向新、证据在累积；
  - `争议（contested）`：来源间存在实质分歧；
- 置信度与 Evidence Record 的 claim strength（speculative/observed/supported/strong）一致，不静默升级。

### 5.6 多视角综合（v2.0，可选，参考 literature-review/STORM）
- 主题跨多个子方向时，模拟 3–5 个专家视角（如「做效率的 ML 系统研究者」「做理论保证的统计学家」）；
- 每个视角做多轮 Q&A：视角提问 → 生成检索查询 → 检索补漏 → 基于论文作答（带引用）；
- 合并各视角产出，去冗余，按主题组织——保证覆盖多样性（不只覆盖最流行的方法）。

## 6. 反模式（Anti-Patterns）

- 只挑支持自己偏好的证据，忽略矛盾证据（cherry-picking）；
- 逐篇罗列摘要而不做跨文献连接（sequential summary 不等于 synthesis）；
- 把相关性弱、方法学有缺陷或掠夺性来源写进综述；
- 无法追溯来源的结论进入综述；
- 把「争议」写成「共识」，把「新兴」写成「已确立」（置信度虚高）；
- 凑数：文献不足时硬写（诚实优先于 fulfillment）。

## 7. 综述方法学自述

综述正文应包含一段方法学自述：检索的数据库、检索式（或检索日志引用）、时间窗、纳入/排除标准、去重后最终纳入文献数——让综述可复现、可审计。数据直接来自 `02_检索日志.md`。
