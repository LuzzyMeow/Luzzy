# -*- coding: utf-8 -*-
"""ZIP archive toolkit: detect encryption, build cracker hashes, verify, decrypt.

Commands
    detect  <zip>                        classify encryption, suggest a route
    hash    <zip> [--full]               emit a hashcat/john $pkzip$ line
    verify  <zip> <password>             cheap check (check byte + structure)
    decrypt <zip> <password> <outdir>    full decrypt + CRC32 verify + write
    check   <file>                       size + CRC32 of an arbitrary file
    selftest [--tmp DIR]                 build test archives, prove the crypto round-trips

Exit codes: 0 = ok / 1 = not verified / 2 = usage or format problem.

Only ZipCrypto (legacy PKWARE) is decrypted here. WinZip AES is detected and
routed to hashcat -m 13600 / john instead; use 7-Zip or WinRAR to unpack AES
archives once the password is known.
"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

# --------------------------------------------------------------- ZipCrypto


def _crc_table():
    tab = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if (c & 1) else (c >> 1)
        tab.append(c & 0xFFFFFFFF)
    return tab


CRCTAB = _crc_table()


class ZipCrypto:
    """PKWARE traditional encryption. Validated against hashcat's PKZIP kernel."""

    def __init__(self, password):
        self.k0 = 0x12345678
        self.k1 = 0x23456789
        self.k2 = 0x34567890
        for b in password:
            self._update(b)

    def _update(self, byte):
        tab = CRCTAB
        k0 = self.k0
        k1 = self.k1
        k2 = self.k2
        k0 = ((k0 >> 8) ^ tab[(k0 ^ byte) & 0xFF]) & 0xFFFFFFFF
        k1 = (k1 + (k0 & 0xFF)) & 0xFFFFFFFF
        k1 = (k1 * 134775813 + 1) & 0xFFFFFFFF
        k2 = ((k2 >> 8) ^ tab[(k2 ^ ((k1 >> 24) & 0xFF)) & 0xFF]) & 0xFFFFFFFF
        self.k0, self.k1, self.k2 = k0, k1, k2

    def _stream_byte(self):
        temp = (self.k2 | 2) & 0xFFFF
        return ((temp * (temp ^ 1)) >> 8) & 0xFF

    def encrypt(self, data):
        out = bytearray(len(data))
        for i, b in enumerate(data):
            out[i] = b ^ self._stream_byte()
            self._update(b)
        return bytes(out)

    def decrypt(self, data):
        out = bytearray(len(data))
        for i, b in enumerate(data):
            p = b ^ self._stream_byte()
            out[i] = p
            self._update(p)
        return bytes(out)


def _u2(raw, off):
    return struct.unpack_from("<H", raw, off)[0]


def _u4(raw, off):
    return struct.unpack_from("<I", raw, off)[0]


# ------------------------------------------------------------ zip parsing


def _decode_name(raw_name, flags):
    if flags & 0x800:
        return raw_name.decode("utf-8", "replace")
    for enc in ("gbk", "cp437"):
        try:
            return raw_name.encode("cp437").decode(enc)
        except Exception:
            continue
    return raw_name.decode("cp437", "replace")


def parse_entries(path):
    """Return every central-directory entry with the fields needed for attacks."""
    raw = open(path, "rb").read()
    i = raw.rfind(b"PK\x05\x06")
    if i < 0:
        raise SystemExit("no EOCD record - not a plain single-disk zip")
    n_total = _u2(raw, i + 10)
    cd_off = _u4(raw, i + 16)
    if cd_off == 0xFFFFFFFF or n_total == 0xFFFF:
        raise SystemExit("zip64 archive - this helper does not handle it")

    entries = []
    off = cd_off
    for _ in range(n_total):
        if _u4(raw, off) != 0x02014B50:
            break
        vneed = _u2(raw, off + 6)
        flags = _u2(raw, off + 8)
        method = _u2(raw, off + 10)
        mtime = _u2(raw, off + 12)
        crc = _u4(raw, off + 16)
        csize = _u4(raw, off + 20)
        usize = _u4(raw, off + 24)
        fnlen = _u2(raw, off + 28)
        exlen = _u2(raw, off + 30)
        cmlen = _u2(raw, off + 32)
        loff = _u4(raw, off + 42)
        name_raw = raw[off + 46: off + 46 + fnlen]
        extra = raw[off + 46 + fnlen: off + 46 + fnlen + exlen]

        aes = aes_strength = aes_vendor = None
        real_method = method
        p = 0
        while p + 4 <= len(extra):
            hid = _u2(extra, p)
            hsz = _u2(extra, p + 2)
            if hid == 0x9901 and hsz >= 7:
                aes_vendor = _u2(extra, p + 4)       # 1 = AE-1 (keeps CRC), 2 = AE-2
                aes_strength = extra[p + 8]          # 1/2/3 -> 128/192/256 bit
                real_method = _u2(extra, p + 9)      # compression hidden behind method 99
                aes = {1: 128, 2: 192, 3: 256}.get(aes_strength, aes_strength)
            p += 4 + hsz

        lfn = _u2(raw, loff + 26)
        lex = _u2(raw, loff + 28)
        entries.append({
            "name": _decode_name(name_raw, flags),
            "version": vneed, "flags": flags, "method": method,
            "real_method": real_method, "mtime": mtime,
            "crc": crc, "csize": csize, "usize": usize,
            "aes_bits": aes, "aes_strength": aes_strength, "aes_vendor": aes_vendor,
            "data_off": loff + 30 + lfn + lex, "loff": loff,
            "fnlen": lfn, "exlen": lex, "raw": raw, "path": path,
            "encrypted": bool(flags & 0x0001),
        })
        off += 46 + fnlen + exlen + cmlen
    return entries


# WinZip AES strength enum -> salt length / key length
AES_SALT = {1: 8, 2: 12, 3: 16}
AES_KEY = {1: 16, 2: 24, 3: 32}


def first_attackable(entries):
    """First entry attackable with the ZipCrypto primitives in this file."""
    for e in entries:
        if e["encrypted"] and e["method"] in (0, 8) and not e["aes_bits"]:
            return e
    return None


def first_entry(entries):
    """First encrypted entry, whatever the scheme."""
    for e in entries:
        if e["encrypted"]:
            return e
    return None


def aes_verifier(entry, password):
    """WinZip AES quick check: the last 2 bytes of the PBKDF2 output.

    Only 16 bits of filtering, and pure Python pays the full 1000-round PBKDF2
    per candidate. Use it for dictionaries, never for brute force.
    """
    import hashlib
    salt_len = AES_SALT[entry["aes_strength"]]
    key_len = AES_KEY[entry["aes_strength"]]
    off = entry["data_off"]
    salt = entry["raw"][off:off + salt_len]
    pv_stored = entry["raw"][off + salt_len:off + salt_len + 2]
    km = hashlib.pbkdf2_hmac("sha1", password, salt, 1000, key_len * 2 + 2)
    return km[-2:] == pv_stored


# ----------------------------------------------------------- hash building


def checksum_bytes(entry):
    """CS as zip2john computes it: 2 bytes, big-endian order."""
    if entry["flags"] & 0x0008:          # sizes unknown -> derived from timestamp
        v = entry["mtime"]
        return "%02x%02x" % ((v >> 8) & 0xFF, v & 0xFF), "timestamp"
    crc = entry["crc"]
    return "%02x%02x" % ((crc >> 24) & 0xFF, (crc >> 16) & 0xFF), "crc"


def gen_hash(path, full=False, ndata=36):
    """Emit a $pkzip$ / $pkzip2$ line accepted by hashcat and john."""
    entries = parse_entries(path)
    e = first_attackable(entries)
    if e is None:
        raise SystemExit("no ZipCrypto-encrypted component-0/8 entry found")
    cs, src = checksum_bytes(e)
    check_bytes = 1 if e["version"] >= 20 else 2
    if full:
        n = e["csize"]
        data = e["raw"][e["data_off"]:e["data_off"] + n]
        src_t = e["mtime"] if (e["flags"] & 0x0008) else e["crc"]
        tc = "%02x%02x" % ((src_t >> 24) & 0xFF, (src_t >> 16) & 0xFF)
        offex = 30 + e["fnlen"] + e["exlen"]
        line = ("$pkzip2$1*%d*2*0*%x*%x*%x*0*%x*%d*%x*%s*%s*%s*$/pkzip2$" % (
            check_bytes, e["csize"], e["usize"], e["crc"], offex, e["method"],
            n, cs, tc, data.hex()))
    else:
        n = min(ndata, e["csize"])
        data = e["raw"][e["data_off"]:e["data_off"] + n]
        line = "$pkzip$1*%d*1*0*%d*%x*%s*%s*$/pkzip$" % (
            check_bytes, e["method"], n, cs, data.hex())
    return line, e, cs, src


# ------------------------------------------------------------- verification

MAGICS = [
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF87a", "GIF"), (b"GIF89a", "GIF"),
    (b"PK\x03\x04", "ZIP"), (b"Rar!\x1a\x07", "RAR"),
    (b"7z\xbc\xaf\x27\x1c", "7z"), (b"\x1f\x8b", "GZIP"),
    (b"BZh", "BZIP2"), (b"\xfd7zXZ", "XZ"), (b"%PDF", "PDF"),
    (b"\x7fELF", "ELF"), (b"MZ", "PE"), (b"\xd0\xcf\x11\xe0", "OLE"),
    (b"ID3", "MP3"), (b"OggS", "OGG"), (b"RIFF", "RIFF"),
    (b"fLaC", "FLAC"), (b"\x1a\x45\xdf\xa3", "Matroska"),
]


def looks_like_a_file(body):
    """Cheap structural sanity check on decrypted bytes."""
    if len(body) < 16:
        return False, "too short"
    for sig, name in MAGICS:
        if body.startswith(sig):
            return True, name
    if body[4:8] == b"ftyp":
        return True, "MP4"
    if body[0:1] == b"\x00" and body[1:4].isalpha() and body[4:8].isalnum():
        return True, "MP4-like box"
    return False, "no known signature"


def verify(path, password, npfx=131072):
    """Cheap candidate check.

    Returns (verdict, detail, info) with verdict one of:
      "no"        definitely not this password
      "plausible" check byte and stream structure agree, but the decrypted
                  content carries no recognisable file signature
      "likely"    the same, plus a recognised file signature
    Only the full CRC32 check in decrypt() or unzip.js settles it.
    """
    entries = parse_entries(path)
    e = first_attackable(entries)
    if isinstance(password, str):
        password = password.encode("utf-8")
    if e is None:
        a = first_entry(entries)
        if a is None:
            return "no", "no encrypted entry in this archive", {"check_ok": False}
        if not a["aes_bits"]:
            return "no", "entry uses unsupported method %d" % a["method"], {"check_ok": False}
        ok = aes_verifier(a, password)
        info = {"check_ok": ok, "scheme": "WinZip AES-%d" % a["aes_bits"],
                "inflated": None, "head": ""}
        if not ok:
            return "no", "password verifier mismatch", info
        return ("plausible",
                "verifier matched (1/65536 by chance); confirm with unzip.js, which "
                "checks the HMAC-SHA1-80", info)
    n = min(npfx, e["csize"])
    whole_entry = n >= e["csize"]
    blob = e["raw"][e["data_off"]:e["data_off"] + n]
    plain = ZipCrypto(password).decrypt(blob)
    check_ok = plain[11] == ((e["crc"] >> 24) & 0xFF)
    if e["version"] < 20:
        check_ok = check_ok and plain[10] == ((e["crc"] >> 16) & 0xFF)
    body = plain[12:]
    info = {"check_ok": check_ok}
    if not check_ok:
        return "no", "check byte mismatch", info

    struct_ok, detail = True, ""
    if e["method"] == 8:
        d = zlib.decompressobj(-15)
        try:
            res = d.decompress(body)
            info["inflated"] = len(res)
            info["eof_at_prefix"] = d.eof
            if d.eof:
                # a complete stream is only legitimate when the whole entry is here
                if not whole_entry or len(res) != e["usize"]:
                    return "no", "stream ended inside the prefix", info
            elif len(res) < 64:
                struct_ok, detail = False, "too little inflated output"
            body = res
        except zlib.error as ex:
            return "no", "inflate failed: %s" % ex, info
    else:
        info["inflated"] = len(body)
        if not whole_entry and len(body) < 64:
            struct_ok, detail = False, "too little data"
    info["head"] = body[:16].hex(" ")
    if not struct_ok:
        return "no", detail, info

    magic_ok, magic_why = looks_like_a_file(body)
    if magic_ok:
        return "likely", "recognised %s" % magic_why, info
    if e["method"] == 8:
        return "plausible", "deflate stream consistent, no file signature", info
    return "plausible", "check byte only (stored entry, no known plaintext)", info


def decrypt(path, password, outdir):
    """Full decrypt + CRC32 verification + write. Slow in Python on big files."""
    if isinstance(password, str):
        password = password.encode("utf-8")
    written, failed = [], []
    for e in parse_entries(path):
        if e["aes_bits"]:
            failed.append((e["name"], "WinZip AES-%d: run unzip.js, this pure-Python "
                                      "path has no AES" % e["aes_bits"]))
            continue
        if not e["encrypted"] or e["method"] not in (0, 8):
            continue
        blob = e["raw"][e["data_off"]:e["data_off"] + e["csize"]]
        plain = ZipCrypto(password).decrypt(blob)
        if plain[11] != ((e["crc"] >> 24) & 0xFF):
            failed.append((e["name"], "check byte mismatch"))
            continue
        body = plain[12:]
        try:
            data = zlib.decompress(body, -15) if e["method"] == 8 else body
        except zlib.error as ex:
            failed.append((e["name"], "inflate: %s" % ex))
            continue
        got = zlib.crc32(data) & 0xFFFFFFFF
        if got != e["crc"] or len(data) != e["usize"]:
            failed.append((e["name"], "crc %08x != %08x" % (got, e["crc"])))
            continue
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir, os.path.basename(e["name"]))
        with open(out, "wb") as f:
            f.write(data)
        written.append((out, len(data)))
    return written, failed


# ------------------------------------------------------------- self test


def create_test_zip(path, password, filename="payload.bin", payload=None, method=8):
    """Build a real ZipCrypto archive so the implementation can be cross-checked."""
    if payload is None:
        payload = b"zip-password-recovery self test\n" * 40
    if isinstance(password, str):
        password = password.encode("utf-8")
    if isinstance(filename, str):
        filename = filename.encode("utf-8")
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    if method == 8:
        co = zlib.compressobj(6, zlib.DEFLATED, -15)
        comp = co.compress(payload) + co.flush()
    else:
        comp = payload
    header = bytearray(os.urandom(10))
    header.append((crc >> 16) & 0xFF)
    header.append((crc >> 24) & 0xFF)
    zc = ZipCrypto(password)
    blob = zc.encrypt(bytes(header)) + zc.encrypt(comp)
    dos_time, dos_date, flags, ver = 0x7000, 0x5900, 0x0001, 20
    local = struct.pack("<IHHHHHIIIHH", 0x04034B50, ver, flags, method,
                        dos_time, dos_date, crc, len(blob), len(payload),
                        len(filename), 0)
    body = local + filename + blob
    cd = (struct.pack("<I", 0x02014B50) + struct.pack("<HH", ver, ver)
          + struct.pack("<HHHH", flags, method, dos_time, dos_date)
          + struct.pack("<III", crc, len(blob), len(payload))
          + struct.pack("<HHH", len(filename), 0, 0)
          + struct.pack("<HH", 0, 0) + struct.pack("<II", 0, 0))
    cd_blob = cd + filename
    eocd = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, 1, 1,
                       len(cd_blob), len(body), 0)
    with open(path, "wb") as f:
        f.write(body + cd_blob + eocd)
    return path


def selftest(tmpdir):
    """Build real archives and prove classification, hashing and decryption work."""
    os.makedirs(tmpdir, exist_ok=True)
    signed = b"\x89PNG\r\n\x1a\n" + b"payload for the round trip test\n" * 60
    unsigned = b"no signature here, just text\n" * 80
    cases = [
        ("deflate-signed", 8, "test123", signed),
        ("stored-signed", 0, "store-me", signed),
        ("deflate-unsigned", 8, "plain-pw", unsigned),
    ]
    ok = True
    for i, (label, method, pwd, payload) in enumerate(cases):
        zp = os.path.join(tmpdir, "selftest_%d_%s.zip" % (i, label))
        create_test_zip(zp, pwd, "payload.bin", payload, method=method)
        line, e, cs, src = gen_hash(zp)
        v_ok, why_ok, _ = verify(zp, pwd)
        v_bad, why_bad, _ = verify(zp, pwd + "x")
        written, failed = decrypt(zp, pwd, os.path.join(tmpdir, "out_%d" % i))
        good = (v_ok in ("likely", "plausible") and v_bad == "no"
                and len(written) == 1 and not failed)
        ok = ok and good
        print("%-17s method=%d  %s" % (label, method, zp))
        print("  hash    : %s" % line[:78])
        print("  cs=%s (%s)" % (cs, src))
        print("  verify  : correct=%s (%s)  wrong=%s" % (v_ok, why_ok, v_bad))
        print("  decrypt : written=%d failed=%d" % (len(written), len(failed)))

    # optional AES coverage: pyzipper builds the fixture, node unwraps it
    aes_zip = os.path.join(tmpdir, "selftest_aes256.zip")
    try:
        import pyzipper
        with pyzipper.AESZipFile(aes_zip, "w", compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(b"aes-pw")
            zf.setencryption(pyzipper.WZ_AES, nbits=256)
            zf.writestr("payload.png", signed)
    except ImportError:
        print("AES                 skipped: install pyzipper (pip install pyzipper) or run")
        print("                    scripts/make_aes_fixtures.py and check with unzip.js")
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    v_ok, why_ok, _ = verify(aes_zip, "aes-pw")
    v_bad, _, _ = verify(aes_zip, "aes-pw-x")
    node = shutil.which("node")
    js = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unzip.js")
    node_ok = None
    if node:
        r_good = subprocess.run([node, js, aes_zip, "aes-pw",
                                 os.path.join(tmpdir, "out_aes")], capture_output=True)
        r_bad = subprocess.run([node, js, aes_zip, "aes-pw-x",
                                os.path.join(tmpdir, "out_aes_bad")], capture_output=True)
        node_ok = (r_good.returncode == 0 and r_bad.returncode != 0)
    aes_case = (v_ok == "plausible" and v_bad == "no" and node_ok is not False)
    ok = ok and aes_case
    print("aes-256             method=99  %s" % aes_zip)
    print("  verify  : correct=%s (%s)  wrong=%s" % (v_ok, why_ok, v_bad))
    print("  unzip.js: %s" % ("PASS" if node_ok else
                              ("skipped (node not found)" if node_ok is None else "FAIL")))
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ------------------------------------------------------------------- main


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]

    if cmd == "detect":
        for e in parse_entries(argv[2]):
            if e["aes_bits"]:
                kind = "WinZip AES-%d (AE-%d)" % (e["aes_bits"], e["aes_vendor"] or 1)
                route = ("recover with hashcat -m 13600 (GPU) or john; once known, "
                         "scripts/unzip.js extracts and verifies it by HMAC-SHA1-80")
            elif e["encrypted"]:
                kind = "ZipCrypto (legacy)"
                route = "scripts/crack.py, john+zip2john, or bkcrack with known plaintext"
            else:
                kind = "not encrypted"
                route = "just extract it"
            print("%-40s method=%d flags=%#06x csize=%d usize=%d"
                  % (e["name"][:40], e["method"], e["flags"], e["csize"], e["usize"]))
            print("    encryption : %s" % kind)
            print("    route      : %s" % route)
        return 0

    if cmd == "hash":
        line, e, cs, src = gen_hash(argv[2], full="--full" in argv)
        print("entry   : %s" % e["name"])
        print("method  : %d   version=%d flags=%#06x" % (e["method"], e["version"], e["flags"]))
        print("crc32   : %08x  csize=%d usize=%d" % (e["crc"], e["csize"], e["usize"]))
        print("cs      : %s (from %s)" % (cs, src))
        print("hash    : %s" % line)
        return 0

    if cmd == "verify":
        verdict, why, info = verify(argv[2], argv[3])
        print("check byte : %s" % info.get("check_ok"))
        print("inflated   : %s bytes" % info.get("inflated"))
        print("head hex   : %s" % info.get("head", ""))
        print("assessment : %s - %s" % (verdict, why))
        if verdict != "likely":
            print("             confirm first: python ziptool.py decrypt <zip> <pw> <outdir>")
            print("                            node unzip.js <zip> <pw> [outdir]")
        return 0 if verdict != "no" else 1

    if cmd == "decrypt":
        written, failed = decrypt(argv[2], argv[3], argv[4])
        for out, size in written:
            print("OK   %s (%d bytes)" % (out, size))
        for name, why in failed:
            print("FAIL %s : %s" % (name, why))
        print("VERIFY: %s" % ("PASS" if written and not failed else "INCOMPLETE"))
        return 0 if written and not failed else 1

    if cmd == "check":
        d = open(argv[2], "rb").read()
        print("file  : %s" % argv[2])
        print("size  : %d" % len(d))
        print("crc32 : %08x" % (zlib.crc32(d) & 0xFFFFFFFF))
        print("head  : %s" % d[:16].hex(" "))
        return 0

    if cmd == "selftest":
        if "--tmp" in argv:
            tmp = os.path.abspath(argv[argv.index("--tmp") + 1])
        else:
            tmp = tempfile.mkdtemp(prefix="ziptool-selftest-")
        return selftest(tmp)

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
