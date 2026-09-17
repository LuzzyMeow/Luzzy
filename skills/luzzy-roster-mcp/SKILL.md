---
name: luzzy-roster-mcp
description: >
  Use when the Luzzy checklist (必读清单) hits the MCP 开发 / 接入 / 维护 category —
  reading sub-items for MCP server development, client integration and maintenance; six entries, take four.
  Answers "MCP类目的6条里取哪4条" "写MCP服务器先读什么" "MCP的SDK文档是哪些" "排查MCP工具不出现".
  Do NOT use for executing the task itself — discipline and red lines live in the Luzzy
  system prompt — nor for the reading gate, receipt, or triage logic, nor for other
  checklist categories or tasks unrelated to this one.
license: MIT
metadata:
  version: "1.0.0"
  author: "鹿溪 (LuzzyMeow)"
  category: "luzzy-roster"
  maturity: "L2"
---

# MCP 开发 / 接入 / 维护 · 仓库子项明细

提示词 §1.1.6 命中「MCP 开发 / 接入 / 维护」后，读本文件拿仓库子项明细与执行细则。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（6 条 → 取 4 条）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | `https://modelcontextprotocol.io/docs/2026-07-28/sdk` | 正文——规范与 SDK 选型 |
| 2 | `https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers` | 正文——连接本地服务器 |
| 3 | **TypeScript SDK** `https://github.com/modelcontextprotocol/typescript-sdk` | 正文 |
| 4 | **Python SDK** `https://github.com/modelcontextprotocol/python-sdk` | 正文 |
| 5 | **参考服务器集合** `https://github.com/modelcontextprotocol/servers` | 正文 |
| 6 | **协议仓库** `https://github.com/modelcontextprotocol/modelcontextprotocol` | 正文 |

协议与会话生命周期变化快，凭记忆写必错——先读官方来源再动手。开发设计规则与供应链安全红线见提示词 §14.13；传输选型、客户端配置与常见失败见下方执行细则。

## 执行细则（提示词 §14.13 的操作明细）

**传输选型**：

| 传输 | 何时用 | 配置形态 |
|---|---|---|
| **stdio** | 本机进程，最常用（本地工具、文件系统、CLI 包装） | `command` + `args` + `env` |
| **Streamable HTTP** | 远端服务、多客户端共享、需要鉴权 | `url` + `headers` |
| **SSE** | 仅当客户端只支持 SSE（多数新客户端已支持 Streamable HTTP） | `url`（需代理时另配） |

**默认选 stdio**；只有确实要跨机器共享或集中鉴权时才上 HTTP。SSE 属兼容选项，不作首选。

**导入到客户端**：

1. 确认客户端支持哪种传输
2. 找到该客户端的配置文件（**先探本机实际路径**，别硬写——位置随版本变动）
3. 写入配置：本地进程写 `command` / `args` / `env`；远端写 `url` / `headers`
4. **密钥走环境变量引用**，不写配置文件明文（Claude `${VAR}`、Hermes `${VAR}` / `${env:VAR}`、OpenCode `{env:VAR}`）
5. 重启或重载（Hermes 是 `/reload-mcp`；QwenPaw 每 2 秒自动热重载）
6. **验证工具真的出现在会话里**，再动手调用

**工具命名**：多数客户端暴露为 `mcp__<server>__<tool>`；连字符等非标识符字符会被替换成下划线（`my-api` → `mcp__my_api__tool`）。写过滤规则时用**原始工具名**，不是替换后的名字。

**常见失败**：工具不出现 → 服务器是否启动成功？客户端是否重载？server 名是否与配置一致？｜连接超时 → stdio 查命令路径能否手动跑起来，HTTP 查网络与鉴权头｜鉴权失败 → 密钥是否真的注入（环境变量没设时占位符会原样保留，不一定报错）｜工具被过滤 → `include` / `exclude` 优先级、用的是原始名还是替换后名字｜Windows 启动失败 → 路径分隔符、`.cmd` / `.bat` 包装、`cwd`。

## Examples

Input: 命中「MCP 开发」
Output: 6 条取 4（协议文档 + 对应语言 SDK 优先）→ 落回执 → 按 §14.13 实测后再声称可用。

Input: 给客户端接入 MCP
Output: 读完 4 条 → 密钥走环境变量引用 → 验证工具真的出现在会话里再调用。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

纪律、红线与验收标准见提示词 §14.13；本 skill 装清单明细与操作性执行细则。
