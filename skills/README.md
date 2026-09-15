# Luzzy 配套 skill

本目录是 [Luzzy](../README.md) 的配套技能层。提示词 [`prompt/Luzzy.md`](../prompt/Luzzy.md) 负责**每轮都生效的硬规定**，本目录负责**命中特定场景才需要的操作细则**——两层分工，规则不重复。

命中场景时，提示词 §1.1 的必读清单会指向这里的本地路径；本机已有就直接读，不必联网。

## 技能一览

| 技能 | 用途 | 何时触发 | 许可 |
|---|---|---|---|
| [`luzzy-skill-architect/`](luzzy-skill-architect/) | 创建、审计、诊断、融合 Agent Skills 的元框架：PPER 协议 + 五阶段生命周期 + L0–L5 成熟度 + 七设计模式 + 十反模式库 + 质量门禁 | 创建 / 改进 / 审计 skill，写 `SKILL.md`，校验触发词，评估成熟度，融合多个 skill | Apache-2.0 |
| [`luzzy-skill-meihuayishu/`](luzzy-skill-meihuayishu/) | 梅花易数技能家族（L5）：零依赖起卦引擎 + 《周易》《梅花易数》原文内置 + 原书占例回归 16/16 | 用户要算卦、起卦、占卜、用名字 / 时间 / 报数起卦 | MIT |
| [`luzzy-bilibili-notes/`](luzzy-bilibili-notes/) | 把 B 站视频提取成结构化 Markdown 笔记：默认抓标题、简介、AI 字幕、全部公开评论（含二级回复）四项，解析 SRT，重组章节 | 用户给 B 站链接要提取内容、转笔记、转文档、抓字幕、看简介与评论 | MIT |

## 安装到某个 Agent

三种方式，按需选一种：

```bash
# 1) 直接用（推荐）：把本仓库克隆到工作区，提示词里的清单会指向 skills/<名>/
git clone git@github.com:LuzzyMeow/Luzzy.git

# 2) 装进该 Agent 的用户级 skill 目录（以 Claude Code 为例）
cp -r Luzzy/skills/luzzy-skill-architect ~/.claude/skills/

# 3) 装进跨平台目录（Codex / OpenClaw 等认这个）
cp -r Luzzy/skills/luzzy-bilibili-notes ~/.agents/skills/
```

各家 harness 的 skill 目录与 MCP 配置路径速查，见 [`AGENTS.md`](../AGENTS.md) 第七节。

## 维护须知

- **`luzzy-skill-meihuayishu/` 自带维护宪章**：[`AGENTS.md`](luzzy-skill-meihuayishu/AGENTS.md)。它规定了十条红线（经典文本不可改写、计算一律走引擎、回归门槛不可放宽等）与四类变更流程。**改动该技能前必须先完整读它**，并跑通三条回归命令：

  ```bash
  cd skills/luzzy-skill-meihuayishu
  python evals/integrity_check.py    # 结构完整性 + 版本四处一致
  python evals/run.py                # 16 组回归用例（含五个原书占例）
  python lunarcal.py --selftest      # 34 项历表锚点
  ```

- **`luzzy-skill-architect/` 自带触发校验**：

  ```bash
  python skills/luzzy-skill-architect/scripts/validate-trigger.py skills/<技能目录>
  ```

- **新增配套 skill**：按 `luzzy-skill-architect` 的质量门禁产出（`name` 与目录名一致、`description` 只写触发条件含负面触发词、正文 ≤500 行、≥2 组 I/O 示例、含 `Verify` 段），并在本文件与提示词 §1.1 的清单里登记。

## 来源与许可

前两个技能原为独立仓库，2026 年迁入本仓库统一维护，原仓库已删除；迁移保持内容原样，仅改写指向旧仓库的路径引用，各技能的 `README.md` 保留其历史说明。

| 技能 | 原仓库 | 许可 | 要求 |
|---|---|---|---|
| luzzy-skill-architect | `LuzzyMeow/Luzzy-Skill-Architect` | Apache-2.0 | 保留 `LICENSE` 与版权声明 |
| luzzy-skill-meihuayishu | `LuzzyMeow/Luzzy-Skill-MeiHuaYiShu` | MIT | 保留 `LICENSE` 与版权声明 |

各技能的 `LICENSE` 随目录保留，未做改动。`luzzy-skill-meihuayishu` 内置的经典文本均为公有领域（作者逝世逾百年），历法数据表为社区公开成果，出处见其 `references/sources.md`。
