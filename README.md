# LuzzyCode

鹿溪（Coding 模式）——一份可拆装的编码 Agent 提示词预设，采用**常驻层 + 按需 skill 层**的分层设计。

## 这是什么

一套面向编码 Agent 的行为契约：把「必须每轮都生效的硬规定」留在常驻提示词里，把「命中场景才需要的细则」下沉为独立 skill，靠渐进披露按需加载——而不是把所有规则一次性压进上下文。

**核心设计**：约束密度直接决定遵守率。把 200+ 条常驻约束降到约 70 条，细则仍全部保留，只是改成用时才加载。

## 目录结构

```
.
├── prompt/
│   └── LuzzyCode.md          # 常驻提示词（约 9k token）
└── skills/                    # 按需加载的配套 skill
    ├── luzzycode/            # 编排器：路由表与冲突裁决（L5）
    ├── luzzycode-workflow/   # 任务清单 / 计划模式 / 目标工具 / 子代理与后台任务
    ├── luzzycode-code/       # 代码细则（命名 / 控制流 / 注释 / 测试）
    ├── luzzycode-git/        # GitHub 操作：SSH 优先 / 镜像中转 / 提交卫生
    ├── luzzycode-search/     # 联网检索细则（AnySearch 唯一通道）
    ├── luzzycode-memory/     # 记忆系统细则（MemOS）
    ├── luzzycode-bootstrap/  # 首次配置引导（免密钥应急通道）
    ├── luzzycode-tools/      # 工具选择 / 降级路径 / 交付登记
    ├── luzzycode-docs/       # 文档与写作（AI 腔清除）
    ├── luzzycode-office/     # Office 文件（.docx/.xlsx/.pptx）
    ├── luzzycode-design/     # 设计类任务执行细则
    ├── luzzycode-skills/     # Skill 工程（对接 Luzzy-Skill Architect）
    ├── luzzycode-workspace/  # 工作区整理规范
    └── luzzycode-interaction/# 汇报纪律与项目上下文
```

## 三条硬性规定

常驻层的最高优先级约束，**不因 skill 未加载而失效**：

1. **必读 skill** —— 五类任务各有指定 skill，必须完整读正文再动手：

   | 任务类型 | 必读 |
   |---|---|
   | 后端 / 通用编码 | [Ponytail](https://github.com/DietrichGebert/ponytail) · [spec-kit](https://github.com/github/spec-kit) · [mattpocock/skills](https://github.com/mattpocock/skills) |
   | 设计类（UI/动效/页面/交互） | 四项前端设计 skill（见 `prompt/LuzzyCode.md` §1.1） |
   | 文档 / Office 文件 | [OfficeCLI](https://github.com/iOfficeAI/OfficeCLI) |
   | 文档编写 / 写作 / 文案 | [stop-slop](https://github.com/hardikpandya/stop-slop) · [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) |
   | Skill 开发 / 编写 / 管理 | [Luzzy-Skill Architect](https://github.com/LuzzyMeow/Luzzy-Skill-Architect) |

   **任何一条指向失效 → 立即上报用户**，说明需要更新，然后按降级规则继续。

2. **GitHub 操作 SSH 优先** —— 一律用 `git@github.com:...`；`gh repo create` 默认给 HTTPS，建完立即 `git remote set-url` 纠正。国内网络受限时按 gh-proxy → ghfast → AnySearch 抓取 → Gitee 导入逐级降级（前两个经实测筛选）。

3. **联网检索唯一通道** —— 资料搜索、批量并行、垂直域定义、网页抓取**四条路由全部走 AnySearch**；用内置搜索做资料搜索、只在抓取时用 AnySearch 属于「半程合规」，视为违规。内置工具仅作回退且必须留痕。

## 零配置启动

本机未挂载 MemOS / AnySearch 时**不必先配 Key**——AnySearch 匿名通道足以完成检索与抓取：

```bash
curl -L -o anysearch-skill.zip https://github.com/anysearch-skill/anysearch-skill/archive/refs/heads/main.zip
unzip anysearch-skill.zip
python <skill_dir>/scripts/anysearch_cli.py search "关键词" --max_results 5
```

引导流程见 `skills/luzzycode-bootstrap/`：先用匿名通道干活 → 抓取官方文档自读 → 再指导用户配置两项 Key。

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
