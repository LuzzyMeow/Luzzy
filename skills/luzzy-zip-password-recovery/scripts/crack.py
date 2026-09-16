# -*- coding: utf-8 -*-
"""Multi-process ZipCrypto cracker: dictionary, numeric and mask attacks.

Filter chain, cheapest first:
  1. check byte - decrypt the 12-byte header; byte[11] must equal CRC>>24 (~1/256 pass)
  2. structure  - deflate: inflate the decrypted prefix and reject a stream that ends
                  inside the prefix (a real archive cannot); stored: match known
                  plaintext (--magic) or the built-in file-signature table
  3. full CRC32 - NOT done here. Every reported candidate must be confirmed with
                  `ziptool.py decrypt` or `unzip.js`; a 1/256 false positive is normal.

Usage
    python crack.py dict <zip> <wordlist> [wordlist ...] [--magic HEX] [--off N]
    python crack.py num  <zip> <digits> [--prefix TEXT] [--magic HEX] [--off N]
    python crack.py mask <zip> <charset> <length> [--magic HEX] [--off N]

Options
    --magic HEX   known plaintext bytes at the start of the file body (after the
                  12-byte encryption header). Kills the 1/256 false positives on
                  stored entries, where no deflate stream is available to check.
    --off N       offset of --magic inside the body (default 0)
    --no-filter   disable step 2 entirely (expect a flood of false positives)

Examples
    python crack.py dict secret.zip rockyou.txt
    python crack.py num  secret.zip 8
    python crack.py mask secret.zip 0123456789abcdef 6
    python crack.py dict video.zip rockyou.txt --magic 0000002066747970
"""
import argparse
import multiprocessing as mp
import os
import sys
import time
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ziptool import (CRCTAB, parse_entries, first_attackable, first_entry,  # noqa: E402
                     AES_SALT, AES_KEY, MAGICS)

T = {}


def _init(zpath, magic_hex, off, use_filter):
    entries = parse_entries(zpath)
    e = first_attackable(entries)
    T["aes"] = None
    T["scheme"] = "ZipCrypto"
    if e is None:
        e = first_entry(entries)
        if e is None:
            raise SystemExit("no encrypted entry in this archive")
        if not e["aes_bits"]:
            raise SystemExit("entry uses unsupported compression method %d" % e["method"])
        salt_len = AES_SALT[e["aes_strength"]]
        key_len = AES_KEY[e["aes_strength"]]
        off0 = e["data_off"]
        T["aes"] = {
            "salt": e["raw"][off0:off0 + salt_len],
            "pv": e["raw"][off0 + salt_len:off0 + salt_len + 2],
            "dklen": key_len * 2 + 2,
        }
        T["scheme"] = "WinZip AES-%d" % e["aes_bits"]
        return
    T["ct"] = e["raw"][e["data_off"]:e["data_off"] + 4096]
    T["want"] = (e["crc"] >> 24) & 0xFF
    T["method"] = e["method"]
    T["one_check_byte"] = e["version"] >= 20     # version >= 20 validates byte 11 only
    T["want10"] = (e["crc"] >> 16) & 0xFF
    T["usize"] = e["usize"]
    T["small"] = e["csize"] <= 4096              # whole entry fits inside the prefix
    T["magic"] = bytes.fromhex(magic_hex) if magic_hex else None
    T["off"] = off
    T["filter"] = use_filter


def _keys(pwd):
    tab = CRCTAB
    k0, k1, k2 = 0x12345678, 0x23456789, 0x34567890
    for ch in pwd:
        k0 = ((k0 >> 8) ^ tab[(k0 ^ ch) & 0xFF]) & 0xFFFFFFFF
        k1 = (k1 + (k0 & 0xFF)) & 0xFFFFFFFF
        k1 = (k1 * 134775813 + 1) & 0xFFFFFFFF
        k2 = ((k2 >> 8) ^ tab[(k2 ^ ((k1 >> 24) & 0xFF)) & 0xFF]) & 0xFFFFFFFF
    return k0, k1, k2


def test_check_byte(pwd):
    tab = CRCTAB
    k0, k1, k2 = _keys(pwd)
    ct = T["ct"]
    n = 12 if len(ct) >= 12 else len(ct)
    p = 0
    for i in range(n):
        temp = (k2 | 2) & 0xFFFF
        p = ct[i] ^ (((temp * (temp ^ 1)) >> 8) & 0xFF)
        k0 = ((k0 >> 8) ^ tab[(k0 ^ p) & 0xFF]) & 0xFFFFFFFF
        k1 = (k1 + (k0 & 0xFF)) & 0xFFFFFFFF
        k1 = (k1 * 134775813 + 1) & 0xFFFFFFFF
        k2 = ((k2 >> 8) ^ tab[(k2 ^ ((k1 >> 24) & 0xFF)) & 0xFF]) & 0xFFFFFFFF
        if i == 10 and not T["one_check_byte"] and p != T["want10"]:
            return False
    return p == T["want"]


def _decrypt_prefix(pwd):
    tab = CRCTAB
    k0, k1, k2 = _keys(pwd)
    ct = T["ct"]
    out = bytearray(len(ct))
    for i in range(len(ct)):
        temp = (k2 | 2) & 0xFFFF
        p = ct[i] ^ (((temp * (temp ^ 1)) >> 8) & 0xFF)
        out[i] = p
        k0 = ((k0 >> 8) ^ tab[(k0 ^ p) & 0xFF]) & 0xFFFFFFFF
        k1 = (k1 + (k0 & 0xFF)) & 0xFFFFFFFF
        k1 = (k1 * 134775813 + 1) & 0xFFFFFFFF
        k2 = ((k2 >> 8) ^ tab[(k2 ^ ((k1 >> 24) & 0xFF)) & 0xFF]) & 0xFFFFFFFF
    return bytes(out[12:])


def structure_ok(pwd):
    if not T["filter"]:
        return True
    body = _decrypt_prefix(pwd)
    if T["method"] == 8:
        d = zlib.decompressobj(-15)
        try:
            res = d.decompress(body)
        except zlib.error:
            return False
        if d.eof:
            # a complete deflate stream is only legitimate when the whole entry
            # fits inside the prefix; otherwise the real stream cannot have ended
            if not T["small"] or len(res) != T["usize"]:
                return False
        elif len(res) < 64:
            return False
        body = res
    if T["magic"] is not None:
        off, mag = T["off"], T["magic"]
        return body[off:off + len(mag)] == mag
    if T["method"] == 0:
        if any(body.startswith(sig) for sig, _ in MAGICS):
            return True
        if body[4:8] == b"ftyp":
            return True
        if body[0:1] == b"\x00" and body[1:4].isalpha() and body[4:8].isalnum():
            return True
        return False
    return True


def hit(pwd):
    if T["aes"]:
        import hashlib
        a = T["aes"]
        km = hashlib.pbkdf2_hmac("sha1", pwd, a["salt"], 1000, a["dklen"])
        return km[-2:] == a["pv"]
    return test_check_byte(pwd) and structure_ok(pwd)


def w_dict(lines):
    out = []
    for item in lines:
        pwd = item.rstrip(b"\r\n")
        if pwd and hit(pwd):
            out.append(pwd)
    return out


def w_num(args):
    start, end, width, prefix = args
    out = []
    fmt = b"%s%0" + str(width).encode() + b"d"
    for i in range(start, end):
        pwd = fmt % (prefix, i)
        if hit(pwd):
            out.append(pwd)
    return out


def w_mask(args):
    start, end, charset, length = args
    out = []
    base = len(charset)
    for i in range(start, end):
        n = i
        chars = bytearray(length)
        for j in range(length - 1, -1, -1):
            chars[j] = charset[n % base]
            n //= base
        if hit(bytes(chars)):
            out.append(bytes(chars))
    return out


def _report(pwds):
    print("--- candidates passing the cheap filters ---")
    for p in pwds:
        for enc in ("utf-8", "gbk"):
            try:
                print("  %r  (%s)" % (p, p.decode(enc)))
                break
            except Exception:
                continue
    print("CONFIRM every candidate before trusting it:")
    print("  python ziptool.py decrypt <zip> <password> <outdir>")
    print("  node unzip.js <zip> <password> [outdir]")


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    for name in ("dict", "num", "mask"):
        s = sub.add_parser(name)
        s.add_argument("zip")
        s.add_argument("rest", nargs="+")
        s.add_argument("--magic", default=None)
        s.add_argument("--off", type=int, default=0)
        s.add_argument("--no-filter", action="store_true")
    a = ap.parse_args()

    mp.set_start_method("spawn", force=True)
    args = (a.zip, a.magic, a.off, not a.no_filter)
    _init(*args)
    nproc = min(16, os.cpu_count() or 4)

    if T["aes"]:
        print("scheme  : WinZip AES - pure Python can only test the 2-byte password "
              "verifier")
        print("check   : verifier match passes 1/65536 by chance, and 1000 PBKDF2 rounds "
              "per candidate make this")
        print("          roughly a thousand times slower than ZipCrypto. Fine for "
              "dictionaries, useless for brute force.")
        print("          A GPU (hashcat -m 13600) is the right tool for anything wider.")
        print("CONFIRM candidates with: node scripts/unzip.js <archive> <password> [outdir]")
    else:
        e = first_attackable(parse_entries(a.zip))
        print("target  : %s  entry=%s method=%d" % (a.zip, e["name"], e["method"]))
        print("check   : crc=%08x -> byte[11] must be %02x (this filter alone passes 1/256)"
              % (e["crc"], T["want"]))
        if not T["filter"]:
            print("WARNING : --no-filter, expect a flood of false positives")

    if a.mode == "dict":
        lines = []
        for p in a.rest:
            lines.extend(open(p, "rb").read().split(b"\n"))
        print("mode    : dict, %d candidates from %d file(s)" % (len(lines), len(a.rest)))
        step = max(1, len(lines) // (nproc * 4))
        chunks = [lines[i:i + step] for i in range(0, len(lines), step)]
        worker = w_dict
    elif a.mode == "num":
        width = int(a.rest[0])
        prefix = a.rest[1].encode() if len(a.rest) > 1 else b""
        total = 10 ** width
        step = max(1, total // (nproc * 8))
        chunks = [(i, min(i + step, total), width, prefix) for i in range(0, total, step)]
        print("mode    : numeric width=%d prefix=%r space=%d" % (width, prefix, total))
        worker = w_num
    else:
        charset = a.rest[0].encode()
        length = int(a.rest[1])
        total = len(charset) ** length
        step = max(1, total // (nproc * 8))
        chunks = [(i, min(i + step, total), charset, length)
                  for i in range(0, total, step)]
        print("mode    : mask charset=%r len=%d space=%d" % (charset, length, total))
        worker = w_mask

    t0 = time.time()
    found = []
    with mp.Pool(processes=nproc, initializer=_init, initargs=args) as pool:
        try:
            for res in pool.imap_unordered(worker, chunks):
                if res:
                    found.extend(res)
                    break
        except KeyboardInterrupt:
            pool.terminate()
    dt = time.time() - t0
    print("elapsed : %.1f s over %d workers" % (dt, nproc))
    _report(found) if found else print("no candidate found in this keyspace")
    return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
