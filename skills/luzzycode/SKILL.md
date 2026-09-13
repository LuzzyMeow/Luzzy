---
name: luzzycode
description: >
  Use when operating under the LuzzyCode preset and needing the detailed rules
  behind one of its resident constraints, or when routing to the right
  LuzzyCode child skill.
  Handles routing to nine child skills covering workflow orchestration, code
  discipline, Git operations, web search, memory, workspace hygiene, tool usage,
  design tasks, and skill engineering.
  Triggers: "LuzzyCode", "鹿溪", "which luzzy skill", "luzzycode rules",
  "preset details", "预设细则", "该查哪个 skill".
  Do NOT use for general coding tasks with no LuzzyCode involvement — load the
  specific child skill directly instead (luzzycode-code, luzzycode-git, etc.).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "orchestrator"
  source_repos:
    - name: "LuzzyCode"
      repo: "https://github.com/LuzzyMeow/LuzzyCode"
      role: "canonical source of this skill family"
---

# LuzzyCode · 编排器

本 skill 是 LuzzyCode 预设的**路由入口**。常驻提示词 `prompt/LuzzyCode.md` 承载硬规定与核心纪律；细则分散在九个子 skill 中，按场景加载。

**硬规定不在此处**——它们常驻提示词 §一，不依赖任何 skill 加载：① 必读 skill ② GitHub SSH 优先 ③ AnySearch 唯一通道。

## 路由表

| 场景 | 加载 | 典型触发 |
|---|---|---|
| 立清单 / 进计划态 / 开目标 / 委派子代理 / 后台任务 | `luzzycode-workflow` | 「列个计划」「并行查」「跑长任务」 |
| 写代码 / 重构 / 修 bug 的细则 | `luzzycode-code` | 「命名规范」「加测试」「提交前」 |
| 克隆 / 推送 / 建仓库 / remote / PR | `luzzycode-git` | 「传到 GitHub」「推送报错」「remote」 |
| 联网搜索 / 垂直检索 / 抓网页 | `luzzycode-search` | 「查一下」「搜最新」「抓这个链接」 |
| 检索 / 写入 / 删除记忆、知识库 | `luzzycode-memory` | 「记一下」「上次说的」「建知识库」 |
| 开工检查 / 清理临时产物 / 收尾 | `luzzycode-workspace` | 「工作区乱了」「收尾」「清理」 |
| 调工具 / 工具缺失降级 / 交付登记 | `luzzycode-tools` | 「用哪个工具」「工具报错」「交付」 |
| 写文档 / README / 报告 / 文案 | `luzzycode-docs` | 「写 README」「文案」「润色」「像 AI 写的」 |
| 处理 .docx / .xlsx / .pptx | `luzzycode-office` | 「Word」「Excel」「PPT」「文档批处理」 |
| 首次对话、未配置记忆 / 搜索 | `luzzycode-bootstrap` | 「怎么配置」「没有密钥」「首次使用」 |
| UI / 动效 / 页面 / 交互设计 | `luzzycode-design` | 「做个界面」「加动效」「设计稿」 |
| 创建 / 审计 / 融合 skill | `luzzycode-skills` | 「写个 skill」「审计技能」「合并技能」 |
| 汇报格式 / 项目上下文 / 文档落地 | `luzzycode-interaction` | 「怎么汇报」「项目结构」「写文档」 |

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

## Verify

- 子 skill 加载后，其正文规则应能直接指导当前动作
- 若加载后发现与常驻提示词冲突 → **以常驻提示词的硬规定为准**，并向用户报告冲突
