#!/usr/bin/env python3
"""LuzzyCode 质量门禁校验。

校验 skills/luzzycode-*/SKILL.md 是否满足 skills/luzzycode-skills/SKILL.md
里写明的门禁条目，以及仓库级一致性（计数、路径、链接模板）。

用法：
    python scripts/check-skills.py            # 校验，失败返回 1
    python scripts/check-skills.py --verbose  # 逐项打印通过情况

只依赖标准库。frontmatter 用最小解析器读取，不引入 PyYAML 依赖。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MAX_BODY_LINES = 500

# 装饰性字符。★ 用于表格里的星数（数字后面，属数据而非装饰），单独豁免。
DECORATIVE = re.compile(r"[\u2600-\u27BF\u2B00-\u2BFF\uFE0F\uD83C-\uDBFF]")
STAR_DATA = re.compile(r"[\d.]+k?★")
HRULE = re.compile(r"^---\s*$", re.M)

# 子 skill 计数在常驻提示词里写阿拉伯数字、在编排器里写中文数字，两处都要对得上。
# 覆盖当前规模上下若干档；超出范围时该处退化为只查阿拉伯数字。
CN_NUM = {
    18: "十八", 19: "十九", 20: "二十", 21: "二十一",
    22: "二十二", 23: "二十三", 24: "二十四", 25: "二十五",
}


class Report:
    def __init__(self, verbose: bool) -> None:
        self.failures: list[str] = []
        self.passes: list[str] = []
        self.verbose = verbose

    def check(self, ok: bool, label: str) -> bool:
        if ok:
            self.passes.append(label)
            if self.verbose:
                print(f"  ok   {label}")
        else:
            self.failures.append(label)
            print(f"  FAIL {label}")
        return ok


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal frontmatter reader: only needs name + description + metadata."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str] = {}
    # name
    nm = re.search(r"(?m)^name:\s*(.+?)\s*$", block)
    if nm:
        out["name"] = nm.group(1).strip().strip("\"'")
    # description may be a folded block (>) or a plain scalar
    dm = re.search(r"(?ms)^description:\s*(.*?)(?=\n[a-z_]+:|\Z)", block)
    if dm:
        raw = dm.group(1)
        if raw.lstrip().startswith((">", "|")):
            raw = raw.lstrip()[1:]
        out["description"] = " ".join(raw.split())
    out["_has_metadata"] = "yes" if re.search(r"(?m)^metadata:", block) else "no"
    return out


def body_of(text: str) -> str:
    return re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", text, count=1, flags=re.S)


def check_skill(path: Path, rep: Report) -> None:
    name = path.parent.name
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    body = body_of(text)
    lines = body.splitlines()

    if not rep.check(bool(fm), f"{name}: frontmatter 可解析"):
        return

    rep.check(fm.get("name") == name, f"{name}: name 与目录名一致")
    rep.check(
        bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", ""))),
        f"{name}: name 符合 kebab-case",
    )

    desc = fm.get("description", "")
    rep.check(len(desc) >= 40, f"{name}: description 非空且够长")
    rep.check(
        bool(re.search(r"Do NOT use|Do not use|不要用|不负责", desc)),
        f"{name}: description 含负面触发词",
    )
    rep.check(
        not re.search(r"Step \d|Phase \d|第一步|第二步", desc),
        f"{name}: description 未泄漏执行步骤",
    )

    rep.check(
        len(lines) <= MAX_BODY_LINES,
        f"{name}: 正文 {len(lines)} 行 ≤ {MAX_BODY_LINES}",
    )
    # 第二人称检查：引号内的话（用户原话、触发词、反模式示例）与行内代码不算
    prose = re.sub(r"「[^」]*」", "", body)
    prose = re.sub(r"`[^`]*`", "", prose)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.S)
    rep.check("\u4f60" not in prose, f"{name}: 正文无第二人称「你」（引号内引用除外）")
    rep.check(bool(re.search(r"(?m)^##+\s*Verify", body)), f"{name}: 含 Verify 段")
    rep.check(
        len(re.findall(r"(?m)^Input[:：]", body)) >= 2,
        f"{name}: 含至少 2 组 Input → Output 示例",
    )
    # 装饰性格式。来源标注引用块是唯一豁免（用于定位该 skill 的仓库地址）。
    scan = re.sub(r"<!-- self-link -->\n>.*?\n", "", body)
    scan = STAR_DATA.sub("", scan)
    rep.check(not DECORATIVE.search(scan), f"{name}: 无 emoji 装饰")
    rep.check(not HRULE.search(scan), f"{name}: 无装饰性分隔线")


def check_repo(rep: Report) -> None:
    dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    names = [p.name for p in dirs]
    n_sub = len([n for n in names if n != "luzzycode"])

    prompt = (ROOT / "prompt" / "LuzzyCode.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    rep.check(
        all((SKILLS_DIR / n / "SKILL.md").exists() for n in names),
        "仓库: 每个 skill 目录都有 SKILL.md",
    )
    rep.check(
        len(re.findall(r"luzzycode-", readme)) > 0 and f"{len(names)} 个" in readme,
        f"仓库: README 计数与目录一致（{len(names)} 个）",
    )

    # 提示词里提到的每个 luzzycode-* 名字都真实存在
    mentioned = set(re.findall(r"`?(luzzycode-[a-z]+)`?", prompt))
    bogus = sorted(m for m in mentioned if m not in names)
    rep.check(not bogus, f"仓库: 提示词引用的 skill 名都存在（悬空: {bogus or '无'}）")

    # 路由表覆盖全部子 skill（编排器自身不参与路由）
    router = (SKILLS_DIR / "luzzycode" / "SKILL.md").read_text(encoding="utf-8")
    routed = {m for m in re.findall(r"luzzycode-[a-z]+", router)}
    missing = sorted(set(names) - routed - {"luzzycode"})
    rep.check(not missing, f"仓库: 编排器路由表覆盖全部子 skill（漏: {missing or '无'}）")

    # 提示词里的抓取链接模板仍然指向本仓库
    rep.check(
        "raw.githubusercontent.com/LuzzyMeow/LuzzyCode" in prompt,
        "仓库: 提示词含本仓库抓取链接模板",
    )

    # 子 skill 计数声明与实际一致。
    # 两处口径不同：常驻提示词用阿拉伯数字（「N 个子 skill」），编排器用中文数字
    # （「N个子 skill」）。原先只查提示词里的中文写法，而该写法实际在编排器里，
    # 于是检查空转——编排器的计数漂移了也不会报。两处都查。
    def declared_count(text: str, pattern: str) -> int | None:
        m = re.search(pattern, text)
        return int(m.group(1)) if m else None

    p_num = declared_count(prompt, r"(\d+)\s*个子 skill")
    rep.check(
        p_num is None or p_num == n_sub,
        f"仓库: 提示词中子 skill 计数与实际 {n_sub} 一致（声明: {p_num if p_num is not None else '未找到'}）",
    )

    router_num = None
    for value, word in CN_NUM.items():
        if f"{word}个子 skill" in router:
            router_num = value
            break
    rep.check(
        router_num is None or router_num == n_sub,
        f"仓库: 编排器中子 skill 计数与实际 {n_sub} 一致（声明: {router_num if router_num is not None else '未找到'}）",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    rep = Report(args.verbose)
    print("校验 skills/ …")
    for d in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        check_skill(d / "SKILL.md", rep)

    print("\n校验仓库级一致性 …")
    check_repo(rep)

    print(f"\n通过 {len(rep.passes)} 项，失败 {len(rep.failures)} 项")
    if rep.failures:
        print("\n失败明细：")
        for f in rep.failures:
            print(f"  - {f}")
        return 1
    print("全部门禁通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
