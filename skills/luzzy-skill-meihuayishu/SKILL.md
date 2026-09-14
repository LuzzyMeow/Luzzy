---
name: luzzy-skill-meihuayishu
description: >
  Use when the user wants plum blossom (Meihua Yishu) divination by any method:
  name strokes, date/time, or number reporting. Handles intent routing, engine
  invocation, hexagram calculation, and structured interpretation with embedded
  classical sources. Use when the user says "算卦", "占卜", "起卦", "梅花易数",
  "帮我算一卦", "名字算卦", "时间起卦", "报数起卦", "算算感情", "测测运势",
  "起一卦", "占一占".
  Do NOT use for general I Ching philosophy, academic Zhouyi analysis, or
  Bazi/Six-Yao (六爻) divination.
license: MIT
compatibility: >
  requires: python>=3.8. Self-contained: engine.py / lunarcal.py / gua_index.json /
  references/ all live in this skill directory. On some platforms the family is
  mounted at /workspace/meihua/ — the same layout, different mount point.
metadata:
  version: "2.2.0"
  author: "软糖"
  category: "易学占卜"
  target-maturity: "L5"
  workspace:
    engine: "engine.py（本技能根目录；部署后即 /workspace/meihua/engine.py）"
    lunarcal: "lunarcal.py（同上）"
    gua_db: "gua_index.json（同上）"
    references: "references/（内置原文资料，离线优先）"
allowed-tools: Read Write Bash Skill WebSearch WebFetch
---

# 梅花易数 · Skill Family 编排者

统一梅花易数入口。识别起卦方式 → 调用本目录引擎 → 查内置卦爻辞（离线优先）→ 综合解卦并标注出处。

## 资料查阅优先级（强制）

解卦引文按以下顺序取材，逐级回退，禁止跳级：

1. **内置原文（离线，第一优先）**——本目录 `references/`：
   - `zhouyi-shangjing.md` / `zhouyi-xiajing.md`：周易 64 卦经文（卦辞+爻辞+用九用六）
   - `gua_index.json`：64 卦索引（卦名/卦画/上下卦/爻位/ctext 链接）
   - `meihua-juan1.md`~`juan3.md`：《梅花易数》全文（起卦法、体用总诀、断占总诀）
2. **联网双源验证**——仅在用户要求核对、或内置资料查不到所需条目时使用：
   - ctext.org（武英殿十三经注疏本）：`https://ctext.org/book-of-changes/{slug}/zhs`，slug 见 `gua_index.json` 的 `url` 字段
   - 维基文库（交叉第二源）：`https://zh.wikisource.org/zh-hans/周易` 对应卦页
   - 两源不一致时照录差异并告知用户，不得擅自取舍。
3. **回退清单**——仍查不到时按 `references/sources.md` 的站点梯次检索。

## 路由规则

| 用户输入特征 | 路由方法 | 读取子技能 |
|-------------|---------|-----------|
| 名字、姓名、笔画、字占 | 姓名笔画起卦 | `meihua-name-divination/SKILL.md` |
| 时间、日期、现在、今天、某年某月 | 时间起卦 | `meihua-time-divination/SKILL.md` |
| 数字、报数 | 报数起卦 | `meihua-baoshu-qigua/SKILL.md` |
| 物数、声音、方位见物、丈尺等古法 | 按原文起例 | 直接查 `references/meihua-juan1.md`（象数易理篇之一/二）照原文起卦，再回到本流程第 3 步 |
| 未指定方式 | 默认时间起卦（用当前时刻） | `meihua-time-divination/SKILL.md` |

## 执行流程

### 1. 识别方式，收集输入

- 姓名起卦：确认名字（简体/繁体原样），单人还是两人（两人各起或合字，须先问明）。
- 时间起卦：确认日期时间（默认当前时刻）。
- 报数起卦：请用户先静心想好所问之事，再报 2 或 3 个数。
- 任何方式都先确认**所问何事**；不因事不占（原文：不动不占，不因事不占）。

### 2. 调用本目录引擎（严禁手动计算）

统一用本技能根目录的 `engine.py`（部署环境中通常位于 `/workspace/meihua/`），禁止手动算余数、查八卦表：

```bash
# 报数起卦（2数：动爻=(数1+数2)÷6；3数：动爻=数3÷6）
python3 <技能根目录>/engine.py number <数1> <数2> [<数3>]

# 时间起卦（先用 lunarcal.py 换算四要素）
python3 <技能根目录>/lunarcal.py <年> <月> <日> <时> <分>
# 从输出提取：年支数、农历月数、农历日、时支数（默认农历月法，忠于原文）
python3 <技能根目录>/engine.py time <年支数> <月数> <农历日> <时支数>

# 笔画起卦（按字占规则分配上下卦笔画后传入）
python3 <技能根目录>/engine.py bihua <上卦总笔画> <下卦总笔画> [<动爻数>]
```

### 3. 解析引擎输出

引擎输出含：本卦（卦名/序/六爻）、动爻位置、变卦、互卦（上互/下互）、体卦/用卦（五行）、生克关系。向用户完整呈现这些字段。

### 4. 引经文（内置优先）

- 动爻爻辞：查 `references/zhouyi-{shangjing|xiajing}.md` 中本卦条目对应爻。
- 变卦卦辞：同文件中变卦条目的卦辞。
- 解卦方法论：体用生克查 `references/meihua-juan2.md`「体用总诀」；分类占断（婚姻/求财/疾病等）查同篇十八占；三要十应查篇三、篇四。
- 需在线验证时按上文「资料查阅优先级」第 2 级执行。

### 5. 综合解卦

四层叠加，逐层给出判断依据并标注引文出处（文件名+卦名+爻位）：

1. 体用生克：体宜受生比和，忌受克（卷二·体用总诀）
2. 动爻爻辞：先看《周易》爻辞以断吉凶（卷二·占卜总诀）
3. 互卦：事之中间
4. 变卦：事之终应

结尾提示：卦象为传统术数文化参考，不构成任何现实决策建议。

## 示例

**输入**：「帮我用报数起卦，问新项目能不能成，就报 7 和 8」
**执行**：确认问题 → `python3 engine.py number 7 8` → 引擎得 7=艮(上)、8=坤(下)、动爻=(7+8)÷6=15÷6余3，第三爻动，本卦山地剥之艮，互坤坤，体艮土用坤土比和 → 查内置周易剥卦六三爻辞「剥之，无咎」与艮卦卦辞「艮：艮其背，不获其身，行其庭，不见其人，无咎」→ 按 体用比和→爻辞→互变 顺序输出四层判断，标注出处，附文化参考提示。

**输入**：「2026 年 8 月 29 日 12 点 10 分起一卦问出行」
**执行**：`python3 lunarcal.py 2026 8 29 12 10` → 得年支午(7)、农历七月(7)、十七日(17)、时支午(7) → `python3 engine.py time 7 7 17 7` → 31÷8余7艮为上卦，38÷8余6坎为下卦，38÷6余2二爻动，山水蒙之山地剥，互见坤震（地雷复）→ 引蒙卦九二爻辞「包蒙吉；纳妇吉；子克家」→ 四层解卦并标注出处。

## Verify

- [ ] engine.py / lunarcal.py 成功执行（退出码 0）？
- [ ] 动爻、体用、互卦、变卦全部由引擎计算，未手动计算余数？
- [ ] 爻辞/卦辞引自内置 references/？联网仅为双源验证且有 ≥2 独立来源？
- [ ] 输出含四层判断，且每层标注出处（文件+卦名+爻位）？
- [ ] 已确认用户所问何事，并附「文化参考，非决策建议」提示？
