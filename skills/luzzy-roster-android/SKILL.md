---
name: luzzy-roster-android
description: >
  Use when the Luzzy checklist (必读清单) hits the Android 开发 / 模拟器 category —
  reading sub-items for Android development and emulator work; six entries, take four; requires the ZCode android-emulator plugin.
  Answers "Android开发的清单子项" "模拟器插件怎么装" "android-dev正文在哪" "adb文档是哪一条".
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

# Android 开发 / 模拟器 · 仓库子项明细

提示词 §1.1.6 命中「Android 开发 / 模拟器」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（6 条 → 取 4 条）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | `https://developer.android.com/develop` | 正文 |
| 2 | `https://developer.android.com/tools/adb` | 正文 |
| 3 | `https://developer.android.com/compose` | 正文 |
| 4 | `https://developer.android.com/build` | 正文 |
| 5 | 插件自带正文 `skills/android-dev/SKILL.md` | 工作流与工具说明 |
| 6 | 插件自带正文 `skills/android-dev/INSTALL_ENVIRONMENT.md` | 环境缺失时的固定安装流程 |

**硬性前置：先从 ZCode 插件市场装 `android-emulator`**（`zcode-plugins-official` 源）——不在 ZCode 内就没有这套 MCP 工具。插件缓存典型路径：`~/.zcode/cli/plugins/cache/zcode-plugins-official/android-emulator/<版本>/skills/android-dev/`。工具面（23 个）、标准工作流与失败路径见提示词 §14.12。

## Examples

Input: 命中「Android 开发」
Output: 6 条取 4（含插件自带正文两条）→ 落回执 → 按 §14.12 工作流走。

Input: 插件没装、工具没出现
Output: 不假装可用、不用裸 adb 硬拼 → 按提示词 §14.12 给安装四步并澄清。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.12；本 skill 只装清单明细。
