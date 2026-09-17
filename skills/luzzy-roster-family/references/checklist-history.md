# 清单子项变更登记（roster 家族共享）

各 roster skill 的仓库子项与执行细则在这里增删改。每条变更写明：日期、skill、子项、动作（入 / 出 / 换 / 迁）、理由。

| 日期 | skill | 子项 | 动作 | 理由 |
|---|---|---|---|---|
| 2026-09-16 | 全部 | 全部子项明细 | 迁 | 从 `prompt/Luzzy.md` §1.1.6 分离：提示词每类只留一行指向，明细与安装坑位下沉各 roster skill（常驻预算瘦身；仓库链接的新陈代谢不再触碰提示词）。同日删除临时方案 `luzzy-skill-roster`（单一文件装全部明细），由 21 个分 skill 取代 |
| 2026-09-16 | design | 新增第 5 条：**emilkowalski/skills**（38.1k star，MIT）——动效与 UI 打磨专家纪律，主技能 `emil-design-eng`（动画决策框架）必读，动效任务加读 `animate` / `review-animations` 子技能 | 入 | 用户点名新增；设计类基线由 4 条扩为 5 条（全读不折减），提示词 §1.1.6 / §1.1.8 / §14.1 条数口径同步；注意其 SKILL.md 首段「Initial Response」话术不覆盖总路由权，已在 roster 内标注 |
| 2026-09-16 | reverse | 新增第 2 条：**luzzy-zip-password-recovery**（本地配套 skill，MIT，v1.1.1）——ZIP 密码恢复（ZipCrypto/WinZip AES 分类、字典/掩码/已知明文、CRC32+HMAC 全量验证，含 4 脚本 4 references）；ziptool selftest PASS、validate-trigger 11/11 | 入 | 用户交付；挂靠逆向/授权渗透类（授权门同 §六/§14.10），roster-reverse 子项表 1→2 条，提示词 §1.1.6 主表同步；name 与目录名对齐为 luzzy-zip-password-recovery，7z/RAR 越界由其 references/other-formats.md 承接 |
| 2026-09-18 | ppt | 安装要点差异补离线兜底一句 | 迁 | §14.3 的安装要点差异段删除：roster 原已装有大半内容，只补「clone 后拷含正文层」的离线兜底；选择纪律与交付标准留提示词 |
| 2026-09-18 | reverse | 前置要求（Node / Python / Java 版本）+ 场景路由表 | 迁 | 从提示词 §14.10 迁入「执行细则」节；整仓 clone 与 `tool-index.md` 警示已在子项表第 1 条，不重复 |
| 2026-09-18 | assets | 消费方式（Lobe UI 安装细节 / Lobe Icons 接入 / Game Icon Pack 用法） | 迁 | 从提示词 §14.11 迁入「执行细则」节，去重后只装子项表没有的增量；许可纪律与商标边界留提示词 |
| 2026-09-18 | android | 工具面 23 枚举、标准工作流 7 步、start_emulator 语义、环境要求、常见失败路径 | 迁 | 从提示词 §14.12 迁入「执行细则」节；硬性前置四步、先读插件正文与安全红线留提示词 |
| 2026-09-18 | mcp | 传输选型表、导入客户端 6 步、工具命名、常见失败 | 迁 | 从提示词 §14.13 迁入「执行细则」节；关键设计规则、必须实测与供应链红线留提示词 |
| 2026-09-18 | browser | 三条接入路径、稳定入口命令族、执行纪律、失败路径表 | 迁 | 从提示词 §14.16 迁入「执行细则」节；前置引导与权限红线留提示词。六节下沉后提示词 35,790 → 33,133 token，§十四 只留纪律 / 红线 / 验收标准 |

## 登记纪律

- 修链接 / 改坑位描述 / 改执行细则 → 只改对应 roster skill，提示词不动
- 改**条数** → 对应 roster skill 与提示词 §1.1.6 主表「条数」列**两侧同步**
- 新增类目（第十八类）→ 提示词级变更：先改提示词，再建 roster skill，最后回本文件登记
