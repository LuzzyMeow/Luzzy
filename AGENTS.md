# LuzzyCode 维护指南

面向维护本仓库的 Agent。仓库身份、分层设计与规则正文见 `README.md` 与 `prompt/LuzzyCode.md`；本文件只讲**怎么改、改哪里、什么不许动**，以及接入各家 harness 时要用的路径。

---

## 一、仓库是什么

LuzzyCode 给编码 Agent 用的一套行为契约，分两层：

| 层 | 位置 | 进上下文时机 |
|---|---|---|
| 常驻层 | `prompt/LuzzyCode.md` | 每次请求 |
| skill 层 | `skills/<name>/SKILL.md` | 命中场景按需加载 |

**权威来源**：`https://github.com/LuzzyMeow/LuzzyCode`（本仓库）。

## 二、目录与文件

```
LuzzyCode/
├── prompt/LuzzyCode.md        常驻提示词（注入为 system prompt）
├── skills/
│   ├── luzzycode/             编排器：路由表 + 冲突裁决
│   └── luzzycode-*/           各子 skill，每个目录一个 SKILL.md
├── scripts/check-skills.py    质量门禁（纯标准库）
├── AGENTS.md                  本文件
└── README.md                  门面文档
```

**没有** `package.json` / `pyproject.toml` 之类的清单文件——本仓库不是软件项目，是提示词与 skill 的文本仓库。唯一的可执行件是 `scripts/check-skills.py`。

## 三、改动流程

1. 读 `README.md` 与 `prompt/LuzzyCode.md`，确认要动的是哪一层
2. 判断归属：**每轮都要生效的硬规定留常驻层**，细则下沉为 skill（硬规定下沉会形成「要读 skill 才知道要读 skill」的循环依赖）
3. 改 skill → 先读 `skills/luzzycode-skills/SKILL.md` 与它引用的 Luzzy-Skill Architect
4. 跑门禁：`python scripts/check-skills.py`（退出码 0 才算过）
5. 推送走 SSH：`git remote -v` 两行都应是 `git@github.com:` 开头

### 增删 skill 时同步四处

| 处 | 改什么 |
|---|---|
| `skills/` | 新建 / 删除目录与 `SKILL.md` |
| `skills/luzzycode/SKILL.md` | 路由表加行；正文里的子 skill 计数 |
| `prompt/LuzzyCode.md` | §1.1 必读表（若涉及）；§12 计数；§12.1 名字清单 |
| `README.md` | 结构树、skill 计数、徽章、提示词预算表的实测数字 |

`scripts/check-skills.py` 会检查计数一致性（提示词查阿拉伯数字、编排器查中文数字）与路由表覆盖率，漏改会被它抓出来。

## 四、门禁查什么

```bash
python scripts/check-skills.py            # 失败返回 1
python scripts/check-skills.py --verbose  # 逐项打印
```

单 skill：`name` 与目录名一致且 kebab-case、`description` 含负面触发词且不泄漏步骤、正文 ≤500 行且无第二人称、至少 2 组 Input→Output、有 `Verify` 段、无 emoji 与装饰分隔线。
仓库级：计数与目录一致、提示词引用的 skill 名都存在、编排器路由表覆盖全部子 skill、抓取链接模板仍指向本仓库。

**门禁写了就必须能跑**——纯文字清单会静默失效，这个仓库已经吃过一次亏。

## 五、README 里的数字必须实测

token 数用 `tiktoken` 的 `o200k_base` 实测，不估算。口径：

| 项 | 算法 |
|---|---|
| 常驻行数/token | 整个 `prompt/LuzzyCode.md` |
| 按需行数 | 删掉 frontmatter 但保留其后换行，再数行 |
| 按需 token | 只算正文（去掉 frontmatter） |
| frontmatter | 单独计，属**常驻**开销（每轮都在上下文里） |

改了提示词或 skill 就要重测并更新 README 的预算表与徽章。

## 六、绝对不许做

- 硬编码密钥、令牌、账号
- `git push --force`
- 改测试或门禁来让检查通过
- 把硬规定从常驻层下沉为 skill
- 在仓库里散落无主的临时文件——本轮产物本轮清
- 未经要求新建成品文档

---

## 七、接入 harness：路径速查

要把 LuzzyCode 的 skill 装到某个 Agent、或找它的 MCP 配置时，按下表定位。**先探本机是否真有该目录，再动手**；下表路径以各项目官方文档为准，但版本会变，用前建议复核一次。

**官方文档链接固化在此**，供后续维护或使用提示词的 Agent 直接阅读——不用再搜一遍。

### ZCode（Z.ai）

**官方文档**：
- 插件市场与插件体系说明 —— https://zcode.z.ai/docs（ZCode 官方文档）
- 插件内 MCP 声明格式见本机插件缓存里的 `.mcp.json` 与 `.zcode-plugin/plugin.json`

| 项 | 路径 |
|---|---|
| skill 目录 | `~/.zcode/skills/`、项目内 `.zcode/` |
| 插件缓存 | `~/.zcode/cli/plugins/cache/<来源>/<插件名>/<版本>/` |
| 配置 | `~/.zcode/cli/config.json`（`plugins.enabledPlugins` 与 `plugins.options`） |
| MCP | 插件自带 `.mcp.json`；官方插件由 ZCode 插件宿主拉起（命令被改写成 `ZCode.exe … __zcode-plugin-host`），**第三方插件不被自动改写** |
| 工具命名 | 模型侧 `mcp__<server>__<tool>`（连字符转下划线） |

ZCode 插件可同时打包 skills、commands、MCP server。官方插件源为 `zcode-plugins-official`。典型范例：`android-emulator` 插件的 `README.md` 写明了 SEA 构建改写 manifest 的机制。

### DSH（DeepSeek Harness）

**官方文档**：
- 项目主页与开发者预览 —— https://www.deepseek.com/harness/en/
- 官方 skill 与文档规范示例 —— https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-doc/SKILL.md
- 插件体系说明 —— https://github.com/deepseek-ai/deepseek-harness

| 项 | 路径 |
|---|---|
| skill 目录 | `~/.agents/skills/`（发现根，启动时扫描）；仓库内 `.agents/skills/` |
| 插件安装 | `dsh plugin --profile <名> add <包>` |
| 插件形态 | bundle（`package.json` 声明 `dsh.bundle.patch`）／plugin（`cordis.yml` 挂载）／library（仅依赖，无安装路径） |
| 文档规范 | 仓库 `AGENTS.md` + `docs/AGENTS.md` |

**装之前先分辨包形态**：读 `package.json` 与入口文件，别按文件夹名字猜。给 library 写「安装指引」是常见错误。

### Claude Code

**官方文档**：
- Skills 指南 —— https://code.claude.com/docs/en/skills
- MCP 接入（本地 stdio / 远端 HTTP / SSE 三种） —— https://code.claude.com/docs/en/claude_code_docs_map
- 插件与 MCP 集成 skill 范例 —— https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/mcp-integration/SKILL.md

| 项 | 路径 |
|---|---|
| skill 目录 | `~/.claude/skills/`（用户级）、`<项目>/.claude/skills/` |
| MCP | 全局 `~/.claude.json`；项目级 `.mcp.json` |
| 插件 | `.claude-plugin/plugin.json` |

`--add-dir` / `/add-dir` 加入的目录，其 `.claude/skills/` 与 `.claude/commands/` 会被一并加载。

### Codex CLI

**官方文档**：
- AGENTS.md 自定义指令 —— https://learn.chatgpt.com/docs/agent-configuration/agents-md
- 配置参考（`config.toml`、`mcp_servers`） —— https://learn.chatgpt.com/docs/config-file/config-reference
- AGENTS.md 开放格式说明 —— https://agents.md/

| 项 | 路径 |
|---|---|
| 指令文件 | 仓库根 `AGENTS.md`（逐级向下读；存在 `AGENTS.override.md` 时优先读它）；全局 `~/.codex/AGENTS.md` |
| MCP | `~/.codex/config.toml` 的 `mcp_servers` |
| skill | 以**目录**为单位同步，不是散文件 |

Codex 在动手前读 `AGENTS.md`——所以本仓库的维护约束对它直接生效。

### OpenClaw

**官方文档**：
- Skills 配置参考 —— https://docs.openclaw.ai/tools/skills-config
- Skills 概念与加载顺序 —— https://docs.openclaw.ai/tools/skills
- 创建自定义 skill —— https://docs.openclaw.ai/tools/creating-skills

| 项 | 路径 |
|---|---|
| skill 配置 | `~/.openclaw/openclaw.json` 的 `skills` |
| 受管 skill 目录 | `~/.openclaw/skills` |
| 个人 skill 目录 | `~/.agents/skills` |
| 项目级 | `<workspace>/skills`、`<workspace>/.agents/skills` |
| 额外扫描目录 | `skills.load.extraDirs`（优先级最低） |
| MCP 客户端注册表 | `~/.openclaw/skills/config/mcporter.json` |
| 安装策略 | `skills.install`；操作员审批 `security.installPolicy` |

注意：`agents.entries.*.skills` 的显式列表**替换**默认值而非合并；写成 `[]` 等于该 agent 看不到任何 skill。

### Hermes Agent（Nous Research）

**官方文档**：
- MCP 配置参考（完整键位、过滤、OAuth） —— https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- Skills 系统 —— https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- 官方 skill 范例（含 MCP 构建） —— https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mcp/fastmcp/SKILL.md

| 项 | 路径 |
|---|---|
| skill 目录 | `~/.hermes/skills/`（唯一事实源；首次安装时内置 skill 从仓库拷入） |
| MCP 配置 | `~/.hermes/config.yaml` 的 `mcp_servers:` |
| 密钥 | `~/.hermes/.env`（配置里用 `${VAR}` 或 `${env:VAR}` 引用） |
| OAuth 令牌 | `~/.hermes/mcp-tokens/<server>.json` |
| 重载 | `/reload-mcp` |
| 工具命名 | `mcp__<server>__<tool>`，非字母数字下划线字符会被替换为 `_` |

`trust: untrusted` 会让所有写操作走审批面；`tools.include` 优先于 `tools.exclude`。

### QwenPaw（AgentScope）

**官方文档**：
- 配置与工作目录 —— https://qwenpaw.agentscope.io/docs/config/
- MCP 客户端配置 —— https://qwenpaw.agentscope.io/docs/mcp
- Skills 系统 —— https://qwenpaw.agentscope.io/docs/skills
- 项目仓库 —— https://github.com/agentscope-ai/QwenPaw

| 项 | 路径 |
|---|---|
| 工作目录 | `~/.qwenpaw`（环境变量 `QWENPAW_WORKING_DIR`） |
| 全局配置 | `~/.qwenpaw/config.json` |
| Agent 配置 | `~/.qwenpaw/workspaces/<agent_id>/agent.json`（含 `mcp.clients`、`tools`、`skills`） |
| 共享 skill 池 | `~/.qwenpaw/skill_pool/` |
| 工作区 skill | `~/.qwenpaw/workspaces/<agent_id>/skills/` |
| skill 开关 | `~/.qwenpaw/workspaces/<agent_id>/skill.json` |
| 密钥目录 | `~/.qwenpaw.secret/`（`providers.json`、`envs.json`） |

`agent.json` 优先级高于全局 `config.json`；文件改动每 2 秒自动热重载。

### OpenCode

**官方文档**：
- 配置参考（优先级、`mcp`、`instructions`、变量替换） —— https://opencode.ai/docs/config/
- MCP 服务器配置 —— https://opencode.ai/docs/mcp-servers
- 插件（`.opencode/plugins/` / npm） —— https://opencode.ai/docs/plugins

| 项 | 路径 |
|---|---|
| 全局配置 | `~/.config/opencode/opencode.json` |
| 项目配置 | `<项目>/opencode.json`（优先级高于全局） |
| skill / tools / 主题 | `.opencode/` 目录（agents、commands、plugins 同） |
| MCP | 配置里的 `mcp` 段 |
| 自定义路径 | 环境变量 `OPENCODE_CONFIG`（配置文件）、`OPENCODE_CONFIG_DIR`（目录） |
| 管理端强制配置 | Linux `/etc/opencode/`、macOS `/Library/Application Support/opencode/`、Windows `%ProgramData%\opencode` |

优先级（低到高）：远端 `.well-known/opencode` → 全局 → 自定义 → 项目 → `.opencode/` → 内联 → 管理端。同名键后者覆盖前者。

### Cherry Studio

**官方文档**：
- 内置工具、知识库、技能与 MCP —— https://docs.cherryai.com.cn/docs/en-us/advanced-basic/agent-workspace/tools-knowledge-skills-mcp
- 项目仓库 —— https://github.com/CherryHQ/cherry-studio

| 项 | 路径 |
|---|---|
| MCP 配置 | 图形界面「设置 → MCP 服务器」（也支持直接改 `config.json`） |
| 已安装 MCP 落点 | 用户目录下的 `.cherrystudio/`（Windows 典型为 `C:\Users\<用户>\.cherrystudio\`） |
| skill | 以 Agent 工作区的「技能」形式配置（内置工具、知识库、技能、MCP 同区） |

**Cherry Studio 是图形界面的桌面应用**：MCP 依赖模型的函数调用能力，且需要先在设置里连接并启动服务器，再回到 Agent 编辑窗口绑定。它是 GUI 优先，路径随版本变动较多，**以界面实际显示为准**。

---

## 八、给其他 Agent 的提示

- 本仓库的规则**以 `prompt/LuzzyCode.md` 为准**；本文件是维护说明，不替代它
- 要装 skill 到某台机器时：先确认该 harness 的真实 skill 目录（上表 + 本机勘探），再拷；**不要凭表硬写路径**
- 上表路径来自各项目官方文档（2026-09 核对）。harness 迭代快，路径可能变——发现不符就报告并更新本文件
- 改动本仓库前先跑一次门禁，拿到基线；改完再跑，对比差异
