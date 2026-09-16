---
name: luzzy-roster-office
description: >
  Use when the Luzzy checklist (必读清单) hits the 文档 / Office 文件 category —
  repository sub-items for reading / writing Office files (docx / xlsx / pptx) via OfficeCLI.
  Answers "Office文件用什么工具" "docx xlsx pptx的清单子项" "OfficeCLI怎么接入" "PDF归哪一类".
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

# 文档 / Office 文件 · 仓库子项明细

提示词 §1.1.6 命中「文档 / Office 文件」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

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
| 1 | **OfficeCLI** `https://github.com/iOfficeAI/OfficeCLI` | 正文——单二进制、无需安装 Office，覆盖 Word / Excel / PowerPoint 读写与自动化 |

Office 文件是二进制封装格式，不要用文本工具直读。产出必须回读验证（能打开、内容正确）；改前先备份。执行纪律见提示词 §14.5。

**PDF 归属**：先读 OfficeCLI，按它的能力清单判断是否覆盖；不覆盖 → 按 §五 澄清。

## Examples

Input: 命中「文档 / Office 文件」
Output: 读本表 1 条 → 读完正文再动手 → 落回执。

Input: 生成 .xlsx 交付
Output: 读 OfficeCLI 正文 → 生成后回读验证 → 交付登记。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.5；本 skill 只装清单明细。
