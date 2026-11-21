#!/usr/bin/env python3
"""生成单章义理图页：chapters/chNN.html（单文件、零外链、SVG 内联）。

用法：python3 tools/build_chapter_page.py 01
数据来源：book/义理图-总目.md（章、文件、题、金句）、book/义理图-复核账.md（该章复核节）。
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CN = "零一二三四五六七八九"

def cn_zh(n):
    d = "零一二三四五六七八九"
    if n < 10: return d[n]
    if n == 10: return "十"
    if n < 20: return "十" + d[n % 10]
    t, o = divmod(n, 10)
    return d[t] + "十" + (d[o] if o else "")

def cn_num(s):
    """汉字章号 → int（支持 一…八十一）"""
    s = s.replace("第", "").replace("章", "").strip()
    if not s: return 0
    if "十" in s:
        a, _, b = s.partition("十")
        tens = CN.index(a) if a else 1
        ones = CN.index(b) if b else 0
        return tens * 10 + ones
    return CN.index(s)

# 主图先、补图后；第一章另定义理推进序
ORDER = {
    1: ["ch01-wu-you.svg", "ch01-miao-jiao.svg", "ch01-zhi-yue.svg",
        "ch01d-yong-xian-pan-ju.svg", "ch01e-you-wu-shuang-guan.svg"],
}

def parse_inventory(n):
    txt = (ROOT / "book/义理图-总目.md").read_text(encoding="utf8")
    rows = []
    for line in txt.splitlines():
        m = re.match(r"\| (第[^|]+章) \| `([^`]+)` \| ([^|]+) \| (.+) \|$", line.strip())
        if m and cn_num(m.group(1)) == n:
            rows.append({"file": m.group(2), "title": m.group(3).strip(), "gold": m.group(4).strip()})
    return rows

def parse_review(n, name):
    p = ROOT / "book/义理图-复核账.md"
    if not p.exists(): return ""
    txt = p.read_text(encoding="utf8")
    m = re.search(r"^## 第[^\n]*章｜[^\n]*\n(.*?)(?=^## |\Z)", txt, flags=re.S | re.M)
    # 取章号匹配
    for sec in re.finditer(r"^## (第[^｜]+)｜([^\n]*)\n(.*?)(?=^## |\Z)", txt, flags=re.S | re.M):
        if cn_num(sec.group(1)) == n:
            return sec.group(3).strip()
    return ""

def md2html(md):
    out, i, lines = [], 0, md.splitlines()
    while i < len(lines):
        l = lines[i].rstrip()
        if not l.strip():
            i += 1; continue
        if l.startswith("|"):
            head = []
            while i < len(lines) and lines[i].startswith("|"):
                head.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in head]
            cells = [c for c in cells if not all(set(x) <= set("-: ") for x in c)]
            out.append("<table>")
            for k, row in enumerate(cells):
                tag = "th" if k == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>")
            out.append("</table>")
            continue
        if l.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("</ul>")
            continue
        if re.match(r"^\d+\. ", l):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                out.append(f"<li>{inline(re.sub(r'^\d+\. ', '', lines[i]))}</li>"); i += 1
            out.append("</ol>")
            continue
        out.append(f"<p>{inline(l)}</p>"); i += 1
    return "\n".join(out)

def inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s

STYLE = """
:root{--paper:#F8F3E6;--ink:#2F2A24;--seal:#A2503B;--green:#4A5C55;--line:#DCCBB0}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif;line-height:1.85}
.wrap{max-width:1000px;margin:0 auto;padding:56px 28px 96px}
.top{font-family:'Noto Sans CJK SC',sans-serif;font-size:12px;letter-spacing:2px;color:var(--seal)}
.top a{color:var(--seal);text-decoration:none;border-bottom:1px dotted var(--seal);margin-right:18px}
h1{font-size:30px;font-weight:400;margin:14px 0 4px;letter-spacing:1px}
.sub{color:#6E6459;font-size:13.5px;margin:0 0 8px}
.meta{font-family:'Noto Sans CJK SC',sans-serif;font-size:11.5px;letter-spacing:1.2px;color:#A89577;
 border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0;margin:22px 0 40px}
figure{margin:0 0 54px;padding:0}
figure svg{display:block;width:100%;height:auto;border:1px solid var(--line)}
.cap{display:flex;gap:14px;align-items:baseline;margin:10px 0 0;
 font-family:'Noto Sans CJK SC',sans-serif;font-size:12px;color:#6E6459;letter-spacing:.6px}
.cap b{font-weight:600;color:var(--ink);font-size:13.5px;letter-spacing:1px}
.cap .gold{color:var(--seal)}
.zoom{margin-left:auto;color:#A89577;text-decoration:none;border-bottom:1px dotted #C8B79A;
 font-size:11.5px;letter-spacing:1px;white-space:nowrap}
.badge{display:inline-block;font-size:10.5px;letter-spacing:2px;color:#A89577;border:1px solid var(--line);
 padding:1px 7px;margin-right:10px}
h2{font-size:15px;font-weight:600;letter-spacing:2px;color:var(--green);margin:48px 0 10px;
 padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:14px;font-weight:600;margin:26px 0 6px}
p{margin:8px 0;font-size:15px}
strong{color:var(--seal);font-weight:600}
code{font-family:'Noto Sans Mono CJK SC',monospace;font-size:12px;background:#EFE7D5;padding:1px 4px;border-radius:2px}
table{border-collapse:collapse;width:100%;margin:14px 0 18px;font-size:14px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#EFE7D5;font-family:'Noto Sans CJK SC',sans-serif;font-size:12.5px;letter-spacing:1px;font-weight:600}
ul,ol{margin:8px 0;padding-left:22px;font-size:15px}
li{margin:4px 0}
.foot{margin-top:56px;padding-top:14px;border-top:1px solid var(--line);
 font-family:'Noto Sans CJK SC',sans-serif;font-size:11px;letter-spacing:1.6px;color:#A89577}
"""

def build(n):
    rows = parse_inventory(n)
    if not rows: sys.exit(f"章 {n} 在总目里没有条目")
    order = ORDER.get(n)
    if order:
        rows.sort(key=lambda r: order.index(r["file"]) if r["file"] in order else 99)
    ch_name = rows and f"第{n}章"
    title_map = {1: "道可道，非常道"}
    zh = cn_zh(n)
    chapter_title = title_map.get(n, "")
    review = parse_review(n, chapter_title)
    ver = (ROOT / "VERSION").read_text().strip()
    figs = []
    for r in rows:
        svg = (ROOT / "book/义理图" / r["file"]).read_text(encoding="utf8")
        badge = "补图" if re.search(rf"ch{n:02d}[d-z]", r["file"]) else "主图"
        figs.append(f"""<figure>
{svg}
<figcaption class="cap"><span class="badge">{badge}</span><b>{r['title']}</b><span>{r['file']}</span><span class="gold">金句：{r['gold']}</span><a class="zoom" href="../book/义理图/{r['file'][:-4]}.png" target="_blank" rel="noopener">看原图</a></figcaption>
</figure>""")
    body = "\n".join(figs)
    if review:
        body += f"\n<h2>复核账</h2>\n{md2html(review)}"
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>润泽说 道可道之道德经 · 第{zh}章 义理图</title>
<style>{STYLE}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">总站</a><a href="../book/道可道·道德经心法读本.html">阅读版</a><a href="../book/义理图-总目.md">总目</a></div>
<h1>第{zh}章｜{chapter_title}</h1>
<p class="sub">一章三图为本；本章另有补图，补图不占主图位次，只为另开一境。</p>
<div class="meta">正册共 {len(rows)} 幅　·　复核账随章落地　·　版本 {ver}</div>
{body}
<div class="foot">润泽说 道可道之道德经　·　义理图单章页　·　版本 {ver}</div>
</div></body></html>"""
    out = ROOT / "chapters" / f"ch{n:02d}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf8")
    print(f"{out.relative_to(ROOT)}  {len(html.encode())} B  图 {len(rows)} 幅  复核账 {'有' if review else '无'}")

if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
