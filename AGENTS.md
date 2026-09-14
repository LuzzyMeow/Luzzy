# LuzzyCode 维护指南

面向维护本仓库的 Agent。仓库身份与规则正文见 `README.md` 与 `prompt/LuzzyCode.md`；本文件只讲**怎么改、改哪里、什么不许动**，以及接入各家 harness 时要用的路径。

---

## 一、仓库是什么

LuzzyCode 给编码 Agent 用的一套行为契约，**全部装在一个文件里**：`prompt/LuzzyCode.md`。

早先版本是「常驻提示词 + 22 个按需加载的 skill」，但 §1.1 的必读清单与各 skill 正文里的清单是同一份数据的两个副本（实测 14 个 skill 重复了提示词里的链接），两处并存必然漂移。现已改为单一文件，清单只有一个事实源。

**权威来源**：`https://github.com/LuzzyMeow/LuzzyCode`（本仓库）。

## 二、目录与文件

```
LuzzyCode/
├── prompt/LuzzyCode.md        全部规则（唯一载体，注入为 system prompt）
├── AGENTS.md                  本文件
├── README.md                  门面文档
├── LICENSE
└── .gitattributes
```

**没有** `package.json` / `pyproject.toml` 之类的清单文件，也**没有构建与门禁脚本**——本仓库不是软件项目，是一份提示词文本。所有校验靠人工核对（第四节）。

## 三、改动流程

1. 读 `README.md` 与 `prompt/LuzzyCode.md`，确认要动的是哪一节
2. 改 `prompt/LuzzyCode.md`
3. 按第四节的清单人工核对（尤其 `§` 交叉引用与数字）
4. 按实测更新 `README.md` 的「提示词预算」表与徽章数字（口径见第五节）
5. 推送走 SSH：`git remote -v` 两行都应是 `git@github.com:` 开头

改完最容易出的两类错是**交叉引用悬空**（改了章节编号没改引用）与 **README 数字漂移**（改了提示词没重测）——第四节给了对应的核对方法。

**改动时要守的一条**：规则只有一个事实源。如果某条规则在文件里出现两次，删掉一份，改成引用（`见 §N`）——这正是本次重构要解决的问题。

## 四、改完怎么核对

没有自动门禁，改完按这张表人工过一遍。每项都给了「怎么快速验」：

| 类别 | 核对什么 | 怎么验 |
|---|---|---|
| 结构 | 十七个章节标题齐全（〇 至 十四、附录 A/B） | 搜 `^# ` 列出所有一级标题对一遍 |
| 清单 | §1.1 的十四类齐全，条数与「条数 / 执行要点」列对得上 | 数一遍表格行，与列里写的数字核对 |
| 规则语义 | 「全读 / 超过 4 条取 4」「读 ≠ 装 ≠ 用」「唯一载体」三条在位 | 搜关键词 |
| **交叉引用** | 文中所有 `§N.N` 都能找到对应小节 | 把所有 `§` 引用抄出来，逐个跳过去看；**改章节编号时最容易漏** |
| 残留 | 无指向旧机制的写法（`luzzycode-*`、`skills/`、skill 加载、`§1.1a`） | 搜这些关键词，应无命中 |
| 格式 | 无装饰性 emoji（✅ ⚠ 🚫 三档标记、✗ ✓ 正反例标记豁免）、无裸露分隔线 | 目视 + 搜 `^---$` |
| 安全 | 无硬编码密钥形态 | 搜 `sk-` / `ghp_` / `Bearer` |
| **数字** | README 的行数、token、徽章等于实测值 | 第五节命令重测，**每次必做** |

**代价要认**：早先的门禁是纯文字清单，从没被执行过，于是 22 个 skill 全部违反其中的「无装饰性格式」而无人发现。现在回到人工核对，风险最高的是**数字漂移**——所以第五节把它列为每次必做，其余各项靠交付前过一遍。

## 五、README 里的数字必须实测

token 数用 `tiktoken` 的 `o200k_base` 实测，不估算：

```bash
python -c "import tiktoken,pathlib; t=pathlib.Path('prompt/LuzzyCode.md').read_text(encoding='utf-8'); e=tiktoken.get_encoding('o200k_base'); n=len(e.encode(t)); print(len(t.splitlines()),'行', n,'token'); print('徽章', f'{n/1000:.1f}k')"
```

| 项 | 算法 |
|---|---|
| 行数 | `len(prompt.splitlines())` |
| token | `len(tiktoken.get_encoding("o200k_base").encode(prompt))` |
| 徽章 | `f"{token/1000:.1f}k"` |

改了提示词就要重测并更新 README 的预算表与徽章。这是**唯一无法靠肉眼发现**的漂移项，务必每次都做。

`AGENTS.md` 自身的体量不进预算（它不必注入 system prompt）。

## 六、绝对不许做

- 硬编码密钥、令牌、账号
- `git push --force`
- 改自检脚本或 README 来让检查通过
- 把规则写成两份（同一条规则在两个地方各写一遍）
- 在仓库里散落无主的临时文件——本轮产物本轮清
- 未经要求新建成品文档

---

## 七、接入 harness：路径速查

要把本提示词用到某个 Agent、或找它的 MCP 配置时，按下表定位。**先探本机是否真有该目录，再动手**；下表路径以各项目官方文档为准，但版本会变，用前建议复核一次。

**官方文档链接固化在此**，供后续维护或使用的 Agent 直接阅读——不用再搜一遍。

### ZCode（Z.ai）

**官方文档**：插件市场与插件体系 —— https://zcode.z.ai/docs ；插件内 MCP 声明格式见本机插件缓存里的 `.mcp.json` 与 `.zcode-plugin/plugin.json`

| 项 | 路径 |
|---|---|
| 提示词注入 | 作为 system prompt / 项目指令加载；ZCode 无强制的 skill 目录要求 |
| 插件缓存 | `~/.zcode/cli/plugins/cache/<来源>/<插件名>/<版本>/` |
| 配置 | `~/.zcode/cli/config.json`（`plugins.enabledPlugins` 与 `plugins.options`） |
| MCP | 插件自带 `.mcp.json`；官方插件由 ZCode 插件宿主拉起（命令被改写成 `ZCode.exe … __zcode-plugin-host`），**第三方插件不被自动改写** |
| 工具命名 | 模型侧 `mcp__<server>__<tool>`（连字符转下划线） |

ZCode 插件可同时打包 skills、commands、MCP server。官方插件源为 `zcode-plugins-official`。典型范例：`android-emulator` 插件的 `README.md` 写明了 SEA 构建改写 manifest 的机制。

### DSH（DeepSeek Harness）

**官方文档**：项目主页 —— https://www.deepseek.com/harness/en/ ；官方 skill 与文档规范示例 —— https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-doc/SKILL.md

| 项 | 路径 |
|---|---|
| 指令文件 | 仓库根 `AGENTS.md`；skill 目录 `~/.agents/skills/` 与仓库内 `.agents/skills/` |
| 插件安装 | `dsh plugin --profile <名> add <包>` |
| 插件形态 | bundle（`package.json` 声明 `dsh.bundle.patch`）／plugin（`cordis.yml` 挂载）／library（仅依赖，无安装路径） |

**装之前先分辨包形态**：读 `package.json` 与入口文件，别按文件夹名字猜。

**本机预设的部署链路（同步本提示词到 DSH 时的实测经验）**

DSH 的 agent 预设放在 `~/.dsh/.agent-presets/<预设名>/`（本仓库对应 `luzzycode`）。提示词不是直接读文件，而是被**机械嵌入** YAML：

```
persona.md  --(node sync-persona.mjs)-->  agent.cordis.yml 的 config.prefix: |- 块
   ↑ 唯一真源，与 prompt/LuzzyCode.md 逐字节一致         ↑ 6 空格缩进，禁止手工编辑
```

同步流程（四条，缺一不可）：

1. **先备份 `persona.md`**（同步脚本只备份 YAML，不备份 persona 正本），命名沿用 `persona.md.bak-<原因>-<时间戳>`
2. **覆盖 `persona.md`**，内容与仓库 `prompt/LuzzyCode.md` **逐字节一致**
3. `cd ~/.dsh/.agent-presets/luzzycode && node sync-persona.mjs`
4. **复核**：脚本会自行解析回验 + 逐字节比对 + 顶层条目数校验，任一不过自动回滚；稳妥起见再独立跑一次解析比对

**四条硬约束（踩过坑，别复发）**：

| 约束 | 原因 |
|---|---|
| **行尾必须 LF** | 从仓库复制来的文件在工作区可能是 CRLF（本仓库已实测发生过）。CRLF 会让回验在第 1 行就失败：`YAML 侧 "…" / 源文件 "…\r"`。复制后先规整 `\r\n` → `\n`，**不要指望 `.gitattributes` 在 checkout 时自动转换** |
| **字段名必须是 `prefix`** | DSH 2.0.9+ 的 persona schema 要求必填 `prefix`；用旧的 `text` 会导致 preset 组装无限失败重试（host 日志刷 `ValidationError: $.prefix missing required value`） |
| **禁止手改 YAML 标量** | 生成块由脚本产出并回验；手改会让下一次同步产生巨大且无法比对的 diff |
| **顶层条目数不能变** | 脚本会校验（本机为 17 条），变了说明误伤了块外结构 |

**验证命令**（脚本之外独立复核一遍，确认解析出的文本与源文件一致）：

```bash
cd ~/.dsh/.agent-presets/luzzycode && node -e "
const fs=require('fs'), yaml=require('/Users/<你>/.dsh/profiles/desktop/node_modules/js-yaml');
const T=new yaml.Type('tag:yaml.org,2002:js',{kind:'scalar',construct:d=>d,resolve:()=>true});
const p=yaml.load(fs.readFileSync('agent.cordis.yml','utf8'),{schema:yaml.DEFAULT_SCHEMA.extend([T])}).find(e=>e.id==='persona');
const src=fs.readFileSync('persona.md','utf8').replace(/\n+$/,'');
console.log('逐字节一致:', p.config.prefix.replace(/\n$/,'')===src);
"
```

- **生效时机**：改动只对**新会话**生效；进行中的会话上下文里仍是旧文本
- **登记惯例**：每次改动在 `persona.changes.md` 追加一条（日期 + 性质 + 踩坑 + 校验结果 + 回滚命令），`preset.yml` 的 `description` 也要跟着改——它是预设列表里显示的说明，最容易被忘
- **回滚**：恢复 `persona.md.bak-*` 与 `agent.cordis.yml.bak-sync-*` 两个文件即可

**本机 skill 目录已清空（2026-09-14）**：`~/.dsh/skills/` 下 19 个 `luzzycode-*` 目录已删除——它们是 `b1833cc` 时代手工拷进去的（18 个子 skill + 编排器），会让 DSH 继续扫描并暴露给模型，与本提示词「不再有配套 skill」的口径冲突。

删除前核对过三件事：该目录下**只有** `luzzycode-*`（无其他 skill）；`~/.dsh/settings.yaml` 只是把 `luzzycode` 设为**默认预设名**，不引用 skills；另一个预设 `liangshen` 无任何引用。目录本身保留（空）。

**恢复来源**：本仓库 git 历史 `0a474c2`（`git show 0a474c2:skills/<名>/SKILL.md`）——那里有全部 **23** 项，比本机部署的 19 项还多（含 reverse / assets / android / mcp）。今后若再装回，记住它会被 DSH 扫描并向模型暴露，与单一提示词口径冲突。

### Claude Code

**官方文档**：Skills —— https://code.claude.com/docs/en/skills ；MCP 接入（本地 stdio / 远端 HTTP / SSE） —— https://code.claude.com/docs/en/claude_code_docs_map ；插件内 MCP 集成范例 —— https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/mcp-integration/SKILL.md

| 项 | 路径 |
|---|---|
| 指令文件 | 项目根 `CLAUDE.md`（本仓库的 `AGENTS.md` 亦可读） |
| MCP | 全局 `~/.claude.json`；项目级 `.mcp.json` |
| skill 目录 | `~/.claude/skills/`、`<项目>/.claude/skills/`（若你另有 skill） |

### Codex CLI

**官方文档**：AGENTS.md 自定义指令 —— https://learn.chatgpt.com/docs/agent-configuration/agents-md ；配置参考（`config.toml`、`mcp_servers`） —— https://learn.chatgpt.com/docs/config-file/config-reference ；开放格式说明 —— https://agents.md/

| 项 | 路径 |
|---|---|
| 指令文件 | 仓库根 `AGENTS.md`（逐级向下读；存在 `AGENTS.override.md` 时优先读它）；全局 `~/.codex/AGENTS.md` |
| MCP | `~/.codex/config.toml` 的 `mcp_servers` |

Codex 在动手前读 `AGENTS.md`——所以本文件的维护约束对它直接生效。

### OpenClaw

**官方文档**：Skills 配置参考 —— https://docs.openclaw.ai/tools/skills-config ；Skills 概念与加载顺序 —— https://docs.openclaw.ai/tools/skills ；创建自定义 skill —— https://docs.openclaw.ai/tools/creating-skills

| 项 | 路径 |
|---|---|
| 指令文件 | `~/.openclaw/openclaw.json`；项目级 `<workspace>/` |
| skill 目录 | `~/.openclaw/skills`、`~/.agents/skills`、`<workspace>/skills`、`<workspace>/.agents/skills` |
| 额外扫描目录 | `skills.load.extraDirs`（优先级最低） |
| MCP 客户端注册表 | `~/.openclaw/skills/config/mcporter.json` |
| 安装策略 | `skills.install`；操作员审批 `security.installPolicy` |

注意：`agents.entries.*.skills` 的显式列表**替换**默认值而非合并；写成 `[]` 等于该 agent 看不到任何 skill。

### Hermes Agent（Nous Research）

**官方文档**：MCP 配置参考（键位、过滤、OAuth） —— https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference ；Skills 系统 —— https://hermes-agent.nousresearch.com/docs/user-guide/features/skills ；官方 skill 范例 —— https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mcp/fastmcp/SKILL.md

| 项 | 路径 |
|---|---|
| 指令文件 | 项目 `AGENTS.md`；skill 目录 `~/.hermes/skills/`（唯一事实源） |
| MCP 配置 | `~/.hermes/config.yaml` 的 `mcp_servers:` |
| 密钥 | `~/.hermes/.env`（配置里用 `${VAR}` 或 `${env:VAR}` 引用） |
| OAuth 令牌 | `~/.hermes/mcp-tokens/<server>.json` |
| 重载 | `/reload-mcp` |
| 工具命名 | `mcp__<server>__<tool>`，非字母数字下划线字符会被替换为 `_` |

`trust: untrusted` 会让所有写操作走审批面；`tools.include` 优先于 `tools.exclude`。

### QwenPaw（AgentScope）

**官方文档**：配置与工作目录 —— https://qwenpaw.agentscope.io/docs/config/ ；MCP 客户端配置 —— https://qwenpaw.agentscope.io/docs/mcp ；项目仓库 —— https://github.com/agentscope-ai/QwenPaw

| 项 | 路径 |
|---|---|
| 工作目录 | `~/.qwenpaw`（环境变量 `QWENPAW_WORKING_DIR`） |
| 全局配置 | `~/.qwenpaw/config.json` |
| Agent 配置 | `~/.qwenpaw/workspaces/<agent_id>/agent.json`（含 `mcp.clients`、`tools`、`skills`） |
| 提示词 / 人设 | 工作区内的 `AGENTS.md`、`SOUL.md`、`PROFILE.md`（由 `system_prompt_files` 控制加载） |
| 密钥目录 | `~/.qwenpaw.secret/`（`providers.json`、`envs.json`） |

`agent.json` 优先级高于全局 `config.json`；文件改动每 2 秒自动热重载。

### OpenCode

**官方文档**：配置参考（优先级、`mcp`、`instructions`、变量替换） —— https://opencode.ai/docs/config/ ；MCP 服务器配置 —— https://opencode.ai/docs/mcp-servers ；插件 —— https://opencode.ai/docs/plugins

| 项 | 路径 |
|---|---|
| 全局配置 | `~/.config/opencode/opencode.json` |
| 项目配置 | `<项目>/opencode.json`（优先级高于全局） |
| 指令文件 | 配置里的 `instructions` 数组（可指向 `AGENTS.md`） |
| MCP | 配置里的 `mcp` 段 |
| 自定义路径 | 环境变量 `OPENCODE_CONFIG`（配置文件）、`OPENCODE_CONFIG_DIR`（目录） |
| 管理端强制配置 | Linux `/etc/opencode/`、macOS `/Library/Application Support/opencode/`、Windows `%ProgramData%\opencode` |

优先级（低到高）：远端 `.well-known/opencode` → 全局 → 自定义 → 项目 → `.opencode/` → 内联 → 管理端。

### Cherry Studio

**官方文档**：内置工具、知识库、技能与 MCP —— https://docs.cherryai.com.cn/docs/en-us/advanced-basic/agent-workspace/tools-knowledge-skills-mcp ；项目仓库 —— https://github.com/CherryHQ/cherry-studio

| 项 | 路径 |
|---|---|
| MCP 配置 | 图形界面「设置 → MCP 服务器」（也支持直接改 `config.json`） |
| 已安装 MCP 落点 | 用户目录下的 `.cherrystudio/`（Windows 典型为 `C:\Users\<用户>\.cherrystudio\`） |
| 提示词 | 以 Agent 工作区的「技能」或系统提示形式配置 |

**Cherry Studio 是图形界面的桌面应用**：MCP 依赖模型的函数调用能力，且需要先在设置里连接并启动服务器，再回到 Agent 编辑窗口绑定。它是 GUI 优先，路径随版本变动较多，**以界面实际显示为准**。

---

## 八、给其他 Agent 的提示

- 本仓库的规则**以 `prompt/LuzzyCode.md` 为准**；本文件是维护说明，不替代它
- 要接入某台机器时：先确认该 harness 的真实配置位置（上表 + 本机勘探），再写；**不要凭表硬写路径**
- 上表路径来自各项目官方文档（2026-09 核对）。harness 迭代快，路径可能变——发现不符就报告并更新本文件
- 改动本仓库前先跑一次自检拿基线；改完再跑，对比差异
