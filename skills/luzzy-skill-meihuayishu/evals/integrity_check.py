# -*- coding: utf-8 -*-
"""
integrity_check.py —— 仓库结构完整性检查（AGENTS.md §1 R5/R6/R7 的机器门槛）

检查项：必备文件齐备 / SKILL frontmatter name 合规（编排器=luzzy-skill-meihuayishu，子技能=目录名）/ SKILL ≤500 行 /
版本四处一致（4×SKILL + evals.json + README 徽章）/ gua_index 64 项爻位唯一、
卦画连续、爻位↔上下卦↔先天数交叉一致 / 上经30下经34 / 评测文件有效 / 引文抽验。

用法：python3 evals/integrity_check.py    （退出码 0 = 全过）
维护规则见仓库根 AGENTS.md。
"""
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ok = True


def chk(name, cond, detail=''):
    global _ok
    print(('PASS ' if cond else 'FAIL ') + name + (f'  [{detail}]' if detail and not cond else ''))
    _ok = _ok and cond


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


# ── 1. 必备文件 ────────────────────────────────────────────────
REQUIRED = [
    'SKILL.md', 'engine.py', 'lunarcal.py', 'gua_index.json', 'README.md',
    'AGENTS.md', 'LICENSE', '.gitignore',
    'meihua-time-divination/SKILL.md', 'meihua-name-divination/SKILL.md',
    'meihua-baoshu-qigua/SKILL.md',
    'references/README.md', 'references/sources.md',
    'references/meihua-juan1.md', 'references/meihua-juan2.md', 'references/meihua-juan3.md',
    'references/zhouyi-shangjing.md', 'references/zhouyi-xiajing.md',
    'evals/evals.json', 'evals/run.py',
]
missing = [p for p in REQUIRED if not os.path.isfile(os.path.join(ROOT, p))]
chk('必备文件齐备（20 项）', not missing, f'缺失 {missing}')

# ── 2. SKILL frontmatter 与行数 ───────────────────────────────
SKILLS = ['SKILL.md', 'meihua-time-divination/SKILL.md',
          'meihua-name-divination/SKILL.md', 'meihua-baoshu-qigua/SKILL.md']
for p in SKILLS:
    text = read(p)
    expected = 'luzzy-skill-meihuayishu' if p == 'SKILL.md' else \
        os.path.basename(os.path.dirname(os.path.abspath(os.path.join(ROOT, p))))
    m = re.search(r'^name:\s*(\S+)', text, re.M)
    chk(f'{p} name 合规（编排器=luzzy-skill-meihuayishu，子技能=目录名）',
        m and m.group(1) == expected,
        f'name={m.group(1) if m else None} 预期={expected}')
    lines = text.count('\n') + 1
    chk(f'{p} ≤500 行', lines <= 500, f'{lines} 行')
    chk(f'{p} 含 Verify 清单', '## Verify' in text)
    chk(f'{p} description 含反触发或从属说明',
        ('Do NOT use' in text) or ('仅覆盖起卦环节' in text))

# ── 3. 版本四处一致 ───────────────────────────────────────────
versions = {}
for p in SKILLS:
    m = re.search(r'version:\s*"?([\d.]+)"?', read(p))
    versions[p] = m.group(1) if m else None
versions['evals/evals.json'] = json.loads(read('evals/evals.json')).get('版本')
m = re.search(r'version-([\d.]+)-', read('README.md'))
versions['README.md 徽章'] = m.group(1) if m else None
chk('版本四处一致（4×SKILL + evals + README）',
    len({v for v in versions.values()}) == 1 and None not in versions.values(),
    str(versions))

# ── 4. gua_index.json 结构 ────────────────────────────────────
db = json.loads(read('gua_index.json'))['卦']
NUM = {'乾': 1, '兑': 2, '离': 3, '震': 4, '巽': 5, '坎': 6, '艮': 7, '坤': 8}
TRI = {'111': '乾', '110': '兑', '101': '离', '100': '震',
       '011': '巽', '010': '坎', '001': '艮', '000': '坤'}
chk('64 卦', len(db) == 64, str(len(db)))
chk('卦序 1-64 连续', [g['序'] for g in db] == list(range(1, 65)))
chk('爻位串唯一', len({g['爻'] for g in db}) == 64)
chk('卦画连续 U+4DC0-4DFF', all(g['卦画'] == chr(0x4DC0 + i) for i, g in enumerate(db)))
chk('slug 唯一且小写',
    len({g['slug'] for g in db}) == 64 and all(g['slug'] == g['slug'].lower() for g in db))
chk('上经 30 / 下经 34',
    sum(1 for g in db if g['经'] == '上经') == 30 and sum(1 for g in db if g['经'] == '下经') == 34)
bad = [g['卦名'] for g in db
       if not (TRI[g['爻'][:3]] == g['下卦'] and NUM[TRI[g['爻'][:3]]] == g['下卦数']
               and TRI[g['爻'][3:]] == g['上卦'] and NUM[TRI[g['爻'][3:]]] == g['上卦数'])]
chk('爻位↔上下卦↔先天数 交叉一致', not bad, str(bad))
chk('全部卦带 ctext 核验 URL', all(g['url'].startswith('https://ctext.org/book-of-changes/') for g in db))

# ── 5. 评测文件有效 ───────────────────────────────────────────
ev = json.loads(read('evals/evals.json'))
chk('评测用例 ≥16 组', len(ev.get('用例', [])) >= 16, str(len(ev.get('用例', []))))
chk('评测含原书占例组', any(c.get('组') == '原书占例' for c in ev.get('用例', [])))

# ── 6. 引文抽验（SKILL 示例所引经文必须真实存在） ─────────────
sh, xj = read('references/zhouyi-shangjing.md'), read('references/zhouyi-xiajing.md')
QUOTES = [
    ('蒙九二', '包蒙吉；纳妇吉；子克家'),
    ('剥六三', '剥之，无咎'),
    ('颐初九', '舍尔灵龟，观我朵颐，凶'),
    ('艮卦辞', '艮其背，不获其身，行其庭，不见其人，无咎'),
    ('师九二', '在师中吉，无咎，王三锡命'),
]
for label, key in QUOTES:
    chk(f'引文存在：{label}', key in sh + xj)

print('\n完整性检查:', '全部通过' if _ok else '存在失败项——不得发布！')
sys.exit(0 if _ok else 1)
