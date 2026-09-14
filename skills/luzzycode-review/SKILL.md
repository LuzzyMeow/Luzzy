---
name: luzzycode-review
description: >
  Use when reviewing a diff, pull request, or existing code for defects, security
  problems, or design issues, or when setting up automated review in CI.
  Handles selection among Agent Skills quality review, Open Code Review,
  sanyuan-skills, and Shippie, plus the division of labour with Ponytail review.
  Triggers: "review this PR", "review my changes", "check this diff", "code review",
  "security review", "代码审查", "评审", "看看这段代码", "查安全问题".
  Do NOT use for reviewing an entire repository for over-engineering (that is
  Ponytail `-audit`), for writing new code (see luzzycode-code), or for Git
  operations (see luzzycode-git).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "quality"
  source_repos:
    - name: "agent-skills"
      repo: "https://github.com/addyosmani/agent-skills"
    - name: "open-code-review"
      repo: "https://github.com/alibaba/open-code-review"
---

# LuzzyCode · 代码审查

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-review/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-review) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-review/SKILL.md)

## 硬性前置：先读所选审查 skill 的正文

| skill | 星数 | 定位 | 何时选它 |
|---|---|---|---|
| [Agent Skills](https://github.com/addyosmani/agent-skills) | 94k | `skills/code-review-and-quality/`：按正确性 / 可读性 / 架构 / 安全 / 性能五维审 | **默认选它**，覆盖面最广 |
| [Open Code Review](https://github.com/alibaba/open-code-review) | 23.5k | 确定性流水线 + LLM Agent，行级评论，可接 CI | 大规模自动审查、接 CI |
| [sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills) | 3.9k | 专家级：SOLID、安全、性能、错误处理、边界条件 | 要**深度**审一个改动 |
| [Shippie](https://github.com/mattzcarey/shippie) | 2.5k | 可扩展的审查 + QA agent，GitHub Action | 要可配置的 CI 审查流程 |

**读取顺序**：本机 skill 目录已有就用加载工具按精确名字读 → 没有就抓仓库 `SKILL.md` 正文（注意子目录路径，不在仓库根）→ 主域不通走镜像（常驻 §1.2）→ 全部失败**【立即上报失效链接】**，再按 `luzzycode-tools` 的降级路径继续。

## 与 Ponytail 的分工

| 维度 | 谁审 |
|---|---|
| **过度设计**（多余抽象、投机代码、能删的） | Ponytail `-review` / `-audit` |
| **正确性 / 安全 / 性能 / 架构** | 本 skill 的四家 |
| **工作区与提交卫生** | skill `luzzycode-git` + `luzzycode-workspace` |

两者**互补，可以都跑**。只跑 Ponytail 会漏掉安全缺陷；只跑本 skill 会漏掉过度设计。

## 审查纪律

1. **先读 diff 再评论**：不看上下文就给意见，等于猜
2. **区分「必须改」与「建议」**：把阻塞性问题排在前面，风格偏好放最后
3. **给行号与具体改法**：说「第 42 行 `catch` 吞了异常」而不是「错误处理不好」
4. **不重写实现**：审查给意见，不顺手把整个文件改掉——除非用户要求直接修
5. **不评审既有风格偏好**：仓库已有的命名与结构约定不推翻（常驻提示词 §七「跟随项目现有约定」）
6. **安全项零容忍**：硬编码凭据、注入、越权、日志泄漏——发现即标为阻塞
7. **测试缺失要点名**：**非平凡逻辑**改动（分支 / 循环 / 解析 / 金额 / 安全路径）没带测试，属阻塞项；平凡改动不在此列（口径与 `luzzycode-code` 一致）

## 输出格式

```
## 阻塞项（必须改）
- `src/api.ts:42` — catch 块吞异常，失败静默。建议：记录后上抛

## 建议
- `src/api.ts:88` — 这个可选参数从未被传入，可删

## 已确认无问题
- 认证路径的边界处理正确
```

**不要**只给一堆「可以考虑」——审查的价值在于分清轻重。

## 示例

Input: 「review 一下我的改动」
Output: 读 Agent Skills 的 `code-review-and-quality` → 看 `git diff` → 按五维过 → 输出分级的清单 → 有 Ponytail 时补跑 `-review` 查过度设计

Input: 「接入 CI 做自动审查」
Output: 评估 Open Code Review 与 Shippie → 读其正文 → 给出接入方案 → 说明各自的触发条件与配额

Input: 用户只给了文件名，没给 diff
Output: 先确认审什么范围（本次改动 / 整个文件 / 整个仓库）——按 §五 澄清，不要擅自审全仓

## Verify

- 动手前：所选审查 skill 的正文读到了吗？
- 看过 diff 的完整上下文吗？
- 输出分了级吗（阻塞 / 建议 / 已确认）？
- 每条意见带行号与具体改法吗？
- 安全项有遗漏吗？
- 有没有顺手改掉不该改的代码？
