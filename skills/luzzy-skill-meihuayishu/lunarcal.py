# -*- coding: utf-8 -*-
"""
lunarcal.py —— 公历 → 农历 / 年支 / 时辰 / 节气月 换算（梅花易数时间起卦四要素）

纯标准库，无第三方依赖。覆盖 1900-01-31 至 2100-12-31。

数据来源（置信度说明）
  lunarInfo / sTermInfo 两表转自社区通行历表 jjonline/calendar.js v1.0.3
  （201 项，1900-2100；含 2016-08-13 修订的 2033 闰月条目）。
  已用下列公开历表事实校验（--selftest 自动执行）：
    春节：2020-01-25、2023-01-22、2024-02-10、2025-01-29、2026-02-17 均为正月初一
    节日：2024-09-17、2025-10-06 为八月十五；2026-06-19 为五月初五
    闰月：1987 闰六月、1993 闰三月、2001 闰四月、2004 闰二月、2006 闰七月、
          2009 闰五月、2012 闰四月、2014 闰九月、2017 闰六月、2020 闰四月、
          2023 闰二月、2025 闰六月、2033 闰十一月
    节气：2024/2026 立春 2/4、2025 立春 2/3、2024 冬至 12/21、2026 冬至 12/22
  极早年（1900-1950）锚点较少；对其输出存疑时，按 sources.md 联网万年历核对农历日后再用。

用法（与 SKILL 约定一致）
  python3 lunarcal.py <年> <月> <日> <时> <分>    # 公历日期时刻 → 四要素
  python3 lunarcal.py                             # 不带参数 = 当前时刻
  python3 lunarcal.py --selftest                  # 内置数据自检

输出约定（供 agent 解析）
  年支 <序数>(<支名>) <干支年> [立春界说明]
  农历月 <序数>(<月名>)          # 闰月按本月数，标注〔闰〕
  农历日 <序数>(<日名>)
  时支 <序数>(<支名>) [时段]     # 23 点起为晚子时，默认不换农历日
  节气月 <序数>(<支名>月) [下一节]  # 寅月=1 … 丑月=12，按 12 节交节日分界
  四要素(A法·农历月): engine.py time <年支> <月> <日> <时支>
"""

import sys
from datetime import date, datetime

# ---------------------------------------------------------------------------
# 农历位表 1900-2100（201 项）：0x 位含义见函数 _leap_month/_leap_days/_month_days
# ---------------------------------------------------------------------------
_LUNAR_RAW = """
0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
0x06ca0,0x0b550,0x15355,0x04da0,0x0a5b0,0x14573,0x052b0,0x0a9a8,0x0e950,0x06aa0,
0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b6a0,0x195a6,
0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,
0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,
0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50,0x06b20,0x1a6c4,0x0aae0,
0x0a2e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05d55,0x056a0,0x0a6d0,0x055d4,
0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,
0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,
0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252,
0x0d520
"""

# 节气日表 1900-2100（201 项 × 30 位十六进制）：每年 6 组、每组 5 位编码 4 个
# 节气的「日」，解码规则见 term_day()；月 = (n+1)//2（n=1 小寒 … n=24 冬至）
_STERM_RAW = """
9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c3598082c95f8c965cc920f,97bd0b06bdb0722c965ce1cfcc920f,
b027097bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c359801ec95f8c965cc920f,97bd0b06bdb0722c965ce1cfcc920f,
b027097bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c359801ec95f8c965cc920f,97bd0b06bdb0722c965ce1cfcc920f,
b027097bd097c36b0b6fc9274c91aa,9778397bd19801ec9210c965cc920e,97b6b97bd19801ec95f8c965cc920f,97bd09801d98082c95f8e1cfcc920f,
97bd097bd097c36b0b6fc9210c8dc2,9778397bd197c36c9210c9274c91aa,97b6b97bd19801ec95f8c965cc920e,97bd09801d98082c95f8e1cfcc920f,
97bd097bd097c36b0b6fc9210c8dc2,9778397bd097c36c9210c9274c91aa,97b6b97bd19801ec95f8c965cc920e,97bcf97c3598082c95f8e1cfcc920f,
97bd097bd097c36b0b6fc9210c8dc2,9778397bd097c36c9210c9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c3598082c95f8c965cc920f,
97bd097bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c3598082c95f8c965cc920f,
97bd097bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c359801ec95f8c965cc920f,
97bd097bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c359801ec95f8c965cc920f,
97bd097bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,97bcf97c3598082c95f8c965cc920f,
97bd097bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9210c8dc2,9778397bd19801ec9210c9274c920e,97b6b97bd19801ec95f8c965cc920f,
97bd07f5307f595b0b0bc920fb0722,7f0e397bd097c36b0b6fc9210c8dc2,9778397bd097c36c9210c9274c920e,97b6b97bd19801ec95f8c965cc920f,
97bd07f5307f595b0b0bc920fb0722,7f0e397bd097c36b0b6fc9210c8dc2,9778397bd097c36c9210c9274c91aa,97b6b97bd19801ec9210c965cc920e,
97bd07f1487f595b0b0bc920fb0722,7f0e397bd097c36b0b6fc9210c8dc2,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,
97bcf7f1487f595b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,
97bcf7f1487f595b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,
97bcf7f1487f531b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c965cc920e,
97bcf7f1487f531b0b0bb0b6fb0722,7f0e397bd07f595b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,97b6b97bd19801ec9210c9274c920e,
97bcf7f0e47f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,9778397bd097c36b0b6fc9210c91aa,97b6b97bd197c36c9210c9274c920e,
97bcf7f0e47f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,9778397bd097c36b0b6fc9210c8dc2,9778397bd097c36c9210c9274c920e,
97b6b7f0e47f531b0723b0b6fb0722,7f0e37f5307f595b0b0bc920fb0722,7f0e397bd097c36b0b6fc9210c8dc2,9778397bd097c36b0b70c9274c91aa,
97b6b7f0e47f531b0723b0b6fb0721,7f0e37f1487f595b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc9210c8dc2,9778397bd097c36b0b6fc9274c91aa,
97b6b7f0e47f531b0723b0b6fb0721,7f0e27f1487f595b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,
97b6b7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,
97b6b7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,9778397bd097c36b0b6fc9274c91aa,
97b6b7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,9778397bd097c36b0b6fc9274c91aa,
97b6b7f0e47f531b0723b0787b0721,7f0e27f0e47f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,9778397bd097c36b0b6fc9210c91aa,
97b6b7f0e47f149b0723b0787b0721,7f0e27f0e47f531b0723b0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,9778397bd097c36b0b6fc9210c8dc2,
977837f0e37f149b0723b0787b0721,7f07e7f0e47f531b0723b0b6fb0722,7f0e37f5307f595b0b0bc920fb0722,7f0e397bd097c35b0b6fc9210c8dc2,
977837f0e37f14998082b0787b0721,7f07e7f0e47f531b0723b0b6fb0721,7f0e37f1487f595b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc9210c8dc2,
977837f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,
977837f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd097c35b0b6fc920fb0722,
977837f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,
977837f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,
977837f0e37f14998082b0787b06bd,7f07e7f0e47f149b0723b0787b0721,7f0e27f0e47f531b0b0bb0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,
977837f0e37f14998082b0723b06bd,7f07e7f0e37f149b0723b0787b0721,7f0e27f0e47f531b0723b0b6fb0722,7f0e397bd07f595b0b0bc920fb0722,
977837f0e37f14898082b0723b02d5,7ec967f0e37f14998082b0787b0721,7f07e7f0e47f531b0723b0b6fb0722,7f0e37f1487f595b0b0bb0b6fb0722,
7f0e37f0e37f14898082b0723b02d5,7ec967f0e37f14998082b0787b0721,7f07e7f0e47f531b0723b0b6fb0722,7f0e37f1487f531b0b0bb0b6fb0722,
7f0e37f0e37f14898082b0723b02d5,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e37f1487f531b0b0bb0b6fb0722,
7f0e37f0e37f14898082b072297c35,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,
7f0e37f0e37f14898082b072297c35,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,7f0e27f1487f531b0b0bb0b6fb0722,
7f0e37f0e366aa89801eb072297c35,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f149b0723b0787b0721,7f0e27f1487f531b0b0bb0b6fb0722,
7f0e37f0e366aa89801eb072297c35,7ec967f0e37f14998082b0723b06bd,7f07e7f0e47f149b0723b0787b0721,7f0e27f0e47f531b0723b0b6fb0722,
7f0e37f0e366aa89801eb072297c35,7ec967f0e37f14998082b0723b06bd,7f07e7f0e37f14998083b0787b0721,7f0e27f0e47f531b0723b0b6fb0722,
7f0e37f0e366aa89801eb072297c35,7ec967f0e37f14898082b0723b02d5,7f07e7f0e37f14998082b0787b0721,7f07e7f0e47f531b0723b0b6fb0722,
7f0e36665b66aa89801e9808297c35,665f67f0e37f14898082b0723b02d5,7ec967f0e37f14998082b0787b0721,7f07e7f0e47f531b0723b0b6fb0722,
7f0e36665b66a449801e9808297c35,665f67f0e37f14898082b0723b02d5,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,
7f0e36665b66a449801e9808297c35,665f67f0e37f14898082b072297c35,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,
7f0e26665b66a449801e9808297c35,665f67f0e37f1489801eb072297c35,7ec967f0e37f14998082b0787b06bd,7f07e7f0e47f531b0723b0b6fb0721,
7f0e27f1487f531b0b0bb0b6fb0722
"""

LUNAR_INFO = [int(x, 16) for x in _LUNAR_RAW.split(',')]
STERM_INFO = [x.strip() for x in _STERM_RAW.split(',') if x.strip()]

_STEMS = '甲乙丙丁戊己庚辛壬癸'
_BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
_TERM_NAMES = ['小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨',
               '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑',
               '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']
_MONTH_CN = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
_BASE = date(1900, 1, 31)   # 1900 年正月初一


# ---------------------------------------------------------------------------
# 农历位表解码
# ---------------------------------------------------------------------------
def _leap_month(y):
    """农历 y 年闰几月（0 = 无闰月）"""
    return LUNAR_INFO[y - 1900] & 0xF


def _leap_days(y):
    """农历 y 年闰月天数（无闰月为 0）"""
    if _leap_month(y):
        return 30 if LUNAR_INFO[y - 1900] & 0x10000 else 29
    return 0


def _month_days(y, m):
    """农历 y 年 m 月（非闰月）天数"""
    return 30 if LUNAR_INFO[y - 1900] & (0x10000 >> m) else 29


def _year_days(y):
    """农历 y 年总天数"""
    total, bit = 348, 0x8000
    while bit > 0x8:
        if LUNAR_INFO[y - 1900] & bit:
            total += 1
        bit >>= 1
    return total + _leap_days(y)


def solar2lunar(y, m, d):
    """公历 → 农历。返回 dict(year, month, day, is_leap)；超界抛 ValueError。"""
    if not (1900 <= y <= 2100):
        raise ValueError(f'仅支持 1900-2100 年，收到 {y}')
    cur = date(y, m, d)
    if cur < _BASE:
        raise ValueError('早于 1900-01-31（1900 年正月初一），超出数据范围')
    offset = (cur - _BASE).days
    i, temp = 1900, 0
    while i < 2101 and offset > 0:
        temp = _year_days(i)
        offset -= temp
        i += 1
    if offset < 0:
        offset += temp
        i -= 1
    l_year = i
    leap = _leap_month(l_year)
    is_leap, temp = False, 0
    i = 1
    while i < 13 and offset > 0:
        if leap > 0 and i == leap + 1 and not is_leap:
            i -= 1
            is_leap = True
            temp = _leap_days(l_year)
        else:
            temp = _month_days(l_year, i)
        if is_leap and i == leap + 1:
            is_leap = False
        offset -= temp
        i += 1
    if offset == 0 and leap > 0 and i == leap + 1:
        if is_leap:
            is_leap = False
        else:
            is_leap = True
            i -= 1
    if offset < 0:
        offset += temp
        i -= 1
    return {'year': l_year, 'month': i, 'day': offset + 1, 'is_leap': is_leap}


def day_cn(d):
    if d == 10:
        return '初十'
    if d == 20:
        return '二十'
    if d == 30:
        return '三十'
    return '初十廿卅'[d // 10] + '一二三四五六七八九十'[d % 10 - 1]


def ganzhi_year(lyear):
    """农历年序 → 干支名（如 2026 → 丙午）"""
    return _STEMS[(lyear - 4) % 10] + _BRANCHES[(lyear - 4) % 12]


def zhi_num(lyear):
    """农历年序 → 年支数 1-12（子1 … 亥12）"""
    return (lyear - 4) % 12 + 1


# ---------------------------------------------------------------------------
# 节气
# ---------------------------------------------------------------------------
def term_day(y, n):
    """公历 y 年第 n 个节气（1=小寒 … 3=立春 … 24=冬至）的「日」；月 = (n+1)//2。

    每年 30 位十六进制串分 6 组、每组 5 位，转十进制后恰为 6 位数字
    [日1][日2两位][日3][日4两位]（节为个位日、气为两位日，天然对齐）。
    """
    s = STERM_INFO[y - 1900]
    g, k = (n - 1) // 4, (n - 1) % 4
    info = str(int(s[g * 5:g * 5 + 5], 16))
    if k == 0:
        return int(info[0])
    if k == 1:
        return int(info[1:3])
    if k == 2:
        return int(info[3])
    return int(info[4:6])


def term_date(y, n):
    return date(y, (n + 1) // 2, term_day(y, n))


def lichun_date(y):
    """公历 y 年立春日期（年支分界用）"""
    return term_date(y, 3)


def nian_zhi_lichun(y, m, d):
    """立春界年支（本技能默认）：立春前属上一年。返回 (支数, 干支名, 说明)"""
    lc = lichun_date(y)
    cur = date(y, m, d)
    if cur < lc:
        ly = y - 1
        note = f'立春界: {y}-{lc.month:02d}-{lc.day:02d} 立春未到 → 属上一年 {ganzhi_year(ly)}'
    else:
        ly = y
        note = f'立春界: {y}-{lc.month:02d}-{lc.day:02d} 立春已过 → 属 {ganzhi_year(ly)}'
    return zhi_num(ly), ganzhi_year(ly), note


def jieqi_yue(y, m, d):
    """节气月（寅月=1 … 丑月=12），按 12 节交节日分界。返回 (序数, 支名, 下一节说明)"""
    yue_branch = '寅卯辰巳午未申酉戌亥子丑'
    cur = date(y, m, d)
    best = None
    for yy in (y - 1, y):
        for n in range(1, 25, 2):        # 奇数序为「节」
            if not (1900 <= yy <= 2100):
                continue
            t = term_date(yy, n)
            if t <= cur and (best is None or t > best[0]):
                best = (t, yy, n)
    if best is None:
        raise ValueError('节气计算超出数据范围')
    _, _, n = best
    num = ((n - 3) // 2) % 12 + 1
    # 下一节（提示交节日期）
    nxt = None
    for yy in (y, y + 1):
        for n2 in range(1, 25, 2):
            if not (1900 <= yy <= 2100):
                continue
            t = term_date(yy, n2)
            if t > cur and (nxt is None or t < nxt[0]):
                nxt = (t, _TERM_NAMES[n2 - 1])
    note = f'下一节 {nxt[1]} {nxt[0].isoformat()}' if nxt else ''
    return num, yue_branch[num - 1], note


# ---------------------------------------------------------------------------
# 时辰
# ---------------------------------------------------------------------------
def shichen(h):
    """小时(24 制) → (时支数 1-12, 支名, 时段串)"""
    num = ((h + 1) // 2) % 12 + 1
    name = _BRANCHES[num - 1]
    if name == '子':
        span = '23:00-00:59'
    else:
        lo = (num - 1) * 2 - 1
        span = f'{lo:02d}:00-{lo + 1:02d}:59'
    return num, name, span


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _fmt(y, m, d, hh, mi):
    lunar = solar2lunar(y, m, d)
    znum, gz, note = nian_zhi_lichun(y, m, d)
    mnum, mname, mnote = jieqi_yue(y, m, d)
    snum, sname, sspan = shichen(hh)
    leap_tag = '〔闰月，按本月数取〕' if lunar['is_leap'] else ''
    lines = [
        f'公历   {y:04d}-{m:02d}-{d:02d} {hh:02d}:{mi:02d}',
        f'年支   {znum}({_BRANCHES[znum - 1]}) {gz}年 [{note}]',
        f'农历月 {lunar["month"]}({_MONTH_CN[lunar["month"] - 1]}月){leap_tag}',
        f'农历日 {lunar["day"]}({day_cn(lunar["day"])})',
        f'时支   {snum}({sname}) [{sspan}]',
        f'节气月 {mnum}({mname}月) [{mnote}]',
    ]
    if lunar['is_leap']:
        lines.append('说明   闰月原文无明文，本表按本月数取（闰六月按 6）。')
    if hh == 23:
        lines.append('说明   23 点为晚子时；本技能默认不换农历日（当日农历日+子时），如从换日派请自行按次日农历日重算。')
    lines.append(f'四要素(A法·农历月): engine.py time {znum} {lunar["month"]} {lunar["day"]} {snum}')
    lines.append(f'      (B法·节气月): engine.py time {znum} {mnum} {lunar["day"]} {snum}   ← 变通，非原文月法')
    return '\n'.join(lines)


def _selftest():
    ok = True

    def chk(name, cond, detail=''):
        nonlocal ok
        print(('PASS ' if cond else 'FAIL ') + name + ('  ' + detail if detail and not cond else ''))
        ok = ok and cond

    chk('lunarInfo 共 201 项', len(LUNAR_INFO) == 201, f'实际 {len(LUNAR_INFO)}')
    chk('sTermInfo 共 201 项', len(STERM_INFO) == 201, f'实际 {len(STERM_INFO)}')
    chk('sTermInfo 均为 30 位十六进制', all(len(s) == 30 for s in STERM_INFO))
    for (yy, mm, dd) in [(2020, 1, 25), (2023, 1, 22), (2024, 2, 10), (2025, 1, 29), (2026, 2, 17)]:
        r = solar2lunar(yy, mm, dd)
        chk(f'{yy} 春节=正月初一', r['month'] == 1 and r['day'] == 1,
            f'实际 农历{r["month"]}月{r["day"]}日')
    r = solar2lunar(2024, 9, 17)
    chk('2024-09-17 中秋=八月十五', r['month'] == 8 and r['day'] == 15, f'实际 {r["month"]}月{r["day"]}')
    r = solar2lunar(2025, 10, 6)
    chk('2025-10-06 中秋=八月十五', r['month'] == 8 and r['day'] == 15, f'实际 {r["month"]}月{r["day"]}')
    r = solar2lunar(2026, 6, 19)
    chk('2026-06-19 端午=五月初五', r['month'] == 5 and r['day'] == 5, f'实际 {r["month"]}月{r["day"]}')
    for yy, lm in [(1987, 6), (1993, 3), (2001, 4), (2004, 2), (2006, 7), (2009, 5),
                   (2012, 4), (2014, 9), (2017, 6), (2020, 4), (2023, 2), (2025, 6), (2033, 11)]:
        chk(f'{yy} 闰{lm}月', _leap_month(yy) == lm, f'实际 闰{_leap_month(yy) or "无"}')
    chk('2024 立春=2/4', term_day(2024, 3) == 4, f'实际 {term_day(2024, 3)}')
    chk('2025 立春=2/3', term_day(2025, 3) == 3, f'实际 {term_day(2025, 3)}')
    chk('2026 立春=2/4', term_day(2026, 3) == 4, f'实际 {term_day(2026, 3)}')
    chk('1987 立春=2/4（源码文档例）', term_day(1987, 3) == 4, f'实际 {term_day(1987, 3)}')
    chk('2024 冬至=12/21', term_day(2024, 24) == 21, f'实际 {term_day(2024, 24)}')
    chk('2026 冬至=12/22', term_day(2026, 24) == 22, f'实际 {term_day(2026, 24)}')
    chk('09 时=巳时(6)', shichen(9)[0] == 6)
    chk('12 时=午时(7)', shichen(12)[0] == 7)
    chk('23 时=子时(1)', shichen(23)[0] == 1)
    chk('00 时=子时(1)', shichen(0)[0] == 1)
    print('自检结果:', '全部通过' if ok else '存在失败项！')
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == '--selftest':
        return _selftest()
    if argv:
        if len(argv) < 3:
            print('用法: python3 lunarcal.py <年> <月> <日> [时 [分]] | --selftest')
            return 2
        y, m, d = int(argv[0]), int(argv[1]), int(argv[2])
        hh = int(argv[3]) if len(argv) > 3 else 12
        mi = int(argv[4]) if len(argv) > 4 else 0
    else:
        now = datetime.now()
        y, m, d, hh, mi = now.year, now.month, now.day, now.hour, now.minute
    try:
        print(_fmt(y, m, d, hh, mi))
    except ValueError as e:
        print(f'错误: {e}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
