---
name: luzzycode-windows
description: >
  Use when repairing, optimizing, debloating, or diagnosing a Windows system, or
  when running any system-level Windows configuration change.
  Handles restore-point creation, change confirmation, selection among WinUtil /
  Win11Debloat / Sophia Script, registry and service-change safety, and rollback.
  Triggers: "windows is slow", "remove bloatware", "windows repair", "blue screen",
  "boot failure", "system optimization", "windows 卡", "去预装", "蓝屏", "系统优化",
  "修复系统", "清理系统".
  Do NOT use for application-level bugs, for driver or hardware faults needing a
  vendor tool, or for Linux/macOS system administration.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "system-ops"
---

# LuzzyCode · Windows 系统修复

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-windows/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-windows) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-windows/SKILL.md)

## 硬性前置：先读工具正文

动手前必读所选工具的仓库正文（口径见常驻提示词 §1.1）：

| 工具 | 定位 | 何时选它 |
|---|---|---|
| [WinUtil](https://github.com/ChrisTitusTech/winutil)（62.5k★） | 安装软件 + 去臃肿 + 排障 + 管更新 | 通用维护、全新装机 |
| [Win11Debloat](https://github.com/Raphire/Win11Debloat)（56.8k★） | 轻量 PowerShell，移除预装、关遥测 | 只需精准去臃肿 |
| [Sophia Script](https://github.com/farag2/Sophia-Script-for-Windows)（9.7k★） | 150+ 函数精细调优 | 细粒度配置 |

## 安全红线（高于一切，不可协商）

这三家都会**改系统级设置**，部分改动不可逆。

1. **先建还原点，再动手**
   ```powershell
   # 检查是否已启用系统保护
   Get-ComputerRestorePoint
   # 启用并创建还原点（需管理员）
   Enable-ComputerRestore -Drive "C:\"
   Checkpoint-Computer -Description "LuzzyCode-before-optimize" -RestorePointType MODIFY_SETTINGS
   ```
   Verify: `Get-ComputerRestorePoint` 列出刚建的还原点，且时间戳为本次操作前。

2. **复述改动再执行**：跑任何脚本前，把「将要改什么」列成清单给用户，拿到**明确确认**后才执行（常驻提示词 §六）。

3. **禁止盲跑远程脚本**：不要直接 `irm https://... | iex`。先下载、读内容、确认无害，再执行。

4. **分级执行**：涉及注册表、组策略、服务禁用的改动，**逐项确认**，不要一次全上。WinUtil 的 `Advanced` 预设**禁止**在用户生产机上直接跑。

5. **不叠脚本**：出问题用还原点回滚，**不要**再叠第二个优化脚本去修第一个的后果。

6. **不碰数据**：系统优化脚本不该动用户文件。任何声称要「清理」用户目录的，先停下来问。

## 标准流程

1. **诊断先行**：先搞清楚问题是什么，再选工具。收集：系统版本、症状、发生时间、最近装过什么
   ```powershell
   Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber
   Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, TotalVisibleMemorySize, FreePhysicalMemory
   ```
2. **建还原点**（上面第 1 条）
3. **列改动清单 → 用户确认**
4. **执行**（从最小改动开始，不要一上来就 Advanced）
5. **回读验证**：确认改动生效、系统仍正常启动、关键功能可用
6. **记录**：改了什么、怎么回滚，写进回答

## 常见症状 → 处置方向

| 症状 | 先查 | 别急着做 |
|---|---|---|
| 开机慢 | 启动项、服务、磁盘健康 | 不要直接禁用一堆服务 |
| 卡顿 | 内存占用、磁盘 IO、后台进程 | 不要盲目「优化注册表」 |
| 预装软件多 | 用 Win11Debloat 精准移除 | 不要手删 `WindowsApps` 目录 |
| 蓝屏 | 事件查看器、最近驱动/更新 | 不要用「系统优化」脚本治蓝屏 |
| 磁盘满 | `WinSxS`、休眠文件、更新缓存 | 不要手删 `WinSxS` |

## 示例

Input: 「电脑卡，帮我优化一下」
Output: 先诊断（版本 / 内存 / 启动项 / 磁盘）→ 给出具体瓶颈结论 → 建议最小改动 → 建还原点 → 列改动清单 → 用户确认 → 执行 → 回读验证

Input: 「把 Windows 的预装软件都删了」
Output: 选 Win11Debloat → 列出去掉哪些应用 → 建还原点 → 确认 → 执行 → 验证系统正常

Input: 用户想在生产机上跑 WinUtil Advanced 预设
Output: **停下来问用途** → 说明 Advanced 的风险（可能影响稳定性）→ 建议先用 Minimal/Standard，或先在非生产机验证

## Verify

- 动手前：还原点建了吗？`Get-ComputerRestorePoint` 能列出吗？
- 改动清单给用户确认了吗？
- 脚本内容是读过的，还是盲跑的？
- 执行后：系统能正常启动吗？关键功能还在吗？
- 回答里写明「改了什么 + 怎么回滚」了吗？
