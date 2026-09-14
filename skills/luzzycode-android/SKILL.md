---
name: luzzycode-android
description: >
  Use when a task involves creating, modifying, building, running, debugging,
  screenshotting, or automating an Android app, or when driving an Android
  emulator or USB device through the ZCode android-emulator plugin.
  Handles the ZCode plugin-market installation gate, the plugin's own skill
  reading, preflight environment checks, emulator and AVD lifecycle, Gradle
  build and install flow, screenshot verification, and ADB-based UI automation.
  Triggers: "android app", "android 开发", "安卓应用", "emulator", "模拟器", "AVD",
  "adb", "apk install", "jetpack compose", "gradle 构建", "跑一下安卓", "截屏看界面".
  Do NOT use for reverse engineering or analyzing a third-party APK (see
  luzzycode-reverse), for plain Kotlin or Java questions with no Android runtime
  involved, or for iOS development.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "android"
---

# LuzzyCode · Android 应用开发与模拟器

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-android/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-android) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-android/SKILL.md)

## 硬性前置一：插件必须从 ZCode 插件市场装

这套能力是 **ZCode 官方插件** `android-emulator@zcode-plugins-official`。它的 MCP 服务器由 ZCode 的插件宿主拉起（插件清单里的命令被指向 `ZCode.exe` + `__zcode-plugin-host`），**不在 ZCode 内就没有这套工具**。

| 步骤 | 内容 |
|---|---|
| 1 | 用户安装 **ZCode** |
| 2 | 在 ZCode 的**插件市场**安装 `android-emulator`（官方源 `zcode-plugins-official`） |
| 3 | 启用插件，按需配置 `sdk_path` / `default_avd` / `api_level` / `jdk_major` 等 |
| 4 | 会话里出现 `mcp__android_emulator__*` 工具，才算可用 |

**模拟器本体不在 ZCode 界面内**：Android Emulator 用**自己的桌面窗口**渲染（插件 MVP 的明确设计），ZCode 侧只提供控制它的 MCP 工具。

**插件没装 / 工具没出现时**：不假装可用，也不用裸 `adb` 与 `emulator` 命令硬拼一套替代流程。按常驻提示词 §五 澄清，说明需要在 ZCode 插件市场安装该插件并给出上面四步；用户拒绝安装就说明该能力缺失及其影响，其余工作照常推进。

## 硬性前置二：先读插件自带的正文

装上插件后，完整阅读它自带的正文（随插件缓存，路径 `<插件缓存>/skills/android-dev/`）：

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 工作流、工具说明、构建排障 |
| `INSTALL_ENVIRONMENT.md` | 环境缺失时的固定安装流程（macOS shell / Windows PowerShell） |

典型缓存落点：`~/.zcode/cli/plugins/cache/zcode-plugins-official/android-emulator/<版本>/skills/android-dev/`。

**只看到插件介绍页或工具名列表不算读过**；路径找不到就按 §1.1a 的纪律上报，不要凭印象编造流程。

## 官方文档与入口（固化，不必再搜）

### 插件本体

| 项 | 位置 |
|---|---|
| 插件标识 | `android-emulator@zcode-plugins-official`（ZCode 官方源） |
| 插件缓存 | `~/.zcode/cli/plugins/cache/zcode-plugins-official/android-emulator/<版本>/` |
| 插件 README | 缓存目录下的 `README.md`（含 MVP 范围、23 个工具清单、环境要求） |
| 插件 skill | 缓存目录下的 `skills/android-dev/SKILL.md` 与 `skills/android-dev/INSTALL_ENVIRONMENT.md` |
| 插件清单 | 缓存目录下的 `.zcode-plugin/plugin.json`、`.mcp.json` |
| 配置项 | ZCode 的 `~/.zcode/cli/config.json` → `plugins.options["android-emulator@zcode-plugins-official"]`（可配 `sdk_path` / `default_avd` / `api_level` / `build_tools_version` / `system_image_variant` / `system_image_abi` / `jdk_major`） |

### Android 官方文档

| 主题 | 链接 |
|---|---|
| 开发者总入口 | https://developer.android.com/develop |
| ADB（调试桥） | https://developer.android.com/tools/adb |
| Jetpack Compose | https://developer.android.com/compose |
| Gradle 构建配置 | https://developer.android.com/build |
| 模拟器 | https://developer.android.com/studio/run/emulator |
| AVD 管理 | https://developer.android.com/studio/run/managing-avds |
| SDK 命令行工具（`sdkmanager` / `avdmanager`） | https://developer.android.com/tools/sdkmanager |
| platform-tools（含 `adb`） | https://developer.android.com/tools/releases/platform-tools |
| Build-Tools（含 `apksigner` / `zipalign`） | https://developer.android.com/tools/releases/build-tools |
| UI Automator（UI 自动化的底层） | https://developer.android.com/training/testing/other-components/ui-automator |

## MCP 工具面

模型侧名字是 `mcp__android_emulator__<工具>`。23 个工具分四组：

| 组 | 工具 |
|---|---|
| 诊断与项目 | `android_preflight` · `android_discover_project` · `android_create_app` |
| 构建 | `android_build_app` · `android_build_and_run` |
| 设备与模拟器 | `android_list_devices` · `android_list_avds` · `android_start_emulator` · `android_stop_emulator` · `android_create_avd` · `android_install_app` · `android_launch_app` · `android_terminate_app` · `android_open_url` |
| 观察与 UI 自动化 | `android_screenshot` · `android_logs` · `android_ui_status` · `android_ui_describe` · `android_ui_resolve` · `android_ui_tap` · `android_ui_swipe` · `android_ui_type_text` · `android_ui_keyevent` |

**工具优先**：能用 MCP 工具完成的，不要退回裸 `adb` / `emulator` 命令。

## 标准工作流

1. **先诊断**：`android_preflight`。缺环境就按 `INSTALL_ENVIRONMENT.md` 的固定流程补，不要自创安装命令。
2. **摸项目**：`android_discover_project` 拿 Gradle root、模块、variant、applicationId、APK 输出。结果里的 `warnings` 要先读再构建，缺 `gradle.properties` / `local.properties` / wrapper 先修。
3. **建项目**（仅当确实没有）：`android_create_app` 生成最小 Kotlin + Jetpack Compose 应用，之后直接改 Kotlin / Compose 文件。
4. **构建并跑起来**：`android_build_and_run`。discovery 有歧义时传 `module` / `variant` / `applicationId`；指定目标传 `serial`。先读返回的 `output` 找编译错误，需要更多细节再看它给的日志路径。
5. **亲眼看**：`android_screenshot` 做视觉验收——这是本预设 §十 的要求，不靠读代码推断界面。
6. **运行时检查**：`android_open_url` / `android_launch_app` / `android_terminate_app` / `android_logs`。
7. **UI 自动化**：先 `android_ui_status`；点击坐标前先用 `android_ui_describe` 或 `android_ui_resolve` 定位。UI 自动化不可用时，退到构建 / 运行 / 截图三项，并明说 UI 自动化不可用。

**`android_start_emulator` 只启动新的 GUI 模拟器、不复用已有目标**；已有设备或模拟器就把它的 `serial` 传给后续工具。

## 环境要求

| 项 | 要求 |
|---|---|
| 宿主系统 | **macOS 或 Windows**；**Linux 不支持**（`android_preflight` 会直接报不支持） |
| Android 工具 | Android Studio 或 Android 命令行工具；SDK platform-tools（`adb`） |
| 模拟器 | Android SDK emulator 工具 + 至少一个 AVD |
| 真机 | 开好 USB 调试的设备，传 `serial` 即可，无需 AVD |
| Node.js | 24 |
| 可选 | `PATH` 里有 Gradle（生成项目缺 wrapper 时用） |
| 可配置 | SDK 路径、默认 AVD、API level、build-tools 版本、系统镜像 variant / ABI、JDK 主版本 |

## 安全红线

- **不代替用户**接受 Android SDK 许可、输入密码、清空模拟器数据、删除 AVD——遇到就停下来问（常驻 §六 / §七）
- `android_create_app` 默认不覆盖已生成文件；**只有用户明确确认后**才传 `overwrite: true`
- `sdkmanager --licenses` 这类要用户显式批准的动作，先拿到确认再跑
- 生成的工程与产物落**用户的项目**，不落进 LuzzyCode 仓库

## 常见失败路径

| 症状 | 处置 |
|---|---|
| 插件未装 / 工具不出现 | 澄清并给安装四步；不假装可用 |
| `preflight` 报缺项 | 按 `INSTALL_ENVIRONMENT.md` 走，**不要重装 SDK**去治一个只缺 Gradle 的环境 |
| 没有 AVD 但有就绪 USB 真机 | 继续——把该设备 `serial` 传给目标工具 |
| Gradle 报 `android.useAndroidX` 未启用 | 建 / 改 `gradle.properties`，加 `android.useAndroidX=true` |
| Gradle 找不到 SDK | 在 Gradle root 建 `local.properties`，写 `sdk.dir=<SDK 路径>` |
| 缺 `gradlew` | 装 Gradle 后 `gradle wrapper --gradle-version 8.9`，或让 `android_build_app` 尝试生成 |
| `sdkmanager` / `avdmanager` 找不到 Java | 按 `INSTALL_ENVIRONMENT.md` 导出匹配的 `JAVA_HOME` 再试；symlink 那步要先确认 |
| Windows 许可未接受导致装包失败 | 先拿用户明确批准，再跑 `sdkmanager.bat --licenses` |
| Windows 无模拟器加速 | 请用户开虚拟化 / WHPX 或装完 Emulator 驱动，再重跑 `preflight` |
| 系统镜像下载超时 | 先用 `default` 镜像、用同一命令加长超时重试，再换更大的 `google_apis` |

## 与相邻 skill 的分工

| 场景 | 走哪 |
|---|---|
| 逆向 / 分析别人的 APK（脱壳、签名、Hook） | `luzzycode-reverse` |
| 纯 Kotlin / Java 代码问题，不碰 Android 运行时 | `luzzycode-code` |
| 写 HTML 页面、浏览器实测 | `luzzycode-webdev` |
| 界面视觉风格、配色、动效 | `luzzycode-design` |
| iOS 开发 | 不在本预设覆盖范围 |

## 示例

Input: 「帮我做个安卓小应用，能显示当前时间」
Output: 确认插件已装且 `mcp__android_emulator__*` 可用（否则走安装四步）→ 读 `android-dev/SKILL.md` → `android_preflight` → `android_discover_project`（无项目）→ `android_create_app` → 直接改 Compose 文件 → `android_build_and_run` → `android_screenshot` 亲眼看界面 → 交付

Input: 「这个安卓项目构建报错了，帮我看看」
Output: `android_discover_project` 读 `warnings` → `android_build_app` 拿 `output` 定位编译错误 → 修 Kotlin / Gradle 配置 → 重跑 → 真机或模拟器上 `serial` 验证 → 需要运行时证据时 `android_logs`

Input: 「帮我看看这个别人的 APK 是怎么实现的」
Output: 这是**逆向**不是开发 → 转 `luzzycode-reverse`，走 reverse-skill 的 `apk-reverse` 路由

## Verify

- 动手前：插件装了吗？`mcp__android_emulator__*` 工具真的在会话里吗？
- `android-dev/SKILL.md` 正文读到了吗？（只看工具名列表不算）
- 环境缺失时走的是 `INSTALL_ENVIRONMENT.md` 的固定流程，还是自创命令？
- 有没有代替用户接受许可、输密码、清数据、删 AVD？（有就是违规）
- `overwrite: true` 是拿到用户明确确认后才传的吗？
- 界面用 `android_screenshot` 亲眼看过吗？没看就明说「未做视觉验收」
- Linux 宿主上报为不支持时，是否明确告知用户而不是硬试？
