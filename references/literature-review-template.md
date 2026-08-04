# Literature Review Paper Template

## Usage
This template provides the skeleton for a thematic literature review paper that synthesizes existing research, identifies gaps, and proposes future directions.

## Citation & Linking Convention（引用与链接约定，必须遵守 · Obsidian wikilink）

所有生成文档都在 Obsidian vault 中，内部引用统一用 Obsidian wikilink `[[…]]`（自动跟踪改名、生成反向链接与图谱）；相对 Markdown 链接仅用于导出到 Obsidian 外（如 GitHub 预览）。

- 每处正文引用与参考文献条目必须**可点击跳转到对应论文 MD**，禁止纯文本编号：
  - 正文：`[[论文/<主题>/<论文短名-年>/<md文件名>|<作者 年份>]]`（md 名唯一可简写 `[[<md文件名>|…]]`）
  - 参考文献：`[[论文/<主题>/<论文短名-年>/<md文件名>|<完整参考文献>]]`
- **链接目标是 md 文件，不是文件夹名**；写前用 `rg --files 论文/<主题> -g "*.md"` 核对真实文件名；历史遗留文件以实际文件名为准。
- 转换稿 md 顶部自带「原文 PDF」链接（`[[<论文短名-年>.pdf]]`，转换脚本自动插入），需要跳 PDF 时直接链它。
- 未下载 / 未转换的文献不得出现在正文引用与参考文献。

示例：
- 正文：Transformer-based schedulers achieve lower blocking ...（[[论文/<主题>/2020-multi-tenant-prov/2020-multi-tenant-prov|Cao et al. 2020]]）
- 参考文献：
  1. [[论文/<主题>/2020-multi-tenant-prov/2020-multi-tenant-prov|Cao, Y., et al. Multi-Tenant Provisioning for QKD Networks. IEEE TNSM, 2020.]]

---

# [Paper Title in Title Case]

**Author(s):** [Author Name(s)]
**Affiliation(s):** [Department, Institution]
**Date:** [Date]

---

## Abstract

[Background and rationale: 1-2 sentences.]
[Purpose and scope of the review: 1 sentence.]
[Method: 1 sentence on search strategy and source selection.]
[Key findings from the synthesis: 2-3 sentences.]
[Implications and identified gaps: 1-2 sentences.]

**Keywords**: [keyword1], [keyword2], [keyword3], [keyword4], [keyword5]

---

## 1. Introduction

### 1.1 Topic and Rationale
[Why is this literature review needed? What makes it timely?]
[2 paragraphs with citations]

### 1.2 Scope and Boundaries
[What is included and excluded? Time period? Disciplines? Geographies?]
[1 paragraph]

### 1.3 Review Methodology
[Search strategy: databases, keywords, inclusion/exclusion criteria.]
[Number of sources reviewed.]
[1-2 paragraphs]

### 1.4 Organization of the Review
[Preview the thematic structure.]
[1 paragraph]

---

## 2. [Theme 1: Descriptive Title]

### 2.1 [Sub-Theme A]
[Review literature on this sub-theme.]
[2-3 paragraphs with citations]

### 2.2 [Sub-Theme B]
[Review literature on this sub-theme.]
[2-3 paragraphs with citations]

### 2.3 Summary of Theme 1
[What does the literature collectively tell us about this theme?]
[1 paragraph]

---

## 3. [Theme 2: Descriptive Title]

### 3.1 [Sub-Theme A]
[2-3 paragraphs with citations]

### 3.2 [Sub-Theme B]
[2-3 paragraphs with citations]

### 3.3 Summary of Theme 2
[1 paragraph]

---

## 4. [Theme 3: Descriptive Title]

### 4.1 [Sub-Theme A]
[2-3 paragraphs with citations]

### 4.2 [Sub-Theme B]
[2-3 paragraphs with citations]

### 4.3 Summary of Theme 3
[1 paragraph]

---

## 5. Cross-Cutting Synthesis

### 5.1 Convergent Findings
[What do the themes agree on? What patterns emerge across themes?]
[1-2 paragraphs]

### 5.2 Divergent Findings and Debates
[Where do researchers disagree? What are the unresolved debates?]
[1-2 paragraphs]

### 5.3 Methodological Observations
[What methods dominate? What methods are underused?]
[1 paragraph]

---

## 6. Research Gaps and Future Directions

### 6.1 Identified Gaps
[List and discuss 3-5 specific gaps in the literature.]
[1-2 paragraphs]

### 6.2 Proposed Research Agenda
[What should future researchers investigate? What methods should they use?]
[1-2 paragraphs]

---

## 7. Conclusion

### 7.1 Key Takeaways
[Summarize the 3-5 most important insights from the review.]

### 7.2 Implications for Practice and Policy
[How should practitioners or policymakers use these insights?]

---

## AI Disclosure
[Standard AI disclosure statement.]

---

## References
[Complete reference list in selected citation format.]
