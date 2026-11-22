# 图库总目生成器 —— 在仓库根执行：python3 tools/inventory.py
# 依据：tools/make_yili_svg.py 的 FIGS/GOLD（正册）+ 磁盘实况（参照稿、旧稿）
import importlib.util, glob, os, re, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_gen():
    spec = importlib.util.spec_from_file_location("m", os.path.join(REPO, "tools", "make_yili_svg.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def cn_num(s):
    s = s.replace("第", "").replace("章", "")
    d = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
    if "十" in s:
        a, b = s.split("十")
        return (d.get(a, 1) if a else 1) * 10 + (d.get(b, 0) if b else 0)
    return d.get(s, 0)

def size_of(p):
    s = open(p, encoding="utf8").read(200)
    mm = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    return f"{mm.group(1)}×{mm.group(2)}" if mm else "?"

# 参照稿：人工登记的说明（新增一张须在此补一行）
REF_NOTE = {
 "ziqian/ziqian-ch01": ("子虔版第 23 页观妙图，忠实仿画", "参照·仿画"),
 "ziqian/ziqian-ch01-visible": ("仿画叠「物质→生态」可见可感色带", "参照·仿画"),
 "ziqian/ziqian-ladder": ("补全十九级涌现阶梯，两曲线交点落「人体」", "参照·骨架"),
 "ziqian/ziqian-ladder-visible": ("阶梯叠三段色面：须知仪器／肉眼与身体可及／可见而不可及", "参照·骨架"),
 "alt/dao-sheng-yi-er-san": ("生成之序：无·一·二·三·万，反者道之动为引擎", "备选·不落（拟 ch01f）"),
}
OLD_NOTE = {
 "ch38-wu-ji": "五级滑落旧稿，被同章新图取代",
 "ch51-sheng-bu-you": "生而不有旧稿，被同章新图取代",
 "ch67-san-bao": "三宝旧稿，被同章新图取代",
 "ch77-zhang-gong": "张弓旧稿，被同章新图取代",
 "ch81-bu-ji": "九个不旧稿，被同章新图取代",
 "ch05c-yi-jia-tian-ping": "天平旧稿，用户否决后改画一把锁",
}

def func_gold_map():
    """函数名 -> 金句键：扫描源码里每个 def 内的 gold(...) 调用"""
    src = open(os.path.join(REPO, "tools", "make_yili_svg.py"), encoding="utf8").read()
    out = {}
    for mm in re.finditer(r"^def (\w+)\(", src, re.M):
        name = mm.group(1)
        seg = src[mm.end(): mm.end() + 40000]
        g = re.search(r'gold\([^,]+,\s*"([^"]+)"', seg)
        if g:
            out[name] = g.group(1)
    return out

def build():
    m = load_gen()
    fg = func_gold_map()
    figs = m.FIGS
    gold = m.GOLD
    ver = open(os.path.join(REPO, "VERSION"), encoding="utf8").read().strip()
    hp = os.path.join(REPO, ".git", "HEAD")
    head = open(hp, encoding="utf8").read().strip()
    if head.startswith("ref: "):
        rp = os.path.join(REPO, ".git", head[5:].strip())
        head = open(rp, encoding="utf8").read().strip() if os.path.exists(rp) else "unborn"
    L = []
    L.append("# 义理图总目\n")
    L.append("> 本文件由 `tools/inventory.py` 自动生成，勿手改。改图请改 `tools/make_yili_svg.py` 后重跑本器。\n")
    L.append(f"> 生成于 {datetime.date.today()}　　版本 {ver}　　HEAD `{head[:7]}`\n")
    L.append("\n图分三类，不可混：**正册**（一章三图，另设补图）／**参照稿**（学习与待入册，不计入）／**存疑旧稿**（被否，留档不销毁）。\n")

    # 甲 正册
    # 主图/补图按「每章前三幅」定，不按字母：既有章从 b 起编（如第四十一章 b/c/d），
    # 只看字母会误判。同章排序：无字母在前，带字母按字典序。
    from collections import defaultdict as _dd
    per = _dd(list)
    for k, v in figs.items():
        per[v[0]].append(k)
    extra_n = 0
    for ch, ks in per.items():
        ks.sort(key=lambda k: (0 if re.match(r"^ch\d\d-", k) else 1, k))
        extra_n += max(0, len(ks) - 3)
    main_n = len(figs) - extra_n
    L.append(f"\n## 甲 正册 · {len(figs)} 幅（八十一章：主图 {main_n} 幅，补图 {extra_n} 幅）\n")
    L.append("| 章 | 文件 | 题 | 金句（首句） |\n|---|---|---|---|")
    rows = []
    for k, v in figs.items():
        ch, title = v[0], v[1]
        gk = fg.get(getattr(v[2], "__name__", "")) or k.split("-")[0]
        g = gold.get(gk, [])
        first = g[0] if g else "—"
        rows.append((cn_num(ch), k, ch, title, first))
    rows.sort(key=lambda r: (r[0], r[1]))
    for _, k, ch, title, first in rows:
        L.append(f"| {ch} | `{k}.svg` | {title} | {first} |")
    L.append(f"\n合计 **{len(figs)}** 幅：八十一章各三幅主图（{main_n}），另有补图 {extra_n} 幅（第一章 d／e、第二十八章 d、第三十章 d／e、第三十一章 d、第三十二章 d／e）。\n")

    # 乙 参照稿 / 备选（分两组列，不混）
    refdir = os.path.join(REPO, "book", "义理图", "_refs")
    groups = [("乙·一 参照稿（子虔）", "ziqian/"), ("乙·二 备选（成形未落）", "alt/")]
    n_ref = n_alt = 0
    for gtitle, pref in groups:
        L.append(f"\n## {gtitle} · 不计入正册\n")
        L.append("| 文件 | 尺寸 | 是什么 | 状态 |\n|---|---|---|---|")
        for p_ in sorted(glob.glob(os.path.join(refdir, pref + "*.svg"))):
            rel = os.path.relpath(p_, refdir)[:-4]
            note, st = REF_NOTE.get(rel, ("（未登记，请在 tools/inventory.py 的 REF_NOTE 补一行）", "未登记"))
            L.append(f"| `_refs/{rel}.svg` | {size_of(p_)} | {note} | {st} |")
            if pref == "alt/":
                n_alt += 1
            else:
                n_ref += 1

    # 丙 旧稿
    L.append("\n## 丙 存疑旧稿 · 留档不销毁\n")
    L.append("| 文件 | 说明 |\n|---|---|")
    n_old = 0
    for p in sorted(glob.glob(os.path.join(REPO, "book", "义理图", "old", "*.svg"))):
        k = os.path.basename(p)[:-4]
        L.append(f"| `old/{k}.svg` | {OLD_NOTE.get(k, '早期改版，被同章新图取代（缘由待补）')} |")
        n_old += 1

    # 丁 统计
    L.append("\n## 丁 统计与规矩\n")
    L.append(f"- 正册 {len(figs)} 幅（svg＋png 各一份，含补图 {extra_n}（第一章 d／e、第二十八章 d、第三十章 d／e、第三十一章 d、第三十二章 d／e））；参照稿 {n_ref} 组；备选 {n_alt} 组；旧稿 {n_old} 幅。")
    L.append("- 命名：正册 `chNNx-短题.svg`（NN 章号两位，x 为 a/b/c 序号，短题为汉语拼音连写）；参照稿 `_refs/<来源>/<名>.svg`；旧稿原键不动，便于追溯被谁取代。")
    L.append("- 只认 `tools/make_yili_svg.py` 的 FIG 键为「正册」；`_refs/` 与 `old/` 一律不计入 243。")
    L.append("- 出图：`python3 tools/make_yili_svg.py <完整键名>`；参照稿：`python3 tools/refs/refs_*.py`。")
    L.append("- 被否的稿不许删，撤入 `old/` 并在本表登记缘由；缘由一时说不清的，写「待补」，不编造。")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    out = build()
    open(os.path.join(REPO, "book", "义理图-总目.md"), "w", encoding="utf8").write(out)
    print(f"ok  {len(out)} 字节")
