---
name: luzzycode-workspace
description: >
  Use when starting a task in a repository, cleaning up temporary artifacts, or
  closing out a session's workspace.
  Handles pre-work git status triage, temp artifact destinations, file naming
  discipline, the end-of-task cleanup checklist, dirty-workspace handling, and
  the authorization boundary for deletion.
  Triggers: "workspace is messy", "clean up", "git status", "leftover files",
  "temp files", "工作区", "清理", "临时文件", "收尾", "工作区乱了".
  Do NOT use for Git commit or push operations (see luzzycode-git), for deciding
  document content (see luzzycode-interaction), or for code style (see
  luzzycode-code).
---

# LuzzyCode · 工作区整理规范

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-workspace/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-workspace) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-workspace/SKILL.md)

## 三条基线

- 工作区是用户的，不是草稿纸——任何写入都要能回答三问：属于谁、放在哪、何时清理
- 只增不删不是整洁，是堆积；【本轮产物本轮清】，不留待下轮
- 整洁的验收标准是「新人看一眼 `git status` 就能看懂」，不是「文件都还在」

## 开工前

- 接手先看一眼 `git status`：分清「本轮会碰的」与「本来就脏的」，后者别动（处置见本节末尾）
- 先确认本轮产物该落在哪：仓库既有约定优先，没有才用下面的默认落点
- 大体积中间物（模型权重、数据集、构建缓存、安装包）**先定落点与 gitignore，再开始下载**——别下完才发现污染了仓库

## 落点纪律

- 临时产物【必须】投放到可识别落点：`logs/`、`archive/`、系统临时目录（`%TEMP%` / `$TMPDIR`）或 gitignore 覆盖区
- 【禁止在工作区散落无主文件】：`tmp1.json`、`test_copy/`、`output (2).txt`、`untitled.md`、`新建文本文档.txt` 这类一律不许出现
- 一次性脚本【不进仓库根目录】：确需保留就放 `scripts/` 并写清用途，否则用完即删
- 下载的压缩包、安装包、大体积中间物：落地即登记，用完立即删，【不留过夜】
- 落点服从仓库既有约定，【禁止平行落点】：已有 `docs/` 就不许再建 `notes/`、`.agent/`、`output/` 之类的第二套目录
- 构建产物、依赖缓存、本地配置、密钥文件所在目录，【必须】补进 `.gitignore`

## 命名纪律

- 文件名带用途（必要时带日期），禁 `新建`、`副本`、`final`、`最终版`、`(2)` 这类后缀
- 同一用途只保留最新一份，旧版进 `archive/`，【不并行堆叠】

## 收尾自检（任务结束前逐条过，漏一条不算交付）

- 我本轮创建的中间物都清了吗？（构建产物、缓存、下载包、一次性脚本、失败试验目录）
- `git status` 里有没有不该出现的新文件？逐个判定「该入库」还是「该删除」
- 新增产物目录是否已补进 `.gitignore`？
- 有没有留下空目录、空文件、半成品？
- 工作区是否【不比开工前更乱】？变乱了就当场收拾

## 脏工作区处置

- 开工即发现工作区已乱：先别动手清，告知用户「当前工作区有 N 个疑似遗留文件」，列清单问是否清理
- 授权边界：【只授权清理本轮自己创建的临时产物】——不是本轮造的、用户给的、版本控制跟踪的、来源不明的，一律先列清单问用户
- 清理动作【可逆优先】：先删可重建的产物，可能有用的一律移入 `archive/` 而不是直接删
- `archive/` 只进不出；版本控制跟踪的目录【永不代为清理】

## 何时写文档

- 判断标准：下个会话需要它吗？该写——决策与理由、调研结论与来源、环境与踩坑、代码里读不出来的约定；不写——过程流水账、代码本身能回答的东西
- 【优先追加，不新开】：能在既有文档里续写就续写；确需新开前，先确认既有文档里没有它的位置
- 默认文档族（仓库无约定时才用）：`PLAN-<范围>.md`、`RESEARCH-<主题>.md`、`STATUS-<范围>.md`、`WORKLOG.md`、`archive/`；调研类文档带来源与置信度
- 与「边界三档」的分工：那里禁的是「未经要求的成品文档」，本节管的是「后续工作必需的过程留痕」

## 示例

Input: 跑完测试，工作区多了 `coverage/` 和 `test_copy/`
Output: `coverage/` 是可重建构建产物 → 删除并补进 `.gitignore`；`test_copy/` 是本轮试验目录 → 删除。工作区回到开工前状态

Input: 接手时 `git status` 显示 5 个来源不明的文件
Output: 不擅自清理 → 告知「当前工作区有 5 个疑似遗留文件」并列出 → 问用户是否清理

## Verify

- 收尾自检五项是否逐条过？（中间物 / git status / gitignore / 空目录 / 不比开工前更乱）
- 清理动作是否只涉及本轮自己创建的产物？
- 可能有用的是否移入 `archive/` 而非直接删？

