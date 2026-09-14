# -*- coding: utf-8 -*-
"""
run.py —— 梅花易数技能家族回归评测运行器

执行 evals.json 全部用例：engine.py 用例逐条断言期望子串；
lunarcal 用例通过导入 lunarcal 模块复用其 CLI 逻辑。

用法（在本目录或技能根目录均可）：
  python3 evals/run.py        # 或 python evals/run.py
退出码 0 = 全部通过。
"""

import io
import json
import os
import subprocess
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import lunarcal  # noqa: E402


def run_engine(args):
    return subprocess.run(
        [sys.executable, os.path.join(_ROOT, 'engine.py')] + args,
        capture_output=True, text=True, encoding='utf-8', errors='replace')


def run_case(case):
    name = case['名']
    if 'args' in case:
        proc = run_engine(case['args'])
        out = proc.stdout + proc.stderr
        if proc.returncode != 0:
            return False, f'退出码 {proc.returncode}：{out.strip()[:300]}'
    elif case.get('cmd_py') == 'lunarcal_selftest':
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = lunarcal._selftest()
        out = buf.getvalue()
        if rc != 0 or '存在失败' in out:
            return False, f'selftest 退出码 {rc}，输出：\n{out[:500]}'
    elif case.get('cmd_py') == 'lunarcal_date':
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = lunarcal.main(case['pyargs'])
        out = buf.getvalue()
        if rc != 0:
            return False, f'lunarcal 退出码 {rc}：{out.strip()[:300]}'
    else:
        return False, '用例缺少 args / cmd_py 字段'

    missing = [e for e in case['expect'] if e not in out]
    if missing:
        return False, f'输出缺少期望子串 {missing}；实际输出前 400 字：\n{out[:400]}'
    return True, 'OK'


def main():
    with open(os.path.join(_ROOT, 'evals', 'evals.json'), encoding='utf-8') as f:
        data = json.load(f)
    total = passed = 0
    for case in data['用例']:
        total += 1
        try:
            ok, detail = run_case(case)
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f'运行器异常：{e}'
        passed += ok
        mark = 'PASS' if ok else 'FAIL'
        print(f'[{mark}] {case["组"]} · {case["名"]}')
        if not ok:
            print(f'       {detail}')
    print(f'\n结果：{passed}/{total} 通过' + (' —— ALL PASS' if passed == total else ' —— 存在失败！'))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
