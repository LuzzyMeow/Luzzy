---
name: luzzycode-ppt
description: >
  Use when producing a presentation, slide deck, keynote, pitch deck, sharing
  session, or report deck, including requests for 演示文稿, 幻灯片, slides, deck,
  or a launch-event style page.
  Handles selection among the three PPT skills (Guizang / Dashi / HTML PPT
  Studio), whole-repository installation, and acceptance of the delivered deck.
  Triggers: "make a PPT", "make slides", "pitch deck", "keynote", "presentation",
  "做 PPT", "演示文稿", "幻灯片", "汇报材料", "分享稿", "路演材料".
  Do NOT use for reading or editing an existing .pptx file as a file (see
  luzzycode-office), for general HTML pages (see luzzycode-webdev), or for
  visual style decisions on a page (see luzzycode-design).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "presentation"
---

# LuzzyCode · 做 PPT

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-ppt/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-ppt) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-ppt/SKILL.md)

## 硬性前置：先读工具正文

用户说「做 PPT」「演示文稿」「幻灯片」「slides」「deck」「keynote」「分享稿」「汇报材料」「发布会风格页面」，**全部算**做 PPT。**三家全部读完**（3 条 ≤4，按常驻 §1.1 不折减）——读懂三家差异才谈得上择优；**安装按需求择一，不要三家全装**。口径见常驻提示词 §1.1。

**读取顺序**：本机 skill 目录已有就用加载工具按精确名字读 → 没有就整仓安装并读 `SKILL.md` 正文 → 主域不通走镜像（常驻 §1.2）→ **全部失败【立即上报失效链接】**，再按 §五 澄清，确认用户是否接受用模型自身能力直接产出 HTML 版。

| skill | 星数 | 风格与能力 | 何时选它 |
|---|---|---|---|
| [归藏PPT](https://github.com/op7418/guizang-ppt-skill) | 26.2k | 横向翻页**单文件 HTML**；两套视觉系统（电子杂志×电子墨水 / 瑞士国际主义）；WebGL 背景、演讲者模式、观众屏同步、讲稿备注、多平台封面 | 要**设计感强**的演讲/发布会风格，或明确说「杂志风」「瑞士风」 |
| [大狮PPT](https://github.com/chuspeeism/dashi-ppt-skill) | 8.1k | 12 套主题 × 1020 版式；浏览器内**自带编辑控制台**（改字、换图、拖滑杆调模块）；**导出 PPTX / PDF / HTML 离线包** | 需要**交付 .pptx / .pdf 文件**，或用户要拿到手自己再改 |
| [HTML PPT Studio](https://github.com/lewislulu/html-ppt-skill) | 8.3k | 模板驱动：36 主题 × 36 布局 × 47 动画（27 CSS + 20 Canvas）× 15 完整 deck + 演讲者模式 | 要**快速出量**、需要挑主题与布局，或做小红书图文一类多图排版 |

**分工边界**：读取或编辑**已有的 .pptx 文件**走 skill `luzzycode-office`（OfficeCLI）；本 skill 管**从零产出一份 deck**。

## 选择纪律

1. **用户指定了风格或格式 → 直接选对应那家**。说不清 → 按常驻提示词 §五 澄清，问「要单文件网页 PPT，还是要能导出 pptx / pdf？」
2. **不要三家全装**。先查本机已装哪家，缺哪家再装哪家。
3. **必须整仓安装**：三家的正文都依赖 `assets/` `references/` `templates/` `scripts/` 等资源目录，**只抓 `SKILL.md` 单文件拿不到可用能力**。
4. 安装前先读该仓库 `README` 的安装章节，**按 README 的命令装**，不要自己发明命令。
5. 克隆走常驻提示词 §1.2：优先 SSH；连不上再用 `gh-proxy.com` / `ghfast.top` 代理。

## 安装要点（各家差异）

| skill | 正文在哪 | 安装命令 | 坑 |
|---|---|---|---|
| 归藏PPT | 仓库根 `SKILL.md` | `npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill` | 装完确认 `SKILL.md` `assets/` `references/` 三项都在 |
| 大狮PPT | **在 `skills/dashi-ppt/` 子目录**，不在仓库根 | `npx dashi-ppt-skill@latest`（国内加 `--registry=https://registry.npmmirror.com`） | 需 **Node.js 20+**；导出 PPTX/PDF 需本机有 Chrome / Chromium / Edge |
| HTML PPT Studio | 仓库根 `SKILL.md` | `npx skills add https://github.com/lewislulu/html-ppt-skill` | 运行时需要 `SKILL.md` `assets/` `templates/` `references/` `scripts/`；`docs/` 约 4.6MB，离线副本可删 |

离线或装不上时的兜底：**skill 就是一个含 `SKILL.md` 的目录**，`git clone` 后把**含正文的那一层**拷进 agent 扫描的 skills 目录（`~/.dsh/skills/`）——归藏与 HTML PPT Studio 的正文在仓库根，直接拷仓库；**大狮的正文在 `skills/dashi-ppt/` 子目录**，要拷的是那一层，拷完目标目录下必须能直接看到 `SKILL.md`。拷完用文件工具确认 `SKILL.md` 在位；**确认失败就别硬用**，退回 `npx` 安装命令，或向用户说明这一家装不上、改用另外两家。

## 交付标准

1. **产物能直接打开**：单文件 HTML 双击可看，不需要起服务器；给了导出文件就给出文件路径
2. **必须亲眼看**：用浏览器或图像读取工具（如 `read_image`）看过实际渲染，不要只读代码推断（常驻提示词 §十）
3. **不要溢出版面**：逐页检查文字溢出、底部留白、标题被导航条遮挡。归藏与大狮都带校验脚本，能跑就跑
4. **图片进槽位**：配图按模板预留比例生成，且**不要把页脚、标题、页码、角标画进图片里**
5. **页数受控**：用户没指定时，先给页数方案再生成，不要一上来铺 30 页
6. **导出格式对齐需求**：用户要的是 `.pptx` 就给 `.pptx`，不要拿 HTML 顶替

## 示例

Input: 「帮我把这篇文章做成一份 PPT」
Output: 先问「要单文件网页 PPT，还是要能导出 pptx/pdf？」+ 页数与受众 → 选定一家 → 读该仓库 README 安装章节 → 整仓安装 → 读 `SKILL.md` 走它的工作流 → 生成 → 浏览器打开逐页看 → 截图核对溢出 → 交付

Input: 「做一份 8 页的技术分享 slides，赛博朋克风」
Output: 风格与页数都明确 → 选 HTML PPT Studio（36 主题里有 `cyberpunk-neon`）→ 整仓安装 → 读 `SKILL.md` 与 `references/themes.md` → 从 `tech-sharing` 模板起手 → 逐页渲染核对 → 交付

Input: 「做份融资路演材料，我要能改的 pptx」
Output: 明确要 pptx + 需要自己再改 → 选大狮PPT → 确认本机 Node 20+ 与 Chrome → 安装 → 读 `skills/dashi-ppt/SKILL.md` → 生成 → 导出 pptx → 打开导出文件确认可编辑 → 交付（同时给 HTML 版便于继续改）

Input: 「把这份别人发我的 .pptx 改一下」
Output: 这是**改文件**不是做 deck → 转 skill `luzzycode-office`，读 OfficeCLI

## Verify

- 动手前：该读的那一家 `SKILL.md` 正文读到了吗？不是只看 README 摘要吧？
- 是**整仓**装的吗？`assets/` `references/` `templates/` 在位吗？
- 大狮那条：Node 版本够 20 吗？导出用的浏览器在吗？
- 产物真的打开看过吗？逐页查过溢出与遮挡吗？用 `read_image` 或浏览器确认过吗？没看就明说「未做视觉验收」
- 用户要的格式给了吗？要 pptx 有没有给成 HTML？
