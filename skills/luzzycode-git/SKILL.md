---
name: luzzycode-git
description: >
  Use when performing Git or GitHub operations — cloning, pulling, pushing,
  setting remotes, creating repositories, committing, branching, or opening PRs,
  including when GitHub is unreachable and a mirror is needed.
  Handles SSH-preferred remote handling, remote correction after repository
  creation, SSH connectivity probing, domestic mirror proxying (gh-proxy /
  ghfast / Gitee import), commit hygiene, line-ending normalization, and push
  failure diagnosis.
  Triggers: "clone", "push", "pull", "git remote", "create a repo", "gh repo",
  "SSH", "HTTPS remote", "commit", "branch", "PR", "GitHub 打不开", "镜像",
  "加速", "仓库", "推送", "克隆", "提交".
  Do NOT use for editing source code content, for web search (see
  luzzycode-search), or for general file management unrelated to version control.
---

# LuzzyCode · GitHub 与 Git 操作

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-git/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-git) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-git/SKILL.md)

## SSH 优先（强制）

GitHub 操作**一律优先 SSH 形式** `git@github.com:<owner>/<repo>.git`，不用 `https://github.com/...` 的 HTTPS 形式。

**理由**：SSH 走密钥认证，不依赖 token 有效期，也不会把凭据写进 `.git/config`。

### 创建仓库后的必做纠正

`gh repo create` 默认给出 **HTTPS remote**——建完**立即改正**：

```bash
gh repo create <name> --public --source=. --remote=origin --description "..."
git remote set-url origin git@github.com:<owner>/<repo>.git
git remote -v                       # 必须显示 git@github.com: 开头
git push -u origin main
```

Verify: `git remote -v` 的两行都以 `git@github.com:` 开头，才算切换成功。

### 先探通道再操作

不确定 SSH 可用性时先探一次：

```bash
ssh -T git@github.com
```

Expected: `Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.`

- 退出码为 1 但出现上面这句话 → **认证成功**（GitHub 不提供 shell，属正常）
- 本机 SSH 可能配置为走 `ssh.github.com:443` 以绕过 22 端口封锁：

  ```
  Host github.com
    HostName ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_ed25519
  ```

  这是**正常配置，不要改它**。

## 例外：何时可以退回 HTTPS

仅当 SSH 明确不可用：无密钥、认证失败且无法修复、网络封锁且镜像不可达。退回时**必须在回答里说明原因**。

## 国内网络受限：镜像中转

SSH 与直连 GitHub 都不通时，**逐级降级**：

| 手段 | 用法 | 实测状态 |
|---|---|---|
| **gh-proxy 代理** | clone：`git clone https://gh-proxy.com/https://github.com/<owner>/<repo>.git`<br>raw：`https://gh-proxy.com/https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>`<br>archive：`https://gh-proxy.com/https://github.com/<owner>/<repo>/archive/refs/heads/main.zip` | clone 与 raw 均实测可用 |
| **ghfast 代理** | 同上，域名换 `ghfast.top` | raw 实测可用；clone 可能超时 |
| **AnySearch 抓取** | `extract` 抓 `raw.githubusercontent.com` 或 `github.com/.../blob/...` | 走 AnySearch 通道，不受 GitHub 连通性影响 |
| **Gitee 导入** | Gitee「从 GitHub 导入仓库」建镜像后从 Gitee clone | 兜底，需用户账号 |

**优先级**：SSH 直连 → gh-proxy → AnySearch 抓单文件 → Gitee 导入

**使用前先探一次**（镜像域名会失效；上表两个是实测 7 个后筛出的可用项，其余 5 个已不可用）：

```bash
curl -fsSL -o /dev/null -w "%{http_code}\n" \
  https://gh-proxy.com/https://raw.githubusercontent.com/<owner>/<repo>/main/README.md
```

Expected: `200`。非 200 就换下一个手段，并在回答里说明换了哪个。

**安全边界**：代理站会看到请求的 URL——**只用于公开仓库的读取**。私有仓库、含凭据的拉取，宁可停下问用户，也不走第三方代理。

## 提交卫生

- **小步提交**，每次改动一个清晰的 save point
- **明确列出文件**，【禁 `git add .`】——避免把临时产物、密钥、构建产物带进提交
- commit message 说清「**为什么改**」，不只说改了什么
- 【禁 `git push --force`】——常驻 §七 列为「绝不做」，**本 skill 不设例外**。历史需要重写时停下来向用户说明，由用户决定并自行执行
- 提交前扫一遍敏感信息：API key、token、私钥、真实凭据一律不得入库；文档里的凭据使用 `${PLACEHOLDER}` 占位

## 换行符与跨平台

纯文本仓库（文档、skill）加 `.gitattributes` 统一为 LF：

```
* text=auto eol=lf
*.md text eol=lf
*.png binary
```

Verify: `git ls-files --eol` 输出中文本文件为 `i/lf w/lf`。

CRLF 会污染 diff，也可能影响部分 frontmatter 解析器——跨平台读取的仓库必须归一化。

## 推送失败诊断

| 现象 | 处置 |
|---|---|
| `Permission denied (publickey)` | SSH 密钥未加载或未加到 GitHub；先 `ssh -T git@github.com` 探 |
| `Could not resolve hostname` | 网络/DNS 问题；本机 SSH 走 443 配置可绕过 |
| `failed to push some refs` | 远端有新提交；先 `git pull --rebase` 再推 |
| `src refspec main does not match any` | 尚未提交；先 `git commit` |
| `Updates were rejected` | 分支保护或非快进；【不要 force push】，先与用户确认 |

**失败不无限重试**：同一错误最多试 3 次，之后换路径或向用户说明。

## 示例

Input: 用户要「把这个文件夹传到 GitHub」
Output: `gh repo create` → `git remote set-url origin git@github.com:...` → `git remote -v` 确认 → `git push -u origin main` → 独立克隆复核

Input: 用户说「推送报错了」
Output: 先看错误类型 → `Permission denied` 则探 SSH 通道 → 若通道正常则查远端分支状态 → 报告具体原因，不盲目 force push

## Verify

- 建仓库后：`git remote -v` 两行是否都以 `git@github.com:` 开头？
- 推送前：改动文件是显式列出的，还是用了 `git add .`？
- 提交前扫过敏感信息吗（API key / token / 私钥 / 真实凭据）？
- 换行符：`git ls-files --eol` 里文本文件是否为 `i/lf w/lf`？
- 有没有执行过 `git push --force`？（有就是违规——本 skill 不设例外）
- 同一错误重试超过 3 次了吗？超了就该换路径或说明
