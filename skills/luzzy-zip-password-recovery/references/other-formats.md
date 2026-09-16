# 拓展：ZIP 之外的其他加密格式

本 skill 的脚本只处理 ZIP（ZipCrypto + WinZip AES）。其他格式走同一套方法论，
只是换工具与模式号。**先判格式，再找对应的 2hashcat 工具，再交给 GPU。**

## 通用流程

1. 确认真实格式（扩展名会骗人）：看文件头。
   `7z` = `37 7A BC AF 27 1C`；`RAR4` = `52 61 72 21 1A 07 00`；
   `RAR5` = `52 61 72 21 1A 07 01 00`；`ZIP` = `50 4B 03 04`。
2. 确认加密方式与是否加密文件名（RAR/7z 可加密头部，那样连文件名都看不到）。
3. 用对应的提取工具生成哈希。
4. 用 hashcat/john 破解；拿到密码后用原生工具解包。

## 格式 → 工具 → 模式

| 格式 | 提取工具 | hashcat 模式 | 备注 |
|---|---|---|---|
| ZIP ZipCrypto / WinZip AES | `zip2john`（或本 skill 的脚本） | 17200–17230 / 13600 | 本 skill 覆盖 |
| 7z (AES-256) | `7z2hashcat`（也见新版 john 的 `7z2john`） | 11600 | 逆向转换：`philsmd/hc_to_7z` |
| RAR3 (含 header 加密) | `rar2john` | 12500 | |
| RAR5 | `rar2john` | 13000 | RAR5 的 KDF 更重，CPU 基本无望 |
| SecureZIP AES | `zip2john` 未必适用 | 23001 / 23002 / 23003（AES-128/192/256） | 见 hashcat 算法列表 |
| PKZIP Master Key | — | 20500 / 20510 | 老式「主密钥」归档 |
| PDF | `pdf2john` | 10400 / 10500 / 10600 / 10700 | 按版本选 |
| MS Office 2007+ | `office2john` | 9400 / 9500 / 9600 | 2003 及更早用 `$0/$1/$3/$4` 那几档 |

模式号以本机 hashcat 的 `--example-hashes` 输出为准（版本间会调整）；
上面这张表只用于选路。

## john 的格式清单（本机二进制实测，2026-09）

`john --list=formats` 中与本主题相关的条目：

```
7z  7z-opencl   PKZIP   rar   rar-opencl   RAR5   RAR5-opencl   securezip   ZIP   ZIP-opencl   ZipMonster
```

**关键区分**：`ZIP` 指 WinZip AES（哈希形如 `$zip2$`），`PKZIP` 指传统 ZipCrypto。
**只有 `ZIP` 带 `-opencl` 变体**——john 能上 GPU 的只有 WinZip AES，传统 ZipCrypto 只有 CPU 格式
（源码树里也只有 `opencl_zip_fmt_plug.c`，没有 `opencl_pkzip_*`）。

把这句和 hashcat 的限制合起来，得到一条硬结论：

> **单个大条目的 ZipCrypto 压缩包，GPU 帮不上忙。**
> hashcat 因 `MAX_DATA` 与内核硬条件收不下，john 又没有对应的 OpenCL 格式。
> 只能走 CPU：`john --format=PKZIP`，或本 skill 的 `scripts/crack.py`。

同目录 `run/` 下的提取工具：`zip2john.exe`、`rar2john.exe`、`7z2john.pl`（Perl，需 Perl 运行时）、
`pdf2john.pl`（Perl）、`office2john.py`（Python）。

## 7z 的实际操作

```bash
7z2hashcat archive.7z > hash.txt          # 需要 perl
hashcat -m 11600 hash.txt wordlist.txt
```

- `7z2hashcat` 是 hashcat 官方论坛的工具，输出可直接喂 `-m 11600`；john 侧的对应物是
  `7z2john.pl`（同样是 Perl 脚本，Windows 上要先有 Perl 运行时）
- 7z 用 AES-256 + 可配置的迭代次数，KDF 比 WinZip AES 更重，**CPU 毫无意义**
- 若归档加密了文件名，`7z2hashcat` 可能需要额外的字节信息，按其 README 处理
- john 侧可以跑 GPU：格式名 `7z-opencl`

## RAR 的实际操作

```bash
rar2john archive.rar > hash.txt
hashcat -m 12500 hash.txt wordlist.txt    # RAR3
hashcat -m 13000 hash.txt wordlist.txt    # RAR5
```

RAR5 用 PBKDF2-HMAC-SHA256 且迭代次数高，即便在 GPU 上也要按「每秒多少」
来估计，别按「每秒多少百万」。

## 与 ZIP 路线的取舍

- 拿到**已知明文**时，ZIP 的 ZipCrypto 有 bkcrack 这条捷径（其他格式没有等价物）
- WinZip AES 与 7z/RAR5 都属于「KDF 挡在前面」，只能靠 GPU 摊平
- 字典策略是共通的：先试同源密码、站点口令、纯数字，再上通用大表

## 规模化

单机不够用时，`Hashtopolis`（https://github.com/hashtopolis/server）是开源的
分布式 hashcat/john 编排平台，服务端派活、多台机器跑任务并回传结果。
本项目不接入它，仅在需要横向扩展时作为下一步方向记录。
