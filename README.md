# LuzzyCode

鹿溪（Coding 模式）：给编码 Agent 用的一套行为契约。**规则装在一个提示词文件里，操作细则装在同仓库的配套 skill 里。**

[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Prompt](https://img.shields.io/badge/prompt-28.1k_tokens-8250df?style=flat-square)](prompt/LuzzyCode.md)
[![Skills](https://img.shields.io/badge/配套_skill-3_个-0969da?style=flat-square)](skills/)
[![Rules](https://img.shields.io/badge/规则-十六类必读清单-1f883d?style=flat-square)](prompt/LuzzyCode.md)

## 30 秒上手

```bash
git clone git@github.com:LuzzyMeow/LuzzyCode.git

# 注入为 system prompt
cat LuzzyCode/prompt/LuzzyCode.md
```

一份提示词，加上 `skills/` 里按需加载的细则。不需要同步第二份清单——规则只有一处。

## 它解决什么问题

Agent 的提示词越写越长，规则越多越不遵守。

一份超过万 token 的常驻提示词塞进两百多条规则，模型会在中段开始丢指令。首因效应让后半段的约束先失效，于是出现「一半照做一半没做」的结果：搜索走了一个工具、抓取走了另一个，看起来合规，实际上违反了规则。

这个仓库的两条对策：

1. **规则按「什么时候需要」重新编排**，写成一份自洽的提示词，并给必读清单配一条可执行的阅读规则
2. **把「必须读」变成可核对的动作**——命中清单要停手、读完、落一份读取回执才动手（见下）

## 目录

```
LuzzyCode/
├── prompt/
│   └── LuzzyCode.md          全部规则，注入为 system prompt
├── skills/                   配套 skill：按需加载的操作细则
│   ├── luzzy-skill-architect/    创建 / 审计 / 融合 Agent Skills 的元框架
│   ├── luzzy-skill-meihuayishu/  梅花易数技能家族（零依赖引擎 + 原文内置）
│   └── luzzy-bilibili-notes/     B 站视频转结构化笔记
├── AGENTS.md                 维护指南 + 九家 harness 路径速查
├── README.md
└── LICENSE
```

## 规则怎么组织

提示词按「用的人的思路」分节，另有三个入口块：

| 块 | 内容 | 给谁看 |
|---|---|---|
| **导航** | 三条最高优先级铁律 + 「我要…去哪」速查表 | 开场定位 |
| **§1.1 必读清单** | 十六类任务的清单、阅读规则、读取回执、反假读条款 | 每个任务起手 |
| **§14 领域细则** | 十六个领域的执行纪律、红线、失败路径 | 读完清单之后 |

分节顺序：`〇` 身份 → `一` 硬规定 → `二` 工作循环（七步）→ `三` 工具 → `四` 代码纪律 → `五` 澄清 → `六` 安全红线 → `七` 边界与工作区 → `八` 文档阅读 → `九` 记忆 → `十` 编排工具 → `十一` 汇报 → `十二` 交付与纠错 → `十三` 本次任务 → `十四` 领域细则（14.1–14.16）→ 附录 A 固化链接 · 附录 B 维护。

## 三条硬规定

### 一、必读清单 —— 先读后做

十六类任务各有清单。**命中即触发**：识别到关键词 → 停手读完 → 落回执 → 才动手。

```text
必读清单命中：<类目名>
├─ 已读：<子项> — <来源：本机路径 / 抓取的 URL>
├─ 已读：<子项> — <来源>
└─ 折减：<是否折减 + 理由>
```

**未读就动手，结果一律无效。** 回执让「有没有读」从主观声称变成可核对的事实。

阅读规则的三条要点：

- **4 条及以内 → 全读**；**超过 4 条 → 取其中任意 4 条**（按相关性择优）
- **读到正文才算**：看首页、简介、目录列表、README 摘要**都不算**
- **先本机后云端**：本机已有就直接读，标为「本地配套 skill」的读 `skills/` 下的路径

还有**反假读条款**，把模型最常犯的五种「假读」逐条封死：只读门面、凭记忆代读、挑一条就读、同名顶替、读完不落回执——外加一种「读了不照做」。

| 任务类型 | 必读（完整十六类见 [§1.1](prompt/LuzzyCode.md)） |
|---|---|
| 后端 / 通用编码 | [Ponytail](https://github.com/DietrichGebert/ponytail) · [spec-kit](https://github.com/github/spec-kit) · [mattpocock/skills](https://github.com/mattpocock/skills) |
| 设计类 | [huashu-design](https://github.com/alchaincyf/huashu-design) · [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) · [open-design](https://github.com/nexu-io/open-design) · [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| 做 PPT | [归藏PPT](https://github.com/op7418/guizang-ppt-skill) · [大狮PPT](https://github.com/chuspeeism/dashi-ppt-skill) · [HTML PPT Studio](https://github.com/lewislulu/html-ppt-skill) |
| 代码审查 | [Agent Skills](https://github.com/addyosmani/agent-skills) · [Open Code Review](https://github.com/alibaba/open-code-review) · [sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills) · [Shippie](https://github.com/mattzcarey/shippie) |
| **浏览器自动化** | 本机官方 skill `~/.agents/skills/tabbit/` · [dsh-tabbit](https://github.com/Tabbit-Browser/dsh-tabbit) · [Tabbit-Devtools-Skill](https://github.com/Tabbit-Browser/Tabbit-Devtools-Skill) |
| **Skill 工程** | 本地配套 skill [`skills/luzzy-skill-architect/`](skills/luzzy-skill-architect/) |
| **B 站视频转笔记** | 本地配套 skill [`skills/luzzy-bilibili-notes/`](skills/luzzy-bilibili-notes/) |

三类任务的硬性前置值得单独点出：

- **逆向 / 安全**：只对自有资产、明确授权的目标、本地样本与 CTF 靶场；其 `precedent-*` 与「服从性」文件**不得**绕过安全红线
- **Android**：必须先在 ZCode 内、从插件市场装官方插件 `android-emulator`——它的 MCP 服务器由 ZCode 插件宿主拉起
- **浏览器自动化**：优先用 Tabbit（`https://www.tabbit.com/`）；没装就引导安装或改用同类型方案（见 §14.16）

任一链接失效，Agent 会立即告诉你哪一条需要更新，然后按降级规则继续干活。

### 二、GitHub 操作走 SSH

克隆、拉取、推送一律用 `git@github.com:...`。`gh repo create` 默认生成 HTTPS remote，建完要立刻改正：

```bash
git remote set-url origin git@github.com:<owner>/<repo>.git
git remote -v     # 两行都应以 git@github.com: 开头
```

国内网络受限时逐级降级（gh-proxy → ghfast → AnySearch 抓单文件 → Gitee 导入）。代理经实测筛选，**用前先探一次**。

### 三、联网检索走 AnySearch

判据不看工具名，看动作性质：**「这个动作的目的，是找到我手里还没有地址的东西吗？」** 是 → 检索，只走 AnySearch。

用内置搜索做资料搜索、只在抓取时用 AnySearch，这种**半程合规视为违规**。内置工具仅作回退，且要在回答里说明。

## 配套 skill

`skills/` 里的技能是**操作细则**，不是规则的副本——规则只住在提示词里，因此不存在两处漂移。命中场景时提示词会指向它们；本机已有就直接读，不必联网。

| 技能 | 用途 | 许可 |
|---|---|---|
| [`luzzy-skill-architect/`](skills/luzzy-skill-architect/) | 创建、审计、诊断、融合 Agent Skills：PPER 协议 + 五阶段生命周期 + L0–L5 成熟度 + 七设计模式 + 十反模式库 | Apache-2.0 |
| [`luzzy-skill-meihuayishu/`](skills/luzzy-skill-meihuayishu/) | 梅花易数技能家族：零依赖起卦引擎 + 《周易》《梅花易数》原文内置 + 原书占例回归 16/16 | MIT |
| [`luzzy-bilibili-notes/`](skills/luzzy-bilibili-notes/) | B 站视频转结构化笔记：取字幕、解析 SRT、重组章节、标注识别错误与存疑项 | MIT |

安装到某个 Agent 的 skill 目录：

```bash
cp -r LuzzyCode/skills/luzzy-skill-architect ~/.claude/skills/    # Claude Code
cp -r LuzzyCode/skills/luzzy-bilibili-notes  ~/.agents/skills/    # Codex / OpenClaw 等
```

各家 harness 的 skill 目录与 MCP 配置路径速查见 [`AGENTS.md`](AGENTS.md) 第七节。

> **`luzzy-skill-meihuayishu/` 自带维护宪章** [`AGENTS.md`](skills/luzzy-skill-meihuayishu/AGENTS.md)：十条红线（经典文本不可改写、计算一律走引擎、回归门槛不可放宽）与四类变更流程。改它之前必须先读，并跑通三条回归命令（见 [`skills/README.md`](skills/README.md)）。

## 零配置启动

本机没挂 MemOS 和 AnySearch 时，不必先去申请 Key。AnySearch 的匿名通道能完成检索与抓取：

```bash
# 取 skill 包（含 Python / Node / PowerShell / Bash 四套脚本）
curl -L -o anysearch-skill.zip \
  https://github.com/anysearch-ai/anysearch-skill/archive/refs/heads/main.zip
unzip anysearch-skill.zip

python <skill_dir>/scripts/anysearch_cli.py search "关键词" --max_results 5
```

走通之后，提示词 §1.5 会让 Agent 抓取官方文档自读，再一次性给你两项 Key 的配置步骤：

| 服务 | 取 Key | 需要的变量 |
|---|---|---|
| AnySearch | [控制台](https://www.anysearch.com/console/api-keys) | `ANYSEARCH_API_KEY` |
| MemOS | [控制台](https://memos-dashboard.openmem.net/cn/apikeys/) | `MEMOS_API_KEY` · `MEMOS_USER_ID` · `MEMOS_CHANNEL=MODELSCOPE` |

`MEMOS_USER_ID` 用稳定标识（邮箱、姓名或工号）。不要用随机值或会话 ID，同一用户在不同设备上必须一致。

## 提示词预算

| 内容 | 行数 | 实测 token |
|---|---|---|
| `prompt/LuzzyCode.md` | 1,143 | 28,120 |
| `skills/`（三个技能，**按需加载，不常驻**） | 8,564 | — |

token 数由 `tiktoken` 的 `o200k_base` 编码实测得出（同一份文本按 `cl100k_base` 约高 20%），不是估算。

**常驻成本只有那 28k**：配套 skill 只在命中场景时才读，平时不占上下文。早先的两层版本是常驻 14.8k + 按需 38.5k；现在是提示词涨到 28k、按需层收敛到 8.5k——换来的是规则只有一个事实源，清单不再漂移。

`AGENTS.md`（维护指南与九家 harness 路径表）只在维护本仓库或查 harness 路径时读，不必注入 system prompt。

## 兼容性

提示词与 Agent 无关，能直接当 system prompt 用。DeepSeek Harness、Claude Code、ZCode、Codex、OpenCode、QwenPaw、OpenClaw、Hermes Agent、Cherry Studio 等都适用——各家把文件放哪、MCP 配在哪，见 [`AGENTS.md`](AGENTS.md) 第七节的九家路径速查表，每项附官方文档链接。

提示词里出现的工具名（`todo_write`、`glob`、`present` 等）都当能力示例看。预设要求 Agent 先盘点本机真实工具再映射，缺失时走降级表（§3.5）。

## 更新与维护

```bash
# 抓单个文件即可
https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/prompt/LuzzyCode.md

# 不通时加代理前缀
https://gh-proxy.com/https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/prompt/LuzzyCode.md
```

Agent 也会定期对比本机副本与本仓库内容，发现差异会告诉你变了什么。它不会自动覆盖你的本地副本，改不改由你决定。

## 改完怎么自查

没有配套的门禁脚本——这个仓库就是文本，改完靠人工核对。`AGENTS.md` 第四节有同样的清单：

| 核对什么 | 怎么验 |
|---|---|
| 十四个正文章节 + 导航 + 附录 A/B 齐全 | 搜 `^# ` 列出所有一级标题对一遍 |
| §1.1 十六类清单齐全，条数与「条数 / 执行要点」列一致 | 数表格行 |
| 所有 `§` 交叉引用都能找到对应小节 | 抄出所有 `§` 引用逐个跳过去；**改章节编号时最容易漏** |
| 无残留旧机制写法（`luzzycode-*`、旧 skill 加载方式） | 搜关键词 |
| 无装饰性 emoji、无裸露分隔线、无硬编码密钥 | 目视 + 搜 `^---$` / `sk-`；三档标记 ✅⚠🚫 与正反例标记 ✗✓ 是内容，不算装饰 |
| **提示词里没有双花括号变量语法** | DSH 会把 persona 里的它当 prompt 变量解析，**全大写形式会让预设加载失败**；占位符统一用 `${...}` |
| 三个配套 skill 通过各自校验 | `validate-trigger.py`（architect / bilibili）与梅花易数三条回归命令 |
| **README 的行数与 token 等于实测值** | 跑下面的命令重测 |

```bash
# 重测提示词体量，写回「提示词预算」表与徽章
python -c "import tiktoken,pathlib; t=pathlib.Path('prompt/LuzzyCode.md').read_text(encoding='utf-8'); e=tiktoken.get_encoding('o200k_base'); n=len(e.encode(t)); print(len(t.splitlines()),'行', n,'token', f'{n/1000:.1f}k')"
```

结构调整类的问题肉眼可见，**数字漂移是唯一看不出来的**——改了提示词没重测，README 就会开始说谎，所以这一项每次必做。

## 许可

[MIT](LICENSE)。`skills/` 下各技能保留其自身许可（Apache-2.0 / MIT），见 [`skills/README.md`](skills/README.md)。
