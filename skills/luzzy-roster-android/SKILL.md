---
name: luzzy-roster-android
description: >
  Use when the Luzzy checklist (必读清单) hits the Android 开发 / 模拟器 category —
  reading sub-items for Android development and emulator work; six entries, take four; requires the ZCode android-emulator plugin.
  Answers "Android开发的清单子项" "模拟器插件怎么装" "android-dev正文在哪" "adb文档是哪一条".
  Do NOT use for executing the task itself — discipline and red lines live in the Luzzy
  system prompt — nor for the reading gate, receipt, or triage logic, nor for other
  checklist categories or tasks unrelated to this one.
license: MIT
metadata:
  version: "1.0.0"
  author: "鹿溪 (LuzzyMeow)"
  category: "luzzy-roster"
  maturity: "L2"
---

# Android 开发 / 模拟器 · 仓库子项明细

提示词 §1.1.6 命中「Android 开发 / 模拟器」后，读本文件拿仓库子项明细与执行细则。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（6 条 → 取 4 条）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | `https://developer.android.com/develop` | 正文 |
| 2 | `https://developer.android.com/tools/adb` | 正文 |
| 3 | `https://developer.android.com/compose` | 正文 |
| 4 | `https://developer.android.com/build` | 正文 |
| 5 | 插件自带正文 `skills/android-dev/SKILL.md` | 工作流与工具说明 |
| 6 | 插件自带正文 `skills/android-dev/INSTALL_ENVIRONMENT.md` | 环境缺失时的固定安装流程 |

**硬性前置：先从 ZCode 插件市场装 `android-emulator`**（`zcode-plugins-official` 源）——不在 ZCode 内就没有这套 MCP 工具。插件缓存典型路径：`~/.zcode/cli/plugins/cache/zcode-plugins-official/android-emulator/<版本>/skills/android-dev/`。

## 执行细则（提示词 §14.12 的操作明细）

**工具面（23 个，模型侧名字为 `mcp__android_emulator__<工具>`）**：诊断与项目 `android_preflight` / `android_discover_project` / `android_create_app`｜构建 `android_build_app` / `android_build_and_run`｜设备与模拟器 `android_list_devices` / `android_list_avds` / `android_start_emulator` / `android_stop_emulator` / `android_create_avd` / `android_install_app` / `android_launch_app` / `android_terminate_app` / `android_open_url`｜观察与 UI 自动化 `android_screenshot` / `android_logs` / `android_ui_status` / `android_ui_describe` / `android_ui_resolve` / `android_ui_tap` / `android_ui_swipe` / `android_ui_type_text` / `android_ui_keyevent`。**能用工具完成的，不要退回裸 adb**。

**标准工作流**：

1. **先诊断**：`android_preflight`。缺环境就按 `INSTALL_ENVIRONMENT.md` 的固定流程补，**不要自创安装命令**
2. **摸项目**：`android_discover_project` 拿 Gradle root、模块、variant、applicationId、APK 输出。结果里的 `warnings` 先读再构建；缺 `gradle.properties` / `local.properties` / wrapper 先修
3. **建项目**（仅当确实没有）：`android_create_app` 生成最小 Kotlin + Jetpack Compose 应用，之后直接改 Kotlin / Compose 文件
4. **构建并跑起来**：`android_build_and_run`。discovery 有歧义时传 `module` / `variant` / `applicationId`；指定目标传 `serial`。先读返回的 `output` 找编译错误
5. **亲眼看**：`android_screenshot` 做视觉验收（提示词 §14.1），不靠读代码推断界面
6. **运行时检查**：`android_open_url` / `android_launch_app` / `android_terminate_app` / `android_logs`
7. **UI 自动化**：先 `android_ui_status`；点击坐标前先用 `android_ui_describe` 或 `android_ui_resolve` 定位。不可用时退到构建 / 运行 / 截图三项，并明说 UI 自动化不可用

**`android_start_emulator` 只启动新的 GUI 模拟器、不复用已有目标**；已有设备或模拟器就把它的 `serial` 传给后续工具。

**环境要求**：宿主 **macOS 或 Windows**（**Linux 不支持**，`preflight` 会直接报不支持）｜Android Studio 或命令行工具｜SDK platform-tools（`adb`）｜emulator 工具 + 至少一个 AVD（真机可免）｜Node.js 24｜可选 `PATH` 里有 Gradle。

**常见失败路径**：插件未装 → 按提示词 §14.12 给安装四步｜`preflight` 报缺项 → 按 `INSTALL_ENVIRONMENT.md` 走，**不要重装 SDK** 去治一个只缺 Gradle 的环境｜没有 AVD 但有就绪 USB 真机 → 继续，把 `serial` 传给目标工具｜Gradle 报 `android.useAndroidX` 未启用 → 建 / 改 `gradle.properties`｜Gradle 找不到 SDK → 建 `local.properties` 写 `sdk.dir=`｜缺 `gradlew` → `gradle wrapper --gradle-version 8.9`｜`sdkmanager` 找不到 Java → 按说明导出匹配 `JAVA_HOME`｜Windows 许可未接受 → 先拿明确批准再跑 `sdkmanager.bat --licenses`｜Windows 无模拟器加速 → 请用户开虚拟化 / WHPX｜镜像下载超时 → 先用 `default` 镜像并加长超时重试。

## Examples

Input: 命中「Android 开发」
Output: 6 条取 4（含插件自带正文两条）→ 落回执 → 按 §14.12 工作流走。

Input: 插件没装、工具没出现
Output: 不假装可用、不用裸 adb 硬拼 → 按提示词 §14.12 给安装四步并澄清。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

纪律、红线与验收标准见提示词 §14.12；本 skill 装清单明细与操作性执行细则。
