# LuzzyCode

鹿溪（Coding 模式）——一份可拆装的编码 Agent 提示词预设，采用**常驻层 + 按需 skill 层**的分层设计。

## 这是什么

一套面向编码 Agent 的行为契约：把「必须每轮都生效的硬规定」留在常驻提示词里，把「命中场景才需要的细则」下沉为独立 skill，靠渐进披露按需加载——而不是把所有规则一次性压进上下文。

**核心设计**：约束密度直接决定遵守率。把 200+ 条常驻约束降到约 70 条，细则仍全部保留，只是改成用时才加载。

## 目录结构

```
.
├── prompt/
│   └── LuzzyCode.md          # 常驻提示词（约 4.9k token）
└── skills/                    # 按需加载的配套 skill（合计约 10k token）
    ├── luzzycode-workflow/    # 任务清单 / 计划模式 / 目标工具 / 子代理与后台任务
    ├── luzzycode-tools/       # 文件与代码工具 / 命令执行 / 交付登记 / 降级路径
    ├── luzzycode-search/      # 联网检索细则（AnySearch 唯一通道）
    ├── luzzycode-workspace/   # 工作区整理规范
    ├── luzzycode-memory/      # 记忆系统细则（MemOS）
    ├── luzzycode-interaction/ # 汇报纪律与项目上下文
    ├── luzzycode-design/      # 设计类任务执行细则
    └── luzzycode-code/        # 代码与 Git 细则
```

## 两条硬性规定

常驻层的最高优先级约束，**不因 skill 未加载而失效**：

1. **必读 skill** —— 开发任何代码类任务前必须完整阅读 [Ponytail](https://github.com/DietrichGebert/ponytail)；设计类任务前必须完整阅读四项前端设计 skill（见 `prompt/LuzzyCode.md` §1.1）
2. **联网检索唯一通道** —— 资料搜索、批量并行、垂直域定义、网页抓取**四条路由全部走 AnySearch**；用内置搜索做资料搜索、只在抓取时用 AnySearch 属于「半程合规」，视为违规。内置工具仅作回退且必须留痕

## 使用方式

### 作为系统提示词
把 `prompt/LuzzyCode.md` 内容作为系统提示词注入，其余 8 个 skill 放入 Agent 的 skill 目录。

### 安装 skill
```bash
git clone https://github.com/LuzzyMeow/LuzzyCode.git
cp -r LuzzyCode/skills/* ~/.dsh/skills/      # DeepSeek Harness
# 或 ~/.claude/skills/ 、~/.agents/skills/ 等符合 agentskills 规范的目录
```

skill 采用标准 frontmatter 格式（`name` kebab-case + `description` 必填），已被 DSH 解析器逐条验证通过。

### 按需裁剪
8 个 skill 相互独立，可以只取需要的部分。常驻提示词里引用了它们，删除对应 skill 时建议同时删掉 §12.1 索引里的那一行。

## 分层预算

| 层 | 文件 | 行数 | 估算 token |
|---|---|---|---|
| 常驻 | `prompt/LuzzyCode.md` | 165 | ~4,900 |
| 按需 | 8 个 skill（合计） | 410 | ~10,050 |

典型编码任务加载常驻 + `luzzycode-workflow` + `luzzycode-code` ≈ 8,100 token；纯对话只付常驻的 4,900。

## 兼容性

- 提示词本身与 Agent 无关，可直接用作系统提示词
- skill 为通用 `SKILL.md` 格式，兼容 DSH、Claude Code、及符合 agentskills 规范的宿主
- 文档中提到的工具名（`todo_write`、`glob`、`present` 等）均为**能力示例**，预设要求 Agent 自行映射到本机真实工具，缺失时走降级路径

## 许可

见 [LICENSE](LICENSE)。
