---
name: luzzy-roster-browser
description: >
  Use when the Luzzy checklist (必读清单) hits the 浏览器自动化 / 网页操作 category —
  reading sub-items for real-browser automation (Tabbit official skill, DSH plugin, DevTools CDP skill).
  Answers "浏览器自动化读什么" "tabbit的官方skill在哪" "接管已登录的浏览器" "网页操作的任务名怎么起".
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

# 浏览器自动化 / 网页操作 · 仓库子项明细

提示词 §1.1.6 命中「浏览器自动化 / 网页操作」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

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
| 1 | 本机官方 skill `~/.agents/skills/tabbit/`（`SKILL.md` + `references/recovery.md` + `references/host-routing.md`） | 权威正文——随浏览器 Runtime 同步 |
| 2 | **dsh-tabbit 官方插件** `https://github.com/Tabbit-Browser/dsh-tabbit` | 正文——DeepSeek Harness 集成 |
| 3 | **Tabbit-Devtools-Skill** `https://github.com/Tabbit-Browser/Tabbit-Devtools-Skill` | 正文——接管既有 Chrome / Edge |

缺 Tabbit 本体时先读官网 `https://www.tabbit.com/` 与引导（提示词 §14.16）；装完**必须启动一次**浏览器，CLI launcher 与官方 skill 才会注册。共享 cookie 的取用红线（绝不外发、用完即删、绝不入库）与登录 / 验证码 / 支付留给用户的边界见提示词 §14.16。

## Examples

Input: 命中「浏览器自动化」
Output: 读本表 3 条 → 永远用稳定 launcher → 任务名唯一并复用 → 落回执。

Input: 页面要登录
Output: 登录交回用户完成 → 复用已登录会话继续 → cookie 落临时目录用完即删。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.16；本 skill 只装清单明细。
