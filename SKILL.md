---
name: scholar
description: |
  学术研究全流程 Skill，覆盖「研究方向分析/细化 → 文献检索/下载/转MD → 文献综述 → 解决方案设计 → 代码实现 → 论文写作（LaTeX）→ 科研插图/学习笔记/知识库检索」。凡学术/科研场景任务（包括「帮我分析/细化研究方向」「GNN+强化学习（如 MAPPO）做网络资源调度、QKD 应用」这类方向分析与论文写作）优先触发本 Skill，优先于 generic 研究类/文献类 Skill。
  触发词：「确定研究方向」「帮我分析这个方向」「细化方向」「帮我选题」「方向太模糊」「brainstorm」「检索文献」「下载论文」「找文献」「做文献综述」「review the literature」「summarize papers」「文献调研」「写论文」「paper writing」「latex 写作」「画图」「科研插图」「graphical abstract」「整理文件」「导入教材」「书籍入库」「检索我的知识库」「参考我的笔记」「根据我的文档回答」「rag」「retrieve」等。
  已实现：流程0「研究方向确认」（模糊方向 → 多轮交互 + 文献验证收敛为可执行方向）、流程一「文献检索与文献综述」（三步可拆可合）、流程二「解决方案设计」（场景分析/实现逻辑/代码架构三份文档，多方案逐篇生成）、流程三「代码实现」（按代码架构 TDD 落地）、流程四「论文写作」（写→润色→翻译→再润色→review 循环，LaTeX 编译，历史版本与 review 反馈存档）。
  首次触发判定：读取 skill 根目录 state.json，不存在或 setup_complete != true 即为首次触发，需先完成一次性配置（密钥 + 自动创建三库骨架，见「首次触发状态」）；每次触发先检查该状态，再路由到对应流程。
---

# Scholar · 学术工作流

面向学术研究场景的通用 Skill，采用**多流程结构**：每个流程独立，可整体或分步执行。

- 本文件（SKILL.md）是**路由与总览**，只包含流程清单、触发规则和共享资产索引。
- 每个流程的详细步骤存放在 `workflows/` 目录，**按需读取**，避免上下文臃肿。
- 共享脚本（`scripts/`）与参考文档（`references/`）由所有流程复用，只有一份。

## 首次触发状态（强制，先于一切流程）

**每次触发本 Skill，第一步必须读取 `<skill_dir>/state.json` 判断是否首次触发**，然后再进入流程路由：

- **首次触发**：`state.json` 不存在，或 `setup_complete != true`；
- **非首次触发**：`setup_complete == true`（读取并复用已保存的密钥与路径，不再询问）。

### 首次触发流程（强制：先配置密钥，再回答问题）

**铁律：首次触发时，无论用户问什么，都先完成密钥配置；全部配置完成前，不回答用户问题、不进入任何流程。**

1. 告知用户：「首次使用 scholar，需要先完成密钥配置（约 1 分钟），配置完成后我立刻回答你的问题」；
2. **展示密钥教程**：读取 `references/key-setup-guide.md`，把三个密钥的用途、获取方式（AnySearch 注册 / MinerU Token / Unpaywall 邮箱）完整列给用户；
3. **逐个收集密钥**（先 `python scripts/manage_keys.py list` 看已有哪些）：
   - `ANYSEARCH_API_KEY`（可选，匿名可用）、`MINERU_TOKEN`（可选，flash 免认证）、`UNPAYWALL_EMAIL`（可选）——依次询问，用户提供则 `python scripts/manage_keys.py set <KEY> <value>` 保存；用户明确说「跳过」才记为跳过；**每个密钥都必须过一遍，未处理完不得进入下一步**；
4. **初始化三库骨架（自动，不询问路径）**：在当前工作目录（cwd，即当前项目）直接创建三个并行的子文件夹——`论文/`（论文库）、`笔记/`（学习笔记库，可直接作为 Obsidian vault 打开）、`书籍/`（教材库）——及各库导航/索引文件：`python scripts/init_workspace.py init`；三库默认跟随当前项目；用户已有独立 Obsidian vault / 书籍库目录想复用旧库时，可在之后用 `python scripts/setup_state.py set-path <key> <value>` 显式覆盖（可选，非首次触发内容）；
5. **标记完成**：`python scripts/setup_state.py complete`（记录首次触发时间）；
6. **配置完成后，回到用户最初的问题**，按正常路由（判断流程）开始回答。

### 非首次触发

- 直接读取 `state.json` 与 `.env` 复用配置，**不重复询问密钥/路径**；
- 用户明确要求重新配置（换 key / 换路径）时：`manage_keys.py` 更新密钥、`setup_state.py set-path` 更新路径；`setup_state.py reset` 可重置为未完成状态。

### 状态文件

- 位置：`<skill_dir>/state.json`（本机级，已被 `.gitignore` 排除，**不上传 GitHub**）；
- **更新保留**：`.env`（密钥）与 `state.json`（配置）都是本机文件；`git pull` 更新或重跑安装脚本都会自动保留，**不会覆盖已保存的密钥与路径**，更新后无需重新配置；
- 模板：`state.json.example`；查看状态：`python scripts/setup_state.py status`。

## 三库文件系统（强制）

**三库默认建在当前工作目录（cwd，即当前项目），首次触发自动创建，不询问路径**：

```text
<当前项目>/                    ← cwd
├── 论文/                      ← 论文库
│   ├── 00_索引.md             ← 论文库索引（研究方向注册表，库级导航）
│   └── <主题>/                ← 研究方向文件夹（流程0/一在论文库下创建，禁止建在 cwd 根）
│       ├── 00_项目导航.md     ← 主题级导航（本 skill 维护）
│       ├── 00_研究方向.md / 03_文献综述.md / 解决方案/ / implementation/ / paper/ / figures/
│       └── <论文短名-年>/     ← 每篇论文一个文件夹：pdf + md
├── 笔记/                      ← 学习笔记库（可直接作为 Obsidian vault 打开）
│   ├── 00-导航.md / 02-Index.md / Sources/Papers/ / Knowledge/ / _system/
├── 书籍/                      ← 教材库（书籍库管理工具维护）
│   ├── 00_索引.md
│   └── <方向>/<教材名>/（pdf + md + 图床）
└── .scholar_tmp/               ← 临时工作区（会话结束清理；Obsidian 隐藏点目录）
```

- 创建命令：`python scripts/init_workspace.py init`（幂等，已存在则跳过，**不做全盘扫描**）；新建研究方向：`python scripts/init_workspace.py add-topic "<主题>"`（在 `论文/<主题>/` 建文件夹 + `00_项目导航.md` + 登记 `论文/00_索引.md`）；
- **每次触发第一步确认三库骨架存在**（缺失才创建，不检查其他文件系统内容）；**研究方向文件夹一律建在论文库下**（`论文/<主题>/`），禁止在 cwd 根目录直接创建主题文件夹；
- 三库各自导航文件各管各库，统一「文件变动时才更新」纪律（见「项目导航文档」）；
- 用户已有独立 Obsidian vault / 书籍库目录：用 `setup_state.py set-path` 覆盖默认位置（可选，不强制）。

### 工作纪律（防混乱 + 提速，强制）

1. **临时文件不进项目根目录**：所有临时脚本与中间产物（`_*.py` / `_*.txt` / `_*.json` 等）一律放 `<项目>/.scholar_tmp/`（`init` 已创建）；阶段结束或会话结束时运行 `python scripts/init_workspace.py cleanup-tmp` 清空；**禁止在项目根目录或主题文件夹散落临时文件**；
2. **优先用自带脚本，不手写重复轮子**：检索用 `scripts/anysearch/`（`search` / `batch_search`，注意 anysearch **没有 `-o` 参数**）与 `scripts/arxiv_search.py`（`-o/--output` 是其专属参数，别混用）；下载用 `scripts/fetch.py`（可一次传多个 DOI）；转换用 `scripts/convert_pdf_to_md.py`；确需写临时脚本 → 必须放 `.scholar_tmp/`；
3. **下载成功才建论文文件夹**：`论文/<主题>/<论文短名-年>/` 文件夹只在 PDF 成功落地后创建；下载失败的 DOI **不建文件夹**（已误建则删除空文件夹），只在 `01_检索结果.md` 标记 reason；
4. **长文先目录后小节**：综述/长文先读章节标题与目录，再按需读相关小节，**不重复整篇读取**（已读内容不复读）；批量检索一次查询到位，避免逐条小步调用拖慢节奏；
5. **Windows 编码**：运行脚本时如遇控制台编码报错（GBK/UnicodeDecodeError），先执行 `$env:PYTHONIOENCODING = "utf-8"` 再跑（脚本已内置 UTF-8 输出处理）。

## 流程总览

| 流程 | 名称 | 触发要点 | 状态 |
|------|------|----------|------|
| 流程0 | 研究方向确认 | 确定研究方向 / 帮我选题 / 方向太模糊 / brainstorm | ✅ 已实现 |
| 流程一 | 文献检索与文献综述 | 检索文献 / 下载论文 / 文献综述 | ✅ 已实现 |
| 流程二 | 解决方案设计 | 方案设计 / 技术方案 / 怎么实现 / 架构设计 | ✅ 已实现 |
| 流程三 | 代码实现 | 写代码 / 实现 / 落地 / 把方案做成 | ✅ 已实现 |
| 流程四 | 论文写作 | 写论文 / paper writing / latex 写作 / 把结果写成论文 | ✅ 已实现 |

## 触发路由规则

1. 触发时**先检查 `state.json` 完成首次触发判定**（见「首次触发状态」）并确认三库骨架存在（见「三库文件系统」），再判断用户需求属于哪个流程；无法判断时，询问用户要执行哪个流程。
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

1. **触发时（任何流程第一步）**：检查 `论文/<主题>/00_项目导航.md` 是否存在：不存在 → 确认主题文件夹后立即按模板生成（`python scripts/init_workspace.py add-topic "<主题>"`）；存在 → 读取并复用，确认根目录无变化后继续。**不读导航文档不开工**；
2. **文件变动时更新（铁律）**：**只有文件发生变动才更新**导航文档（创建 / 删除 / 重命名 / 移动 / 转换完成）：§文件结构（新增/移动文件）、§文档索引（状态变化）、§文献库索引（新下载/转换的论文及位置）、§当前状态、§更新记录（只增不删）；无文件变动的轮次不重写导航；
3. **位置变更必须同步**：任何文件被重命名/移动时，同步更新导航文档——不允许「文件在但导航没更新」；
4. 导航文档始终反映最新状态，历史保留在更新记录中。
5. **三库导航体系**：论文库导航 `论文/00_索引.md`（库级：研究方向注册表）+ `论文/<主题>/00_项目导航.md`（主题级：本文件）、书籍库导航 `书籍/00_索引.md`（书籍库管理工具维护）、笔记库导航 `笔记/00-导航.md`（学习笔记工具维护）——各管各库、互不替代，统一「文件变动时才更新」纪律。


## 密钥获取与保存规则

- 密钥**只在首次触发时批量询问缺失项**（判定见「首次触发状态」，教程见 `references/key-setup-guide.md`），保存到本地 `.env` 后，之后触发自动读取，不再反复询问用户。
- 保存位置：`<skill_dir>/.env`（已被 `.gitignore` 排除，**不会上传到 GitHub**）。
- 管理命令：`python scripts/manage_keys.py set <KEY> <value>` 保存；`get` / `list` / `delete` 读取、查看、删除。
- anysearch：触发时若无 `ANYSEARCH_API_KEY` 则询问用户，提供后保存；之后每次自动使用。用户没有 key 则匿名访问。
- MinerU：`flash` 免认证；`extract` 需要 `MINERU_TOKEN`——转换脚本自动从 `.env` 读取并传 `--token`；缺失时提示用户保存后再跑。
- paper-fetch：`UNPAYWALL_EMAIL` 缺失时询问用户；提供后保存，之后不再问。
- 机构认证会话：`PAPER_FETCH_INSTITUTIONAL=1`（+ `PAPER_FETCH_EZPROXY`）可选；cookie jar 存在时流程一自动走两级机构下载（见「机构认证下载」），不属首次触发必问项。
- 密钥失效/更新：`delete` 删除后重新 `set`。

## 机构认证下载（付费墙文献）

公开 OA 源（Unpaywall/S2/arXiv/PMC/OpenAlex/OpenAIRE/MDPI CDN）找不到的 2025+ 付费墙论文（IEEE、Springer、IOP、de Gruyter 等），只能靠机构订阅。scholar 内置完整机构认证下载链路，**不保存账号密码，只保存登录会话 cookie**（`<skill_dir>/.scholar_institutional/cookies.txt`，已被 `.gitignore` 排除，`git pull` 更新不会覆盖）。

### 会话建立（一次性，登录向导）

```bash
python scripts/institutional_login.py <登录URL> [额外域名...]
```

- 弹出可见浏览器，用户完成机构登录（含 MFA），回终端回车，会话 cookie 自动落盘；
- **资源 URL 分流（决定走哪条机构路径，以地址栏实际为准）**：含 `ezproxy`/`libproxy` → EZproxy 校外访问；含 `webvpn`/`vpn` → WebVPN；含 `cas`/`authserver` → 学校统一身份（看 `service=` 回调决定资源站）；含 `carsi`/`idp`/`shibboleth` → 联邦认证（CARSI/Shibboleth，「Access through your institution」选学校）；登录页不是最终失败，认证后应回到资源站；
- 入口 URL 选择：
  - 学校有 EZproxy：`https://ezproxy.<学校>.edu/login`（图书馆「校外访问」链接）；
  - 无 EZproxy 的学校（如 Politecnico di Milano）：用出版商「Access through your institution」入口——打开目标 IEEE 文章页 → Sign In → Institutional Sign In → 搜索选择学校（如 Politecnico di Milano）→ 学校登录页完成认证；额外域名填 `ieeexplore.ieee.org`；
- cookie 按域名隔离，**每个出版商登录一次**（IEEE 一次登录可下该会话内所有文章；Springer/IOP/de Gruyter 等需各自登录一次，同域名不重复）；会话通常几小时有效，MFA 属正常，过期重跑即可。

### 依赖（浏览器下载必需：cloakbrowser）

`institutional_login.py` / `institutional_download.py` 需要 `cloakbrowser` 包（stealth Chromium）。该包可能只装在某个 Python 解释器里（本机实测在 `C:\\Python313\\python.exe`，默认 anaconda 里没有）；脚本会自动探测可用解释器（优先 `CLOAKBROWSER_PYTHON` 环境变量 → 常见路径 `C:\\Python313\\python.exe` 等 → `py -0p` 列出的已装 Python → PATH → 当前解释器），探测到即自动切换，无需手动指定。若确实未安装，会打印明确指引（含安装命令与 `CLOAKBROWSER_PYTHON` 设置方法）。

```powershell
# 指定已装 cloakbrowser 的解释器（推荐；脚本自动使用，仍报"缺少"时设这个）
$env:CLOAKBROWSER_PYTHON = 'C:\Python313\python.exe'
# 在目标解释器上安装一次
& 'C:\Python313\python.exe' -m pip install -U cloakbrowser
```

### 自动判定 + 两级下载（流程一付费墙主解）

遇到付费墙下载失败时，先检查 cookie jar 是否存在（`<skill_dir>/.scholar_institutional/cookies.txt`）：

1. **一级：urllib 直连**：`PAPER_FETCH_INSTITUTIONAL=1 python scripts/fetch.py <DOI>`——带 cookie 直连出版商；适合未做浏览器指纹校验的出版商；
2. **二级：浏览器上下文下载（WAF 出版商必用）**：
   ```bash
   python scripts/institutional_download.py --dois <失败DOI清单.txt> --out <输出目录> [--headful]
   ```
   用 CloakBrowser 复用同一 cookie jar 发起请求，能通过 IEEE 的 AWS WAF（urllib 直连会被 418 拦截，即使 cookie 有效）；成功后立即触发 MD 转换；WAF 严格时加 `--headful`；
   > **三级（推荐优先）：CDP 复用已登录浏览器**——用户已在 Edge/Chrome 完成机构登录（含 MFA）时，直接用该登录态下载，**不再重复 MFA**：
   > ```powershell
   > pwsh scripts/edge_cdp.ps1          # 启动/检测带调试端口的 Edge（专用 profile）
   > # 在该 Edge 窗口完成机构登录后：
   > $env:PAPER_FETCH_INSTITUTIONAL = '1'
   > $env:PAPER_FETCH_CDP_PORT = '9222'
   > python scripts/fetch.py <DOI>      # 机构模式自动以 CDP 兜底下载付费墙 PDF
   > ```
   > 也可单独下载：`node scripts/cdp_download.mjs --url <pdf-url> --out <file.pdf> --port 9222`（零依赖，Node 22+）；端口被占用时 `edge_cdp.ps1` 自动复用现有调试浏览器（如日常 Edge 带调试端口）。
3. **cookie 过期判定**：连续 `418` / 登录页 HTML / `403` → 重跑登录向导，不影响已保存的 key。

### 下载失败分级（报告时按此判断，避免无意义重试）

- **纯付费墙**（2025-2026 新论文且无 OA）：IEEE/Springer/IOP/de Gruyter 等 `not_found` → 先查 cookie jar：有 → 走上面两级下载；无 → 询问用户是否开通机构认证（登录向导）或替换为 OA 文献；
- **HTTP 418（IEEE AWS WAF）**：cookie 有效但 urllib 被指纹拦截 → 用 `institutional_download.py`（浏览器模式）；仍 418 → 会话过期，重跑登录向导；
- **MDPI 403**：`www.mdpi.com` 对部分 IP 全 UA 封禁 → 已内置 `pub.mdpi-res.com` CDN 兜底（任意模式），一般直接成功；
- **arXiv/PMC 型**：历史 `NoneType` 崩溃已修复 → 直接重试即可；
- **Sci-Hub 命中但下载 403/not_a_pdf**：镜像 CDN 不稳定 → 属重试类，换个时段或镜像再试；
- **HTTP 200 但返回 HTML（`http_200_not_pdf`）**：登录成功但机构无该刊订阅（De Gruyter 跳 `unauthorizedDownload`；IOP 常无权限）→ 属客观无权限，**直接标记失败**并替换 OA 文献，勿反复重试/重登录；
- **超大 PDF**（>50MB，如 17MB 云端转换超时属转换问题）：下载/转换选网络稳定时段重试。

## 共享脚本索引

| 脚本 | 用途 |
|------|------|
| `scripts/fetch.py` + `scripts/cloak_pdf.py` | 文献 PDF 下载（paper-fetch，多源解析 + %PDF 校验；含 OpenAIRE 源、MDPI CDN 兜底、机构 cookie jar/EZproxy） |
| `scripts/institutional_login.py` | 机构认证登录向导（EZproxy/SSO，导出会话 cookie jar，不存密码） |
| `scripts/institutional_download.py` | 机构认证浏览器下载（复用 cookie jar 过 WAF 下载 IEEE 等付费墙 PDF，headless 默认；自动探测 cloakbrowser 解释器） |
| `scripts/convert_pdf_to_md.py` | PDF→MD 转换（MinerU CLI；内置长超时上传兜底，支持 URL 模式/大文件，extract 输出 md+images） |
| `scripts/mineru/install.ps1` | MinerU 官方安装器（随 Skill 分发） |
| `scripts/manage_keys.py` | 密钥管理（set/get/list/delete） |
| `scripts/anysearch/` | 实时搜索 CLI（anysearch） |
| `scripts/arxiv_search.py` | arXiv/bioRxiv 搜索脚本 |
| `scripts/citation-verification/` | 引用核验脚本 |
| `scripts/latex/` | LaTeX 引擎检测 + 编译脚本（流程四） |
| `scripts/books_ingest.py` | 书籍库维护：ensure-skeleton / list-orphan-pdfs / ingest（归类+转换+登记索引） |

## 自包含声明（独立 Skill）

- **scholar 为自包含 Skill**：所有方法论、规范、脚本、参考均已内嵌于本目录（`workflows/`、`standards/`、`references/`、`scripts/`、`tools/`），**不依赖任何其他 Skill 目录**；
- 文中「参考来源 / 本地 skill」字样仅表示**设计溯源**（方法源自何处），scholar 运行时不读取那些外部 skill 的文件；scholar 是多个 Skill 融合的产物，完整融合来源与链接见 `README.md`「融合产物」章节；
- 外部依赖仅为系统级工具与可选桌面应用：Python、rg、LaTeX、MinerU CLI、defuddle npm 包，以及绘图后端 draw.io desktop / PowerPoint / WPS（由内嵌 MCP server 调用，缺失时按 `tools/科研插图.md` 降级路径处理）；
- 已内嵌：research-ideation 全套（`references/research-ideation/`）、citation-verification / nature-writing / paper-self-review 参考（`references/`）、anysearch CLI（`scripts/anysearch/`）、paper-fetch 下载脚本（`scripts/fetch.py`、`cloak_pdf.py`）、scientific-illustrator v1.5.2 插件全套（`plugins/scientific-illustrator/`：3 个 MCP server + 6 个子 skill + officejs，MIT）。

## 共享参考文档

| 文档 | 内容 |
|------|------|
| `references/zotero-rules.md` | Zotero 目录/缓存规则、Evidence Record 模板、Claim Promotion Gate |
| `references/key-setup-guide.md` | 首次触发密钥教程（AnySearch / MinerU / Unpaywall 的用途与获取方式） |
| `references/citation-verification/` | 引用核验规则与 API 用法 |
| `references/paper-self-review/` | 综述/论文自查清单与最终判定 |
| `references/nature-writing/` | Nature 风格写作规范（精选章节） |
| `references/web-extraction.md` | defuddle 网页提取用法 |
| `references/search-protocols/` | 检索 API 协议（OpenAlex/Crossref/arXiv） |
| `references/search-quality/` | 检索质量标准（质量评分/关键词） |
| `references/synthesis-guide.md` | 检索三关筛选、布尔式、滚雪球、综合方法 |
| `references/literature-review-template.md` | 文献综述结构化模板 |
| `references/solution-templates/` | 解决方案三文档模板（场景分析/实现逻辑/代码架构） |
| `references/latex-template/` | 默认论文格式模板（IEEE CS Magazine（CsMag）官方模板：main.tex + IEEEcsmag.cls，仅格式） |
| `references/project-navigation-template.md` | 项目导航文档模板（`00_项目导航.md`：文件结构 / 文档索引 / 文献库索引 / 当前状态 / 更新记录） |
| `references/vault-navigation-template.md` | 笔记库导航模板（`00-导航.md`：项目笔记库结构（当前项目 `笔记/`）/ 命名规则 / 论文笔记注册表 / 当前状态 / 维护铁律） |
| `references/research-ideation/` | 研究方向确认参考（scholar 内嵌：5W1H / gap 分析 / 研究问题 / 研究契约 / 方法选择 / 检索策略 / 研究计划 / Zotero 集成） |
| `standards/` | 写作规范库（`通用写作规范.md` 跨任务底线 + 每个写作任务一份规范，随反馈持续更新；索引见 `standards/_INDEX.md`） |

## 工具索引（不在流程内，按需触发）

| 工具 | 用途 | 触发要点 | 文档 | 依赖 |
|------|------|----------|------|------|
| 科研插图 | 神经网络结构图 / 训练与推理架构图 / 流程图 / 图形摘要 / 机理图（可编辑矢量，draw.io 或 PowerPoint/WPS） | 画图 / 插图 / 结构图 / 架构图 / 流程图 / neural network diagram / graphical abstract | `tools/科研插图.md` | scholar 内嵌 `plugins/scientific-illustrator/`（MCP 注册见工具文档） |
| 学习笔记 | 把论文提炼为个人学习笔记，写入当前项目 `笔记/` 库（wiki 链接互链/跳转，搭建个人知识体系；目录可直接作为 Obsidian vault 打开） | 学习笔记 / 知识笔记 / 论文笔记 / 搭建知识体系 / knowledge note | `tools/学习笔记.md` | 无（默认当前项目 `笔记/`；可选复用既有 vault） |
| 书籍库管理 | 书籍库（PDF 教材）骨架创建 + 增量维护：游离 PDF 归类、MD 转换、`00_索引.md` 登记 | 导入教材 / 书籍入库 / 整理教材 / 检查新 pdf / 分类教材 / books / textbook | `tools/书籍库管理.md` | 可选（`scripts/books_ingest.py`） |
| 知识库检索 | 无向量 RAG 问答：回答问题时检索本地论文/笔记/书籍/Zotero 缓存并溯源（`rg` 关键词召回 + LLM 相关性 + 整页读取，不做 embedding） | 检索我的知识库 / 参考我的笔记 / 根据我的文档回答 / 查一下我之前记的 / rag / retrieve / grounded answer | `tools/知识库检索.md` | 无（`rg` 已具备，无需脚本与密钥） |

- 工具不是流程步骤：由用户在任意流程中按需触发，或流程三/四需要图表素材时调用；
- 工具产出（`论文/<主题>/figures/`，示意图目录）是流程四论文素材；实验数据图在 `论文/<主题>/implementation/figures/`（流程三按 03 §4 产出），两类图不混放；
- 新增工具时在此表登记一行，并在 `tools/` 下新建对应文档。


## 新增流程规范

新增流程时：

1. 在「流程总览」登记一行（名称、触发要点、状态）；
2. 在 `workflows/` 下新建 `流程N-名称.md`，内容包含：触发条件、触发模式（可拆可合）、步骤、输入输出、依赖的共享脚本/参考文档；
3. 在「触发路由规则」中补充该流程的文件映射；
4. 流程内如有写作任务，在 `standards/` 下新建对应写作规范（见 `standards/_INDEX.md` 模板）并登记；
5. 共用 `scripts/` 与 `references/`，不复制脚本，不修改其他流程文件。

