# ZIP 密码恢复 · 工具与来源

本文件是唯一的外部工具索引。所有链接在 2026-09 实测或核实过；使用前若失效，
按 Luzzy 提示词 §1.1.9 上报并走镜像（gh-proxy / ghfast）。

## 决策表：先看这张

| 情形 | 用什么 | 理由 |
|---|---|---|
| ZipCrypto，小/中档字典或掩码 | `scripts/crack.py` | 自带，零依赖，16 进程 |
| ZipCrypto，需要 GPU 或超大掩码 | hashcat `-m 17200/17210` | 仅限**条目数据 ≤ 320 KB** |
| ZipCrypto，手上有 12+ 字节已知明文 | **bkcrack** | 直接恢复密钥，绕过密码搜索 |
| ZipCrypto，任意大小、要跑 john | john + `zip2john` | 支持大文件（内联全部数据） |
| WinZip AES-128/192/256 | hashcat `-m 13600` 或 john | PBKDF2 1000 轮，必须 GPU 才有速度 |
| 已拿到密码，要解出文件 | `scripts/unzip.js`（大文件）/ `scripts/ziptool.py decrypt` | 全文件 CRC32 强校验 |
| 已拿到密码，WinZip AES 解包 | 7-Zip / WinRAR | 本套脚本只做 ZipCrypto |

## hashcat / hashcat

- 仓库：https://github.com/hashcat/hashcat （26.8k★，MIT）
- 官网与二进制：https://hashcat.net/hashcat/ — 当前版本 v7.1.2（2025.08.23）
- 直接下载：`https://hashcat.net/files/hashcat-7.1.2.7z`
- Windows 用法：解压后**必须在 hashcat 自己的目录里运行**（它按相对路径找 `./OpenCL/`），
  否则报 `./OpenCL/: No such file or directory`
- 设备检查：`hashcat.exe -I`；NVIDIA 卡只需驱动自带的 OpenCL 运行时，
  出现 `Falling back to OpenCL runtime` 属正常（CUDA 后端没装 Toolkit 时才这样）
- 相关模式：`13600`（WinZip AES）、`17200/17210`（单条目 PKZIP 压缩/存储）、
  `17220/17225/17230`（多条目）；模式细节与硬限制见 `pkzip-hash-format.md`
- 许可：MIT

## openwall/john

- 仓库：https://github.com/openwall/john （13.6k★）
- 官方 Windows 二进制（jumbo，含 `zip2john.exe`）：
  `https://www.openwall.com/john/k/john-1.9.0-jumbo-1-win64.zip` （63 MB）
  - 7z 版：`https://www.openwall.com/john/k/john-1.9.0-jumbo-1-win64.7z`
  - 实测该站国内下载约 **290 KB/s**，63 MB 需约 4 分钟；hashcat.net 则可到 9 MB/s
- 哈希提取：`run\zip2john.exe [-c] archive.zip`
  - `-c` = checksum-only，只输出 36 字节的部分数据条目，**输出很小**（推荐先用它）
  - 不加 `-c` 会**把全部压缩数据内联成十六进制**：75 MB 的条目会产生 150 MB 的哈希行
    （官方自己也提示 "It is normal for some outputs to be very large"）
  - 输出格式与 hashcat 的 `$pkzip2$` 兼容，两边可以互相喂
- 破解：`john.exe --format=pkzip --wordlist=xxx hash.txt`；`--show` 查看结果
- 许可：Openwall / GPL 系（jumbo）

## kimci86/bkcrack

- 仓库：https://github.com/kimci86/bkcrack （2.2k★，**zlib/png 许可**）
- 原理：Biham–Kocher 已知明文攻击。ZipCrypto 的密钥流由密码初始化后**用明文持续更新**，
  因此给定密文 + **12 字节已知明文（其中至少 8 字节连续）**即可反解出内部密钥（3 个 32 位整数）
- 安装：GitHub Releases 有 **Windows / macOS / Ubuntu 预编译包**，解压即用
  （Windows 需 Microsoft Visual C++ 运行库）；或用 CMake 自行编译
- 关键命令：
  - `bkcrack -L archive.zip` — 列出条目与加密方式
  - `bkcrack -C encrypted.zip -c cipher -P plain.zip -p plain` — 从压缩包取已知明文
  - `bkcrack -c cipherfile -p plainfile -o offset` — 已知明文不在开头时指定偏移（可为负）
  - `bkcrack -c cipherfile -p plainfile -x 25 4b4f -x 30 21` — 稀疏已知明文补齐到 12 字节
  - `bkcrack -k <k0> <k1> <k2> -D decrypted.zip` — 用密钥生成无密码副本
  - `bkcrack -k ... -r 10 ?p` — 从密钥暴力找回密码；`-m` 支持掩码
- 何时值得上：手上**真的知道**压缩内容的一部分（同系列文件、已知文件头、模板文件）
- 局限：只对 **ZipCrypto** 有效；对 WinZip AES 无效

## 其他常用件

| 工具 | 用途 | 来源 |
|---|---|---|
| 7-Zip / WinRAR | 已知密码后解 AES 包；也可用于小规模试密码 | 各自官网 |
| `zlib`（Python / Node 内置） | deflate 解压与 CRC32，无需额外依赖 | 标准库 |

## 本机实测环境记录（2026-09）

- Windows + AMD Ryzen 7 5800H（16 逻辑核）+ RTX 3050 Ti + 32 GB RAM
- Python（miniconda）、Node v24、Git、curl.exe 均在位；**无 7z、无 gcc**
- hashcat 7.1.2 Windows 二进制 + 官方 john win64 二进制可直接跑，无需编译
- 二进制包解压：Windows 自带 `tar.exe`（bsdtar）**可以直接解 7z**，
  即 `tar -xf hashcat-7.1.2.7z -C <目标目录>`；`.zip` 用 `Expand-Archive`
