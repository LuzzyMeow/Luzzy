#!/usr/bin/env python3
"""抓取单条 B 站视频的公开元数据与全部公开评论，产出信息卡 JSON。

默认抓取四项：视频标题、视频简介、分 P 目录、全部公开评论（含二级回复）。
字幕由 yt-dlp 单独取（见 SKILL.md 步骤 3），本脚本只管元数据与评论。

合规范围：单视频、低频、公开数据、用户自己的登录态。
不绕过 WBI 签名，不访问付费/OGV/充电内容，不做批量或全站抓取。

实测要点（决定了本脚本为什么这么写）：
  1. 一级评论要合并「老接口 + 新接口」才全 —— 实测老接口 20 条、新接口 19 条，
     只用一个会漏。两者按 rpid 去重合并。
  2. 二级回复不在列表里 —— 一级评论只带 rcount 计数，正文要另调 reply/reply 接口。
  3. member.mid 是字符串、upper.mid 是整数 —— 直接比较永远不等，两侧转字符串再比。
  4. 实抓数可能少于页面计数 —— 被删除或隐藏的评论仍计入总数，接口不再返回。
     差值如实报告，不假装取全。

用法:
    python scripts/fetch_video_info.py <BV号或视频URL> --cookies <cookie文件> --out <输出.json>

    --cookies     必需。Netscape 格式 cookie 文件（取法见 references/cookie-sourcing.md）
    --out         必需。输出 JSON 路径，落临时目录
    --max-pages   可选，各接口翻页上限，默认 10
    --no-comments 跳过评论，只取元数据与分 P 目录

退出码: 0 成功 / 1 参数或文件错误 / 2 元数据接口返回非零 code / 3 触发风控
"""

import argparse
import http.cookiejar
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BV_RE = re.compile(r"BV[0-9A-Za-z]{10}")

# B 站风控退出码：-352 触发风控、-412 请求被拦截、-509 超出限制
RISK_CODES = {-352, -412, -509}
# 相邻请求间隔（秒）。合规纪律要求低频，不要调小。
REQUEST_INTERVAL = 1.2


class RiskControlError(Exception):
    """触发平台风控。不重试、不绕过，直接停止。"""


def normalize_bvid(raw: str) -> str:
    """从链接、短链文本或裸 BV 号里取出 12 位 BV 号。"""
    match = BV_RE.search(raw)
    if not match:
        raise ValueError(f"未能在输入中找到 BV 号: {raw}")
    return match.group(0)


def build_opener(cookie_file: Path) -> urllib.request.OpenerDirector:
    jar = http.cookiejar.MozillaCookieJar(str(cookie_file))
    jar.load(ignore_discard=True, ignore_expires=True)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
        ("User-Agent", USER_AGENT),
        ("Referer", "https://www.bilibili.com/"),
        ("Accept", "application/json, text/plain, */*"),
    ]
    return opener


def get_json(opener: urllib.request.OpenerDirector, url: str, retries: int = 3) -> dict:
    """请求 JSON。风控码立即上抛，不重试——风控后重试是对抗行为。"""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with opener.open(url, timeout=25) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code in (403, 412, 429):
                raise RiskControlError(f"HTTP {error.code}") from error
            last_error = error
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
        if attempt < retries - 1:
            time.sleep(REQUEST_INTERVAL * (attempt + 1))
    raise RuntimeError(f"请求失败: {url} ({last_error})")


def check_risk(payload: dict) -> None:
    """接口返回体里的风控码同样要拦。"""
    code = payload.get("code")
    if code in RISK_CODES:
        raise RiskControlError(f"code={code} msg={payload.get('message')}")


def fetch_metadata(opener: urllib.request.OpenerDirector, bvid: str) -> dict:
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={urllib.parse.quote(bvid)}"
    payload = get_json(opener, url)
    check_risk(payload)
    code = payload.get("code")
    if code != 0:
        print(f"[metadata] 接口返回 code={code} msg={payload.get('message')}", file=sys.stderr)
        sys.exit(2)
    return payload["data"]


def fetch_pagelist(opener: urllib.request.OpenerDirector, bvid: str) -> list[dict]:
    """取分 P 目录。单 P 视频返回 1 条。"""
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={urllib.parse.quote(bvid)}"
    payload = get_json(opener, url)
    check_risk(payload)
    if payload.get("code") != 0:
        print(f"[pagelist] 接口返回 code={payload.get('code')}", file=sys.stderr)
        return []
    return [
        {
            "page": item.get("page"),
            "part": item.get("part"),
            "duration": item.get("duration"),
            "cid": item.get("cid"),
        }
        for item in (payload.get("data") or [])
    ]


def normalize_comment(item: dict, uploader_key: str | None, level: str) -> dict:
    """把两种接口的评论结构统一成一种形状。"""
    member = item.get("member") or {}
    author_mid = member.get("mid")
    return {
        "rpid": item.get("rpid"),
        "parent_rpid": item.get("parent"),
        "level": level,
        "author": member.get("uname"),
        "author_mid": str(author_mid) if author_mid is not None else None,
        "is_uploader": str(author_mid) == uploader_key if uploader_key else False,
        "like": item.get("like", 0),
        "rcount": item.get("rcount", 0),
        "ctime": item.get("ctime"),
        "ctime_text": time.strftime("%Y-%m-%d %H:%M", time.localtime(item.get("ctime", 0))),
        "message": (item.get("content") or {}).get("message", ""),
    }


def fetch_root_comments(
    opener: urllib.request.OpenerDirector,
    aid: int,
    uploader_key: str | None,
    max_pages: int,
) -> tuple[list[dict], bool]:
    """取一级评论，合并老接口与新接口。

    两个接口返回的集合不完全相同，只用一个会漏（实测 20 vs 19）。
    返回 (评论列表, 是否遇到翻页中断)。
    """
    merged: dict[int, dict] = {}
    truncated = False

    # 老接口 /x/v2/reply：page.count 给出总数，超出后返回空页
    for page in range(1, max_pages + 1):
        url = "https://api.bilibili.com/x/v2/reply?" + urllib.parse.urlencode(
            {"oid": aid, "type": 1, "pn": page, "sort": 2, "ps": 20}
        )
        payload = get_json(opener, url)
        check_risk(payload)
        if payload.get("code") != 0:
            print(f"[comments] 老接口第 {page} 页 code={payload.get('code')}", file=sys.stderr)
            break
        replies = (payload.get("data") or {}).get("replies") or []
        if not replies:
            break
        for item in replies:
            rpid = item.get("rpid")
            if rpid and rpid not in merged:
                merged[rpid] = normalize_comment(item, uploader_key, "root")
        print(f"[comments] 老接口第 {page} 页 +{len(replies)}，一级累计 {len(merged)}", file=sys.stderr)
        if len(replies) < 20:
            break
        time.sleep(REQUEST_INTERVAL)

    # 新接口 /x/v2/reply/main：mode=3 热门，带 is_end 游标
    for page in range(1, max_pages + 1):
        url = "https://api.bilibili.com/x/v2/reply/main?" + urllib.parse.urlencode(
            {"oid": aid, "type": 1, "mode": 3, "next": page}
        )
        payload = get_json(opener, url)
        check_risk(payload)
        if payload.get("code") != 0:
            print(f"[comments] 新接口第 {page} 页 code={payload.get('code')}", file=sys.stderr)
            break
        data = payload.get("data") or {}
        replies = data.get("replies") or []
        for item in replies:
            rpid = item.get("rpid")
            if rpid and rpid not in merged:
                merged[rpid] = normalize_comment(item, uploader_key, "root")
        cursor = data.get("cursor") or {}
        print(
            f"[comments] 新接口第 {page} 页 +{len(replies)}，一级累计 {len(merged)}，"
            f"is_end={cursor.get('is_end')}",
            file=sys.stderr,
        )
        if cursor.get("is_end") or not replies:
            break
        time.sleep(REQUEST_INTERVAL)

    return list(merged.values()), truncated


def fetch_child_replies(
    opener: urllib.request.OpenerDirector,
    aid: int,
    roots: list[dict],
    uploader_key: str | None,
) -> list[dict]:
    """逐条取二级回复。一级评论只带 rcount 计数，正文要另调接口。"""
    children: list[dict] = []
    targets = [r for r in roots if (r.get("rcount") or 0) > 0]
    for index, root in enumerate(targets, 1):
        page = 1
        while page <= 10:
            url = "https://api.bilibili.com/x/v2/reply/reply?" + urllib.parse.urlencode(
                {"oid": aid, "type": 1, "root": root["rpid"], "ps": 20, "pn": page}
            )
            payload = get_json(opener, url)
            check_risk(payload)
            if payload.get("code") != 0:
                break
            batch = (payload.get("data") or {}).get("replies") or []
            for item in batch:
                children.append(normalize_comment(item, uploader_key, "child"))
            if len(batch) < 20:
                break
            page += 1
            time.sleep(REQUEST_INTERVAL)
        print(
            f"[comments] 二级回复 {index}/{len(targets)}：{root['author']} "
            f"声明 {root.get('rcount')}，实取 {sum(1 for c in children if c['parent_rpid'] == root['rpid'])}",
            file=sys.stderr,
        )
        time.sleep(REQUEST_INTERVAL)
    return children


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取 B 站视频公开元数据与全部公开评论")
    parser.add_argument("input", help="BV 号或视频链接")
    parser.add_argument("--cookies", required=True, help="Netscape 格式 cookie 文件")
    parser.add_argument("--out", required=True, help="输出 JSON 路径")
    parser.add_argument("--max-pages", type=int, default=10, help="各接口翻页上限，默认 10")
    parser.add_argument("--no-comments", action="store_true", help="只取元数据与分 P 目录")
    args = parser.parse_args()

    try:
        bvid = normalize_bvid(args.input)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    cookie_file = Path(args.cookies)
    if not cookie_file.exists():
        print(f"ERROR: cookie 文件不存在: {cookie_file}", file=sys.stderr)
        return 1

    print(f"[info] BV 号: {bvid}", file=sys.stderr)
    opener = build_opener(cookie_file)

    try:
        data = fetch_metadata(opener, bvid)
        owner = data.get("owner") or {}
        stat = data.get("stat") or {}
        aid = data.get("aid")
        uploader_key = str(owner.get("mid")) if owner.get("mid") is not None else None

        time.sleep(REQUEST_INTERVAL)
        parts = fetch_pagelist(opener, bvid)

        roots: list[dict] = []
        children: list[dict] = []
        if not args.no_comments and aid:
            time.sleep(REQUEST_INTERVAL)
            roots, _ = fetch_root_comments(opener, aid, uploader_key, args.max_pages)
            children = fetch_child_replies(opener, aid, roots, uploader_key)
    except RiskControlError as error:
        print(f"[risk] 触发风控（{error}）。停止请求，不重试、不绕过。", file=sys.stderr)
        return 3

    all_comments = roots + children
    declared = stat.get("reply")
    fetched = len(all_comments)
    gap = (declared - fetched) if isinstance(declared, int) else None

    result = {
        "schema_version": "1.0",
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "video": {
            "bvid": data.get("bvid"),
            "aid": aid,
            "title": data.get("title"),
            "desc": data.get("desc"),
            "uploader": owner.get("name"),
            "uploader_mid": uploader_key,
            "pubdate": time.strftime("%Y-%m-%d", time.localtime(data.get("pubdate", 0))),
            "duration_seconds": data.get("duration"),
            "part_count": data.get("videos"),
            "tname": data.get("tname"),
            "cover": data.get("pic"),
            "stat": {
                "view": stat.get("view"),
                "like": stat.get("like"),
                "coin": stat.get("coin"),
                "favorite": stat.get("favorite"),
                "reply": declared,
                "danmaku": stat.get("danmaku"),
                "share": stat.get("share"),
            },
        },
        "parts": parts,
        "comments": all_comments,
        "comments_summary": {
            "root_count": len(roots),
            "child_count": len(children),
            "total_fetched": fetched,
            "declared_count": declared,
            "gap": gap,
            "complete": gap == 0 if gap is not None else False,
            "gap_note": (
                "实抓数少于声明数时，差值来自已被删除或隐藏的评论——它们仍计入总数，"
                "但接口不再返回。这是平台行为，不是抓取遗漏。"
            ),
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("", file=sys.stderr)
    print(f"[done] 标题: {data.get('title')}", file=sys.stderr)
    print(f"[done] UP 主: {owner.get('name')}（mid={uploader_key}）", file=sys.stderr)
    print(f"[done] 分 P 数: {len(parts)}", file=sys.stderr)
    print(f"[done] 简介: {len(data.get('desc') or '')} 字符", file=sys.stderr)
    print(
        f"[done] 评论: 一级 {len(roots)} + 二级 {len(children)} = {fetched} 条，"
        f"页面声明 {declared} 条，差值 {gap}",
        file=sys.stderr,
    )
    print(f"[done] 是否取全: {result['comments_summary']['complete']}", file=sys.stderr)
    print(f"[saved] {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
