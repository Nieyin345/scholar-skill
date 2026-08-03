# LaTeX 模板（scholar 默认）

- 默认模板：**IEEE Computer Society Magazine（CsMag）** 官方 LaTeX 模板（`IEEEcsmag.cls`，来自 IEEE Template Selector：https://template-selector.ieee.org）
- `main.tex` — 模板主文件（**仅格式**，不含写作风格；风格与内容规范见 `standards/论文写作规范.md`）
- `IEEEcsmag.cls` / `sfmath.sty` / `upmath.sty` — 模板类与数学宏包（随模板分发）
- `fig1.jpg` / `fig2.jpg` — 模板示例图（正式写作时替换；删除后需同步移除 `main.tex` 中对应 `\includegraphics`）
- `CsMag_template.pdf` / `IEEEtran_HOWTO.pdf` — 官方编译示例与 HOWTO（本地参考，已被 `.gitignore` 排除，不上传 GitHub）
- 用途：流程四写论文时，用户没有自己的模板则使用本模板
- 编译：`python scripts/latex/compile_latex.py main.tex`（IEEE CS Mag 推荐 pdflatex；脚本自动选择引擎）
- 参考文献：本模板使用内嵌 `\begin{thebibliography}`（IEEE 引用格式），不依赖外部 `.bib`
