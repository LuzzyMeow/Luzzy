# AGENTS.md · LuzzyCode

给在本仓库里干活的 Agent 读的项目说明。上位规则是 `prompt/LuzzyCode.md`，本文件只讲这个仓库自己的事。

## 这是什么

鹿溪（Coding 模式）预设的**权威源仓库**。内容是提示词与 skill，不是可运行程序。

- `prompt/LuzzyCode.md` —— 常驻提示词，**唯一真源**
- `skills/` —— 19 个 skill，每个一个目录一个 `SKILL.md`
- `README.md` —— 对外门面，面向使用者

## 工作区约定

工作区根就是本目录 `C:\Users\Administrator\Desktop\LuzzyCode`。

**不要在桌面根目录（`C:\Users\Administrator\Desktop\`）生成 `LuzzyCode.md` 之类的副本。** 提示词只有 `prompt/LuzzyCode.md` 一份真源，散落的副本会互相打架。

临时脚本、探测产物、实验文件放系统临时目录，不要落在仓库里。

## 改动的三条纪律

### 一、提示词与 skill 清单必须同步

`prompt/LuzzyCode.md` §12.1 是 skill 索引。**新增、改名、删除 skill 时，同一轮里改完三处**：

1. `skills/<名>/SKILL.md` 本体
2. `prompt/LuzzyCode.md` §12.1 的清单行
3. `skills/luzzycode/SKILL.md` 的路由表行

漏掉第 2、3 处，Agent 就找不到自家 skill。改完数一遍：

| 位置 | 应有行数 | 说明 |
|---|---|---|
| `skills/` 磁盘目录 | 19 | 含编排器 `luzzycode` |
| §12.1 清单 | 19 | 同样含编排器那一行 |
| `luzzycode` 路由表 | 18 | **只列子 skill**，编排器不路由到自己 |

编排器 description 里的 child skill 数量对应路由表，是 **eighteen**。

### 二、改完必须过解析器校验

用 DSH 真实的解析规则校验全部 skill，不要只看文件存在：

```bash
node <probe>/validate-repo.mjs
# 期望输出：SUMMARY ok=19 bad=0
```

`name` 必须是 kebab-case 且与目录名一致，`description` 必填。旧式驼峰键（`disableModelInvocation` / `modelInvocable` / `userInvocable`）会被硬拒。

### 三、README 里的数字要能复现

行数与 token 数是实测值，不是估的：

```bash
python -c "import tiktoken,pathlib; e=tiktoken.get_encoding('o200k_base'); \
print(len(e.encode(pathlib.Path('prompt/LuzzyCode.md').read_text(encoding='utf-8'))))"
```

换了编码或改了正文，同步更新 README「提示词预算」表。

## 同步到本机预设

改完 `prompt/LuzzyCode.md` 后，本机预设不会自动跟着变。链路是单向的：

```
prompt/LuzzyCode.md  →  persona.md  →  agent.cordis.yml 的 persona.config.prefix 块
                        (机械生成，禁止手工编辑 YAML 标量)
```

用 `sync-persona.mjs` 走这条链路，它带解析回验：反解出的文本与 `persona.md` 不一致就回滚。

预设目录：`C:\Users\Administrator\.dsh\.agent-presets\luzzycode\`

校验要点：

- `config.prefix` 是必填字段名。DSH 2.0.9 起不再接受旧的 `config.text`
- 块用 `|-` 指示符，所以 YAML 解析出来的文本**比 `persona.md` 少末尾一个换行**。这是规范行为，不是缺陷
- 顶层条目应为 **17** 条
- 预设只在**进程启动时**读取，改动对新会话生效；skill 走热重载，改完即可用

改动登记写进预设目录的 `persona.changes.md`。

## 推送

remote 已是 SSH（`git@github.com:LuzzyMeow/LuzzyCode.git`）。用 `git push origin main`。

不要再建远程副本；本仓库本身就是权威源。

## 本仓库自己的 skill

`skills/luzzycode-skills/` 讲怎么写 skill，`skills/luzzycode-git/` 讲怎么推 GitHub。改本仓库时这两个照常适用。

写正文遵守 stop-slop 与 avoid-ai-writing 的口径：无 em dash（中文 `——` 不受限）、主动语态、具体优于抽象、两句好过三句排比、不写空洞过渡。
