---
name: luzzycode-bootstrap
description: >
  Use when starting an initial conversation on a host where MemOS memory or
  AnySearch web search is not yet configured, or when the user asks how to set
  up those two capabilities.
  Handles the keyless AnySearch CLI fallback, REST anonymous mode, self-fetching
  the reference docs and skill links, and API key configuration guidance for both
  services.
  Triggers: "not configured", "no API key", "how do I set up search",
  "how do I set up memory", "first time", "未配置", "没有密钥", "怎么配置",
  "首次使用", "装不上".
  Do NOT use when both capabilities are already working (call luzzycode-search or
  luzzycode-memory directly), or for installing unrelated software.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "onboarding"
---

# LuzzyCode · 首次配置引导

**前提**：用户首次对话，且本机未挂载 MemOS 记忆或 AnySearch 搜索。

**核心原则**：**不要因为「没配 Key」而停止工作**——AnySearch 匿名通道足以完成检索与抓取，先干活，再引导配置。

## 第一步：用免密钥通道打通检索

### 方式 A — AnySearch Skill CLI（推荐）

```bash
# 1) 下载 Skill 包
curl -L -o anysearch-skill.zip https://github.com/anysearch-skill/anysearch-skill/archive/refs/heads/main.zip
#    直连不通走镜像：
#    https://gh-proxy.com/https://github.com/anysearch-skill/anysearch-skill/archive/refs/heads/main.zip
unzip anysearch-skill.zip

# 2) 自检 —— 按已装运行时择一
python <skill_dir>/scripts/anysearch_cli.py doc        # Python>=3.6 + requests
node   <skill_dir>/scripts/anysearch_cli.js doc        # Node>=12，无外部依赖
powershell -ExecutionPolicy Bypass -File <skill_dir>/scripts/anysearch_cli.ps1 doc
bash   <skill_dir>/scripts/anysearch_cli.sh doc

# 3) 搜索与抓取
python <skill_dir>/scripts/anysearch_cli.py search "关键词" --max_results 5
```

Verify: 自检命令返回一段 JSON 即安装成功。

### 方式 B — REST 匿名直调（无脚本时）

```bash
# 搜索
curl -X POST https://api.anysearch.com/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"关键词","max_results":10,"format":"markdown"}'

# 垂直搜索：加 tag（单值 {domain}.{sub_domain}）+ params
curl -X POST https://api.anysearch.com/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Go 1.26 release notes","tag":"code.doc","params":{"library":"golang"},"max_results":10}'

# 查垂直域定义（不消耗配额）
curl "https://api.anysearch.com/v1/sub-domains?domain=code&domain=finance"

# 抓网页（严格 JSON：仅 url 一个字段）
curl -X POST https://api.anysearch.com/v1/extract \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article"}'
```

- **匿名模式无需 Authorization 头**，按 IP 限流 + 日配额
- **不要**带无效 Key——网关会返回 401/403，**不会**静默降级为匿名
- **402 配额耗尽会自动注册**：响应 message 含 `username` / `password` / `api_key`；**整条响应按敏感信息处理**，不写日志、不入公开文件，拿到后改用 `Authorization: Bearer <key>`

## 第二步：自行读文档与 skill

用刚打通的通道抓取下列内容并读懂，再向用户解释：

1. AnySearch API 文档 —— https://www.anysearch.com/docs
2. MemOS 文档总览 —— https://memos-docs.openmem.net/cn/
3. MemOS MCP 接入指南 —— https://memos-docs.openmem.net/cn/mcp_agent/mcp/guide/
4. 常驻提示词 §1.1 表格里的全部 skill 链接
5. 本仓库 —— https://github.com/LuzzyMeow/LuzzyCode （检查自身 skill 是否有更新）

## 第三步：指导用户配置

**一次说清，不挤牙膏**。先复述落点，确认后再写入。

### AnySearch
- 建 Key：https://www.anysearch.com/console/api-keys
- 写入变量：`ANYSEARCH_API_KEY`
- MCP 传输方式按宿主选：
  - **streamable-http（首选）**：`{"mcpServers":{"anysearch":{"type":"streamable-http","url":"https://api.anysearch.com/mcp","headers":{"Authorization":"Bearer ${ANYSEARCH_API_KEY}"}}}}`
  - **stdio 代理**（Cline / VS Code Copilot / 旧版客户端）：用 `mcp-remote` 桥接
  - **SSE 代理**（Cursor / Windsurf）：先用 `supergateway` 起本地代理，再指向 `http://localhost:8000/sse`
- 不配 Key 也可用：省掉 `headers` 即走匿名

### MemOS
- 建 Key：https://memos-dashboard.openmem.net/cn/apikeys/
- 写入变量：`MEMOS_API_KEY` + `MEMOS_USER_ID` + `MEMOS_CHANNEL=MODELSCOPE`
- **`MEMOS_USER_ID` 必须用稳定标识**（邮箱 / 姓名全称 / 工号），**不要**用随机值、设备 ID 或会话 ID——同一用户在不同设备上必须一致
- stdio 配置：
  ```json
  {"mcpServers":{"memos-api-mcp":{"timeout":60,"type":"stdio","command":"npx",
    "args":["-y","@memtensor/memos-api-mcp@latest"],
    "env":{"MEMOS_API_KEY":"<key>","MEMOS_USER_ID":"<stable-id>","MEMOS_CHANNEL":"MODELSCOPE"}}}}
  ```
- 参考：npm `@memtensor/memos-api-mcp`

## 第四步：写盘前复述

告诉用户将要写入**哪个文件、哪个变量名**，确认后再落盘（安全红线）。**密钥绝不写进代码、日志、公开文件或本预设正文。**

## 示例

Input: 用户首次对话，本机无搜索与记忆工具，任务是「帮我查一下某个库的最新版本」
Output: 不索要 Key → 走方式 A 或 B 匿名搜索 → 给出答案 → 顺带说明「如需更高配额与跨会话记忆，可配这两个 Key」并给控制台链接

Input: 用户问「这两个工具怎么配」
Output: 抓取两份官方文档 → 按本机宿主给出对应传输方式的完整配置片段 → 复述落点 → 等确认

Input: 用户说「不想配 Key」
Output: 不重复索取 → 继续用匿名通道完成任务 → 说明配额限制这一缺失影响

## Verify

- 引导阶段是否真的完成了检索？（不是只给了链接就结束）
- 配置片段是否匹配用户实际的宿主与传输能力？
- 写盘前是否复述了落点并获得确认？
- `MEMOS_USER_ID` 是否是稳定标识而非随机值？
- 用户拒绝后是否停止索取？
