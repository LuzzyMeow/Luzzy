---
name: luzzy-roster-planning
description: >
  Use when the Luzzy checklist (必读清单) hits the 项目规划 / 需求拆解 category —
  repository sub-items for project planning and requirement breakdown: four frameworks, read all.
  Answers "项目规划要读哪四家" "需求拆解用什么skill" "写技术方案先读什么" "spec-kit和OpenSpec怎么选".
  Do NOT use for executing the task itself — discipline and red lines live in the Luzzy
  system prompt — nor for the reading gate, receipt, or triage logic, nor for other
  checklist categories or tasks unrelated to this one.
license: MIT
metadata:
  version: "1.0.0"
  author: "鹿溪 (LuzzyMeow)"
  category: "luzzy-roster"
  maturity: "L2"
---

# 项目规划 / 需求拆解 · 仓库子项明细

提示词 §1.1.6 命中「项目规划 / 需求拆解」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（4 条 → 全读（执行时按需求择一））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **spec-kit** `https://github.com/github/spec-kit` | 正文 |
| 2 | **OpenSpec** `https://github.com/Fission-AI/OpenSpec` | 正文 |
| 3 | **GSD Core** `https://github.com/open-gsd/gsd-core` | 正文 |
| 4 | **planning-with-files** `https://github.com/OthmanAdi/planning-with-files` | 正文 |

规划质量要求（先写「不做什么」、每阶段有可验收产出、标依赖与风险）与项目级 / 会话级的层级判分见提示词 §14.6 与 §10.1——规划跨会话落文档，会话进度走任务清单，别混。

## Examples

Input: 命中「项目规划」
Output: 读本表 4 条 → 全读 → 执行择一 → 落回执。

Input: 新项目立项
Output: 同上 → 先把「不做什么」写清楚再拆阶段 → 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.6；本 skill 只装清单明细。
