---
name: luzzy-zip-password-recovery
description: >
  Use when a ZIP archive's password must be recovered, or its contents extracted
  without the password: "crack zip password", "破解 zip 密码", "解压密码忘了",
  "加密压缩包打不开", "这个压缩包的密码是多少", "zip2john", "hashcat PKZIP",
  "ZipCrypto", "WinZip AES", "recover archive password", "brute force a zip".
  Handles encryption classification, hash extraction, dictionary / mask /
  known-plaintext attacks, full-file CRC32 verification and extraction of every
  entry. Do NOT use for other formats — RAR files, sevenzip archives, PDF, Office documents,
  disk images — different formats need different tools (see
  references/other-formats.md); never attempt any of this without the owner's
  written authorization.
license: MIT
metadata:
  version: "1.1.1"
  author: "鹿溪 / Luzzy"
---

# ZIP Password Recovery

## Scope and authorization

Recover the password of a password-protected ZIP, or open it without one. Three
schemes exist and they need different handling:

| Scheme | Marker in the archive | Cost per guess | Search route | Unpack route |
|---|---|---|---|---|
| ZipCrypto (legacy PKWARE) | flag bit 0, no AES extra field | one CRC32 table loop | `scripts/crack.py`, john `PKZIP`, bkcrack | `unzip.js` / `ziptool.py decrypt` |
| WinZip AES-128/192/256 | extra field 0x9901, method 99 | PBKDF2-HMAC-SHA1 x1000 | hashcat `-m 13600`, john `ZIP-opencl` | `unzip.js` |
| none | flag bit 0 clear | nothing to crack | — | extract directly |

Both schemes are handled end to end by this skill's own scripts. Only the
*search* for an AES password needs a GPU to be practical.

Confirm the archive belongs to the user or that they are authorized to open it.
A forgotten password on the user's own machine is a routine recovery job;
anything else stops and asks before any attempt.

## Workflow

1. Classify the archive.

   ```
   python scripts/ziptool.py detect <archive.zip>
   ```

   Verify: the output names ZipCrypto, WinZip AES-<bits> (AE-1 or AE-2), or not
   encrypted, together with every entry's method, sizes and CRC32.

2. Choose the route.

   - ZipCrypto, dictionary or modest keyspace -> `scripts/crack.py`.
   - ZipCrypto, and part of the plaintext is known -> bkcrack. A known-plaintext
     attack recovers the keys outright and skips the password search.
   - ZipCrypto, one large entry, wide keyspace -> john `--format=PKZIP` (CPU) or
     `scripts/crack.py`. There is no GPU path for this case; see the note below.
   - WinZip AES -> extract the hash with `zip2john`, then hashcat `-m 13600`
     (GPU) or john `ZIP-opencl`. A pure-Python dictionary search is possible but
     a thousand times slower; use it only for short candidate lists.
   - Not encrypted -> extract, nothing to do.

3. Spend cheap knowledge before compute.

   Try what costs nothing first. Archives published by one source usually share
   a password, so a sibling archive already recovered is the single highest-value
   candidate. Then the archive's own base name, the inner file names, uploader
   codes, plain digit strings.

   ```
   python scripts/crack.py dict <archive.zip> <wordlist> [more wordlists ...]
   ```

   Verify: the run reports either candidate passwords or an exhausted keyspace,
   and always prints the confirmation command for what it reports.

4. Widen only as far as the evidence justifies.

   ```
   python scripts/crack.py num  <archive.zip> 6
   python scripts/crack.py num  <archive.zip> 8
   python scripts/crack.py mask <archive.zip> 0123456789abcdef 6
   python scripts/crack.py dict <archive.zip> rockyou.txt --magic 0000002066747970
   ```

   Token pools and ordering: pure digits first (6, 8, 9 digits cover a large
   share of real-world Chinese sharing passwords), then digits with a known
   prefix, then dates, then general wordlists with rules. A local
   `password.lst` next to a john build is already about 1.8M candidates and
   costs seconds.

   `--magic` supplies known plaintext at the start of the file body and is the
   only reliable extra filter for stored (method 0) entries; without it, stored
   entries pass the check byte at roughly 1/256 and produce noise.

   Verify: throughput is reported. A 16-process Python run reaches about 200k
   ZipCrypto guesses per second, which bounds what is worth attempting; when the
   remaining keyspace needs more, move to hashcat on a GPU.

5. Confirm before believing anything.

   ```
   node scripts/unzip.js <archive.zip> <password> [outdir]
   python scripts/ziptool.py decrypt <archive.zip> <password> <outdir>
   ```

   `unzip.js` re-decrypts every entry and checks integrity: CRC32 and length for
   ZipCrypto and AE-1, HMAC-SHA1-80 over the ciphertext for AES. A match is proof
   at 2^-32 odds for CRC32 and 2^-80 for the HMAC.

   Verify: the tool prints `VERIFY: PASS`; never report a password on the
   strength of the check byte or the AES password verifier alone.

6. Report the password, the extracted paths, and which verification passed.

## When a GPU actually helps

Measured and cited numbers, so the choice is not guesswork:

| Case | Rate | Source |
|---|---|---|
| This skill, 16 CPU processes, ZipCrypto | ~200k/s | measured here |
| hashcat `-m 17200` on an RTX 3090 | ~5.4 GH/s | published benchmark |
| hashcat `-m 13600` (WinZip AES) on an RTX 6000 Ada | ~16.7 MH/s | published benchmark |

The GPU is roughly 25,000x faster on PKZIP - but **only for archives hashcat can
load at all**: every entry's data must fit `MAX_DATA` of 320 KB, and modes 17200
and 17210 additionally require the complete deflate stream inline. A single
large entry therefore has no hashcat path, and john has no OpenCL kernel for
traditional ZipCrypto either (its GPU formats are `ZIP-opencl`, `7z-opencl`,
`rar-opencl`). Large single-entry ZipCrypto archives are CPU-bound; that is a
property of the tools, not of the hardware.

## Candidate strategy that actually paid off

Two archives from one source both opened with the same password, found in
john's bundled `password.lst` within seconds. The lesson generalizes:

1. Sibling archives first. Same publisher, same password.
2. The archive and file names are the next cheapest signal.
3. Digits before words, and short before long.
4. Only then general wordlists, and only then masks.
5. Every candidate is confirmed by full decryption, never by the cheap filter.

## Scripts

Standalone; run from anywhere. Pyzipper is needed only by the AES fixture
builder and the AES part of the self test.

| Script | Invocation | Purpose |
|---|---|---|
| `scripts/ziptool.py` | `detect` `hash` `verify` `decrypt` `check` `selftest` | classification, hash generation, cheap verification, full decrypt with CRC32 |
| `scripts/crack.py` | `dict` / `num` / `mask` | multi-process search, auto-detecting ZipCrypto or AES |
| `scripts/unzip.js` | `node unzip.js <archive> <pwd> [outdir]` | fast full decrypt of every entry; CRC32 and HMAC verification |
| `scripts/make_aes_fixtures.py` | `python make_aes_fixtures.py <outdir>` | builds WinZip AES fixtures with an independent implementation, for regression testing |

Use `unzip.js` for large archives: it decrypts 75 MB in about 2.5 s where the
Python path needs one to two minutes. Run `ziptool.py selftest` to prove the
implementation works before trusting it on real data; it builds its own
archives, checks the hash line, tests both correct and wrong passwords, and
covers AES end to end when pyzipper and node are present.

## Tool sources

Primary projects, usable as-is on Windows without a compiler:

- **hashcat** - https://github.com/hashcat/hashcat (MIT). GPU recovery.
  Binaries: https://hashcat.net/hashcat/ (`hashcat-7.1.2.7z`).
  Run it from its own directory or it fails with `./OpenCL/: No such file or directory`.
- **John the Ripper (jumbo)** - https://github.com/openwall/john.
  Windows build with `zip2john.exe`, `rar2john.exe`, `7z2john.pl`:
  `https://www.openwall.com/john/k/john-1.9.0-jumbo-1-win64.zip`.
- **bkcrack** - https://github.com/kimci86/bkcrack (zlib licence, Windows
  prebuilt packages on the releases page). Known-plaintext attack on ZipCrypto:
  12 bytes of known plaintext, at least 8 contiguous, recover the internal keys.

Other open-source projects worth knowing when the primary ones do not fit:
`agourlay/zip-password-finder` (Rust, ZIP ZipCrypto+AES and 7z AES-256),
`keyunluo/pkcrack` (maintained build of the original known-plaintext tool),
`fcrackzip` (classic CPU ZipCrypto), `philsmd/hc_to_7z` (hashcat hash back to
7z), `hashtopolis/server` (distributed hashcat orchestration).

Model-specific details, install notes, measured speeds and a graded source list:
`references/tools-and-links.md` and `references/sources.md`.

## Examples

Input: `帮我破解 C:\Users\me\Desktop\合集.zip` - one 70 MB stored MP4, ZipCrypto.

Output:
  detect -> `山水系列 (57).mp4 method=0 flags=0x0001 csize=73982784` -> ZipCrypto
  `crack.py dict` with the sibling archive's recovered password -> candidate in 3.5 s
  `unzip.js` -> `VERIFY: PASS - password is correct (1 file(s))`, CRC32 47cbda98
  matched, file written next to the archive

Input: `7-Zip keeps asking for a password on this zip and I never set one`

Output:
  detect -> `WinZip AES-256 (AE-2)`, method 99
  route -> `zip2john` for the hash, then hashcat `-m 13600` on a GPU
  after recovery `unzip.js` extracts it and confirms the HMAC-SHA1-80

Input: `破解一下这个 rar` -> out of scope here: RAR needs `rar2john` plus hashcat
`-m 12500` or `-m 13000`. Point at `references/other-formats.md` and say so.

## Verify

- `python scripts/ziptool.py selftest` prints `SELFTEST: PASS`.
- A recovered password is accepted only after `VERIFY: PASS` from `unzip.js` or
  `ziptool.py decrypt`.
- ZipCrypto: the extracted CRC32 equals the archive's recorded CRC32. AES: the
  HMAC-SHA1-80 matches, and for AE-1 the CRC32 matches too.
- A candidate that passed the cheap filter but failed the full check is a false
  positive. Report it as such, not as a result.
- Extracted files are re-readable: re-open the written file and recompute its
  CRC32 before declaring success.

## Known limits

- Pure Python drives ZipCrypto fast and AES only for short dictionaries; AES
  brute force belongs on a GPU.
- zip64 archives are rejected by the Python parser; `unzip.js` does not handle
  zip64 either.
- Archives whose entries use *different* passwords cannot be attacked as one
  unit; the scripts assume the first encrypted entry shares the password.
- Stored (method 0) entries give only a 1/256 cheap filter unless known
  plaintext is supplied with `--magic`.

## Failure paths

| Symptom | Cause | Action |
|---|---|---|
| thousands of candidates from a stored entry | only the 1/256 check byte filtered them | re-run with `--magic`, or confirm each candidate |
| hashcat refuses the hash | entry data exceeds `MAX_DATA` 320 KB | use john or `scripts/crack.py` |
| hashcat loads the hash but never hits | `-m 17200` needs the whole deflate stream inline | switch modes per `references/pkzip-hash-format.md` |
| hashcat says `No hashes loaded` for 17230 | that mode requires at least 3 entries | use 17200/17210 for a single entry |
| `./OpenCL/: No such file or directory` | hashcat started outside its own directory | re-run with the hashcat directory as cwd |
| AES verifier matched but HMAC failed | the 1/65536 false positive | reject the candidate, keep searching |
| extracted name looks like mojibake | Chinese archives store names in GBK with the UTF-8 flag unset | none needed, the scripts decode GBK first |
| `zip2john` emits a 150 MB hash line | it inlines all compressed data | use `-c` for the small checksum-only form |

## References

| File | Load when |
|---|---|
| `references/pkzip-hash-format.md` | hand-building a `$pkzip$` hash, debugging a mode that will not load, or needing the check-byte and known-plaintext rules |
| `references/tools-and-links.md` | choosing between hashcat, john and bkcrack; installing on Windows; checking measured speeds and licences |
| `references/sources.md` | needing to know how confident a claim is, or which official specification or paper backs it |
| `references/other-formats.md` | the archive turns out to be RAR, 7z or something else, or the job needs to scale out |
