---
name: luzzycode-mcp
description: >
  Use when developing, importing, wiring, debugging, or maintaining an MCP
  (Model Context Protocol) server, or when adding an MCP server to a client
  such as ZCode, Claude Code, Codex, OpenCode, Hermes, or QwenPaw.
  Handles the mandatory official-SDK and spec reading, transport selection
  (stdio / Streamable HTTP / SSE), tool-design rules, client config injection,
  cross-harness path lookup, and supply-chain safety for third-party servers.
  Triggers: "MCP", "MCP server", "model context protocol", "add MCP", "mcp.json",
  "mcp_servers", "stdio server", "streamable http", "tool schema", "MCP 开发",
  "接入 MCP", "配置 MCP", "写个 MCP 工具", "MCP 报错".
  Do NOT use for calling an already-configured MCP tool (just call it), or for
  building a plugin that merely bundles an MCP server (see luzzycode-skills for
  packaging, this skill for the server itself).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "integration"
---

# LuzzyCode · MCP 开发与接入

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-mcp/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-mcp) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-mcp/SKILL.md)

## 硬性前置：先读官方来源（链接已固化，不必再搜）

**做 MCP 相关任务前，必须按常驻 §1.1 的阅读规则读完清单**——本类 6 条**超过 4 条，取其中 4 条**完整阅读（按本次任务相关性择优）。协议与会话生命周期变化快，凭记忆写必错。

### 协议与规范

| 用途 | 链接 |
|---|---|
| 规范总览与版本 | https://modelcontextprotocol.io |
| SDK 分层与选型 | https://modelcontextprotocol.io/docs/2026-07-28/sdk |
| 连接本地服务器（stdio 配置格式） | https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers |
| 协议仓库（schema 与规范源） | https://github.com/modelcontextprotocol/modelcontextprotocol |

### 官方 SDK

| 语言 | 仓库 | 说明 |
|---|---|---|
| TypeScript | https://github.com/modelcontextprotocol/typescript-sdk | 13.4k★，官方 TS SDK（服务器 + 客户端） |
| Python | https://github.com/modelcontextprotocol/python-sdk | 24.3k★，官方 Python SDK，MIT |
| 参考服务器集合 | https://github.com/modelcontextprotocol/servers | 90.3k★，官方参考实现与社区服务器目录 |

**判定标准**：只看到仓库简介或 README 摘要**不算读过**；必须读到具体的开发指引正文。

### 各客户端官方 MCP 文档

| 客户端 | 文档 |
|---|---|
| Claude Code | https://code.claude.com/docs/en/claude_code_docs_map |
| Claude 插件内 MCP 集成范例 | https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/mcp-integration/SKILL.md |
| Codex CLI | https://learn.chatgpt.com/docs/config-file/config-reference |
| Hermes Agent | https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference |
| OpenCode | https://opencode.ai/docs/mcp-servers |
| QwenPaw | https://qwenpaw.agentscope.io/docs/mcp |
| Cherry Studio | https://docs.cherryai.com.cn/docs/en-us/advanced-basic/agent-workspace/tools-knowledge-skills-mcp |
| DSH | https://www.deepseek.com/harness/en/ |

**各家路径速查**（skill 目录、配置文件位置、工具命名）：见本仓库 `AGENTS.md` 第七节——那里按 harness 列了路径表与官方文档链接。

## 一、开发 MCP 服务器

### 先选传输方式

| 传输 | 何时用 | 配置形态 |
|---|---|---|
| **stdio** | 本机进程，最常用（本地工具、文件系统、CLI 包装） | `command` + `args` + `env` |
| **Streamable HTTP** | 远端服务、多客户端共享、需要鉴权 | `url` + `headers` |
| **SSE** | 仅当客户端只支持 SSE（多数新客户端已支持 Streamable HTTP） | `url`（需代理时另配） |

**默认选 stdio**；只有确实要跨机器共享或集中鉴权时才上 HTTP。SSE 属兼容选项，不作为首选。

### 关键设计规则

- **工具粒度按意图分，不按 API 端点分**：一个工具做一件完整的事，别把 `GET` / `POST` 拆成两个工具
- **描述是给模型看的**：写清「什么时候用」与「不要什么时候用」，比写实现细节重要
- **schema 用 SDK 的类型系统生成**，手写 JSON Schema 容易与实现漂移
- **只读与写操作分开命名**，让客户端能做权限分级（Hermes 的 `trust: untrusted` 就依赖 `readOnlyHint`）
- **返回结构化结果**，不要返回人类排版过的长字符串——模型要的是数据
- **错误要可诊断**：报错说明缺什么、怎么补，不要只说 failed
- **不要在一次调用里做长时间阻塞**；长任务拆成「启动 + 查询状态」

### 最小骨架

TypeScript（官方 SDK）：

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.tool("lookup_thing", "查询某物的当前状态。只读。", { id: z.string() },
  async ({ id }) => ({ content: [{ type: "text", text: JSON.stringify(await lookup(id)) }] }));

await server.connect(new StdioServerTransport());
```

Python（官方 SDK）：结构与上面一致，用 `FastMCP` 或低层 `Server`；具体 API 以 https://github.com/modelcontextprotocol/python-sdk 的正文为准，不要照抄本段。

**写完后必须实测**：起服务器 → 用客户端连上 → 调用一次 → 确认返回。未实测不许声称可用。

## 二、导入到客户端

### 通用流程

1. **确认客户端支持哪种传输**（查上表对应文档）
2. **找到该客户端的配置文件**（`AGENTS.md` 第七节有全表；**先探本机实际路径**，别硬写）
3. **写入配置**：本地进程写 `command` / `args` / `env`；远端写 `url` / `headers`
4. **密钥走环境变量引用**，不写进配置文件明文——Claude 用 `${VAR}`，Hermes 用 `${VAR}` / `${env:VAR}`，OpenCode 用 `{env:VAR}`
5. **重启或重载**（Hermes 是 `/reload-mcp`；QwenPaw 每 2 秒自动热重载）
6. **验证工具真的出现在会话里**，再动手调用

### 工具命名

多数客户端把 MCP 工具暴露为 `mcp__<server>__<tool>`；连字符等非标识符字符会被替换成下划线（`my-api` → `mcp__my_api__tool`）。写过滤规则时用**原始工具名**，不是替换后的名字。

### 常见失败

| 症状 | 先查 |
|---|---|
| 工具不出现 | 服务器是否启动成功？客户端是否重载？server 名是否与配置一致？ |
| 连接超时 | stdio：命令路径对不对、能否手动跑起来；HTTP：网络与鉴权头 |
| 鉴权失败 | 密钥是否真的注入（环境变量没设时占位符会原样保留，不一定报错） |
| 工具被过滤掉 | `include` / `exclude` 优先级；名字用的是原始名还是替换后名字 |
| Windows 上启动失败 | 路径分隔符、`.cmd` / `.bat` 包装、`cwd` 设置 |

## 三、维护既有 MCP

- **改工具签名 = 破坏性变更**：客户端缓存工具列表，改完要通知使用者重载
- **版本化**：server 名里不夹版本，版本走包版本号
- **供应链安全**（这一条是红线）：接入**第三方 MCP 服务器**前，先审源码、权限、网络行为，再让用户明确确认注册。第三方服务器能读本机文件、发网络请求、执行命令
- **最小权限**：能用 `include` 白名单就不要全量开放；能标只读就标
- **日志不落密钥**：调试输出里不打印 token 与凭据

## 与相邻 skill 的分工

| 场景 | 走哪 |
|---|---|
| 调用**已配好**的 MCP 工具 | 直接调，不用本 skill |
| 把 MCP 服务器**打包成插件** | `luzzycode-skills`（打包）+ 本 skill（服务器本身） |
| 逆向一个第三方 MCP 服务器的实现 | `luzzycode-reverse` |
| 只是想知道某客户端的 skill 装在哪 | `AGENTS.md` 第七节 |

## 示例

Input: 「帮我写个 MCP 服务器，能查本机磁盘占用」
Output: 读官方 SDK 文档与规范 → 选 stdio（本机工具）→ 用官方 SDK 起骨架 → 工具粒度定为「查询指定路径占用」（只读）→ 本地实测：起服务、连上、调用 → 写客户端配置（密钥不硬编）→ 验证工具出现在会话里

Input: 「把这个 MCP 配到 Codex 里」
Output: 查 Codex 官方配置文档 → 定位 `~/.codex/config.toml` 的 `mcp_servers`（先探本机确认路径存在）→ 写入 command/args/env（密钥用环境变量引用）→ 重启 Codex → 确认 `mcp__<server>__<tool>` 可见

Input: 「网上找了个 MCP，帮我装上」
Output: **先审后装**——读源码、看权限与网络行为 → 向用户说明它要什么权限 → 拿到明确确认 → 配最小权限（白名单）→ 再注册

## Verify

- 动手前：官方 SDK 文档与规范读了吗？（只看 README 摘要不算）
- 传输方式选对了吗？本地工具是不是无理由用了 HTTP？
- 服务器**实测**过吗——起得来、连得上、调得通？
- 配置写进的是该客户端的**真实路径**吗？（先探本机再写）
- 密钥走环境变量引用了吗？有没有写进配置文件明文？
- 第三方服务器：审源码了吗？用户明确确认了吗？权限收到最小了吗？
- 工具名用了**原始名**写过滤规则吗？
