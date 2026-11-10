#!/usr/bin/env python3
"""把 data/ 的分章数据注入站点模板，生成根目录 index.html。

八十一章的链接直指阅读页里各章的锚点（形如「第一章道可道非常道」），
点一下章号就跳到那一章。
"""
import html
import json
import os
import re
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BOOK = os.path.join(REPO, "book", "道可道·道德经心法读本.html")
ENTITY = "book/道可道·道德经心法读本.html"

VOLS = [
    ("根", 25, "道是什么", "道法自然"),
    ("动", 40, "它怎么动", "反者道之动"),
    ("生", 42, "万物怎么长出来", "道生一"),
    ("落", 38, "秩序怎么滑下去", "失道而后德"),
    ("还", 81, "人怎么回去", "为而不争"),
]


def anchors():
    s = open(BOOK, encoding="utf-8").read()
    ids = re.findall(r'id="(第[^"]*章[^"]*)"', s)
    out = {}
    for i in ids:
        m = re.match(r"第(.+?)章", i)
        if not m:
            continue
        out[m.group(1)] = i
    return out


def main():
    rows = [json.loads(l) for l in open(os.path.join(REPO, "data", "daodejing-81.jsonl"),
                                        encoding="utf-8")]
    by_id = {r["id"]: r for r in rows}
    amap = anchors()

    blocks = []
    for name, main_ch, ask, anchor_name in VOLS:
        chs = sorted(r["id"] for r in rows if r["volume"] == name)
        chips = []
        for cid in chs:
            r = by_id[cid]
            aid = amap.get(r["no"], "")
            href = ENTITY + ("#" + urllib.parse.quote(aid) if aid else "")
            chips.append(
                '          <a href="%s" title="第%s章 · %s">%d</a>'
                % (href, r["no"], html.escape(r["title"]), cid)
            )
        blocks.append(
            "    <div class=\"vol\">\n"
            "      <div class=\"dot\"></div>\n"
            "      <div class=\"name\">%s</div>\n"
            "      <p class=\"ask\">%s</p>\n"
            "      <p class=\"anchor\">第%d章 %s</p>\n"
            "      <p class=\"count\">%d 章</p>\n"
            "      <div class=\"chips\">\n%s\n      </div>\n"
            "    </div>"
            % (name, ask, main_ch, anchor_name, len(chs), "\n".join(chips))
        )

    tpl = open(os.path.join(HERE, "index_template.html"), encoding="utf-8").read()
    assert "<!--VOLS-->" in tpl
    out = tpl.replace("<!--VOLS-->", "\n".join(blocks))
    dst = os.path.join(REPO, "index.html")
    open(dst, "w", encoding="utf-8").write(out)
    print("index.html %d 字节 · 章链 %d 个（有锚点 %d）"
          % (os.path.getsize(dst), len(rows), len(amap)))


if __name__ == "__main__":
    main()
