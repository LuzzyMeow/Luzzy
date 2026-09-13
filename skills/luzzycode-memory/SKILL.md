---
name: luzzycode-memory
description: >
  Use when retrieving, writing, deleting, or giving feedback on cross-session
  memory, or when operating on a knowledge base.
  Handles memory retrieval timing, write-worthiness judgment, environment
  annotation format, the four-step memory safety check, knowledge base document
  operations, and deletion plus feedback flow.
  Triggers: "remember this", "what do you know about me", "last time we",
  "forget that", "knowledge base", "记忆", "记一下", "上次说的", "删除记忆", "知识库".
  Do NOT use for web search or page fetching (see luzzycode-search), for general
  note-taking inside a repository, or for documenting decisions in project files
  (see luzzycode-interaction).
---

# LuzzyCode · 记忆系统细则

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-memory/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-memory) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-memory/SKILL.md)

**前提（常驻硬规定）**：动手前必检索、收尾必写入，不许跳过；本机未挂载时说明「记忆能力不可用」再继续其余工作。工具名仅为示例，以本机实际暴露的工具为准。

## 能力清单

- **检索记忆**（如 `search_memory`）：query 用当前话题的**简洁主题关键词**（对日期不敏感，别用日期当关键词）；提到知识库但未给 ID 时 knowledgebase_ids 传 `["all"]`
- **写入记忆**（如 `add_message`）：把本轮用户消息与你的回答一起写入
- **读取用户画像**（如 `get_user_profile`）：回答「我是谁」「你知道我什么吗」类问题时调用，与检索记忆配合
- **删除记忆**（如 `delete_memory`）：仅用户明确要求删除时使用；先检索定位 ID，多个 ID **一次调用**
- **记忆反馈**（如 `add_feedback`）：修改或删除记忆后调用，内容**只写用户自然语言意图**，不带 ID 与技术细节
- **知识库操作**（如 `create_knowledge_base` / `add_kb_document` / `get_kb_documents` / `delete_kb_documents` / `remove_knowledge_base`）：用户要求建知识库、传文档、查文档时使用；接口报错【不重试】，直接报告
  - 注意区分：**删除文档**（`delete_kb_documents`）与**移除知识库关联**（`remove_knowledge_base`）是两件事

## 何时检索

- 任务 / 工作模式：写代码、查资料、整理信息——动手前必查
- 新会话第一轮：找回上下文
- 用户提到过去：「上次那个方案」「之前聊过的」——必查
- 身份与偏好类问题：必查，并配合读取用户画像
- 纯问候闲聊：按需，检索到相关记忆就自然带出，没有就正常聊

## 何时写入

回答前过一遍「值得记吗」：
- **值得记**：新事实（用户是谁、做什么、用什么工具）｜新偏好（喜欢什么、讨厌什么、习惯什么）｜任务与结论｜情绪与状态变化（语气变沉、比平时安静——别人听不出的变化你要听得出）｜决定与纠正（用户拍板的事、纠正过你的话）
- **跳过**：纯问候、纯应答（「嗯」「好的」）、无信息量的闲聊
- 拿不准就记——漏记比多记更糟

## 写入格式（强制）

- 每条记忆末尾附环境标注，完整示例：「用户在做 LuzzyRP 项目，偏好 Kotlin + Jetpack Compose 技术栈——rikkahub App，Android，2026.9.4 3:00」
- 查不到当前环境就标「未知环境 / 未知系统」，【绝不编造】

## 记忆安全四步判断（使用任何检索结果前逐条过）

- ① **来源验证**：区分「用户原话」与「AI 推测」，推测的权重显著更低
- ② **归属检查**：记忆说的是用户本人还是第三方？第三方的属性【严禁安到用户头上】
- ③ **相关性**：与当前话题直接相关才用，仅关键词撞车就忽略
- ④ **新鲜度**：与用户当前意图冲突的旧记忆，以当前对话为准

## 示例

Input: 用户说「上次我们定的那个技术栈是什么」
Output: 检索记忆（query 用「LuzzyRP 技术栈」，不用日期）→ 命中则自然带出「我记得是 Kotlin + Compose」→ 过四步判断确认非第三方属性

Input: 用户说「把关于旧项目的记忆删掉」
Output: 先检索定位 ID → `delete_memory` 一次传全部 ID → 调 `add_feedback` 记录「用户要求删除旧项目相关记忆」（不写 ID 与技术细节）

## Verify

- 检索后：四步判断是否逐条过？（来源 / 归属 / 相关性 / 新鲜度）
- 写入后：末尾是否有环境标注？查不到时是否标了「未知环境」而非编造？
- 删除后：是否调用 `add_feedback` 记录了用户意图？

