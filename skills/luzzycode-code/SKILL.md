---
name: luzzycode-code
description: >
  Use when writing, refactoring, or reviewing code and needing LuzzyCode's
  concrete code standards — naming, control flow, comments, tests, output format.
  Handles naming conventions, guard-clause preference, nesting limits, exception
  handling rules, comment policy, test requirements, and code-first output.
  Triggers: "naming convention", "add tests", "refactor this", "fix this bug",
  "code style", "变量命名", "加测试", "重构", "写代码规范".
  Do NOT use for Git or GitHub operations (see luzzycode-git), for design or UI
  work (see luzzycode-design), or for the mandatory Ponytail / spec-kit /
  mattpocock reads themselves — those are hard rule §1.1.
---

# LuzzyCode · 代码细则

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-code/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-code) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-code/SKILL.md)

**硬性前置**：开发任何代码类任务前，必须完整阅读 **三项** skill —— **Ponytail** `https://github.com/DietrichGebert/ponytail`、**spec-kit** `https://github.com/github/spec-kit`、**mattpocock/skills** `https://github.com/mattpocock/skills`（口径与读取顺序见常驻提示词 §1.1）。本节是它们之外的项目级细则。

## 最小改动
- 只改必须改的；不顺手重构、不加未要求的功能、不写投机性防御代码
- 删除优于新增，无聊优于聪明

## 可直接运行
- 补齐 import、依赖与端点；从零建项目附依赖清单与 README

## 先读后写
- 先看邻近代码的命名、库与模式再动笔
- 不确定库是否可用时先查项目依赖清单，【绝不假设知名库就存在】

## 命名
- 函数用动词短语、变量用名词短语
- 禁 1-2 字符命名（循环变量除外）
- 禁无意义缩写（`genYmdStr` → `generateDateString`）

## 控制流
- guard clause 优先，先处理错误与边界
- 嵌套不超过 2-3 层
- 【绝不 catch 而不处理】——要么处理、要么记录、要么上抛，不许吞异常

## 注释
- 默认不写；确需注释只解释「为什么」，一行以内
- 【禁止 TODO 注释】——要么实现，要么提给用户
- 留下有已知天花板的有意简化时，用 `ponytail:` 注释写明天花板与升级路径

## 测试
- 改动涉及逻辑时补测试；跑通全部测试再报完成
- 测试失败根因默认在代码而非测试，修根因不压制报错
- 非平凡逻辑（分支 / 循环 / 解析 / 金额 / 安全路径）留一个能跑的检查（assert 自检或一个小测试）；平凡一行代码不需要

## Git

Git 与 GitHub 操作（SSH 优先、remote 纠正、提交卫生、推送排障）见 skill `luzzycode-git`。

## 输出格式
- 代码优先，其后最多三行说明跳过了什么、什么时候需要补
- 解释比代码长就把解释删掉

## 示例

Input: 需要在订单列表里按状态筛选
Output: 复用既有 `filterBy()` helper 加一个 `status` 分支；不新建 `FilterService` 类

Input: 修「用户列表偶尔显示旧数据」的 bug
Output: 先 grep 所有调用方 → 发现 3 处共用 `fetchUsers()` → 在 `fetchUsers()` 内修缓存失效，而非在 3 个页面各加一次

## Verify

- 改动涉及逻辑 → 跑通全部测试再报完成
- 非平凡逻辑 → 留下至少一个可运行的检查（assert 自检或小测试）
- 提交前 → `git status` 确认无无主临时文件
