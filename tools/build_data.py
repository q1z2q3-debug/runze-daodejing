#!/usr/bin/env python3
"""从全本 Markdown 生成对外发布用的结构化数据。

产出：
  data/daodejing-81.jsonl   八十一章，一章一条（含经文、小注、全文）
  README 的章节索引由本脚本打印，人工确认后写入 README
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "book", "道可道·道德经心法读本（全本）.md")

VOLUMES = {
    "根": {"main": 25, "chapters": [1, 4, 14, 15, 21, 23, 25, 26, 34, 41, 47, 48, 56, 62, 70]},
    "动": {"main": 40, "chapters": [9, 24, 30, 36, 40, 43, 63, 64, 73, 76, 77]},
    "生": {"main": 42, "chapters": [5, 6, 7, 10, 11, 16, 39, 42, 45, 50, 51, 52, 55, 59]},
    "落": {"main": 38, "chapters": [2, 3, 12, 13, 17, 18, 19, 20, 29, 31, 38, 46, 53, 57,
                                    58, 60, 61, 65, 68, 69, 71, 72, 74, 75]},
    "还": {"main": 81, "chapters": [8, 22, 27, 28, 32, 33, 35, 37, 44, 49, 54, 66, 67,
                                    78, 79, 80, 81]},
}
CHAPTER_OF = {c: v for v, d in VOLUMES.items() for c in d["chapters"]}

CN = "一二三四五六七八九十"


def cn_num(n):
    if n <= 10:
        return "十" if n == 10 else CN[n - 1]
    t, u = divmod(n, 10)
    return ("" if t == 1 else CN[t - 1]) + "十" + (CN[u - 1] if u else "")


def section(body, name):
    """取 ## name 到下一个 ## 之间的内容。"""
    m = re.search(r"^## %s\s*\n(.*?)(?=^## |\Z)" % re.escape(name), body, re.S | re.M)
    return m.group(1).strip() if m else ""


def main():
    s = open(SRC, encoding="utf-8").read()

    heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"^# (.+)$", s, re.M)]
    blocks = []
    for i, (pos, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(s)
        blocks.append((title, s[pos:end]))

    chapters = {}
    for title, body in blocks:
        m = re.match(r"^第(.+?)章｜(.+)$", title)
        if not m:
            continue
        no, name = m.group(1), m.group(2).strip()
        n = {cn_num(i): i for i in range(1, 82)}[no]

        b = re.sub(r'<p align="center">(.*?)</p>', r"\1", body)
        b = re.sub(r"^---$", "", b, flags=re.M)
        b = re.sub(r"^# 第.+?章｜.+\n", "", b, flags=re.M)
        b = re.sub(r"\n{3,}", "\n\n", b).strip()

        raw_all = section(b, "本章原文")
        raw = re.split(r"\n(?:对\s*照|小\s*注|【小注)", raw_all)[0].strip()
        marks = {"经 文", "经文", "原 文", "原文"}
        stop = {"对 照", "小 注", "注 释", "字 义", "校 勘", "异 文", "补 注", "出 处"}
        stop_keys = {m.replace(" ", "") for m in stop}
        mark_keys = {m.replace(" ", "") for m in marks}
        lines = []
        for ln in raw.splitlines():
            if not ln.startswith(">"):
                continue
            txt = re.sub(r"\*\*", "", ln.lstrip(">").strip())
            key = txt.replace(" ", "")
            if key in stop_keys:
                break
            if key in mark_keys:
                continue
            lines.append(txt)
        if lines:
            scripture = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
        else:
            scripture = re.sub(r"\n{3,}", "\n\n", raw).strip()
        notes = re.sub(r"\n{2,}", "\n", section(b, "本章原文").replace(
            "\n".join(ln for ln in raw.splitlines() if ln.startswith(">")), "")).strip()

        chapters[n] = {
            "id": n,
            "no": no,
            "title": name,
            "volume": CHAPTER_OF[n],
            "scripture": scripture,
            "notes": notes,
            "text": b,
        }

    assert len(chapters) == 81, "章数不足：%d" % len(chapters)
    outdir = os.path.join(REPO, "data")
    os.makedirs(outdir, exist_ok=True)
    rows = [chapters[i] for i in range(1, 82)]
    with open(os.path.join(outdir, "daodejing-81.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total = sum(len(re.sub(r"\s", "", r["text"])) for r in rows)
    print("章 %d / 非空白字 %d" % (len(rows), total))
    for v, d in VOLUMES.items():
        print("  卷%s 主章%d %d 章" % (v, d["main"], len(d["chapters"])))
    return rows


if __name__ == "__main__":
    main()
