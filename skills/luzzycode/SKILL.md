---
name: luzzycode
description: >
  Use when operating under the LuzzyCode preset and needing the detailed rules
  behind one of its resident constraints, or when routing to the right
  LuzzyCode child skill.
  Handles routing to nineteen child skills covering workflow orchestration,
  project planning, code discipline, code review, Git operations, web search,
  memory, onboarding, tool usage, documentation, Office files, presentation
  decks, HTML web development, Windows system repair, design tasks, skill
  engineering, workspace hygiene, reverse engineering, and interaction style.
  Triggers: "LuzzyCode", "鹿溪", "鹿溪喵", "which luzzy skill", "luzzycode rules",
  "preset details", "预设细则", "该查哪个 skill", "配套 skill".
  Do NOT use for general coding tasks with no LuzzyCode involvement — load the
  specific child skill directly instead (luzzycode-code, luzzycode-git, etc.).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "orchestrator"
  repository: "https://github.com/LuzzyMeow/LuzzyCode"
  source_repos:
    - name: "LuzzyCode"
      repo: "https://github.com/LuzzyMeow/LuzzyCode"
      role: "canonical source of this skill family"
---

# LuzzyCode · 编排器

本 skill 是 LuzzyCode 预设的**路由入口**。常驻提示词 `prompt/LuzzyCode.md` 承载硬规定与核心纪律；细则分散在十九个子 skill 中，按场景加载。

**权威仓库**：https://github.com/LuzzyMeow/LuzzyCode
**skill 目录**：https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills

**硬规定不在此处**——它们常驻提示词 §一，不依赖任何 skill 加载：① 必读 skill ② GitHub SSH 优先 ③ AnySearch 唯一通道。

## 子 skill 的抓取链接

本机缺哪个就抓哪个，把 `<名>` 换成下表的名字：

| 用途 | 链接 |
|---|---|
| 抓正文 | `https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/<名>/SKILL.md` |
| 镜像兜底 | `https://gh-proxy.com/https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/<名>/SKILL.md` |
| 浏览目录 | `https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/<名>` |

## 路由表

| 场景 | 加载 | 典型触发 |
|---|---|---|
| 立清单 / 进计划态 / 开目标 / 委派子代理 / 后台任务 | [`luzzycode-workflow`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-workflow) | 「列个计划」「并行查」「跑长任务」 |
| 写代码 / 重构 / 修 bug 的细则 | [`luzzycode-code`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-code) | 「命名规范」「加测试」「提交前」 |
| 克隆 / 推送 / 建仓库 / remote / PR | [`luzzycode-git`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-git) | 「传到 GitHub」「推送报错」「remote」 |
| 联网搜索 / 垂直检索 / 抓网页 | [`luzzycode-search`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-search) | 「查一下」「搜最新」「抓这个链接」 |
| 检索 / 写入 / 删除记忆、知识库 | [`luzzycode-memory`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-memory) | 「记一下」「上次说的」「建知识库」 |
| 开工检查 / 清理临时产物 / 收尾 | [`luzzycode-workspace`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-workspace) | 「工作区乱了」「收尾」「清理」 |
| 调工具 / 工具缺失降级 / 交付登记 | [`luzzycode-tools`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-tools) | 「用哪个工具」「工具报错」「交付」 |
| 写文档 / README / 报告 / 文案 | [`luzzycode-docs`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-docs) | 「写 README」「文案」「润色」「像 AI 写的」 |
| 处理 .docx / .xlsx / .pptx | [`luzzycode-office`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-office) | 「Word」「Excel」「PPT」「文档批处理」 |
| 做 PPT / 演示文稿 / 幻灯片 | [`luzzycode-ppt`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-ppt) | 「做个 PPT」「slides」「汇报材料」 |
| HTML 页面 / 网页应用 / HTML 产物 | [`luzzycode-webdev`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-webdev) | 「做个网页」「HTML 页面」「浏览器测试」 |
| Windows 修复 / 优化 / 去臃肿 | [`luzzycode-windows`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-windows) | 「电脑卡」「去预装」「蓝屏」「系统优化」 |
| 项目规划 / 需求拆解 / 写方案 | [`luzzycode-planning`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-planning) | 「规划一下」「拆需求」「写方案」 |
| 代码审查 / 评审 PR | [`luzzycode-review`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-review) | 「review 一下」「代码审查」「查安全问题」 |
| 首次对话、未配置记忆 / 搜索 | [`luzzycode-bootstrap`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-bootstrap) | 「怎么配置」「没有密钥」「首次使用」 |
| UI / 动效 / 页面 / 交互设计 | [`luzzycode-design`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-design) | 「做个界面」「加动效」「设计稿」 |
| 创建 / 审计 / 融合 skill | [`luzzycode-skills`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-skills) | 「写个 skill」「审计技能」「合并技能」 |
| 逆向 / 渗透测试 / 安全研究 | [`luzzycode-reverse`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-reverse) | 「逆向」「APK 改包」「JS 签名」「脱壳」「CTF」「渗透测试」「恶意样本」 |
| 汇报格式 / 项目上下文 / 文档落地 | [`luzzycode-interaction`](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-interaction) | 「怎么汇报」「项目结构」「写文档」 |

**路由规则**：
1. 命中单一场景 → 直接加载对应子 skill
2. 命中多个 → 全部加载（如「写个 skill 并推到 GitHub」→ `luzzycode-skills` + `luzzycode-git`）
3. 无匹配 → 不加载任何子 skill，按常驻提示词执行

## 本项目的位置

本 skill family 的权威来源是 `https://github.com/LuzzyMeow/LuzzyCode`。修改任何子 skill 时：

1. 改本地 `skills/<name>/SKILL.md`
2. 按 `luzzycode-skills` 的质量门禁自检
3. 用 `luzzycode-git` 的 SSH 流程推送

## 失效上报

任一路由目标的 skill 仓库失效、正文拿不到 → **立即告知用户**该指向需要更新，再按子 skill 的降级规则继续。

## 示例

Input: 「我要写个 skill 并推到 GitHub」
Output: 命中多场景 → 同时加载 `luzzycode-skills` + `luzzycode-git`（路由规则 2）→ 先按 skill 工程走质量门禁，再按 SSH 流程推送

Input: 「这个任务该查哪个 skill」
Output: 比对路由表的「典型触发」列 → 命中单一场景就直接加载那一个；无匹配就不加载任何子 skill，按常驻提示词执行（路由规则 3）

Input: 「LuzzyCode 的 skill 索引是不是过时了」
Output: 加载本 skill 拿路由表 → 与仓库 `skills/` 目录逐条比对 → 发现差异就报告，不擅自改常驻层

## Verify

- 加载的子 skill，其正文规则能否直接指导当前动作？只拿到目录摘要就是没加载成功
- 路由是否命中多个场景？命中多个就要全部加载，不能只取一个
- 与常驻提示词的硬规定冲突时，是否以硬规定为准并向用户报告了冲突？
