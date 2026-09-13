---
name: luzzycode-office
description: >
  Use when reading, editing, generating, or batch-processing Office files —
  .docx, .xlsx, .pptx — or when automating Word/Excel/PowerPoint workflows.
  Handles the mandatory OfficeCLI skill requirement, format-specific pitfalls, and
  verification of produced files.
  Triggers: "Word doc", "Excel file", "PowerPoint", "edit this spreadsheet",
  "generate a report doc", "docx", "xlsx", "pptx", "Office 文件", "表格",
  "幻灯片", "文档批处理".
  Do NOT use for Markdown or plain-text documents (see luzzycode-docs), for PDF
  handling unless OfficeCLI covers it, or for reading source code.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "document-io"
---

# LuzzyCode · Office 文件处理

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-office/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-office) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-office/SKILL.md)

## 硬性前置：必须先完整阅读 OfficeCLI

**任何涉及 .docx / .xlsx / .pptx 的读取、编辑、生成、自动化任务之前，必须完整阅读**：

**OfficeCLI** —— https://github.com/iOfficeAI/OfficeCLI

**触发口径（全部算）**：Word / Excel / PowerPoint 文件的读取、编辑、生成、批量处理、格式转换、内容提取、模板填充。

**读取顺序**：
1. 先用 skill 加载工具按精确名称从会话 skill 目录读取（首选）
2. 目录里没有 → 从上述仓库读取 `SKILL.md` 正文
3. 都不行 → AnySearch 抓取 / §1.2 镜像中转
4. **全部失败 → 立即上报用户该指向失效**，再按下方兜底

**判定标准**：只看到仓库简介或 README 摘要**不算读过**；必须是 skill 指令正文。

## 为什么必读

Office 文件是**二进制封装格式**，不是纯文本。直接用文本工具读写会损坏文件结构。OfficeCLI 是专为 agent 设计的 Office 套件——单二进制、无需安装 Office，覆盖 Word / Excel / PowerPoint 的读写与自动化。它给出了正确的调用方式与各格式的坑位说明。

## 通用纪律

- **先备份再改**：修改既有 Office 文件前，先复制一份；破坏性改动前告知用户
- **不猜格式细节**：样式、公式、合并单元格、图表这类结构，以 OfficeCLI 的说明为准，不凭经验推断
- **产出必须验证**：生成的 `.docx` / `.xlsx` / `.pptx` 要**回读一次**确认能正常打开、内容正确——不能只看命令返回成功
- **大文件注意体量**：Office 文件可能很大，读取时优先取所需范围而不是整份载入上下文
- **不把二进制内容塞进上下文**：用工具读取结构化的内容，不要 cat 原始字节

## 与其他 skill 的分工

| 场景 | 走哪 |
|---|---|
| 写 Markdown / README / 报告文本 | `luzzycode-docs` |
| 生成的是 `.docx` / `.xlsx` / `.pptx` | 本 skill |
| 写代码去读写 Office 文件 | 编码类必读（§1.1）+ 本 skill |

## 示例

Input: 「把这份 xlsx 里的空白行删掉」
Output: 先读 OfficeCLI → 备份原文件 → 按 OfficeCLI 方式读取并定位空白行 → 删除 → 回读验证行数与内容 → 交付

Input: 「根据这份数据生成一份 Word 报告」
Output: 先读 OfficeCLI → 确认模板或结构要求（有歧义按 §五 澄清）→ 生成 .docx → 回读验证能打开且段落正确 → 交付

## Verify

- 动手前：OfficeCLI 正文是否读到了？
- 改前是否备份了原文件？
- 产出是否**回读验证**过（能打开、内容对）？
- 是否避免把二进制内容直接塞进上下文？
- 破坏性操作前是否告知了用户？
