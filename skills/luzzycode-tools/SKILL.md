---
name: luzzycode-tools
description: >
  Use when choosing or troubleshooting local tools — file discovery, content
  search, reading, editing, image inspection, command execution, artifact
  registration with present, or skill loading.
  Handles glob/grep/read/write/edit/read_image selection, command execution with
  background jobs, the read-before-write rule, present registration, and the
  degradation table for every tool that may be absent on a given host.
  Triggers: "which tool", "tool not available", "permission denied", "run this
  command", "background job", "deliver the file", "工具", "命令执行", "后台运行",
  "工具报错", "交付".
  Do NOT use for web search tooling (see luzzycode-search), for Git operations
  (see luzzycode-git), or for skill authoring rules (see luzzycode-skills).
---

# LuzzyCode · 工具使用细则

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-tools/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-tools) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-tools/SKILL.md)

**前提**：本预设点名的工具名一律只是**能力示例**——动手前先盘点本机实际暴露了哪些工具，映射到真实工具。缺失就降级，【绝不硬调不存在的工具】。

## 文件与代码工具

- **找文件用路径模式工具**（如 `glob`）：按 `**/*.ts`、`src/**/*.test.js` 这类模式定位，【不要】用 shell 的 `find` / `dir` 拼凑
- **搜内容用检索工具**（如 `grep`）：ripgrep 正则，返回文件 + 行号。「修 bug 先查所有调用方」「先读邻近代码的命名与模式」都靠它落地——【不要】用 shell 的 `findstr` / `Select-String` 代替
- **读文本用读取工具**（如 `read`）：带行号、支持 `offset` / `limit` 分段续读；【不要】用 `cat` / `type` / `Get-Content` 读文件
- **改文件两条路**：小改动用定点替换工具（如 `edit`，要求原文在文件中唯一，多处命中就扩大上下文或显式声明全替换）；整体重写用写入工具（如 `write`，**会覆盖全文**）
- **改前必读**：写入或定点替换前【必须】先读过该文件——没读过的文件直接改会被拒，而且你也不知道自己在覆盖什么
- **看图片用图像读取工具**（如 `read_image`）：读 PNG / JPEG / WebP / GIF。**设计类任务的验收靠它**——渲染出的页面截图、设计稿、图标产物，看一眼比读一百行样式代码有用；不要为了看图去装图像库或生成缩略图

## 命令执行

- **命令走命令执行工具**（如 `pwsh`）：它每次都是**全新进程**，cwd、变量、函数都不保留——所以【不要】用 `cd` 切目录，改用 `workdir` 参数；读环境变量用 `$env:NAME`
- **长命令后台跑**：构建、装依赖、跑全量测试、大范围扫描用后台模式（如 `run_in_background`）启动，立刻拿到 job id 去干别的——【不许干等】；前台直跑只留给秒级命令
- **失败要看清**：非零退出会带 `[exit code: N]` 标记，先判断原因再决定下一步，别把失败当成功继续
- 被沙箱策略拒绝时返回的是明确的「访问被拒」标记，那是策略问题不是命令写错——不要换个写法重试同一件事

## 交付登记

- **文件即交付物**：创建或修改的文件如果是用户要**收到**的产物，写完用交付登记工具（如 `present`）登记，**并在最终回答里用可点击的行内代码路径提到它**。只在正文里写个路径字符串不算交付——用户点不开
- **登记前先确认本机有这个工具**：预设不一定挂载了它。**没挂载时不要硬调**（会被拒），改为在回答里用可点击的绝对路径交付，并说明「本机无登记工具」
- 登记前确认文件确实已存在落盘；登记的是**当前源文件**，内容不会被复制或固化

## Skill 加载

- **先查后装**：命中 skill 场景时，先看**会话 skill 目录**里有没有现成的；有就按精确名字用 skill 加载工具（如 `skill`）直接读取——**这比去 GitHub 下载快得多，是首选路径**
- 目录里没有才走云端获取流程；两者都失败才按澄清提问处理
- 目录里的条目只有摘要，**不加载就不算读过**——不要凭目录里的一句话描述推断 skill 内容

## 工具缺失时的降级路径

| 缺什么 | 怎么办 |
|---|---|
| `present` | 回答里给可点击绝对路径，说明本机无登记工具 |
| `ask_user_question` | 用正文提问，仍守「单次最多 3 问、封闭式选项优先」 |
| `glob` / `grep` | 用命令执行工具里的等价命令（`Get-ChildItem -Recurse` / `Select-String`） |
| `read_image` | 说明「无法做视觉验收」，请用户确认，【不自封完成】 |
| 子代理 / 目标 / 计划类工具 | 自己串行做，并在回答里说明少了什么 |
| 记忆 / 搜索工具 | 说明该能力不可用，其余部分照常完成 |

**禁止**：调用本机不存在的工具然后声称完成；也禁止因为工具缺失就静默跳过该做的事。

## 示例

Input: 需要找项目里所有 `*.test.ts` 文件
Output: 用 `glob` 按 `**/*.test.ts` 定位；不用 shell 的 `Get-ChildItem` 拼凑

Input: 要跑一个耗时的全量测试
Output: 用 `pwsh` 的 `run_in_background` 启动拿 job id → 继续干别的 → 用 `job_output` 收结果；不干等

Input: 写完了用户要的产物文件
Output: 若本机挂载了 `present` 则登记；未挂载则不硬调，改为在回答里给可点击绝对路径并说明

## Verify

- 改文件前：是否已读过该文件？（没读过会被拒）
- 后台任务：收口时是否全部收齐、无关的是否已停掉？
- 交付：文件是否真实落盘？登记或路径是否给了？
