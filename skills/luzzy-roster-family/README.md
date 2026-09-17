# Luzzy Roster Skill Family — 生成规范

本目录下的 `luzzy-roster-*` 系列 skill 由同一份生成规范产出，共享同一骨架。每个 skill 对应 `prompt/Luzzy.md` §1.1.6 十七类清单中的一个**独立类目**（设计类的三个框架子项与学术格的两组各自分裂为独立 skill，共 21 个）。

## 共同约定

- **职责**：装该类目的仓库子项明细（URL、条数、读什么、安装坑位、体积与许可警示）与**操作性执行细则**（工具面、命令族、安装差异、失败路径——2026-09-18 从提示词 §十四 迁入，各 skill 以「执行细则」节承载，提示词原位留一行指向）
- **不装**：阅读规则（提示词 §1.1.3）、门与回执（§1.1.1–1.1.2）、分诊（§1.1.5）、触发口径（§1.1.8）、纪律 / 红线 / 验收标准（提示词 §十四）——这些只住提示词，本家族一律不复制
- **frontmatter 模板**：`name: luzzy-roster-<slug>`；description 结构为 `Use when the Luzzy checklist (必读清单) hits the <中文名> category ... Answers "<触发引语>" ... Do NOT use for ...`
- **triggers.json**：每家 5–10 条，正例覆盖该类目的真实问法，负例覆盖相邻类目（防止误激活）
- **校验**：`python skills/luzzy-skill-architect/scripts/validate-trigger.py skills/luzzy-roster-<slug>`，激活率须 ≥80%

## 目录清单（21 个）

| slug | 类目 | 条数口径 |
|---|---|---|
| backend | 后端 / 通用编码 | 3 全读 |
| design | 设计类（基线五条） | 5 全读 |
| design-compose | 设计类子项 · Compose | 3 全读（与 design 叠加） |
| design-vue | 设计类子项 · Vue | 3 全读（与 design 叠加） |
| design-react | 设计类子项 · React | 3 全读（与 design 叠加） |
| office | 文档 / Office 文件 | 1 全读 |
| ppt | 做 PPT / 演示文稿 | 3 全读 |
| writing | 文档编写 / 写作 / 文案 | 2 全读 |
| html | HTML / 网页开发 | 7 取 4 |
| windows | Windows 系统修复 / 优化 | 3 全读 |
| planning | 项目规划 / 需求拆解 | 4 全读 |
| code-review | 代码审查 | 4 全读 |
| reverse | 逆向 / 授权渗透 / 安全研究 | 2 全读（reverse 路由包 + 本地 zip-password-recovery） |
| assets | 素材 / 图标 / 组件库 | 4 全读 |
| android | Android 开发 / 模拟器 | 6 取 4 |
| mcp | MCP 开发 / 接入 / 维护 | 6 取 4 |
| skilldev | Skill 开发 / 编写 / 管理 | 1 全读 |
| browser | 浏览器自动化 / 网页操作 | 3 全读 |
| bilibili | B 站视频转笔记 | 1 全读 |
| academic | 学术研究 / 论文撰写 | 4 全读 |
| problem-solving | 学科题目解答 / 解题方法论 | 3 全读 |

## 变更登记

子项明细的增删改记录在 [references/checklist-history.md](references/checklist-history.md)（本家族共享一份）。修链接只改对应 roster skill；改条数 → 提示词 §1.1.6 主表同步。新增类目（第十八类）属于提示词级变更：先改提示词，再建对应 roster skill。

**更名 roster（改 slug）时的硬要求**：① 全仓 grep 旧 slug（`prompt/`、`README.md`、本目录），应零命中后才算完成——提示词里最易漏的位置是 §1.1.8 触发口径与 §十四 的行内引用；② 同步本文件上方 slug 表与目录名；③ 同步 harness 已装副本（删旧装新）。改完后按 AGENTS.md 第四节「交叉引用」行做三方比对（行内引用 / 目录名 / 本表）。