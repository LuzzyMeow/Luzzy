#!/usr/bin/env python3
"""把 B 站视频的 SRT 字幕转成带时间戳的纯文本，供后续重组为笔记。

只做确定性的事：合并碎片行、去掉序号与时间戳、输出分段文本。
不做语义重组——那是 Agent 读文本后的事。

用法:
    python scripts/parse_srt.py <字幕.srt> [--timestamps] [--out 输出路径]

    --timestamps   每段前保留 [mm:ss] 标记，便于回视频核对
    --out          写入文件；省略则打到标准输出

退出码: 0 成功 / 1 文件不可读 / 2 未解析到任何字幕段
"""

import argparse
import re
import sys
from pathlib import Path

TIMESTAMP_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)
INDEX_RE = re.compile(r"^\d+$")


def parse_srt(text: str) -> list[tuple[float, str]]:
    """返回 [(起始秒, 文本)]，按出现顺序，已合并多行。"""
    cues: list[tuple[float, str]] = []
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        match = TIMESTAMP_RE.search(line)
        if not match:
            index += 1
            continue
        start = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))
        index += 1
        body: list[str] = []
        while index < len(lines):
            current = lines[index].strip()
            if not current or TIMESTAMP_RE.search(current):
                break
            body.append(current)
            index += 1
        merged = "".join(body).strip()
        if merged:
            cues.append((float(start), merged))
    return cues


def merge_fragments(cues: list[tuple[float, str]], gap_seconds: float = 0.8) -> list[tuple[float, str]]:
    """把间隔很短的相邻短句并成一句，减少 AI 字幕的碎片感。"""
    merged: list[tuple[float, str]] = []
    for start, text in cues:
        if merged:
            last_start, last_text = merged[-1]
            if start - last_start < gap_seconds and len(last_text) < 40:
                merged[-1] = (last_start, last_text + text)
                continue
        merged.append((start, text))
    return merged


def format_clock(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="B 站 SRT 字幕转纯文本")
    parser.add_argument("srt", help="字幕文件路径")
    parser.add_argument("--timestamps", action="store_true", help="保留 [mm:ss] 标记")
    parser.add_argument("--out", help="输出文件路径，省略则打到标准输出")
    args = parser.parse_args()

    path = Path(args.srt)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"无法读取 {path}: {error}", file=sys.stderr)
        return 1

    cues = merge_fragments(parse_srt(raw))
    if not cues:
        print(f"{path} 中未解析到字幕段（确认是 SRT 格式）", file=sys.stderr)
        return 2

    blocks = [
        f"[{format_clock(start)}] {text}" if args.timestamps else text
        for start, text in cues
    ]
    output = "\n".join(blocks) + "\n"

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"写入 {args.out}：{len(cues)} 段，{len(output)} 字符", file=sys.stderr)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
