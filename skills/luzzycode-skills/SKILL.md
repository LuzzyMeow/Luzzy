---
name: luzzycode-skills
description: >
  Use when creating, designing, improving, auditing, reviewing, fusing, or
  managing Agent Skills (SKILL.md files), or when applying this project's own
  skill-quality standards.
  Handles the mandatory Luzzy-Skill Architect reading requirement, skill quality
  gates, progressive disclosure design, trigger validation, and this repository's
  own skill conventions.
  Triggers: "create a skill", "write a SKILL.md", "audit this skill", "review my
  skill", "improve my skill", "merge skills", "fuse skills", "skill family",
  "trigger test", "maturity level", "写 skill", "建技能", "审计技能", "技能质量".
  Do NOT use for writing general documentation, README files, or standalone
  scripts unrelated to the Agent Skills format.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "meta-skill"
---

# LuzzyCode · Skill 工程

## 硬性前置：必须先完整阅读 Luzzy-Skill Architect

**任何涉及 skill 的操作之前，必须完整阅读**：

**https://github.com/LuzzyMeow/Luzzy-Skill-Architect**

**触发口径（全部算，不许跳过）**：创建、设计、改进、审计、评审、融合（fusion）、拆分为 skill family、把长提示词转成 skill、编写 `SKILL.md`、校验 trigger、评估成熟度。

**读取顺序**：
1. 先用 skill 加载工具按精确名字 `luzzy-skill-architect` 从会话 skill 目录读取（首选）
2. 目录里没有 → 从上述仓库读取 `SKILL.md` 正文
3. 都不行 → AnySearch 抓取 / GitHub 镜像站
4. 全部失败 → 澄清提问，确认用户是否接受无 skill 执行

**判定标准**：只看到仓库简介、目录列表或 README 摘要**不算读过**；必须是 skill 指令正文。

## 为什么必须读

Architect 定义了 skill 的生命周期协议与质量门禁（PPER 四阶段、五阶段生命周期、成熟度 L0–L5、反模式库）。不读它直接写 skill，会系统性犯这些错误：

| 反模式 | 后果 |
|---|---|
| description 写成能力总结而非触发条件 | agent 读摘要就跳过正文 |
| 缺负面触发词（Do NOT use for...） | 误激活，不该用时也触发 |
| 第二人称「你应该…」 | 不如祈使句可执行 |
| 参考文件链式引用（references → references） | 加载路径不可控 |
| 正文超 500 行不拆分 | 违背渐进披露，常驻预算失控 |
| 缺验证步骤 | 静默失败 |

## 本项目自身的 skill 规范

在 Architect 标准之上，本项目的额外约定：

### 结构约定
- 每个 skill 独立目录，`SKILL.md` 必备
- 正文超 500 行 → 拆到 `references/`，**引用深度不超过 1 层**
- 需要确定性脚本 → `scripts/`，且每个脚本必须在正文里有调用说明
- 固定格式产出 → `assets/` 模板，占位符用 `{{PLACEHOLDER}}`

### 分层归属判断

| 内容性质 | 归属 |
|---|---|
| 每轮都必须生效的硬规定、安全红线 | **常驻提示词**（不得下沉为 skill） |
| 命中特定场景才需要的细则 | **skill**（按需加载） |
| 单次任务的临时指令 | 都不是——直接对话 |

**关键约束**：硬规定若下沉为 skill，会形成「要读 skill 才知道要读 skill」的循环依赖——硬规定必须留常驻层。

### 质量门禁（提交前逐项过）

- [ ] `name` 与目录名一致，符合 kebab-case
- [ ] `description` 只写触发条件，**不泄漏执行步骤**
- [ ] `description` 含负面触发词（`Do NOT use for...`）
- [ ] 正文用祈使句，无第二人称
- [ ] 正文 ≤ 500 行
- [ ] 含至少 2 组 Input → Output 示例
- [ ] 含 `Verify:` 验证步骤
- [ ] 无装饰性格式（emoji、分隔线、装饰性引用块）
- [ ] 通过 DSH 解析器校验（frontmatter + kebab-case 命名）

### 触发验证

用 Architect 自带脚本做 L1 触发测试：

```bash
python scripts/validate-trigger.py <skill-dir>
```

- 激活率 < 80% → 回改 description，补关键词或同义词
- 误激活 → 补负面触发词
- 漏激活 → 补同义词与触发短语

## 示例

Input: 「帮我写一个处理 PDF 的 skill」
Output: 先读 Luzzy-Skill Architect → 走 Phase 1 六问（任务、触发词、类型、是否需要 scripts/references、是否属于 skill family、完成标准）→ 确认 profile card → Phase 2 设计目录树 → Phase 3 按触发优先写 description → Phase 4 跑 validate-trigger.py → 报告激活率

Input: 「这个 skill 老是误触发，帮我看看」
Output: 读 Architect 的 anti-patterns → 判定为 AP-5（缺负面触发词）→ 在 description 补 `Do NOT use for ...` → 重跑 validate-trigger.py 对比激活率

## 边界

- 本 skill 只管 **skill 本身的工程质量**；具体技能内容（如前端设计怎么做）由对应 skill 负责
- 涉及本仓库的 Git 操作 → 走 `luzzycode-git`
