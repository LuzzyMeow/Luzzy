---
name: luzzy-roster-skilldev
description: >
  Use when the Luzzy checklist (必读清单) hits the Skill 开发 / 编写 / 管理 category —
  the meta-skill for creating, auditing and fusing Agent Skills: Luzzy-Skill Architect.
  Answers "写SKILL.md之前读什么" "skill开发的清单子项" "怎么校验触发词" "创建skill的规范".
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

# Skill 开发 / 编写 / 管理 · 仓库子项明细

提示词 §1.1.6 命中「Skill 开发 / 编写 / 管理」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（1 条 → 全读）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **Luzzy-Skill Architect**（本地配套 skill）`skills/luzzy-skill-architect/SKILL.md` | 完整正文——PPER 四阶段、五阶段生命周期、成熟度 L0–L5、反模式库与质量门禁；同目录 `references/` 与 `scripts/` 按需加载 |

任何涉及 skill 的操作（创建、审计、评审、融合、拆分 family、校验 trigger）之前，先读完 architect 正文再动手——不读直接写会系统性踩反模式（description 写成能力总结、缺负面触发词、第二人称、链式引用、超 500 行、缺验证步骤）。质量门禁与触发验证用法见提示词 §14.14。

## Examples

Input: 要新建一个 skill
Output: 读本表 1 条（architect 完整正文）→ 按 PPER 与门禁产出 → 落回执。

Input: 要把长提示词转成 skill
Output: 读 architect → 按其 Phase 1–4 走 → 触发校验 ≥80% 再交付。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.14；本 skill 只装清单明细。
