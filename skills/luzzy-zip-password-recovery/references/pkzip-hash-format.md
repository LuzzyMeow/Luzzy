# PKZIP 哈希格式与 hashcat 模式硬限制

本文件是调试与生成 `$pkzip$` 哈希时的唯一依据。内容来自 hashcat 的
`src/modules/module_1720*.c`、`OpenCL/m17200_a0-pure.cl` 与 john 的 `src/zip2john.c` 源码。

## 1. ZipCrypto 算法（决定一切的前提）

三个 32 位密钥，初值固定：

```
k0 = 0x12345678   k1 = 0x23456789   k2 = 0x34567890
```

按键更新（`c` 为明文字节）：

```
k0 = crc32_tab[(k0 ^ c) & 0xFF] ^ (k0 >> 8)
k1 = (k1 + (k0 & 0xFF)) * 134775813 + 1     (mod 2^32)
k2 = crc32_tab[(k2 ^ (k1 >> 24)) & 0xFF] ^ (k2 >> 8)
```

密钥流字节：`temp = (k2 | 2) & 0xFFFF; ks = ((temp * (temp ^ 1)) >> 8) & 0xFF`
加密：`c = p ^ ks` 后 `update(p)`；解密：`p = c ^ ks` 后 `update(p)`。

密码先逐字节 `update(b)` 初始化。注意 `k1 * 134775813` 会溢出 32 位：
JS 里必须用 `Math.imul`，Python 里用 `& 0xFFFFFFFF`。

**为什么弱**：校验只用 12 字节加密头，且**只有最后 1 个字节**参与比对（见 §3），
没有 PBKDF2 那样的迭代。一次候选 = 一次建密钥 + 12 字节解密。

## 2. 两个格式：`$pkzip$` 与 `$pkzip2$`

```
$pkzip$ C*B*[ DT*MT {CL*UL*CR*OF*OX} * CT*DL*CS [/TC] * DA ]* $/pkzip$
```

| 字段 | 含义 |
|---|---|
| `C` | 条目数（hash_count），写在签名单词尾部，如 `$pkzip$1` |
| `B` | 有效校验字节数：`zip version needed >= 20` 时为 1，否则 2 |
| `DT` | 数据类型：1=部分数据、2=完整数据内联、3=从文件读（john 的 `*ZFILE*` 指针） |
| `MT` | magic 类型，恒为 0 |
| `CL/UL/CR/OF/OX` | 压缩长、原始长、CRC32、本地头偏移、数据在头之后的偏移（**DT>1 时才出现**） |
| `CT` | 压缩方式：8=deflate、0=stored |
| `DL` | `DA` 的字节数（**十六进制**） |
| `CS` | 2 字节校验值，见 §3 |
| `TC` | 仅 `$pkzip2$` 有；时间戳导出的校验值 |
| `DA` | 十六进制数据 |

版本判定是**签名单词的长度**：`$pkzip$1` 长 8 → v1（无 TC）；`$pkzip2$1` 长 9 → v2（有 TC）。
v1 时内核令 `checksum_from_timestamp = checksum_from_crc`。

## 3. 校验字节（CS）怎么算 —— 最容易错的一处

```
flags & 0x0008（流式/数据描述符）  →  CS = lastmod_time >> 8, lastmod_time & 0xFF
否则                              →  CS = (crc >> 24) & 0xFF, (crc >> 16) & 0xFF
```

内核比对逻辑（`m17200_a0-pure.cl:614-619`）：

```
checksum_size == 2 时：第 10 个字节 比对 CS & 0xFF 或 TC & 0xFF
无论何种情况：        第 11 个字节 比对 CS >> 8  或 TC >> 8
```

即：**解密后第 12 个字节必须等于 CRC32 的最高字节**。这就是 1/256 假阳性的来源。

## 4. hashcat 模式与**硬限制**

| 模式 | 名称 | 接受 `CT` | hash_count |
|---|---|---|---|
| 17200 | PKZIP (Compressed) | 仅 8 | **必须 =1** |
| 17210 | PKZIP (Uncompressed) | 仅 0 | 必须 =1 |
| 17220 | PKZIP (Compressed Multi-File) | — | — |
| 17225 | PKZIP (Mixed Multi-File) | 0 与 8 | — |
| 17230 | PKZIP (Mixed Multi-File Checksum-Only) | 0 与 8 | **3–8** |

三条会直接卡死「单个大文件」的限制：

1. `MAX_DATA = 320 * 1024`（module 与 kernel 都有）——`DA` 超过 320 KB 直接被拒。
   单个 75 MB 条目无法内联。
2. 17200/17210 的内核末尾有一行硬条件：

   ```c
   if (ret != MZ_STREAM_END || infstream.total_out != uncompressed_length) continue;
   ```

   即**必须把整个 deflate 流解完并产出完整长度**才认可候选。
   于是「只给 36 字节部分数据」的 `DT=1` 哈希在 17200 上**永远不可能命中**。
3. 17230（Checksum-Only，唯一不做完整校验的模式）要求 `hash_count >= 3`，
   单条目压缩包凑不出来；用同一条数据重复 3 次会让过滤退化到 1/256，
   几乎必然先撞上假阳性。

**结论：单个大条目的 ZIP 不要指望 hashcat，走 john 或 `scripts/crack.py`。**
hashcat 仍值得保留的用途：小包、AES 模式 13600、以及用官方内核**反向验证自写实现**。

## 5. 生成哈希时的手工核对

对单条目、需要小哈希时（DT=1，取前 36 字节）：

```
$pkzip$1*<B>*1*0*<CT>*24*<CS>*<前 36 字节密文的十六进制>*$/pkzip$
```

`24` 是十六进制写的 36。先与官方 `zip2john -c` 的输出对一遍 `CS` 与数据段，一致再往下走。

官方 `zip2john -c` 实测输出（v2 形态，多了 TC）：

```
$pkzip2$1*1*1*0*8*24*<CS>*<TC>*<36 字节>*$/pkzip2$
```

两者 `CS` 与 36 字节数据必须**逐字节一致**。

## 6. 已知明文路线（bkcrack）

ZipCrypto 的密钥流由密码初始化后**持续用明文更新**，所以：

- 密文 + **≥12 字节已知明文**（≥8 字节连续）→ 反解内部密钥（3×32 位）
- 拿到密钥即可解密全部同密码条目，无需知道密码本身
- 密码另有办法找回：`bkcrack -k <k0> <k1> <k2> -r 10 ?p`（复杂度约 n^(l-6)）

已知明文的常见来源：同一来源的其它文件（同编码器产出的文件头往往字节一致）、
模板文件、可预测的文件头（如 MP4 的 `ftyp` box、JPEG 的 SOI/APPn 段）。

## 7. 实测记录（供参照，勿套用具体数值）

- 75 MB、deflate、ZipCrypto 单条目：本机 16 进程 Python 约 **22 万候选/秒**；
  6 位数字 4.4 s、8 位数字 457 s
- Node（V8）解密 75 MB 约 **2.5 s**；纯 Python 同量级要 1–2 分钟
- 单个 `$pkzip$` 的 `DT=1` 假阳性率约 1/256 —— **必须**用全文件 CRC32 做最终判定
