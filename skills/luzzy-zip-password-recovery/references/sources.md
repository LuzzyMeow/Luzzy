# 来源与置信度分级

本文件记录本 skill 里每条技术断言的来源。断言可溯源，才敢照着它写代码。
分级口径：**一类**＝官方规范 / 厂商自家规范 / 同行评审论文 / 一手源码；
**二类**＝社区论坛、工程博客、个人仓库。二类只用于印证，不作为唯一依据。

## 一类来源（可作为唯一依据）

| 来源 | 能定住什么 | 链接 |
|---|---|---|
| **WinZip AES 加密规范 AE-1/AE-2**，文档版本 1.04，2009-01-30 | AES 条目的全部格式：method 99 + extra 0x9901（7 数据字节）、AE-1 存 CRC 而 AE-2 存 0、条目布局 `salt + pv(2) + 密文 + auth(10)`、PBKDF2 迭代 1000、CTR 模式、HMAC-SHA1 截断 10 字节、Encrypt-then-MAC | https://www.winzip.com/en/support/aes-encryption/ （镜像：https://chromium.googlesource.com/external/github.com/nmoinvaz/minizip/+/2.7.1/doc/winzip_aes.md） |
| **PKWARE .ZIP File Format Specification (APPNOTE.TXT)** | 基础 ZIP 结构与传统加密（ZipCrypto）的定义 | 规范索引 https://libzip.org/specifications/ ；格式描述 https://www.loc.gov/preservation/digital/formats/fdd/fdd000354.shtml |
| **Biham & Kocher (1994), A known plaintext attack on the PKZIP stream cipher** | 已知明文攻击的理论基础：由密码初始化、随明文持续更新，故 12 字节已知明文可反解密钥 | DOI `10.1007/3-540-60590-8_12` |
| **Kohno, Attacking and Repairing the WinZip Encryption Scheme**（ACM CCS 2004；亦见其 UCSD 学位论文） | WinZip AE 方案的攻击与修复分析，说明 Encrypt-then-MAC 内核与外围交互处的缺陷 | https://cryptosec.ucsd.edu/miscpapers/winzip-ccs04.pdf |
| **hashcat 源码** `src/modules/module_1720*.c` 与 `OpenCL/m17200_a0-pure.cl` | `$pkzip$`/`$pkzip2$` 字段语义、`MAX_DATA = 320 KB`、17200/17210 内核末尾那条「必须解完整流」的硬条件、17230 要求 `hash_count >= 3` | 本仓库克隆后可直接读；上游 https://github.com/hashcat/hashcat |
| **john 源码** `src/zip2john.c` | CS 的取法（`crc>>24 / crc>>16`，流式时改用时间戳）、`check_bytes` 由 version≥20 决定为 1、`-c` 只输出 36 字节部分数据 | https://github.com/openwall/john |
| **RFC 2898 / 2104 / 3686** | PBKDF2、HMAC、AES-CTR 的标准定义 | https://www.rfc-editor.org/info/rfc3686/ |

## 二类来源（用来印证，不单独采信）

| 来源 | 印证了什么 | 与本 skill 的对应 |
|---|---|---|
| hashcat 论坛帖 *choose PKZIP 17225 or 17230 or both?*（2024-12） | 同样的包 17225 能跑、17230 报 `No hashes loaded`——正是「17230 需要多条目」的表现 | 印证 `references/pkzip-hash-format.md` §4 |
| Reddit *Hashcat and a large hash* | `zip2john` 产出 15 亿字符的哈希行，hashcat 报 `Oversized line detected` | 印证单条目大包必须换 john / 本 skill 的 Python 路线 |
| Nvidia RTX 3090 / 4090 / 6000 Ada 的 hashcat 基准 gist 与论坛帖 | `-m 17200` 可达 **5.4 GH/s**（3090）；`-m 13600` WinZip 在 6000 Ada 上 **16.7 MH/s** | 量化「为什么 AES 必须上 GPU」 |
| agourlay, *Brute forcing protected ZIP archives in Rust* 与其工具 `zip-password-finder` | 同思路的独立实现（ZIP ZipCrypto+AES、7z AES-256） | 备选工具，见 `tools-and-links.md` |
| hashcat 论坛 *7z2hashcat* 帖 | 7z → `-m 11600` 的标准流程 | 见 `other-formats.md` |

## 一手实测（本机 2026-09，Windows / Ryzen 7 5800H / RTX 3050 Ti）

这些是自己量出来的，不是引用：

- ZIPCrypto 单条目、deflate、75 MB：Python 16 进程约 **22 万候选/秒**；6 位数字 4.4 s、8 位数字 457 s
- Node 解密同尺寸：**约 2.5 s**（纯 Python 同量级要 1–2 分钟）
- WinZip AES 解密（本 skill 实现）与 pyzipper 造的 AES-128/192/256 样本逐条比对：HMAC 全部匹配
- 单个 `$pkzip$` 的 `DT=1` 假命中率实测约 **1/256**（与理论一致）；AES 校验值假命中率 **1/65536**（与 WinZip 规范写明的一致）

## 交叉验证结论

| 断言 | 一类依据 | 独立印证 | 置信度 |
|---|---|---|---|
| ZipCrypto 第 12 字节 = CRC 最高字节 | hashcat 内核源码 + john 源码 | 本机实测（造包 → hashcat 破解） | 高 |
| 单条目大包不能用 hashcat 17200 | `MAX_DATA` 与内核硬条件（源码） | Reddit 用户报告 + 论坛帖 | 高 |
| WinZip AES 用 CTR，128 位**小端**计数器、起始 1 | WinZip 规范（CTR）+ pyzipper 实现 | 本机实测：AES 样本解密并且 HMAC 匹配 | 高 |
| AES 只靠 2 字节校验值不足以判定 | WinZip 规范明写 1/65536 | 本机实测率一致 | 高 |
| 17230 需要 ≥3 条目 | hashcat 源码 `hash_count < 3` | 论坛帖「同样报 No hashes loaded」 | 高 |

## 已排除的不可信来源

搜索结果里大量「ZIP 密码恢复软件」推广页（passcovery、systools、brevisoft 等）：
无技术细节、结论无法验证，且多为商业软件导流。**本 skill 不引用这一类来源。**
