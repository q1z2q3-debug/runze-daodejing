#!/usr/bin/env python3
"""生成 book/义理图-版本总表.md：每幅现行图的历史版本清单。"""
import pathlib, re, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "book/义理图"
VER = (ROOT / "VERSION").read_text().strip()
CN = "零一二三四五六七八九"

def cn(n):
    if n < 10: return CN[n]
    if n == 10: return "十"
    if n < 20: return "十" + CN[n % 10]
    t, o = divmod(n, 10)
    return CN[t] + "十" + (CN[o] if o else "")

rows = []
for f in sorted(FIG.glob("*.svg")):
    m = re.match(r"ch(\d{2})[a-z]?-", f.name)
    if not m: continue
    n = int(m.group(1))
    hist = sorted((FIG / "_versions" / f"ch{n:02d}").glob(f"{f.stem}.v*.svg")) \
        if (FIG / "_versions" / f"ch{n:02d}").exists() else []
    vs = [re.search(r"\.v([\d.]+)\.svg$", h.name).group(1) for h in hist]
    rows.append((n, f.name, len(vs), vs))

lines = ["# 义理图版本总表", "",
         f"> 本文件由 `tools/version_index.py` 自动生成，勿手改。生成于 {time.strftime('%Y-%m-%d')}　版本 {VER}", "",
         "> 规矩：每一版都留，任何一版都不删。现行版在 `book/义理图/`，历史版在 `book/义理图/_versions/chNN/`。", "",
         "| 章 | 现行图 | 历史版本数 | 版本清单 |", "|---|---|---|---|"]
covered = len([r for r in rows if r[2]])
for n, name, cnt, vs in rows:
    lines.append(f"| 第{cn(n)}章 | `{name}` | {cnt} | {'、'.join('v'+v for v in vs) if vs else '—'} |")
lines += ["", f"**统计**：现行 {len(rows)} 幅，已建版本档 {covered} 幅，历史版本合计 {sum(r[2] for r in rows)} 份。"]
(ROOT / "book/义理图-版本总表.md").write_text("\n".join(lines) + "\n", encoding="utf8")
print(f"版本总表：现行 {len(rows)} 幅，有档 {covered} 幅")
