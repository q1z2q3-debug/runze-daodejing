#!/usr/bin/env python3
"""把 book/义理图/*.svg 内嵌进阅读版（每章原文之后、本章导读之前）。

只嵌一份：图内的 SVG 直接作为节点写进正文，不引外链、不引图片文件。
图的题与「读图一句」取自 book/义理图-体例.md；取不到就只写文件名。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BOOK = os.path.join(REPO, "book", "道可道·道德经心法读本.html")
FIGS = os.path.join(REPO, "book", "义理图")
STYLE = os.path.join(REPO, "book", "义理图-体例.md")

NUM = "一二三四五六七八九"


def cn2int(s):
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十")
        return (NUM.index(a) + 1 if a else 1) * 10 + (NUM.index(b) + 1 if b else 0)
    return NUM.index(s) + 1


def read_style():
    """体例表 → {文件名主干: (章, 题, 一句)}"""
    out = {}
    for ln in open(STYLE, encoding="utf-8"):
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        stem = None
        for i, c in enumerate(cells):
            c2 = c.strip("`").strip()
            if c2.endswith(".svg"):
                c2 = c2[:-4]
            if re.match(r"^ch\d\d", c2):
                stem = c2
                cells_tail = cells[i + 1:]
                break
        if not stem:
            continue
        if stem.startswith("ch0") or stem.startswith("ch1"):
            pass
        # 题 = stem 之后第一列；一句 = 描述里「读图一句：」
        title = cells_tail[0] if cells_tail else stem
        desc = " ".join(cells_tail[1:]) if len(cells_tail) > 1 else ""
        m = re.search(r"读图一句：(.+?)\.?\s*\|?$", desc)
        one = m.group(1).strip().rstrip("。") if m else ""
        if not one and len(cells_tail) == 2 and desc:
            one = desc.rstrip("。")          # 早期三列行，第三列即读图一句
        if "旧稿已撤" in desc:
            out[stem] = (title, "", True)
            continue
        out[stem] = (title, one, False)
    return out


def main():
    meta = read_style()
    files = sorted(f[:-4] for f in os.listdir(FIGS) if f.endswith(".svg"))
    by_ch = {}
    for k in files:
        m = re.match(r"^ch(\d\d)", k)
        if not m:
            continue
        by_ch.setdefault(int(m.group(1)), []).append(k)

    html = open(BOOK, encoding="utf-8").read()

    # 1) 样式只加一次
    if ".yili{" not in html:
        css = """
.yili{
  width:min(92vw,720px);margin:34px 0 40px calc(50% - min(46vw,360px));
}
.yili .lead{
  font-size:12px;letter-spacing:.42em;color:var(--ochre);
  border-bottom:1px solid var(--line);padding-bottom:7px;margin:0 0 18px;
}
.yili .lead span{letter-spacing:.1em;color:var(--muted);font-size:11px}
.yili figure{margin:0 0 30px;cursor:zoom-in}
.yili figure svg{
  display:block;width:100%;height:auto;
  background:#F8F3E6;border:1px solid var(--line);
}
.yili figcaption{
  margin:10px auto 0;font-size:13px;line-height:1.85;color:var(--muted);max-width:520px;
}
.yili figcaption b{display:block;color:var(--ink);font-weight:600;letter-spacing:.08em;margin-bottom:3px}
.yili figure.zoom{
  position:fixed;inset:0;z-index:80;margin:0;padding:16px;cursor:zoom-out;
  background:#F5F2ED;display:flex;align-items:center;justify-content:center;
}
.yili figure.zoom svg{width:auto;height:92vh;max-width:96vw;border:none}
.yili figure.zoom figcaption{display:none}
@media(max-width:520px){
  .yili figcaption{font-size:12.5px}
}
"""
        html = html.replace("</style>", css + "</style>", 1)

    # 2) 逐章插入
    heads = list(re.finditer(r'<h1 id="第(.+?)章', html))
    inserts = []
    for i, m in enumerate(heads):
        no = cn2int(m.group(1))
        start = m.start()
        nxt = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        seg = html[start:nxt]
        pos = seg.find('<h2 id="本章导读')
        if pos < 0:
            continue
        ks = by_ch.get(no, [])
        if not ks:
            continue
        parts = ['<div class="yili">',
                 '<p class="lead">义理图<span>　%d 幅</span></p>' % len(ks)]
        for k in ks:
            svg = open(os.path.join(FIGS, k + ".svg"), encoding="utf-8").read()
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
            title, one = meta.get(k, (k, ""))[:2]
            cap = "<b>%s</b>" % title
            if one:
                cap += "读图一句：%s。" % one
            parts.append('<figure>\n%s\n<figcaption>%s</figcaption>\n</figure>' % (svg, cap))
        parts.append("</div>\n")
        inserts.append((start + pos, "\n".join(parts)))

    for pos, block in reversed(inserts):
        html = html[:pos] + block + html[pos:]

    if "yiliZoom" not in html:
        zoom = """<script id="yiliZoom">
document.querySelectorAll(".yili figure").forEach(function (f) {
  f.addEventListener("click", function () { f.classList.toggle("zoom"); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") f.classList.remove("zoom");
  });
});
</script>
"""
        html = html.replace("</body>", zoom + "</body>", 1)
        html = html.replace("</style>", "\n</style>", 0) if False else html

    open(BOOK, "w", encoding="utf-8").write(html)
    print("插入 %d 章 · 图 %d 幅 · 文件 %d 字节"
          % (len(inserts), sum(len(v) for v in by_ch.values()), os.path.getsize(BOOK)))


if __name__ == "__main__":
    main()
