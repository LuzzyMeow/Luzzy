#!/usr/bin/env python3
"""§1.1.8 门覆盖审计：真实任务语料 x 触发口径关键词面的词面覆盖。

测什么：prompt/Luzzy.md §1.1.8 各条目的触发关键词，对 evals/gate-corpus.json
里真实任务说法的子串覆盖（recall），门槛默认 80%。
不测什么：模型行为。词面审计只能暴露关键词表的盲区，不能证明模型会照做——
行为证据靠转录测录积累（见本目录 README.md）。

用法：
  python evals/eval-gate-coverage.py
  python evals/eval-gate-coverage.py --threshold 80 --corpus evals/gate-corpus.json --prompt prompt/Luzzy.md

退出码：0 全过；1 任一类目 recall 低于门槛 / triage 或 chitchat 误命中 / multi 全空。
仅用标准库。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 语料类目 ID → §1.1.8 条目名（「」内文字）。改 §1.1.8 条目名时同步本表。
CANON = {
    "backend": "开发任何代码类任务",
    "design": "设计类",
    "design-subitem": "设计类子项",
    "writing": "文档 / 写作类",
    "office": "Office 文件",
    "ppt": "做 PPT",
    "html": "HTML / 网页开发",
    "windows": "Windows 修复 / 优化",
    "planning": "项目规划 / 需求拆解",
    "code-review": "代码审查",
    "reverse": "逆向 / 授权渗透 / 安全研究",
    "assets": "素材 / 图标 / 组件库",
    "android": "Android 开发 / 模拟器",
    "mcp": "MCP 开发 / 接入 / 维护",
    "skilldev": "涉及 skill 的一切操作",
    "browser": "浏览器自动化 / 网页操作",
    "bilibili": "B 站视频转笔记 / 字幕提取",
    "academic": "学术研究 / 论文撰写",
    "problem-solving": "学科题目解答 / 解题方法论",
}

# 过宽或纯连接性的碎片，不作为触发面
STOPWORDS = {"应用", "依赖", "问题", "文件", "原生", "内容", "给", "条"}

BULLET_RE = re.compile(r"^- \*\*「(.+?)」(.*?)\*\*：(.*)$")
SPLIT_RE = re.compile(r"[、，。；：：（）()【】/·\s\*`\"']+")
LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_.\-]{1,}")


def parse_bullets(prompt_text: str) -> dict:
    """解析 §1.1.8：条目名 → 触发碎片集。

    - 条目名后带限定语的（「类目未知」本身就算命中、「设计类」触发时先分流）
      是路由规则，不产关键词
    - 关键词取第一个句号前的枚举（句号后是说明文字）
    - 条目名里的拉丁 token（PPT / MCP / HTML / Android / Office / Windows）也算触发面
    """
    m = re.search(r"^### 1\.1\.8 .*?$([\s\S]*?)(?=^### |\Z)", prompt_text, re.M)
    if not m:
        sys.exit("ERROR: prompt 里找不到 §1.1.8 小节")
    bullets = {}
    for line in m.group(1).splitlines():
        bm = BULLET_RE.match(line.strip())
        if not bm:
            continue
        name, qualifier, text = bm.group(1), bm.group(2), bm.group(3)
        if qualifier.strip():
            continue
        frags = set()
        # 关键词取条目正文第一个句号前的枚举（句号后是说明文字）
        for seg in text.split("。")[0].split("——"):
            for raw in SPLIT_RE.split(seg):
                f = raw.strip("*`「」→ .").strip()
                if len(f) >= 2 and f not in STOPWORDS:
                    frags.add(f)
            for tok in LATIN_RE.findall(seg):
                if tok.lower() not in STOPWORDS:
                    frags.add(tok)
        # 条目名只贡献拉丁 token（PPT / MCP / HTML / Android / Office / Windows）；
        # CJK 触发词应住在正文枚举里，不从条目名拆——否则「Office 文件」会产出过宽的「文件」
        for tok in LATIN_RE.findall(name):
            frags.add(tok)
        if frags:
            bullets[name] = sorted(frags)
    return bullets


def match(frags, utterance: str) -> list:
    u = utterance.lower()
    return [f for f in frags if f.lower() in u]


def main() -> int:
    ap = argparse.ArgumentParser(description="§1.1.8 门覆盖审计")
    ap.add_argument("--corpus", default="evals/gate-corpus.json")
    ap.add_argument("--prompt", default="prompt/Luzzy.md")
    ap.add_argument("--threshold", type=int, default=80, help="各类目 recall 门槛（百分比）")
    args = ap.parse_args()

    prompt_text = Path(args.prompt).read_text(encoding="utf-8")
    corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))
    bullets = parse_bullets(prompt_text)

    # CANON 里指向的条目必须都能解析到，否则是断链
    missing_bullets = [f"{cid}→「{name}」" for cid, name in CANON.items() if name not in bullets]
    if missing_bullets:
        print("ERROR: CANON 指向的 §1.1.8 条目缺失（改了条目名没同步 CANON？）：")
        for x in missing_bullets:
            print("  -", x)
        return 1

    frag_map = {cid: bullets[name] for cid, name in CANON.items()}

    stats = {cid: {"total": 0, "hit": 0, "miss": []} for cid in CANON}
    failures, crossfire = [], []

    for e in corpus["entries"]:
        kind, expected, utt = e["kind"], e["expected"], e["utterance"]
        hits = [cid for cid in CANON if match(frag_map[cid], utt)]

        if kind == "task":
            for cid in expected:
                stats[cid]["total"] += 1
                if cid in hits:
                    stats[cid]["hit"] += 1
                else:
                    stats[cid]["miss"].append(utt)
            extra = [h for h in hits if h not in expected]
            if extra:
                crossfire.append((e["id"], utt, extra))
        elif kind == "multi":
            if not any(cid in hits for cid in expected):
                failures.append(f"multi 全空：[{e['id']}] {utt}（期望之一命中：{'/'.join(expected)}）")
            extra = [h for h in hits if h not in expected]
            if extra:
                crossfire.append((e["id"], utt, extra))
        elif kind in ("triage", "chitchat"):
            if hits:
                why = ", ".join(f"{h}:{m[0]}" for h in hits for m in [match(frag_map[h], utt)])
                failures.append(f"{kind} 误命中：[{e['id']}] {utt} ← {why}")
        else:
            failures.append(f"未知 kind：[{e['id']}] {kind}")

    print(f"§1.1.8 门覆盖审计（门槛 {args.threshold}%，语料 {len(corpus['entries'])} 条）")
    print("=" * 72)
    ok = True
    for cid in CANON:
        s = stats[cid]
        if s["total"] == 0:
            print(f"  {cid:<18} （语料无 task 条目，跳过）")
            continue
        recall = 100 * s["hit"] / s["total"]
        mark = "PASS" if recall >= args.threshold else "FAIL"
        if mark == "FAIL":
            ok = False
        print(f"  {cid:<18} {s['hit']}/{s['total']}  {recall:5.1f}%  {mark}")
        for utt in s["miss"]:
            print(f"      miss: {utt}")

    if crossfire:
        print("-" * 72)
        print("跨类目命中（并列属正常，仅提示——语句同时命中了期望之外的类目）：")
        for eid, utt, extra in crossfire:
            print(f"  [{eid}] {utt}  → 额外命中：{', '.join(extra)}")

    if failures:
        print("-" * 72)
        print("失败项：")
        for f in failures:
            print("  -", f)

    print("=" * 72)
    print("词面审计只证明关键词表覆盖了这些说法，不证明模型会照做——行为证据见 evals/README.md 的测录协议。")
    return 0 if ok and not failures else 1


if __name__ == "__main__":
    sys.exit(main())
