# Family 说明（非 skill 目录）

`luzzy-roster-family/` 是 **roster 家族的登记与规范目录，本身不是 Agent Skill**——十七类清单的 21 个分 skill 与它平级，各自独立放在 `skills/` 下。这个目录存放：

- `README.md`：家族生成规范与 21 个成员的目录清单
- `references/checklist-history.md`：子项变更登记（家族共享一份）

不设 `SKILL.md` 是有意的：家族规范是给**维护者**看的（何时建新 roster、怎么登记变更），不是给运行中的 agent 消费的操作细则——后者由每个 roster skill 自己承载。把它做成 skill 反而会造出「要读 roster 才知道要读哪个 roster」的循环依赖（提示词 §14.14 的分层归属原则）。