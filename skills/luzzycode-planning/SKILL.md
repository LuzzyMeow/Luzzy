---
name: luzzycode-planning
description: >
  Use when planning a project before coding, decomposing requirements into tasks,
  writing a technical approach, or setting up persistent plans that survive
  context loss.
  Handles selection among spec-kit, OpenSpec, Get Shit Done, and
  planning-with-files, plus the boundary against the in-session task list.
  Triggers: "plan this project", "break down requirements", "write a spec",
  "technical plan", "roadmap", "项目规划", "需求拆解", "写方案", "排期", "立项".
  Do NOT use for the in-session task list (see luzzycode-workflow), for
  implementation details once a plan exists, or for reviewing existing code
  (see luzzycode-review).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "planning"
---

# LuzzyCode · 项目规划

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-planning/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-planning) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-planning/SKILL.md)

## 硬性前置：先读所选规划 skill 的正文

| skill | 星数 | 定位 | 何时选它 |
|---|---|---|---|
| [spec-kit](https://github.com/github/spec-kit) | 136k | GitHub 官方规格驱动开发工具包 | 正式项目，从规格走到实现，走 GitHub 流程 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 68k | 轻量规格层，改动以 delta 跟踪 | 已有仓库要加规格层，或做增量变更 |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done) | 64.5k | 元提示 + 上下文工程，抗上下文腐化 | 长任务、多阶段，担心上下文退化 |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 26.8k | 计划落盘到 `task_plan.md` / `findings.md` / `progress.md` | 要**可恢复**的计划 |

## 与 §三 任务清单的分工（最常混淆的一处）

| | 项目规划（本 skill） | 任务清单（`luzzycode-workflow`） |
|---|---|---|
| 管什么 | 项目级：目标、范围、阶段、交付物 | 会话级：当前这一段的执行进度 |
| 存活多久 | 跨会话，落盘到文档 | 当前会话，整表重写 |
| 谁看 | 团队 / 未来的自己 | 自己，当前任务内 |
| 粒度 | 里程碑、模块、验收标准 | ≤14 词的单个可验收动作 |

**判据**：**「下个会话还需要它吗？」** 需要 → 项目规划；不需要 → 任务清单。

## 规划质量要求

1. **先把「不做什么」写清楚**：范围蔓延是规划失败的头号原因
2. **每个阶段有可验收的产出**：写「阶段 2 产出：可登录的注册页」而不是「阶段 2：做认证」
3. **标明依赖与顺序**：哪些能并行、哪些必须等
4. **写出已知风险与假设**：不确定的地方明确标出来，别假装想清楚了
5. **不写实施细节**：规划说清做什么与验收标准，怎么写在实施时定

## 落点

计划文档放哪，服从 skill `luzzycode-workspace` 的落点纪律与仓库既有约定：

- 仓库已有 `docs/` 或既有计划文档 → **追加进去**，不新开目录
- 没有约定 → 用默认族：`PLAN-<范围>.md`、`RESEARCH-<主题>.md`、`STATUS-<范围>.md`、`WORKLOG.md`

## 示例

Input: 「我要做一个记账 App，帮我规划一下」
Output: 先澄清（平台？单机还是多端？谁用？）→ 读 spec-kit 或 planning-with-files → 写目标 / 不做什么 / 阶段划分 / 每阶段验收标准 / 风险 → 落盘到 `PLAN-记账App.md`

Input: 「这个需求帮我拆成任务」
Output: 先判是项目级还是会话级——项目级走本 skill 的规划工具；只服务当前会话就走 §三 任务清单

Input: 长任务跑到一半上下文被压缩了
Output: 读 `planning-with-files` → 把计划、发现、进度落盘 → 之后每轮从盘上恢复，不靠上下文记忆

## Verify

- 动手前：所选规划 skill 的正文读到了吗？
- 计划里写了「不做什么」吗？
- 每个阶段有可验收的产出吗？
- 依赖与顺序标了吗？风险与假设写了吗？
- 该落盘的落盘了吗？落点符合仓库约定吗？
- 有没有把项目规划误当成会话清单（或反过来）？
