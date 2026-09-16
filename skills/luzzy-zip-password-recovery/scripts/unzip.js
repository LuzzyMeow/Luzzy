'use strict';
// Archive decryptor: ZipCrypto (legacy PKWARE) and WinZip AES (AE-1 / AE-2).
// parse -> decrypt -> verify -> inflate -> write. Needs only node:crypto + node:zlib.
//
//   node unzip.js <archive> <password> [outdir]
//
// Exits 0 only when every entry passed its integrity check:
//   ZipCrypto    CRC32 and length match the header
//   WinZip AES   HMAC-SHA1-80 over the ciphertext matches, plus CRC32 for AE-1
// A non-zero exit means the password is wrong or the archive is damaged.
//
// AES details follow the WinZip AE-1/AE-2 specification:
//   key material = PBKDF2-HMAC-SHA1(password, salt, 1000, 2*keyLen + 2)
//   encKey = km[:keyLen]   macKey = km[keyLen:2*keyLen]   pv = km[2*keyLen:]
//   data = AES-CTR with a 128-bit LITTLE-ENDIAN counter starting at 1
//   auth = HMAC-SHA1(macKey, ciphertext) truncated to 10 bytes
// The 2-byte password verifier filters wrong passwords at only 1/65536, so the
// HMAC decides. Never trust the verifier alone.

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

const SRC = process.argv[2];
const PWD = process.argv[3];
if (!SRC || !PWD) {
  console.error('usage: node unzip.js <archive> <password> [outdir]');
  process.exit(2);
}
const OUTDIR = process.argv[4] ||
  path.join(path.dirname(SRC), path.basename(SRC, path.extname(SRC)) + '_解压');
const pwd = Buffer.from(PWD, 'utf8');

const CRCTAB = new Uint32Array(256);
for (let i = 0; i < 256; i++) {
  let c = i;
  for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
  CRCTAB[i] = c >>> 0;
}
function crc32(buf) {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) c = (c >>> 8) ^ CRCTAB[(c ^ buf[i]) & 0xFF];
  return (c ^ 0xFFFFFFFF) >>> 0;
}

// ---------------------------------------------------------------- AES-CTR

const AES_SALT = { 1: 8, 2: 12, 3: 16 };
const AES_KEY = { 1: 16, 2: 24, 3: 32 };

function aesKeys(password, salt, keyLen) {
  const km = crypto.pbkdf2Sync(password, salt, 1000, keyLen * 2 + 2, 'sha1');
  return {
    encKey: km.subarray(0, keyLen),
    macKey: km.subarray(keyLen, keyLen * 2),
    pv: km.subarray(keyLen * 2),
  };
}

function counterBlocks(startValue, blocks) {
  const ctr = Buffer.alloc(blocks * 16);
  let v = BigInt(startValue);
  for (let i = 0; i < 16; i++) { ctr[i] = Number(v & 0xFFn); v >>= 8n; }
  for (let b = 1; b < blocks; b++) {
    ctr.copy(ctr, b * 16, (b - 1) * 16, b * 16);
    for (let i = b * 16; i < (b + 1) * 16; i++) {
      if (ctr[i] === 0xFF) ctr[i] = 0; else { ctr[i]++; break; }
    }
  }
  return ctr;
}

// the AES-CTR keystream is AES-ECB applied to the counter blocks
function ctrKeystream(key, startBlock, blocks) {
  const c = crypto.createCipheriv('aes-' + (key.length * 8) + '-ecb', key, null);
  c.setAutoPadding(false);
  return Buffer.concat([c.update(counterBlocks(startBlock, blocks)), c.final()]);
}

function aesCtrDecrypt(key, data) {
  const out = Buffer.allocUnsafe(data.length);
  const CHUNK = 1 << 16;                       // 64 KiB of data per batch
  for (let off = 0; off < data.length; off += CHUNK) {
    const len = Math.min(CHUNK, data.length - off);
    const ks = ctrKeystream(key, off / 16 + 1, Math.ceil(len / 16));
    for (let i = 0; i < len; i++) out[off + i] = data[off + i] ^ ks[i];
  }
  return out;
}

// --------------------------------------------------------------- ZipCrypto

function zipCryptoDecrypt(password, data) {
  let k0 = 0x12345678, k1 = 0x23456789, k2 = 0x34567890;
  const upd = (b) => {
    k0 = ((k0 >>> 8) ^ CRCTAB[(k0 ^ b) & 0xFF]) >>> 0;
    k1 = (k1 + (k0 & 0xFF)) >>> 0;
    k1 = (Math.imul(k1, 134775813) + 1) >>> 0;
    k2 = ((k2 >>> 8) ^ CRCTAB[(k2 ^ ((k1 >>> 24) & 0xFF)) & 0xFF]) >>> 0;
  };
  for (let i = 0; i < password.length; i++) upd(password[i]);
  const out = Buffer.allocUnsafe(data.length);
  for (let i = 0; i < data.length; i++) {
    const temp = (k2 | 2) & 0xFFFF;
    const ks = (Math.imul(temp, temp ^ 1) >>> 8) & 0xFF;
    const p = data[i] ^ ks;
    out[i] = p;
    upd(p);
  }
  return out;
}

// ------------------------------------------------------------------ parse

const buf = fs.readFileSync(SRC);
let eocd = -1;
for (let i = buf.length - 22; i >= 0; i--) {
  if (buf.readUInt32LE(i) === 0x06054B50) { eocd = i; break; }
}
if (eocd < 0) { console.error('no EOCD record - not a plain single-disk zip'); process.exit(2); }

const total = buf.readUInt16LE(eocd + 10);
let cdOff = buf.readUInt32LE(eocd + 16);
const entries = [];
for (let i = 0; i < total; i++) {
  if (buf.readUInt32LE(cdOff) !== 0x02014B50) break;
  const flags = buf.readUInt16LE(cdOff + 8);
  const method = buf.readUInt16LE(cdOff + 10);
  const crc = buf.readUInt32LE(cdOff + 16);
  const csize = buf.readUInt32LE(cdOff + 20);
  const usize = buf.readUInt32LE(cdOff + 24);
  const fnlen = buf.readUInt16LE(cdOff + 28);
  const exlen = buf.readUInt16LE(cdOff + 30);
  const cmlen = buf.readUInt16LE(cdOff + 32);
  const loff = buf.readUInt32LE(cdOff + 42);
  const nameRaw = buf.subarray(cdOff + 46, cdOff + 46 + fnlen);
  const extra = buf.subarray(cdOff + 46 + fnlen, cdOff + 46 + fnlen + exlen);

  let aes = null, realMethod = method;
  for (let p = 0; p + 4 <= extra.length;) {
    const hid = extra.readUInt16LE(p), hsz = extra.readUInt16LE(p + 2);
    if (hid === 0x9901 && hsz >= 7) {
      aes = { vendorVersion: extra.readUInt16LE(p + 4), strength: extra[p + 8] };
      realMethod = extra.readUInt16LE(p + 9);
    }
    p += 4 + hsz;
  }
  let name;
  try { name = new TextDecoder((flags & 0x800) ? 'utf-8' : 'gbk').decode(nameRaw); }
  catch (e) { name = 'entry_' + i + '.bin'; }

  const lfn = buf.readUInt16LE(loff + 26);
  const lex = buf.readUInt16LE(loff + 28);
  entries.push({
    name, flags, method, realMethod, crc, csize, usize, aes,
    dataOff: loff + 30 + lfn + lex,
    encrypted: (flags & 1) === 1,
  });
  cdOff += 46 + fnlen + exlen + cmlen;
}

console.log('archive :', SRC);
console.log('entries :', entries.length);

let okCount = 0, failCount = 0;
const t0 = Date.now();

for (const e of entries) {
  const scheme = e.aes ? 'AES-' + (AES_KEY[e.aes.strength] * 8)
    : (e.encrypted ? 'ZipCrypto' : 'plain');
  const raw = buf.subarray(e.dataOff, e.dataOff + e.csize);

  let comp = null, note = '';

  if (e.aes) {
    const saltLen = AES_SALT[e.aes.strength];
    const keyLen = AES_KEY[e.aes.strength];
    if (raw.length < saltLen + 12) {
      console.log('FAIL  ' + e.name + ' : truncated AES entry');
      failCount++; continue;
    }
    const salt = raw.subarray(0, saltLen);
    const pvStored = raw.subarray(saltLen, saltLen + 2);
    const ct = raw.subarray(saltLen + 2, raw.length - 10);
    const authStored = raw.subarray(raw.length - 10);
    const { encKey, macKey, pv } = aesKeys(pwd, salt, keyLen);
    if (!pv.equals(pvStored)) {
      console.log('FAIL  ' + e.name + ' : password verifier mismatch (wrong password)');
      failCount++; continue;
    }
    const auth = crypto.createHmac('sha1', macKey).update(ct).digest().subarray(0, 10);
    if (!auth.equals(authStored)) {
      console.log('FAIL  ' + e.name + ' : HMAC-SHA1-80 mismatch (1/65536 verifier collision)');
      failCount++; continue;
    }
    comp = aesCtrDecrypt(encKey, ct);
    note = 'AE-' + (e.aes.vendorVersion === 2 ? '2' : '1') + ' hmac ok';
  } else if (e.encrypted) {
    const plain = zipCryptoDecrypt(pwd, raw);
    if (plain[11] !== ((e.crc >> 24) & 0xFF)) {
      console.log('FAIL  ' + e.name + ' : ZipCrypto check byte mismatch');
      failCount++; continue;
    }
    comp = plain.subarray(12);
    note = 'check byte ok';
  } else {
    comp = raw;
    note = 'not encrypted';
  }

  let data;
  try {
    data = (e.realMethod === 8)
      ? zlib.inflateRawSync(comp, { maxOutputLength: e.usize + 4096 })
      : comp;
  } catch (err) {
    console.log('FAIL  ' + e.name + ' : inflate: ' + err.message);
    failCount++; continue;
  }

  // AE-2 stores 0 in the CRC field; only AE-1 and ZipCrypto carry a real CRC
  const got = crc32(data);
  const crcOk = (e.crc === 0) || (got === e.crc);
  const sizeOk = data.length === e.usize;
  if (!crcOk || !sizeOk) {
    console.log('FAIL  ' + e.name + ' : crc ' + got.toString(16).padStart(8, '0') +
      ' vs ' + e.crc.toString(16).padStart(8, '0') + ', length ' + data.length +
      ' vs ' + e.usize);
    failCount++; continue;
  }

  const out = path.join(OUTDIR, e.name);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, data);
  console.log('OK    ' + e.name + '  ' + scheme + '  ' + data.length + ' bytes  ' + note);
  console.log('      -> ' + out);
  okCount++;
}

console.log('elapsed : ' + (Date.now() - t0) + ' ms');
console.log('VERIFY  : ' + (failCount === 0 && okCount > 0
  ? 'PASS - password is correct (' + okCount + ' file(s))'
  : 'FAIL - ' + failCount + ' failed, ' + okCount + ' ok'));
process.exit(failCount === 0 && okCount > 0 ? 0 : 1);
