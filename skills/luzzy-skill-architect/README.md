# Luzzy-Skill-Architect

> 元技能架构师 — 创建、诊断、升级 Agent Skills 的全生命周期工程工具。

遵循 [agentskills.io](https://agentskills.io/specification) 开放标准，内建 PPER 思考协议（CoT+ReAct），覆盖从零创建到成熟度评估的完整技能工程方法论。

---

## 快速开始

本技能随 [Luzzy](https://github.com/LuzzyMeow/LuzzyPrompt) 分发，位于该仓库的 `skills/luzzy-skill-architect/`，无需单独克隆。原独立仓库已删除，本文件保留其历史说明。

安装到某个 Agent（以 WorkBuddy 为例，其他平台参见下方兼容性列表）：

```bash
# 从 Luzzy 仓库取本技能
cp -r LuzzyPrompt/skills/luzzy-skill-architect ~/.workbuddy/skills/

# 运行自验证
python scripts/validate-trigger.py .
```

支持的 Agent 平台：WorkBuddy、Claude Code、VS Code Copilot、Cursor、Gemini CLI、OpenAI Codex、Windsurf 等。各平台技能安装路径参见 [references/ecosystem-map.md](references/ecosystem-map.md)。

---

## 核心能力

| 维度 | 内容 |
|------|------|
| **思考协议** | PPER（Perception → Planning → Execution → Reflection）固定执行引擎 |
| **五阶段流程** | 理解意图 → 结构设计 → 撰写产出 → 验证触发 → 迭代打磨 |
| **技能融合** | 2+技能合并为 Skill Family，1+1≥2保障，四维准入评估，三层融合场景，自更新机制 |
| **成熟度模型** | L0-L5 六级阶梯，带完整升级路径 |
| **设计模式** | 七种可复用模式（Trigger-First / Progressive Disclosure / Domain Variant / Workflow Chain / Tool Augmentation / Template Factory / Skill Fusion） |
| **反模式库** | 十种常见错误，每个含 Before/After 案例 |
| **质量门禁** | 五个阶段 × 多层硬性检查清单 |
| **生态决策** | Skill vs CLAUDE.md vs MCP vs Rules 定位指南 |
| **评测体系** | L1 触发测试 + L2 单次执行 + L3 批量评测（evals.json） |

---

## 目录结构

```
Luzzy-Skill-Architect/
├── SKILL.md                          # 入口：PPER协议 + 五阶段流程 + 质量门禁
├── references/                       # 按需加载的参考文档
│   ├── maturity-model.md             # L0-L5 成熟度升级详解
│   ├── design-patterns.md            # 七种设计模式 + 决策树
│   ├── anti-patterns.md              # 十种反模式 + 修复案例
│   ├── ecosystem-map.md              # 技能 vs 其他 Agent 机制
│   ├── vendor-extensions.md          # 平台扩展字段参考
│   ├── evaluation-guide.md           # L3 批量评测体系
│   └── skill-fusion.md               # 技能融合方法论（准入评估/自更新）
├── assets/
│   ├── templates/                    # 技能骨架模板
│   │   ├── skill-basic.md            # L1 单文件技能
│   │   ├── skill-structured.md       # L2-L3 带拆分技能
│   │   └── skill-family.md           # L5 编排型技能家族
│   └── protocols/                    # 思考协议模板
│       ├── pper-protocol.md          # 完整四阶段协议
│       ├── otav-protocol.md          # 轻量 Observe-Think-Act-Verify
│       └── react-protocol.md         # 探索型 Thought-Action-Observation
└── scripts/
    ├── validate-trigger.py           # L1 触发词自动验证
    ├── fusion-analyzer.py            # 融合兼容性自动评分
    └── check-updates.py              # 源仓库更新检测
```

---

## 使用示例

### 创建新技能

```
User: "帮我创建一个数据库迁移技能"
→ Luzzy-Skill-Architect 激活
→ Phase 1-2: 意图捕获 + 结构设计
→ Phase 3: 产出 db-migration/SKILL.md + references/{postgres,mysql}.md
→ Phase 4: 验证 description 触发准确率
→ Phase 5: 迭代至 L3 成熟度
```

### 审计现有技能

```
User: "审查我的 deploy 技能"
→ 反模式检测：发现 description 泄露执行步骤（AP-1）
→ 成熟度诊断：当前 L1，可升级至 L3
→ 给出具体修复方案和目录重组建议
```

### 融合技能

```
User: "把我的 code-review 和 test-runner 合并成一个 PR-check 技能"
→ Phase 2.5 融合分析：四维评分 100/100 → VERDICT: STRONG
→ 生成 pr-checks/ 编排器 + 保留子技能完整目录
→ 记录源仓库地址，启用自更新机制
```

---

## 设计哲学

- **标准优先**：仅依赖 agentskills.io spec 的六个标准字段，vendor 扩展作为知识附录
- **结构驱动**：先设计目录树，再写 SKILL.md — 不生成不能解释存在理由的目录
- **自指涉示范**：本技能自身完美遵循它所教授的所有原则（description 纯触发词、body 密集格式 ≤500 行、渐进式加载 references/）
- **渐进式指导**：不假设用户背景，在流程中自然教授渐进式加载、description trigger 理论、token 预算等概念

---

## 参考源

| 项目 | 链接 |
|------|------|
| agentskills.io 规范 | https://agentskills.io/specification |
| anthropics/skills | https://github.com/anthropics/skills |
| agentskills/agentskills | https://github.com/agentskills/agentskills |
| Claude Code Skills 文档 | https://code.claude.com/docs/en/skills.md |
| Agent Skills 101 教程 | https://blog.serghei.pl/posts/agent-skills-101/ |
| 嵌套技能讨论 (#137) | https://github.com/agentskills/agentskills/issues/137 |

---

## 兼容性

- **目标平台**：完全跨平台 spec-level
- **规范版本**：agentskills.io 开放标准
- **依赖**：`skills-ref`（可选，用于格式验证）；Python 3.8+（可选，用于触发词脚本）
- **支持的 Agent 平台**：WorkBuddy、Claude Code、VS Code Copilot、Cursor、Gemini CLI、OpenAI Codex、Windsurf 等

## 贡献

欢迎通过 Issue 和 PR 参与改进：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 确保通过自验证：`python scripts/validate-trigger.py .`
4. 遵循本项目的[设计哲学](#设计哲学)和[反模式规范](references/anti-patterns.md)
5. 提交 PR 并描述改动

提交前请确认未引入新的反模式。

## License

Apache 2.0 — 详见仓库中的 LICENSE 文件（若未包含，请参考 https://www.apache.org/licenses/LICENSE-2.0）。
