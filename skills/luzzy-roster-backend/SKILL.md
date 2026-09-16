---
name: luzzy-roster-backend
description: >
  Use when the Luzzy checklist (必读清单) hits the 后端 / 通用编码 category —
  repository sub-items for backend / general coding tasks (Ponytail, spec-kit, mattpocock/skills).
  Answers "后端编码要读哪些仓库" "写后端代码前先读什么" "通用编码的清单子项是什么" "Ponytail 的配套命令有哪些".
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

# 后端 / 通用编码 · 仓库子项明细

提示词 §1.1.6 命中「后端 / 通用编码」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（3 条 → 全读）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **Ponytail** `https://github.com/DietrichGebert/ponytail` | 正文；另含 review / audit / debt / gain / help 配套 |
| 2 | **spec-kit** `https://github.com/github/spec-kit` | 正文 |
| 3 | **mattpocock/skills** `https://github.com/mattpocock/skills` | 正文 |

## Examples

Input: 命中「后端 / 通用编码」
Output: 读本表三条 → 全读正文 → Ponytail 的阶梯与纪律以提示词 §四 为准 → 落回执。

Input: 只想要 spec-kit 的用法
Output: 仍按口径全读三条（折减只在超过 4 条时允许）→ 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §四 与 §14.2；本 skill 只装清单明细。
