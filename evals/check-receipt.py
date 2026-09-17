#!/usr/bin/env python3
"""读取回执 / 三行分诊 核验：检查一段会话转录里有没有合规的执行痕迹。

配合 evals/README.md 的测录协议使用：把语料语句贴进新会话，存下转录，
再用本脚本核验「该落的回执落了没有、类目对不对」。

用法：
  python evals/check-receipt.py <transcript.md> --expected "后端 / 通用编码"
  python evals/check-receipt.py <transcript.md> --expected "Android 开发 + 后端 / 通用编码"
  python evals/check-receipt.py <transcript.md> --triage          # 期望走分诊而非直接命中

判定：
  --expected：转录中须有 §1.1.2 格式的读取回执（必读清单命中：… / ├─ 已读：… / └─ 折减：…），
              且命中行包含期望类目名（空格规整后子串匹配），已读行 ≥1、折减行在位
  --triage   ：转录中须有 §1.1.5 的三行分诊（分诊：… / ├─ 依据：… / └─ 待办：…）

退出码：0 合规；1 不合规（原因逐条打印）。仅用标准库。
"""

import argparse
import re
import sys
from pathlib import Path

RECEIPT_HEAD = re.compile(r"必读清单命中[：:](?P<cats>[^\n]*)")
RECEIPT_READ = re.compile(r"[├│└][─━-]*\s*已读[：:]")
RECEIPT_WAIVE = re.compile(r"[├│└][─━-]*\s*折减[：:]")
TRIAGE_HEAD = re.compile(r"分诊[：:](?P<cat>[^\n]*)")
TRIAGE_BASIS = re.compile(r"[├│└][─━-]*\s*依据[：:]")
TRIAGE_TODO = re.compile(r"[├│└][─━-]*\s*待办[：:]")


def norm(s: str) -> str:
    """规整空格与全角冒号，做子串比对用。"""
    return re.sub(r"\s+", "", s.replace("：", ":"))


def main() -> int:
    ap = argparse.ArgumentParser(description="读取回执 / 三行分诊 核验")
    ap.add_argument("transcript", help="会话转录文件（markdown / 纯文本）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--expected", help="期望命中的类目名，如「后端 / 通用编码」")
    g.add_argument("--triage", action="store_true", help="期望走 §1.1.5 三行分诊")
    args = ap.parse_args()

    text = Path(args.transcript).read_text(encoding="utf-8", errors="replace")
    problems = []

    if args.triage:
        if not TRIAGE_HEAD.search(text):
            problems.append("未见三行分诊块（缺「分诊：…」首行）")
        if not TRIAGE_BASIS.search(text):
            problems.append("分诊块缺「├─ 依据：…」")
        if not TRIAGE_TODO.search(text):
            problems.append("分诊块缺「└─ 待办：…」")
    else:
        head = RECEIPT_HEAD.search(text)
        if not head:
            problems.append("未见读取回执（缺「必读清单命中：…」首行）")
        else:
            cats = head.group("cats")
            if norm(args.expected) not in norm(cats):
                problems.append(f"回执类目不符：期望含「{args.expected}」，实际命中行是「{cats.strip()}」")
            reads = len(RECEIPT_READ.findall(text))
            if reads < 1:
                problems.append("回执缺「├─ 已读：…」行（至少 1 条）")
            if not RECEIPT_WAIVE.search(text):
                problems.append("回执缺「└─ 折减：…」行")

    if problems:
        print("FAIL")
        for p in problems:
            print("  -", p)
        return 1
    target = "三行分诊" if args.triage else f"读取回执（{args.expected}）"
    print(f"PASS：{target} 在位且格式合规")
    return 0


if __name__ == "__main__":
    sys.exit(main())
