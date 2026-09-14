# -*- coding: utf-8 -*-
"""
engine.py —— 梅花易数起卦引擎（本技能家族根目录；部署后即 /workspace/meihua/engine.py）

只做起卦：先天八卦取余 → 六十四卦查表 → 互卦 → 变卦 → 体用 → 五行生克。
解卦引文由 agent 按 SKILL 流程查 references/，引擎只输出卦象与引文指引。

规则出处（《梅花易数》卷一，全文见 references/meihua-juan1.md）
  卦以八除：数 ÷8 取余作卦，整除取 8 = 坤。
  爻以六除：总数 ÷6 取余作动爻，整除取 6 = 上爻动。
  年月日时起卦：年+月+日 ÷8 为上卦；再加时 ÷8 为下卦；年月日时总数 ÷6 为动爻。
  互卦起例：去初爻与上爻，中间四爻分作两卦——三四五爻为上互（上卦）、二三四爻为下互（下卦）。
  体用：动爻所在之卦为用卦，另一卦为体卦（卷二体用总诀；动爻在内卦则用为下卦）。

用法
  python3 engine.py number <数1> <数2> [<数3>]      # 报数：2数动爻=(数1+数2)÷6；3数动爻=数3÷6
  python3 engine.py time <年支数> <月数> <农历日> <时支数>
  python3 engine.py bihua <上卦总笔画> <下卦总笔画> [<动爻总数>]
                                                   # 笔画：2参动爻=(上+下)÷6；3参动爻=第3参÷6
                                                   # （原文物数占例加时法：第3参传 数1+数2+时辰数）
  python3 engine.py help

边界（与 meihua-baoshu-qigua SKILL 边界表一致）
  0 → ÷8 取 8（坤）；整除 ÷8 取 8、÷6 取 6；负数取绝对值；小数取整数部分。
"""

import json
import os
import sys

_NUM2TRI = {1: '111', 2: '110', 3: '101', 4: '100', 5: '011', 6: '010', 7: '001', 8: '000'}
# 三爻位串自下而上；(名, 先天数, 五行)
_TRI = {'111': ('乾', 1, '金'), '110': ('兑', 2, '金'), '101': ('离', 3, '火'),
        '100': ('震', 4, '木'), '011': ('巽', 5, '木'), '010': ('坎', 6, '水'),
        '001': ('艮', 7, '土'), '000': ('坤', 8, '土')}
_TRI_XIANG = {'乾': '天', '兑': '泽', '离': '火', '震': '雷',
              '巽': '风', '坎': '水', '艮': '山', '坤': '地'}
_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}   # 木生火…
_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}     # 木克土…
_POS = {1: '初', 2: '二', 3: '三', 4: '四', 5: '五', 6: '上'}

_BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_BASE, 'gua_index.json'), encoding='utf-8') as _f:
    _DB = json.load(_f)
_BY_BITS = {g['爻']: g for g in _DB['卦']}


def mod8(n):
    """卦以八除：整除取 8（坤）"""
    r = n % 8
    return 8 if r == 0 else r


def mod6(n):
    """爻以六除：整除取 6（上爻动）"""
    r = n % 6
    return 6 if r == 0 else r


def _to_int(s):
    """小数取整数部分；负数取绝对值（数值清洗在解析层完成）"""
    return abs(int(float(s)))


def _tri_of(num):
    bits = _NUM2TRI[num]
    name, _, wx = _TRI[bits]
    return name, num, wx


def _full_name(upper, lower, gua_name):
    if upper == lower:
        return f'{upper}为{_TRI_XIANG[upper]}'
    return f'{_TRI_XIANG[upper]}{_TRI_XIANG[lower]}{gua_name}'


def _relation(other_wx, ti_wx):
    """他卦五行相对体卦的关系"""
    if other_wx == ti_wx:
        return '比和'
    if _SHENG[other_wx] == ti_wx:
        return '生体（吉）'
    if _KE[other_wx] == ti_wx:
        return '克体（凶）'
    if _SHENG[ti_wx] == other_wx:
        return '体生（泄）'
    return '体克（耗）'


def _line_label(bits, pos):
    """动爻爻题：阳爻称九、阴爻称六（初九 / 九二 / 六三 / 九四 / 六五 / 上九）"""
    yao = '九' if bits[pos - 1] == '1' else '六'
    if pos == 1:
        return f'初{yao}'
    if pos == 6:
        return f'上{yao}'
    return f'{yao}{_POS[pos]}'


def _yao_labels(bits):
    return '、'.join(_line_label(bits, p) for p in range(1, 7))


def analyze(upper_num, lower_num, moving, how_desc, div_notes):
    ub, lb = _NUM2TRI[upper_num], _NUM2TRI[lower_num]
    bits = lb + ub                      # 六爻位串自下而上：下卦在前
    ben = _BY_BITS[bits]
    upper, _, uwx = _TRI[ub]
    lower, _, lwx = _TRI[lb]

    # 互卦：二三四爻为下互、三四五爻为上互；重卦以上互为上卦、下互为下卦
    xbits = bits[1:4] + bits[2:5]
    hu = _BY_BITS[xbits]
    hu_up, _, hu_uwx = _TRI[bits[2:5]]
    hu_lo, _, hu_lwx = _TRI[bits[1:4]]

    # 变卦：动爻阴阳互变
    vbits = list(bits)
    vbits[moving - 1] = '0' if bits[moving - 1] == '1' else '1'
    vbits = ''.join(vbits)
    bian = _BY_BITS[vbits]

    # 体用：动爻在内卦（1-3爻）→ 用为下卦、体为上卦；在外卦（4-6爻）反之
    if moving <= 3:
        ti_name, ti_num, ti_wx = upper, upper_num, uwx
        yong_name, yong_num, yong_wx = lower, lower_num, lwx
        ti_side = '上卦（外）'
        yong_side = '下卦（内）'
    else:
        ti_name, ti_num, ti_wx = lower, lower_num, lwx
        yong_name, yong_num, yong_wx = upper, upper_num, uwx
        ti_side = '下卦（内）'
        yong_side = '上卦（外）'

    ref_file = 'zhouyi-shangjing.md' if ben['经'] == '上经' else 'zhouyi-xiajing.md'
    out = []
    out.append('=== 梅花易数起卦结果 ===')
    out.append(f'[输入] {how_desc}')
    for note in div_notes:
        out.append(f'[取卦] {note}')
    out.append(f'[本卦] 第{ben["序"]}卦 {_full_name(upper, lower, ben["卦名"])} {ben["卦画"]}'
               f'（上{upper}{uwx}·下{lower}{lwx}）')
    out.append(f'       六爻自下而上：{_yao_labels(bits)}')
    out.append(f'[动爻] 第{moving}爻（{_line_label(bits, moving)}）· '
               f'{"内卦" if moving <= 3 else "外卦"}')
    out.append(f'[变卦] {_full_name(_TRI[vbits[3:]][0], _TRI[vbits[:3]][0], bian["卦名"])} '
               f'{bian["卦画"]}（第{bian["序"]}卦）')
    out.append(f'[互卦] 上互{hu_up}({_TRI[bits[2:5]][2]})·下互{hu_lo}({_TRI[bits[1:4]][2]}) '
               f'→ {_full_name(hu_up, hu_lo, hu["卦名"])} {hu["卦画"]}（第{hu["序"]}卦）')
    out.append(f'[体用] 动爻所在为用：体={ti_name}({ti_wx})[{ti_side}] '
               f'用={yong_name}({yong_wx})[{yong_side}]')
    out.append(f'[生克] 用·{yong_name}{yong_wx} 对 体·{ti_name}{ti_wx}：{_relation(yong_wx, ti_wx)}')
    out.append(f'       上互·{hu_up}{hu_uwx} 对 体：{_relation(hu_uwx, ti_wx)}'
               f'；下互·{hu_lo}{hu_lwx} 对 体：{_relation(hu_lwx, ti_wx)}'
               f'；变卦·{bian["卦名"]} 对 体：{_relation(_TRI[vbits[3:]][2], ti_wx)}')
    out.append('[引文] 动爻爻辞：《周易·' + ben['卦名'] + '》' + _line_label(bits, moving)
               + f' → references/{ref_file}「{ben["卦名"]}」条')
    out.append('       变卦卦辞：《周易·' + bian['卦名'] + '》 → 同文件「' + bian['卦名'] + '」条')
    out.append('[核验] ' + ben['url'])
    return '\n'.join(out)


def _div8_note(prefix, n, tri_num):
    r = n % 8
    head = '整除取8' if r == 0 else f'余{r}'
    name, _, wx = _TRI[_NUM2TRI[tri_num]]
    return f'{prefix}：{n} ÷8 {head} → {name}（{wx}）'


def _div6_note(prefix, n, moving):
    r = n % 6
    head = '整除取6' if r == 0 else f'余{r}'
    return f'{prefix}：{n} ÷6 {head} → 第{moving}爻'


def cmd_number(n1, n2, n3=None):
    up, lo = mod8(n1), mod8(n2)
    notes = [_div8_note('上卦', n1, up), _div8_note('下卦', n2, lo)]
    if n3 is None:
        total = n1 + n2
        moving = mod6(total)
        desc = f'报数起卦：数1={n1}（上卦），数2={n2}（下卦）'
        notes.append(_div6_note('动爻：（数1+数2）=' + str(total), total, moving))
    else:
        moving = mod6(n3)
        desc = f'报数起卦（3数）：数1={n1}（上卦），数2={n2}（下卦），数3={n3}（取动爻）'
        notes.append(_div6_note('动爻', n3, moving))
    return analyze(up, lo, moving, desc, notes)


def cmd_time(yz, mo, dy, sz):
    s1 = yz + mo + dy
    s2 = s1 + sz
    up, lo, moving = mod8(s1), mod8(s2), mod6(s2)
    desc = f'时间起卦：年支={yz}，月={mo}，日={dy}，时支={sz}'
    notes = [_div8_note(f'上卦：年月日（{yz}+{mo}+{dy}）=' + str(s1), s1, up),
             _div8_note(f'下卦：加时（{s1}+{sz}）=' + str(s2), s2, lo),
             _div6_note('动爻：年月日时总数', s2, moving)]
    return analyze(up, lo, moving, desc, notes)


def cmd_bihua(up_strokes, lo_strokes, n3=None):
    up, lo = mod8(up_strokes), mod8(lo_strokes)
    notes = [_div8_note('上卦', up_strokes, up), _div8_note('下卦', lo_strokes, lo)]
    if n3 is None:
        total = up_strokes + lo_strokes
        moving = mod6(total)
        desc = f'笔画起卦：上卦总笔画={up_strokes}，下卦总笔画={lo_strokes}'
        notes.append(_div6_note('动爻：（上+下）=' + str(total), total, moving))
    else:
        moving = mod6(n3)
        desc = (f'笔画起卦（3参）：上卦总笔画={up_strokes}，下卦总笔画={lo_strokes}，'
                f'第3参={n3}（÷6取动爻；若为「上+下+时辰」总数即原文物数占例加时法）')
        notes.append(_div6_note('动爻', n3, moving))
    return analyze(up, lo, moving, desc, notes)


def _check_range(label, v, lo, hi):
    if not (lo <= v <= hi):
        print(f'〔警告〕{label}={v} 超出常理范围（{lo}-{hi}），已照算；请核对输入。', file=sys.stderr)


HELP = __doc__


def main(argv):
    if not argv or argv[0] in ('help', '-h', '--help'):
        print(HELP)
        return 0
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == 'number':
            if len(args) not in (2, 3):
                print('用法: engine.py number <数1> <数2> [<数3>]')
                return 2
            vals = [_to_int(a) for a in args]
            if len(vals) == 2:
                _check_range('数1', vals[0], 1, 9999)
                _check_range('数2', vals[1], 1, 9999)
                print(cmd_number(vals[0], vals[1]))
            else:
                print(cmd_number(vals[0], vals[1], vals[2]))
        elif cmd == 'time':
            if len(args) != 4:
                print('用法: engine.py time <年支数> <月数> <农历日> <时支数>')
                return 2
            yz, mo, dy, sz = [_to_int(a) for a in args]
            _check_range('年支数', yz, 1, 12)
            _check_range('月数', mo, 1, 12)
            _check_range('农历日', dy, 1, 30)
            _check_range('时支数', sz, 1, 12)
            print(cmd_time(yz, mo, dy, sz))
        elif cmd == 'bihua':
            if len(args) not in (2, 3):
                print('用法: engine.py bihua <上卦总笔画> <下卦总笔画> [<动爻总数>]')
                return 2
            vals = [_to_int(a) for a in args]
            if len(vals) == 2:
                print(cmd_bihua(vals[0], vals[1]))
            else:
                print(cmd_bihua(vals[0], vals[1], vals[2]))
        else:
            print(f'未知命令 {cmd}。可用: number / time / bihua / help')
            return 2
    except ValueError:
        print('参数须为数字（小数取整、负数取绝对值）。', file=sys.stderr)
        return 2
    except KeyError:
        print('内部错误：卦位串未命中六十四卦表（gua_index.json）。', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
