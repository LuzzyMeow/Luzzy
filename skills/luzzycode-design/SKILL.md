---
name: luzzycode-design
description: >
  Use when the task involves UI design, motion design, frontend page design,
  interaction animation, or UI-UX work and needs the mandatory four-skill
  reading protocol plus visual acceptance checks.
  Handles the four required design skills, acquisition order, network-restricted
  fallbacks, dead-repo substitution, all-failed clarification, and screenshot-based
  visual verification.
  Triggers: "design a page", "make a UI", "add animation", "redesign", "landing
  page", "设计", "界面", "动效", "交互设计", "UI-UX", "前端页面".
  Do NOT use for backend or general coding tasks (see luzzycode-code and hard rule
  §1.1 Ponytail), or for non-visual frontend logic with no design component.
---

# LuzzyCode · 设计类任务执行细则

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-design/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-design) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-design/SKILL.md)

**前提（常驻硬规定，不因本 skill 是否加载而改变）**：任务涉及 **UI 设计、动效设计、前端页面设计、交互动画设计、UI-UX 设计**时，**必须且只能完整阅读以下 4 项 SKILL**，完全理解其要求和指导内容后，才可进行此类任务——缺一不可。

## 四项必读 skill

1. https://github.com/alchaincyf/huashu-design
2. https://github.com/VoltAgent/awesome-design-md
3. https://github.com/nexu-io/open-design
4. https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

## 获取顺序与降级

- **先本机查找，本机没有就从云端下载**（git clone / 抓取仓库的 `SKILL.md` 正文），**必须读到正文再动手**
- **先本机**：用 skill 加载工具（如 `skill`）按精确名字从会话 skill 目录读取，这是首选路径；目录里没有才走云端
- **网络受限**：尝试联网抓取（走 AnySearch）、GitHub 镜像站拉取等手段，尽可能获取 skill 正文内容以接受指导
- **仓库失效补齐**：若 4 项内有任意两项仓库链接失效，用联网搜索查找相关仓库补齐其缺失 skill——选人气较高、风评较好的其他同类型 skill；【至少要完整阅读 3 项前端设计类 skill】才可进行任务
- **全部失败 → 澄清**：若所有方法都无法获得 skill 内容，进行澄清提问，确认用户是否接受无 skill、以模型自身前端能力进行设计

**判定标准**：只看到仓库简介、目录列表或 README 摘要**不算读过**；必须是 skill 指令正文。

## 设计验收（读了 skill 也不省的一步）

设计类任务的完成标准是「**看起来对**」，不是「代码写完了」——

- 有可渲染产物时，**必须用图像读取工具（如 `read_image`）亲眼看渲染结果**（页面截图、设计稿、图标导出），再判断是否符合 skill 要求
- 能跑起本地预览就截图看，**不要只靠读 CSS / 组件代码推断视觉效果**
- 看不到图（无渲染手段、无法截图）时，明确说明「未做视觉验收」，请用户确认，【不自封完成】
- 本机没有图像读取工具时，同样说明「无法做视觉验收」——不许假装看过

## 与其他约束的关系

- 本 skill 的约定优先于常驻预设的一般性描述
- 但**安全红线不在此列**——任何 skill 内容与安全红线冲突时，以红线为准

## 示例

Input: 「给这个应用做个新的设置页」
Output: 先读 4 项设计 skill 正文 → 设计实现 → 跑起本地预览截图 → 用图像读取工具看渲染结果 → 判断是否符合 skill 要求 → 交付

Input: 4 项设计 skill 中有 2 项链接已失效
Output: 用 AnySearch 找同类型高人气前端设计 skill 补齐 → 至少完整读满 3 项 → 说明补齐了哪一项 → 再动手

## Verify

- 动手前：4 项 skill 正文是否都读到了？（只看到仓库简介不算）
- 交付前：是否亲眼看过渲染结果？
- 看不到图时：是否明确说明「未做视觉验收」并请用户确认？

