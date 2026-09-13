---
name: luzzycode-docs
description: >
  Use when writing or rewriting prose — README files, documentation, reports,
  release notes, emails, marketing copy, or any user-facing text.
  Handles the mandatory stop-slop and avoid-ai-writing skill reads, AI-tell
  removal, tone calibration, and documentation placement.
  Triggers: "write a README", "write docs", "draft a report", "write copy",
  "polish this text", "sounds like AI", "写文档", "写 README", "文案", "润色",
  "AI 腔", "报告".
  Do NOT use for pure code comments (see luzzycode-code), for Office file
  manipulation (see luzzycode-office), or for deciding where files belong
  (see luzzycode-workspace).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "writing"
---

# LuzzyCode · 文档与写作

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-docs/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-docs) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-docs/SKILL.md)

## 硬性前置：必须先完整阅读两项写作 skill

**任何文档编写 / 写作 / 文案创作任务之前，必须完整阅读**：

1. **stop-slop** —— https://github.com/hardikpandya/stop-slop
2. **avoid-ai-writing** —— https://github.com/conorbronsdon/avoid-ai-writing

**触发口径（全部算）**：写 README / 说明 / 报告 / 发布说明 / 邮件 / 对外文章 / 营销文案，或对既有文本做润色改写。

**读取顺序**：
1. 先用 skill 加载工具按精确名字从会话 skill 目录读取（首选）
2. 目录里没有 → 从上述仓库读取 `SKILL.md` 正文
3. 都不行 → AnySearch 抓取 / §1.2 镜像中转
4. **全部失败 → 立即上报用户该指向失效**，再按下方降级继续

**判定标准**：只看到仓库简介或 README 摘要**不算读过**；必须是 skill 指令正文。

## 为什么必读

这两项专治「AI 腔」——它们定义了机器生成文本的特征清单（过度对仗、空洞排比、「不仅是…更是…」、三段式总结、emoji 装饰、无信息量的过渡句）与替换策略。不读就写，产出会带明显机器痕迹，尤其在对外文案与正式文档里。

## 写作纪律（skill 之外的通用要求）

- **先想清楚给谁看**：技术文档给工程师，面向用户文案给终端用户——同一件事两种写法
- **删掉不加信息的句子**：「值得注意的是」「总而言之」「在当今快速发展的…」这类一律删
- **具体优于抽象**：写「冷启动 1.2 秒」而不是「性能优异」
- **能短就别长**：一句话能说完不写三句；解释比代码长就把解释删掉（同 §四）
- **不堆 emoji 与分隔线**：正式文档不用装饰性符号
- **术语一致**：同一概念全文用同一个词，不换着花样说
- **中文标点用全角**，中英混排时英文术语前后不加多余空格

## 落点

- 文档放哪、叫什么名字，服从 skill `luzzycode-workspace` 的落点纪律与仓库既有约定
- **禁止平行落点**：仓库已有 `docs/` 就不再建 `notes/`
- 未经要求不主动创建 README / 总结 / 报告（常驻提示词 §七「绝不做」）

## 示例

Input: 「给这个项目写个 README」
Output: 先读 stop-slop + avoid-ai-writing → 读仓库既有约定与 `package.json` → 写：项目是什么 / 怎么装 / 怎么用 / 怎么测 → 自检有无 AI 腔 → 交付

Input: 「这段话读起来像 AI 写的，帮我改」
Output: 读 avoid-ai-writing 的特征清单 → 逐条对照原文 → 删排比与过渡句、换具体表达 → 给出改后版本并说明删了什么

Input: 两项写作 skill 仓库都访问不了
Output: **立即上报**「stop-slop 与 avoid-ai-writing 指向链接失效，需要你更新」→ 用本 skill「写作纪律」一节兜底完成 → 交付时说明未读到 skill 正文

## Verify

- 动手前：两项写作 skill 正文是否都读到了？
- 交付前：通读一遍，是否还有 AI 腔特征（空洞排比 / 过渡句 / emoji 装饰）？
- 是否有不加信息量的句子？删掉后是否更好？
- 术语是否全文一致？
- 标点是否为全角？
- 落点是否符合仓库约定、未造平行目录？
