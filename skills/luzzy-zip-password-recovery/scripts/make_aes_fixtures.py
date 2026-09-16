# -*- coding: utf-8 -*-
"""Build WinZip-AES test archives with an independent implementation (pyzipper).

Used only to validate scripts/unzip.js. Not needed at runtime.

    python make_aes_fixtures.py <outdir>
"""
import os
import sys

import pyzipper

CASES = [
    # (name, bits, compression, payload)
    ("aes128-deflate", 128, pyzipper.ZIP_DEFLATED, None),
    ("aes192-deflate", 192, pyzipper.ZIP_DEFLATED, None),
    ("aes256-deflate", 256, pyzipper.ZIP_DEFLATED, None),
    ("aes256-stored", 256, pyzipper.ZIP_STORED, None),
]

PASSWORD = b"aes-test-pw"
SIGNED = b"\x89PNG\r\n\x1a\n" + b"aes fixture payload\n" * 200


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "..", ".fixtures")
    os.makedirs(outdir, exist_ok=True)
    for name, bits, comp, _ in CASES:
        p = os.path.join(outdir, name + ".zip")
        with pyzipper.AESZipFile(p, "w", compression=comp,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(PASSWORD)
            zf.setencryption(pyzipper.WZ_AES, nbits=bits)
            zf.writestr("payload.png", SIGNED)
        print("%s  bits=%d  comp=%s" % (p, bits, comp))
    print("password:", PASSWORD.decode())
    print("outdir:", outdir)


if __name__ == "__main__":
    main()
