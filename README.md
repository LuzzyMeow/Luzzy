# LuzzyCode

鹿溪（Coding 模式）：给编码 Agent 用的一套行为契约，拆成常驻提示词与 19 个按需加载的 skill。

[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-19-1f6feb?style=flat-square)](skills/)
[![Resident](https://img.shields.io/badge/resident-11.9k_tokens-8250df?style=flat-square)](prompt/LuzzyCode.md)
[![Convention](https://img.shields.io/badge/format-agentskills.io-0969da?style=flat-square)](https://agentskills.io/specification)

## 30 秒上手

```bash
# 1. 取仓库
git clone git@github.com:LuzzyMeow/LuzzyCode.git

# 2. 装 skill 到 Agent 的 skill 目录
cp -r LuzzyCode/skills/* ~/.dsh/skills/     # DeepSeek Harness
# 其他宿主：~/.claude/skills/ · ~/.agents/skills/ · <project>/.agents/skills/

# 3. 把常驻提示词注入为 system prompt
cat LuzzyCode/prompt/LuzzyCode.md
```

## 它解决什么问题

Agent 的提示词越写越长，规则越多越不遵守。

一份 13k token 的常驻提示词塞进 200 多条规则，模型会在中段开始丢指令。首因效应让后半段的约束先失效，于是出现「一半照做一半没做」的结果：搜索走了一个工具、抓取走了另一个，看起来合规，实际上违反了规则。

LuzzyCode 把这个问题拆成两层解决。

## 分层设计

| 层 | 放什么 | 何时进上下文 |
|---|---|---|
| 常驻层 | 每轮必须生效的硬规定、安全红线 | 每次请求 |
| skill 层 | 命中特定场景才需要的细则 | 用时加载 |

常驻约束从 200 多条压到 70 条左右，细则一条没删，改成按需取用。

常驻层还留了一条反向约束：硬规定**不许**下沉为 skill。否则会形成循环依赖，要读 skill 才知道要读 skill。

## 仓库结构

```
LuzzyCode/
├── prompt/
│   └── LuzzyCode.md              常驻提示词，注入为 system prompt
├── skills/
│   ├── luzzycode/                编排器，路由表与冲突裁决
│   ├── luzzycode-workflow/       清单 / 计划 / 目标 / 子代理
│   ├── luzzycode-code/           命名 / 控制流 / 注释 / 测试
│   ├── luzzycode-git/            SSH 优先 / 镜像中转 / 提交卫生
│   ├── luzzycode-search/         AnySearch 四条路由
│   ├── luzzycode-memory/         MemOS 记忆与知识库
│   ├── luzzycode-bootstrap/      首次配置引导
│   ├── luzzycode-tools/          工具选择与降级路径
│   ├── luzzycode-docs/           写作规则与 AI 腔清除
│   ├── luzzycode-office/         .docx / .xlsx / .pptx
│   ├── luzzycode-ppt/            归藏·大狮·HTML PPT Studio 选择与验收
│   ├── luzzycode-webdev/         HTML 页面与浏览器实测
│   ├── luzzycode-design/         四项设计 skill 与视觉验收
│   ├── luzzycode-planning/       四家规划工具选择
│   ├── luzzycode-review/         四家审查工具选择
│   ├── luzzycode-windows/        Windows 修复与安全红线
│   ├── luzzycode-skills/         skill 工程
│   ├── luzzycode-workspace/      落点纪律与收尾自检
│   └── luzzycode-interaction/    汇报格式与项目上下文
├── scripts/
│   └── check-skills.py           质量门禁校验脚本
├── README.md
├── LICENSE
└── .gitattributes
```

## 三条硬性规定

常驻层的最高优先级约束。它们不依赖 skill 加载，每轮都在上下文里。

### 一、必读 skill

十类任务各有指定 skill，读完正文才算通过。看仓库首页或目录列表不算。

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
| skill 开发 / 管理 | [Luzzy-Skill Architect](https://github.com/LuzzyMeow/Luzzy-Skill-Architect) |

编码、设计、PPT、网页开发、Windows、规划、审查这几类都给了多家，按需求择一或组合，细则各在对应的 `luzzycode-*` skill 里。

任一链接失效，Agent 立刻告诉你哪一条需要更新，然后走降级规则继续干活。

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

## 十九个 skill

<details open>
<summary><b>编排与流程</b></summary>

| skill | 加载时机 | 覆盖内容 |
|---|---|---|
| `luzzycode` | 需要路由到子 skill | 路由表、冲突裁决 |
| `luzzycode-workflow` | 立清单 / 进计划态 / 开目标 / 委派子代理 | 清单三态语义、计划态只读、目标生命周期（含 3 回合阻塞规则）、后台任务 |
| `luzzycode-planning` | 立项 / 拆需求 / 写方案 | spec-kit·OpenSpec·GSD Core·planning-with-files 四家选择、与会话清单的分工 |
| `luzzycode-interaction` | 汇报 / 获取项目上下文 | 汇报格式、AGENTS.md 优先的阅读顺序、文档落地 |

</details>

<details open>
<summary><b>开发与交付</b></summary>

| skill | 加载时机 | 覆盖内容 |
|---|---|---|
| `luzzycode-code` | 写代码 / 重构 / 修 bug | 命名、控制流、注释、测试、产出格式 |
| `luzzycode-review` | 评审 diff / PR / 既有代码 | Agent Skills·Open Code Review·sanyuan-skills·Shippie 四家选择、与 Ponytail 的分工 |
| `luzzycode-git` | 克隆 / 推送 / 建仓库 / remote | SSH 优先、remote 纠正、镜像中转、提交卫生、换行符归一 |
| `luzzycode-tools` | 调工具 / 工具缺失 | glob·grep·read·write·edit·read_image、后台命令、present 登记、降级表 |
| `luzzycode-workspace` | 开工 / 收尾清理 | 落点纪律、命名、收尾自检、脏工作区授权边界 |
| `luzzycode-docs` | 写 README / 报告 / 文案 | 两项写作 skill 调用、AI 腔清除、文档落点 |
| `luzzycode-office` | 处理 Office 文件 | OfficeCLI 调用、格式坑位、产出回读验证 |
| `luzzycode-ppt` | 做 PPT / 演示文稿 / 幻灯片 | 归藏·大狮·HTML PPT Studio 三家选择、整仓安装、逐页验收 |
| `luzzycode-webdev` | 做 HTML 页面 / 网页应用 | 官方 skills 调用、浏览器实测、响应式与可访问性 |

</details>

<details open>
<summary><b>能力集成</b></summary>

| skill | 加载时机 | 覆盖内容 |
|---|---|---|
| `luzzycode-search` | 联网检索 / 抓网页 | 四条路由、垂直域、参数纪律、来源分级、内容安全 |
| `luzzycode-memory` | 检索 / 写入 / 删除记忆 | MemOS 能力清单、写入格式、四步安全判断、知识库操作 |
| `luzzycode-bootstrap` | 首次对话且未配置 | 免密钥通道、文档抓取、配置引导 |
| `luzzycode-design` | UI / 动效 / 页面设计 | 四项设计 skill 获取与降级、截图验收 |
| `luzzycode-windows` | Windows 修复 / 优化 / 去臃肿 | WinUtil·Win11Debloat·Sophia Script 三家选择、还原点与改动确认红线 |
| `luzzycode-skills` | 创建 / 审计 / 融合 skill | Architect 调用、质量门禁、触发验证 |

</details>

十九个 skill 相互独立。完整的「场景 → skill」路由表在 `luzzycode` 的正文里，常驻提示词 §12.1 只留名字清单与抓取链接模板——同一份清单不放两处，免得漂移也免得白付常驻预算。增删 skill 时同步三处：`skills/` 目录、`luzzycode` 的路由表、常驻 §12.1 的名字清单。

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

走通之后，`luzzycode-bootstrap` 会抓取官方文档自读，再一次性给你两项 Key 的配置步骤：

| 服务 | 取 Key | 需要的变量 |
|---|---|---|
| AnySearch | [控制台](https://www.anysearch.com/console/api-keys) | `ANYSEARCH_API_KEY` |
| MemOS | [控制台](https://memos-dashboard.openmem.net/cn/apikeys/) | `MEMOS_API_KEY` · `MEMOS_USER_ID` · `MEMOS_CHANNEL=MODELSCOPE` |

`MEMOS_USER_ID` 用稳定标识（邮箱、姓名或工号）。不要用随机值或会话 ID，同一用户在不同设备上必须一致。

## 提示词预算

| 层 | 内容 | 行数 | 实测 token |
|---|---|---|---|
| 常驻 | `prompt/LuzzyCode.md` | 428 | 11,894 |
| 按需 | 19 个 skill 正文 | 1,476 | 27,869 |

token 数由 `tiktoken` 的 `o200k_base` 编码实测得出（同一份文本按 `cl100k_base` 约高 20%），不是估算。

「按需」只算 skill 的**正文**——每个 skill 的 frontmatter（`description` 等）是常驻 skill 目录的一部分，每轮都在上下文里，19 个合计约 3.9k token，属常驻开销。

典型编码任务加载常驻加 `luzzycode-workflow`、`luzzycode-code`、`luzzycode-git` 三个 skill 的正文，约 17.7k token。纯闲聊只付常驻的 11.9k。

skill 的加载靠 description 触发。每个 description 都写了「何时用」和「不要用」，避免误激活。

## 兼容性

提示词与 Agent 无关，能直接当 system prompt 用。

skill 走 agentskills.io 的 `SKILL.md` 规范，`name` 用 kebab-case，`description` 必填。DeepSeek Harness、Claude Code 以及符合该规范的宿主都能加载。十九个 skill 逐个过了 DSH 的解析器校验。

提示词里出现的工具名（`todo_write`、`glob`、`present` 等）都当能力示例看。预设要求 Agent 先盘点本机真实工具再映射，缺失时走 `luzzycode-tools` 里的降级表。

## 更新与维护

常驻提示词 §1.1a 规定了本机缺 skill 时的抓取流程：

```bash
# 抓单个 skill 正文
https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/<名字>/SKILL.md

# 不通时加代理前缀
https://gh-proxy.com/https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/<名字>/SKILL.md
```

Agent 也会定期对比本机 skill 目录与本仓库内容，发现差异会告诉你变了什么。它不会自动覆盖你的本地预设，改不改由你决定。

## 质量门禁

改完 skill 跑一遍校验，它检查 `luzzycode-skills` 里写明的门禁条目，外加仓库级一致性：

```bash
python scripts/check-skills.py            # 失败返回 1
python scripts/check-skills.py --verbose  # 逐项打印通过情况
```

查这些：`name` 与目录名一致且 kebab-case、`description` 含负面触发词且不泄漏步骤、正文 ≤500 行且无第二人称、至少 2 组 Input→Output、有 `Verify` 段、无 emoji 与装饰分隔线；仓库级查计数是否与目录一致、提示词引用的 skill 名是否存在、编排器路由表是否覆盖全部子 skill、抓取链接模板是否仍指向本仓库。

只用标准库，不依赖 PyYAML。门禁脚本自身也守着一条纪律：**写了就必须能跑**——上一版的门禁是纯文字清单，从没被执行过，于是 19 个 skill 全部违反其中的「无装饰性格式」而无人发现。

## 许可

[MIT](LICENSE)
