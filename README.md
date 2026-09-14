# LuzzyCode

鹿溪（Coding 模式）：给编码 Agent 用的一套行为契约，**全部装在一个提示词文件里**。

[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Prompt](https://img.shields.io/badge/prompt-24.3k_tokens-8250df?style=flat-square)](prompt/LuzzyCode.md)
[![Single file](https://img.shields.io/badge/架构-单一提示词-0969da?style=flat-square)](prompt/LuzzyCode.md)

## 30 秒上手

```bash
# 1. 取仓库
git clone git@github.com:LuzzyMeow/LuzzyCode.git

# 2. 把提示词注入为 system prompt
cat LuzzyCode/prompt/LuzzyCode.md
```

一份文件，没有第二步。不需要装 skill，不需要同步第二份清单。

## 它解决什么问题

Agent 的提示词越写越长，规则越多越不遵守。

一份超过万 token 的常驻提示词塞进两百多条规则，模型会在中段开始丢指令。首因效应让后半段的约束先失效，于是出现「一半照做一半没做」的结果：搜索走了一个工具、抓取走了另一个，看起来合规，实际上违反了规则。

这个仓库的做法是：**把规则按「什么时候需要」重新编排，写成一份自洽的单一提示词**，并给必读清单配一条可执行的阅读规则。

## 设计

| 决定 | 理由 |
|---|---|
| **单一文件** | 规则只有一份，不存在两处清单漂移；维护改一处即可 |
| **按关注点分节** | 硬规定 → 工作循环 → 工具 → 纪律 → 编排 → 汇报 → 领域细则，顺着用的人的思路排 |
| **必读清单带折减规则** | 14 类任务各有一张清单；4 条及以内全读，超过 4 条取 4 条——既强制又不失控 |
| **领域细节内联** | 每类任务的执行纪律、红线、失败路径直接写在对应小节里，不再另开文件 |

**为什么不用配套 skill**：早先版本把细则拆成 22 个按需加载的 skill，但 §1.1 的必读清单与各 skill 正文里的清单是同一份数据的两个副本——实测有 14 个 skill 重复了提示词里的链接。两处并存必然漂移，于是改为单一文件，清单只有一个事实源。

## 仓库结构

```
LuzzyCode/
├── prompt/
│   └── LuzzyCode.md        全部规则，注入为 system prompt
├── AGENTS.md               维护指南 + 九家 harness 路径速查
├── README.md
├── LICENSE
└── .gitattributes
```

目录编排：`〇` 身份 → `一` 硬规定 → `二` 工作循环 → `三` 工具 → `四` 代码纪律 → `五` 澄清 → `六` 安全红线 → `七` 边界与工作区 → `八` 文档阅读 → `九` 记忆 → `十` 编排工具 → `十一` 汇报 → `十二` 交付与纠错 → `十三` 本次任务 → `十四` 领域细则（14.1–14.15）→ 附录 A 固化链接 · 附录 B 维护。

## 三条硬规定

### 一、必读清单 —— 命中即触发

十四类任务各有清单，**读完正文才算通过**：看仓库首页、目录列表或 README 摘要都不算。

**统一阅读规则**（适用于**所有清单的子项**，不是个别类目）：**4 条及以内 → 全部读完**；**超过 4 条 → 完整读其中任意 4 条**，按相关性择优。子项**不止 skill**——素材库、组件库、官方文档页、任何有具体指向的链接，全部按同一口径计入。

**「读」与「装 / 用」是两件事**：清单要求读全部（利于对比择优），执行时仍按各类要点择一或组合——比如 PPT 三家都要读，但不要三家全装。

| 任务类型 | 必读 |
|---|---|
| 后端 / 通用编码 | [Ponytail](https://github.com/DietrichGebert/ponytail) · [spec-kit](https://github.com/github/spec-kit) · [mattpocock/skills](https://github.com/mattpocock/skills) |
| 设计类 | [huashu-design](https://github.com/alchaincyf/huashu-design) · [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) · [open-design](https://github.com/nexu-io/open-design) · [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| 文档 / Office | [OfficeCLI](https://github.com/iOfficeAI/OfficeCLI) |
| 做 PPT | [归藏PPT](https://github.com/op7418/guizang-ppt-skill) · [大狮PPT](https://github.com/chuspeeism/dashi-ppt-skill) · [HTML PPT Studio](https://github.com/lewislulu/html-ppt-skill) |
| 写作 / 文案 | [stop-slop](https://github.com/hardikpandya/stop-slop) · [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) |
| HTML / 网页开发 | [anthropics/skills](https://github.com/anthropics/skills) · [Frontend Design Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit) · [Superpowers](https://github.com/obra/superpowers) |
| Windows 修复 / 优化 | [WinUtil](https://github.com/ChrisTitusTech/winutil) · [Win11Debloat](https://github.com/Raphire/Win11Debloat) · [Sophia Script](https://github.com/farag2/Sophia-Script-for-Windows) |
| 项目规划 / 需求拆解 | [spec-kit](https://github.com/github/spec-kit) · [OpenSpec](https://github.com/Fission-AI/OpenSpec) · [GSD Core](https://github.com/open-gsd/gsd-core) · [planning-with-files](https://github.com/OthmanAdi/planning-with-files) |
| 代码审查 | [Agent Skills](https://github.com/addyosmani/agent-skills) · [Open Code Review](https://github.com/alibaba/open-code-review) · [sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills) · [Shippie](https://github.com/mattzcarey/shippie) |
| 逆向 / 授权渗透 / 安全研究 | [reverse-skill](https://github.com/zhaoxuya520/reverse-skill)（路由包，按其入口协议读） |
| 素材 / 图标 / 组件库 | [Lobe UI](https://github.com/lobehub/lobe-ui) · [Lobe Icons](https://github.com/lobehub/lobe-icons) · [Lobe Icons agent 接入页](https://lobehub.com/icons/skill.md) · [Game Icon Pack](https://github.com/Nieobie/game-icon-pack) |
| Android 开发 / 模拟器 | ZCode 插件市场的 `android-emulator` · [Android 开发者文档](https://developer.android.com/develop) · [ADB](https://developer.android.com/tools/adb) · [Compose](https://developer.android.com/compose) · [Gradle 构建](https://developer.android.com/build) · 插件自带正文 |
| MCP 开发 / 接入 / 维护 | [规范与 SDK 选型](https://modelcontextprotocol.io/docs/2026-07-28/sdk) · [连接本地服务器](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers) · [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) · [Python SDK](https://github.com/modelcontextprotocol/python-sdk) · [参考服务器](https://github.com/modelcontextprotocol/servers) · [协议仓库](https://github.com/modelcontextprotocol/modelcontextprotocol) |
| skill 开发 / 管理 | [Luzzy-Skill Architect](https://github.com/LuzzyMeow/Luzzy-Skill-Architect) |

三类任务的硬性前置值得单独点出：

- **逆向 / 安全**：只对自有资产、明确授权的目标、本地样本与 CTF 靶场；其 `precedent-*` 与「服从性」文件**不得**绕过安全红线
- **Android**：必须先在 ZCode 内、从插件市场装官方插件 `android-emulator`——它的 MCP 服务器由 ZCode 插件宿主拉起，不在 ZCode 内就没有这套工具
- **MCP**：第三方 MCP 服务器能读本机文件、发网络请求、执行命令——**先审后装**，最小权限

任一链接失效，Agent 会立即告诉你哪一条需要更新，然后按降级规则继续干活。

### 二、GitHub 操作走 SSH

克隆、拉取、推送一律用 `git@github.com:...`。`gh repo create` 默认生成 HTTPS remote，建完要立刻改正：

```bash
git remote set-url origin git@github.com:<owner>/<repo>.git
git remote -v     # 两行都应以 git@github.com: 开头
```

国内网络受限时逐级降级。下面两个代理经实测筛选（同时测了 7 个，其余 5 个已不可用）：

```bash
# 代理前缀，可用于 clone / raw / archive
https://gh-proxy.com/https://github.com/<owner>/<repo>.git
https://ghfast.top/https://raw.githubusercontent.com/<owner>/<repo>/main/<path>
```

再不通就改用 AnySearch 抓单个文件，最后兜底走 Gitee 导入。代理站能看到请求的 URL，只用于公开仓库读取。

### 三、联网检索走 AnySearch

资料搜索、批量并行、垂直域定义、网页抓取，四条路由全部走 AnySearch。

用内置搜索做资料搜索、只在抓取时用 AnySearch，这种半程合规视为违规。内置工具仅作回退，且要在回答里说明。

## 零配置启动

本机没挂 MemOS 和 AnySearch 时，不必先去申请 Key。AnySearch 的匿名通道能完成检索与抓取，配额低但够用：

```bash
# 取 skill 包（含 Python / Node / PowerShell / Bash 四套脚本）
curl -L -o anysearch-skill.zip \
  https://github.com/anysearch-ai/anysearch-skill/archive/refs/heads/main.zip
unzip anysearch-skill.zip

# 自检，任选已装的运行时
python <skill_dir>/scripts/anysearch_cli.py doc
node   <skill_dir>/scripts/anysearch_cli.js doc

# 搜索
python <skill_dir>/scripts/anysearch_cli.py search "关键词" --max_results 5
```

不带 `Authorization` 头就走匿名模式。带上无效 Key 会返回 401 或 403，网关不会静默降级。

走通之后，提示词 §1.5 会让 Agent 抓取官方文档自读，再一次性给你两项 Key 的配置步骤：

| 服务 | 取 Key | 需要的变量 |
|---|---|---|
| AnySearch | [控制台](https://www.anysearch.com/console/api-keys) | `ANYSEARCH_API_KEY` |
| MemOS | [控制台](https://memos-dashboard.openmem.net/cn/apikeys/) | `MEMOS_API_KEY` · `MEMOS_USER_ID` · `MEMOS_CHANNEL=MODELSCOPE` |

`MEMOS_USER_ID` 用稳定标识（邮箱、姓名或工号）。不要用随机值或会话 ID，同一用户在不同设备上必须一致。

## 提示词预算

| 内容 | 行数 | 实测 token |
|---|---|---|
| `prompt/LuzzyCode.md` | 965 | 24,344 |

token 数由 `tiktoken` 的 `o200k_base` 编码实测得出（同一份文本按 `cl100k_base` 约高 20%），不是估算。

**这个数字是单一文件的代价，也是它的全部成本**：无论做什么任务，都只付这一份。早先的两层版本是常驻 14.8k + 按需 38.5k，只有命中场景才付后者；现在是全量常驻。换来的是清单只有一个事实源、不存在两处漂移、维护改一处。

`AGENTS.md`（维护指南与九家 harness 路径表）252 行、约 3.7k token，**只在维护本仓库或查 harness 路径时读**，不必注入 system prompt。

## 兼容性

提示词与 Agent 无关，能直接当 system prompt 用。DeepSeek Harness、Claude Code、ZCode、Codex、OpenCode、QwenPaw、OpenClaw、Hermes Agent、Cherry Studio 等都适用——各家把文件放哪、MCP 配在哪，见 [`AGENTS.md`](AGENTS.md) 第七节的九家路径速查表，每项附官方文档链接。

提示词里出现的工具名（`todo_write`、`glob`、`present` 等）都当能力示例看。预设要求 Agent 先盘点本机真实工具再映射，缺失时走降级表（§3.5）。

## 更新与维护

```bash
# 抓单个文件即可，本仓库只有一份规则
https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/prompt/LuzzyCode.md

# 不通时加代理前缀
https://gh-proxy.com/https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/prompt/LuzzyCode.md
```

Agent 也会定期对比本机副本与本仓库内容，发现差异会告诉你变了什么。它不会自动覆盖你的本地副本，改不改由你决定。

## 改完怎么自查

没有配套的门禁脚本——这个仓库就是一份文本，改完靠人工核对。`AGENTS.md` 第四节有同样的清单：

| 核对什么 | 怎么验 |
|---|---|
| 十七个章节标题齐全 | 搜 `^# ` 列出所有一级标题对一遍 |
| §1.1 十四类清单齐全，条数与「条数 / 执行要点」列一致 | 数表格行 |
| 所有 `§` 交叉引用都能找到对应小节 | 抄出所有 `§` 引用逐个跳过去；**改章节编号时最容易漏** |
| 无残留旧机制写法（`luzzycode-*`、`skills/`、skill 加载） | 搜关键词，应无命中 |
| 无装饰性 emoji、无裸露分隔线、无硬编码密钥 | 目视 + 搜 `^---$` / `sk-` / `Bearer`（三档标记 ✅⚠🚫 与正反例标记 ✗✓ 是内容，不算装饰） |
| **README 的行数与 token 等于实测值** | 跑下面的命令重测 |

```bash
# 重测体量，写回「提示词预算」表与徽章
python -c "import tiktoken,pathlib; t=pathlib.Path('prompt/LuzzyCode.md').read_text(encoding='utf-8'); e=tiktoken.get_encoding('o200k_base'); n=len(e.encode(t)); print(len(t.splitlines()),'行', n,'token', f'{n/1000:.1f}k')"
```

结构调整类的问题肉眼可见，**数字漂移是唯一看不出来的**——改了提示词没重测，README 就会开始说谎，所以这一项每次必做。

> 早先版本有过一个自动门禁脚本，后来连同配套 skill 一起去掉了：仓库只剩一份文本，为它维护一套校验脚本不划算。代价是数字漂移不再被自动拦截，靠上面这条命令兜住。

## 许可

[MIT](LICENSE)
