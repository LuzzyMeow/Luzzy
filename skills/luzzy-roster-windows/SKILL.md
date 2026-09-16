---
name: luzzy-roster-windows
description: >
  Use when the Luzzy checklist (必读清单) hits the Windows 系统修复 / 优化 category —
  repository sub-items for Windows repair and debloat: three scripts, read all, execute one.
  Answers "Windows优化用哪家脚本" "去预装臃肿用哪个" "Sophia和WinUtil差在哪" "清理启动项读什么".
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

# Windows 系统修复 / 优化 · 仓库子项明细

提示词 §1.1.6 命中「Windows 系统修复 / 优化」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（3 条 → 全读（执行时按需求择一））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **WinUtil** `https://github.com/ChrisTitusTech/winutil` | 通用维护与全新装机，有 Standard / Minimal / Advanced 预设 |
| 2 | **Win11Debloat** `https://github.com/Raphire/Win11Debloat` | 轻量 PowerShell，只做精准去臃肿 |
| 3 | **Sophia Script** `https://github.com/farag2/Sophia-Script-for-Windows` | 150+ 函数，细粒度系统配置 |

读懂三家差异才能择优。**安全红线高于一切（提示词 §14.8）**：先建还原点再动手（`Checkpoint-Computer` 撞节流必须回读确认）；跑脚本前复述改动清单拿明确确认；禁止盲跑 `irm | iex`；WinUtil 的 Advanced 预设禁止在生产机直接跑。

## Examples

Input: 命中「Windows 修复」
Output: 三家都读对比 → 按症状择一执行 → 先还原点、再复述、再动手 → 落回执。

Input: 预装应用多
Output: 三家读完 → 择 Win11Debloat 精准移除 → 不手删 `WindowsApps` → 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.8；本 skill 只装清单明细。
