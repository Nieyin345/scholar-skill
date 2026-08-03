# scholar 密钥获取教程（首次触发必读）

首次触发 scholar 时，会**先完成密钥配置，再回答你的问题**。本文件列出全部密钥的用途与获取方式；每个密钥都过一遍（提供，或对可选项明确说「跳过」）后即完成，之后不再要求重填。

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

## 配置流程（agent 按此执行）

1. 运行 `python scripts/manage_keys.py list` 查看 `.env` 已有的密钥；
2. 依次询问三个密钥（缺失的）：用户提供 → `python scripts/manage_keys.py set <KEY> <value>` 保存；用户明确说「跳过」→ 记为跳过，不保存；**每个密钥都要过一遍，未处理完不得进入下一步**；
3. 全部处理完后 `python scripts/setup_state.py complete` 标记首次配置完成；
4. **配置完成后，回到用户最初的问题**，按正常流程回答。

> 密钥保存在 `<skill_dir>/.env`（本机文件，不上传 GitHub）；之后更新 skill（git pull / 重装）会自动保留，不会要求重填。
