---
name: luzzy-roster-academic
description: >
  Use when the Luzzy checklist (必读清单) hits the 学术研究 / 论文撰写 category —
  repository sub-items for academic research and paper writing; volume and license traps included.
  Answers "写论文先读什么" "做研究读哪四家" "查文献综述用什么skill" "scientific-agent-skills能整仓clone吗".
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

# 学术研究 / 论文撰写 · 仓库子项明细

提示词 §1.1.6 命中「学术研究 / 论文撰写」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（4 条 → 全读）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **academic-research-skills** `https://github.com/Imbad0202/academic-research-skills` | 正文；许可为 **NOASSERTION**（读不受影响，要装或对外分发前先确认条款） |
| 2 | **Supervisor-Skills** `https://github.com/HKUSTDial/Supervisor-Skills` | 正文（中文，博导视角）；许可为 **NOASSERTION**，同上 |
| 3 | **scientific-agent-skills** `https://github.com/K-Dense-AI/scientific-agent-skills` | 合集仓的读法：读它的**技能索引 / 目录页，再读 1-2 个与当前任务对口的技能的 SKILL.md 正文**——按需读，不逐个枚举，只读 README 摘要不算读过；**体积 252 MB，不要整仓 clone**——要装时按需取单个技能目录 |
| 4 | **AI-Research-SKILLs** `https://github.com/Orchestra-Research/AI-Research-SKILLs` | 正文——AI / ML 方向的研究工程 |

执笔纪律（来源可溯、不编造文献、区分已知与推断、引用格式统一、不生成假数据）见提示词 §14.17。**读 ≠ 装**：装之前先核体积与许可。

## Examples

Input: 命中「学术研究 / 论文」
Output: 读本表 4 条 → 全读 → 执笔纪律生效 → 落回执。

Input: 要装 scientific-agent-skills
Output: 252 MB——不整仓 clone，按需取单个技能目录 → 先核许可。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.17；本 skill 只装清单明细。
