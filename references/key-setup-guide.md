# scholar 密钥获取教程（按需查阅）

scholar **不设「先配置再使用」的首次触发门禁**：密钥只在**用到的那一刻**按需获取——功能需要且缺失时，agent 会查阅本文件，把用途与获取方式列给你；你提供后保存到本地 `.env`，之后自动复用；key 失效（401 / 403 / invalid / expired）时同样按本文件重新获取。

## 1. ANYSEARCH_API_KEY — 实时搜索（可选，匿名可用）

- **用途**：流程0/一的实时网络与文献检索（高质量/高引文献搜索）。
- **获取**（注册只需真实邮箱，约 30 秒，免验证码）：
  - 方式 A（推荐）：把你的邮箱告诉 agent，agent 调用 anysearch 注册接口一键注册，密码会发到该邮箱，之后在 anysearch 控制台拿到 API Key 交给 agent 保存；
  - 方式 B：到 https://www.anysearch.com 注册并登录 → 控制台获取 API Key。
- **不填**：功能仍可用，但走匿名模式（有次数限制）。

## 2. MINERU_TOKEN — PDF→MD 精提取（仅 extract 模式需要）

- **用途**：文献 PDF 转 Markdown（流程一、书籍库）。`flash` 模式免认证可直接用；`extract` 精提取（保留布局 + 图表资产）才需要 Token。
- **获取**：到 https://mineru.net 注册 → 控制台 → API 管理 / Token 页面创建 API Token（直达：https://mineru.net/apiManage/token ）。
- **不填**：转换自动使用 `flash` 模式（免认证，质量略低）。

## 3. UNPAYWALL_EMAIL — 文献下载 Unpaywall 源（可选）

- **用途**：流程一 `fetch.py` 下载论文时启用 Unpaywall 合法免费全文源。
- **获取**：**无需注册**，Unpaywall API 免费，官方只要求提供一个邮箱作为 API 调用标识（推荐机构邮箱）：https://unpaywall.org 。
- **不填**：下载少一个免费源（仍走 arXiv / 开放获取等源）。

## 按需获取流程（agent 按此执行）

1. 执行到需要某个 key 的功能时，先 `python scripts/manage_keys.py get <KEY>` 检查 `.env`；已有 → 直接复用，不询问；
2. 缺失 → 把本文件对应小节（用途 + 获取方式）展示给用户，询问密钥；
3. 用户提供 → `python scripts/manage_keys.py set <KEY> <value>` 保存后继续执行；用户明确「跳过」→ 降级运行（AnySearch 匿名 / MinerU flash / Unpaywall 少一个源），不阻塞、不反复追问；
4. 脚本报 key 失效（401 / 403 / invalid / expired）→ 告知用户该 key 已失效，重新执行第 2~3 步，覆盖保存后重试。

> 密钥保存在 `<skill_dir>/.env`（本机文件，不上传 GitHub）；之后更新 skill（git pull / 重装）会自动保留，不会要求重填。
