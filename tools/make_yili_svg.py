#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""义理图生成：手写 SVG，按《道德经》章次出图。

体例（承《论语》图示规矩，2026-11-19 定）：
- 竖排单版，宽 380，高按内容定，一次只讲一个关系；
- 纸墨四色：墨 #2F2A24、赭 #A2503B、青 #4A5C55、线 #DCCBB0 / #E6D8C2，纸 #F8F3E6；
- 字号不小于 10.5，图上文字只作标注，不成段；
- 不画人物像，不写字帖；不用生成模型，不引外链；
- 坐标一律由常量推出，不手填零散数字。

用法：
    python3 tools/make_yili_svg.py            # 生成全部已登记的图
    python3 tools/make_yili_svg.py ch01       # 只生成一章
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "义理图")

INK, SEAL, GREEN, LINE, LINE2, PAPER = "#2F2A24", "#A2503B", "#4A5C55", "#DCCBB0", "#E6D8C2", "#F8F3E6"
SERIF = "'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS = "'Noto Sans CJK SC','Noto Sans SC',sans-serif"


def head(w, h, aria, kicker, title, sub, total_h=None):
    """统一页头：小字题签、主标题、一句副题。返回 (svg 片段, 内容起始 y)。"""
    y0 = 26
    s = [f'<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg viewBox="0 0 {w} {total_h or h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{aria}" '
         f'font-family="{SERIF}">',
         f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 z" fill="#6E6459"/></marker>'
         f'<marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 z" fill="{GREEN}"/></marker>'
         f'<marker id="arrL" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M10 0 L0 5 L10 10 z" fill="{GREEN}"/></marker>'
         f'<marker id="arrS" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 z" fill="{SEAL}"/></marker></defs>',
         f'<rect x="0" y="0" width="{w}" height="{total_h or h}" fill="{PAPER}"/>',
         f'<text x="20" y="{y0}" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">{kicker}</text>',
         f'<text x="20" y="{y0 + 32}" font-size="21" fill="{INK}">{title}</text>']
    if sub:
        s.append(f'<text x="20" y="{y0 + 52}" font-size="10.5" fill="#6E6459">{sub}</text>')
    return "\n".join(s), y0 + (74 if sub else 62)


def box(x, y, w, h, fill="none", stroke=LINE, dash=None, width=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}/>'


def txt(x, y, t, size=11, fill=None, anchor="start", font=None, weight=None, spacing=None, opacity=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    f = f' font-family="{font}"' if font else ""
    wgt = f' font-weight="{weight}"' if weight else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill or INK}"{a}{f}{wgt}{sp}{op}>{t}</text>'


def arrow(x1, y1, x2, y2, color="#6E6459", width=1.2, dash=None, head="arr"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d} '
            f'marker-end="url(#{head})"/>')


def vline(x, y1, y2, color=LINE, width=1):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


# ============ 第一章 · 无有同出 ============
def ch01_wu_you():
    W, H = 380, 624
    body, y = head(W, H, "无与有同出而异名：一个场，两种取景", "第 一 章 · 总 纲", "无、有同出",
                   "不是两个东西，是同一个场的两种取景。", H)
    s = [body]
    # 顶：道 · 未形（虚线场）
    s.append(box(110, y, 160, 54, fill="#F2EADA", stroke=LINE, dash="4 4"))
    s.append(txt(190, y + 24, "道 · 未形", 12.5, INK, "middle"))
    s.append(txt(190, y + 42, "不可名，只可取其向", 10.5, "#6E6459", "middle"))
    # 分叉
    s.append(arrow(170, y + 56, 118, y + 86))
    s.append(arrow(210, y + 56, 282, y + 86))
    # 左右：无 / 有
    yb = y + 88
    s.append(box(20, yb, 150, 96, fill="#FBF6EC"))
    s.append(txt(30, yb + 24, "无", 18, SEAL))
    s.append(txt(52, yb + 24, "名天地之始", 10.5, "#6E6459"))
    s.append(txt(30, yb + 48, "取其未定形的那一面", 10.5, INK))
    s.append(txt(30, yb + 68, "观其妙：微而未显", 10.5, GREEN))
    s.append(txt(30, yb + 86, "——不是「什么都没有」", 10, "#6E6459"))

    s.append(box(210, yb, 150, 96, fill="#FBF6EC"))
    s.append(txt(220, yb + 24, "有", 18, SEAL))
    s.append(txt(242, yb + 24, "名万物之母", 10.5, "#6E6459"))
    s.append(txt(220, yb + 48, "取其已成形的那一面", 10.5, INK))
    s.append(txt(220, yb + 68, "观其徼：显而有界", 10.5, GREEN))
    s.append(txt(220, yb + 86, "——不是「永远在场」", 10, "#6E6459"))

    # 相生环
    yc = yb + 96 + 18
    s.append(f'<path d="M 120 {yc - 6} Q 190 {yc - 26} 260 {yc - 6}" fill="none" stroke="{GREEN}" stroke-width="1.1" '
             f'marker-end="url(#arr)"/>')
    s.append(f'<path d="M 260 {yc + 14} Q 190 {yc + 34} 120 {yc + 14}" fill="none" stroke="{GREEN}" stroke-width="1.1" '
             f'marker-end="url(#arr2)"/>')
    s.append(txt(190, yc + 2, "相 生", 11, GREEN, "middle", spacing="2"))
    s.append(txt(190, yc + 52, "无生有，有归无；一环不居", 10.5, "#6E6459", "middle"))

    # 同出而异名
    yd = yc + 66
    s.append(vline(190, yd - 6, yd + 10, "#C9B79A"))
    s.append(box(70, yd + 10, 240, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yd + 36, "同 出 而 异 名", 13, INK, "middle", spacing="2"))

    # 玄
    yx = yd + 66
    s.append(arrow(190, yx - 16, 190, yx + 6))
    s.append(f'<circle cx="190" cy="{yx + 46}" r="40" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(txt(190, yx + 42, "玄", 22, SEAL, "middle"))
    s.append(txt(190, yx + 62, "又 玄", 10, "#6E6459", "middle", spacing="1"))
    s.append(txt(190, yx + 104, "名是取景，不是东西；取景一换，名就换。", 10.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第一章 · 指月三境 ============
def ch01_zhi_yue():
    W, H = 380, 636
    body, y = head(W, H, "指月三境：执字、会心、入境", "第 一 章 · 读 法", "指月三境",
                   "手指指月，人常盯着手指。三层就是把手指松开。", H)
    s = [body]
    bands = [
        ("第一境 · 执字", "老子讲，我记；主客分明", "字是讲义：字义、断句、概念", 3, 1.0),
        ("第二境 · 会心", "顺指望去，知其所指", "方向对了，隔阂淡了", 2, 0.55),
        ("第三境 · 入境", "指、言、经俱舍；唯有月在", "没有读经的我，也没有被读的经", 0, 0.0),
    ]
    yb = y
    for i, (t1, t2, t3, strokes, op) in enumerate(bands):
        h = 116
        s.append(box(20, yb, 340, h, fill="#FBF6EC" if i else "#F2EADA"))
        s.append(txt(32, yb + 26, t1, 13, SEAL if i == 0 else (INK if i == 1 else GREEN)))
        s.append(txt(32, yb + 48, t2, 10.5, INK))
        s.append(txt(32, yb + 68, t3, 10.5, "#6E6459"))
        # 手（随层递减笔画）
        hx, hy = 232, yb + 68
        if strokes:
            # 一指：袖口 + 指身（三角），越往后越短、越淡
            tip = 300 - (0 if strokes == 3 else 16)
            s.append(f'<path d="M {hx} {hy + 10} L {tip} {hy + 2} L {tip} {hy + 12} Z" fill="{INK}" opacity="{op * 0.9:.2f}" stroke="none"/>')
            s.append(f'<line x1="{hx}" y1="{hy - 2}" x2="{hx}" y2="{hy + 22}" stroke="{INK}" stroke-width="1.1" opacity="{op}"/>')
            if strokes >= 2:
                s.append(f'<line x1="{hx + 6}" y1="{hy + 2}" x2="{hx + 6}" y2="{hy + 20}" stroke="{INK}" stroke-width="0.7" opacity="{op}"/>')
            if strokes >= 3:
                s.append(f'<line x1="{tip - 10}" y1="{hy + 4}" x2="{tip - 6}" y2="{hy + 10}" stroke="{INK}" stroke-width="0.7" opacity="{op}"/>')
        # 月
        r = 16 if i < 2 else 24
        mx, my = (320, yb + 60) if i < 2 else (306, yb + 58)
        s.append(f'<circle cx="{mx}" cy="{my}" r="{r}" fill="none" stroke="{GREEN}" stroke-width="{1.3 if i < 2 else 1.7}" opacity="{1 if i == 2 else 0.65}"/>')
        if i < 2:
            s.append(f'<circle cx="{mx}" cy="{my}" r="{r - 6}" fill="none" stroke="{GREEN}" stroke-width="0.8" opacity="0.5"/>')
            s.append(txt(mx, my + 46, "月", 10, "#6E6459", "middle"))
        else:
            s.append(f'<circle cx="{mx}" cy="{my}" r="{r + 7}" fill="none" stroke="{GREEN}" stroke-width="0.5" opacity="0.35"/>')
        if i < 2:
            s.append(arrow(190, yb + h, 190, yb + h + 22, "#C9B79A", 1.0))
        yb += h + 24
    s.append(txt(190, yb + 12, "松手不是丢掉字，是不再靠字。", 10.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第一章 · 妙徼两层 ============
def ch01_miao_jiao():
    W, H = 380, 636
    body, y = head(W, H, "观妙与观徼：向下探未形，向上看见界", "第 一 章 · 观 法", "观妙 · 观徼",
                   "同一件事，向下看是「妙」，向上看是「徼」。", H)
    s = [body]
    cx = 168
    top, bot = y + 10, y + 424
    s.append(vline(cx, top, bot, "#C9B79A", 1.2))
    s.append(arrow(cx, top, cx, top - 6, "#6E6459", 1.2))
    s.append(arrow(cx, bot, cx, bot + 6, "#6E6459", 1.2))
    # 上：徼
    s.append(txt(cx + 22, top + 16, "徼 · 已显", 11, GREEN))
    s.append(txt(cx + 22, top + 34, "层层显化：星系 · 生命 · 社群 · 乐", 10, "#6E6459"))
    for i, lab in enumerate(["星系", "生命", "社群"]):
        yy = top + 58 + i * 30
        s.append(f'<line x1="{cx - 26}" y1="{yy}" x2="{cx - 4}" y2="{yy}" stroke="{LINE}" stroke-width="1"/>')
        s.append(txt(cx - 32, yy + 4, lab, 9.5, "#8A7C69", "end"))
    # 中：界
    ymid = top + 196
    s.append(f'<ellipse cx="{cx}" cy="{ymid}" rx="88" ry="20" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(txt(cx, ymid + 4, "显 界", 10.5, "#6E6459", "middle", spacing="2"))
    s.append(txt(cx, ymid + 36, "界之内是「有」；界之外不是空，是未显。", 10, "#6E6459", "middle"))
    # 下：妙
    yb2 = top + 292
    s.append(txt(cx + 22, yb2, "妙 · 未形", 11, SEAL))
    s.append(txt(cx + 22, yb2 + 18, "未定形处：量子 · 势能 · 未有之势", 10, "#6E6459"))
    s.append(txt(cx + 22, yb2 + 38, "不是没有，是还没显", 10, "#6E6459"))
    for i, lab in enumerate(["量子", "势能", "未发"]):
        yy = yb2 + 62 + i * 26
        s.append(f'<line x1="{cx - 26}" y1="{yy}" x2="{cx - 4}" y2="{yy}" stroke="{LINE}" stroke-width="1" stroke-dasharray="2 3"/>')
        s.append(txt(cx - 32, yy + 4, lab, 9.5, "#8A7C69", "end"))
    s.append(txt(cx, bot + 40, "两头都是同一件事：说「有」或说「无」，只在你站界内还是界外。", 10.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二章 · 六组对偶 ============
def ch02_liu_zu():
    W, H = 380, 548
    body, y = head(W, H, "六组对偶：执名则生对立", "第 二 章 · 对 照", "六组对偶",
                   "名一立，对面就跟着立；六组全是同一件事。", H)
    s = [body]
    pairs = [("有", "无"), ("难", "易"), ("长", "短"), ("高", "下"), ("音", "声"), ("前", "后")]
    yb = y + 4
    rowh = 40
    for i, (a, b) in enumerate(pairs):
        yy = yb + i * rowh
        s.append(f'<rect x="20" y="{yy}" width="150" height="{rowh - 8}" fill="#FBF6EC" stroke="{LINE2}"/>')
        s.append(f'<rect x="210" y="{yy}" width="150" height="{rowh - 8}" fill="#FBF6EC" stroke="{LINE2}"/>')
        s.append(txt(95, yy + 23, a, 12, SEAL, "middle"))
        s.append(txt(285, yy + 23, b, 12, SEAL, "middle"))
        s.append(f'<path d="M 178 {yy + 16} L 202 {yy + 16}" stroke="{GREEN}" stroke-width="1" '
                 f'marker-start="url(#arrL)" marker-end="url(#arr)"/>')
    yend = yb + len(pairs) * rowh
    s.append(txt(190, yb - 8, "名 之 一 侧", 10, "#6E6459", "middle", spacing="1"))
    s.append(txt(190, yend + 18, "相 生 相 成：无此则无彼", 10.5, GREEN, "middle", spacing="1"))
    # 结论
    s.append(box(20, yend + 34, 340, 76, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(32, yend + 60, "是以圣人处无为之事", 12.5, INK))
    s.append(txt(32, yend + 82, "不立这把尺，故不随之起倒；行不言之教，事成而不居。", 10.5, "#6E6459"))
    s.append(txt(32, yend + 100, "执一岸，必被另一岸牵着走。", 10.5, SEAL))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第十一章 · 三容器：利与用 ============
def ch11_li_yong():
    W, H = 380, 596
    body, y = head(W, H, "车、器、室三容器：有给利，无给用", "第 十 一 章 · 器 喻", "利与用",
                   "三件东西，一个道理：有形给依托，虚空给功能。", H)
    s = [body]
    rows = [
        ("毂", "辐、毂、舆", "毂中之虚", "轴穿而转", "车之用"),
        ("器", "黏土、器壁", "器腹之腔", "盛而能容", "器之用"),
        ("室", "墙、户、牖", "室中之虚", "居而能通", "室之用"),
    ]
    yb = y + 2
    for i, (icon, you, wu, act, use) in enumerate(rows):
        h = 106
        s.append(box(20, yb, 340, h, fill="#FBF6EC" if i % 2 == 0 else "#F6EFE0"))
        # 图标
        cx, cy = 56, yb + 50
        if i == 0:
            import math
            s.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{INK}" stroke-width="1.1"/>')
            for k in range(12):
                a = math.radians(k * 30)
                s.append(f'<line x1="{cx + 7*math.cos(a):.1f}" y1="{cy + 7*math.sin(a):.1f}" '
                         f'x2="{cx + 20*math.cos(a):.1f}" y2="{cy + 20*math.sin(a):.1f}" stroke="{INK}" stroke-width="0.7"/>')
            s.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{SEAL}" stroke-width="1"/>')
        elif i == 1:
            s.append(f'<path d="M {cx-22} {cy-14} Q {cx} {cy+22} {cx+22} {cy-14}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
            s.append(f'<line x1="{cx-24}" y1="{cy-14}" x2="{cx+24}" y2="{cy-14}" stroke="{INK}" stroke-width="0.9"/>')
            s.append(f'<line x1="{cx-22}" y1="{cy-14}" x2="{cx+22}" y2="{cy-14}" stroke="{SEAL}" stroke-width="0.5" opacity="0.6"/>')
        else:
            s.append(box(cx - 24, cy - 14, 48, 30, "none", INK, None, 1.1))
            s.append(f'<line x1="{cx-8}" y1="{cy-14}" x2="{cx-8}" y2="{cy+16}" stroke="{SEAL}" stroke-width="1"/>')
        s.append(txt(cx, yb + 88, icon, 10, "#8A7C69", "middle"))
        # 文字两列
        s.append(txt(96, yb + 28, you, 11, SEAL))
        s.append(txt(96, yb + 46, "有 · 立界", 10, "#6E6459"))
        s.append(txt(96, yb + 72, wu, 11, GREEN))
        s.append(txt(96, yb + 90, "无 · 让位", 10, "#6E6459"))
        s.append(txt(248, yb + 44, act, 11, INK))
        s.append(txt(248, yb + 62, use, 10.5, "#6E6459"))
        yb += h + 8
    # 结语
    yc = yb + 6
    s.append(box(20, yc, 340, 58, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 24, "有之以为利，无之以为用", 13, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 44, "不是先有器壁再补一个空，是器壁把那个空撑出来。", 10, "#6E6459", "middle"))
    s.append(txt(190, yc + 78, "该立多少界，该留多少空——这是一份分寸表，不是技巧。", 10.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二十二章 · 曲则全 ============
def ch22_qu_ze_quan():
    W, H = 380, 640
    body, y = head(W, H, "六句三截：能受、肯少、然后抱一", "第 二 十 二 章 · 处 世", "曲则全",
                   "六句不是六条策略，是同一条规律的六个截面。", H)
    s = [body]
    # 形四句
    s.append(txt(20, y + 12, "一 · 就形说：姿态能屈", 10.5, SEAL))
    pairs = [("曲", "全", "能受"), ("枉", "直", "屈而后伸"), ("洼", "盈", "低处聚水"), ("敝", "新", "旧极则新")]
    yb = y + 22
    for i, (a, b, note) in enumerate(pairs):
        yy = yb + i * 34
        s.append(f'<rect x="20" y="{yy}" width="44" height="26" fill="#FBF6EC" stroke="{LINE2}"/>')
        s.append(txt(42, yy + 18, a, 11.5, INK, "middle"))
        s.append(f'<line x1="70" y1="{yy+13}" x2="94" y2="{yy+13}" stroke="{GREEN}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(f'<rect x="100" y="{yy}" width="44" height="26" fill="#F2EADA" stroke="{LINE}"/>')
        s.append(txt(122, yy + 18, b, 11.5, GREEN, "middle"))
        s.append(txt(156, yy + 18, note, 10, "#6E6459"))
    # 量二句
    yq = yb + 4 * 34 + 10
    s.append(txt(20, yq + 12, "二 · 就量说：心里的账", 10.5, SEAL))
    for i, (a, b, note) in enumerate([("少", "得", "手里不满，才接得住"), ("多", "惑", "尺子越多，越量不准")]):
        yy = yq + 22 + i * 34
        s.append(f'<rect x="20" y="{yy}" width="44" height="26" fill="#FBF6EC" stroke="{LINE2}"/>')
        s.append(txt(42, yy + 18, a, 11.5, INK, "middle"))
        s.append(f'<line x1="70" y1="{yy+13}" x2="94" y2="{yy+13}" stroke="{GREEN}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(f'<rect x="100" y="{yy}" width="44" height="26" fill="#F2EADA" stroke="{LINE}"/>')
        s.append(txt(122, yy + 18, b, 11.5, GREEN if i == 0 else SEAL, "middle"))
        s.append(txt(156, yy + 18, note, 10, "#6E6459"))
    # 抱一
    y1 = yq + 22 + 2 * 34 + 6
    s.append(vline(190, y1 - 4, y1 + 8, "#C9B79A"))
    s.append(box(110, y1 + 8, 160, 34, fill="#E9DFCC", stroke="#C9B79A"))
    s.append(txt(190, y1 + 31, "抱一 · 为天下式", 11.5, INK, "middle"))
    # 四不 → 四果
    y2 = y1 + 54
    quads = [("不自见", "故明"), ("不自是", "故彰"), ("不自伐", "故有功"), ("不自矜", "故长")]
    for i, (a, b) in enumerate(quads):
        col, row = i % 2, i // 2
        x = 20 + col * 172
        yy = y2 + row * 32
        s.append(txt(x, yy + 18, a, 10.5, INK))
        s.append(f'<line x1="{x+62}" y1="{yy+13}" x2="{x+86}" y2="{yy+13}" stroke="{LINE}" stroke-width="1"/>')
        s.append(txt(x + 92, yy + 18, b, 10.5, GREEN))
    # 收
    y3 = y2 + 2 * 32 + 10
    s.append(box(20, y3, 340, 50, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 22, "夫唯不争，故天下莫能与之争", 11, INK, "middle"))
    s.append(txt(190, y3 + 41, "诚全而归之：归是回家，不是得利。", 10, SEAL, "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二十五章 · 有物混成 ============
def ch25_dao_fa():
    W, H = 380, 562
    body, y = head(W, H, "名只是手指，四大只到自然为止", "第 二 十 五 章 · 总 纲", "道法自然",
                   "不是它比天地老，是天地离了它不成。", H)
    s = [body]
    # 名与指
    y0 = y + 4
    s.append(txt(20, y0 + 12, "强为之名：字之曰道，名之曰大", 8.8, "#8A7C69"))
    names = ["道", "大", "逝", "远", "反"]
    for i, n in enumerate(names):
        s.append(box(20 + i * 44, y0 + 20, 38, 26, fill="#F2EADA", stroke="#C9B79A"))
        s.append(txt(39 + i * 44, y0 + 38, n, 10, SEAL, "middle"))
    s.append(arrow(250, y0 + 33, 296, y0 + 33, color="#6E6459", head="arr"))
    s.append(f'<circle cx="324" cy="{y0+33}" r="18" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(txt(324, y0 + 37, "？", 11, "#6E6459", "middle"))
    s.append(txt(20, y0 + 62, "名是给有边界的东西用的；对没有边界的东西，名只是手指。", 8.2, "#8A7C69"))
    # 四大：人地天道
    y1 = y0 + 78
    lv = [("王", "人亦大：四大之一"), ("地", "厚而载"), ("天", "覆而运"), ("道", "自本自根")]
    for i, (a, b) in enumerate(lv):
        yy = y1 + i * 26
        s.append(box(20, yy, 92, 22, fill="#FBF6EC" if i < 3 else "#E9DFCC", stroke="#C9B79A"))
        s.append(txt(66, yy + 15, a, 9.4, INK, "middle"))
        s.append(txt(120, yy + 15, b, 8.0, "#6E6459"))
        if i:
            s.append(arrow(66, yy - 4, 66, yy + 1, color="#C9B79A", head="arr"))
    s.append(txt(240, y1 + 14, "域中有四大，", 8.6, "#8A7C69"))
    s.append(txt(240, y1 + 30, "而王居其一焉。", 8.6, "#8A7C69"))
    # 四法
    y2 = y1 + 4 * 26 + 8
    s.append(box(20, y2, 340, 36, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 16, "人法地 → 地法天 → 天法道 → 道法自然", 9.6, INK, "middle"))
    s.append(txt(190, y2 + 31, "法者，以其为则：不是层层复制，是逐层取法。", 8.0, "#6E6459", "middle"))
    # 逝远反：一次呼吸
    y3 = y2 + 54
    cx, cy, r = 150, y3 + 44, 34
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    import math
    for k, lab in enumerate(["逝", "远", "反"]):
        ang = -90 + k * 120
        px = cx + r * math.cos(math.radians(ang))
        py = cy + r * math.sin(math.radians(ang))
        s.append(txt(px, py + 4, lab, 10, GREEN, "middle"))
    s.append(txt(cx, cy + 4, "环", 8.6, "#8A7C69", "middle"))
    s.append(txt(196, y3 + 26, "大曰逝，逝曰远，远曰反", 8.8, SEAL))
    s.append(txt(196, y3 + 42, "世界不是一场没有回头路的散开，", 8.2, "#6E6459"))
    s.append(txt(196, y3 + 56, "是一次呼吸。", 8.2, "#6E6459"))
    yc = y3 + 92
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "道法自然。", 10.4, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 33, "上面没有更高的东西在命令它：自己如此，不借外力。", 8.2, "#6E6459", "middle"))
    s.append(gold(yc + 48, "ch25"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十八章 · 五级滑落 ============
def ch38_wu_ji():
    W, H = 380, 652
    body, y = head(W, H, "道、德、仁、义、礼：一道五级台阶", "第 三 十 八 章 · 秩 序", "五级滑落",
                   "越往下，越靠「作意」撑；作意越重，越要强制。", H)
    s = [body]
    steps = [("道", "无", "万物自化"), ("上德", "无以为", "有德而不自知"),
             ("下德", "有以为", "守德而恐失"), ("仁", "为之而无以为", "体恤不图报"),
             ("义", "为之而有以为", "带是非立场"), ("礼", "攘臂而扔之", "强引使从")]
    yb = y + 4
    for i, (name, mark, note) in enumerate(steps):
        yy = yb + i * 50
        s.append(box(20, yy, 84, 40, fill="#FBF6EC" if i < 2 else "#F6EFE0"))
        s.append(txt(32, yy + 25, name, 12.5, SEAL if i > 1 else INK))
        s.append(txt(112, yy + 25, mark, 10.5, GREEN if i < 3 else SEAL))
        s.append(txt(206, yy + 25, note, 9.5, "#6E6459"))
        if i < len(steps) - 1:
            s.append(arrow(62, yy + 40, 62, yy + 48, "#C9B79A", 1.0))
    yend = yb + len(steps) * 50
    s.append(txt(20, yend + 14, "失道而后德，失德而后仁，失仁而后义，失义而后礼。", 10, "#6E6459"))
    s.append(box(20, yend + 28, 340, 64, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(32, yend + 50, "大丈夫处其厚，不居其薄；处其实，不居其华。", 10.5, INK))
    s.append(txt(32, yend + 72, "不是分出谁高谁低，是认清自己此刻站在第几级。", 10, "#6E6459"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十章 · 反者道之动 ============
def ch40_fan_zhe():
    W, H = 380, 536
    body, y = head(W, H, "反者道之动，弱者道之用：一台反向的机器", "第 四 十 章 · 公 理", "反向的机器",
                   "动力取自回环，方法取自柔曲，根基取自空位。", H)
    s = [body]
    # 左：环
    cx, cy, r = 110, y + 92, 58
    import math
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE2}" stroke-width="0.8"/>')
    def pt(deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)
    # 上弧：翻过去（外推），赭
    x1, y1 = pt(200); x2, y2 = pt(345)
    s.append(f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{SEAL}" stroke-width="1.5" marker-end="url(#arrS)"/>')
    # 下弧：翻回来（回归），青
    x3, y3 = pt(20); x4, y4 = pt(165)
    s.append(f'<path d="M {x3:.1f} {y3:.1f} A {r} {r} 0 0 1 {x4:.1f} {y4:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr2)"/>')
    s.append(txt(cx, cy + 4, "反", 15, INK, "middle"))
    s.append(txt(cx, cy + 26, "同一次翻转", 9.5, "#8A7C69", "middle"))
    s.append(txt(20, cy + r + 26, "赭：翻过去（推到头，另一端已在门口）", 9, SEAL))
    s.append(txt(20, cy + r + 42, "青：翻回来（回到源头，向内观照）", 9, GREEN))
    s.append(txt(20, y + 8, "反者 · 道之动", 10.5, INK))
    # 右：弱
    s.append(txt(206, y + 8, "弱者 · 道之用", 10.5, INK))
    s.append(f'<path d="M 216 {y+44} Q 260 {y+14} 300 {y+44} Q 322 {y+58} 344 {y+40}" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(txt(216, y + 76, "弱，木之柔曲；不是衰弱", 9.5, "#8A7C69"))
    # 对比表
    yt = y + 210
    s.append(box(20, yt, 160, 132, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(box(200, yt, 160, 132, fill="#FBF6EC", stroke="{LINE2}"))
    s.append(txt(32, yt + 22, "世人那台", 10.5, "#8A7C69"))
    s.append(txt(212, yt + 22, "老子那台", 10.5, GREEN))
    left = ["动力：加码", "方法：硬顶", "根基：堆叠", "→ 加到无处可加，卡死"]
    right = ["动力：回环", "方法：柔曲", "根基：空位", "→ 一直转"]
    for i in range(4):
        col_l = RGB = "#6E6459"
        s.append(txt(32, yt + 48 + i * 22, left[i], 9.5, "#6E6459"))
        s.append(txt(212, yt + 48 + i * 22, right[i], 9.5, GREEN if i == 3 else INK))
    # 底
    yb = yt + 148
    s.append(txt(190, yb, "天下万物生于有，有生于无。", 12, INK, "middle"))
    s.append(txt(190, yb + 20, "根基在空位：壁围出空，空生出用。", 10, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十二章 · 道生一 ============
def ch42_dao_sheng():
    W, H = 380, 520
    body, y = head(W, H, "道生一，一生二，二生三，三生万物", "第 四 十 二 章 · 生 发", "生发总图",
                   "三是被二撑出来的那道空，不是阴阳之外的第三样东西。", H)
    s = [body]
    chain = [("道", "无极 · 浑然未显"), ("一", "太极 · 未判"), ("二", "阴阳 · 有与无")]
    yb = y + 4
    for i, (n, note) in enumerate(chain):
        yy = yb + i * 56
        s.append(box(20, yy, 40, 34, fill="#E9DFCC" if i == 0 else "#FBF6EC"))
        s.append(txt(40, yy + 23, n, 14, INK, "middle"))
        s.append(txt(72, yy + 23, note, 10, "#6E6459"))
        s.append(arrow(66, yy + 34, 66, yy + 52, "#6E6459", 1.0))
    # 二三
    y2 = yb + 3 * 56 + 6
    s.append(txt(20, y2 + 4, "二生三：两端一立，中间撑开一道位", 10.5, INK))
    s.append(f'<rect x="20" y="{y2+16}" width="96" height="52" fill="#FBF6EC" stroke="{LINE2}"/>')
    s.append(txt(68, y2 + 48, "阴", 13, "#4A5C55", "middle"))
    s.append(f'<rect x="264" y="{y2+16}" width="96" height="52" fill="#FBF6EC" stroke="{LINE2}"/>')
    s.append(txt(312, y2 + 48, "阳", 13, SEAL, "middle"))
    s.append(f'<rect x="128" y="{y2+16}" width="124" height="52" fill="#F2EADA" stroke="#C9B79A" stroke-dasharray="3 3"/>')
    s.append(txt(190, y2 + 40, "三", 12, INK, "middle"))
    s.append(txt(190, y2 + 58, "虚位 · 冲气", 9.5, "#8A7C69", "middle"))
    # 万物
    yw = y2 + 82
    s.append(arrow(190, yw, 190, yw + 16, "#6E6459", 1.0))
    s.append(box(20, yw + 18, 340, 58, fill="#FBF6EC", stroke="{LINE2}"))
    s.append(txt(30, yw + 40, "三生万物：负阴而抱阳，冲气以为和。", 11, INK))
    s.append(txt(30, yw + 60, "配比不同、节律不同，遂显为万千物类。", 9.5, "#6E6459"))
    s.append(txt(190, yw + 96, "填实了那道空，生发即止——这是全书对「生」的唯一定义。", 10, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十一章 · 生而不有 ============
def ch51_sheng_bu_you():
    W, H = 380, 508
    body, y = head(W, H, "道生、德畜、物形、势成：四者合力而不居功", "第 五 十 一 章 · 玄 德", "生而不有",
                   "亭是有顶无壁的小屋；宰，是钻进屋里当差的那个人。", H)
    s = [body]
    feeders = [("道", "生"), ("德", "畜"), ("物", "形"), ("势", "成")]
    yb = y + 4
    for i, (n, v) in enumerate(feeders):
        x = 20 + i * 86
        s.append(box(x, yb, 76, 46, fill="#FBF6EC", stroke="{LINE2}"))
        s.append(txt(x + 38, yb + 20, n, 12, INK, "middle"))
        s.append(txt(x + 38, yb + 38, v + "之", 9.5, GREEN, "middle"))
        s.append(f'<line x1="{x + 38}" y1="{yb + 46}" x2="{x + 38}" y2="{yb + 58}" stroke="{LINE}" stroke-width="1"/>')
    # 合力条
    s.append(box(20, yb + 58, 340, 26, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(txt(190, yb + 76, "四者合力，万物以成", 10, "#6E6459", "middle"))
    # 六事
    yy = yb + 94
    s.append(box(20, yy, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yy + 18, "长之 · 育之 · 亭之 · 毒之 · 养之 · 覆之", 10.5, INK, "middle"))
    s.append(txt(190, yy + 36, "亭＝有顶无壁，让它停一停；毒＝厚，让它自己长厚", 9.5, "#6E6459", "middle"))
    # 三不
    y3 = yy + 58
    items = [("生而不有", "生了，不占为己有"), ("为而不恃", "做了，不拿它当本事"), ("长而不宰", "养了，不进那间屋当差")]
    for i, (a, b) in enumerate(items):
        y4 = y3 + i * 48
        s.append(txt(20, y4 + 20, a, 12, SEAL))
        s.append(txt(132, y4 + 20, b, 9.5, "#6E6459"))
    y5 = y3 + 3 * 48 + 4
    s.append(box(20, y5, 340, 40, fill="#E9DFCC", stroke="#C9B79A"))
    s.append(txt(190, y5 + 26, "是谓玄德", 12, INK, "middle", spacing="2"))
    s.append(txt(190, y5 + 62, "同一条德，落到人身上就是：养得住，放得下。", 10, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十七章 · 三宝 ============
def ch67_san_bao():
    W, H = 380, 548
    body, y = head(W, H, "慈、俭、不敢为天下先：三条活得久的约束", "第 六 十 七 章 · 三 宝", "三宝",
                   "「长」量的是时间，不是位次：做得成，还要做得久。", H)
    s = [body]
    cols = [("慈", "心里长草，护生", "勇"), ("俭", "把散出的收成一束绳", "广"), ("不敢为先", "不抢位次", "长 · 久")]
    yb = y + 4
    for i, (n, note, effect) in enumerate(cols):
        x = 20 + i * 116
        s.append(box(x, yb, 108, 108, fill="#FBF6EC", stroke="{LINE2}"))
        s.append(txt(x + 54, yb + 26, n, 13.5, SEAL if i < 2 else INK, "middle"))
        # 简符
        cx, cy = x + 54, yb + 52
        if i == 0:
            s.append(f'<path d="M {cx-16} {cy+8} Q {cx} {cy-16} {cx+16} {cy+8}" fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
            s.append(f'<line x1="{cx}" y1="{cy+8}" x2="{cx}" y2="{cy+18}" stroke="{GREEN}" stroke-width="1"/>')
        elif i == 1:
            for k in range(3):
                s.append(f'<path d="M {cx-14} {cy-8+k*9} Q {cx} {cy-16+k*9} {cx+14} {cy-8+k*9}" fill="none" stroke="{GREEN}" stroke-width="1"/>')
        else:
            s.append(f'<line x1="{cx-18}" y1="{cy+10}" x2="{cx+18}" y2="{cy+10}" stroke="{GREEN}" stroke-width="1"/>')
            s.append(f'<line x1="{cx-10}" y1="{cy+10}" x2="{cx-10}" y2="{cy-8}" stroke="{GREEN}" stroke-width="1"/>')
        s.append(txt(x + 54, yb + 86, note, 9, "#6E6459", "middle"))
        s.append(f'<line x1="{x+54}" y1="{yb+108}" x2="{x+54}" y2="{yb+124}" stroke="{LINE}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(txt(x + 54, yb + 142, effect, 11.5, GREEN if i < 2 else INK, "middle"))
    # 反面
    yw = yb + 158
    s.append(box(20, yw, 340, 50, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(30, yw + 20, "今舍慈且勇，舍俭且广，舍后且先，死矣。", 10.5, SEAL))
    s.append(txt(30, yw + 40, "三样一起舍，就是把「久」换成了「快」。", 9.5, "#6E6459"))
    s.append(txt(190, yw + 76, "夫慈，以战则胜，以守则固。", 11, INK, "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第七十七章 · 张弓 ============
def ch77_zhang_gong():
    W, H = 380, 618
    body, y = head(W, H, "张弓：上弦不是拉满，是找那个刚好", "第 七 十 七 章 · 调 平", "张弓",
                   "拉满是使力，调平是找平；拉满会断，调平才久。", H)
    s = [body]
    # 弓
    cx, cy = 190, y + 96
    s.append(f'<path d="M {cx-70} {cy+40} Q {cx} {cy-64} {cx+70} {cy+40}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="{cx-70}" y1="{cy+40}" x2="{cx+70}" y2="{cy+40}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(cx + 8, cy + 30, "弓", 9.5, "#8A7C69", "middle"))
    s.append(txt(cx + 46, cy + 58, "弦", 9.5, "#8A7C69"))
    # 高抑 / 下举
    s.append(arrow(cx - 96, cy - 6, cx - 44, cy - 48, "#C9B79A", 1.0))
    s.append(txt(20, cy - 52, "高者抑之：按，一只手够", 9.5, "#6E6459"))
    s.append(arrow(cx - 96, cy + 60, cx - 44, cy + 34, "#C9B79A", 1.0))
    s.append(txt(20, cy + 78, "下者举之：举，要两只手", 9.5, "#6E6459"))
    s.append(txt(cx + 84, cy - 4, "有余者损", 9.5, "#6E6459"))
    s.append(txt(cx + 84, cy + 16, "不足者补", 9.5, "#6E6459"))
    # 两天道
    yt = cy + 108
    s.append(box(20, yt, 160, 96, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(box(200, yt, 160, 96, fill="#FBF6EC", stroke="{LINE2}"))
    s.append(txt(32, yt + 22, "天之道", 10.5, GREEN))
    s.append(txt(212, yt + 22, "人之道", 10.5, SEAL))
    s.append(txt(32, yt + 46, "损有余", 9.5, INK))
    s.append(txt(32, yt + 62, "补不足", 9.5, INK))
    s.append(txt(32, yt + 82, "往下按一半，往上抬到底", 9, "#6E6459"))
    s.append(txt(212, yt + 46, "损不足", 9.5, INK))
    s.append(txt(212, yt + 62, "奉有余", 9.5, INK))
    s.append(txt(212, yt + 82, "越缺越拿，越有越给", 9, "#6E6459"))
    s.append(txt(190, yt + 128, "孰能有余以奉天下？唯有道者。", 11, INK, "middle"))
    s.append(txt(190, yt + 148, "上弦的人不使力，使的是眼。", 10, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第八十一章 · 不积 ============
def ch81_bu_ji():
    W, H = 380, 690
    body, y = head(W, H, "九个不：全书收口的方式是划掉", "第 八 十 一 章 · 收 口", "九个不",
                   "他不肯说「这就是道」，只说：不是这个，不是这个。", H)
    s = [body]
    words = ["不美", "不信", "不辩", "不善", "不博", "不知", "不积", "不害", "不争"]
    yb = y + 4
    for i, w in enumerate(words):
        col, row = i % 3, i // 3
        x = 20 + col * 116
        yy = yb + row * 40
        s.append(box(x, yy, 100, 32, fill="#FBF6EC", stroke="{LINE2}"))
        s.append(txt(x + 50, yy + 22, w, 11.5, INK, "middle"))
        s.append(f'<line x1="{x+18}" y1="{yy+8}" x2="{x+82}" y2="{yy+24}" stroke="{SEAL}" stroke-width="0.8" opacity="0.6"/>')
    # 泉与仓
    yc = yb + 3 * 40 + 14
    s.append(box(20, yc, 160, 92, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(box(200, yc, 160, 92, fill="#FBF6EC", stroke="{LINE2}"))
    s.append(txt(32, yc + 22, "仓", 12, "#8A7C69"))
    s.append(txt(32, yc + 44, "积则满，满则溢，溢则空", 9.5, "#6E6459"))
    s.append(txt(32, yc + 62, "守住会空", 9.5, SEAL))
    s.append(txt(212, yc + 22, "泉", 12, GREEN))
    s.append(txt(212, yc + 44, "既以为人，己愈有", 9.5, "#6E6459"))
    s.append(txt(212, yc + 62, "给出不会少", 9.5, GREEN))
    # 收
    yend = yc + 108
    s.append(box(20, yend, 340, 50, fill="#E9DFCC", stroke="#C9B79A"))
    s.append(txt(190, yend + 22, "天之道，利而不害；圣人之道，为而不争。", 10.5, INK, "middle"))
    s.append(txt(190, yend + 40, "全书第一句划掉一个，最后一句划掉九个。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第四十章 · 三动图（反者道之动 → 生一、二、三） ============
def ch40_san_dong():
    W, H = 380, 640
    body, y = head(W, H, "反者道之动：一个动作，连翻三回", "第 四 十 章 · 生 发 动 力", "一次动，三次翻",
                   "不是三台机器，是同一个「反」翻了三回。", H)
    s = [body]
    rows = [
        ("动 ①", "道生一", "收成一团，还没分面", "一 · 太极", "圆而未判"),
        ("动 ②", "一生二", "一翻成两，同一道口两侧", "二 · 阴阳", "有与无、形与气"),
        ("动 ③", "二生三", "两面对立，中缝被撑开", "三 · 虚位", "缝不是东西，是撑出来的位"),
    ]
    ys, rowh = y + 4, 148
    cx, r = 262, 30
    for i, (tag, act, note, label, sub) in enumerate(rows):
        yy = ys + i * rowh
        s.append(txt(20, yy + 12, tag, 9.5, "#8A7C69"))
        # 反：环
        ax, ay = 48, yy + 50
        s.append(f'<circle cx="{ax}" cy="{ay}" r="20" fill="none" stroke="{LINE2}" stroke-width="0.8"/>')
        s.append(f'<path d="M {ax} {ay-20} A 20 20 0 0 1 {ax} {ay+20}" fill="none" stroke="{SEAL}" stroke-width="1.2" marker-end="url(#arrS)"/>')
        s.append(f'<path d="M {ax} {ay+20} A 20 20 0 0 1 {ax} {ay-20}" fill="none" stroke="{GREEN}" stroke-width="1.2" marker-end="url(#arr2)"/>')
        s.append(txt(ax, ay + 4, "反", 11.5, INK, "middle"))
        s.append(txt(ax, yy + 96, act, 10, SEAL, "middle"))
        s.append(txt(88, yy + 30, note, 9, "#6E6459"))
        # 右：结果
        cy = yy + 50
        if i == 0:
            s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FBF6EC" stroke="{INK}" stroke-width="1.2"/>')
            s.append(txt(cx, cy + 5, "一", 12.5, INK, "middle"))
        elif i == 1:
            s.append(f'<path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy} Z" fill="#E4EBE7" stroke="{GREEN}" stroke-width="1"/>')
            s.append(f'<path d="M {cx+r} {cy} A {r} {r} 0 0 1 {cx-r} {cy} Z" fill="#F0E1D9" stroke="{SEAL}" stroke-width="1"/>')
            s.append(txt(cx, cy - 12, "阴", 10, GREEN, "middle"))
            s.append(txt(cx, cy + 22, "阳", 10, SEAL, "middle"))
        else:
            gap = 11
            s.append(f'<path d="M {cx-r} {cy-gap} A {r} {r} 0 0 1 {cx+r} {cy-gap}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
            s.append(f'<path d="M {cx-r} {cy+gap} A {r} {r} 0 0 0 {cx+r} {cy+gap}" fill="none" stroke="{SEAL}" stroke-width="2"/>')
            s.append(f'<line x1="{cx+r+3}" y1="{cy}" x2="{cx+r+12}" y2="{cy}" stroke="#B9A88E" stroke-width="0.8"/>')
            s.append(txt(cx + r + 20, cy + 4, "三", 10.5, "#8A7C69"))
        s.append(txt(cx, yy + (106 if i == 2 else 100), label, 10, INK, "middle"))
        s.append(txt(cx, yy + (124 if i == 2 else 118), sub, 8.8, "#8A7C69", "middle"))
    yb = ys + 3 * rowh + 2
    s.append(box(20, yb, 340, 52, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yb + 22, "三生万物：靠的不是力气，是那道缝没被填实。", 10.5, INK, "middle"))
    s.append(txt(190, yb + 42, "反不是往回退，是翻到另一面；翻一次，显一层。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三章 · 不造标 ============
def ch03_bu_zao_biao():
    W, H = 380, 484
    body, y = head(W, H, "三个「不」，一个动作：不主动造标", "第 三 章 · 治 世", "不造标",
                   "标尺不起，争、盗、乱便无处生根——不是不许人，是不先把尺子立起来。", H)
    s = [body]
    rows = [("不尚贤", "不争", "不把人的长处摆成徽章"),
            ("不贵难得之货", "不为盗", "不把稀罕东西标成高价"),
            ("不见可欲", "心不乱", "不把勾人的东西摆在眼前")]
    yb = y + 6
    for i, (a, b, note) in enumerate(rows):
        yy = yb + i * 36
        s.append(txt(20, yy + 16, a, 10.5, SEAL))
        s.append(f'<line x1="112" y1="{yy+11}" x2="136" y2="{yy+11}" stroke="{LINE}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(txt(142, yy + 16, b, 10.5, INK))
        s.append(txt(184, yy + 16, note, 9, "#6E6459"))
    # 器剖面：壁与空
    yy = yb + 3 * 36 + 26
    s.append(txt(20, yy, "后半章转治身：壁与空，同一只器", 9.5, "#8A7C69"))
    top, bot = yy + 26, yy + 108
    s.append(f'<rect x="30" y="{top}" width="14" height="{bot-top}" fill="{INK}" opacity="0.55"/>')
    s.append(f'<rect x="130" y="{top}" width="14" height="{bot-top}" fill="{INK}" opacity="0.55"/>')
    s.append(f'<line x1="44" y1="{bot}" x2="130" y2="{bot}" stroke="{INK}" stroke-width="1" opacity="0.55"/>')
    s.append(txt(87, (top + bot) / 2 + 4, "空", 12, "#8A7C69", "middle"))
    s.append(txt(150, top + 8, "壁", 9, SEAL))
    s.append(txt(166, top + 20, "壁：实其腹 · 强其骨", 9, SEAL))
    s.append(txt(166, top + 38, "厚其壁，是让它立得住", 9, "#6E6459"))
    s.append(txt(166, top + 56, "守其空，是让它容得下", 9, "#6E6459"))
    s.append(txt(166, top + 76, "虚心弱志＝守其空，不是抽空人", 8.8, GREEN))
    # 收
    yc = yy + 130
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 27, "为无为，则无不治", 12, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 70, "最易读错处：把「不造标」读成「不许人」，或读成禁欲。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四章 · 道冲不盈 ============
def ch04_dao_chong():
    W, H = 380, 496
    body, y = head(W, H, "道冲：一个永远装不满的空", "第 四 章 · 本 体", "装不满的空",
                   "上半说它是什么，下半说你怎么办；中间贯通的那句，是「有生于无」。", H)
    s = [body]
    # 器
    cx, top, bot, half = 110, y + 22, y + 132, 62
    s.append(f'<path d="M {cx-half} {top} L {cx-half} {bot-24} Q {cx} {bot+16} {cx+half} {bot-24} L {cx+half} {top}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{cx-half-8}" y1="{top}" x2="{cx+half+8}" y2="{top}" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="{cx-24}" y1="{top+18+i*22}" x2="{cx+24}" y2="{top+18+i*22}" stroke="{LINE2}" stroke-width="0.7" stroke-dasharray="2 3"/>')
    s.append(txt(cx, top - 10, "冲 · 虚", 9.5, "#8A7C69", "middle"))
    s.append(txt(cx + half + 20, top + 26, "用之或不盈", 10, GREEN))
    s.append(txt(cx + half + 20, top + 42, "倒多少进去，它都不满", 8.8, "#6E6459"))
    s.append(txt(cx + half + 20, top + 64, "渊兮，似万物之宗", 9.5, SEAL))
    # 四修
    ys = y + 176
    s.append(txt(20, ys, "落到人身上：四句实修", 9.5, "#8A7C69"))
    quads = [("挫其锐", "磨去锋芒", "先减，不是先增"),
             ("解其纷", "理清纠缠", "把结打开，不加新结"),
             ("和其光", "收敛光耀", "亮而不刺人"),
             ("同其尘", "落回尘土", "与粗处同处")]
    for i, (a, b, c) in enumerate(quads):
        col, row = i % 2, i // 2
        x = 20 + col * 174
        yy = ys + 14 + row * 46
        s.append(txt(x, yy + 16, a, 10.5, SEAL))
        s.append(txt(x + 54, yy + 16, b, 9.5, "#6E6459"))
        s.append(txt(x, yy + 32, c, 8.8, "#8A7C69"))
    # 收
    yc = ys + 112
    s.append(box(20, yc, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 20, "湛兮，似或存；吾不知谁之子，象帝之先。", 10, INK, "middle"))
    s.append(txt(190, yc + 38, "它先于一切被命名者——连「谁生的」都问不到它头上。", 9, "#6E6459", "middle"))
    s.append(txt(190, yc + 66, "四句不是四种修养，是把加在身上的东西一件件卸下来。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五章 · 橐籥：中是枢 ============
def ch05_tuo_yue():
    W, H = 380, 524
    body, y = head(W, H, "橐籥：中不是点，是枢", "第 五 章 · 用 之", "中不是点，是枢",
                   "读成点，就成了折中、和稀泥；读成枢，才知道它一直在动。", H)
    s = [body]
    # 风箱
    x1, x2, ty, by = 40, 240, y + 30, y + 132
    s.append(box(x1, ty, x2 - x1, by - ty, fill="#FBF6EC", stroke="{INK}", width=1.2))
    s.append(f'<rect x="{x1+56}" y="{ty+8}" width="12" height="{by-ty-16}" fill="{INK}" opacity="0.5"/>')
    s.append(f'<line x1="{x1+62}" y1="{ty+4}" x2="{x1+62}" y2="{ty-16}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M {x1+50} {ty-24} h24" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{x1+96}" y1="{by-30}" x2="{x1+156}" y2="{by-30}" stroke="{GREEN}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    s.append(f'<line x1="{x1+156}" y1="{by-18}" x2="{x1+96}" y2="{by-18}" stroke="{GREEN}" stroke-width="1.2" marker-end="url(#arrL)"/>')
    s.append(txt(x1 + 96, by + 8, "往复：不是停在中，是穿过中", 8.8, GREEN))
    s.append(txt(x1 + 12, ty - 26, "两端闭合与拉开", 8.8, "#8A7C69"))
    s.append(box(x2 + 6, ty + 30, 96, 26, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(txt(x2 + 54, ty + 47, "出风", 9.5, SEAL, "middle"))
    s.append(arrow(x2, ty + 43, x2 + 4, ty + 43, "#C9B79A", 0.8))
    # 三词链
    ys = y + 168
    chain = [("不仁", "自持：顺自性运行，不添私情"),
             ("橐籥", "开合：生机在中间那个支点"),
             ("守中", "守枢：守住那个一直在动的位置")]
    for i, (a, b) in enumerate(chain):
        yy = ys + i * 46
        s.append(box(20, yy, 62, 30, fill="#FBF6EC", stroke="{LINE2}"))
        s.append(txt(51, yy + 20, a, 11, SEAL, "middle"))
        s.append(txt(92, yy + 20, b, 9.5, "#6E6459"))
        if i < 2:
            s.append(vline(51, yy + 30, yy + 44, "#C9B79A"))
    yc = ys + 3 * 46 + 6
    s.append(box(20, yc, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 26, "多言数穷，不如守中", 11, INK, "middle"))
    s.append(txt(190, yc + 58, "「中」不是 0 与 1 之间的 0.5，是天平求不到的静止。", 9.5, "#6E6459", "middle"))
    s.append(txt(190, yc + 74, "它是那台机器里，一直在来回穿过的支点。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六章 · 谷神 ============
def ch06_gu_shen():
    W, H = 380, 484
    body, y = head(W, H, "谷、门、一线：玄牝三级", "第 六 章 · 生 生", "谷神不死",
                   "虚能受，受而能生，生而不竭——三级说的是一件事。", H)
    s = [body]
    # 谷
    yg = y + 16
    s.append(f'<path d="M 40 {yg+56} Q 60 {yg+6} 96 {yg+56}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<path d="M 96 {yg+56} Q 132 {yg+6} 152 {yg+56}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="30" y1="{yg+56}" x2="162" y2="{yg+56}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(96, yg + 40, "谷", 11, GREEN, "middle"))
    s.append(txt(178, yg + 20, "两山之间的凹陷", 9, "#6E6459"))
    s.append(txt(178, yg + 36, "虚而能受；不是被填满的坑", 9, "#6E6459"))
    s.append(txt(178, yg + 54, "谷神不死", 9.5, SEAL))
    # 门
    yd = yg + 92
    s.append(txt(20, yd, "玄牝之门：它从哪里出入", 9, "#8A7C69"))
    s.append(f'<line x1="68" y1="{yd+14}" x2="68" y2="{yd+62}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="124" y1="{yd+14}" x2="124" y2="{yd+62}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="56" y1="{yd+14}" x2="136" y2="{yd+14}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="70" y1="{yd+42}" x2="88" y2="{yd+42}" stroke="{GREEN}" stroke-width="1" marker-end="url(#arr2)"/>')
    s.append(f'<line x1="122" y1="{yd+52}" x2="104" y2="{yd+52}" stroke="{GREEN}" stroke-width="1" marker-end="url(#arrL)"/>')
    s.append(txt(158, yd + 30, "天地根：出也从此，入也从此", 9, "#6E6459"))
    s.append(txt(158, yd + 48, "门不装东西，只给一个进出的口", 9, "#6E6459"))
    # 绵绵
    yl = yd + 96
    s.append(txt(20, yl, "绵绵若存，用之不勤", 9, "#8A7C69"))
    s.append(f'<path d="M {40} {yl+34} Q {90} {yl+8} {140} {yl+34} Q {190} {yl+60} {240} {yl+34} Q {290} {yl+8} {340} {yl+34}" fill="none" stroke="{SEAL}" stroke-width="1.1" opacity="0.8"/>')
    s.append(txt(190, yl + 62, "细得几乎看不见，却一直没断", 9, "#6E6459", "middle"))
    # 收
    yc = yl + 82
    s.append(box(20, yc, 340, 62, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(32, yc + 22, "「神」不是人格神：是「申」，闪电屈曲之象，虚中不测的势能。", 9, INK))
    s.append(txt(32, yc + 40, "「玄牝」不是性别：是牡牝往复的整套本能，不归男女。", 9, INK))
    s.append(txt(32, yc + 58, "读成神灵，多一个主宰；读成肉身，少一半天地。", 9, SEAL))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第七章 · 不自生 ============
def ch07_bu_zi_sheng():
    W, H = 380, 402
    body, y = head(W, H, "不自生，故能长生", "第 七 章 · 立 身", "不自生",
                   "无私之后，那个「私」是被成全的，不是被交换的。", H)
    s = [body]
    s.append(txt(20, y + 8, "同一笔账，两处记法", 9.5, "#8A7C69"))
    cols = [("天地", [("不自生", "长生")]), ("圣人", [("后其身", "身先"), ("外其身", "身存")])]
    yb = y + 20
    s.append(txt(60, yb, "天地", 10, GREEN, "middle"))
    s.append(txt(214, yb, "圣人", 10, SEAL, "middle"))
    rows = [("不自生", "长生"), ("后其身", "身先"), ("外其身", "身存")]
    for i, (a, b) in enumerate(rows):
        yy = yb + 20 + i * 44
        s.append(txt(20, yy + 16, a, 10, INK))
        s.append(f'<line x1="62" y1="{yy+11}" x2="86" y2="{yy+11}" stroke="{LINE}" stroke-width="1"/>')
        s.append(txt(92, yy + 16, b, 10, GREEN))
        if i > 0:
            s.append(txt(190, yy + 16, a, 10, INK))
            s.append(f'<line x1="234" y1="{yy+11}" x2="258" y2="{yy+11}" stroke="{LINE}" stroke-width="1"/>')
            s.append(txt(264, yy + 16, b, 10, SEAL))
        else:
            s.append(txt(190, yy + 16, "（天地只此一笔）", 8.5, "#8A7C69"))
    # 警
    yw = yb + 20 + 3 * 44 + 8
    s.append(box(20, yw, 340, 50, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(32, yw + 22, "若先退一步，等着赚回来——那是权谋，不是老子。", 9.5, SEAL))
    s.append(txt(32, yw + 40, "把无私当手段、把成私当回报，这一章的读法就整个翻过去了。", 9, "#6E6459"))
    yc = yw + 66
    s.append(txt(190, yc, "非以其无私邪？故能成其私。", 11.5, INK, "middle"))
    s.append(txt(190, yc + 20, "成，是顺带的；不是先讲价、再让利。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第八章 · 上善若水 ============
def ch08_shang_shan():
    W, H = 380, 478
    body, y = head(W, H, "上善若水：几于道，不等于道", "第 八 章 · 取 象", "上善若水",
                   "「若」是像，不是是；「善」是取向，不是标签。", H)
    s = [body]
    # 水
    yw = y + 10
    s.append(f'<path d="M 30 {yw+10} Q 90 {yw+40} 150 {yw+30} Q 210 {yw+20} 260 {yw+56} Q 290 {yw+76} 340 {yw+70}" fill="none" stroke="{INK}" stroke-width="1.2" opacity="0.75"/>')
    s.append(f'<ellipse cx="150" cy="{yw+42}" rx="14" ry="8" fill="{LINE2}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(150, yw + 44, "石", 8, "#8A7C69", "middle"))
    s.append(txt(300, yw + 30, "处众人之所恶", 9, SEAL))
    s.append(txt(300, yw + 46, "往低处走，不挑地方", 8.5, "#6E6459"))
    # 三理由
    yb = yw + 70
    rs = [("利万物", "先给，不等回报"), ("而不争", "不与所利者争位"), ("故几于道", "是接近，不是等同")]
    for i, (a, b) in enumerate(rs):
        s.append(txt(20, yb + 14 + i * 22, a, 9.5, GREEN))
        s.append(txt(86, yb + 14 + i * 22, b, 9, "#6E6459"))
    # 七善
    ys = yb + 92
    s.append(txt(20, ys, "七善：七处取向，一句话落到一处", 9.5, "#8A7C69"))
    seven = [("居善地", "择下不择高"), ("心善渊", "心似深潭，不浅不躁"), ("与善仁", "给不图还"),
             ("言善信", "话可验"), ("政善治", "事理顺"), ("事善能", "做得到"), ("动善时", "动在时上")]
    for i, (a, b) in enumerate(seven):
        col, row = i % 2, i // 2
        x = 20 + col * 176
        yy = ys + 18 + row * 26
        s.append(txt(x, yy + 16, a, 9.5, INK))
        s.append(txt(x + 44, yy + 16, b, 8.5, "#6E6459"))
    yc = ys + 18 + 4 * 26 + 20
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 26, "夫唯不争，故无尤", 11.5, INK, "middle"))
    s.append(txt(190, yc + 60, "水不与石争路，绕过去，仍到低处。", 9.5, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第九章 · 持而盈之（进与退，同一根尺子） ============
def ch09_ying_man():
    W, H = 380, 648
    body, y = head(W, H, "一根箭头＝一步；退，是唯一不往前的一步", "第 九 章 · 事 成", "持而盈之",
                   "满不是问题；满了还要再加一步，才是问题。", H)
    s = [body]
    rows = [("持", "盈", "已满还要拿住，不如其已"),
            ("揣", "锐", "还要磨尖，不可长保"),
            ("金玉", "满堂", "还要囤着，莫之能守"),
            ("富贵", "骄", "还要显出来，自遗其咎")]
    y0 = y + 8
    s.append(txt(20, y0, "一、四根向前的箭头", 9.2, "#8A7C69"))
    for i, (a, b, note) in enumerate(rows):
        yy = y0 + 22 + i * 38
        s.append(txt(24, yy + 16, a, 12, SEAL, spacing="1"))
        s.append(f'<line x1="70" y1="{yy+11}" x2="104" y2="{yy+11}" stroke="{LINE}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(txt(87, yy + 4, "又进一步", 7.2, "#A89577", "middle"))
        s.append(txt(110, yy + 16, b, 12, INK, spacing="1"))
        s.append(txt(170, yy + 16, note, 8.6, "#6E6459"))
    y1 = y0 + 22 + 4 * 38
    # 二、反向的那一根
    s.append(txt(20, y1 + 6, "二、唯一一根反向的：停手", 9.2, "#8A7C69"))
    ya = y1 + 20
    s.append(box(20, ya, 72, 26, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(56, ya + 18, "身退", 10.5, SEAL, "middle", spacing="1"))
    s.append(f'<line x1="258" y1="{ya+13}" x2="102" y2="{ya+13}" stroke="{SEAL}" stroke-width="1" marker-end="url(#arrS)"/>')
    s.append(txt(266, ya + 17, "退：不往前，只停", 8.6, SEAL))
    # 三、身／功 对轴（子虔）
    yb = ya + 42
    s.append(txt(20, yb, "三、同一件事的两头：功与身", 9.2, "#8A7C69"))
    yaxis = yb + 34
    s.append(f'<line x1="52" y1="{yaxis}" x2="328" y2="{yaxis}" stroke="{LINE2}" stroke-width="1"/>')
    s.append(f'<line x1="132" y1="{yaxis-7}" x2="96" y2="{yaxis-7}" stroke="{SEAL}" stroke-width="1" marker-end="url(#arrS)"/>')
    s.append(f'<line x1="248" y1="{yaxis+7}" x2="286" y2="{yaxis+7}" stroke="{GREEN}" stroke-width="1" marker-end="url(#arr2)"/>')
    s.append(txt(52, yaxis + 4, "身", 11, SEAL, "middle", spacing="1"))
    s.append(txt(328, yaxis + 4, "功", 11, INK, "middle", spacing="1"))
    s.append(txt(96, yaxis - 14, "退：事留在外面", 8.2, "#6E6459"))
    s.append(txt(292, yaxis + 24, "进：事越做越大", 8.2, "#6E6459"))
    s.append(txt(20, yaxis + 34, "功可以越做越大，身只有一副；两头一起用，才有得退。", 8.6, "#8A7C69"))
    # 四、阴阳＝度（正版太极：两半合成）
    yc = yaxis + 56
    s.append(txt(20, yc, "四、度：两半互含，不是折中", 9.2, "#8A7C69"))
    R, cx, cyy = 48, 190, yc + 58
    D = "#7B766E"
    s.append(f'<circle cx="{cx}" cy="{cyy}" r="{R}" fill="{D}"/>')
    s.append(f'<path d="M {cx},{cyy-R} A {R},{R} 0 0 1 {cx},{cyy+R} L {cx},{cyy-R} Z" fill="{PAPER}"/>')
    s.append(f'<circle cx="{cx}" cy="{cyy-R/2}" r="{R/2}" fill="{D}"/>')
    s.append(f'<circle cx="{cx}" cy="{cyy+R/2}" r="{R/2}" fill="{PAPER}"/>')
    s.append(f'<circle cx="{cx}" cy="{cyy}" r="{R}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{cx}" cy="{cyy-R/2}" r="7" fill="{PAPER}"/>')
    s.append(f'<circle cx="{cx}" cy="{cyy+R/2}" r="7" fill="{D}"/>')
    s.append(txt(cx - 25, cyy + 4, "进", 11, PAPER, "middle", spacing="1"))
    s.append(txt(cx + 27, cyy + 10, "退", 11, D, "middle", spacing="1"))
    s.append(txt(20, cyy - 16, "进：黑那半，", 8.5, "#6E6459"))
    s.append(txt(20, cyy, "一直在加", 8.5, "#6E6459"))
    s.append(txt(20, cyy + 22, "加到端就溢", 8.2, "#8A7C69"))
    s.append(txt(300, cyy - 16, "退：白那半，", 8.5, "#6E6459", "end"))
    s.append(txt(300, cyy, "知道停在哪格", 8.5, "#6E6459", "end"))
    s.append(txt(300, cyy + 22, "两点即两半所含", 8.2, "#8A7C69", "end"))
    s.append(txt(cx, cyy + R + 24, "能退，进才立得住；只会进，那点退就被挤没了。", 8.4, "#8A7C69", "middle"))
    # 收
    yf = cyy + R + 40
    s.append(box(20, yf, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yf + 19, "功遂身退，天之道。", 11.5, INK, "middle", spacing="1"))
    s.append(txt(190, yf + 35, "退的是那只还要加一步的手，不是事。", 8.6, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三章 · 尚即过度（壁与空） ============
def ch03_shang_ji_guo_du():
    W, H = 380, 636
    body, y = head(W, H, "「尚」是把自然的分寸，抬成表态", "第 三 章 · 治 世", "尚即过度",
                   "壁在，空才用得起；壁胀了，空就用不上。", H)
    s = [body]
    rows = [("不尚贤", "使民不争", "把长处摆成徽章"),
            ("不贵难得之货", "使民不为盗", "把稀罕标成高价"),
            ("不见可欲", "使民心不乱", "把勾人的摆到眼前")]
    yb = y + 2
    for i, (a, b, note) in enumerate(rows):
        yy = yb + i * 24
        s.append(txt(20, yy + 14, a, 9.5, SEAL))
        s.append(f'<line x1="112" y1="{yy+9}" x2="132" y2="{yy+9}" stroke="{LINE}" stroke-width="1" marker-end="url(#arr)"/>')
        s.append(txt(138, yy + 14, b, 9.5, INK))
        s.append(txt(206, yy + 14, note, 8.5, "#6E6459"))
    s.append(txt(20, yb + 3 * 24 + 6, "三个动作是同一件：不主动抬它，标尺就不起来。", 9, "#8A7C69"))
    # 经文四句 ↔ 壁／空
    ys = yb + 3 * 24 + 30
    s.append(txt(20, ys, "经文四句，恰好分成壁与空", 9.5, "#8A7C69"))
    top, bot = ys + 30, ys + 104
    s.append(f'<rect x="36" y="{top}" width="13" height="{bot-top}" fill="{INK}" opacity="0.62"/>')
    s.append(f'<rect x="132" y="{top}" width="13" height="{bot-top}" fill="{INK}" opacity="0.62"/>')
    s.append(f'<line x1="49" y1="{bot}" x2="132" y2="{bot}" stroke="{INK}" stroke-width="1" opacity="0.5"/>')
    s.append(txt(90, (top + bot) / 2 + 4, "空", 12, "#8A7C69", "middle"))
    s.append(txt(26, top - 6, "壁", 9, SEAL))
    s.append(txt(162, top + 2, "实其腹 · 强其骨 → 壁", 9.5, SEAL))
    s.append(txt(162, top + 18, "厚其壁，是让它立得住", 8.5, "#6E6459"))
    s.append(txt(162, top + 48, "虚其心 · 弱其志 → 空", 9.5, GREEN))
    s.append(txt(162, top + 64, "守其空，是让空用得起", 8.5, "#6E6459"))
    # 同一段壁，三种质地
    yz = ys + 128
    s.append(txt(20, yz, "同一段壁的三种质地：变的是壁，空一直是空", 9.2, "#8A7C69"))
    cy = yz + 62
    R = 44
    thin = 7
    r1 = R - thin / 2
    s.append(f'<circle cx="72" cy="{cy}" r="{r1}" fill="none" stroke="{INK}" stroke-width="{thin}" opacity="0.34"/>')
    s.append(txt(72, cy + 4, "空", 9.5, "#8A7C69", "middle"))
    s.append(txt(72, cy + R + 16, "薄壁", 10, SEAL, "middle"))
    s.append(txt(72, cy + R + 32, "不及：立不住", 8.4, "#6E6459", "middle"))
    s.append(txt(72, cy + R + 46, "空虽在，器不成", 8.2, "#6E6459", "middle"))
    # 实其腹：深灰、适中
    thick = 17
    r2 = R - thick / 2
    s.append(f'<circle cx="190" cy="{cy}" r="{r2}" fill="none" stroke="{INK}" stroke-width="{thick}" opacity="0.66"/>')
    s.append(txt(190, cy + 4, "空", 9.5, "#8A7C69", "middle"))
    s.append(txt(190, cy + R + 16, "实其腹", 10, SEAL, "middle"))
    s.append(txt(190, cy + R + 32, "分寸：壁致密而空存", 8.4, "#6E6459", "middle"))
    s.append(txt(190, cy + R + 46, "利与用俱", 8.2, "#6E6459", "middle"))
    # 海绵壁：更深、更厚、带孔，腔被挤小
    thick2 = 26
    r3 = R - thick2 / 2
    s.append(f'<circle cx="308" cy="{cy}" r="{r3}" fill="none" stroke="{INK}" stroke-width="{thick2}" opacity="0.72"/>')
    pores = []
    for gx in range(-R, R + 1, 6):
        for gy in range(-R, R + 1, 6):
            rr = gx * gx + gy * gy
            ri = (R - thick2 + 4) ** 2
            if ri < rr < (R - 5) ** 2:
                pores.append(f'<circle cx="{308+gx}" cy="{cy+gy}" r="2.2" fill="{PAPER}" opacity="0.85"/>')
    s.append("".join(pores))
    s.append(txt(308, cy + 4, "空", 9, "#8A7C69", "middle"))
    s.append(txt(308, cy + R + 16, "海绵壁", 10, SEAL, "middle"))
    s.append(txt(308, cy + R + 32, "过度：壁胀、变厚", 8.4, "#6E6459", "middle"))
    s.append(txt(308, cy + R + 46, "腔被挤小，空吸进孔里", 7.9, "#6E6459", "middle"))
    # 辨义
    yr = cy + R + 62
    s.append(box(20, yr, 340, 60, fill="#F6EFE0", stroke="#C9B79A", dash="4 3"))
    s.append(txt(32, yr + 17, "「虚」不是实的反面：是有的那部分自己松成海绵", 8.8, SEAL))
    s.append(txt(32, yr + 33, "虚其心：在空上做减法，留白，空还照用。", 8.6, "#6E6459"))
    s.append(txt(32, yr + 49, "虚其腹：在壁上被动的松，料变多孔、变胀，空反被吃掉。", 8.6, "#6E6459"))
    # 收
    yc = yr + 74
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "有之以为利，无之以为用。", 11.5, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 34, "过与不及，皆失其用。", 8.8, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


def ch10_bao_yi():
    W, H = 380, 592
    body, y = head(W, H, "六问一答：对内做主人，对外做租客", "第 十 章 · 勘 验", "载营魄抱一",
                   "六问各管一件，底子只有一句质问：你是不是在当主人？", H)
    s = [body]
    qs = [("载营魄抱一", "能无离乎", "身心一处，不各走各的"),
          ("专气致柔", "能婴儿乎", "气顺到软，不绷着"),
          ("涤除玄览", "能无疵乎", "擦净那面镜子，不留斑"),
          ("爱民治国", "能无为乎", "事办了，人不被搅"),
          ("天门开阖", "能为雌乎", "开合之际，肯受不肯抢"),
          ("明白四达", "能无知乎", "都懂了，不拿懂去压人")]
    yb = y + 4
    for i, (a, b, note) in enumerate(qs):
        yy = yb + i * 44
        s.append(txt(20, yy + 16, a, 10, INK))
        s.append(txt(112, yy + 16, b + "？", 9, "#8A7C69"))
        s.append(txt(20, yy + 32, note, 8.8, "#8A7C69"))
    # 两栏
    ya = yb + 6 * 44 + 8
    s.append(box(20, ya, 160, 92, fill="#F6EFE0", stroke="{LINE2}"))
    s.append(box(200, ya, 160, 92, fill="#FBF6EC", stroke="{LINE2}"))
    s.append(txt(32, ya + 22, "对内：主人", 10, SEAL))
    s.append(txt(32, ya + 44, "自心是唯一有全权的地方", 8.8, "#6E6459"))
    s.append(txt(32, ya + 60, "只能自己修，自己守", 8.8, "#6E6459"))
    s.append(txt(212, ya + 22, "对外：租客", 10, GREEN))
    s.append(txt(212, ya + 44, "万物只是暂住，可养可建", 8.8, "#6E6459"))
    s.append(txt(212, ya + 60, "不可占有，不可改写其性", 8.8, "#6E6459"))
    # 收
    yc = ya + 108
    s.append(box(20, yc, 340, 52, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 22, "生而不有，为而不恃，长而不宰，是谓玄德", 9.5, INK, "middle"))
    s.append(txt(190, yc + 42, "勘破了那份主宰欲，德自然现成——不必另修一个德出来。", 9, "#6E6459", "middle"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十二章 · 五色令人目盲 ============
def ch12_wu_se():
    W, H = 380, 472
    body, y = head(W, H, "门不是要封死，是接法要自己管", "第 十 二 章 · 受 体", "门开五处",
                   "受于身，不如治于身：物自己来，怎么接是我。", H)
    s = [body]
    rows = [("五色", "目盲", "看得越花，反而越看不清"),
            ("五音", "耳聋", "声音越满，反而听不进"),
            ("五味", "口爽", "味道越重，口中越失味"),
            ("驰骋畋猎", "心发狂", "追得越欢，心越收不住"),
            ("难得之货", "行妨", "稀罕的东西，先绊住脚")]
    y0 = y + 8
    for i, (a, b, note) in enumerate(rows):
        yy = y0 + i * 32
        s.append(txt(20, yy + 16, a, 9.5, SEAL))
        s.append(arrow(104, yy + 11, 128, yy + 11, color="#C9B79A", head="arr"))
        s.append(txt(134, yy + 16, b, 9.5, INK))
        s.append(txt(184, yy + 16, note, 8.2, "#6E6459"))
    y1 = y0 + 5 * 32 + 4
    s.append(txt(20, y1, "五句不是五条禁令：说的是接收那一头先垮了。", 8.6, "#8A7C69"))
    # 为腹 / 为目
    y2 = y1 + 16
    s.append(box(20, y2, 160, 46, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(100, y2 + 20, "为腹：以物养己", 9.5, GREEN, "middle"))
    s.append(txt(100, y2 + 36, "重心在里头，物来养它", 8.2, "#6E6459", "middle"))
    s.append(box(200, y2, 160, 46, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(280, y2 + 20, "为目：以物役己", 9.5, SEAL, "middle"))
    s.append(txt(280, y2 + 36, "重心在外头，物来役它", 8.2, "#6E6459", "middle"))
    yc = y2 + 62
    s.append(box(20, yc, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "为腹不为目：去彼取此。", 11.5, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 35, "不是不要眼耳，是不把人生的重心交给外面。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch12"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十三章 · 宠辱若惊 ============
def ch13_chong_ru():
    W, H = 380, 442
    body, y = head(W, H, "惊的不是宠辱，是那个钉在壁上的我", "第 十 三 章 · 荣 辱", "惊的是我",
                   "宠辱本身没有力气；力气是把自己交出去那一刻给的。", H)
    s = [body]
    cy = y + 66
    cx = 190
    # 俯视杯：外壁＝我，内腔＝空
    s.append(f'<circle cx="{cx}" cy="{cy}" r="56" fill="#E9DCC4" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="37" fill="{PAPER}" stroke="{LINE}" stroke-width="1"/>')
    s.append(txt(cx, cy + 4, "空", 8.6, "#8A7C69", "middle"))
    s.append(txt(cx, cy - 62, "壁＝我", 8.4, SEAL, "middle"))
    s.append(arrow(56, cy, cx - 62, cy, color="#4A5C55", head="arr2"))
    s.append(arrow(324, cy, cx + 62, cy, color="#A2503B", head="arrS"))
    s.append(txt(58, cy - 24, "得之若惊", 8.2, "#6E6459"))
    s.append(txt(322, cy - 24, "失之若惊", 8.2, "#6E6459", "end"))
    s.append(txt(58, cy + 40, "宠", 13, GREEN, "middle", spacing="1"))
    s.append(txt(322, cy + 40, "辱", 13, SEAL, "middle", spacing="1"))
    s.append(txt(cx, cy + 78, "宠为下：一求它，就把自己放在下位。", 8.6, "#8A7C69", "middle"))
    y2 = cy + 96
    s.append(box(20, y2, 340, 46, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(190, y2 + 19, "吾所以有大患者，为吾有身；及吾无身，吾有何患？", 8.8, INK, "middle"))
    s.append(txt(190, y2 + 35, "无身不是把壁拆了，是不把自己钉在壁上。", 8.4, "#6E6459", "middle"))
    yc = y2 + 64
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 20, "贵以身为天下，若可寄天下。", 11, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 36, "先把自己看重，别人才敢把事托给你——不是相反。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch13"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第十四章 · 视之不见 ============
def ch14_yi_xi_wei():
    W, H = 380, 418
    body, y = head(W, H, "把「看得见才算有」降回局部工具", "第 十 四 章 · 道 体", "三样工具探不到",
                   "探不到不等于没有；探得到也不等于全部。", H)
    s = [body]
    rows = [("视之不见", "夷", "眼睛这条线，走到这里就断了"),
            ("听之不闻", "希", "耳朵这条线，走到这里就断了"),
            ("搏之不得", "微", "手这条线，走到这里就断了")]
    y0 = y + 8
    for i, (a, name, note) in enumerate(rows):
        yy = y0 + i * 34
        s.append(txt(20, yy + 15, a, 9.5, SEAL))
        s.append(txt(102, yy + 15, name, 10, GREEN))
        s.append(f'<line x1="122" y1="{yy+11}" x2="200" y2="{yy+11}" stroke="{LINE}" stroke-width="1"/>')
        s.append(txt(206, yy + 15, note, 8.2, "#6E6459"))
    y1 = y0 + 3 * 34 + 6
    s.append(arrow(190, y1 + 4, 190, y1 + 14, color="#A2503B", head="arrS"))
    y2 = y1 + 6
    s.append(box(60, y2, 260, 40, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(190, y2 + 17, "此三者不可致诘，故混而为一", 9.8, INK, "middle"))
    s.append(txt(190, y2 + 33, "三条线都断，断处却指着同一个东西。", 8.4, "#6E6459", "middle"))
    y3 = y2 + 58
    s.append(txt(20, y3, "惚恍：其上不皦，其下不昧；迎之不见其首，随之不见其后。", 8.6, "#8A7C69"))
    yc = y3 + 12
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "执古之道，以御今之有。", 10.5, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 35, "能知古始，是谓道纪：不是复古，是拿源流来看眼前。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch14"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十五章 · 古之善为道者 ============
def ch15_shan_wei_dao():
    W, H = 380, 460
    body, y = head(W, H, "七喻不是七种美德，是七种「不」", "第 十 五 章 · 体 道", "七个比喻",
                   "微妙玄通，深不可识：认不出，是因为他不把自己摆出来。", H)
    s = [body]
    items = [("豫", "冬涉川", "不敢抢先"),
             ("犹", "畏四邻", "不敢自专"),
             ("俨", "其若客", "不敢当主"),
             ("涣", "若凌释", "不结死冰"),
             ("敦", "其若朴", "不带修饰"),
             ("旷", "其若谷", "不填满自己"),
             ("混", "其若浊", "不装作清")]
    y0 = y + 6
    for i, (a, b, note) in enumerate(items):
        col = i % 2
        row = i // 2
        xx = 20 + col * 176
        yy = y0 + row * 34
        s.append(txt(xx, yy + 16, a, 11, SEAL, spacing="1"))
        s.append(txt(xx + 22, yy + 16, b, 9, INK))
        s.append(txt(xx + 96, yy + 16, note, 8, "#6E6459"))
    y1 = y0 + 4 * 34 + 6
    s.append(txt(20, y1, "七字一个字都不褒：说的都是「不肯往前站一步」。", 8.6, "#8A7C69"))
    y2 = y1 + 18
    s.append(box(20, y2, 340, 52, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(32, y2 + 18, "孰能浊以静之徐清？", 9.2, SEAL))
    s.append(txt(200, y2 + 18, "不是澄清，是让它自己沉下来。", 8.4, "#6E6459"))
    s.append(txt(32, y2 + 36, "孰能安以动之徐生？", 9.2, GREEN))
    s.append(txt(200, y2 + 36, "不是不动，是动得慢，才生得出来。", 8.4, "#6E6459"))
    yc = y2 + 70
    s.append(box(20, yc, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "不欲盈：夫唯不盈，故能蔽而新成。", 10.5, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 35, "不装满，旧样子才换得成新样子。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch15"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十六章 · 致虚极，守静笃 ============
def ch16_zhi_xu_ji():
    W, H = 380, 478
    body, y = head(W, H, "观不是往外看，是看它回到哪里", "第 十 六 章 · 修 法", "归根",
                   "万物并作，吾以观复：动的看一头，复的看另一头。", H)
    s = [body]
    left = y + 8
    nodes = ["万物并作", "芸芸", "归根", "静"]
    for i, t in enumerate(nodes):
        yy = left + i * 30
        s.append(box(20, yy, 108, 24, fill="#F6EFE0", stroke="#C9B79A"))
        s.append(txt(74, yy + 17, t, 9, INK, "middle"))
        if i:
            s.append(arrow(74, yy - 6, 74, yy - 1, color="#C9B79A", head="arr"))
    s.append(txt(20, left + 4 * 30 + 14, "这条线往下：动到最后，都要回到根。", 8.4, "#8A7C69"))
    right = left + 8
    nodes2 = ["复命", "常", "明"]
    for i, t in enumerate(nodes2):
        yy = right + i * 30
        s.append(box(252, yy, 108, 24, fill="#F6EFE0", stroke="#C9B79A"))
        s.append(txt(306, yy + 17, t, 9, INK, "middle"))
        if i:
            s.append(arrow(306, yy - 6, 306, yy - 1, color="#4A5C55", head="arr2"))
    s.append(txt(252, right + 3 * 30 + 14, "往上：回到根，才叫常与明。", 8.4, "#8A7C69"))
    s.append(arrow(132, left + 3 * 30 + 12, 230, left + 3 * 30 + 12, color="#A2503B", head="arrS"))
    s.append(arrow(236, left + 3 * 30 + 8, 236, right + 0 * 30 + 30, color="#A2503B", head="arrS"))
    # 果链
    y2 = left + 4 * 30 + 30
    s.append(txt(20, y2, "知常而后：一条顺下来的链", 9.2, "#8A7C69"))
    chain = ["知常", "容", "公", "全", "天", "道", "久"]
    y3 = y2 + 30
    for i, t in enumerate(chain):
        xx = 24 + i * 48
        s.append(box(xx, y3, 40, 24, fill="#F2EADA", stroke="#C9B79A"))
        s.append(txt(xx + 20, y3 + 16, t, 8.6, INK, "middle"))
        if i:
            s.append(arrow(xx - 8, y3 + 12, xx - 1, y3 + 12, color="#6E6459", head="arr"))
    s.append(txt(20, y3 + 44, "不知常，妄作凶：这一条反过来，是从根部一断到底。", 8.4, SEAL))
    yc = y3 + 62
    s.append(box(20, yc, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "致虚极，守静笃。", 11.5, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 35, "虚到极、静到笃，才看得见「复」这件事。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch16"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第十七章 · 太上，下知有之 ============
def ch17_tai_shang():
    W, H = 380, 432
    body, y = head(W, H, "四级不是四种人，是同一件事的四次退化", "第 十 七 章 · 治 道", "四级台阶",
                   "从上往下：不必被感念 → 要被感念 → 只能被怕 → 连怕也不怕。", H)
    s = [body]
    rows = [("太上", "下知有之", "只知有他，不必感念"),
            ("其次", "亲而誉之", "要被感念了"),
            ("其次", "畏之", "只能被怕了"),
            ("其次", "侮之", "连怕也不怕了")]
    y0 = y + 12
    for i, (lv, t, note) in enumerate(rows):
        yy = y0 + i * 40
        s.append(txt(20, yy + 22, lv, 9, "#8A7C69"))
        s.append(box(66, yy, 108, 30, fill="#F6EFE0" if i else "#F2EADA", stroke="#C9B79A"))
        s.append(txt(120, yy + 20, t, 9.6, INK if i < 2 else "#6E6459", "middle"))
        s.append(txt(188, yy + 20, note, 8.4, "#6E6459"))
        if i:
            s.append(arrow(120, yy - 6, 120, yy - 1, color="#C9B79A", head="arr"))
    y1 = y0 + 4 * 40 + 9
    s.append(txt(20, y1, "信不足焉，有不信焉：不是下面不信，是上面先不足。", 8.6, "#8A7C69"))
    yc = y1 + 16
    s.append(box(20, yc, 340, 48, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 20, "功成事遂，百姓皆谓：我自然。", 10.8, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 37, "最好的治理，是做完之后没人把它记在谁头上。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch17"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十八章 · 大道废，有仁义 ============
def ch18_da_dao_fei():
    W, H = 380, 464
    body, y = head(W, H, "先有缺口，才有那个被举起来的名字", "第 十 八 章 · 世 相", "四对因果",
                   "四句同一个句式：先废，才有一个被标举的名字。", H)
    s = [body]
    rows = [("大道废", "有仁义", "补丁"),
            ("慧智出", "有大伪", "更精致的仿制品"),
            ("六亲不和", "有孝慈", "关系破了，才讲孝慈"),
            ("国家昏乱", "有忠臣", "朝廷乱了，才显忠臣")]
    y0 = y + 8
    for i, (a, b, note) in enumerate(rows):
        yy = y0 + i * 34
        s.append(txt(20, yy + 16, a, 9.6, SEAL))
        s.append(arrow(96, yy + 11, 122, yy + 11, color="#C9B79A", head="arr"))
        s.append(txt(128, yy + 16, b, 9.6, INK))
        s.append(txt(196, yy + 16, note, 8.2, "#6E6459"))
    y1 = y0 + 4 * 34 + 8
    s.append(txt(20, y1, "名字本身不坏；坏在补丁被当成了原因。", 8.6, "#8A7C69"))
    y2 = y1 + 16
    s.append(box(20, y2, 340, 52, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "一个东西要被单独提出、大力宣扬、由衷赞颂，", 8.8, INK, "middle"))
    s.append(txt(190, y2 + 36, "本身就是信号：它原来所在的那处，已经有了缺口。", 8.8, INK, "middle"))
    yc = y2 + 70
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "大道废，有仁义。", 11, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 34, "不是骂仁义：是给仁义记一笔来处。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch18"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第十九章 · 绝圣弃智 ============
def ch19_jue_sheng():
    W, H = 380, 442
    body, y = head(W, H, "不是把好东西扔掉，是把它从被标举的位置上撤下来", "第 十 九 章 · 减 法", "三绝三弃",
                   "上一章是诊断，这一章是方子。", H)
    s = [body]
    rows = [("绝圣弃智", "民利百倍", "不靠聪明立标准，人反而松"),
            ("绝仁弃义", "民复孝慈", "不拿仁义当旗，孝慈自己回来"),
            ("绝巧弃利", "盗贼无有", "不抬巧利，偷的念头没有落处")]
    y0 = y + 8
    for i, (a, b, note) in enumerate(rows):
        yy = y0 + i * 36
        s.append(txt(20, yy + 16, a, 9.6, SEAL))
        s.append(arrow(100, yy + 11, 126, yy + 11, color="#C9B79A", head="arr"))
        s.append(txt(132, yy + 16, b, 9.6, INK))
        s.append(txt(196, yy + 16, note, 8.0, "#6E6459"))
    y1 = y0 + 3 * 36 + 8
    s.append(txt(20, y1, "此三者以为文，不足：撤了三样，还不够。", 8.6, "#8A7C69"))
    y2 = y1 + 16
    s.append(txt(20, y2, "故令有所属——落到三件更实的事上：", 8.8, "#6E6459"))
    y3 = y2 + 14
    items = [("见素", "看见本来的"), ("抱朴", "抱住未加工的"), ("少私寡欲", "少一点自己要")]
    for i, (a, b) in enumerate(items):
        xx = 20 + i * 114
        s.append(box(xx, y3, 106, 44, fill="#F6EFE0", stroke="#C9B79A"))
        s.append(txt(xx + 53, y3 + 19, a, 9.4, GREEN, "middle"))
        s.append(txt(xx + 53, y3 + 34, b, 7.8, "#6E6459", "middle"))
    y4 = y3 + 56
    s.append(txt(20, y4, "绝学无忧：不是不学，是不再拿那套标尺学。", 8.6, "#8A7C69"))
    yc = y4 + 14
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "绝圣弃智，民利百倍。", 10.8, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 34, "撤的是位置，不是东西。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch19"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二十章 · 唯之与阿 ============
def ch20_wei_zhi_yu_e():
    W, H = 380, 508
    body, y = head(W, H, "尺子一换，答案就换", "第 二 十 章 · 独 异", "两把尺子",
                   "唯之与阿、善之与恶，相去几何？", H)
    s = [body]
    y0 = y + 6
    s.append(txt(150, y0 + 14, "众人", 9.6, "#8A7C69", "middle"))
    s.append(txt(290, y0 + 14, "我", 9.6, SEAL, "middle"))
    s.append(f'<line x1="20" y1="{y0+22}" x2="360" y2="{y0+22}" stroke="{LINE}" stroke-width="0.8"/>')
    rows = [("熙熙如享太牢", "泊兮其未兆"),
            ("昭昭", "昏昏"),
            ("察察", "闷闷"),
            ("皆有馀", "独若遗")]
    for i, (a, b) in enumerate(rows):
        yy = y0 + 30 + i * 36
        s.append(txt(150, yy + 16, a, 8.6, INK, "middle"))
        s.append(txt(290, yy + 16, b, 8.6, SEAL, "middle"))
        if i:
            s.append(f'<line x1="20" y1="{yy-4}" x2="360" y2="{yy-4}" stroke="{LINE2}" stroke-width="0.6"/>')
    s.append(f'<line x1="220" y1="{y0+26}" x2="220" y2="{y0+30+4*36-8}" stroke="{LINE2}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    y1 = y0 + 30 + 4 * 36 + 2
    s.append(txt(20, y1, "他如春登台、如婴儿未孩；我儽儽兮若无所归。", 8.2, "#8A7C69"))
    s.append(txt(20, y1 + 14, "不是清高：是把自己那把尺，从别人手里拿回来。", 8.4, "#8A7C69"))
    y2 = y1 + 30
    s.append(box(20, y2, 340, 50, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "人之所畏，不可不畏——但不是每一份畏，都值得接着怕。", 8.6, INK, "middle"))
    s.append(txt(190, y2 + 36, "荒兮其未央哉：这套尺子铺得很远，一直没个尽头。", 8.4, "#6E6459", "middle"))
    yc = y2 + 68
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 20, "贵食母。", 11, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 37, "众人有恃，我独有所养：养的是那个母，不是那套尺。", 8.2, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch20"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二十一章 · 孔德之容 ============
def ch21_kong_de():
    W, H = 380, 548
    body, y = head(W, H, "德不是修出来的，是流出来的", "第 二 十 一 章 · 道 之 为 物", "孔德之容",
                   "道不抓取时是道；被我们抓取时，才成恍兮惚兮。", H)
    s = [body]
    # 道 → 德
    y0 = y + 4
    s.append(box(60, y0, 56, 26, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(88, y0 + 17, "道", 10, INK, "middle", spacing="1"))
    s.append(arrow(120, y0 + 13, 196, y0 + 13, color="#A2503B", head="arrS"))
    s.append(txt(158, y0 + 9, "流", 8.2, SEAL, "middle"))
    s.append(box(200, y0, 120, 26, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(260, y0 + 17, "德：容", 9.6, INK, "middle", spacing="1"))
    s.append(txt(20, y0 + 42, "德不是自己长成一套，是道流过它，它才有样子。", 8.4, "#8A7C69"))
    # 恍惚四层
    y1 = y0 + 56
    s.append(box(20, y1, 340, 28, fill="#F6EFE0", stroke="#C9B79A", dash="4 3"))
    s.append(txt(190, y1 + 18, "惚兮恍兮：不是它模糊，是抓取时只剩一个轮廓", 8.2, "#6E6459", "middle"))
    rows = [("象", "其中有个模糊的样子"),
            ("物", "那样子里，有东西"),
            ("精", "东西里有极细的质"),
            ("信", "这质可验、不骗人")]
    y2 = y1 + 36
    for i, (a, b) in enumerate(rows):
        yy = y2 + i * 30
        s.append(txt(40, yy + 15, a, 12.5, SEAL if i < 2 else GREEN))
        s.append(txt(74, yy + 15, b, 8.6, "#6E6459"))
        if i:
            s.append(arrow(52, yy - 6, 52, yy + 1, color="#C9B79A", head="arr"))
    s.append(f'<line x1="30" y1="{y2-6}" x2="30" y2="{y2+3*30+16}" stroke="{LINE2}" stroke-width="1"/>')
    s.append(txt(20, y2 + 4 * 30 + 8, "越往里越细，但每一层都是真的：不是越玄越空。", 8.4, "#8A7C69"))
    # 路标
    y3 = y2 + 4 * 30 + 28
    s.append(txt(20, y3, "名：一条一直立在那里的路标", 9, "#8A7C69"))
    yy = y3 + 36
    s.append(f'<line x1="30" y1="{yy}" x2="352" y2="{yy}" stroke="{LINE2}" stroke-width="1"/>')
    for i in range(3):
        xx = 70 + i * 110
        s.append(f'<line x1="{xx}" y1="{yy}" x2="{xx}" y2="{yy-14}" stroke="{LINE}" stroke-width="1"/>')
        s.append(box(xx - 16, yy - 27, 32, 13, fill="#F2EADA", stroke="#C9B79A"))
        s.append(txt(xx, yy - 17, "名", 7.6, SEAL, "middle"))
    s.append(txt(30, yy + 18, "路标一直在（其名不去）；但路标不是那个地方。", 8.4, "#6E6459"))
    yc = yy + 34
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "自今及古，其名不去，以阅众甫。", 10, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 33, "往回看不是怀旧：是拿这条不断的名，看清万物怎么起头。", 8.0, "#6E6459", "middle"))
    s.append(gold(yc + 48, "ch21"))
    s.append('</svg>')
    return "\n".join(s)



GOLD = {
    "ch12": ["五色不盲人，逐色者自盲；五音不聋人，溺音者自聋。", "去彼取此，去的是执，取的是定。"],
    "ch13": ["杯壁承一气，珍重莫轻伤；不缚荣辱相，中空纳天光。", "壁不可碎，执壁为我才碎；养身如养器，护壁不据壁。"],
    "ch14": ["视之不见非无，是目不及；听之不闻非寂，是耳不及。", "执古御今，不是驭世，是安己。"],
    "ch15": ["盈则封，封则死；不盈则虚，虚则生。", "浊不须搅，静之自清；根不须催，安之自生。"],
    "ch16": ["万物并作，观其归；归根曰静，静曰复命。", "妄作者凶，顺常者久；没身不殆者，非命长，是险少。"],
    "ch17": ["贵言者，非不言，是不以言夺人之自性。", "功成事遂，百姓曰「我自然」——此谓善治。"],
    "ch18": ["药能已病，药不是身子。", "凡被标举者，皆是缺口的形状。"],
    "ch19": ["所绝者名，所复者实；文不足以为治，令有所属乃安。", "破其外饰，守其本根；破而不立，台面自有人填。"],
    "ch20": ["唯之与阿，相去几何——尺子定的，不是事定的。", "众人贵末，我贵食母；末可争，母不可争。"],
    "ch21": ["孔德之容，惟道是从：德不是修出来的，是流出来的。", "名不去，是路标一直在；路标在，不等于路标就是那个地方。"],
    "ch23": ["自然不是「不管」，是「不需要管」——差别全在有没有人在使劲。", "信不足，不是话说得不够多，是话后面没有人。"],
    "ch24": ["借来的高度站不住，省下的步子走不远。", "不处不是割掉，是不长——约束是按住它，不处是根本不在那儿站。"],
    "ch25": ["不是它比天地老，是天地离了它不成。", "名是给有边界的东西用的；对没有边界的东西，名只是手指。"],
    "ch45b_jing": ["满得溢出来的，是在往外倒；满在里面不溢的，是在往里续。"],
    "ch48a": ["学问把世界切得越来越细，切得越细越好用；可那条「通」，恰恰不在细处。"],
    "ch48b": ["损之又损，以至于无为。"],
    "ch48c": ["「取天下」的「取」是割耳朵，所以老子换了一个动作：不是割，是不动。"],
    "ch47a": ["透过框看，你看见的每一块都是真的；可你真的没看见框外。"],
    "ch47b": ["其出弥远，其知弥少。"],
    "ch56a": ["锐是芒，不是刀；芒不伤人，只扎人；所以要磨，不要砍。"],
    "ch56b": ["纷是套，不是乱；乱能理，套只能解。"],
    "ch56c": ["六把尺都要一个「我」在中间才量得动；中间空了，尺就落不下来。"],
    "ch55a": ["藏是往里放，含是含在嘴边；藏起来的东西会忘，含在嘴里的忘不掉。"],
    "ch55b": ["成年人攥拳是为了抓，婴儿攥拳是为了收；抓是往外，收是往里，一只是同一只手。"],
    "ch55c": ["婴儿哭一天嗓子不坏，不是嗓子好，是他从不憋气；一憋，就有了「存」，有了「伤」。"],
    "ch54a": ["楼是立在地方的，律是立在人心里的；地方会被换，人心不容易。"],
    "ch54b": ["手会松，怀不会；所以抱得住的东西，都是放进怀里的，不是端在手上的。"],
    "ch54c": ["德往外走，先多，再久，再厚，最后匀；匀了才叫普，不是到处都有，是到处一样。"],
    "ch53a": ["「径」是步道：快，是因为窄；窄，是因为只打算一个人过。"],
    "ch53b": ["台阶越高，田越荒，仓越虚；这三句不是三件事，是一件事的三个刻度。"],
    "ch53c": ["留出来的空能装，抽出来的空只剩响；两个都是空，一个是杯，一个是坑。"],
    "ch52a": ["母生子，是天道；子归母，是功夫；本章讲的，就是这后半圈。"],
    "ch52b": ["「兑」是口，「袭」是袍，「救」是止；三个字，一个在收口，一个在穿衣，一个在刹车。"],
    "ch52c": ["光是照东西的，明是那个照本身；光一直在外面，人就一直在外面。"],
    "ch51a": ["道负责「有」，德负责「留住」；一个不占地方，一个专门存。"],
    "ch51b": ["亭是有顶无壁的屋子，宰是屋下当差的人；一个给顶，一个进屋。"],
    "ch51c": ["「不有」是总开关：一划「这是我的」，恃与宰就自己跟上来了。"],
    "ch50a": ["三成是天给的，三成是自己走进去的；后面这个「亦」字，是老子唯一想说的那句。"],
    "ch50b": ["「厚」和「地」是同一个方向：都是往下堆；堆到成层，人就站在自己堆的那块土上。"],
    "ch50c": ["他不是没遇到兕虎，是兕虎找不到那个可以下角的地方。"],
    "ch49a": ["一把尺能定长短，也能把人钉在短的那一格里。"],
    "ch49b": ["「歙」是吸，「注」是灌；一个往里收，一个往外倒。"],
    "ch49c": ["「浑」是水声，不是糊涂；水还在流，只是不再一格一格地流。"],
    "ch47c": ["站在路口的人只能选一条路；知道路怎么走的人，不必选。"],
    "ch46b": ["他不是把刀收了，是把刀改成了犁。"],
    "ch46c": ["先站住，才够；先够，永远不够。",
              "靠外物撑起来的「够」，是借来的；借来的东西，主人随时可以收回。"],
    "ch46a": ["一个国家的秩序好不好，看马站在哪儿就知道；不必看它说什么。",
               "「却」这个字自己写着答案：马是被拉回来的，欲是自己节住的。"],
    "ch45c_gong": ["弓不常张，话不说满，力不使尽。"],
    "ch45c_qin": ["最响的一声，常常是没弹出来的那一下。"],
    "ch45c_dao": ["「正」不是被谁摆正的，是它自己终于站住了。"],
    "ch45c_bi": ["直、巧、辩，三样都在「收」上见高低。",
                 "「正」不是被谁摆正的，是它自己终于站住了。"],
    "ch45c_old": ["动可以赢一场冷，只有静能了断一场热。",
               "「正」不是被谁摆正的，是它自己终于站住了。"],
    "ch45b": ["一刀切过去的直，走不了远路；能缩一下的直，才真的到得了。",
               "巧到要人看出巧，那是手艺；巧到看不出使过劲，那才是本事。"],
    "ch45a": ["真正不破的，是那个本来就有破口的。",
               "封死的器，压力全落在自己身上；留口的器，压力从那个口出去了。"],
    "ch44c": ["知足不是心态好，是站得稳；站得稳的人不抢，不抢的人不容易被踩。",
               "忍是拉住自己，止是把脚放下；一个还在跟自己较劲，一个已经不较了。"],
    "ch44b": ["喜欢是不要钱的，甚爱是要月供的。",
               "藏是一件件往里搬，亡是一件件往外跑；搬得越多，跑得越勤。"],
    "ch44a": ["「亲」是「到得了」——名够不着，身够得着；这一问不必回答，字义已经答了。",
               "失去是丢东西；不停地得，是把自己也搭进去当本钱。"],
    "ch43b": ["撞是把自己的力交出去，跑是把自己的力留着。",
               "它赢的方式，是让「强弱」这场比赛根本不成立。"],
    "ch43a": ["「柔」从木，是能曲能直；「坚」从土，硬成一块。一个还能变，一个已经定了。",
               "柔不是没有力量，是力量还没有被固定成一个方向。"],
    "ch42c": ["三不是第三样东西，是被二撑开的那道空。",
               "分出去，又合回来；不是一条直线，是一条环。"],
    "ch42b": ["纯阴则死，纯阳则散。",
               "壁厚到把中空填实，器还在，用已亡。"],
    "ch41d": ["「晚成」是把终点挪远，「免成」是把终点取消。",
               "不是它没有样子，是任何样子都只是它的一块。"],
    "ch41c": ["下士没有看错，他看的是背面；他只是不知道那件东西还有另一面。",
               "有之以为利，无之以为用。"],
    "ch41b": ["「晚成」是把终点挪远，「免成」是把终点取消。",
               "不是它没有样子，是任何样子都只是它的一块。"],
    "ch41a": ["下士没有看错，他看的是背面；他只是不知道那件东西还有另一面。",
               "不是道难懂，是道难看；难懂可以学，难看只能翻过来看。"],
    "ch40b": ["万物形于有，有自无中生；金钱为器壁，幸福是虚空。",
               "外求终有尽，内守得本源；知反明弱用，静里见真诠。"],
    "ch40a": ["道动常归反，物极必回还。",
               "妙用存柔弱，不竞自安闲。"],
    "ch39b": ["数得清的是零件，数不清的才是那辆车。",
               "玉的体面是别人给的，石的体面是自己有的。"],
    "ch39a": ["「壹」是装满封口的壶；「一」只是一道横，没有盖。",
               "「得一」的对面不是「不得」，是「无以」——不是没得到，是拿不出了。"],
    "ch38": ["失道而后德，失德而后仁，失仁而后义，失义而后礼。",
              "药可治病，药不是饭；礼可维序，礼不是和。"],
    "ch37b": ["压住火的不是更多的柴，是把它从柴上挪开。",
              "静的对立面不是「动」，是「驰」。"],
    "ch37a": ["「为」的原型是一只手牵着象：无为撤掉的不是事，是那只手。",
              "「化」字本带一个「教」；老子加了一个「自」——同一条路，方向反了。"],
    "ch36b": ["不是柔把刚打败了，是刚撑不住自己，柔撑得住。",
              "鱼不是被捉走的，是自己跳上岸的。"],
    "ch36a": ["歙是吸气，张是上弦；一口气吸到底，下一口只能是呼。",
              "兴是众手共举，废是无人再举。"],
    "ch35b": ["客停下来不是归，是歇脚；他没有把这儿当家，只是吃了一口饼。",
              "加味的抓人，无味的养人。道是一碗白水：喝不完，也说不浓。"],
    "ch35a": ["同一个「执」字，宾语一换，手就转向了——执罪人是抓人，执中是持己。",
              "手一伸出去，场就变成了门槛。"],
    "ch34b": ["能小，是因为它从不伸手；不伸手，才没人能握住它。",
              "世人求大，是往大里做；道之大，是往小里做出来的。"],
    "ch34": ["张开手臂，抱住的只有一抱；手臂垂着，怀里是整个天地。",
             "世人的大，是把世界收进来；道的大，是让世界不必进来。"],
    "ch33": ["智是识词，明是照见；智越用越熟，明越照越静。",
             "力是筋，越使越少；强是弓，能张能弛。"],
    "ch32": ["知止不是收手不干，是知道地基的边在哪儿——再往外砌，就砌在虚空上了。",
             "江海之为大，在于它不挑水。"],
    "ch31": ["用是借它一次，处是住在它里面；借一次可以，住进去你就变成那种人了。",
             "淡不是无味，是味薄；恬淡不是没有情绪，是不往里面加糖。"],
    "ch30": ["兵是「合」的物理形态：它不让他想通，它让他不能不想通。",
             "弓有力，是因为它被拉满了；而拉满的弓，不能久张。"],
    "ch29": ["切是把一个整体分成几块，捏是把几块不同捏成一个；老子两样都不放心。",
             "和是听得见的，合是摸得着的。"],
    "ch28": ["装弱是权谋，守雌是心法；权谋是知而让，心法是知而不必。",
             "散是必然，老子的态度不是砸器回朴，是认下这个散，在散里用。"],
    "ch26": ["法地，不是学地的形状，是学地的分量。", "不是被外面夺了权，是你自己先把位置让出去了。"],
    "ch27": ["玉的病在里头，言的病在把柄上。", "不是他心肠软，是他看见的分类不成立。"],
}


def gold(y, key):
    out = [f'<line x1="20" y1="{y}" x2="360" y2="{y}" stroke="{LINE2}" stroke-width="0.8"/>']
    out.append(txt(20, y + 14, "本 章 金 句", 8.0, "#A89577", spacing="1"))
    for i, l in enumerate(GOLD[key]):
        out.append(txt(20, y + 14 + (i + 1) * 16, l, 8.4, INK))
    return "\n".join(out)



# ============ 第二十三章 · 希言自然 ============
def ch23_xi_yan_zi_ran():
    W, H = 380, 486
    body, y = head(W, H, "多言本身就是用力，用力过猛的东西撑不久", "第 二 十 三 章 · 自 然", "希言自然",
                   "说得越多，越不长：这一章问的是「你凭什么站得住」。", H)
    s = [body]
    # 风雨
    y0 = y + 4
    s.append(box(20, y0, 340, 52, fill="#F6EFE0", stroke="#C9B79A"))
    for i in range(4):
        xx = 44 + i * 18
        s.append(f'<line x1="{xx}" y1="{y0+12}" x2="{xx+16}" y2="{y0+40}" stroke="{LINE}" stroke-width="1"/>')
    for i in range(9):
        xx = 130 + (i % 5) * 12
        yy = y0 + 16 + (i // 5) * 16
        s.append(f'<line x1="{xx}" y1="{yy}" x2="{xx-3}" y2="{yy+9}" stroke="#B9A98F" stroke-width="1"/>')
    s.append(txt(238, y0 + 22, "飘风不终朝", 9.2, SEAL))
    s.append(txt(238, y0 + 38, "骤雨不终日", 9.2, SEAL))
    s.append(txt(20, y0 + 68, "天地用力，也撑不过一早一日；况于人乎。", 8.4, "#8A7C69"))
    # 三同
    y1 = y0 + 84
    rows = [("道", "同于道"), ("德", "同于德"), ("失", "同于失")]
    for i, (a, b) in enumerate(rows):
        yy = y1 + i * 30
        s.append(txt(40, yy + 16, a, 13, SEAL if a == "失" else GREEN))
        s.append(arrow(70, yy + 11, 118, yy + 11, color="#C9B79A", head="arr"))
        s.append(txt(124, yy + 16, b, 9.6, INK))
        s.append(txt(196, yy + 16, "道亦乐得之" if i == 0 else ("德亦乐得之" if i == 1 else "失亦乐得之"), 8.2, "#6E6459"))
    s.append(txt(20, y1 + 3 * 30 + 14, "不是道偏心，是同类相取：抱一是动作，同于是结果。", 8.2, "#8A7C69"))
    # 信不足
    y2 = y1 + 3 * 30 + 32
    s.append(box(36, y2, 68, 40, fill="none", stroke=LINE, dash="4 3"))
    s.append(txt(70, y2 + 25, "言", 10, "#8A7C69", "middle"))
    s.append(txt(120, y2 + 18, "话说了，话后面没有人：信不足。", 8.6, INK))
    s.append(txt(120, y2 + 32, "不是话说得不够多，是说得太多。", 8.2, "#6E6459"))
    yc = y2 + 48
    s.append(box(20, yc, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "自然不是没有秩序，是秩序自己长出来的。", 9.6, INK, "middle"))
    s.append(txt(190, yc + 34, "自，自身；然，如是：不借外力而自如此。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 48, "ch23"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第二十四章 · 企者不立 ============
def ch24_qi_zhe_bu_li():
    W, H = 380, 460
    body, y = head(W, H, "两个动作，一个方向：想越过自己本来的位置", "第 二 十 四 章 · 余 食 赘 行", "企者不立",
                   "一个求高，一个求快；动机是同一个。", H)
    s = [body]
    # 企 / 跨
    y0 = y + 6
    s.append(txt(20, y0 + 12, "企：举踵", 8.8, SEAL))
    s.append(f'<line x1="24" y1="{y0+56}" x2="158" y2="{y0+56}" stroke="{LINE2}" stroke-width="1"/>')
    # 脚：脚尖点在线上，脚跟抬起
    s.append(f'<line x1="64" y1="{y0+56}" x2="88" y2="{y0+40}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<circle cx="64" cy="{y0+56}" r="2.6" fill="{SEAL}"/>')
    s.append(f'<line x1="88" y1="{y0+40}" x2="88" y2="{y0+56}" stroke="{LINE}" stroke-width="1" stroke-dasharray="2 3"/>')
    # 借来的高度：一段虚的尺
    s.append(f'<line x1="100" y1="{y0+40}" x2="100" y2="{y0+18}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="96" y1="{y0+40}" x2="104" y2="{y0+40}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="96" y1="{y0+18}" x2="104" y2="{y0+18}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(110, y0 + 24, "借来的高度", 8.0, "#6E6459"))
    s.append(txt(110, y0 + 38, "力气一松，落回原高", 7.8, "#8A7C69"))
    s.append(txt(186, y0 + 12, "跨：大步越", 8.8, GREEN))
    s.append(f'<line x1="182" y1="{y0+56}" x2="356" y2="{y0+56}" stroke="{LINE2}" stroke-width="1"/>')
    for xx in (200, 340):
        s.append(f'<ellipse cx="{xx}" cy="{y0+53}" rx="6" ry="3" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<line x1="206" y1="{y0+53}" x2="334" y2="{y0+53}" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(txt(206, y0 + 36, "一步顶两步：半步要还", 7.8, "#8A7C69"))
    s.append(txt(20, y0 + 74, "不是劝人别努力：是这两个动作，都离开了本来的位置。", 8.4, "#8A7C69"))
    # 四句
    y1 = y0 + 92
    quads = [("自见", "不明"), ("自是", "不彰"), ("自伐", "无功"), ("自矜", "不长")]
    for i, (a, b) in enumerate(quads):
        col, row = i % 2, i // 2
        xx = 30 + col * 172
        yy = y1 + row * 30
        s.append(txt(xx, yy + 14, a, 9.4, SEAL))
        s.append(arrow(xx + 44, yy + 9, xx + 66, yy + 9, color="#C9B79A", head="arr"))
        s.append(txt(xx + 72, yy + 14, b, 9.4, "#6E6459"))
    s.append(txt(20, y1 + 2 * 30 + 12, "四个词是同一件事：把自己往前挪了半步。", 8.4, "#8A7C69"))
    # 余食赘行
    y2 = y1 + 2 * 30 + 30
    s.append(box(20, y2, 162, 48, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(101, y2 + 18, "余食", 9.4, SEAL, "middle"))
    s.append(txt(101, y2 + 33, "吃饱了，还要再添一口", 7.8, "#6E6459", "middle"))
    s.append(box(198, y2, 162, 48, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(279, y2 + 18, "赘行", 9.4, SEAL, "middle"))
    s.append(txt(279, y2 + 33, "身上多长出来的一块", 7.8, "#6E6459", "middle"))
    yc = y2 + 64
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "物或恶之，故有道者不处。", 10.4, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 35, "不处不是割掉，是不长在那儿。", 8.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch24"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第二十六章 · 重为轻根 ============
# ============ 第二十六章 · 重为轻根 ============
def ch26_zhong_wei_qing_gen():
    W, H = 380, 600
    body, y = head(W, H, "线在手，筝才在空", "第 二 十 六 章 · 轻 重", "重为轻根",
                   "轻能飞高，是因为下面有东西牵着它。", H)
    s = [body]
    # ---- 重为轻根：有根／失根 ----
    y0 = y + 6
    # 左：有根
    s.append('<polygon points="96,%d 126,%d 96,%d 66,%d" fill="#F2EADA" stroke="%s" stroke-width="1"/>'
             % (y0 + 2, y0 + 30, y0 + 58, y0 + 30, LINE))
    s.append(f'<line x1="66" y1="{y0+30}" x2="126" y2="{y0+30}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<line x1="96" y1="{y0+2}" x2="96" y2="{y0+58}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<line x1="96" y1="{y0+58}" x2="96" y2="{y0+100}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(box(78, y0 + 98, 26, 12, fill="#D9C7A6", stroke="#B9A98F"))
    s.append(f'<circle cx="96" cy="{y0+100}" r="4.6" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="40" y1="{y0+112}" x2="160" y2="{y0+112}" stroke="{LINE}" stroke-width="1"/>')
    s.append(txt(96, y0 + 132, "有根：线在手，筝才在空", 8.2, INK, "middle"))
    # 右：失根
    s.append('<polygon points="292,%d 320,%d 292,%d 264,%d" fill="#F2EADA" stroke="%s" stroke-width="1"/>'
             % (y0 + 8, y0 + 34, y0 + 60, y0 + 34, SEAL))
    s.append(f'<line x1="264" y1="{y0+34}" x2="320" y2="{y0+34}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="292" y1="{y0+8}" x2="292" y2="{y0+60}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="292" y1="{y0+60}" x2="294" y2="{y0+78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="298" y1="{y0+88}" x2="302" y2="{y0+100}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="288" y1="{y0+82}" x2="296" y2="{y0+88}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<line x1="296" y1="{y0+82}" x2="288" y2="{y0+88}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<circle cx="302" cy="{y0+104}" r="4.6" fill="{PAPER}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<line x1="210" y1="{y0+112}" x2="344" y2="{y0+112}" stroke="{LINE}" stroke-width="1"/>')
    s.append(txt(272, y0 + 132, "失根：线一断，筝就落", 8.2, SEAL, "middle"))

    # ---- 静为躁君：有君／失君 ----
    y1 = y0 + 170
    s.append(txt(20, y1 - 10, "静为躁君：君是统摄，不是压制", 8.8, SEAL))
    # 有君：手在上，收放由手
    s.append(box(46, y1 + 24, 42, 24, fill="#D9C7A6", stroke="#B9A98F"))
    s.append(txt(67, y1 + 40, "线轴", 8.0, INK, "middle"))
    s.append(f'<circle cx="67" cy="{y1+18}" r="5" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    s.append(arrow(67, y1 + 12, 34, y1 + 2, color="#6E6459", width=1.0, head="arr"))
    s.append(arrow(67, y1 + 12, 102, y1 + 2, color="#6E6459", width=1.0, head="arr"))
    s.append(txt(30, y1 + 0, "收", 7.4, "#6E6459"))
    s.append(txt(92, y1 + 0, "放", 7.4, "#6E6459"))
    s.append(txt(20, y1 + 68, "有君：收放由手", 8.4, INK))
    s.append(txt(20, y1 + 82, "线放多长，手说了算", 7.6, "#8A7C69"))
    # 失君：手松开，线自己乱摆
    s.append(f'<circle cx="248" cy="{y1+18}" r="5" fill="{PAPER}" stroke="{SEAL}" stroke-width="1"/>')
    zz = [(248, y1 + 14), (248, y1 + 2), (268, y1 + 10), (288, y1 - 2), (308, y1 + 10), (328, y1 - 2), (344, y1 + 4)]
    for i in range(len(zz) - 1):
        s.append(f'<line x1="{zz[i][0]}" y1="{zz[i][1]}" x2="{zz[i+1][0]}" y2="{zz[i+1][1]}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(216, y1 + 68, "失君：手一松，线自己乱摆", 8.4, SEAL))
    s.append(txt(216, y1 + 82, "没人下令，筝就成了风的东西", 7.6, "#8A7C69"))
    s.append(txt(20, y1 + 104, "静不是不动，静是动的发令处；躁不是动，是动失了主。", 8.4, "#6E6459"))
    # ---- 辎重 / 荣观·燕处 ----
    y2 = y1 + 122
    s.append(box(20, y2, 162, 44, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(101, y2 + 17, "辎重：线轴随身", 8.6, GREEN, "middle"))
    s.append(txt(101, y2 + 32, "走到哪，轴都带着", 7.6, "#6E6459", "middle"))
    s.append(box(198, y2, 162, 44, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(279, y2 + 17, "荣观：筝飞得高，好看", 8.4, SEAL, "middle"))
    s.append(txt(279, y2 + 32, "燕处：脚不离地，手不撒开", 7.6, "#6E6459", "middle"))
    # ---- 收 ----
    yc = y2 + 62
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "轻则失根，躁则失君。", 10.4, INK, "middle", spacing="1"))
    s.append(txt(190, yc + 34, "线在手，筝才在空；手一松，筝就成了风的东西。", 8.2, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch26"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第二十七章 · 善行无辙迹 ============
def ch27_shan_xing_wu_zhe_ji():
    W, H = 380, 548
    body, y = head(W, H, "善不是做得多，是做完不留把柄", "第 二 十 七 章 · 善 用", "善行无辙迹",
                   "五种善，五次「不用工具」；不用，事也成了。", H)
    s = [body]
    rows = [("善行", "无辙迹", "路面上最深那道沟，是载重的车压出来的"),
            ("善言", "无瑕谪", "不是说得漂亮，是说得干净"),
            ("善数", "不用筹策", "数得对，不必把筹码摊一桌"),
            ("善闭", "无关楗", "门不闩，也开不了"),
            ("善结", "无绳约", "绳不用，也解不开")]
    y0 = y + 4
    for i, (a, b, note) in enumerate(rows):
        yy = y0 + i * 30
        s.append(txt(20, yy + 16, a, 9.6, SEAL))
        s.append(arrow(64, yy + 11, 86, yy + 11, color="#C9B79A", head="arr"))
        s.append(txt(92, yy + 16, b, 9.0, INK))
        s.append(txt(172, yy + 16, note, 7.8, "#6E6459"))
    y1 = y0 + 5 * 30 + 6
    s.append(txt(20, y1, "五个「不」都是同一件事：动作做尽，痕迹不落。", 8.4, "#8A7C69"))
    # 无弃人 / 无弃物
    y2 = y1 + 16
    s.append(box(20, y2, 162, 42, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(101, y2 + 18, "常善救人：无弃人", 8.6, GREEN, "middle"))
    s.append(txt(101, y2 + 33, "不是心肠软，是分类不成立", 7.6, "#6E6459", "middle"))
    s.append(box(198, y2, 162, 42, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(279, y2 + 18, "常善救物：无弃物", 8.6, GREEN, "middle"))
    s.append(txt(279, y2 + 33, "不是用得省，是没有废物这一格", 7.6, "#6E6459", "middle"))
    s.append(txt(20, y2 + 58, "是谓袭明：这份明不是自己点的，是从上头承来的。", 8.2, "#8A7C69"))
    # 师与资
    y3 = y2 + 74
    s.append(box(20, y3, 162, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(101, y3 + 18, "善人：师", 9, INK, "middle"))
    s.append(txt(101, y3 + 33, "给一个方向", 7.8, "#6E6459", "middle"))
    s.append(box(198, y3, 162, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(279, y3 + 18, "不善人：资", 9, INK, "middle"))
    s.append(txt(279, y3 + 33, "给一份本钱", 7.8, "#6E6459", "middle"))
    yc = y3 + 58
    s.append(box(20, yc, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "不贵其师，不爱其资，虽智大迷。", 9.6, INK, "middle"))
    s.append(txt(190, yc + 34, "迷不在无知，在太会分。", 8.4, SEAL, "middle"))
    s.append(gold(yc + 50, "ch27"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二十八章 · 知其雄 ============
def ch28_zhi_xiong():
    W, H = 380, 608
    body, y = head(W, H, "知而不必，是心法", "第 二 十 八 章 · 溪 谷", "知其雄",
                   "知与守同时：看见了，但不往那儿去。", H)
    s = [body]
    # ---- 三组知守 ----
    cols = [26, 78, 134, 198, 266]
    for cx, lab in zip(cols, ["知（照见）", "守（安住）", "为天下", "常德", "复归"]):
        s.append(txt(cx, y + 6, lab, 7.4, "#8A7C69"))
    rows = [("雄", "雌", "溪", "不离", "婴儿"),
            ("白", "黑", "式", "不忒", "无极"),
            ("荣", "辱", "谷", "乃足", "朴")]
    y0 = y + 16
    for i, (a, b, wei, de, gui) in enumerate(rows):
        yy = y0 + i * 48
        s.append(box(cols[0], yy, 44, 22, fill="#FBF6EC", stroke=LINE))
        s.append(txt(cols[0] + 22, yy + 15, a, 9.2, INK, "middle"))
        s.append(box(cols[1], yy, 44, 22, fill="#EFE3CC", stroke="#C9B79A"))
        s.append(txt(cols[1] + 22, yy + 15, b, 9.2, INK, "middle"))
        s.append(arrow(cols[0] + 46, yy + 11, cols[1] - 4, yy + 11, color="#A2503B", width=0.9, head="arrS"))
        s.append(txt(cols[2], yy + 15, f"为天下{wei}", 8.4, GREEN))
        s.append(txt(cols[3], yy + 15, f"常德{de}", 8.0, INK))
        s.append(txt(cols[4], yy + 15, f"复归{gui}", 8.0, SEAL))
    note_y = y0 + 3 * 48 + 8
    s.append(txt(20, note_y, "知是照见，守是安住；不是先看、再退两步——知不必通向取。", 8.2, "#6E6459"))
    # ---- 溪与谷：一纳一出 ----
    y1 = note_y + 18
    s.append(box(20, y1, 162, 38, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(101, y1 + 16, "溪：众水所归", 8.8, GREEN, "middle"))
    s.append(txt(101, y1 + 30, "受——低处，水自己来", 7.6, "#6E6459", "middle"))
    s.append(box(198, y1, 162, 38, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(279, y1 + 16, "谷：泉水所出", 8.8, GREEN, "middle"))
    s.append(txt(279, y1 + 30, "出——虚而能出", 7.6, "#6E6459", "middle"))
    # ---- 朴散则为器 ----
    y2 = y1 + 54
    s.append(txt(20, y2, "朴散则为器：原木一剖，才成了一件件有用的东西。", 8.4, SEAL))
    s.append(box(26, y2 + 10, 58, 40, fill="#D9C7A6", stroke="#B9A98F"))
    s.append(txt(55, y2 + 34, "朴", 8.8, INK, "middle"))
    for sy, ty in ((y2 + 16, y2 + 14), (y2 + 30, y2 + 30), (y2 + 44, y2 + 46)):
        s.append(arrow(88, sy, 172, ty, color="#6E6459", width=0.7))
    s.append(f'<circle cx="186" cy="{y2+14}" r="7.5" fill="#F2EADA" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<rect x="178" y="{y2+23}" width="15" height="15" fill="#F2EADA" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<polygon points="186,{y2+39} 195,{y2+54} 177,{y2+54}" fill="#F2EADA" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(txt(206, y2 + 26, "同一条原木，", 7.6, "#6E6459"))
    s.append(txt(206, y2 + 38, "剖开就各有其用", 7.6, "#6E6459"))
    s.append(txt(20, y2 + 70, "散是必然：老子不砸器回朴，是认下这个散，在散里用。", 8.0, "#8A7C69"))
    # ---- 大制不割 ----
    y3 = y2 + 96
    s.append(txt(20, y3, "大制不割：最高明的裁制，是刀不动。", 8.4, SEAL))
    s.append(box(30, y3 + 24, 64, 20, fill="#D9C7A6", stroke="#B9A98F"))
    s.append(txt(62, y3 + 38, "木", 8.2, INK, "middle"))
    s.append(f'<rect x="58" y="{y3+0}" width="7" height="5" fill="#E9DFCC" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<line x1="61" y1="{y3+5}" x2="61" y2="{y3+18}" stroke="{SEAL}" stroke-width="1.6"/>')
    s.append(f'<line x1="61" y1="{y3+17}" x2="61" y2="{y3+24}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="2 2"/>')
    s.append(txt(106, y3 + 22, "刀悬在木上，不落", 7.8, SEAL))
    s.append(txt(106, y3 + 36, "制、割二字都带刀，老子偏说不割", 7.6, "#8A7C69"))
    # ---- 收 ----
    yc = y3 + 56
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "知而不必，是心法；知而让，是权谋。", 9.6, INK, "middle", spacing="0.6"))
    s.append(txt(190, yc + 34, "守不是没本事上去，是有本事，但不往那儿去。", 8.2, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch28"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第二十九章 · 天下神器 ============
def ch29_tian_xia_shen_qi():
    W, H = 380, 636
    body, y = head(W, H, "天下是编管，不是一根棍", "第 二 十 九 章 · 神 器", "天下神器",
                   "长短本就不齐，能调成调，不能削成一根。", H)
    s = [body]
    # ---- 一器：编管 ----
    base = y + 126
    s.append(txt(20, y + 4, "一器：编管，长短本就不齐", 8.6, GREEN))
    pipes = [(48, 58), (84, 84), (120, 46), (156, 74), (192, 92), (228, 52)]
    for px, ph in pipes:
        s.append(f'<rect x="{px}" y="{base-ph}" width="15" height="{ph}" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.9"/>')
        s.append(f'<circle cx="{px+7.5}" cy="{base-11}" r="2.2" fill="{PAPER}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(box(42, base - 44, 204, 5, fill="#DCCBB0", stroke="#C9B79A", width=0.7))
    s.append(box(42, base - 18, 204, 5, fill="#DCCBB0", stroke="#C9B79A", width=0.7))
    for i, t in enumerate(["或行或随", "或歔或吹", "或强或羸", "或载或隳"]):
        s.append(txt(258, y + 40 + i * 15, t, 8.0, "#6E6459"))
    s.append(txt(258, y + 106, "八样都是料性，不是毛病", 7.4, SEAL))
    # ---- 两病：削平 / 攥住 ----
    y1 = base + 22
    s.append(txt(20, y1, "两病：一为、一执", 8.6, SEAL))
    # 为：削成一样齐
    b2 = y1 + 92
    for i in range(5):
        s.append(f'<rect x="{28+i*20}" y="{b2-56}" width="15" height="56" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.9"/>')
        s.append(f'<circle cx="{35+i*20}" cy="{b2-10}" r="2.2" fill="{PAPER}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="22" y1="{b2-62}" x2="132" y2="{b2-62}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="4 2"/>')
    s.append(txt(78, b2 + 14, "为：削成一样齐", 8.2, SEAL, "middle"))
    s.append(txt(78, b2 + 27, "音就没了——调不成调", 7.4, "#8A7C69", "middle"))
    # 执：攥住
    s.append(f'<ellipse cx="286" cy="{b2-30}" rx="30" ry="20" fill="#E9DFCC" stroke="{SEAL}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<path d="M266,{b2-40+i*7} q10,-5 20,0" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    for i in range(3):
        s.append(f'<line x1="{272+i*12}" y1="{b2-52}" x2="{274+i*12}" y2="{b2-8}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(286, b2 + 14, "执：攥住不放", 8.2, SEAL, "middle"))
    s.append(txt(286, b2 + 27, "管子捏死，吹不响", 7.4, "#8A7C69", "middle"))
    # ---- 和 / 合 ----
    y2 = y1 + 122
    s.append(box(20, y2, 162, 56, fill="#F6EFE0", stroke="#C9B79A"))
    for i, ph in enumerate([26, 34, 20, 30]):
        s.append(f'<rect x="{34+i*13}" y="{y2+44-ph}" width="10" height="{ph}" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(108, y2 + 18, "和", 10.4, GREEN, spacing="1"))
    s.append(txt(108, y2 + 34, "长短不一，同调共存", 7.6, "#6E6459"))
    s.append(txt(108, y2 + 47, "听得见的", 7.4, "#8A7C69"))
    s.append(box(198, y2, 162, 56, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(f'<rect x="242" y="{y2+26}" width="34" height="20" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<polygon points="236,{y2+26} 282,{y2+26} 274,{y2+14} 244,{y2+14}" fill="#DCCBB0" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(286, y2 + 20, "合", 10.4, SEAL))
    s.append(txt(279, y2 + 40, "盖扣上，边没了", 7.6, "#6E6459", "middle"))
    s.append(txt(279, y2 + 52, "摸得着的", 7.4, "#8A7C69", "middle"))
    # ---- 三去 ----
    y3 = y2 + 72
    s.append(txt(20, y3, "三去：全是减法，不添一件", 8.6, SEAL))
    tags = [("甚", "过度", "孔开太多"), ("奢", "无度", "管加太长"), ("泰", "骄纵越分", "气吹太猛")]
    for i, (name, mid, sub) in enumerate(tags):
        x = 20 + i * 116
        s.append(box(x, y3 + 10, 106, 46, fill="#F6EFE0", stroke="#C9B79A"))
        s.append(txt(x + 12, y3 + 28, "去" + name, 9.4, SEAL))
        s.append(txt(x + 12, y3 + 40, mid + "：" + sub, 7.2, "#6E6459"))
    # ---- 收 ----
    yc = y3 + 68
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 19, "天下神器，不可为也，不可执也。", 9.6, INK, "middle", spacing="0.6"))
    s.append(txt(190, yc + 34, "为者败之，执者失之——不是你不够强，是它本来不是给你捏的。", 8.0, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch29"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十章 · 物壮则老 ============
def ch30_wu_zhuang_ze_lao():
    W, H = 380, 646
    body, y = head(W, H, "兵是一张满弓：一发即止，还是久张到断", "第 三 十 章 · 兵 与 果", "物壮则老",
                   "佐是搭手，不是推手；弓有力，是因为它被拉满了。", H)
    s = [body]

    def bow(cx, cy, w=30, h=44):
        return (f'<path d="M{cx},{cy-h} Q{cx-w},{cy} {cx},{cy+h}" fill="none" stroke="{INK}" stroke-width="1.5"/>')

    # ---- 弓：两态 ----
    s.append(txt(20, y + 6, "兵：一张满弓，两种用法", 8.6, GREEN))
    # 左：一发即止
    s.append(bow(72, y + 74))
    s.append(f'<path d="M72,{y+30} Q48,{y+74} 72,{y+118}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(arrow(56, y + 74, 116, y + 74, SEAL, 1.2, head="arrS"))
    s.append(f'<path d="M72,{y+30} Q86,{y+74} 72,{y+118}" fill="none" stroke="#B9A98F" stroke-width="0.9" stroke-dasharray="4 3"/>')
    s.append(txt(72, y + 140, "满而不久：一矢而止", 8.2, INK, "middle"))
    s.append(txt(72, y + 153, "果而已，不取强", 7.4, "#8A7C69", "middle"))
    # 右：久张
    s.append(bow(252, y + 74))
    s.append(f'<path d="M252,{y+30} Q240,{y+52} 236,{y+68}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M236,{y+80} Q240,{y+98} 252,{y+118}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(236, y + 76, "×", 9.0, SEAL, "middle"))
    s.append(txt(252, y + 140, "久张：弦断弓折", 8.2, SEAL, "middle"))
    s.append(txt(252, y + 153, "取强，则物壮", 7.4, "#8A7C69", "middle"))
    s.append(txt(162, y + 186, "「其事好还」：力发出去，最先回来的是它自己", 7.4, "#6E6459", "middle"))

    # ---- 果：树结果就停 ----
    y1 = y + 202
    s.append(txt(20, y1, "果：树结果就停，人未必", 8.6, GREEN))

    def tree(cx, by, fruit, up):
        out = [f'<line x1="{cx}" y1="{by}" x2="{cx}" y2="{by-40}" stroke="{INK}" stroke-width="1.6"/>']
        out.append(f'<path d="M{cx},{by-26} l-16,-14" stroke="{INK}" stroke-width="1.1"/>')
        out.append(f'<path d="M{cx},{by-30} l16,-16" stroke="{INK}" stroke-width="1.1"/>')
        out.append(f'<path d="M{cx},{by-40} l-8,-14" stroke="{INK}" stroke-width="1"/>')
        out.append(f'<path d="M{cx},{by-40} l10,-16" stroke="{INK}" stroke-width="1"/>')
        for (fx, fy) in fruit:
            out.append(f'<circle cx="{fx}" cy="{fy}" r="4.4" fill="#EFE0C4" stroke="{SEAL}" stroke-width="0.8"/>')
        return "\n".join(out)

    # 左树：结完就停
    s.append(tree(70, y1 + 96, [(54, y1 + 52), (70, y1 + 44), (86, y1 + 54), (62, y1 + 66)], False))
    s.append(f'<line x1="30" y1="{y1+38}" x2="112" y2="{y1+38}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 2"/>')
    s.append(txt(114, y1 + 41, "到这儿就停", 7.4, SEAL))
    s.append(txt(70, y1 + 112, "果而已：不再往上要", 8.0, INK, "middle"))

    # 右树：拿果换更大的自己
    s.append(tree(250, y1 + 96, [(234, y1 + 54), (250, y1 + 46), (266, y1 + 56), (256, y1 + 68)], True))
    s.append(f'<line x1="212" y1="{y1+38}" x2="292" y2="{y1+38}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 2"/>')
    s.append(arrow(280, y1 + 46, 296, y1 + 18, SEAL, 1.2, head="arrS"))
    s.append(txt(250, y1 + 112, "求壮：提前领老", 8.0, SEAL, "middle"))

    # ---- 荆棘 ----
    y2 = y1 + 130
    s.append(txt(20, y2, "师之所处，荆棘生焉", 8.6, GREEN))
    s.append(f'<line x1="22" y1="{y2+62}" x2="358" y2="{y2+62}" stroke="{LINE}" stroke-width="1"/>')
    for i in range(9):
        gx = 34 + i * 14
        s.append(f'<path d="M{gx},{y2+62} l-3,-9 M{gx},{y2+62} l0,-11 M{gx},{y2+62} l4,-9" stroke="#B9A98F" stroke-width="0.8"/>')
    for i in range(4):
        tx = 178 + i * 44
        s.append(f'<path d="M{tx},{y2+62} l6,-16 l-7,-12 l8,-14 l-5,-12" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        for j in range(4):
            yy = y2 + 56 - j * 9
            s.append(f'<path d="M{tx+ (2 if j%2==0 else 6)},{yy} l-7,-3" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(20, y2 + 80, "荒地先长刺，因为刺不需要人养。", 7.6, SEAL))

    # ---- 收 ----
    y3 = y2 + 96
    s.append(box(20, y3, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 19, "物壮则老，是谓不道；不道早已。", 9.6, INK, "middle", spacing="0.6"))
    s.append(txt(190, y3 + 34, "求壮，就是提前领老。", 8.0, "#6E6459", "middle"))
    s.append(gold(y3 + 52, "ch30"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十一章 · 兵者不祥之器 ============
def ch31_bing_zhe_bu_xiang():
    W, H = 380, 552
    body, y = head(W, H, "一件器被定了名，就有了位次：左吉、右凶，兵不许搬到左边", "第 三 十 一 章 · 器 与 位", "兵者不祥之器",
                   "上一章管手，本章管心：给一件东西定名，才知道该怎么拿它。", H)
    s = [body]

    # ---- 一器：定名 ----
    s.append(txt(20, y + 4, "一器：定名", 8.6, GREEN))
    s.append(f'<path d="M62,{y+26} Q74,{y+60} 62,{y+96} Q50,{y+60} 62,{y+26} z" fill="#E9DFCC" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="62" y1="{y+40}" x2="62" y2="{y+84}" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(88, y + 46, "不祥之器", 10.0, SEAL))
    s.append(txt(88, y + 62, "物或恶之，故有道者不处", 7.6, "#6E6459"))
    s.append(txt(88, y + 78, "「处」是止、是安身——不是不能用，是不能住进去", 7.4, "#8A7C69"))

    # ---- 位次：左吉右凶 ----
    y1 = y + 118
    s.append(txt(20, y1, "位次：吉事尚左，凶事尚右", 8.6, GREEN))
    s.append(txt(24, y1 + 22, "左 · 吉", 7.8, GREEN))
    s.append(txt(356, y1 + 22, "右 · 凶", 7.8, SEAL, "end"))
    s.append(vline(24, y1 + 40, y1 + 72, LINE, 1))
    s.append(vline(356, y1 + 40, y1 + 72, LINE, 1))
    s.append(f'<line x1="24" y1="{y1+68}" x2="356" y2="{y1+68}" stroke="{LINE}" stroke-width="1"/>')
    for i, t in enumerate(["冠", "婚", "聘"]):
        x = 44 + i * 30
        s.append(box(x, y1 + 40, 18, 18, fill="#F2EADA", stroke=LINE))
        s.append(txt(x + 9, y1 + 54, t, 7.6, INK, "middle"))
    s.append(box(292, y1 + 40, 18, 18, fill="#FDFBF4", stroke="#C9B79A"))
    s.append(txt(301, y1 + 54, "丧", 7.6, INK, "middle"))
    s.append(box(322, y1 + 40, 18, 18, fill="#E7C9BE", stroke=SEAL))
    s.append(txt(331, y1 + 54, "兵", 7.8, SEAL, "middle"))
    # 借与还
    s.append(f'<path d="M318,{y1+40} Q331,{y1+22} 344,{y1+40}" fill="none" stroke="{SEAL}" stroke-width="0.9" marker-end="url(#arrS)"/>')
    s.append(txt(348, y1 + 40, "借", 7.4, SEAL))
    s.append(txt(24, y1 + 82, "不得已：借它一次，用完还回右位——「恬淡为上」", 7.6, "#6E6459"))
    # 越界：把凶位搬到吉位
    s.append(arrow(318, y1 + 92, 96, y1 + 92, SEAL, 1.0, dash="4 3", head="arrS"))
    s.append(txt(206, y1 + 88, "×", 8.4, SEAL, "middle"))
    s.append(txt(24, y1 + 110, "美之：把右位搬到左位——「乐杀人者，不可以得志于天下」", 7.4, SEAL))

    # ---- 三处落点 ----
    y2 = y1 + 122
    cards = [("恬淡", "味薄，不往里加糖"), ("居左居右", "偏将军左，上将军右"), ("胜而不美", "胜是付，不是得")]
    for i, (t, sub) in enumerate(cards):
        x = 20 + i * 116
        s.append(box(x, y2, 106, 58, fill="#F6EFE0", stroke="#C9B79A"))
        s.append(txt(x + 10, y2 + 20, t, 9.2, INK))
        s.append(txt(x + 10, y2 + 38, sub, 7.2, "#6E6459"))
    s.append(txt(20, y2 + 76, "丧礼是五礼里唯一不许笑的一种：战胜以丧礼处之，就是把它放进那个不许笑的地方。", 7.2, "#8A7C69"))

    # ---- 收 ----
    y3 = y2 + 90
    s.append(box(20, y3, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 19, "兵者不祥之器，非君子之器，不得已而用之。", 9.0, INK, "middle"))
    s.append(txt(190, y3 + 34, "胜不是得，胜是付。", 8.0, "#6E6459", "middle"))
    s.append(gold(y3 + 52, "ch31"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十二章（候选一） · 名与止 ============
def ch32a_ming_zhi():
    W, H = 380, 492
    body, y = head(W, H, "朴是木素，名是裁切；裁到地基的边就停", "第 三 十 二 章 · 其 一", "名 与 止",
                   "朴不是没有形状，是形状还没有被定下来。", H)
    s = [body]

    # ---- 朴 ----
    s.append(txt(20, y + 4, "朴：木素也，未加斧斤", 8.6, GREEN))
    s.append(f'<path d="M34,{y+26} L70,{y+18} L88,{y+44} L80,{y+76} L44,{y+82} L28,{y+52} z" fill="#E9DFCC" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(104, y + 36, "朴不是没有形状", 8.4, INK))
    s.append(txt(104, y + 50, "是形状还没有被定下来", 8.4, INK))
    s.append(txt(104, y + 66, "所以它可方可圆，也可成一只兽", 7.2, "#8A7C69"))

    # ---- 名 ----
    y1 = y + 104
    s.append(txt(20, y1, "名：裁也——把木放进格", 8.6, GREEN))
    for i, t in enumerate(["名一", "名二", "名三"]):
        x = 30 + i * 74
        s.append(box(x, y1 + 12, 64, 36, fill="#F2EADA", stroke=LINE))
        if i == 0:
            s.append(f'<rect x="{x+12}" y="{y1+22}" width="40" height="18" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.8"/>')
        elif i == 1:
            s.append(f'<circle cx="{x+32}" cy="{y1+31}" r="10" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.8"/>')
        else:
            s.append(f'<path d="M{x+12},{y1+40} L{x+32},{y1+20} L{x+52},{y1+40} z" fill="#E9DFCC" stroke="{LINE}" stroke-width="0.8"/>')
        s.append(txt(x + 32, y1 + 62, t, 7.4, "#6E6459", "middle"))
    s.append(txt(20, y1 + 80, "「始制有名」：名是必须立的——不立，连话都说不出", 7.4, "#6E6459"))

    # ---- 止 ----
    y2 = y1 + 96
    s.append(txt(20, y2, "止：地基有边，再砌就砌在虚空上", 8.6, GREEN))
    for i in range(3):
        x = 30 + i * 64
        s.append(box(x, y2 + 12, 56, 36, fill="#F2EADA", stroke=LINE))
    s.append(box(230, y2 + 12, 56, 36, fill="none", stroke=SEAL, dash="4 3", width=0.9))
    s.append(txt(258, y2 + 34, "×", 9.0, SEAL, "middle"))
    s.append(txt(258, y2 + 60, "越界的格", 7.2, SEAL, "middle"))
    s.append(vline(224, y2 + 6, y2 + 56, SEAL, 0.8))
    s.append(txt(228, y2 + 4, "地基边", 7.0, SEAL))
    s.append(txt(20, y2 + 74, "「知止」：知道地基的边在哪儿——不是收手不干，是不往虚空里砌", 7.4, "#6E6459"))

    # ---- 收 ----
    y3 = y2 + 90
    s.append(box(20, y3, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 19, "始制有名，名亦既有，夫亦将知止；知止可以不殆。", 8.8, INK, "middle"))
    s.append(txt(190, y3 + 33, "名越界，不是名坏了，是执名的人把地基当成了天空。", 7.8, "#6E6459", "middle"))
    s.append(gold(y3 + 50, "ch32"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十二章（候选二） · 川谷与江海 ============
def ch32b_chuan_gu():
    W, H = 380, 400
    body, y = head(W, H, "百川各有宽窄急缓，江海不挑水", "第 三 十 二 章 · 其 二", "川 谷 与 江 海",
                   "江海之为大，在于它不要求支流先改成一样的河道。", H)
    s = [body]

    s.append(txt(20, y + 2, "川谷：各有各的走向、宽窄、急缓", 8.4, GREEN))
    rivers = [
        (52, 7, 11, "M52,{a} C40,{c} 62,{d} 46,{b}"),
        (104, 20, 17, "M104,{a} C90,{c} 114,{d} 94,{b}"),
        (152, 11, 13, "M152,{a} C164,{c} 140,{d} 156,{b}"),
        (208, 24, 21, "M208,{a} C194,{c} 220,{d} 200,{b}"),
        (262, 13, 15, "M262,{a} C276,{c} 250,{d} 270,{b}"),
        (316, 6, 9, "M316,{a} C304,{c} 326,{d} 310,{b}")
    ]
    top, bot = y + 16, y + 112
    for (x, w, w2, d) in rivers:
        s.append(f'<path d="{d.format(a=top, c=top+40, d=bot-30, b=bot)}" fill="none" stroke="#C2D0C7" stroke-width="0.8"/>')
        s.append(f'<path d="M{x-w/2},{top+2} C{x-w/2-6},{top+40} {x-w2/2},{bot-30} {x-w2/2},{bot}" fill="none" stroke="#6E6459" stroke-width="1.2"/>')
        s.append(f'<path d="M{x+w/2},{top+2} C{x+w/2+6},{top+40} {x+w2/2},{bot-30} {x+w2/2},{bot}" fill="none" stroke="#6E6459" stroke-width="1.2"/>')
        s.append(f'<circle cx="{x}" cy="{top}" r="{2.4+w*0.18}" fill="none" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(txt(208, y + 96, "宽", 7.2, "#6E6459", "middle"))
    s.append(txt(316, y + 96, "窄", 7.2, "#6E6459", "middle"))
    # 江海
    s.append(f'<path d="M24,{y+112} Q190,{y+96} 356,{y+112} L356,{y+134} Q190,{y+150} 24,{y+134} z" fill="#DCE5DF" stroke="#B9C7BE" stroke-width="0.9"/>')
    for i in range(2):
        s.append(f'<path d="M66,{y+122+i*9} q22,-5 44,0 q22,5 44,0" fill="none" stroke="#9FB0A6" stroke-width="0.8"/>')
    s.append(txt(250, y + 128, "江海", 10.0, GREEN, "middle", spacing="2"))
    s.append(txt(20, y + 160, "不挑水：千条支流不改河道，也能进来", 7.6, "#6E6459"))

    # 对照
    y1 = y + 176
    s.append(box(20, y1, 162, 56, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(32, y1 + 18, "道：同归，不失自性", 8.2, GREEN))
    s.append(txt(32, y1 + 34, "差异不必先被抹平", 7.4, "#6E6459"))
    s.append(txt(32, y1 + 46, "来是「宾」，不是「臣」", 7.4, "#6E6459"))
    s.append(box(198, y1, 162, 56, fill="#F6EFE0", stroke="#C9B79A"))
    s.append(txt(210, y1 + 18, "合：先改成一样的河道", 8.2, SEAL))
    s.append(txt(210, y1 + 34, "削平、捏成一条", 7.4, "#6E6459"))
    s.append(txt(210, y1 + 46, "那是人之合", 7.4, "#6E6459"))

    # 收
    y2 = y1 + 74
    s.append(box(20, y2, 340, 42, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 19, "譬道之在天下，犹川谷之于江海。", 9.4, INK, "middle", spacing="0.6"))
    s.append(txt(190, y2 + 33, "江海之为大，在于它不挑水。", 7.8, "#6E6459", "middle"))
    s.append(gold(y2 + 50, "ch32"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十三章 · 自知者明 ============
def ch33_zi_zhi_zhe_ming():
    W, H = 380, 712
    body, y = head(W, H, "四对八句：前一半是世人正在追的，后一半才是老子要的", "第 三 十 三 章 · 四 对", "自知者明",
                   "前面收的是事；这一章收的是那个做事的人。", H)
    s = [body]

    rows = [
        ("知人 · 智", ("拿灯照别人", "识词、贴标签"), "自知 · 明", ("灯照到自己", "照见，不是想通")),
        ("胜人 · 有力", ("筋：一次性的", "越使越少"), "自胜 · 强", ("弓：能张能弛", "越练越熟")),
        ("知足 · 富", ("备：该有的都有", "缺是单子太长"), "强行 · 有志", ("向外止，向内行", "不肯向内停")),
        ("不失其所 · 久", ("根扎在原处", "位不失，故久"), "死而不亡 · 寿", ("身可以散", "根不能失")),
    ]

    for i, (l1, ln1, r1, rn1) in enumerate(rows):
        cy = y + 2 + i * 122
        for bx in (20, 198):
            s.append(box(bx, cy, 162, 112, fill="#FBF6EC", stroke="#E6D8C2"))
        s.append(txt(32, cy + 20, l1, 8.8, GREEN))
        s.append(txt(210, cy + 20, r1, 8.8, SEAL))
        for bx, note in ((20, ln1), (198, rn1)):
            s.append(txt(bx + 12, cy + 84, note[0], 7.2, "#6E6459"))
            s.append(txt(bx + 12, cy + 97, note[1], 7.2, "#6E6459"))

    # ---- 图标 ----
    # 行1
    c = y + 2
    for bx in (20, 198):
        s.append(f'<path d="M{bx+18},{c+62} l6,-11 l6,11 z" fill="#E7C9BE" stroke="{LINE}" stroke-width="0.7"/>')
        s.append(f'<line x1="{bx+17}" y1="{c+62}" x2="{bx+31}" y2="{c+62}" stroke="{LINE}" stroke-width="0.9"/>')
    # 左：三道光射向「人」
    s.append(f'<circle cx="{52}" cy="{c+36}" r="3.6" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(58, c + 39, "人", 6.6, "#6E6459"))
    for a in (-14, 0, 14):
        s.append(f'<line x1="26" y1="{c+50}" x2="47" y2="{c+38-a/3}" stroke="#C9B79A" stroke-width="0.8"/>')
    # 右：一道光落到镜
    s.append(f'<circle cx="{234}" cy="{c+46}" r="11" fill="#F2EADA" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<path d="M229,{c+50} q5,-9 10,0" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<line x1="204" y1="{c+50}" x2="221" y2="{c+46}" stroke="#C9B79A" stroke-width="0.8"/>')
    s.append(txt(248, c + 50, "我", 6.6, "#6E6459"))

    # 行2 筋 / 弓
    c2 = c + 122
    s.append(f'<rect x="34" y="{c2+44}" width="36" height="11" fill="#E9DFCC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M30,{c2+49} l-7,0 M74,{c2+49} l7,0" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<path d="M214,{c2+32} Q226,{c2+48} 214,{c2+64}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M226,{c2+32} Q238,{c2+48} 226,{c2+64}" fill="none" stroke="#B9A98F" stroke-width="1.0" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="227" y1="{c2+32}" x2="227" y2="{c2+64}" stroke="{INK}" stroke-width="0.9"/>')

    # 行3 碗 / 向内
    c3 = c + 244
    s.append(f'<path d="M34,{c3+40} q12,24 26,0" fill="#F2EADA" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="32" y1="{c3+40}" x2="62" y2="{c3+40}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M38,{c3+48} q11,4 20,0" fill="none" stroke="#9FB0A6" stroke-width="0.8"/>')
    s.append(f'<circle cx="{238}" cy="{c3+50}" r="12" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(238, c3 + 53, "己", 6.6, "#6E6459", "middle"))
    s.append(arrow(206, c3 + 50, 224, c3 + 50, SEAL, 0.9, head="arrS"))

    # 行4 树 / 倒木与苗
    c4 = c + 366
    s.append(f'<line x1="28" y1="{c4+62}" x2="86" y2="{c4+62}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<line x1="54" y1="{c4+62}" x2="54" y2="{c4+34}" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<path d="M54,{c4+62} l-9,7 M54,{c4+62} l9,7 M54,{c4+62} l-3,9 M54,{c4+62} l3,9" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M54,{c4+34} l-8,-9 M54,{c4+34} l8,-9" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="206" y1="{c4+62}" x2="264" y2="{c4+62}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<path d="M206,{c4+60} l38,-16" stroke="#B9A98F" stroke-width="1.6"/>')
    s.append(f'<path d="M226,{c4+52} l3,-13 M230,{c4+52} l6,-4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M246,{c4+44} l2,-14 M248,{c4+44} l6,-5" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="258" cy="{c4+58}" r="2.2" fill="{SEAL}"/>')

    # ---- 收 ----
    y3 = y + 2 + 4 * 122 + 12
    s.append(box(20, y3, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 18, "四对八句：前一半是世人正在追的，后一半才是老子要的。", 8.4, INK, "middle"))
    s.append(txt(190, y3 + 34, "外面守得住，是因为里面先不争了。", 8.0, "#6E6459", "middle"))
    s.append(gold(y3 + 52, "ch33"))
    s.append('</svg>')
    return "\n".join(s)

# ============ 第三十四章 · 不主之谓大 ============
def ch34_bu_zhu_wei_da():
    W, H = 380, 618
    body, y = head(W, H, "一主，即落合；不主，方为和", "第 三 十 四 章 · 三 个 本 义",
                   "不主，故能成其大", "道是场域，不是王座。", H)
    s = [body]

    r1, r2, r3 = y + 8, y + 108, y + 208
    for cy, hh in ((r1, 96), (r2, 96), (r3, 124)):
        s.append(box(20, cy, 340, hh, fill="#FBF6EC", stroke="#E6D8C2"))

    # ---- 一、主＝灯中火主 ----
    s.append(f'<line x1="44" y1="{r1+70}" x2="76" y2="{r1+70}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<path d="M60,{r1+70} l-6,-8 l12,0 z" fill="#E9DFCC" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M60,{r1+40} q5,7 0,12 q-5,-5 0,-12 z" fill="{SEAL}" stroke="{SEAL}" stroke-width="0.6"/>')
    for fy in (r1 + 34, r1 + 46, r1 + 58):
        s.append(f'<line x1="104" y1="{fy}" x2="66" y2="{r1+46}" stroke="#C9B79A" stroke-width="0.8" stroke-dasharray="4 3"/>')
        s.append(f'<circle cx="107" cy="{fy}" r="2.2" fill="none" stroke="#8A7C69" stroke-width="0.7"/>')
    s.append(txt(122, r1 + 26, "主：一个中心，万物向它", 8.6, INK))
    s.append(txt(122, r1 + 42, "「主」本义是灯芯上那一点火，", 7.4, "#6E6459"))
    s.append(txt(122, r1 + 56, "一盏灯只有一个火头，光都从那儿出。", 7.4, "#6E6459"))
    s.append(txt(122, r1 + 78, "做主，就要回答谁合格、谁排第一。", 7.0, SEAL))

    # ---- 二、汎＝浮在水面 ----
    s.append(f'<path d="M34,{r2+32} q30,-8 60,0 q30,8 60,0 l0,22 q-30,-8 -60,0 q-30,8 -60,0 z" fill="#DCE5DF" stroke="#B9C7BE" stroke-width="0.8"/>')
    for i in range(3):
        s.append(f'<path d="M40,{r2+42+i*8} q22,-3 44,0 q22,3 44,0" fill="none" stroke="#9FB0A6" stroke-width="0.7"/>')
    for gx in (50, 70, 90, 112, 132):
        s.append(f'<rect x="{gx}" y="{r2+36}" width="8" height="1.5" fill="#D8B27A"/>')
    s.append(txt(160, r2 + 34, "汎：浮在水面，到处都在", 8.6, GREEN))
    s.append(txt(160, r2 + 50, "水涨它高，水落它低，贴着整个水面；", 7.4, "#6E6459"))
    s.append(txt(160, r2 + 64, "没有固定据点，也不分正路与支路。", 7.4, "#6E6459"))
    s.append(txt(160, r2 + 82, "有中心，就有等级；有等级，就是合。", 7.0, SEAL))

    # ---- 三、大＝一人张两臂 ----
    # 张臂
    s.append(f'<circle cx="62" cy="{r3+24}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="62" y1="{r3+28}" x2="62" y2="{r3+50}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M62,{r3+34} l-22,-5 M62,{r3+34} l22,-5" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M62,{r3+50} l-9,16 M62,{r3+50} l9,16" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="34" y1="{r3+24}" x2="90" y2="{r3+24}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(txt(62, r3 + 88, "张臂：量占多宽", 6.6, SEAL, "middle"))
    # 垂臂
    s.append(f'<circle cx="126" cy="{r3+24}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="126" y1="{r3+28}" x2="126" y2="{r3+50}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M126,{r3+32} l-4,18 M126,{r3+32} l4,18" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M126,{r3+50} l-9,16 M126,{r3+50} l9,16" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M104,{r3+18} q22,-16 44,0" fill="none" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="3 2"/>')
    s.append(txt(126, r3 + 88, "垂臂：怀里天地", 6.6, GREEN, "middle"))
    s.append(txt(154, r3 + 22, "「大」本是一人张开两臂的样子，", 7.4, "#6E6459"))
    s.append(txt(154, r3 + 36, "量的只是占的地方有多宽。", 7.4, "#6E6459"))
    s.append(txt(154, r3 + 56, "张开，抱住的只有一抱；", 7.6, INK))
    s.append(txt(154, r3 + 70, "垂着，怀里是整个天地。", 7.6, INK))
    s.append(txt(154, r3 + 104, "世人的大是把世界收进来，道的大是让它不必进来。", 6.8, SEAL))

    # ---- 收 ----
    y3 = r3 + 128
    s.append(box(20, y3, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 18, "功成而不名有，万物归焉而不为主。", 8.6, INK, "middle"))
    s.append(txt(190, y3 + 34, "同一个「不为主」：从它自己看是小，从万物看是大。", 7.8, "#6E6459", "middle"))
    s.append(gold(y3 + 52, "ch34"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第三十四章 · 一句两读 ============
def ch34b_yi_ju_liang_du():
    import math
    W, H = 380, 690
    body, y = head(W, H, "同一个「不为主」：从它自己看是小，从万物看是大", "第 三 十 四 章 · 同 语 异 名",
                   "一句两读：小与大", "帛书这一句写了两遍，不是抄错，是同语异名。", H)
    s = [body]

    # 经句
    s.append(box(20, y + 4, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 24, "万物归焉而弗为主", 10.4, INK, "middle", spacing="1.5"))
    s.append(txt(190, y + 46, "帛书甲、乙本：前后两处一字不差；通行本把前一处改成「衣养万物」，结构就没了。", 6.9, "#8A7C69", "middle"))

    # 中心与来归
    cx, cy, R = 190, y + 150, 92
    s.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(txt(cx, cy + 4, "不主", 7.6, "#6E6459", "middle"))
    for k in range(10):
        a = math.pi * 2 * k / 10 - math.pi / 2
        dx, dy = cx + R * math.cos(a), cy + R * math.sin(a)
        s.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="2.6" fill="none" stroke="#8A7C69" stroke-width="0.7"/>')
        ix, iy = cx + 34 * math.cos(a), cy + 34 * math.sin(a)
        s.append(f'<line x1="{dx:.1f}" y1="{dy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#C9B79A" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(txt(20, y + 116, "小", 13, GREEN))
    s.append(txt(20, y + 133, "从它自己看", 6.8, "#6E6459"))
    s.append(txt(20, y + 146, "不伸张", 6.8, "#6E6459"))
    s.append(txt(20, y + 158, "不认领", 6.8, "#6E6459"))
    s.append(txt(20, y + 170, "不做主", 6.8, "#6E6459"))
    s.append(txt(342, y + 116, "大", 13, SEAL))
    s.append(txt(342, y + 133, "从万物看", 6.8, "#6E6459", "end"))
    s.append(txt(342, y + 146, "归是真的归", 6.8, "#6E6459", "end"))
    s.append(txt(342, y + 158, "差异都进来", 6.8, "#6E6459", "end"))
    s.append(txt(342, y + 170, "不必改成一样", 6.8, "#6E6459", "end"))
    s.append(txt(190, y + 254, "归，是万物自己走过来的；主，是我伸手去管。", 7.6, "#6E6459", "middle"))

    # 两卡
    ya = y + 272
    s.append(box(20, ya, 162, 96, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(box(198, ya, 162, 96, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(32, ya + 20, "何以为小", 8.4, GREEN))
    s.append(txt(32, ya + 38, "不显、不彰、不宰、不争、不割", 7.2, "#6E6459"))
    s.append(txt(32, ya + 54, "能小，是因为它从不伸手；", 7.2, "#6E6459"))
    s.append(txt(32, ya + 68, "不伸手，才没人能握住它。", 7.2, "#6E6459"))
    s.append(txt(32, ya + 86, "形上切不开，意志上不伸张", 6.9, SEAL))
    s.append(txt(210, ya + 20, "何以为大", 8.4, SEAL))
    s.append(txt(210, ya + 38, "正因不做主，万千差异都能归来", 7.2, "#6E6459"))
    s.append(txt(210, ya + 54, "大不是小之外另修的一层，", 7.2, "#6E6459"))
    s.append(txt(210, ya + 68, "是小自己长出来的结果。", 7.2, "#6E6459"))
    s.append(txt(210, ya + 86, "往大里做，越做越窄", 6.9, SEAL))

    # 恒无欲
    yb = ya + 108
    s.append(box(20, yb, 340, 92, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, yb + 15, "「欲」本书读作发心、志求：从谷从欠——谷能容能纳，欠有所向往。", 7.2, INK))
    s.append(txt(32, yb + 30, "它是中性的那股力，不是后世窄化的贪念。", 7.2, "#6E6459"))
    s.append(txt(32, yb + 48, "第三章所戒，是攀缘之欲：依附外标而生的求。", 7.2, "#6E6459"))
    s.append(txt(32, yb + 66, "本章「恒无欲」：不是把欲掐掉，是那一念从不把场填满、锁死——", 6.9, SEAL))
    s.append(txt(32, yb + 80, "不改造、不统一、不主宰、不占有，那一支从来不发作。", 6.9, SEAL))
    # 谷：两坡夹一容，向往一点
    s.append(f'<path d="M264,{yb+14} L282,{yb+46} L300,{yb+14}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="282" cy="{yb+40}" r="2.4" fill="{SEAL}"/>')
    s.append(f'<line x1="282" y1="{yb+34}" x2="282" y2="{yb+18}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    s.append(txt(282, yb + 62, "谷能容，欠向往", 6.2, "#8A7C69", "middle"))
    s.append(txt(282, yb + 76, "一股中性的力", 6.2, SEAL, "middle"))

    # 收
    yc = yb + 104
    s.append(box(20, yc, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yc + 18, "世人求大，是往大里做；道之大，是往小里做出来的。", 8.4, INK, "middle"))
    s.append(txt(190, yc + 34, "「大」本是一人张两臂：张开只抱一抱，垂着怀里是整个天地。", 7.4, "#6E6459", "middle"))
    s.append(gold(yc + 52, "ch34b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十五章 · 执与场 ============
def ch35a_zhi_yu_chang():
    W, H = 380, 618
    body, y = head(W, H, "宾语一换，手就转向：一个向外扣，一个向内捧", "第 三 十 五 章 · 执 与 场",
                   "执大象，天下往", "图可以挂起来，场只能站进去。", H)
    s = [body]

    s.append(box(20, y + 4, 340, 28, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 23, "执大象，天下往。往而不害，安平泰。", 9.4, INK, "middle"))

    # 一、两只手
    a = y + 46
    s.append(box(20, a, 162, 108, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(box(198, a, 162, 108, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, a + 18, "执罪人：向外扣", 8.2, SEAL))
    s.append(txt(210, a + 18, "执中：向内捧", 8.2, GREEN))
    # 左手扣住一个小人
    s.append(f'<line x1="76" y1="{a+34}" x2="76" y2="{a+48}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="52" y="{a+46}" width="48" height="9" rx="4" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    for i in range(4):
        s.append(f'<line x1="{58+i*10}" y1="{a+55}" x2="{58+i*10}" y2="{a+68}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="76" cy="{a+78}" r="4.4" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="76" y1="{a+82}" x2="76" y2="{a+92}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(36, a + 100, "手形自带一个被抓的人", 6.8, "#8A7C69"))
    # 右手捧着一个「己」
    s.append(f'<path d="M220,{a+84} q6,-14 14,-16" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M256,{a+84} q-6,-14 -14,-16" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="238" cy="{a+62}" r="7" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(238, a + 65, "己", 6.4, GREEN, "middle"))
    s.append(txt(214, a + 100, "捧住的是自己，不是别人", 6.8, "#8A7C69"))

    # 二、场与门槛
    b = a + 116
    s.append(box(20, b, 340, 132, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, b + 18, "场：不是挂起来的图，是站进去的地方", 8.4, INK))
    s.append(f'<circle cx="108" cy="{b+76}" r="38" fill="#F7F1E3" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="5 3"/>')
    s.append(f'<circle cx="108" cy="{b+64}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M108,{b+68} l0,16 M108,{b+72} l-9,8 M108,{b+72} l9,8 M108,{b+84} l-7,10 M108,{b+84} l7,10" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(108, b + 124, "人站在里面", 6.8, "#6E6459", "middle"))
    # 图：画框挂着
    s.append(f'<rect x="188" y="{b+30}" width="46" height="34" fill="#F7F1E3" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M211,{b+30} l0,-10" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<circle cx="211" cy="{b+18}" r="2" fill="{INK}"/>')
    s.append(f'<line x1="192" y1="{b+56}" x2="230" y2="{b+36}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(211, b + 78, "图：可以挂起来", 6.8, "#8A7C69", "middle"))
    # 手伸出去成门槛
    s.append(f'<line x1="146" y1="{b+76}" x2="176" y2="{b+76}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<line x1="168" y1="{b+70}" x2="168" y2="{b+82}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(160, b + 96, "手一伸，场变门槛", 6.9, SEAL))
    s.append(txt(246, b + 108, "进门第一件事，先量你合不合尺寸。", 7.0, "#6E6459"))
    s.append(txt(246, b + 122, "不伸手的场，才容得下你的样子。", 7.0, "#6E6459"))

    # 三、安平泰
    c = b + 144
    s.append(box(20, c, 340, 72, fill="#F7F1E3", stroke="#E6D8C2"))
    # 安：宀下有人
    s.append(f'<path d="M46,{c+34} l14,-12 l14,12" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="60" cy="{c+40}" r="3.4" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="60" y1="{c+44}" x2="60" y2="{c+54}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(60, c + 66, "安：有地方待", 6.6, "#6E6459", "middle"))
    # 平：差异无压
    s.append(f'<rect x="142" y="{c+26}" width="14" height="22" fill="#E9DFCC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<rect x="166" y="{c+34}" width="14" height="14" fill="#E9DFCC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="138" y1="{c+48}" x2="184" y2="{c+48}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(txt(160, c + 66, "平：没人压你", 6.6, "#6E6459", "middle"))
    # 泰：气通
    s.append(f'<path d="M242,{c+30} l0,18 M262,{c+30} l0,18" stroke="{INK}" stroke-width="0.8"/>')
    s.append(arrow(238, c + 40, 268, c + 40, GREEN, 0.9, head="arrS"))
    s.append(txt(253, c + 66, "泰：气走得通", 6.6, "#6E6459", "middle"))
    s.append(txt(20, c + 84, "三字连起来：不是大家都一样，是大家都不用改。", 7.4, SEAL))

    # 收
    y3 = c + 100
    s.append(box(20, y3, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "往，是自己走过去；不是被收拢，不是低头。", 8.2, INK, "middle"))
    s.append(txt(190, y3 + 32, "手一松，场就开了；场一开，人自己会来。", 7.8, "#6E6459", "middle"))
    s.append(gold(y3 + 48, "ch35a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十五章 · 淡 ============
def ch35b_dan_bai_shui():
    W, H = 380, 556
    body, y = head(W, H, "加味的抓人，无味的养人", "第 三 十 五 章 · 味",
                   "道之出口，淡乎其无味", "整章都在饭桌上：饵是饼，味是滋味，淡是薄味。", H)
    s = [body]

    s.append(box(20, y + 4, 340, 28, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 23, "乐与饵，过客止。道之出口，淡乎其无味。", 9.0, INK, "middle"))

    a = y + 44
    s.append(box(20, a, 162, 116, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(box(198, a, 162, 116, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, a + 18, "乐与饵：有味的", 8.2, SEAL))
    s.append(txt(210, a + 18, "道：一碗白水", 8.2, GREEN))
    # 饼与钩
    s.append(f'<circle cx="60" cy="{a+48}" r="17" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    for i in range(3):
        s.append(f'<line x1="{50+i*8}" y1="{a+40}" x2="{52+i*8}" y2="{a+46}" stroke="#8A7C69" stroke-width="0.6"/>')
    s.append(f'<path d="M60,{a+65} l0,10 q0,12 9,12 q8,0 8,-8" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M77,{a+79} l6,4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(96, a + 84, "鱼咬住的是钩，不是饼", 6.8, "#6E6459"))
    s.append(txt(32, a + 100, "饵能让人停，不能让人留。", 7.0, "#6E6459"))
    s.append(txt(32, a + 112, "留不住的，本来就不是你的。", 7.0, "#6E6459"))
    # 白水碗
    s.append(f'<path d="M222,{a+42} q16,30 32,0" fill="#EEF2EE" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="218" y1="{a+42}" x2="258" y2="{a+42}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M225,{a+50} q13,5 24,0" fill="none" stroke="#9FB0A6" stroke-width="0.8"/>')
    s.append(txt(238, a + 64, "淡", 9.0, GREEN, "middle"))
    s.append(txt(272, a + 50, "没味，", 6.8, "#6E6459"))
    s.append(txt(272, a + 62, "离不开", 6.8, "#6E6459"))
    s.append(txt(210, a + 88, "甜饼吃三块就腻；白水喝一辈子不腻。", 6.9, "#6E6459"))
    s.append(txt(210, a + 104, "加味的抓人，无味的养人。", 7.4, SEAL))

    # 过客
    b = a + 128
    s.append(box(20, b, 340, 74, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(32, b + 18, "过客止：客是「寄也」——歇脚，不是归", 8.4, INK))
    s.append(f'<line x1="40" y1="{b+62}" x2="150" y2="{b+62}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<circle cx="88" cy="{b+34}" r="3.6" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="88" y1="{b+38}" x2="88" y2="{b+52}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M88,{b+52} l-5,10 M88,{b+52} l5,10" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="104" y="{b+32}" width="18" height="30" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')

    s.append(txt(134, b + 46, "他没有把这儿当家，只是吃了一口饼；客总是要走的。", 6.9, "#6E6459"))
    s.append(txt(134, b + 62, "执大象的场里，来的人不是客——那儿没有主客之分。", 6.9, GREEN))

    # 三不足
    c = b + 86
    for i, (k, t) in enumerate((("视之不足见", "没有形状，没法照着画"), ("听之不足闻", "没有声调，没法跟着喊"), ("用之不足既", "没有底，所以用不完"))):
        bx = 20 + i * 116
        s.append(box(bx, c, 108, 68, fill="#FBF6EC", stroke="#E6D8C2"))
        s.append(txt(bx + 54, c + 18, k, 7.6, INK, "middle"))
        s.append(txt(bx + 54, c + 36, t, 6.6, "#6E6459", "middle"))
        s.append(txt(bx + 54, c + 56, ["不见其形", "不闻其声", "不见其底"][i], 6.4, SEAL, "middle"))
    # 收
    y3 = c + 80
    s.append(box(20, y3, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "能被人一眼看尽的，用不了几回；用不完的，从来看不尽。", 8.2, INK, "middle"))
    s.append(txt(190, y3 + 32, "真正靠得住的东西，都不加味。", 7.6, "#6E6459", "middle"))
    s.append(gold(y3 + 48, "ch35b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十六章 · 四对节律 ============
def ch36a_si_dui_jie_lv():
    W, H = 380, 536
    body, y = head(W, H, "「固」是必然如此，不是「你就这样办」", "第 三 十 六 章 · 四 对",
                   "四对：一张一阖", "看清节律的人有两种：一种跟着走，一种拿它下套。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 18, "将欲歙之，必固张之；将欲弱之，必固强之；", 7.4, INK, "middle"))
    s.append(txt(190, y + 34, "将欲废之，必固兴之；将欲取之，必固与之。", 7.4, INK, "middle"))

    cells = [(20, y + 50), (198, y + 50), (20, y + 186), (198, y + 186)]
    for cx, cy in cells:
        s.append(box(cx, cy, 162, 126, fill="#FBF6EC", stroke="#E6D8C2"))

    c1, c2 = y + 50, y + 186
    # 一 歙/张：弓与呼
    s.append(txt(32, c1 + 18, "歙 / 张：一口气", 8.2, SEAL))
    s.append(f'<path d="M48,{c1+38} Q68,{c1+62} 48,{c1+86}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="44" y1="{c1+38}" x2="44" y2="{c1+86}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(62, c1 + 52, 92, c1 + 44, SEAL, 0.9, head="arrS"))
    s.append(txt(100, c1 + 52, "上弦之后必放", 6.8, "#6E6459"))
    s.append(txt(32, c1 + 100, "吸气之后必呼，上弦之后必放。", 7.0, INK))
    s.append(txt(32, c1 + 114, "你要收，是因为它已经张满了。", 6.9, SEAL))

    # 二 弱/强：曲枝与绷弦
    s.append(txt(210, c1 + 18, "弱 / 强：能弯的不折", 8.2, GREEN))
    s.append(f'<path d="M216,{c1+80} Q236,{c1+44} 256,{c1+80}" fill="none" stroke="{GREEN}" stroke-width="1.3"/>')
    s.append(f'<line x1="268" y1="{c1+42}" x2="292" y2="{c1+42}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M268,{c1+42} l-6,-4 M292,{c1+42} l6,-4" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(280, c1 + 56, "绷到断", 6.6, SEAL, "middle"))
    s.append(txt(210, c1 + 100, "弱是桡：一根能弯的枝；", 7.0, INK))
    s.append(txt(210, c1 + 114, "强是弦绷紧。弯的不断，绷的会断。", 6.9, SEAL))

    # 三 废/兴：塌屋与众手
    s.append(txt(32, c2 + 18, "废 / 兴：众手与撤手", 8.2, SEAL))
    s.append(f'<rect x="38" y="{c2+56}" width="36" height="24" fill="none" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<path d="M34,{c2+56} l10,-10 l12,8 l14,-12" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M40,{c2+84} l26,-8" stroke="{INK}" stroke-width="0.9" stroke-dasharray="4 3"/>')
    s.append(txt(38, c2 + 96, "屋塌：不用人管", 6.4, "#6E6459"))
    s.append(f'<rect x="118" y="{c2+52}" width="26" height="18" fill="#E9DFCC" stroke="{INK}" stroke-width="0.8"/>')
    for dx in (-14, -4, 8, 18):
        s.append(arrow(131 + dx, c2 + 84, 131 + dx, c2 + 72, GREEN, 0.7, head="arrS"))
    s.append(txt(131, c2 + 96, "四手共举", 6.4, GREEN, "middle"))
    s.append(txt(32, c2 + 114, "举起来要合力，塌下去不用人管。", 6.9, SEAL))

    # 四 取/与：割耳与给饼
    s.append(txt(210, c2 + 18, "取 / 与：拿与给", 8.2, GREEN))
    s.append(f'<circle cx="220" cy="{c2+48}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M228,{c2+48} l16,0" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M244,{c2+44} l0,6 M244,{c2+50} l0,6" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(250, c2 + 50, "取：从别人身上拿", 6.4, "#6E6459"))
    s.append(f'<circle cx="238" cy="{c2+74}" r="8" fill="#E9DFCC" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M220,{c2+86} q14,-3 24,-1" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M244,{c2+85} l4,2 l-4,2" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(210, c2 + 100, "给出去的，都在等着被取。", 6.7, SEAL))
    s.append(txt(210, c2 + 112, "给是给，取是拿，两件事。", 6.4, "#6E6459"))

    # 固 与 收
    y3 = y + 324
    s.append(box(20, y3, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 18, "「固」＝必然如此：说这话的是观天的人。", 8.2, INK, "middle"))
    s.append(txt(190, y3 + 34, "若读成「你就这样办」，就成了下棋的人——同一句，两条路。", 7.4, "#6E6459", "middle"))
    s.append(gold(y3 + 52, "ch36a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十六章 · 微明与渊 ============
def ch36b_wei_ming_yuan():
    import math
    W, H = 380, 592
    body, y = head(W, H, "胜，本义是「任」：刚撑不住自己，柔撑得住", "第 三 十 六 章 · 微 明",
                   "微明 · 渊 · 利器", "看得见的人很多，看得见而不动声色的人很少。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 28, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 21, "是谓微明。柔弱胜刚强。鱼不可脱于渊，国之利器不可以示人。", 7.6, INK, "middle"))

    # 一、微明：拐点未显 + 胜＝任
    a = y + 38
    s.append(box(20, a, 340, 118, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, a + 18, "微明：拐点还没显出来", 8.2, INK))
    s.append(f'<path d="M40,{a+64} Q64,{a+68} 88,{a+38} Q102,{a+22} 116,{a+36} Q132,{a+54} 160,{a+62}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="104" cy="{a+30}" r="2.4" fill="{SEAL}"/>')
    s.append(f'<line x1="102" y1="{a+32}" x2="102" y2="{a+54}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(txt(104, a + 74, "顶点之前，已经有信", 6.2, SEAL))
    # 胜＝任：直梁断 / 弯梁承
    s.append(f'<line x1="200" y1="{a+50}" x2="270" y2="{a+50}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<path d="M232,{a+50} l-3,4 M236,{a+50} l3,-4" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(235, a + 40, "直：撑不住", 6.6, SEAL, "middle"))
    s.append(f'<path d="M200,{a+86} Q235,{a+62} 270,{a+86}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(txt(235, a + 102, "弯：承得住", 6.6, GREEN, "middle"))
    s.append(txt(304, a + 70, "任", 12, GREEN, "middle"))
    s.append(txt(304, a + 84, "胜＝任", 6.2, "#6E6459", "middle"))
    s.append(txt(32, a + 100, "柔不打败刚；刚没有自己站住的地方。", 6.9, INK))
    s.append(txt(32, a + 112, "微不是细小，是没有行迹。", 6.9, "#6E6459"))

    # 二、渊与鱼
    b = a + 130
    s.append(box(20, b, 340, 120, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(32, b + 18, "渊：回水，看不见底", 8.2, INK))
    s.append(f'<circle cx="82" cy="{b+58}" r="32" fill="#DCE5DF" stroke="#B9C7BE" stroke-width="0.8"/>')
    for r in (24, 17, 10):
        s.append(f'<circle cx="82" cy="{b+58}" r="{r}" fill="none" stroke="#9FB0A6" stroke-width="0.5" stroke-dasharray="4 3"/>')
    s.append(f'<ellipse cx="82" cy="{b+58}" rx="9" ry="4" fill="#F7F1E3" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M91,{b+58} l7,-4 l0,8 z" fill="#F7F1E3" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(82, b + 104, "在渊：有地方转", 6.6, GREEN, "middle"))
    s.append(f'<line x1="160" y1="{b+96}" x2="330" y2="{b+96}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<ellipse cx="212" cy="{b+88}" rx="10" ry="4.4" fill="#F7F1E3" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<path d="M222,{b+88} l8,-4 l0,8 z" fill="#F7F1E3" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<path d="M206,{b+82} l-4,-6 M212,{b+81} l0,-7 M218,{b+82} l4,-6" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(212, b + 112, "脱渊：鳃里进沙", 6.6, SEAL, "middle"))
    s.append(txt(170, b + 40, "不是被捉走，是自己跳上岸。", 6.9, INK))
    s.append(txt(170, b + 54, "鱼是「有」，渊是「无」；", 6.4, "#6E6459"))
    s.append(txt(170, b + 66, "本事全长在那片「无」上。", 6.4, "#6E6459"))

    # 三、利器
    c = b + 132
    s.append(box(20, c, 340, 76, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, c + 18, "利器：刀可以挂在墙上", 8.2, GREEN))
    s.append(f'<line x1="40" y1="{c+34}" x2="140" y2="{c+34}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<path d="M76,{c+34} l0,6" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<rect x="75" y="{c+34}" width="6" height="8" fill="#E9DFCC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M74,{c+42} l9,-1 l1,30 l-8,1 z" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(96, c + 54, "挂起来：看得见，但不随手", 6.4, "#6E6459"))
    s.append(txt(196, c + 18, "不能挂在嘴上", 8.2, SEAL))
    s.append(f'<path d="M206,{c+52} q16,-9 32,0" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M206,{c+52} q16,9 32,0" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="222" y1="{c+26}" x2="222" y2="{c+44}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M222,{c+44} l-4,-5 l8,0 z" fill="{SEAL}" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(f'<circle cx="222" cy="{c+36}" r="13" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<line x1="211" y1="{c+47}" x2="233" y2="{c+25}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(246, c + 54, "说出来就成了刀", 6.4, "#6E6459"))

    y3 = c + 88
    s.append(box(20, y3, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "藏刀不是为了让你不知道有刀，是为了让你不必怕刀。", 8.0, INK, "middle"))
    s.append(txt(190, y3 + 32, "这一问，就把本章和权术分开了。", 7.6, "#6E6459", "middle"))
    s.append(gold(y3 + 48, "ch36b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十七章 · 手与象 ============
def ch37a_wei_shou_xiang():
    W, H = 380, 484
    body, y = head(W, H, "无为撤掉的不是事，是那只手", "第 三 十 七 章 · 为",
                   "手牵象，与自化", "「为」从爪从象：一只手在上，一只象在下。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 18, "道常无为而无不为。侯王若能守之，万物将自化。", 7.6, INK, "middle"))
    s.append(txt(190, y + 30, "化而欲作，吾将镇之以无名之朴。", 7.2, "#6E6459", "middle"))

    a = y + 44
    s.append(box(20, a, 162, 122, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(box(198, a, 162, 122, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, a + 18, "为：爪在象上", 8.2, SEAL))
    s.append(txt(210, a + 18, "无为：手撤了", 8.2, GREEN))

    # 象（左）
    s.append(f'<ellipse cx="80" cy="{a+76}" rx="23" ry="13" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="104" cy="{a+66}" r="8.5" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M98,{a+62} q-4,-7 3,-8 q4,0 4,6" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M110,{a+70} q7,9 2,18 q-2,4 1,6" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="108" y1="{a+74}" x2="115" y2="{a+76}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<circle cx="106" cy="{a+64}" r="0.9" fill="{INK}"/>')
    for lx in (64, 74, 86, 95):
        s.append(f'<line x1="{lx}" y1="{a+88}" x2="{lx}" y2="{a+100}" stroke="{INK}" stroke-width="0.9"/>')
    # 手＋绳
    s.append(f'<path d="M72,{a+32} q7,-5 14,-1" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<path d="M74,{a+33} l0,7 M79,{a+33} l0,7 M85,{a+34} l0,7" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<path d="M79,{a+40} q14,12 22,22" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(32, a + 110, "手一动，象才动。", 6.9, "#6E6459"))
    # 象（右，无人牵）
    s.append(f'<ellipse cx="252" cy="{a+76}" rx="23" ry="13" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="276" cy="{a+66}" r="8.5" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M270,{a+62} q-4,-7 3,-8 q4,0 4,6" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M282,{a+70} q7,9 2,18 q-2,4 1,6" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="280" y1="{a+74}" x2="287" y2="{a+76}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<circle cx="278" cy="{a+64}" r="0.9" fill="{INK}"/>')
    for lx in (236, 246, 258, 267):
        s.append(f'<line x1="{lx}" y1="{a+88}" x2="{lx}" y2="{a+100}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M236,{a+38} q14,4 26,-2" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    s.append(txt(238, a + 30, "绳落在地上", 6.2, SEAL))
    s.append(arrow(222, a + 62, 206, a + 56, GREEN, 0.8, head="arrS"))
    s.append(txt(210, a + 110, "象照走：撤的不是事，是手。", 6.9, "#6E6459"))

    # 化 / 自化
    b = a + 134
    s.append(box(20, b, 340, 96, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(32, b + 18, "化：路是别人指的", 8.2, SEAL))
    s.append(txt(200, b + 18, "自化：方向从内起", 8.2, GREEN))
    for cx, col in ((58, INK), (150, INK), (238, GREEN), (300, GREEN)):
        s.append(f'<circle cx="{cx}" cy="{b+50}" r="4" fill="none" stroke="{col}" stroke-width="0.9"/>')
        s.append(f'<line x1="{cx}" y1="{b+54}" x2="{cx}" y2="{b+68}" stroke="{col}" stroke-width="0.9"/>')
        s.append(f'<path d="M{cx},{b+68} l-4,8 M{cx},{b+68} l4,8" stroke="{col}" stroke-width="0.8"/>')
    s.append(arrow(66, b + 48, 138, b + 48, SEAL, 0.9, head="arrS"))
    s.append(txt(102, b + 42, "教", 7.0, SEAL, "middle"))
    s.append(txt(104, b + 92, "「化」本带一个「教」：方向由外给。", 6.7, "#6E6459", "middle"))
    for r in (6, 11):
        s.append(f'<path d="M{300-r},{b+50} a{r},{r} 0 0 1 {2*r},0" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(300, b + 30, "自", 8.0, GREEN, "middle"))
    s.append(txt(300, b + 92, "加一个「自」：同一条路，掉头走。", 6.7, "#6E6459", "middle"))

    y3 = b + 108
    s.append(box(20, y3, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "「为」是那只牵着象的手：象的每一步，都算在它身上。", 7.6, INK, "middle"))
    s.append(txt(190, y3 + 32, "无为：手拿开，象自己走——事一件没少。", 7.6, "#6E6459", "middle"))
    s.append(gold(y3 + 48, "ch37a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十七章 · 朴与静 ============
def ch37b_pu_yu_jing():
    W, H = 380, 592
    body, y = head(W, H, "用刀压人，人会反弹；用木压火，火会自己熄", "第 三 十 七 章 · 朴",
                   "朴 · 静 · 自正", "那块木头没上漆、没雕花、没有名字。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 18, "化而欲作，吾将镇之以无名之朴。", 7.8, INK, "middle"))
    s.append(txt(190, y + 30, "不欲以静，天下将自正。", 7.4, "#6E6459", "middle"))

    # 一、木压火 / 刀压人
    a = y + 44
    s.append(box(20, a, 340, 118, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, a + 18, "镇：一块原木，不加一文", 8.2, INK))
    s.append(f'<rect x="44" y="{a+62}" width="70" height="16" rx="2" fill="#E9DFCC" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="52" y1="{a+68}" x2="108" y2="{a+66}" stroke="#8A7C69" stroke-width="0.5"/>')
    s.append(f'<line x1="52" y1="{a+74}" x2="106" y2="{a+73}" stroke="#8A7C69" stroke-width="0.5"/>')
    for fx, hh in ((46, 16), (113, 13)):
        s.append(f'<path d="M{fx},{a+98} q-6,{-hh/2} 0,{-hh} q6,{hh/2} 0,{hh} z" fill="#EFD9CE" stroke="{SEAL}" stroke-width="0.9"/>')
    for ex in (58, 66, 98):
        s.append(f'<circle cx="{ex}" cy="{a+96}" r="1.2" fill="{SEAL}" opacity="0.7"/>')
    s.append(f'<line x1="38" y1="{a+98}" x2="74" y2="{a+94}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="52" y1="{a+94}" x2="116" y2="{a+98}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(40, a + 58, "没上漆、没雕花、没名字", 6.4, "#6E6459"))
    s.append(txt(126, a + 92, "火不靠扑，靠断柴", 6.8, GREEN))
    # 刀压人
    s.append(f'<circle cx="214" cy="{a+78}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="214" y1="{a+82}" x2="214" y2="{a+96}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="208" y1="{a+62}" x2="222" y2="{a+58}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<line x1="222" y1="{a+58}" x2="232" y2="{a+56}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(arrow(214, a + 62, 214, a + 52, SEAL, 0.8, head="arrS"))
    s.append(txt(232, a + 74, "刀压：越压越弹", 6.4, SEAL))
    s.append(txt(32, a + 110, "「镇」不是压服，是压住那股要起的劲。", 6.9, "#6E6459"))

    # 二、静与驰
    b = a + 130
    s.append(box(20, b, 340, 110, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(32, b + 18, "静：心不往外扯", 8.2, GREEN))
    s.append(txt(200, b + 18, "驰：人坐着，心在跑", 8.2, SEAL))
    s.append(f'<line x1="40" y1="{b+72}" x2="150" y2="{b+72}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<circle cx="86" cy="{b+46}" r="4" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="86" y1="{b+50}" x2="86" y2="{b+66}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M86,{b+66} l-8,6 M86,{b+66} l8,6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M80,{b+72} l-3,3 M92,{b+72} l3,3" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(86, b + 102, "忙，也静", 6.6, GREEN, "middle"))
    s.append(f'<circle cx="240" cy="{b+66}" r="4" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="240" y1="{b+70}" x2="240" y2="{b+84}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M236,{b+84} l-8,8 M236,{b+84} l14,8" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M244,{b+58} q26,-20 52,-6" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    s.append(arrow(280, b + 46, 300, b + 54, SEAL, 0.7, head="arrS"))
    s.append(txt(240, b + 102, "坐，也躁", 6.6, SEAL, "middle"))
    s.append(txt(200, b + 34, "静的反面不是动，是驰。", 6.6, "#6E6459"))

    # 三、自正
    c = b + 122
    s.append(box(20, c, 340, 84, fill="#FBF6EC", stroke="#E6D8C2"))
    s.append(txt(32, c + 18, "自正：各归其位", 8.2, INK))
    s.append(f'<line x1="38" y1="{c+64}" x2="150" y2="{c+64}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="86" y1="{c+64}" x2="86" y2="{c+56}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<ellipse cx="74" cy="{c+56}" rx="9" ry="5" fill="#E9DFCC" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M80,{c+52} l3,-4" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(104, c + 58, "止：脚走到该停的地方", 6.5, "#6E6459"))
    s.append(txt(190, c + 18, "定：要一个人去平", 8.2, SEAL))
    s.append(f'<line x1="188" y1="{c+64}" x2="300" y2="{c+64}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<ellipse cx="228" cy="{c+56}" rx="9" ry="5" fill="#E9DFCC" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M214,{c+46} q14,-8 28,0" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(252, c + 58, "有人按着，才叫定", 6.4, SEAL))
    s.append(txt(32, c + 78, "「正」从止：不是被纠正，是自己走到该停的那一点。", 6.6, "#6E6459"))

    y3 = c + 96
    s.append(box(20, y3, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "压住火的不是更多的柴，是把它从柴上挪开。", 7.8, INK, "middle"))
    s.append(txt(190, y3 + 32, "木头什么都没加，所以压得住。", 7.6, "#6E6459", "middle"))
    s.append(gold(y3 + 48, "ch37b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十八章 · 五级台阶 ============
def ch38_wu_ji_tai_jie():
    W, H = 380, 548
    body, y = head(W, H, "越往下，越靠作意撑；作意越重，越要强制", "第 三 十 八 章 · 滑 落",
                   "五级滑落", "不是一级一级走下去的，是一失再失滑下来的。", H)
    s = [body]

    rows = [("道", "无", "万物自化", GREEN),
            ("上德", "无以为", "有德而不自知", INK),
            ("下德", "有以为", "守德而恐失", SEAL),
            ("仁", "为之而无以为", "体恤不图报", INK),
            ("义", "为之而有以为", "带是非立场", SEAL),
            ("礼", "攘臂而扔之", "强引使从", SEAL)]

    a = y + 26
    step = 42
    w = 110
    for i, (nm, judge, mark, col) in enumerate(rows):
        bx = 26 + i * 14
        by = a + i * step
        fill = "#F6E9E2" if nm == "下德" else "#F7F1E3"
        s.append(f'<rect x="{bx}" y="{by}" width="{w}" height="30" fill="{fill}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<rect x="{bx}" y="{by}" width="3" height="30" fill="{col}"/>')
        s.append(txt(bx + 12, by + 20, nm, 8.8, col))
        s.append(txt(bx + w + 8, by + 13, judge, 6.4, col))
        s.append(txt(bx + w + 8, by + 25, mark, 5.8, "#6E6459"))
        if i < 5:
            s.append(arrow(bx + 52, by + 33, bx + 52, by + step - 4, "#C9B79A", 0.7, head="arrS"))

    y2 = a + 5 * step + 56
    s.append(txt(190, y2, "失道而后德，失德而后仁，失仁而后义，失义而后礼。", 6.4, SEAL, "middle"))

    y3 = y2 + 14
    s.append(box(20, y3, 340, 54, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "大丈夫处其厚，不居其薄；处其实，不居其华。", 7.6, INK, "middle"))
    s.append(txt(190, y3 + 33, "不是分出谁高谁低，是认出自己此刻站在第几级。", 7.0, "#6E6459", "middle"))
    s.append(txt(190, y3 + 47, "压住滑落的，不是往上爬，是不再加那层作意。", 6.6, SEAL, "middle"))
    s.append(gold(y3 + 64, "ch38"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十九章 · 六得一无以 ============
def ch39a_liu_de_yi():
    W, H = 380, 448
    body, y = head(W, H, "得一不是得到什么，是不丢什么", "第 三 十 九 章 · 得 一",
                   "六样东西，各自不裂", "六种整全，不是一种整全。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "昔之得一者：天得一以清，地得一以宁，神得一以灵，", 6.4, INK, "middle"))
    s.append(txt(190, y + 29, "谷得一以盈，万物得一以生，侯王得一以为天下贞。", 6.4, INK, "middle"))

    a = y + 44
    s.append(txt(40, a, "名", 6.0, "#6E6459", "middle"))
    s.append(txt(126, a, "得一（守着的）", 6.2, GREEN, "middle"))
    s.append(txt(258, a, "无以（拿不出的）", 6.2, SEAL, "middle"))
    s.append(f'<line x1="24" y1="{a+6}" x2="338" y2="{a+6}" stroke="{INK}" stroke-width="0.7"/>')

    rows = [("天", "得一以清", "无以清，将恐", "裂"),
            ("地", "得一以宁", "无以宁，将恐", "废"),
            ("神", "得一以灵", "无以灵，将恐", "歇"),
            ("谷", "得一以盈", "无以盈，将恐", "竭"),
            ("万物", "得一以生", "无以生，将恐", "灭"),
            ("侯王", "得一以为天下贞", "无以贵高，将恐", "蹶")]
    rh = 27
    for i, (nm, got, lost, brk) in enumerate(rows):
        ry = a + 10 + i * rh
        s.append(txt(40, ry + 13, nm, 7.0, INK, "middle"))
        s.append(txt(58, ry + 13, got, 6.0, GREEN))
        s.append(txt(196, ry + 13, lost, 6.2, "#6E6459"))
        s.append(txt(330, ry + 14, brk, 9.2, SEAL, "end"))
        s.append(f'<line x1="24" y1="{ry+22}" x2="338" y2="{ry+22}" stroke="{LINE}" stroke-width="0.5"/>')

    y2 = a + 10 + 6 * rh + 8
    s.append(box(20, y2, 340, 50, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 17, "「一」不是把六样并成一样，是六样各自不裂：", 7.2, INK, "middle"))
    s.append(txt(190, y2 + 31, "天得天的整全，地得地的整全，各清、各宁、各灵、各盈、各生、各贞。", 6.6, "#6E6459", "middle"))
    s.append(txt(190, y2 + 44, "「得一」的反面不是「不得」，是「无以」——不是没得到，是拿不出了。", 6.4, SEAL, "middle"))
    s.append(gold(y2 + 62, "ch39a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第三十九章 · 底下的三只脚 ============
def ch39b_di_xia_san_zhi_jiao():
    W, H = 380, 612
    body, y = head(W, H, "一切立着的东西，都靠一个不显眼的部分立着", "第 三 十 九 章 · 托 底",
                   "底下那三只脚", "整全不在明面上。", H)
    s = [body]

    y0 = y + 10
    # 一、鼎
    s.append(txt(24, y0 + 10, "一 · 鼎：贵的那一头，靠贱的那一头立着", 6.6, INK))
    dx, dy = 74, y0 + 26
    s.append(f'<ellipse cx="{dx}" cy="{dy+34}" rx="40" ry="24" fill="#F2EADA" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{dx-28},{dy+14} L{dx-28},{dy+2} L{dx-18},{dy+2}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M{dx+28},{dy+14} L{dx+28},{dy+2} L{dx+18},{dy+2}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    for lx in (dx - 22, dx, dx + 22):
        s.append(f'<line x1="{lx}" y1="{dy+56}" x2="{lx}" y2="{dy+70}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(txt(dx, dy + 38, "贵 · 高", 6.4, SEAL, "middle"))
    s.append(txt(dx, dy + 82, "贱 · 下（三只短足）", 5.8, "#6E6459", "middle"))
    s.append(txt(150, dy + 6, "三千斤的鼎，站在三只短短的脚上。", 6.4, INK))
    s.append(txt(150, dy + 20, "足一断，腹立刻塌；腹越重，塌得越彻底。", 6.4, INK))
    s.append(txt(150, dy + 34, "越重的东西，落地的那一部分越小、越不起眼，", 6.2, "#6E6459"))
    s.append(txt(150, dy + 46, "也从来不写进铭文。", 6.2, "#6E6459"))
    s.append(txt(150, dy + 64, "故贵以贱为本，高以下为基。", 6.8, SEAL))

    # 二、车厢
    y1 = y0 + 136
    s.append(txt(24, y1, "二 · 舆：数遍零件，数不出那个空位", 6.6, INK))
    cx, cy = 84, y1 + 44
    s.append(f'<rect x="{cx-34}" y="{cy-26}" width="68" height="34" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx-34}" y1="{cy-26}" x2="{cx+34}" y2="{cy-26}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<rect x="{cx-20}" y="{cy-20}" width="40" height="22" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="5 4"/>')
    s.append(txt(cx, cy - 7, "空位", 6.0, SEAL, "middle"))
    s.append(f'<circle cx="{cx-18}" cy="{cy+18}" r="12" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="{cx-18}" cy="{cy+18}" r="3" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="{cx+34}" y1="{cy+4}" x2="{cx+62}" y2="{cy+4}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{cx-34}" y1="{cy+8}" x2="{cx+34}" y2="{cy+8}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(cx - 18, cy + 36, "轮", 5.4, "#6E6459", "middle"))
    s.append(txt(cx + 48, cy + 14, "辕", 5.4, "#6E6459", "middle"))
    s.append(txt(cx - 28, cy + 2, "辐", 5.4, "#6E6459"))
    s.append(txt(150, cy - 22, "「舆」是车厢——装人的那个空位，不是车轮车辕。", 6.4, INK))
    s.append(txt(150, cy - 8, "轮、轴、辕、辐，数得再准，也数不出那个空位；", 6.4, INK))
    s.append(txt(150, cy + 6, "空位不在零件里。这就是「数舆无舆」。", 6.4, INK))
    s.append(txt(150, cy + 22, "分析能把「有」拆到极细，拆不出「无」。", 6.2, "#6E6459"))
    s.append(txt(150, cy + 40, "数得清的是零件，数不清的才是那辆车。", 6.8, SEAL))

    # 三、玉与石
    y2 = y1 + 132
    s.append(txt(24, y2, "三 · 玉与石：一块要借光，一块不用", 6.6, INK))
    gy, gx = y2 + 50, 60
    s.append(f'<ellipse cx="{gx}" cy="{gy}" rx="16" ry="12" fill="#F2EADA" stroke="{INK}" stroke-width="0.9"/>')
    for ang in (-70, -35, 0, 35, 70, -100, 110):
        import math
        a1 = math.radians(ang)
        s.append(f'<line x1="{gx+18*math.cos(a1):.1f}" y1="{gy+14*math.sin(a1):.1f}" '
                 f'x2="{gx+25*math.cos(a1):.1f}" y2="{gy+20*math.sin(a1):.1f}" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(gx, gy + 26, "玉 · 琭琭", 5.6, SEAL, "middle"))
    sx = 118
    s.append(f'<path d="M{sx-14},{gy-6} L{sx-4},{gy-14} L{sx+10},{gy-8} L{sx+14},{gy+4} L{sx+4},{gy+13} L{sx-12},{gy+8} Z" fill="#E6D8C2" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(sx, gy + 26, "石 · 珞珞（字从玉）", 5.6, "#6E6459", "middle"))
    s.append(txt(150, gy - 22, "「琭琭」不是玉，是玉的光；光要照，照的人一走就没了。", 6.2, INK))
    s.append(txt(150, gy - 8, "「珞」这个字本身从玉——那块石头不必去做玉。", 6.2, INK))
    s.append(txt(150, gy + 6, "玉的体面是别人给的，石的体面是自己有的。", 6.4, SEAL))
    s.append(txt(150, gy + 22, "不欲琭琭如玉，珞珞如石。", 6.6, GREEN))

    yb = y2 + 96
    s.append(box(20, yb, 340, 48, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yb + 16, "本是不动的，基是不空的；根断了树死，砖抽了墙倒。", 7.0, INK, "middle"))
    s.append(txt(190, yb + 32, "这一章不是叫人往下走，是叫人知道自己在什么上头站着。", 6.6, "#6E6459", "middle"))
    s.append(txt(190, yb + 44, "知道了，就不用怕低；不知道，才要一直往高里垫。", 6.4, SEAL, "middle"))
    s.append(gold(yb + 60, "ch39b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十章 · 一台反装的机器 ============
def ch40a_fan_zhuang_ji_qi():
    W, H = 380, 594
    body, y = head(W, H, "动力取自回环，方法取自柔曲，根基取自空位", "第 四 十 章 · 反 装",
                   "一台反装的机器", "道从不硬来。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 26, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 18, "反者，道之动；弱者，道之用。天下万物生于有，有生于无。", 6.6, INK, "middle"))

    a = y + 40
    s.append(txt(76, a, "世人的机器", 6.2, "#6E6459", "middle"))
    s.append(txt(268, a, "道的那台", 6.2, GREEN, "middle"))
    s.append(f'<line x1="24" y1="{a+6}" x2="338" y2="{a+6}" stroke="{INK}" stroke-width="0.6"/>')

    rh = 96
    # 一、动力
    r1 = a + 16
    s.append(txt(26, r1 + 6, "动", 8.0, SEAL))
    s.append(txt(26, r1 + 20, "力", 8.0, SEAL))
    for i, (lx, ly) in enumerate(((60, r1 + 44), (76, r1 + 32), (92, r1 + 20))):
        s.append(arrow(lx - 12, ly + 10, lx, ly, "#C9B79A", 0.9, head="arrS"))
    s.append(txt(84, r1 + 62, "加码：再多、再快、再强", 5.8, "#6E6459", "middle"))
    s.append(f'<circle cx="268" cy="{r1 + 34}" r="17" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<path d="M268,{r1+17} a17,17 0 1 1 -0.1,0" fill="none" stroke="{GREEN}" stroke-width="1.2"/>')
    s.append(f'<path d="M258,{r1+19} l6,-6 l6,6" fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(txt(268, r1 + 66, "回环：力不往前使，往回转", 5.8, GREEN, "middle"))

    # 二、方法
    r2 = r1 + rh
    s.append(txt(26, r2 + 6, "方", 8.0, SEAL))
    s.append(txt(26, r2 + 20, "法", 8.0, SEAL))
    s.append(f'<rect x="58" y="{r2+16}" width="42" height="16" fill="#F2EADA" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(70, r2 + 2, 70, r2 + 13, "#C9B79A", 0.8, head="arrS"))
    s.append(arrow(88, r2 + 2, 88, r2 + 13, "#C9B79A", 0.8, head="arrS"))
    s.append(f'<path d="M72,{r2+56} l5,-4 l4,4 l5,-4" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<line x1="79" y1="{r2+32}" x2="79" y2="{r2+54}" stroke="{INK}" stroke-width="1.2"/>')

    s.append(txt(84, r2 + 70, "硬顶：顶住、压住、锁住", 5.8, "#6E6459", "middle"))
    s.append(f'<path d="M232,{r2+54} C238,{r2+22} 262,{r2+14} 278,{r2+26} C292,{r2+36} 300,{r2+54} 304,{r2+58}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<circle cx="268" cy="{r2+17}" r="3" fill="{SEAL}"/>')
    s.append(txt(268, r2 + 70, "柔曲：不加在硬处，加在软处", 5.8, GREEN, "middle"))

    # 三、根基
    r3 = r2 + rh
    s.append(txt(26, r3 + 6, "根", 8.0, SEAL))
    s.append(txt(26, r3 + 20, "基", 8.0, SEAL))
    for i in range(3):
        s.append(f'<rect x="{64}" y="{r3+48-i*13}" width="32" height="11" fill="#F2EADA" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(84, r3 + 70, "堆叠：堆到没有一处空", 5.8, "#6E6459", "middle"))
    s.append(f'<rect x="238" y="{r3+22}" width="60" height="34" fill="none" stroke="{GREEN}" stroke-width="1" stroke-dasharray="6 5"/>')
    s.append(txt(268, r3 + 43, "空位", 6.2, GREEN, "middle"))
    s.append(txt(268, r3 + 70, "空位：留一个不被占据的位置", 5.8, GREEN, "middle"))

    y2 = r3 + rh + 4
    s.append(f'<line x1="24" y1="{y2}" x2="338" y2="{y2}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 8, 340, 50, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 25, "两台机器都能转；世人的那台，转到某点就卡死。", 7.0, INK, "middle"))
    s.append(txt(190, y2 + 39, "加无可加，顶无可顶，堆到没有一处空——力尽而事废。", 6.6, "#6E6459", "middle"))
    s.append(txt(190, y2 + 51, "道的那台方向相反，所以能一直转。", 6.6, SEAL, "middle"))
    s.append(gold(y2 + 68, "ch40a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十章 · 一翻二曲 ============
def ch40b_fan_yu_qu():
    W, H = 380, 540
    body, y = head(W, H, "反不是对抗，是翻转；弱不是衰弱，是柔曲", "第 四 十 章 · 翻 与 曲",
                   "一翻，二曲", "环上没有终点，只有转捩点。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "反者，道之动；弱者，道之用。", 7.4, INK, "middle"))
    s.append(txt(190, y + 27, "天下万物生于有，有生于无。", 6.6, "#6E6459", "middle"))

    # 一、环
    c1 = y + 58
    cx, cy, r = 96, c1 + 42, 38
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(cx, cy + 4, "反", 13.0, INK, "middle"))
    s.append(f'<path d="M{cx+6},{cy-r-2} l8,3 l-8,4 z" fill="{SEAL}"/>')
    s.append(f'<path d="M{cx-6},{cy+r+2} l-8,-3 l8,-4 z" fill="{GREEN}"/>')
    s.append(txt(cx, cy - r - 10, "翻过去", 5.8, SEAL, "middle"))
    s.append(txt(cx, cy + r + 14, "翻回来", 5.8, GREEN, "middle"))
    s.append(txt(160, c1 + 20, "「反」，《说文》「覆也」，从又从厂——", 6.4, INK))
    s.append(txt(160, c1 + 33, "一只手把东西翻过来。", 6.4, INK))
    s.append(txt(160, c1 + 50, "翻过去：推到顶，必向对面回转；", 6.2, "#6E6459"))
    s.append(txt(160, c1 + 63, "翻回来：从向外追的路上回头。", 6.2, "#6E6459"))
    s.append(txt(160, c1 + 80, "老子用「反」不用「返」：两件事，一条环。", 6.4, SEAL))

    # 二、曲木
    c2 = c1 + 116
    s.append(txt(24, c2, "二 · 直者易折，弯者能活", 6.6, INK))
    sx, sy = 74, c2 + 22
    s.append(f'<line x1="{sx}" y1="{sy}" x2="{sx}" y2="{sy+56}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<path d="M{sx-7},{sy+30} l7,-5 l7,5 l7,-5" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(sx, sy + 72, "直的：一动就断", 5.6, "#6E6459", "middle"))
    bx, by = 122, c2 + 22
    s.append(f'<path d="M{bx},{by+56} C{bx+4},{by+30} {bx+14},{by+22} {bx+22},{by+26} C{bx+36},{by+32} {bx+40},{by+46} {bx+46},{by+56}" fill="none" stroke="{GREEN}" stroke-width="2.2"/>')
    s.append(f'<circle cx="{bx+22}" cy="{by+18}" r="5" fill="{SEAL}"/>')
    s.append(arrow(bx + 22, by + 4, bx + 22, by + 11, "#C9B79A", 0.7, head="arrS"))
    s.append(txt(bx + 22, sy + 72, "弯的：还能弯", 5.6, GREEN, "middle"))
    s.append(txt(190, c2 + 14, "「弱」，《说文》「桡也」——曲木，", 6.4, INK))
    s.append(txt(190, c2 + 27, "木弯而不折的那个样子。", 6.4, INK))
    s.append(txt(190, c2 + 44, "直的易折，弯的能活；硬的易碎，软的能存。", 6.2, "#6E6459"))
    s.append(txt(190, c2 + 60, "绷得最紧的那一处，最先断。", 6.2, "#6E6459"))
    s.append(txt(190, c2 + 78, "弱不是没力，是把力放在能回来的地方。", 6.4, SEAL))

    yb = c2 + 104
    s.append(f'<line x1="24" y1="{yb-6}" x2="338" y2="{yb-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, yb + 2, 340, 50, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, yb + 19, "刚者求胜于一击，柔者求存于千日。", 7.6, INK, "middle"))
    s.append(txt(190, yb + 34, "一击之后无处可退，千日之后仍在场中。", 6.8, "#6E6459", "middle"))
    s.append(txt(190, yb + 47, "看懂物极必反，是为知止，不是撂手等坏。", 6.6, SEAL, "middle"))
    s.append(gold(yb + 66, "ch40b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十一章 · 三士三种边界 ============
def ch41a_san_shi():
    W, H = 380, 540
    body, y = head(W, H, "不是境界高低，是把边界当不当真", "第 四 十 一 章 · 三 士",
                   "三种边界", "三个人看同一只杯子。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "上士闻道，勤能行之；中士闻道，若存若亡；下士闻道，大笑之。", 6.6, INK, "middle"))
    s.append(txt(190, y + 29, "弗笑，不足以为道。", 6.6, SEAL, "middle"))

    a = y + 46
    # 上士
    r1 = a + 6
    s.append(txt(24, r1 + 44, "上士", 9.0, GREEN))
    for i in range(5):
        x = 68 + i * 15
        s.append(f'<path d="M{x},{r1+28} L{x+8},{r1+34} L{x},{r1+40}" fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(txt(120, r1 + 56, "绵绵不断（勤，帛书作堇）", 5.6, "#6E6459", "middle"))
    s.append(txt(190, r1 + 16, "知道那条线是自己画的，于是不照它活。", 6.4, INK))
    s.append(txt(190, r1 + 32, "他的不同不在能吃苦，在不再需要边界。", 6.2, "#6E6459"))
    s.append(txt(190, r1 + 48, "线一撤，路就通了。", 6.2, GREEN))

    # 中士
    r2 = r1 + 92
    s.append(txt(24, r2 + 44, "中士", 9.0, INK))
    s.append(f'<line x1="68" y1="{r2+34}" x2="94" y2="{r2+34}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="94" y1="{r2+34}" x2="140" y2="{r2+34}" stroke="{INK}" stroke-width="1.0" stroke-dasharray="5 5"/>')
    s.append(txt(104, r2 + 24, "信", 5.4, INK, "middle"))
    s.append(txt(133, r2 + 24, "疑", 5.4, "#6E6459", "middle"))
    s.append(txt(96, r2 + 56, "早上信，晚上疑", 5.6, "#6E6459", "middle"))
    s.append(txt(190, r2 + 16, "看见了那个空的作用，可一动手，还是照边界去动。", 6.4, INK))
    s.append(txt(190, r2 + 32, "讲的时候通，做的时候断——若存若亡。", 6.2, "#6E6459"))
    s.append(txt(190, r2 + 48, "知道边界是画的，却还是照着它活。", 6.2, INK))

    # 下士
    r3 = r2 + 92
    s.append(txt(24, r3 + 44, "下士", 9.0, SEAL))
    s.append(f'<rect x="70" y="{r3+18}" width="34" height="30" fill="#F2EADA" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(87, r3 + 37, "有", 7.0, INK, "middle"))
    s.append(txt(115, r3 + 37, "×", 8.0, SEAL))
    s.append(f'<path d="M112,{r3+50} a10,10 0 0 0 20,0" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(96, r3 + 66, "只信边界内的东西", 5.6, "#6E6459", "middle"))
    s.append(txt(190, r3 + 16, "他只认有形、有成果、有输赢、有定型。", 6.4, INK))
    s.append(txt(190, r3 + 32, "你讲虚、讲退、讲不足，他听到的不是另一层，是「没有」。", 5.9, "#6E6459"))
    s.append(txt(190, r3 + 48, "所以他笑——那不是轻慢，是真诚的不信。", 6.2, SEAL))

    y2 = r3 + 82
    s.append(box(20, y2, 340, 50, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 17, "三个人看同一只杯子：一个只看见壁，一个看见空却不敢松手，", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 31, "一个知道壁和空本来是一回事。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 45, "下士没有看错，他看的是背面。", 6.6, SEAL, "middle"))
    s.append(gold(y2 + 64, "ch41a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十一章 · 翻过来看 ============
def ch41b_fan_guo_lai():
    W, H = 380, 566
    body, y = head(W, H, "一整章十一个「如」，都在说同一件事：道难看", "第 四 十 一 章 · 翻 面",
                   "翻过来，全是反面", "不是深奥，是不好看。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "反，《说文》「覆也」，从又从厂——", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "一只手在崖上把东西翻过来；不是转身走。", 6.2, "#6E6459", "middle"))

    # 翻桌
    t = y + 52
    s.append(f'<rect x="70" y="{t+14}" width="76" height="9" fill="#F2EADA" stroke="{INK}" stroke-width="1"/>')
    for lx in (78, 138):
        s.append(f'<line x1="{lx}" y1="{t+14}" x2="{lx}" y2="{t}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M156,{t+30} a16,16 0 0 1 0,-22" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<path d="M156,{t+8} l-5,5 M156,{t+8} l5,5" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(60, t + 38, "正面", 6.2, INK, "middle"))
    s.append(txt(196, t + 12, "翻一下，正面对你的那一面，就成了反面。", 6.2, INK))
    s.append(txt(196, t + 26, "下士笑的是那个背面；老子手里握的是同一件东西。", 6.0, "#6E6459"))
    s.append(txt(196, t + 42, "他笑，是因为他站在原来那一面。", 6.2, SEAL))

    # 十一个如
    g = t + 66
    s.append(f'<line x1="24" y1="{g-10}" x2="338" y2="{g-10}" stroke="{LINE}" stroke-width="0.6"/>')
    pairs = [("明道", "昧"), ("进道", "退"), ("夷道", "颣"),
             ("上德", "谷"), ("大白", "辱"), ("广德", "不足"),
             ("建德", "偷"), ("质真", "渝"), ("大方", "无隅"),
             ("大器", "免成"), ("大音", "希声"), ("大象", "无形")]
    for i, (lft, rgt) in enumerate(pairs):
        col = i % 2
        row = i // 2
        cx = 20 + col * 168
        cy = g + row * 30
        s.append(box(cx, cy, 160, 24, fill="#F7F1E3", stroke="#E6D8C2"))
        s.append(txt(cx + 14, cy + 16, lft, 6.8, INK))
        s.append(txt(cx + 62, cy + 15, "如", 5.4, "#6E6459", "middle"))
        s.append(txt(cx + 96, cy + 16, rgt, 7.2, SEAL))
    s.append(txt(190, g + 6 * 30 + 8, "道隐无名：名字贴不住，因为它分不开。", 6.2, GREEN, "middle"))

    y2 = g + 6 * 30 + 20
    s.append(box(20, y2, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 16, "不是道难懂，是道难看；难懂可以学，难看只能翻过来看。", 7.0, INK, "middle"))
    s.append(txt(190, y2 + 31, "翻过来的东西，永远背对着站在原来那一面的人。", 6.6, "#6E6459", "middle"))
    s.append(txt(190, y2 + 44, "方到极处，是不需要角来证明自己是方的。", 6.4, GREEN, "middle"))
    s.append(gold(y2 + 60, "ch41b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十一章 · 三种看杯 ============
def ch41c_san_zhong_kan_bei():
    W, H = 380, 606
    body, y = head(W, H, "下士看见壁，就把空当作「没有」", "第 四 十 一 章 · 有 无",
                   "三种看杯", "有之以为利，无之以为用。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "上士闻道，勤能行之；中士闻道，若存若亡；下士闻道，大笑之。", 6.2, INK, "middle"))
    s.append(txt(190, y + 27, "弗笑，不足以为道。", 6.2, SEAL, "middle"))

    def cup(cx, top, h=52, half=26, wall=True, water=False, dash=False):
        stroke = INK if wall else "#C9B79A"
        d = "1" if wall else "0.7"
        out = []
        out.append(f'<path d="M{cx-half},{top} L{cx-half+7},{top+h} L{cx+half-7},{top+h} L{cx+half},{top} " '
                   f'fill="none" stroke="{stroke}" stroke-width="{d}"/>')
        out.append(f'<line x1="{cx-half+7}" y1="{top+h}" x2="{cx+half-7}" y2="{top+h}" stroke="{stroke}" stroke-width="{d}"/>')
        if dash:
            out.append(f'<ellipse cx="{cx}" cy="{top+2}" rx="{half-1}" ry="5" fill="none" stroke="{SEAL}" '
                       f'stroke-width="0.6" stroke-dasharray="4 4"/>')
        else:
            out.append(f'<ellipse cx="{cx}" cy="{top+2}" rx="{half-1}" ry="5" fill="none" stroke="{stroke}" stroke-width="{d}"/>')
        if water:
            out.append(f'<path d="M{cx-half+3},{top+20} L{cx+half-3},{top+20} L{cx+half-6},{top+h-1} '
                       f'L{cx-half+6},{top+h-1} Z" fill="#DCE6E0" stroke="none"/>')
            out.append(f'<line x1="{cx-half+3}" y1="{top+20}" x2="{cx+half-3}" y2="{top+20}" stroke="{GREEN}" stroke-width="0.7"/>')
        return "".join(out)

    # 一、下士
    r1 = y + 48
    s.append(txt(24, r1 + 14, "下士", 8.6, SEAL))
    s.append(txt(24, r1 + 28, "只看见壁", 5.8, "#6E6459"))
    s.append(cup(106, r1 + 16))
    s.append(txt(106, r1 + 38, "×", 9.0, SEAL, "middle"))
    s.append(txt(138, r1 + 26, "空＝", 5.4, SEAL))
    s.append(txt(144, r1 + 38, "「没有」", 5.4, SEAL))
    s.append(txt(170, r1 + 30, "他摸得到的是壁：有形、有成果、有输赢、有定型。", 6.2, INK))
    s.append(txt(170, r1 + 46, "壁里的那一块，他听成「不存在」。", 6.2, "#6E6459"))
    s.append(txt(170, r1 + 66, "所以他笑——笑的是那块空。", 6.4, SEAL))

    # 二、中士
    r2 = r1 + 116
    s.append(txt(24, r2 + 14, "中士", 8.6, INK))
    s.append(txt(24, r2 + 28, "看见空，不敢松手", 5.6, "#6E6459"))
    s.append(cup(106, r2 + 16, dash=True))
    s.append(txt(106, r2 + 42, "空", 6.0, SEAL, "middle"))
    s.append(f'<path d="M134,{r2+20} a12,9 0 0 1 14,4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="148" y1="{r2+24}" x2="150" y2="{r2+32}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(136, r2 + 44, "手抓着壁", 4.9, "#6E6459"))
    s.append(txt(170, r2 + 30, "他看得出空有用，可一动手，还是照着壁去动。", 6.2, INK))
    s.append(txt(170, r2 + 46, "早上信，晚上疑；讲的时候通，做的时候断。", 6.2, "#6E6459"))
    s.append(txt(170, r2 + 66, "知道了是一回事，松手是另一回事。", 6.4, INK))

    # 三、上士
    r3 = r2 + 116
    s.append(txt(24, r3 + 14, "上士", 8.6, GREEN))
    s.append(txt(24, r3 + 28, "壁空一起用", 5.8, "#6E6459"))
    s.append(cup(106, r3 + 16, water=True))
    s.append(txt(106, r3 + 44, "水", 5.6, GREEN, "middle"))
    s.append(f'<path d="M76,{r3+8} a30,10 0 0 1 60,0" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(106, r3 + 4, "一体", 5.0, GREEN, "middle"))
    s.append(txt(170, r3 + 30, "壁围出空，空盛住水；两样一起，杯才成杯。", 6.2, INK))
    s.append(txt(170, r3 + 46, "他不照那条线活，所以线一撤，路就通了。", 6.2, "#6E6459"))
    s.append(txt(170, r3 + 66, "弗笑，不足以为道：被笑，是道的常态。", 6.4, GREEN))

    y2 = r3 + 92
    s.append(box(20, y2, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 16, "下士把空当成「没有」，所以只认壁；他并没有看错——", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 31, "空不是没有，是这个器能用的那一处。", 6.8, "#6E6459", "middle"))
    s.append(txt(190, y2 + 44, "有之以为利，无之以为用。", 6.6, GREEN, "middle"))
    s.append(gold(y2 + 60, "ch41c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十一章 · 大器免成 ============
def ch41d_da_qi_mian_cheng():
    W, H = 380, 486
    body, y = head(W, H, "「晚成」把终点挪远，「免成」把终点取消", "第 四 十 一 章 · 免 成",
                   "大器免成", "不是不成器，是不封口。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "帛书本作「大器免成」；通行本作「大器晚成」。", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "「免」，脱除、除去——把「成」这件事从器上摘下来。", 6.2, SEAL, "middle"))

    a = y + 48
    # 左：晚成
    s.append(txt(24, a + 6, "通行本 · 晚成", 6.6, "#6E6459"))
    cx = 84
    top = a + 24
    s.append(f'<path d="M{cx-26},{top} L{cx-20},{top+50} L{cx+20},{top+50} L{cx+26},{top} Z" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx-27}" y1="{top-6}" x2="{cx+27}" y2="{top-6}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="{cx-27}" y1="{top-6}" x2="{cx-27}" y2="{top}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx+27}" y1="{top-6}" x2="{cx+27}" y2="{top}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="118" y1="{top+10}" x2="150" y2="{top+10}" stroke="#C9B79A" stroke-width="0.6" stroke-dasharray="6 5"/>')
    s.append(f'<line x1="150" y1="{top+2}" x2="150" y2="{top+34}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M150,{top+2} l14,4 l-14,4 z" fill="{SEAL}"/>')
    s.append(txt(157, top + 46, "终点还在", 5.2, SEAL, "middle"))
    s.append(txt(84, top + 66, "慢慢来，总会成的", 5.6, "#6E6459", "middle"))
    s.append(txt(190, a + 34, "承认「成」是终点，只把终点推远一点。", 6.2, INK))
    s.append(txt(190, a + 50, "盖还盖着，器还朝定型走。", 6.2, "#6E6459"))
    s.append(txt(190, a + 68, "这是一句安慰话。", 6.4, INK))

    # 右：免成
    b = a + 104
    s.append(txt(24, b + 6, "帛书本 · 免成", 6.6, GREEN))
    cx2 = 84
    top2 = b + 24
    s.append(f'<path d="M{cx2-26},{top2} L{cx2-20},{top2+50} L{cx2+20},{top2+50} L{cx2+26},{top2} Z" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<ellipse cx="{cx2}" cy="{top2}" rx="26" ry="5" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(f'<path d="M{cx2-14},{top2-6} a14,6 0 0 1 28,0" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    s.append(txt(cx2, top2 - 14, "口一直开着", 5.2, SEAL, "middle"))
    s.append(txt(130, top2 + 12, "成", 9.0, SEAL, "middle"))
    s.append(f'<line x1="120" y1="{top2+8}" x2="140" y2="{top2+8}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(130, top2 + 30, "免＝脱除", 5.0, "#6E6459", "middle"))
    s.append(txt(84, top2 + 58, "不封口，还留着一处在变", 5.4, GREEN, "middle"))
    s.append(txt(190, b + 34, "不往那个终点去，因为「成」就是「定型」。", 6.2, INK))
    s.append(txt(190, b + 50, "一定型，就碰上「物壮则老」：顶点后面只有下坡。", 5.9, "#6E6459"))
    s.append(txt(190, b + 68, "所以它一直留着一处没完成。", 6.4, GREEN))

    y2 = b + 100
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-8}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2, 340, 48, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 16, "「免成」不是不成器，是不封口——永远还留着一处在变。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 31, "一个「免」字和一个「善」字，把「成」分成两件事：自己的成，和让别人成。", 6.2, "#6E6459", "middle"))
    s.append(txt(190, y2 + 44, "它不给自己定型，所以能给别人留出形。", 6.6, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch41d"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十二章 · 和与合 ============
def ch42b_he_yu_ge():
    W, H = 380, 566
    body, y = head(W, H, "和是动着的不散；合是抹去那道虚", "第 四 十 二 章 · 和 合",
                   "和，不是合", "壁厚到把中空填实，器还在，用已亡。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "万物负阴而抱阳，冲气以为和。", 7.2, INK, "middle"))
    s.append(txt(190, y + 27, "负是背在背上，抱是抱在怀里：一物之内，阴在背，阳在怀。", 5.7, "#6E6459", "middle"))

    a = y + 52
    cx, r = 84, 40

    # 一、和
    s.append(txt(24, a, "一 · 和：中间那道虚还空着", 6.4, GREEN))
    cy = a + 62
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="#E6D8C2" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r-2}" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(cx, cy + 4, "阳", 8.6, GREEN, "middle"))
    s.append(f'<path d="M{cx-14},{cy+14} a18,18 0 0 1 28,-24" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<path d="M{cx+12},{cy-14} l5,3 l-6,3" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<path d="M{cx+14},{cy-14} a18,18 0 0 1 -28,24" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(f'<path d="M{cx-12},{cy+14} l-5,-3 l6,-3" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(cx, cy + r + 22, "壁＝阴（背），腔＝阳（怀）", 5.4, "#6E6459", "middle"))
    s.append(txt(150, a + 22, "阴守住成形的边界，阳保有流通的动能，二者互不吞并。", 6.1, INK))
    s.append(txt(150, a + 40, "靠的正是中间那道虚位：它不固化、不占据，", 6.1, INK))
    s.append(txt(150, a + 54, "才容得下两端持续涌摇往来。", 6.1, INK))
    s.append(txt(150, a + 78, "这就是和——", 6.6, GREEN))
    s.append(txt(150, a + 94, "不是静止的均衡，是动着的不散。", 6.6, GREEN))

    # 二、合
    b = a + 150
    s.append(txt(24, b, "二 · 合：把虚位填实，强行归一", 6.4, SEAL))
    cy2 = b + 62
    s.append(f'<circle cx="{cx}" cy="{cy2}" r="{r+6}" fill="#E6D8C2" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{cx}" cy="{cy2}" r="{r-2}" fill="#D9CBB2" stroke="{SEAL}" stroke-width="0.8"/>')
    for i in range(-3, 4):
        s.append(f'<line x1="{cx-30}" y1="{cy2+i*9}" x2="{cx+30}" y2="{cy2+i*9}" stroke="{SEAL}" stroke-width="0.4" opacity="0.55"/>')
    s.append(txt(cx, cy2 + 4, "实", 7.6, SEAL, "middle"))
    s.append(txt(cx, cy2 + r + 22, "外壳还在，形制还像", 5.4, "#6E6459", "middle"))
    s.append(txt(150, b + 22, "用泥把中空填满：阳的流通场没了。", 6.1, INK))
    s.append(txt(150, b + 40, "抹去那道虚、消掉差异、强行归一，器就成了泥坨。", 6.1, INK))
    s.append(txt(150, b + 54, "有之利还在，无之用已绝。", 6.1, "#6E6459"))
    s.append(txt(150, b + 78, "合是消掉中间，", 6.6, SEAL))
    s.append(txt(150, b + 94, "和是容下中间。", 6.6, SEAL))

    y2 = b + 136
    s.append(f'<line x1="24" y1="{y2-8}" x2="338" y2="{y2-8}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 2, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "纯阴则死，纯阳则散；一物之内，形质在外撑着，气化在内转着。", 6.5, INK, "middle"))
    s.append(txt(190, y2 + 34, "抹去中间那道虚，器还在，用已亡。", 6.4, "#6E6459", "middle"))
    s.append(gold(y2 + 62, "ch42b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十二章 · 一圈正反合 ============
def ch42c_zheng_fan_he():
    W, H = 380, 520
    body, y = head(W, H, "分出去，又合回来；不是一条直线，是一条环", "第 四 十 二 章 · 一 环",
                   "正 · 分 · 散 · 和", "三不是第三样东西，是被二撑开的那道空。", H)
    s = [body]

    a = y + 22
    s.append(f'<rect x="52" y="{a}" width="252" height="212" rx="26" fill="none" stroke="{LINE2}" stroke-width="0.7"/>')

    # 四节点
    s.append(box(56, a + 8, 96, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(104, a + 25, "道", 8.0, INK, "middle"))
    s.append(txt(104, a + 39, "正 · 未分", 5.6, "#6E6459", "middle"))

    s.append(box(204, a + 8, 96, 40, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(252, a + 25, "一 · 二 · 三", 6.6, INK, "middle"))
    s.append(txt(252, a + 39, "分 · 撑开虚位", 5.6, "#6E6459", "middle"))

    s.append(box(204, a + 164, 96, 40, fill="#F7F1E3", stroke="#E6D8C2"))
    s.append(txt(252, a + 181, "万物", 8.0, INK, "middle"))
    s.append(txt(252, a + 195, "散 · 配比不同", 5.6, "#6E6459", "middle"))

    s.append(box(56, a + 164, 96, 40, fill="#F6E9E2", stroke="{SEAL}".replace("{","").replace("}","") if False else "#D9B7A6"))
    s.append(txt(104, a + 181, "和", 8.0, GREEN, "middle"))
    s.append(txt(104, a + 195, "动着不散", 5.6, "#6E6459", "middle"))

    # 顺时针箭头
    s.append(f'<line x1="156" y1="{a+28}" x2="196" y2="{a+28}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M196,{a+24} l7,4 l-7,4 z" fill="{INK}"/>')
    s.append(f'<line x1="252" y1="{a+54}" x2="252" y2="{a+158}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M248,{a+158} l4,7 l4,-7 z" fill="{INK}"/>')
    s.append(f'<line x1="198" y1="{a+184}" x2="160" y2="{a+184}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M160,{a+180} l-7,4 l7,4 z" fill="{INK}"/>')
    s.append(f'<line x1="104" y1="{a+158}" x2="104" y2="{a+58}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<path d="M100,{a+58} l4,-7 l4,7 z" fill="{SEAL}"/>')
    s.append(txt(116, a + 100, "反", 7.4, SEAL))
    s.append(txt(116, a + 112, "者", 7.4, SEAL))
    s.append(txt(116, a + 124, "道", 7.4, SEAL))
    s.append(txt(116, a + 136, "之", 7.4, SEAL))
    s.append(txt(116, a + 148, "动", 7.4, SEAL))

    # 中心
    s.append(txt(190, a + 100, "虚位", 7.6, INK, "middle"))
    s.append(txt(190, a + 116, "盅·中·冲", 5.6, "#6E6459", "middle"))
    s.append(txt(190, a + 134, "三不是第三样东西", 5.4, SEAL, "middle"))

    y2 = a + 230
    s.append(box(20, y2, 340, 48, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 16, "三生万物之后，还要「冲气以为和」：中间那道虚没被填实，环才接得上。", 6.2, INK, "middle"))
    s.append(txt(190, y2 + 31, "把虚填实叫「合」——外壳还在，环断了；容着虚叫「和」——路还通着。", 6.2, "#6E6459", "middle"))
    s.append(txt(190, y2 + 44, "所以这条链不是直线往前，是分出去、又合回来。", 6.4, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch42c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十三章 · 柔不是软 ============
def ch43a_rou_bu_shi_ruan():
    W, H = 380, 500
    body, y = head(W, H, "柔从木，是能曲能直；坚从土，是硬成一块", "第 四 十 三 章 · 柔 坚",
                   "柔不是软", "一个还能变，一个已经定了。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "天下之至柔，驰骋于天下之至坚。", 7.0, INK, "middle"))
    s.append(txt(190, y + 27, "「柔」，《说文》「木曲直也」，从木；「坚」，《说文》「刚也」，从土。", 5.6, "#6E6459", "middle"))

    a = y + 52
    # 左：木
    s.append(txt(24, a + 6, "一 · 柔：从木", 6.4, GREEN))
    s.append(f'<path d="M56,{a+30} C86,{a+18} 96,{a+62} 126,{a+48}" fill="none" stroke="{GREEN}" stroke-width="1.6"/>')
    s.append(f'<path d="M56,{a+54} C90,{a+44} 104,{a+86} 126,{a+72}" fill="none" stroke="{GREEN}" stroke-width="0.7" stroke-dasharray="5 4"/>')
    s.append(f'<path d="M56,{a+72} C84,{a+66} 100,{a+94} 126,{a+92}" fill="none" stroke="{GREEN}" stroke-width="0.7" stroke-dasharray="2 4"/>')
    s.append(txt(132, a + 46, "木", 8.4, GREEN))
    s.append(txt(56, a + 92, "同一根枝，三种姿态：能曲能直，说明它还在活、还有余地。", 5.6, "#6E6459"))
    s.append(txt(150, a + 22, "「至柔」不是「软到不能再软」，", 6.2, INK))
    s.append(txt(150, a + 38, "是「变到不能再能变」。", 6.2, INK))
    s.append(txt(150, a + 58, "柔的尽头不是无力，", 6.2, "#6E6459"))
    s.append(txt(150, a + 74, "是没有被任何一种形状锁住。", 6.2, "#6E6459"))

    # 右：土
    b = a + 118
    s.append(txt(24, b + 6, "二 · 坚：从土", 6.4, SEAL))
    s.append(f'<rect x="56" y="{b+18}" width="70" height="60" fill="#E6D8C2" stroke="{INK}" stroke-width="1.2"/>')
    for i in range(1, 6):
        s.append(f'<line x1="{56+i*11}" y1="{b+18}" x2="{56+i*11}" y2="{b+78}" stroke="{INK}" stroke-width="0.4" opacity="0.45"/>')
    for j in range(1, 4):
        s.append(f'<line x1="56" y1="{b+18+j*15}" x2="126" y2="{b+18+j*15}" stroke="{INK}" stroke-width="0.4" opacity="0.45"/>')
    s.append(txt(150, b + 22, "土是实的、是硬的、是不动的：", 6.2, INK))
    s.append(txt(150, b + 38, "一硬成一块，就不再变。", 6.2, INK))
    s.append(txt(150, b + 58, "它的强处是定型，弱处也是定型——", 6.2, "#6E6459"))
    s.append(txt(150, b + 74, "一旦定了，只能以一种方式存在。", 6.2, "#6E6459"))
    s.append(txt(91, b + 94, "已经定了", 5.6, SEAL, "middle"))

    y2 = b + 116
    s.append(f'<line x1="24" y1="{y2-8}" x2="338" y2="{y2-8}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 2, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 18, "一个从木，一个从土；一个还能变，一个已经定了。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 32, "还能变的那个，能穿过已经定的那个。", 6.8, GREEN, "middle"))
    s.append(gold(y2 + 60, "ch43a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十三章 · 不撞，是跑 ============
def ch43b_bu_zhuang_shi_pao():
    W, H = 380, 560
    body, y = head(W, H, "撞是把自己的力交出去，跑是把自己的力留着", "第 四 十 三 章 · 驰 骋",
                   "不撞，是跑", "至柔在至坚身上「驰骋」——不是撞，是跑。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "驰骋，大驱也；骋，直驰也——放马直跑，不绕弯。", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "老子把这个战场上的词，安在最软的那样东西身上。", 5.7, "#6E6459", "middle"))

    wx, wy = 104, None

    # 一、撞
    a = y + 48
    s.append(txt(24, a + 4, "一 · 撞：力交出去", 6.2, SEAL))
    wy = a + 16
    s.append(f'<rect x="{wx}" y="{wy}" width="12" height="64" fill="#E6D8C2" stroke="{INK}" stroke-width="0.8"/>')
    for j in range(4):
        s.append(f'<line x1="{wx}" y1="{wy+8+j*16}" x2="{wx+12}" y2="{wy+8+j*16}" stroke="{INK}" stroke-width="0.4" opacity="0.5"/>')
    s.append(f'<circle cx="76" cy="{wy+30}" r="10" fill="#D9CBB2" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="56" y1="{wy+30}" x2="64" y2="{wy+30}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="50" y1="{wy+26}" x2="58" y2="{wy+26}" stroke="{INK}" stroke-width="0.5" opacity="0.7"/>')
    s.append(f'<line x1="50" y1="{wy+34}" x2="58" y2="{wy+34}" stroke="{INK}" stroke-width="0.5" opacity="0.7"/>')
    s.append(f'<path d="M68,{wy+22} l-8,-6 M68,{wy+38} l-8,6" stroke="{SEAL}" stroke-width="0.7" fill="none"/>')
    s.append(f'<circle cx="92" cy="{wy+16}" r="1.6" fill="{SEAL}"/><circle cx="98" cy="{wy+44}" r="1.4" fill="{SEAL}"/><circle cx="86" cy="{wy+50}" r="1.2" fill="{SEAL}"/>')
    s.append(txt(64, wy + 74, "硬碰硬：两边同时消耗", 5.4, "#6E6459", "middle"))
    s.append(txt(140, a + 20, "两方同时消耗，力气花在「证明自己硬」上。", 6.1, INK))
    s.append(txt(140, a + 36, "赢了也是一身碎屑；输了更不用说。", 6.1, INK))
    s.append(txt(140, a + 58, "撞的那一下，力已经离手了。", 6.4, SEAL))

    # 二、驰骋
    b = a + 106
    s.append(txt(24, b + 4, "二 · 跑：力还留着", 6.2, GREEN))
    wy = b + 16
    s.append(f'<rect x="{wx}" y="{wy}" width="12" height="64" fill="#E6D8C2" stroke="{INK}" stroke-width="0.8"/>')
    for j in range(4):
        s.append(f'<line x1="{wx}" y1="{wy+8+j*16}" x2="{wx+12}" y2="{wy+8+j*16}" stroke="{INK}" stroke-width="0.4" opacity="0.5"/>')
    for k, off in enumerate([18, 32, 46]):
        s.append(f'<path d="M46,{wy+off} C64,{wy+off-6} 82,{wy+off+6} 100,{wy+off} L116,{wy+off} '
                 f'C126,{wy+off-4} 128,{wy+off+3} 132,{wy+off}" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(64, wy + 74, "不接触，所以不损耗", 5.4, "#6E6459", "middle"))
    s.append(txt(140, b + 20, "至柔不与硬碰，消耗只发生在硬的那一方。", 6.1, INK))
    s.append(txt(140, b + 36, "它从硬的东西里穿过去，自己没碰掉一块。", 6.1, INK))
    s.append(txt(140, b + 58, "跑的时候，力一直在自己手里。", 6.4, GREEN))

    # 三、无有入无间
    c = b + 106
    s.append(txt(24, c + 4, "三 · 无有：不占位，无处不入", 6.2, INK))
    wy = c + 16
    s.append(f'<rect x="56" y="{wy+8}" width="86" height="56" fill="#E6D8C2" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="62" y="{wy+14}" width="74" height="44" fill="#D9CBB2" stroke="{INK}" stroke-width="0.5"/>')
    s.append(txt(99, wy + 40, "无间", 6.0, SEAL, "middle"))
    s.append(txt(99, wy + 54, "连一道门缝都没有", 4.8, "#6E6459", "middle"))
    s.append(f'<path d="M40,{wy+22} C60,{wy+16} 80,{wy+26} 100,{wy+21} L132,{wy+21}" fill="none" stroke="{GREEN}" '
             f'stroke-width="0.8" stroke-dasharray="6 4"/>')
    s.append(txt(150, c + 20, "有形之物要靠别人让出一道缝；无形之物不必。", 6.1, INK))
    s.append(txt(150, c + 36, "它不占位置，所以没有哪一处是进不去的。", 6.1, INK))
    s.append(txt(150, c + 58, "它不是凿开缝进去的，它是那扇门本身就有的。", 6.2, INK))

    y2 = c + 100
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "一不接触，二不占位，三还能变。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 34, "柔之所以胜，不是因为更强，是它不参加那场比赛。", 6.4, "#6E6459", "middle"))
    s.append(gold(y2 + 62, "ch43b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十四章 · 三问 ============
def ch44a_san_wen():
    W, H = 380, 520
    body, y = head(W, H, "亲是到得了，多是重，病是病上加病", "第 四 十 四 章 · 三 问",
                   "三问，越问越近", "从别人的眼，到手上的物，到要拿的那个念。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "名与身孰亲？身与货孰多？得与亡孰病？", 6.8, INK, "middle"))
    s.append(txt(190, y + 27, "三问不是三道并列的选择题，是一次往里剥。", 5.7, "#6E6459", "middle"))

    # 一、名与身
    a = y + 50
    s.append(txt(24, a + 6, "一 · 名与身孰亲", 6.2, INK))
    s.append(f'<path d="M42,{a+22} h34 a5,5 0 0 1 5,5 v8 a5,5 0 0 1 -5,5 h-22 l-7,7 v-7 h-5 a5,5 0 0 1 -5,-5 v-8 a5,5 0 0 1 5,-5 z" '
             f'fill="#F2EADA" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(64, a + 33, "名", 5.8, INK, "middle"))
    s.append(f'<line x1="86" y1="{a+32}" x2="104" y2="{a+32}" stroke="#C9B79A" stroke-width="0.6" stroke-dasharray="4 4"/>')
    s.append(f'<circle cx="116" cy="{a+24}" r="4.4" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<line x1="116" y1="{a+28}" x2="116" y2="{a+38}" stroke="{GREEN}" stroke-width="1"/>')
    s.append(txt(116, a + 48, "身", 5.2, GREEN, "middle"))
    s.append(txt(150, a + 22, "名在别人嘴里，落在别人对你的记录上；你摸不到它。", 6.0, INK))
    s.append(txt(150, a + 38, "「亲」，《说文》「至也」——到得了。", 6.0, "#6E6459"))
    s.append(txt(150, a + 56, "一个够不着，一个你就在里头。这一问不必回答。", 6.2, GREEN))

    # 二、身与货
    b = a + 86
    s.append(txt(24, b + 6, "二 · 身与货孰多", 6.2, INK))
    s.append(f'<circle cx="80" cy="{b+20}" r="4.2" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="80" y1="{b+24}" x2="80" y2="{b+44}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="80" y1="{b+44}" x2="72" y2="{b+56}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="80" y1="{b+44}" x2="88" y2="{b+56}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="80" y1="{b+30}" x2="62" y2="{b+30}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<rect x="40" y="{b+14}" width="20" height="16" fill="#E6D8C2" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<rect x="40" y="{b+32}" width="20" height="16" fill="#E6D8C2" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<line x1="50" y1="{b+46}" x2="50" y2="{b+58}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(txt(80, b + 64, "压在谁身上", 5.2, SEAL, "middle"))
    s.append(txt(150, b + 22, "「多」，《说文》「重也」——不是数量，是分量。", 6.0, INK))
    s.append(txt(150, b + 38, "货在身外，可它压在身上；要守它，就得一直看着它。", 6.0, "#6E6459"))
    s.append(txt(150, b + 56, "一个人囤到一定程度，不是他拥有货，是货拥有他。", 6.2, INK))

    # 三、得与亡
    c = b + 88
    s.append(txt(24, c + 6, "三 · 得与亡孰病", 6.2, INK))
    for i in range(3):
        s.append(f'<rect x="46" y="{c+16+i*13}" width="34" height="11" fill="#F0E3D6" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(63, c + 24, "争", 4.9, SEAL, "middle"))
    s.append(txt(63, c + 37, "守", 4.9, SEAL, "middle"))
    s.append(txt(63, c + 50, "怕丢", 4.9, SEAL, "middle"))
    s.append(txt(63, c + 66, "一次「得」，背三份工", 5.0, "#6E6459", "middle"))
    s.append(txt(150, c + 22, "「病」，《说文》「疾加也」——在病上再加一层。", 6.0, INK))
    s.append(txt(150, c + 38, "得到要争，得到要守，守住了还怕丢。", 6.0, "#6E6459"))
    s.append(txt(150, c + 56, "而「亡」只是把这份工卸了。病重的常是那个一直在得的人。", 5.9, SEAL))

    y2 = c + 84
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "三问剥三层：别人的眼、手上的物、要拿的那个念。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 34, "剥到底，只剩一句：你要的那样东西，正在拿什么换。", 6.4, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch44a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十四章 · 月供与逃跑 ============
def ch44b_yue_gong_yu_tao():
    W, H = 380, 520
    body, y = head(W, H, "喜欢不要钱，甚爱要月供；藏得越多，跑得越勤", "第 四 十 四 章 · 费 亡",
                   "月供与逃跑", "甚爱必大费，多藏必厚亡。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "「费」，《说文》「散财用也」，从贝；「亡」，《说文》「逃也」。", 6.2, INK, "middle"))
    s.append(txt(190, y + 27, "一个说的是花钱，一个说的是跑掉——都不是「伤心」，也不是「死」。", 5.7, "#6E6459", "middle"))

    a = y + 48
    s.append(txt(24, a + 6, "一 · 甚爱必大费", 6.2, SEAL))
    s.append(f'<rect x="40" y="{a+20}" width="44" height="40" rx="3" fill="#F7F1E3" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="52" y="{a+32}" width="20" height="16" fill="#E6D8C2" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<path d="M54,{a+32} v-4 a4,4 0 0 1 8,0 v4" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<path d="M64,{a+48} v3 a4,4 0 0 0 8,0 v-3" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(42, a + 70, "锁进边界", 5.0, "#6E6459"))
    for i in range(5):
        s.append(f'<rect x="{92+i*9}" y="{a+26}" width="7" height="24" fill="#F0E3D6" stroke="{SEAL}" stroke-width="0.4"/>')
    s.append(txt(108, a + 60, "按天付", 4.6, SEAL))
    s.append(txt(150, a + 22, "你爱一个名，就要一直维护它：解释、澄清、防误解、应酬。", 5.9, INK))
    s.append(txt(150, a + 38, "「爱」在这里是锁死：每开一次门，都要付一次费。", 5.9, "#6E6459"))
    s.append(txt(150, a + 56, "「大费」的「大」，是这费不一次付清，是按天付。", 6.0, SEAL))

    b = a + 96
    s.append(txt(24, b + 6, "二 · 多藏必厚亡", 6.2, INK))
    s.append(f'<rect x="36" y="{b+18}" width="52" height="44" fill="#F7F1E3" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="36" y1="{b+36}" x2="88" y2="{b+36}" stroke="{INK}" stroke-width="0.6"/>')
    for i in range(3):
        s.append(f'<rect x="{41+i*15}" y="{b+22}" width="11" height="10" fill="#E6D8C2" stroke="{INK}" stroke-width="0.4"/>')
    for i in range(3):
        s.append(f'<rect x="{41+i*15}" y="{b+40}" width="11" height="10" fill="#E6D8C2" stroke="{INK}" stroke-width="0.4"/>')
    for dx, dy in [(16, -10), (30, 2), (26, 20), (6, 26), (-10, 12)]:
        s.append(f'<line x1="88" y1="{b+34}" x2="{88+dx}" y2="{b+34+dy}" stroke="{SEAL}" stroke-width="0.6" stroke-dasharray="4 3"/>')
        s.append(f'<rect x="{88+dx-3}" y="{b+34+dy-3}" width="6" height="6" fill="{SEAL}" opacity="0.85"/>')
    s.append(txt(30, b + 70, "藏得越多，跑得越勤", 5.0, "#6E6459"))
    s.append(txt(150, b + 22, "「亡」是「逃也」——跟「死」不是一回事。", 5.9, INK))
    s.append(txt(150, b + 38, "藏一百样，就有一百样会跑：跑一样疼，跑一样急。", 5.9, "#6E6459"))
    s.append(txt(150, b + 56, "藏是一件件往里搬，亡是一件件往外跑。", 6.0, INK))

    y2 = b + 102
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "这一章不是道德劝谕，是一份成本核算。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 34, "每一次向外抓取，都在从身家性命里扣一笔。", 6.4, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch44b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十四章 · 脚与止 ============
def ch44c_jiao_yu_zhi():
    W, H = 380, 566
    body, y = head(W, H, "足是脚，止是脚趾：站住，才长久", "第 四 十 四 章 · 足 止",
                   "站住，停脚", "知足不是心态好，是站得稳。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "「足」，脚；「止」，脚趾。这两个字本来是身体词。", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "老子不是在劝人心态，是在说一个人得知道自己站在哪儿、什么时候停脚。", 5.3, "#6E6459", "middle"))

    # 左：脚印
    a = y + 50
    s.append(txt(24, a + 6, "一 · 足：站得住的那个地方", 6.0, GREEN))
    cx, top = 84, a + 24
    s.append(f'<ellipse cx="{cx}" cy="{top+40}" rx="17" ry="26" fill="#EFE4CF" stroke="{INK}" stroke-width="0.8"/>')
    for i, (dx, r) in enumerate([(-13, 4.2), (-7, 4.4), (-1, 4.6), (4, 4.2), (9, 3.6)]):
        s.append(f'<circle cx="{cx+dx}" cy="{top+6+abs(dx)*0.4}" r="{r}" fill="none" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(f'<line x1="{cx+22}" y1="{top+2}" x2="{cx+34}" y2="{top-6}" stroke="{GREEN}" stroke-width="0.6"/>')
    s.append(txt(cx + 38, top - 6, "止", 6.0, GREEN))
    s.append(txt(cx, top + 76, "足＝脚：站着的地方", 5.2, "#6E6459", "middle"))
    s.append(txt(150, a + 24, "「足」是脚。知足不是觉得自己够了，", 5.9, INK))
    s.append(txt(150, a + 40, "是知道自己站在哪儿——站得稳的人不抢，", 5.9, INK))
    s.append(txt(150, a + 54, "不抢的人不容易被踩。", 5.9, INK))

    # 右：止与忍
    b = a + 126
    s.append(txt(24, b + 6, "二 · 止：停住的那个动作", 6.0, SEAL))
    s.append(f'<path d="M42,{b+78} C62,{b+58} 82,{b+44} 102,{b+42} C118,{b+41} 128,{b+50} 138,{b+64}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M138,{b+64} C132,{b+72} 124,{b+76} 116,{b+78}" fill="none" stroke="#C9B79A" stroke-width="0.6" stroke-dasharray="4 4"/>')
    s.append(txt(110, b + 32, "顶点", 4.8, SEAL, "middle"))
    s.append(f'<line x1="110" y1="{b+36}" x2="110" y2="{b+41}" stroke="{SEAL}" stroke-width="0.5"/>')
    s.append(f'<circle cx="90" cy="{b+47}" r="4.2" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(txt(74, b + 96, "在这里停脚", 4.9, GREEN, "middle"))
    s.append(txt(144, b + 26, "「止」是脚趾，是落点：", 5.8, INK))
    s.append(txt(144, b + 40, "把脚放下，就不较劲了。", 5.8, INK))
    s.append(txt(144, b + 58, "「忍」是拉住自己，还在往前倾。", 5.8, SEAL))
    s.append(txt(144, b + 78, "一个已经放下，一个还在争。", 5.9, "#6E6459"))

    y2 = b + 110
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 46, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "长久不是不死，是一直没到那个该翻过来的点。", 6.8, INK, "middle"))
    s.append(txt(190, y2 + 34, "过了顶点还在迈步，就撞上「物壮则老」。", 6.2, "#6E6459", "middle"))
    s.append(gold(y2 + 62, "ch44c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十五章 · 留一道缝 ============
def ch45a_liu_yi_dao_feng():
    W, H = 380, 580
    body, y = head(W, H, "不是做得不够，是把缝预留在对的地方", "第 四 十 五 章 · 留 缝",
                   "留一道缝", "大成若缺，其用不敝。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "「缺」，《说文》「器破也」——器皿破了口。", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "到了头的东西，要留一个口；封死了，力就全落在自己身上。", 5.7, "#6E6459", "middle"))

    a = y + 48
    deck = a + 46
    # 桥面两段
    s.append(f'<rect x="34" y="{deck}" width="116" height="11" fill="#E6D8C2" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="162" y="{deck}" width="176" height="11" fill="#E6D8C2" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="150" y1="{deck-4}" x2="150" y2="{deck+15}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="162" y1="{deck-4}" x2="162" y2="{deck+15}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    s.append(txt(156, deck - 12, "缝", 6.4, SEAL, "middle"))
    s.append(f'<path d="M144,{deck+2} l-10,0 M134,{deck+2} l3,-3 M134,{deck+2} l3,3" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(f'<path d="M168,{deck+2} l10,0 M178,{deck+2} l-3,-3 M178,{deck+2} l-3,3" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
    # 桥墩
    for px in (80, 262):
        s.append(f'<path d="M{px-9},{deck+11} L{px+9},{deck+11} L{px+13},{deck+46} L{px-13},{deck+46} Z" fill="#EFE4CF" stroke="{INK}" stroke-width="0.7"/>')
        for k in range(3):
            s.append(f'<line x1="{px-9+k*6}" y1="{deck+11}" x2="{px-13+k*8}" y2="{deck+46}" stroke="{INK}" stroke-width="0.35" opacity="0.5"/>')
    s.append(f'<line x1="20" y1="{deck+46}" x2="340" y2="{deck+46}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(156, deck + 60, "桥面两段之间，故意留一道缝：热胀冷缩，力从缝里放掉", 5.2, "#6E6459", "middle"))

    b = deck + 78
    s.append(txt(24, b + 4, "一 · 封死：力只能落在自己身上", 5.9, SEAL))
    s.append(f'<path d="M52,{b+14} L60,{b+48} L92,{b+48} L100,{b+14}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="52" y1="{b+14}" x2="100" y2="{b+14}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="76" y1="{b+20}" x2="72" y2="{b+32}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="72" y1="{b+32}" x2="78" y2="{b+42}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(76, b + 64, "封死则裂", 5.0, SEAL, "middle"))
    s.append(txt(150, b + 18, "凡是封死了口的器，用久了都会破。", 5.9, INK))
    s.append(txt(150, b + 32, "它里面没有余地，一受力只能裂。", 5.9, INK))

    c = b + 74
    s.append(txt(24, c + 4, "二 · 留缝：力从缝里卸掉", 5.9, GREEN))
    s.append(f'<path d="M52,{c+14} L60,{c+48} L92,{c+48} L100,{c+14}" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(f'<line x1="52" y1="{c+14}" x2="72" y2="{c+14}" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<line x1="80" y1="{c+14}" x2="100" y2="{c+14}" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<path d="M76,{c+10} l-2,-8 M79,{c+10} l2,-8" fill="none" stroke="{GREEN}" stroke-width="0.5"/>')
    s.append(txt(76, c + 62, "留缝不敝", 5.0, GREEN, "middle"))
    s.append(txt(150, c + 18, "留了缝的器，用久了反而不破——", 5.9, INK))
    s.append(txt(150, c + 32, "那道缝一直在替它卸力。", 5.9, INK))

    y2 = c + 80
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "「大成」不是没有做到头，是做到头了，还留一处不封。", 6.2, INK, "middle"))
    s.append(txt(190, y2 + 34, "那个缺口不是缺陷，是泄压的地方。", 6.2, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch45a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十五章 · 五处，一道缝 ============
# ============ 第四十五章 · 井 ============
def ch45b_jing_ying_chong():
    W, H = 380, 468
    body, y = head(W, H, "越深的井，看下去越像空的", "第 四 十 五 章 · 井",
                   "井口看着是空的", "大盈若冲，其用不穷。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 15, "「冲」，虚而不满——里面有东西在动。", 6.4, INK, "middle"))
    s.append(txt(190, y + 27, "不是空，是满在里面、外面不显。", 5.7, "#6E6459", "middle"))

    a = y + 48
    ground = a + 34
    # 井筒剖面
    s.append(f'<line x1="24" y1="{ground}" x2="200" y2="{ground}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M78,{ground} L86,{ground+96} L142,{ground+96} L150,{ground} Z" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M92,{ground+96} L92,{ground+62} L136,{ground+62} L136,{ground+96} Z" fill="#DCE6E0" stroke="{GREEN}" stroke-width="0.5"/>')
    s.append(f'<line x1="92" y1="{ground+62}" x2="136" y2="{ground+62}" stroke="{GREEN}" stroke-width="0.8"/>')
    for k in range(2):
        s.append(f'<path d="M98,{ground+70+k*9} q9,-4 18,0 q9,4 18,0" fill="none" stroke="{GREEN}" stroke-width="0.45" opacity="0.8"/>')
    s.append(txt(114, ground + 84, "水在下面", 4.6, GREEN, "middle"))
    # 井口：看下去是空的
    s.append(f'<ellipse cx="114" cy="{ground}" rx="36" ry="7" fill="#EFE4CF" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<ellipse cx="114" cy="{ground}" rx="26" ry="4.6" fill="#6E6459" opacity="0.55"/>')
    s.append(f'<line x1="114" y1="{ground-8}" x2="114" y2="{ground-26}" stroke="{SEAL}" stroke-width="0.5" stroke-dasharray="3 3"/>')
    s.append(txt(114, ground - 32, "看下去，空的", 5.0, SEAL, "middle"))

    # 右：一只满到口沿的杯子作对照
    s.append(f'<path d="M226,{ground-36} L232,{ground+2} L272,{ground+2} L278,{ground-36}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<ellipse cx="252" cy="{ground-36}" rx="26" ry="5.2" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<rect x="231" y="{ground-34}" width="42" height="18" fill="#E8D9C4" stroke="{SEAL}" stroke-width="0.4"/>')
    s.append(f'<path d="M240,{ground-40} v-3 M252,{ground-40} v-5 M264,{ground-40} v-3" fill="none" stroke="{SEAL}" stroke-width="0.5"/>')
    s.append(txt(252, ground + 16, "满到口沿，一满就到顶", 4.8, SEAL, "middle"))

    b = ground + 112
    s.append(txt(24, b + 10, "井：打得越深，口上看着越空。水不在口上，在下面。", 5.9, INK))
    s.append(txt(24, b + 26, "它不往外倒，所以一直有得打——其用不穷。", 5.9, INK))
    s.append(txt(24, b + 46, "杯子满到口沿，看着是满的；可它一满就到顶，再多一滴都是溢。", 5.9, SEAL))

    y2 = b + 62
    s.append(f'<line x1="24" y1="{y2-4}" x2="338" y2="{y2-4}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "满得溢出来的，是在往外倒；满在里面不溢的，是在往里续。", 6.2, INK, "middle"))
    s.append(txt(190, y2 + 34, "真正充盈的在里面，外面永远是虚的。", 6.2, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch45b_jing"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十五章 · 笔 ============
def ch45c_yin_er_bu_fa():
    W, H = 380, 650
    body, y = head(W, H, "引而不发：有话说得出，却不说满", "第 四 十 五 章 · 弓",
                   "引而不发", "大直若屈，大巧若拙，大辩若讷。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "弓臂是弯的，箭才走得直；弦拉到「满」，弓臂就折。", 5.8, INK, "middle"))
    s.append(txt(190, y + 26, "所以好射手引而不发——留一分不给出去。", 5.6, "#6E6459", "middle"))

    a = y + 52
    cy = a + 92
    # 弓臂（反曲）
    s.append(f'<path d="M82,{cy-70} Q58,{cy-44} 46,{cy-16} Q42,{cy} 46,{cy+16} Q58,{cy+44} 82,{cy+70}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<path d="M82,{cy-70} l-12,-4 M82,{cy+70} l-12,4" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    # 弦（未引）
    s.append(f'<line x1="80" y1="{cy-66}" x2="80" y2="{cy+66}" stroke="{INK}" stroke-width="0.4" opacity="0.45"/>')
    # 满位置（虚线）
    s.append(f'<line x1="126" y1="{cy-12}" x2="126" y2="{cy+12}" stroke="{SEAL}" stroke-width="0.5" stroke-dasharray="3 2"/>')
    s.append(txt(126, cy + 26, "还差一分", 4.6, SEAL, "middle"))
    # 弦（引而不发）
    s.append(f'<line x1="80" y1="{cy-66}" x2="108" y2="{cy}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="80" y1="{cy+66}" x2="108" y2="{cy}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="108" cy="{cy}" r="2.6" fill="{GREEN}"/>')
    # 箭
    s.append(f'<line x1="110" y1="{cy}" x2="246" y2="{cy}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M246,{cy} l-7,-3.4 l0,6.8 z" fill="{INK}"/>')

    # 弓臂受力的裂纹（满时）
    s.append(f'<line x1="72" y1="{cy-74}" x2="66" y2="{cy-62}" stroke="{SEAL}" stroke-width="0.5"/>')
    s.append(f'<line x1="66" y1="{cy-62}" x2="70" y2="{cy-60}" stroke="{SEAL}" stroke-width="0.5"/>')
    s.append(txt(58, cy - 86, "拉到满，先折这里", 4.4, SEAL))
    # 标注箭头
    s.append(f'<line x1="108" y1="{cy+34}" x2="108" y2="{cy+8}" stroke="{GREEN}" stroke-width="0.4"/>')
    s.append(txt(108, cy + 44, "引而不发", 5.2, GREEN, "middle"))

    b = cy + 84
    rows = [
        ("臂 · 大直若屈", "臂做成直的，一拉就折；弯着，力才存得住，箭才走得直。"),
        ("弦 · 大巧若拙", "撒放的人只是松手，弦自己出去——看不出使过劲。"),
        ("不发 · 大辩若讷", "引而不发：话到嘴边、力到弦上，仍留一分不给出去。"),
        ("收 · 清静为正", "射完就松弦。弓不常张，张久了臂就疲。"),
    ]
    for k, (tag, line) in enumerate(rows):
        r = b + k * 44
        s.append(f'<circle cx="30" cy="{r}" r="2.4" fill="{SEAL}" opacity="0.55"/>')
        s.append(txt(42, r + 4, tag, 5.9, SEAL))
        s.append(txt(42, r + 19, line, 5.6, INK))

    y2 = b + 4 * 44 + 4
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "弓不常张，话不说满，力不使尽。", 6.2, INK, "middle"))
    s.append(txt(190, y2 + 34, "三样都留着那一分——那一分，才是能再用的。", 6.2, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch45c_gong"))
    s.append('</svg>')
    return "\n".join(s)

# ============ 第四十六章 · 路上的印子 ============
def horse(s, x, gy, k=1.0, flip=False, col=None, op=0.85):
    """侧立一匹马，脚在 gy，面朝右；flip=True 面朝左。k 为缩放。"""
    col = col or INK
    sx = -k if flip else k
    g = [f'<g transform="translate({x},{gy}) scale({sx},{k})" fill="{col}" opacity="{op}">']
    # 躯干
    g.append('<ellipse cx="-4" cy="-34" rx="24" ry="12"/>')
    g.append('<circle cx="-26" cy="-35" r="11"/>')
    g.append('<circle cx="10" cy="-35" r="11"/>')
    # 颈
    g.append('<path d="M8,-43 L21,-43 L34,-66 L20,-69 Z"/>')
    # 头
    g.append('<path d="M19,-69 L36,-65 L46,-62 L47,-56 L40,-54 L28,-61 Z"/>')
    # 耳
    g.append('<path d="M22,-69 L25,-78 L30,-69 Z"/>')
    # 鬃
    g.append('<path d="M20,-69 l2,-5 l2,5 l2,-6 l2,6" stroke="%s" stroke-width="1.2" fill="none" opacity="0.9"/>' % col)
    # 尾
    g.append(f'<path d="M-32,-42 q-8,16 -6,26" stroke="{col}" stroke-width="2.6" fill="none"/>')
    # 四腿
    for lx, lx2 in ((15, 16), (6, 4), (-22, -25), (-14, -12)):
        g.append(f'<line x1="{lx}" y1="-28" x2="{lx2}" y2="-1" stroke="{col}" stroke-width="2.6"/>')
        g.append(f'<rect x="{lx2-2}" y="-2" width="7" height="2.6"/>')
    g.append('</g>')
    s.extend(g)


def ch46a_lu_shang_yin_zi():
    W, H = 380, 512
    body, y = head(W, H, "一个国家的秩序，看马站在哪儿就知道", "第 四 十 六 章 · 马",
                   "马站在哪儿", "天下有道，却走马以粪；天下无道，戎马生于郊。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「却」，《说文》「节欲也」——先节住欲，再把马拉回来。", 5.8, INK, "middle"))
    s.append(txt(190, y + 26, "「郊」，《说文》「距国百里为郊」——都城往外一百里，最不该见血的一圈。", 5.3, "#6E6459", "middle"))

    a = y + 46
    s.append(txt(24, a + 8, "一 · 有道：马在田里", 5.9, GREEN))
    gy = a + 82
    s.append(f'<line x1="24" y1="{gy}" x2="338" y2="{gy}" stroke="{LINE2}" stroke-width="0.7"/>')
    # 田垄
    for k in range(4):
        yy = gy - 8 - k * 9
        s.append(f'<line x1="28" y1="{yy}" x2="92" y2="{yy}" stroke="{GREEN}" stroke-width="0.45" opacity="0.8"/>')
    s.append(txt(60, gy + 12, "田", 4.6, "#6E6459", "middle"))
    # 车辙
    s.append(f'<line x1="118" y1="{gy+2}" x2="286" y2="{gy+2}" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>')
    s.append(f'<line x1="118" y1="{gy+8}" x2="286" y2="{gy+8}" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>')
    # 马拉车
    horse(s, 168, gy, k=0.66, flip=True)
    s.append(f'<line x1="186" y1="{gy-20}" x2="214" y2="{gy-22}" stroke="{INK}" stroke-width="0.5"/>')
    s.append(f'<rect x="214" y="{gy-30}" width="52" height="24" fill="#E6D8C2" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M214,{gy-30} l-7,-2 M266,{gy-30} l7,-2" stroke="{INK}" stroke-width="0.4" fill="none"/>')
    for wx in (226, 254):
        s.append(f'<circle cx="{wx}" cy="{gy-3}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<circle cx="{wx}" cy="{gy-3}" r="1.8" fill="{INK}" opacity="0.5"/>')
    s.append(txt(240, gy - 38, "却走马以粪", 4.8, GREEN, "middle"))
    s.append(txt(241, gy + 20, "最贵的军资，拉最贱的肥", 4.6, "#6E6459", "middle"))

    b = a + 100
    s.append(txt(24, b + 8, "二 · 无道：马在郊外生崽", 5.9, SEAL))
    gy2 = b + 84
    s.append(f'<line x1="24" y1="{gy2}" x2="338" y2="{gy2}" stroke="{LINE2}" stroke-width="0.7"/>')
    # 城墙
    s.append(f'<rect x="28" y="{gy2-30}" width="66" height="30" fill="none" stroke="{INK}" stroke-width="1"/>')
    for k in range(4):
        s.append(f'<rect x="{30+k*16}" y="{gy2-38}" width="9" height="8" fill="none" stroke="{INK}" stroke-width="0.6"/>')
    s.append(txt(61, gy2 + 12, "国", 4.6, "#6E6459", "middle"))
    # 营帐
    s.append(f'<path d="M104,{gy2} L124,{gy2-26} L144,{gy2} Z" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="124" y1="{gy2-26}" x2="124" y2="{gy2-33}" stroke="{INK}" stroke-width="0.5"/>')
    s.append(txt(124, gy2 + 12, "百里之内", 4.6, "#6E6459", "middle"))
    # 母马与小马
    horse(s, 192, gy2, k=0.76)
    horse(s, 240, gy2, k=0.44)
    s.append(txt(196, gy2 + 12, "母马上阵", 4.6, SEAL, "middle"))
    s.append(txt(246, gy2 + 12, "生在野地", 4.6, SEAL, "middle"))
    # 乱蹄印
    for mx, off in [(288, 0), (312, 4), (330, 0), (300, 9), (322, 12)]:
        s.append(f'<path d="M{mx},{gy2-off} q4,-3.2 8,0" fill="none" stroke="{SEAL}" stroke-width="0.5" opacity="0.85"/>')
    s.append(txt(310, gy2 - 34, "蹄印又急又乱", 4.6, "#6E6459", "middle"))

    c = gy2 + 30
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "同一个国家，两种年景：一匹马往田里去，一匹马在战场生崽。", 5.8, INK, "middle"))
    s.append(txt(190, c + 38, "不必看它说什么，看马站在哪儿。", 6.0, GREEN, "middle"))
    s.append(gold(c + 66, "ch46a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十六章 · 刀改成犁 ============
def ch46b_dao_gai_li():
    W, H = 380, 536
    body, y = head(W, H, "他不是把刀收了，是把刀改成了犁", "第 四 十 六 章 · 犁",
                   "刀改成犁", "天下有道，却走马以粪。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「却」是把冲出去的拉回来；「粪」是把不要的扫回去。", 5.9, INK, "middle"))
    s.append(txt(190, y + 26, "两个都是「收」：一个收力，一个收物。", 5.6, "#6E6459", "middle"))

    a = y + 58
    cy = a + 40
    # 刀
    s.append(txt(24, cy - 44, "刀", 6.2, INK))
    s.append(f'<path d="M44,{cy-12} Q64,{cy-6} 96,{cy-6} L96,{cy+2} Q64,{cy+5} 44,{cy+10} Z" fill="#DDD5C6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="24" y="{cy-5}" width="20" height="12" rx="2" fill="#E6D8C2" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<line x1="44" y1="{cy-12}" x2="44" y2="{cy+10}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(70, cy + 24, "为杀而生", 4.6, "#6E6459", "middle"))

    # 箭头
    s.append(f'<path d="M120,{cy-1} L162,{cy-1}" fill="none" stroke="{GREEN}" stroke-width="0.6" marker-end="url(#arr2)"/>')
    s.append(txt(140, cy + 16, "改用途", 4.6, GREEN, "middle"))
    s.append(txt(140, cy + 28, "不是取消力量", 4.2, "#6E6459", "middle"))

    # 犁
    s.append(txt(300, cy - 44, "犁", 6.2, INK))
    s.append(f'<line x1="180" y1="{cy+34}" x2="340" y2="{cy+34}" stroke="{LINE2}" stroke-width="0.7"/>')
    # 犁辕
    s.append(f'<path d="M210,{cy-2} Q250,{cy-14} 320,{cy-22}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="320" y1="{cy-22}" x2="338" y2="{cy-24}" stroke="{INK}" stroke-width="0.5"/>')
    # 犁把
    s.append(f'<line x1="228" y1="{cy-6}" x2="242" y2="{cy-30}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="242" y1="{cy-30}" x2="254" y2="{cy-26}" stroke="{INK}" stroke-width="0.5"/>')
    # 犁壁
    s.append(f'<path d="M212,{cy+2} L240,{cy+2} L246,{cy+16} L232,{cy+18} Z" fill="#DDD5C6" stroke="{INK}" stroke-width="0.8"/>')
    # 犁铧
    s.append(f'<path d="M206,{cy+10} L232,{cy+18} L214,{cy+34} Z" fill="{INK}" opacity="0.72"/>')
    s.append(f'<line x1="206" y1="{cy+10}" x2="232" y2="{cy+18}" stroke="{INK}" stroke-width="0.5"/>')
    # 翻起的土
    for tx in (196, 244, 262):
        s.append(f'<path d="M{tx},{cy+34} q4,-5 8,-2 q4,3 8,-1" fill="none" stroke="{GREEN}" stroke-width="0.4" opacity="0.7"/>')
    s.append(txt(238, cy + 52, "为生而用：刀形还在，只是改成往前拉", 4.6, GREEN, "middle"))

    b = cy + 64
    rows = [
        ("一 · 收物", "粪，《说文》「弃除也」：把不要的扫出来，再送回田里。"),
        ("二 · 收力", "却，《说文》「节欲也」：马不是自己回来的，是人先把手收住。"),
        ("三 · 换用途", "没说不要马。那个时代最贵的军资，降成最贱的农具。"),
        ("四 · 边界", "刀改犁，是把「推出去」改成「收回来」；边界不再往外长。"),
    ]
    for k, (tag, line) in enumerate(rows):
        r = b + k * 40
        s.append(txt(24, r, tag, 5.6, SEAL))
        s.append(txt(88, r, line, 5.5, INK))

    y2 = b + 4 * 40 + 2
    s.append(f'<line x1="24" y1="{y2-6}" x2="338" y2="{y2-6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 4, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 20, "不是把刀收了，是把刀改成了犁。", 6.4, INK, "middle"))
    s.append(txt(190, y2 + 34, "一件为杀而生的东西，改成一件为生而用的东西。", 5.8, GREEN, "middle"))
    s.append(gold(y2 + 62, "ch46b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十六章 · 三个足 ============
def ch46c_san_ge_zu():
    W, H = 380, 512
    body, y = head(W, H, "先站住，才够；先够，永远不够", "第 四 十 六 章 · 足",
                   "一句话里三个「足」", "故知足之足，常足矣。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "第一个足是脚，第二个足是够，第三个足是一直站着。", 5.9, INK, "middle"))
    s.append(txt(190, y + 26, "书上说：用「知道脚站在哪儿」的那个足，去换「够」的那个足。", 5.4, "#6E6459", "middle"))

    a = y + 46
    s.append(txt(24, a + 6, "一 · 第一个足：脚", 5.9, INK))
    gy = a + 74
    # 左：地在这里
    s.append(f'<line x1="24" y1="{gy}" x2="126" y2="{gy}" stroke="{INK}" stroke-width="1"/>')

    def foot(cx, cy, col, dash=""):
        d = f' stroke-dasharray="3 3"' if dash else ""
        o = []
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="7.4" ry="6" fill="none" stroke="{col}" stroke-width="0.7"{d}/>')
        o.append(f'<path d="M{cx-6},{cy-6} Q{cx-8.5},{cy-14} {cx-5},{cy-19} L{cx+5},{cy-19} Q{cx+8.5},{cy-14} {cx+6},{cy-6} Z" fill="none" stroke="{col}" stroke-width="0.7"{d}/>')
        o.append(f'<ellipse cx="{cx}" cy="{cy-23}" rx="10" ry="6" fill="none" stroke="{col}" stroke-width="0.7"{d}/>')
        for k, (dx, dy, r) in enumerate([(-9.5, -3, 2.5), (-4, -9, 2.2), (1.5, -11, 2.0), (7, -9, 1.9), (10.5, -3, 1.7)]):
            o.append(f'<circle cx="{cx+dx}" cy="{cy-23+dy}" r="{r}" fill="none" stroke="{col}" stroke-width="0.55"{d}/>')
        return o

    for part in foot(72, gy - 8, INK):
        s.append(part)
    s.append(txt(72, gy + 14, "站住：脚知道地在哪儿", 4.8, GREEN, "middle"))

    # 右：地没有了
    s.append(f'<path d="M134,{gy} q6,-4 12,0 q6,4 12,0 q6,-4 12,0 q6,4 12,0" fill="none" stroke="{INK}" stroke-width="0.4" opacity="0.25"/>')
    for part in foot(190, gy - 30, SEAL, "dash"):
        s.append(part)
    s.append(f'<path d="M183,{gy-8} v10 M197,{gy-8} v10" stroke="{SEAL}" stroke-width="0.3" stroke-dasharray="2 2"/>')
    s.append(f'<path d="M176,{gy+2} q14,6 28,0" fill="none" stroke="{SEAL}" stroke-width="0.3" stroke-dasharray="2 2"/>')
    s.append(txt(190, gy + 14, "还在往下探：底下没有地", 4.8, SEAL, "middle"))

    b = gy + 30
    s.append(txt(24, b + 4, "二 · 第二个足：够（门槛）", 5.9, INK))
    s.append(f'<path d="M30,{b+74} L96,{b+66} L96,{b+56} L162,{b+48} L162,{b+38} L228,{b+30} L228,{b+20} L294,{b+12}" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(300, b + 14, "够", 4.8, SEAL))
    s.append(txt(300, b + 26, "的门槛", 4.4, SEAL))
    s.append(txt(36, b + 90, "不知足的人：门槛一级一级往上，脚一直没落地。", 5.4, SEAL))

    c = b + 116
    s.append(txt(24, c, "三 · 第三个足：常——脚先落地，门槛就不动了。", 5.4, GREEN))

    y2 = c + 14
    s.append(f'<line x1="24" y1="{y2}" x2="338" y2="{y2}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, y2 + 8, 340, 44, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y2 + 24, "先站住，才够；先够，永远不够。", 6.4, INK, "middle"))
    s.append(txt(190, y2 + 38, "顺序不能倒：靠外物撑起来的「够」，是借来的。", 5.8, GREEN, "middle"))
    s.append(gold(y2 + 66, "ch46c"))
    s.append('</svg>')
    return "\n".join(s)

# ============ 第四十七章 · 一扇有格的窗 ============
def ch47a_you_ge_de_chuang():
    W, H = 380, 502
    body, y = head(W, H, "透过框看，看见的每一块都是真的", "第 四 十 七 章 · 牖",
                   "一扇有格的窗", "不窥于牖，以知天道。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「窥」，《说文》「小视也」——从孔里看，看见多少由孔决定。", 5.8, INK, "middle"))
    s.append(txt(190, y + 26, "「牖」，《说文》「穿壁以木为交窗」——你看见的每一块，都是被格出来的。", 5.2, "#6E6459", "middle"))

    a = y + 50
    ov = (66, a + 34, 108, 100)   # 窗洞 x,y,w,h
    cx, cyv, r = 120, a + 84, 64
    # 后面的整个太阳
    s.append(f'<circle cx="{cx}" cy="{cyv}" r="{r}" fill="#E8C9A0" opacity="0.9"/>')
    # 墙（四块），把洞留住
    wall = [(30, a + 12, 36, 138), (174, a + 12, 40, 138), (66, a + 12, 108, 22), (66, a + 134, 108, 22)]
    for (wx, wy, ww, wh) in wall:
        s.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    # 直棂：竖木条
    for k in range(5):
        s.append(f'<rect x="{74+k*22}" y="{ov[1]}" width="6" height="{ov[3]}" fill="{INK}" opacity="0.82"/>')
    s.append(f'<rect x="{ov[0]}" y="{ov[1]}" width="{ov[2]}" height="3" fill="{INK}" opacity="0.5"/>')
    # 虚线：太阳其实一直圆着
    s.append(f'<circle cx="{cx}" cy="{cyv}" r="{r+14}" fill="none" stroke="{INK}" stroke-width="0.5" stroke-dasharray="4 3" opacity="0.5"/>')
    s.append(f'<line x1="{cx+r}" y1="{cyv}" x2="222" y2="{cyv}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 2"/>')
    s.append(txt(250, cyv - 6, "框外：太阳一直圆着", 4.6, "#6E6459"))
    s.append(txt(250, cyv + 4, "你没看见的是这一段", 4.6, "#6E6459"))
    s.append(txt(120, a + 172, "窗内：太阳被切成五条——每一条都是真的", 4.8, SEAL, "middle"))

    b = a + 192
    s.append(txt(24, b, "不窥于牖，不是「别看」，是「别从那个洞看」。", 5.9, INK))
    s.append(txt(24, b + 16, "格是真的，天也是真的；可格在中间，天就被格说了算。", 5.6, "#6E6459"))
    s.append(txt(24, b + 32, "要知道天道，先得知道那个框是框，不是天。", 5.6, GREEN))

    c = b + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "透过框看，你看见的每一块都是真的；", 6.2, INK, "middle"))
    s.append(txt(190, c + 36, "可你真的没看见框外。", 6.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch47a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十七章 · 网越密，越看不见 ============
def ch47b_wang_yue_mi():
    W, H = 380, 470
    body, y = head(W, H, "其出弥远，其知弥少", "第 四 十 七 章 · 网",
                   "网越密，越看不见", "其出弥远，其知弥少。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「知」不是信息量，是「通」——知道这一件和那一件，是同一件事。", 5.6, INK, "middle"))
    s.append(txt(190, y + 26, "而「出」是采集：多一件，就多一条线；多一条线，就多一处要连的地方。", 5.2, "#6E6459", "middle"))

    a = y + 58
    cy = a + 62
    for i, (bx, n, lab) in enumerate([(66, 2, "刚出门：还看得见"),
                                     (190, 4, "走远了：线多了"),
                                     (312, 8, "走得很远：看不见了")]):
        s.append(f'<circle cx="{bx}" cy="{cy}" r="42" fill="{GREEN}" opacity="0.28"/>')
        s.append(f'<circle cx="{bx}" cy="{cy}" r="42" fill="none" stroke="{GREEN}" stroke-width="0.5" opacity="0.7"/>')
        s.append(f'<circle cx="{bx}" cy="{cy}" r="9" fill="{GREEN}" opacity="0.9"/>')
        step = 84 / (n + 1)
        for k in range(1, n + 1):
            off = -42 + k * step
            hh = (42 * 42 - off * off) ** 0.5
            s.append(f'<line x1="{bx+off:.1f}" y1="{cy-hh:.1f}" x2="{bx+off:.1f}" y2="{cy+hh:.1f}" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>')
            s.append(f'<line x1="{bx-hh:.1f}" y1="{cy+off:.1f}" x2="{bx+hh:.1f}" y2="{cy+off:.1f}" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>')
        s.append(txt(bx, cy + 56, lab, 4.6, "#6E6459", "middle"))

    b = cy + 76
    s.append(txt(24, b, "三个圆里是同一片「知」。网眼越密，中间那点亮越小；", 5.8, INK))
    s.append(txt(24, b + 16, "线都是你自己一条条捡回来的，捡得越多，越放不下。", 5.8, SEAL))
    s.append(txt(24, b + 32, "老子不是反对看；他反对把「向外看」当成求道的路。", 5.4, "#6E6459"))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "信息是捡回来的，通是放下去的；", 6.2, INK, "middle"))
    s.append(txt(190, c + 36, "捡得越多，越放不下。", 6.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch47b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十七章 · 十字路口 ============
def ch47c_shi_zi_lu_kou():
    W, H = 380, 508
    body, y = head(W, H, "站在路口的人只能选一条", "第 四 十 七 章 · 行",
                   "十字路口", "是以圣人不行而知。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「行」的甲骨文，就是十字路口：四条路通到一处。", 5.8, INK, "middle"))
    s.append(txt(190, y + 26, "所以「不行而知」不是不走路，是「不站在那个路口」。", 5.4, "#6E6459", "middle"))

    a = y + 52
    cx, cy = 150, a + 66
    s.append(f'<rect x="{cx-24}" y="{a+8}" width="48" height="130" fill="#EFE6D4" stroke="{INK}" stroke-width="0.5" opacity="0.8"/>')
    s.append(f'<rect x="{cx-70}" y="{cy-24}" width="140" height="48" fill="#EFE6D4" stroke="{INK}" stroke-width="0.5" opacity="0.8"/>')
    s.append(f'<line x1="{cx-14}" y1="{cy}" x2="{cx-40}" y2="{cy}" stroke="{LINE2}" stroke-width="0.3" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{cx+14}" y1="{cy}" x2="{cx+40}" y2="{cy}" stroke="{LINE2}" stroke-width="0.3" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{cx}" y1="{cy-14}" x2="{cx}" y2="{cy-52}" stroke="{LINE2}" stroke-width="0.3" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{cx}" y1="{cy+14}" x2="{cx}" y2="{cy+52}" stroke="{LINE2}" stroke-width="0.3" stroke-dasharray="4 3"/>')
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        s.append(f'<line x1="{cx+dx*16}" y1="{cy+dy*16}" x2="{cx+dx*58}" y2="{cy+dy*58}" stroke="{SEAL}" stroke-width="0.7" marker-end="url(#arrS)" opacity="0.9"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>')
    s.append(txt(cx, cy + 86, "选一条，就走不成那三条", 4.8, SEAL, "middle"))

    s.append(txt(258, a + 40, "路是同一套走法：", 5.0, GREEN))
    s.append(txt(258, a + 54, "反、弱、有无相生、", 5.4, GREEN))
    s.append(txt(258, a + 66, "冲气为和。", 5.4, GREEN))
    s.append(txt(258, a + 84, "知道一处，就通了全部。", 5.4, GREEN))
    s.append(f'<line x1="252" y1="{a+96}" x2="338" y2="{a+96}" stroke="{LINE2}" stroke-width="0.4"/>')
    s.append(txt(258, a + 110, "知道走法的人，", 4.8, "#6E6459"))
    s.append(txt(258, a + 120, "站不站在路口都一样。", 4.8, "#6E6459"))

    b = a + 178
    s.append(txt(24, b, "不行而知，不是不走路：天下不是一堆散事，是一套统一的运化。", 5.6, INK))
    s.append(txt(24, b + 16, "散事只能一件件去看；一套机制，知道一处就通了全部。", 5.6, INK))
    s.append(txt(24, b + 32, "这就是「不出户」能成立的全部理由：他看的不是多，是那一条律。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "站在路口的人只能选一条路；", 6.2, INK, "middle"))
    s.append(txt(190, c + 36, "知道路怎么走的人，不必选。", 6.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch47c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十八章 · 益与损 ============
def ch48a_yi_yu_sun():
    W, H = 380, 500
    body, y = head(W, H, "学是加法，道是减法", "第 四 十 八 章 · 益损",
                   "一只器，两只手", "为学日益，为道日损。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「益」，《说文》「饶也」——字形是水在皿上，水满出来了。", 5.8, INK, "middle"))
    s.append(txt(190, y + 26, "「损」，《说文》「减也」——从手：一只手从器物上把东西拿掉。", 5.4, "#6E6459", "middle"))

    a = y + 48
    # 左：益（水自己涨出来）
    s.append(txt(86, a + 8, "一 · 益：水自己往外涨", 5.6, SEAL, "middle"))
    mx, my = 86, a + 78
    s.append(f'<path d="M{mx-36},{my-4} L{mx-26},{my+34} Q{mx},{my+44} {mx+26},{my+34} L{mx+36},{my-4} Z" fill="#F0E8D8" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{mx-38}" y1="{my-4}" x2="{mx+38}" y2="{my-4}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M{mx-36},{my-6} q10,4 20,0 q10,-4 20,0 q10,4 20,0" fill="none" stroke="{GREEN}" stroke-width="0.6"/>')
    for dx, dy in ((-38, -2), (-34, 8), (36, 0), (32, 10)):
        s.append(f'<path d="M{mx+dx},{my+dy} q2,5 0,8 q-3,-4 0,-8" fill="none" stroke="{GREEN}" stroke-width="0.5"/>')
    for k in range(3):
        s.append(f'<line x1="{mx-20+k*20}" y1="{my-14}" x2="{mx-20+k*20}" y2="{my-26}" stroke="{SEAL}" stroke-width="0.5" marker-end="url(#arrS)"/>')
    s.append(txt(86, a + 128, "加到一个程度，就不是「有」了", 4.6, "#6E6459", "middle"))
    s.append(txt(86, a + 140, "是「漫出来」", 4.6, "#6E6459", "middle"))

    # 右：损（一只手往外拿）
    s.append(txt(274, a + 8, "二 · 损：手把它拿掉", 5.6, GREEN, "middle"))
    cx = 274
    s.append(f'<rect x="{cx-30}" y="{a+56}" width="60" height="58" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx-30}" y1="{a+70}" x2="{cx+30}" y2="{a+70}" stroke="{GREEN}" stroke-width="0.5"/>')
    s.append(f'<path d="M{cx-28},{a+72} q9,3 18,0 q9,-3 18,0 q9,3 18,0" fill="none" stroke="{GREEN}" stroke-width="0.45" opacity="0.8"/>')
    # 拿走的一块
    s.append(f'<rect x="{cx-9}" y="{a+30}" width="18" height="13" fill="#DDD5C6" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<line x1="{cx}" y1="{a+30}" x2="{cx}" y2="{a+16}" stroke="{GREEN}" stroke-width="0.5" marker-end="url(#arr2)"/>')
    # 一只手（伸向杯口，往外拿）
    s.append(f'<ellipse cx="{cx+34}" cy="{a+34}" rx="12" ry="9" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    for k in range(4):
        s.append(f'<line x1="{cx+26}" y1="{a+28+k*4}" x2="{cx+8}" y2="{a+27+k*4}" stroke="{INK}" stroke-width="0.5"/>')
    s.append(f'<path d="M{cx+42},{a+42} q8,4 6,12" fill="none" stroke="{INK}" stroke-width="0.6"/>')
    s.append(txt(274, a + 128, "拿掉的是粘在上面的那层", 4.6, "#6E6459", "middle"))
    s.append(txt(274, a + 140, "不是杯子本身", 4.6, "#6E6459", "middle"))

    s.append(f'<line x1="188" y1="{a+20}" x2="188" y2="{a+120}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="4 3"/>')

    b = a + 164
    s.append(txt(24, b, "益是水自己涨出来，损是手往外拿；涨不由人，拿要人动手。", 5.8, INK))
    s.append(txt(24, b + 16, "学，是往心里装「有」：一个概念一道边，一个标签一道边。", 5.4, "#6E6459"))
    s.append(txt(24, b + 32, "损，是把粘在「知道」上面的那层执取拿掉——知识还留着。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "学问把世界切得越来越细，切得越细越好用；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "可那条「通」，恰恰不在细处。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch48a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十八章 · 一层套一层的壳 ============
def ch48b_ceng_ke():
    W, H = 380, 646
    body, y = head(W, H, "同一张框：往外推是学，把手松是道", "第 四 十 八 章 · 一图两观",
                   "一图两观", "为学日益，为道日损。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「学」把框往外推，一天多一层；「道」把线往里损，一天少一层。", 5.6, INK, "middle"))
    s.append(txt(190, y + 26, "同一个框，两种读法——这就是「益」和「损」是同一件事的两面。", 5.2, "#6E6459", "middle"))

    a = y + 52
    cx, cy = 132, a + 92
    layers = [
        (16, INK, 1, 0.95, ""),
        (36, INK, 0.8, 0.62, ""),
        (56, SEAL, 0.7, 0.8, "4 3"),
        (76, SEAL, 0.5, 0.35, "5 4"),
    ]
    for (hl, col, w, op, d) in layers:
        dash = f' stroke-dasharray="{d}"' if d else ""
        s.append(f'<rect x="{cx-hl}" y="{cy-hl}" width="{2*hl}" height="{2*hl}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"{dash}/>')

    # 学：同一个角，往外推
    s.append(f'<line x1="{cx+12}" y1="{cy+12}" x2="{cx+84}" y2="{cy+84}" stroke="{SEAL}" stroke-width="0.7" marker-end="url(#arrS)"/>')
    s.append(txt(cx + 40, cy + 100, "学：同一个角往外推，框就大一圈、多一层", 4.8, SEAL))

    # 道：同一条边的四种线质（右侧小图例）
    lx = cx + 88
    s.append(txt(lx, cy - 62, "道：同一条边，一路淡下去", 4.8, GREEN))
    for k, (lw, lop, ld, lab) in enumerate([(0.9, 0.95, "", "一 · 实线"),
                                            (0.8, 0.6, "", "二 · 淡实线"),
                                            (0.7, 0.75, "4 3", "三 · 虚线"),
                                            (0.5, 0.35, "5 4", "四 · 几乎没了")]):
        ly = cy - 44 + k * 22
        dash = f' stroke-dasharray="{ld}"' if ld else ""
        s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+42}" y2="{ly}" stroke="{SEAL}" stroke-width="{lw}" opacity="{lop}"{dash}/>')
        s.append(txt(lx + 48, ly + 2, lab, 4.5, "#6E6459"))

    # 中间过程：一条边还实着，一条边已经虚了
    mb = cy + 126
    s.append(f'<line x1="24" y1="{mb}" x2="338" y2="{mb}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(24, mb + 15, "中间过程：一个框正处在半中间", 5.4, SEAL))
    fx, fy, fh = 58, mb + 62, 26
    s.append(f'<line x1="{fx-fh}" y1="{fy-fh}" x2="{fx+fh}" y2="{fy-fh}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{fx+fh}" y1="{fy-fh}" x2="{fx+fh}" y2="{fy+fh}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{fx+fh}" y1="{fy+fh}" x2="{fx-fh}" y2="{fy+fh}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3.4 2.6"/>')
    s.append(f'<line x1="{fx-fh}" y1="{fy+fh}" x2="{fx-fh}" y2="{fy-fh}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3.4 2.6"/>')
    s.append(f'<path d="M{fx-fh},{fy-fh} l6,-2 M{fx-fh},{fy-fh} l2,-6" stroke="{SEAL}" stroke-width="0.6" fill="none"/>')
    s.append(txt(fx + fh + 8, fy - 16, "上、右两条边：还硬着，撑得住", 4.7, INK))
    s.append(txt(fx + fh + 8, fy - 4, "下、左两条边：已经虚了，不再划人", 4.7, SEAL))
    s.append(txt(fx + fh + 8, fy + 8, "越往下走，实的那两条边也一条条虚掉", 4.7, "#6E6459"))
    s.append(txt(24, mb + 104, "所以「损之又损」不是一次全破：是先破一边，再破一边。", 5.2, GREEN))

    b = mb + 128
    s.append(txt(24, b, "往外读：框一层层变大——这是为学，越学越细，越细越好用。", 5.6, INK))
    s.append(txt(24, b + 16, "读线：每一条边由实变虚——这是为道，不是拆掉框，是让它不再硬着。", 5.6, INK))
    s.append(txt(24, b + 32, "同一张图：你把它往外推，它就多一层；你把手松开，它就淡一层。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "框是同一个框；加和减，是同一只手的两件事。", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "推到极处，框最大、线最淡——那就是无为。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch48b"))
    s.append('</svg>')
    return "\n".join(s)

# ============ 第四十八章 · 一道关，一道关 ============
def ch48c_guan_qia():
    W, H = 380, 512
    body, y = head(W, H, "不是懒，是勤得太多", "第 四 十 八 章 · 事",
                   "一道关，一道关", "取天下常以无事，及其有事，不足以取天下。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「事」，《说文》「职也」：无事不是什么都不干，是不给自己加职分。", 5.5, INK, "middle"))
    s.append(txt(190, y + 26, "「取」，《说文》「捕取也」——从又从耳：割左耳计功的那个取。", 5.4, SEAL, "middle"))

    a = y + 50
    # 上：有事
    s.append(txt(24, a + 8, "一 · 有事：一道关、一道关往上加", 5.6, SEAL))
    gy = a + 56
    s.append(f'<line x1="24" y1="{gy}" x2="338" y2="{gy}" stroke="{INK}" stroke-width="0.8"/>')
    for k in range(3):
        gx = 74 + k * 74
        s.append(f'<line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy-26}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{gx+22}" y1="{gy}" x2="{gx+22}" y2="{gy-26}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{gx-3}" y1="{gy-24}" x2="{gx+25}" y2="{gy-24}" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(36, gy + 28, "每干一件，就多一道边；守的地方越多，漏的地方越多。", 4.8, "#6E6459"))

    b = gy + 48
    # 下：无事
    s.append(txt(24, b + 8, "二 · 无事：一道也不设", 5.6, GREEN))
    gy2 = b + 56
    s.append(f'<line x1="24" y1="{gy2}" x2="338" y2="{gy2}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="28" y1="{gy2-11}" x2="334" y2="{gy2-11}" stroke="{GREEN}" stroke-width="0.35" stroke-dasharray="6 5" opacity="0.6"/>')
    for k in range(3):
        gx = 90 + k * 74
        s.append(f'<line x1="{gx}" y1="{gy2}" x2="{gx}" y2="{gy2-24}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 3"/>')
        s.append(f'<line x1="{gx+22}" y1="{gy2}" x2="{gx+22}" y2="{gy2-24}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 3"/>')
        s.append(f'<line x1="{gx-3}" y1="{gy2-22}" x2="{gx+25}" y2="{gy2-22}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 3"/>')
    s.append(txt(300, gy2 - 32, "虚线：本该有的关，一道也没设", 4.4, "#6E6459", "middle"))
    s.append(txt(36, gy2 + 28, "不新立法度，不频出号令，不年年加码。", 4.8, "#6E6459"))

    c = gy2 + 48
    s.append(txt(24, c, "那个时代最好的治理，是让人感觉不到有人在管。", 5.6, INK))
    s.append(txt(24, c + 16, "一个上位者最容易犯的，不是懒，是勤——他总想再干点什么。", 5.6, SEAL))

    d = c + 42
    s.append(f'<line x1="24" y1="{d}" x2="338" y2="{d}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, d + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, d + 24, "「取天下」的「取」是割耳朵，所以老子换了个动作：", 6.0, INK, "middle"))
    s.append(txt(190, d + 36, "不是割，是不动。", 6.0, SEAL, "middle"))
    s.append(gold(d + 62, "ch48c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第四十九章 · 一把尺 ============
def ch49a_yi_ba_chi():
    W, H = 380, 646
    body, y = head(W, H, "常心是一把自己打的尺：一把尺能定长短，也能把人钉在短的那一格里",
                   "第 四 十 九 章 · 尺 与 气", "一把尺，一口气", "圣人无常心，以百姓心为心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「常心」听着像常理，其实是自己打的尺；尺一伸出去，话就跟着出去。", 5.4, INK, "middle"))
    s.append(txt(190, y + 26, "量人是一口气往外吐，放下是一口气往里吸——同一件事的两头。", 5.2, "#6E6459", "middle"))

    posts = [(66, 84, "甲", "合格"), (136, 58, "乙", "不合格"), (206, 34, "丙", "不合格")]

    # 一、有常心：一把尺，几道格
    t1 = y + 46
    s.append(txt(24, t1, "一、有常心：一把尺横在人头顶", 5.4, SEAL))
    gy1 = t1 + 104
    s.append(box(294, gy1 - 100, 10, 100, fill="#EFE6D4", stroke=INK, width=0.8))
    for k in range(7):
        ty = gy1 - 13 * (k + 1)
        s.append(f'<line x1="{286 if k % 2 == 0 else 289}" y1="{ty}" x2="294" y2="{ty}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(f'<line x1="40" y1="{gy1-64}" x2="294" y2="{gy1-64}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="5 3"/>')
    s.append(txt(30, gy1 - 68, "合格线", 4.6, SEAL))
    for (cx, hh, lab, verdict) in posts:
        s.append(box(cx - 9, gy1 - hh, 18, hh, fill="#EFE6D4", stroke=INK, width=0.8))
        s.append(f'<line x1="{cx-9}" y1="{gy1-hh}" x2="{cx+9}" y2="{gy1-hh}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{cx+9}" y1="{gy1-hh}" x2="294" y2="{gy1-hh}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 3"/>')
        s.append(txt(cx, gy1 + 11, lab + " · " + verdict, 4.6, GREEN if verdict == "合格" else SEAL, "middle"))
    s.append(txt(210, gy1 + 26, "尺一横过来，人就成了几格里的一个读数", 4.6, "#6E6459"))
    s.append(arrow(306, gy1 - 50, 336, gy1 - 50, SEAL, 0.9, head="arrS"))
    s.append(txt(340, gy1 - 48, "吐", 6.2, SEAL))
    s.append(txt(306, gy1 - 36, "标准、评判", 4.4, SEAL))
    s.append(txt(306, gy1 - 26, "一整套「应该」", 4.4, SEAL))

    # 二、无常心：尺放下
    t2 = gy1 + 46
    s.append(txt(24, t2, "二、无常心：尺还在，只是不再横在人头顶", 5.4, GREEN))
    gy2 = t2 + 104
    for (cx, hh, lab, verdict) in posts:
        s.append(box(cx - 9, gy2 - hh, 18, hh, fill="#EFE6D4", stroke=INK, width=0.8))
        s.append(f'<line x1="{cx-9}" y1="{gy2-hh}" x2="{cx+9}" y2="{gy2-hh}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(txt(cx, gy2 + 11, lab, 4.8, "#6E6459", "middle"))
    # 尺躺下
    s.append(f'<rect x="52" y="{gy2 + 40}" width="196" height="11" fill="#EFE6D4" stroke="{GREEN}" stroke-width="0.8"/>')
    for k in range(9):
        s.append(f'<line x1="{62 + k * 21}" y1="{gy2+40}" x2="{62 + k * 21}" y2="{gy2+46}" stroke="{GREEN}" stroke-width="0.4"/>')
    s.append(txt(254, gy2 + 42, "尺收回来了：还在，", 4.5, GREEN))
    s.append(txt(254, gy2 + 52, "只是不量人了", 4.5, GREEN))
    s.append(arrow(306, gy2 - 34, 236, gy2 - 34, GREEN, 0.9, head="arr2"))
    s.append(txt(340, gy2 - 32, "吸", 6.2, GREEN))
    s.append(txt(306, gy2 - 44, "往里收", 4.4, GREEN))
    s.append(txt(24, gy2 - 46, "三个人还是三个高度，各自一个尺寸", 4.6, "#6E6459"))

    b = gy2 + 72
    s.append(txt(24, b, "量人和吐气是同一个动作：尺一伸出去，话就跟着出去。", 5.6, INK))
    s.append(txt(24, b + 16, "「以百姓心为心」不是照他们说的做，是不把人划到哪一栏里去。", 5.6, INK))
    s.append(txt(24, b + 32, "把尺收回来，气才收得住——放下尺不是失去标准，是不再拿它钉人。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "一把尺能定长短，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "也能把人钉在短的那一格里。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch49a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十九章 · 一吸一灌 ============
def ch49b_yi_xi_yi_guan():
    W, H = 380, 560
    body, y = head(W, H, "百姓把耳目当灌渠往外灌，圣人往里吸",
                   "第 四 十 九 章 · 吸 与 灌", "一吸一灌", "歙歙焉，为天下浑其心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「歙」，《说文》「缩鼻也」——鼻子往里一缩，吸气。", 5.6, INK, "middle"))
    s.append(txt(190, y + 26, "「注」，《说文》「灌也」——水往外灌。全章的对位就在这一呼一吸上。", 5.2, "#6E6459", "middle"))

    # 一、注：灌
    t1 = y + 46
    s.append(txt(24, t1, "一、注：耳目是两条灌渠，往外灌", 5.4, SEAL))
    cy1 = t1 + 64
    s.append(f'<circle cx="150" cy="{cy1}" r="26" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(150, cy1 - 34, "百姓", 5.0, "#6E6459", "middle"))
    s.append(f'<circle cx="140" cy="{cy1-6}" r="1.7" fill="{INK}"/><circle cx="160" cy="{cy1-6}" r="1.7" fill="{INK}"/>')
    # 两条渠
    for (xl, yc) in ((46, cy1), ):
        pass
    s.append(f'<rect x="52" y="{cy1+2}" width="72" height="9" fill="#EFE6D4" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<rect x="176" y="{cy1+2}" width="72" height="9" fill="#EFE6D4" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(arrow(120, cy1 + 6.5, 56, cy1 + 6.5, SEAL, 0.9, head="arrS"))
    s.append(arrow(180, cy1 + 6.5, 244, cy1 + 6.5, SEAL, 0.9, head="arrS"))
    s.append(f'<circle cx="40" cy="{cy1+16}" r="2.2" fill="{SEAL}" opacity="0.55"/>')
    s.append(f'<circle cx="262" cy="{cy1+16}" r="2.2" fill="{SEAL}" opacity="0.55"/>')
    s.append(txt(88, cy1 + 26, "眼睛、耳朵：两条朝外的渠", 4.6, SEAL, "middle"))
    s.append(txt(212, cy1 + 26, "水一开就关不上", 4.6, SEAL, "middle"))

    # 二、歙：吸
    t2 = cy1 + 52
    s.append(f'<line x1="24" y1="{t2-8}" x2="338" y2="{t2-8}" stroke="{LINE}" stroke-width="0.6"/>')
    t2b = t2 + 12
    s.append(txt(24, t2b, "二、歙：缩鼻，往里收，不往外吐", 5.4, GREEN))
    cy2 = t2b + 64
    s.append(f'<circle cx="150" cy="{cy2}" r="26" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(150, cy2 - 34, "圣人", 5.0, "#6E6459", "middle"))
    s.append(f'<circle cx="140" cy="{cy2-6}" r="1.7" fill="{INK}"/><circle cx="160" cy="{cy2-6}" r="1.7" fill="{INK}"/>')
    s.append(f'<circle cx="150" cy="{cy2+4}" r="1.7" fill="{SEAL}"/>')
    s.append(arrow(252, cy2 + 4, 178, cy2 + 4, GREEN, 0.9, head="arr2"))
    s.append(txt(256, cy2 - 2, "一口往里吸", 4.6, GREEN))
    s.append(txt(256, cy2 + 10, "不出声，不吐气", 4.6, GREEN))
    s.append(txt(150, cy2 + 42, "吐出去的多是标准、评判、一整套「应该怎样」", 4.6, "#6E6459", "middle"))

    b = cy2 + 58
    s.append(txt(24, b, "大家都往外灌，就没人吸；没人吸，那个场就干了。", 5.6, INK))
    s.append(txt(24, b + 16, "注是结构，不是罪状：眼睛看什么，心就在哪儿。", 5.6, INK))
    s.append(txt(24, b + 32, "所以圣人第一件事不是多说，是把灌口往回收一寸。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「歙」是吸，「注」是灌；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一个往里收，一个往外倒。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch49b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第四十九章 · 浑 ============
def ch49c_hun_shui_sheng():
    W, H = 380, 566
    body, y = head(W, H, "浑是水混着流的声音：水还在流，只是不再一格一格地流",
                   "第 四 十 九 章 · 浑", "浑，是水声", "为天下浑其心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「浑」，《说文》「混流声也」——水混着流的声音。", 5.6, INK, "middle"))
    s.append(txt(190, y + 26, "不是糊涂，不是把人弄傻：是让被切碎的心重新连成一片。", 5.2, "#6E6459", "middle"))

    # 一、一格一格
    t1 = y + 46
    s.append(txt(24, t1, "一、一格一格：每滴都在自己的格子里", 5.4, SEAL))
    ty, by = t1 + 26, t1 + 78
    s.append(f'<line x1="30" y1="{by}" x2="350" y2="{by}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="30" y1="{ty}" x2="350" y2="{ty}" stroke="{LINE}" stroke-width="0.6"/>')
    for xv in (30, 94, 158, 222, 286, 350):
        s.append(f'<line x1="{xv}" y1="{ty}" x2="{xv}" y2="{by}" stroke="{INK}" stroke-width="0.9"/>')
    cells = [(30, 94), (94, 158), (158, 222), (222, 286), (286, 350)]
    for (xa, xb) in cells:
        wy = by - 22
        s.append(f'<line x1="{xa+6}" y1="{wy}" x2="{xb-6}" y2="{wy}" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(txt(30, by + 14, "墙一道一道立着：好坏、得失、敌我，每一刀都切得很准", 4.6, "#6E6459"))

    # 二、浑
    t2 = by + 34
    s.append(txt(24, t2, "二、浑：墙软下来，水连成一片", 5.4, GREEN))
    ty2, by2 = t2 + 26, t2 + 78
    s.append(f'<line x1="30" y1="{by2}" x2="350" y2="{by2}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="30" y1="{ty2}" x2="350" y2="{ty2}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="4 3"/>')
    for xv in (30, 350):
        s.append(f'<line x1="{xv}" y1="{ty2}" x2="{xv}" y2="{by2}" stroke="{INK}" stroke-width="0.9"/>')
    for xv in (94, 158, 222, 286):
        s.append(f'<line x1="{xv}" y1="{ty2}" x2="{xv}" y2="{by2}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="3 3"/>')
    s.append(f'<path d="M34,{by2-22} q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0" '
             f'fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(arrow(70, ty2 + 14, 200, ty2 + 14, GREEN, 0.7, head="arr2"))
    s.append(txt(206, ty2 + 16, "还是有流向", 4.6, GREEN))
    s.append(txt(30, by2 + 14, "格子软了，水重新连成一片；不是没有分别，是不再一格一格站着", 4.6, "#6E6459"))

    b = by2 + 36
    s.append(txt(24, b, "一个时代的心被切碎，不是切得不准，是切得太准。", 5.6, INK))
    s.append(txt(24, b + 16, "每一刀都对，可每个人都站进了一个很小的格子。", 5.6, INK))
    s.append(txt(24, b + 32, "浑，是把格子的墙软下来——水才又能流到别人那儿去。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「浑」是水声，不是糊涂；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "水还在流，只是不再一格一格地流。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch49c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十章 · 一条路 ============
def ch50a_yi_tiao_lu():
    W, H = 380, 566
    body, y = head(W, H, "出生入死是一条路的两头，不是两扇门；三成是天给的，三成是自己走进去的",
                   "第 五 十 章 · 路", "一条路的两头", "出生入死。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「出生入死」不是两扇门，是一条路的两头：从出来的那一处，往进去的那一处走。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "「徒」，《说文》「步行也」——这三成不是三个命定，是三个方向。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "一条路，三种走法", 5.4, SEAL))
    gy = t1 + 96
    top, bot = gy - 16, gy + 16
    s.append(f'<rect x="30" y="{top}" width="320" height="40" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<line x1="34" y1="{gy}" x2="346" y2="{gy}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="6 5"/>')
    s.append(txt(30, top - 10, "出 · 生", 5.0, GREEN))
    s.append(txt(306, top - 10, "入 · 死", 5.0, SEAL))

    # 生之徒：走上缘
    for k, (px, py) in enumerate([(70, top + 6), (146, top + 6), (222, top + 6)]):
        s.append(f'<circle cx="{px}" cy="{py}" r="2.6" fill="{GREEN}" opacity="{0.9-k*0.15}"/>')
    # 死之徒：走下缘
    for k, (px, py) in enumerate([(70, bot - 6), (140, bot - 6), (210, bot - 6)]):
        s.append(f'<circle cx="{px}" cy="{py}" r="2.6" fill="{INK}" opacity="{0.9-k*0.15}"/>')
    # 亦十有三：自己拐下去
    s.append(f'<circle cx="44" cy="{gy}" r="2.6" fill="{SEAL}"/>')
    s.append(f'<circle cx="92" cy="{gy+3}" r="2.6" fill="{SEAL}" opacity="0.8"/>')
    s.append(f'<circle cx="138" cy="{gy+6}" r="2.6" fill="{SEAL}" opacity="0.6"/>')
    s.append(f'<line x1="146" y1="{gy+8}" x2="182" y2="{bot+26}" stroke="{SEAL}" stroke-width="0.8" marker-end="url(#arrS)"/>')
    s.append(f'<ellipse cx="200" cy="{bot+32}" rx="17" ry="6" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(txt(222, bot + 34, "死地：自己堆的土，塌成坑", 4.6, SEAL))

    ly = bot + 42
    for k, (col, lab) in enumerate([(GREEN, "生之徒：顺守生机，十有三"),
                                    (INK, "死之徒：禀赋耗散，十有三"),
                                    (SEAL, "亦十有三：自己走进去的")]):
        s.append(f'<circle cx="34" cy="{ly + k*16 - 2}" r="2.4" fill="{col}"/>')
        s.append(txt(44, ly + k * 16, lab, 4.8, "#6E6459"))

    b = ly + 62
    s.append(txt(24, b, "本来就有一批人容易早亡，那是禀赋与外缘；另外那一批，是自己动手把自己送进去的。", 5.2, INK))
    s.append(txt(24, b + 16, "而这后一批，恰恰是最用心养生的那一批。", 5.2, INK))
    s.append(txt(24, b + 32, "那个「亦」字，是老子全章唯一想说的。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "三成是天给的，三成是自己走进去的；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "这个「亦」字，是老子唯一想说的那句。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch50a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十章 · 一把土 ============
def ch50b_yi_ba_tu():
    W, H = 380, 556
    body, y = head(W, H, "厚、重、沉、地：厚和地是同一个方向，都是往下堆",
                   "第 五 十 章 · 土", "一把土", "以其生生之厚。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「厚」是堆；「地」，《说文》「重浊阴为地」——重的东西沉下来，堆成那一层。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以「死地」不是会死的地方，是已经堆成土的那一层。", 5.2, "#6E6459", "middle"))

    # 一、薄
    t1 = y + 46
    s.append(txt(24, t1, "一、薄：气还通，脚下没有那一层", 5.4, GREEN))
    g1 = t1 + 62
    s.append(f'<line x1="30" y1="{g1}" x2="350" y2="{g1}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="30" y="{g1}" width="320" height="4" fill="#EFE6D4" stroke="{LINE}" stroke-width="0.35"/>')
    for dx in (96, 128, 160):
        s.append(f'<circle cx="{dx}" cy="{g1+9}" r="1.4" fill="{LINE2}" opacity="0.8"/>')
    s.append(arrow(250, g1 - 46, 250, g1 + 2, "#6E6459", 0.8, head="arr"))
    s.append(txt(258, g1 - 30, "角、爪、刃都找不到落点", 4.6, "#6E6459"))
    s.append(txt(258, g1 - 18, "薄薄一层，一按就散", 4.6, "#6E6459"))

    # 二、厚
    t2 = g1 + 40
    s.append(txt(24, t2, "二、厚：一层一层往上堆，堆成一层土", 5.4, SEAL))
    g2 = t2 + 94
    s.append(f'<line x1="30" y1="{g2}" x2="350" y2="{g2}" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(4):
        ly = g2 - 8 * (k + 1)
        s.append(f'<line x1="56" y1="{ly}" x2="304" y2="{ly}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(f'<rect x="56" y="{g2-32}" width="248" height="32" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9" opacity="0.9"/>')
    for k in range(3):
        ly = g2 - 8 * (k + 1)
        s.append(f'<line x1="58" y1="{ly}" x2="302" y2="{ly}" stroke="{LINE}" stroke-width="0.45"/>')
    # 硬壳面 + 被钉住的落点
    s.append(f'<line x1="56" y1="{g2-32}" x2="304" y2="{g2-32}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(arrow(250, g2 - 64, 250, g2 - 32, SEAL, 0.9, head="arrS"))
    s.append(f'<path d="M244,{g2-34} l6,-5 M250,{g2-34} l-6,-5" stroke="{SEAL}" stroke-width="0.7" fill="none"/>')
    s.append(txt(258, g2 - 62, "厚到成层，就硬成一块壳", 4.6, SEAL))
    s.append(txt(258, g2 - 50, "每一处硬，都是一个落点", 4.6, SEAL))
    s.append(txt(24, g2 - 44, "厚 → 重 → 沉 → 地 → 死地", 5.0, SEAL))
    s.append(txt(10, g2 - 8, "补品、防护", 4.5, "#6E6459"))
    s.append(txt(10, g2 + 12, "一层一层堆", 4.5, "#6E6459"))

    b = g2 + 40
    s.append(txt(24, b, "堆的不是坏东西：补品、防护、一整套「我在养」的念头，一样一样都出于好意。", 5.2, INK))
    s.append(txt(24, b + 16, "可「厚」这个字的方向是往下：厚的东西沉，沉到底，就成了地。", 5.2, INK))
    s.append(txt(24, b + 32, "死地不是命给的，是自己一锹一锹堆起来的；撤土比加甲难。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「厚」和「地」是同一个方向：都是往下堆；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "堆到成层，人就站在自己堆的那块土上。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch50b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十章 · 一只角 ============
def ch50c_yi_zhi_jiao():
    W, H = 380, 598
    body, y = head(W, H, "兕无所投其角：不是伤害不来，是伤害找不到落点",
                   "第 五 十 章 · 角", "一只角", "兕无所投其角，虎无所用其爪。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "角要顶穿一样东西，得有一个硬的点；爪要抓，得有一处能挂住的地方。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "不是「伤害不来」，是「伤害找不到落点」。", 5.2, "#6E6459", "middle"))

    def horn(x0, cy, ln=108):
        tip = x0 + ln
        up = f"M{x0},{cy-11} C{x0+46},{cy-17} {tip-40},{cy-13} {tip},{cy}"
        dn = f"C{tip-40},{cy+13} {x0+46},{cy+17} {x0},{cy+11}"
        return [f'<path d="{up} {dn} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>',
                f'<path d="M{x0},{cy-11} q-7,11 0,22" fill="none" stroke="{INK}" stroke-width="0.7"/>',
                f'<line x1="{x0+18}" y1="{cy-13}" x2="{x0+18}" y2="{cy+13}" stroke="{LINE}" stroke-width="0.35"/>',
                f'<line x1="{x0+52}" y1="{cy-12}" x2="{x0+52}" y2="{cy+12}" stroke="{LINE}" stroke-width="0.35"/>']

    # 一、抵硬壳：穿进去了
    t1 = y + 46
    s.append(txt(24, t1, "一、一身设防：每一道防线都是一个可破的点", 5.4, SEAL))
    cy1 = t1 + 66
    s.append(box(202, cy1 - 40, 14, 80, fill="#EFE6D4", stroke=INK, width=1.4))
    for k in range(3):
        s.append(f'<line x1="204" y1="{cy1-26+k*20}" x2="214" y2="{cy1-26+k*20}" stroke="{LINE}" stroke-width="0.4"/>')
    for part in horn(92, cy1):
        s.append(part)
    s.append(f'<path d="M216,{cy1-6} l10,-5 M216,{cy1+6} l10,5" stroke="{SEAL}" stroke-width="0.8" fill="none"/>')
    s.append(arrow(216, cy1, 256, cy1, SEAL, 1.0, head="arrS"))
    s.append(txt(260, cy1 + 2, "穿进去", 4.8, SEAL))
    s.append(txt(30, cy1 + 48, "壳越硬，越像一个可以被钉住的靶心", 4.6, "#6E6459"))

    # 二、抵空处：滑开了
    t2 = cy1 + 76
    s.append(txt(24, t2, "二、无死地：同一只角，没有地方可投", 5.4, GREEN))
    cy2 = t2 + 66
    s.append(f'<line x1="202" y1="{cy2-40}" x2="202" y2="{cy2+40}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="4 4"/>')
    for part in horn(92, cy2):
        s.append(part)
    s.append(f'<path d="M202,{cy2} q12,-6 22,-18" fill="none" stroke="{GREEN}" stroke-width="0.7" marker-end="url(#arr2)"/>')
    s.append(txt(226, cy2 - 24, "角滑开了：无处落点", 4.8, GREEN))
    s.append(txt(30, cy2 + 48, "不是练成刀枪不入——那是把土堆得更厚", 4.6, "#6E6459"))

    b = cy2 + 70
    s.append(txt(24, b, "一个全身紧绷、处处设防的人，恰恰把自己变成了一排靶子。", 5.2, INK))
    s.append(txt(24, b + 16, "无死地，不是没有一处可以被打——是没有一处「可以被定点击中」。", 5.2, INK))
    s.append(txt(24, b + 32, "所以那个「摄」字是往回收：不堆，就不成地。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "他不是没遇到兕虎，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "是兕虎找不到那个可以下角的地方。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch50c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十一章 · 四层链条 ============
def ch51a_si_ceng_lian_tiao():
    W, H = 380, 592
    body, y = head(W, H, "道生、德畜、物形、势成：四层链条，顺序不可颠倒",
                   "第 五 十 一 章 · 链", "四层链条", "道生之，德畜之，物形之，势成之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "道不占地方，它「生」的方式是给一个能容的场；德是把这份生机存住。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "物给边界，势给时候——形管你在哪儿，势管你什么时候。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "四层链条，从虚到成", 5.4, SEAL))

    rows = [(170, "道 生 之", "虚：不占地方，先有「这回事」"),
            (240, "德 畜 之", "蓄：像存粮，把生机留住"),
            (310, "物 形 之", "形：落到质料上，有了边界"),
            (380, "势 成 之", "势：顺着时令风气，才长得成")]
    for k, (yy, name, desc) in enumerate(rows):
        if k < 3:
            s.append(f'<line x1="52" y1="{yy+16}" x2="52" y2="{yy+50}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="4 4"/>')
            if k < 2:
                s.append(arrow(52, yy + 48, 52, yy + 68, GREEN, 0.7, head="arr2"))
        s.append(txt(86, yy + 1, name, 6.6, INK))
        s.append(txt(86, yy + 16, desc, 4.8, "#6E6459"))

    # 图标：四个中心都落在 yy-6
    s.append(f'<circle cx="52" cy="164" r="15" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(txt(52, 167, "道", 5.8, SEAL, "middle"))
    s.append(box(36, 222, 32, 28, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(f'<line x1="36" y1="226" x2="68" y2="226" stroke="{INK}" stroke-width="0.5"/>')
    s.append(txt(52, 243, "德", 5.8, INK, "middle"))
    s.append(box(36, 290, 32, 32, fill="none", stroke=INK, width=0.9))
    s.append(box(44, 298, 16, 16, fill="#EFE6D4", stroke=INK, width=0.6))
    s.append(f'<path d="M32,390 C44,384 60,376 72,364" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(arrow(66, 370, 74, 362, GREEN, 0.7, head="arr2"))

    b = 424
    s.append(txt(24, b, "世俗习惯反过来：只看见有形之物，看不见它后面的虚源与生机。", 5.2, INK))
    s.append(txt(24, b + 16, "所以「物形之」不是起点，是第三层；头一层，是一个不占地方的场。", 5.2, INK))
    s.append(txt(24, b + 32, "四层不能颠倒：先有虚，才有存；先有形，才谈得上顺时。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "道负责「有」，德负责「留住」；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一个不占地方，一个专门存。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch51a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十一章 · 一间屋 ============
def ch51b_yi_jian_wu():
    W, H = 380, 592
    body, y = head(W, H, "亭是有顶无壁的屋子，宰是屋下当差的人：一个给顶，一个进屋",
                   "第 五 十 一 章 · 屋", "一间屋", "亭之毒之……长而不宰。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「亭」，《说文》「民所安定也」——有顶，所以能遮；无壁，所以不拦。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "「宰」，屋下执事者——长养你，却不搬进你屋里当那个管事的。", 5.2, "#6E6459", "middle"))

    # 一、亭：有顶无壁
    t1 = y + 46
    s.append(txt(24, t1, "一、亭之：给一个能停一停的顶", 5.4, GREEN))
    gy1 = t1 + 108
    s.append(f'<line x1="24" y1="{gy1}" x2="356" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M56,{gy1-84} L156,{gy1-112} L256,{gy1-84}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="72" y1="{gy1-87}" x2="240" y2="{gy1-87}" stroke="{INK}" stroke-width="0.6"/>')
    for xv in (76, 236):
        s.append(f'<line x1="{xv}" y1="{gy1-84}" x2="{xv}" y2="{gy1}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="156" cy="{gy1-40}" r="4" fill="none" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(f'<line x1="156" y1="{gy1-36}" x2="156" y2="{gy1-14}" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(f'<line x1="156" y1="{gy1-14}" x2="148" y2="{gy1}" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(f'<line x1="156" y1="{gy1-14}" x2="164" y2="{gy1}" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(txt(292, gy1 - 74, "有顶：能遮", 4.8, GREEN))
    s.append(txt(292, gy1 - 60, "无壁：不拦", 4.8, GREEN))
    s.append(txt(292, gy1 - 48, "谁都能进", 4.6, "#6E6459"))
    s.append(txt(292, gy1 - 36, "谁也不算", 4.6, "#6E6459"))
    s.append(txt(292, gy1 - 26, "被关在里面", 4.6, "#6E6459"))
    s.append(txt(24, gy1 + 14, "毒之：不是替它长，是给它长厚的条件", 4.8, GREEN))

    # 二、宰：加了壁，又住进一个人
    t2 = gy1 + 36
    s.append(txt(24, t2, "二、宰：加了四壁，又搬进一个当差的", 5.4, SEAL))
    gy2 = t2 + 104
    s.append(f'<line x1="24" y1="{gy2}" x2="356" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M56,{gy2-84} L156,{gy2-112} L256,{gy2-84}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(box(76, gy2 - 84, 160, 84, fill="#EFE6D4", stroke=INK, width=1.2))
    s.append(f'<line x1="140" y1="{gy2-84}" x2="140" y2="{gy2-24}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<line x1="140" y1="{gy2-24}" x2="176" y2="{gy2-24}" stroke="{INK}" stroke-width="0.6"/>')
    # 屋里的当差者
    s.append(f'<circle cx="196" cy="{gy2-46}" r="3.4" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<line x1="196" y1="{gy2-42}" x2="196" y2="{gy2-22}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(196, gy2 - 8, "宰", 5.0, SEAL, "middle"))
    s.append(txt(292, gy2 - 60, "墙一立，里面就", 4.6, SEAL))
    s.append(txt(292, gy2 - 50, "有了「谁说了算」", 4.6, SEAL))
    s.append(txt(24, gy2 + 14, "「长养」最自然的下一步，就是搬进去管——这一步要按住的正是它", 4.8, SEAL))

    b = gy2 + 40
    s.append(txt(24, b, "「养大」和「让它长」的差别，不在动作，在手里有没有那一把。", 5.2, INK))
    s.append(txt(24, b + 16, "三个字，一个「不进屋」：亭给顶，毒给厚，宰不给位。", 5.2, INK))
    s.append(txt(24, b + 32, "这一章不教人怎么施恩，教人怎么施恩之后，不进那间屋。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "亭是有顶无壁的屋子，宰是屋下当差的人；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一个给顶，一个进屋。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch51b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十一章 · 一本账 ============
def ch51c_yi_ben_zhang():
    W, H = 380, 552
    body, y = head(W, H, "「不有」是总开关：一划「这是我的」，恃与宰就自己跟上来",
                   "第 五 十 一 章 · 账", "一本账", "生而不有，为而不恃，长而不宰。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「有」就是划一道界：这一块是我的。而这道界最常划在「我养的」这三个字上。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "恃与宰，是「我养了它」的利息；本金不借，利息不来。", 5.2, "#6E6459", "middle"))

    def ledger(cx, cy, filled):
        o = [box(cx - 46, cy - 32, 92, 64, fill="#FBF6EC", stroke=INK, width=1.0),
             f'<line x1="{cx-46}" y1="{cy-14}" x2="{cx+46}" y2="{cy-14}" stroke="{LINE}" stroke-width="0.45"/>',
             f'<line x1="{cx-46}" y1="{cy+4}" x2="{cx+46}" y2="{cy+4}" stroke="{LINE}" stroke-width="0.45"/>',
             f'<line x1="{cx-30}" y1="{cy-32}" x2="{cx-30}" y2="{cy+32}" stroke="{LINE2}" stroke-width="0.4"/>']
        if filled:
            o.append(txt(cx - 24, cy - 18, "我养的", 4.6, SEAL))
        return o

    # 一、不有：账上不记这一笔
    t1 = y + 46
    s.append(txt(24, t1, "一、生而不有：账上不记这一笔", 5.4, GREEN))
    cy1 = t1 + 54
    for part in ledger(94, cy1, False):
        s.append(part)
    s.append(txt(168, cy1 - 6, "没有这一笔，就没有利息", 4.8, "#6E6459"))
    s.append(txt(168, cy1 + 10, "为而不恃：做了，不靠着它站直", 4.6, GREEN))
    s.append(txt(168, cy1 + 22, "长而不宰：养大了，不进去当管事", 4.6, GREEN))

    # 二、有：记上一笔，利息自来
    t2 = cy1 + 58
    s.append(txt(24, t2, "二、一划界：记上「我养的」，两笔利息自己来", 5.4, SEAL))
    cy2 = t2 + 62
    for part in ledger(94, cy2, True):
        s.append(part)
    s.append(arrow(142, cy2 - 8, 208, cy2 - 26, SEAL, 0.9, head="arrS"))
    s.append(arrow(142, cy2 + 8, 208, cy2 + 26, SEAL, 0.9, head="arrS"))
    s.append(txt(214, cy2 - 32, "恃：靠着它站直", 4.8, SEAL))
    s.append(txt(214, cy2 - 20, "说话硬一点，眼神定一点", 4.4, "#6E6459"))
    s.append(txt(214, cy2 + 20, "宰：搬进它屋里", 4.8, SEAL))
    s.append(txt(214, cy2 + 32, "养了，就顺手管起来", 4.4, "#6E6459"))
    s.append(txt(30, cy2 + 44, "这是「好人」的病：坏事的人不恃，好事的人才恃", 4.6, "#6E6459"))

    b = cy2 + 70
    s.append(txt(24, b, "三个「不」是一条递进的线：不有不划界，不恃不靠它站直，不宰不搬进它屋里。", 5.0, INK))
    s.append(txt(24, b + 16, "玄德不是深：玄是两股丝绞在一起——一根看不出怎么绞的绳，才承得住重。", 5.0, INK))
    s.append(txt(24, b + 32, "开关一合，后面两样就关不上；这个开关，就在「这是我的」四个字上。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「不有」是总开关：一划「这是我的」，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "恃与宰就自己跟上来了。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch51c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十二章 · 一个圈 ============
def ch52a_yi_ge_quan():
    W, H = 380, 612
    body, y = head(W, H, "出去是顺水，回来是逆水：这一章的全部功夫，都在逆水那半圈上",
                   "第 五 十 二 章 · 圈", "一个圈", "既得其母，以知其子；既知其子，复守其母。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "母生子，是天道；子归母，是功夫。出去那半圈，一步不用你走，它自己会走。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "回来那半圈，每一步都要你自己迈。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "一个闭环：从母到子，是出去；从子到母，是回来", 5.4, SEAL))

    cy = t1 + 112
    # 上弧：出去（赭）
    s.append(f'<path d="M100,{cy} A110,54 0 0 1 280,{cy}" fill="none" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(f'<polygon points="186,{cy-60} 186,{cy-48} 197,{cy-54}" fill="{SEAL}"/>')
    # 下弧：回来（青）
    s.append(f'<path d="M280,{cy} A110,54 0 0 1 100,{cy}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<polygon points="194,{cy+60} 194,{cy+48} 183,{cy+54}" fill="{GREEN}"/>')

    s.append(f'<circle cx="80" cy="{cy}" r="20" fill="#FBF6EC" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(80, cy + 3, "母", 7.0, INK, "middle"))
    s.append(txt(80, cy + 30, "无·本源", 4.6, "#6E6459", "middle"))
    s.append(f'<circle cx="300" cy="{cy}" r="20" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(300, cy + 3, "子", 7.0, INK, "middle"))
    s.append(txt(300, cy + 30, "有·万象", 4.6, "#6E6459", "middle"))

    s.append(txt(190, cy - 78, "出去：顺水（天定的）", 5.0, SEAL, "middle"))
    s.append(txt(190, cy + 84, "回来：逆水（人做的）", 5.0, GREEN, "middle"))

    b = cy + 106
    s.append(txt(24, b, "两个岔口：站在这半圈上，还是站在那半圈上", 5.4, INK))
    s.append(box(20, b + 10, 164, 54, fill="#FBF6EC", stroke=GREEN))
    s.append(txt(102, b + 26, "塞其兑，闭其门", 5.2, GREEN, "middle"))
    s.append(txt(102, b + 40, "站在回来的半圈上", 4.6, "#6E6459", "middle"))
    s.append(txt(102, b + 52, "终身不勤：不用那么劳", 4.6, "#6E6459", "middle"))
    s.append(box(196, b + 10, 164, 54, fill="#FBF6EC", stroke=SEAL))
    s.append(txt(278, b + 26, "开其兑，济其事", 5.2, SEAL, "middle"))
    s.append(txt(278, b + 40, "站在出去那半圈上", 4.6, "#6E6459", "middle"))
    s.append(txt(278, b + 52, "终身不救：一辈子停不下来", 4.6, "#6E6459", "middle"))

    d = b + 82
    s.append(txt(24, d, "「复」是走回来，不是停下来；没出去过的，谈不上复。", 5.2, INK))
    s.append(txt(24, d + 16, "出去要看得见万象（知子），回来要守得住虚源（守母）；", 5.2, INK))
    s.append(txt(24, d + 32, "不是关在母里不出来——那是闭门造车，不叫守母。", 5.2, GREEN))

    c = d + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "母生子，是天道；子归母，是功夫；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "本章讲的，就是这后半圈。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch52a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十二章 · 一张脸 ============
def ch52b_yi_zhang_lian():
    W, H = 380, 664
    body, y = head(W, H, "塞其兑，闭其门；开其兑，济其事：口一张一收，人就在两个半圈上",
                   "第 五 十 二 章 · 口", "一张脸", "塞其兑，闭其门……开其兑，济其事。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「兑」在《易·说卦》里就是「口」——口、眼、耳、鼻，人身上一共就这几个口。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "塞不是缝上，是「不敞着」。", 5.2, "#6E6459", "middle"))

    # 一、塞
    t1 = y + 46
    s.append(txt(24, t1, "一、塞其兑：把口收一收", 5.4, GREEN))
    cy1 = t1 + 84
    s.append(f'<circle cx="104" cy="{cy1}" r="44" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for ex in (88, 120):
        s.append(f'<circle cx="{ex}" cy="{cy1-12}" r="6" fill="#FBF6EC" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<line x1="{ex-7}" y1="{cy1-12}" x2="{ex+7}" y2="{cy1-12}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="104" cy="{cy1+22}" rx="13" ry="7" fill="#FBF6EC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="91" y1="{cy1+22}" x2="117" y2="{cy1+22}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(104, cy1 + 56, "三孔皆塞", 4.8, SEAL, "middle"))
    s.append(arrow(30, cy1 - 12, 74, cy1 - 12, SEAL, 0.8, head="arrS"))
    s.append(txt(30, cy1 + 2, "外头的东西", 4.4, "#6E6459"))
    s.append(txt(30, cy1 + 12, "进不来", 4.4, "#6E6459"))

    # 二、开
    t2 = cy1 + 74
    s.append(txt(24, t2, "二、开其兑，济其事：口一敞，事一件件往外长", 5.4, SEAL))
    cy2 = t2 + 84
    s.append(f'<circle cx="104" cy="{cy2}" r="44" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for ex in (88, 120):
        s.append(f'<circle cx="{ex}" cy="{cy2-12}" r="6" fill="#FBF6EC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<ellipse cx="104" cy="{cy2+22}" rx="13" ry="7" fill="#FBF6EC" stroke="{INK}" stroke-width="0.7"/>')
    s.append(arrow(74, cy2 - 12, 30, cy2 - 22, SEAL, 0.8, head="arrS"))
    s.append(arrow(134, cy2 - 12, 178, cy2 - 22, SEAL, 0.8, head="arrS"))
    s.append(arrow(104, cy2 + 34, 104, cy2 + 62, SEAL, 0.8, head="arrS"))
    for k, (bx, by) in enumerate([(10, cy2 - 34), (186, cy2 - 34), (96, cy2 + 66)]):
        for m in range(2):
            s.append(box(bx + m * 10, by, 9, 9, fill="#FBF6EC", stroke=SEAL, width=0.6))
    s.append(txt(186, cy2 + 8, "事：一件未", 4.4, "#6E6459"))
    s.append(txt(186, cy2 + 18, "完又起一件", 4.4, "#6E6459"))
    s.append(txt(104, cy2 + 86, "一辈子停不下来：「救」训「止」，不救是止不住", 4.6, SEAL, "middle"))

    b = cy2 + 108
    s.append(txt(24, b, "「塞」与「闭」是两个动作：孔是一个个的，堵；门是一整扇的，合。", 5.2, INK))
    s.append(txt(24, b + 16, "「勤」训「劳」：不勤不是不干活，是不用那么劳。", 5.2, INK))
    s.append(txt(24, b + 32, "两个半圈的分界，就在这几个口上：收着，就在回来那半圈上。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「兑」是口，「袭」是袍，「救」是止；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "三个字，一个在收口，一个在穿衣，一个在刹车。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch52b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十二章 · 一盏灯 ============
def ch52c_yi_zhan_deng():
    W, H = 380, 656
    body, y = head(W, H, "用其光，复归其明：光出去照东西，明是那个照本身",
                   "第 五 十 二 章 · 灯", "一盏灯", "用其光，复归其明，无遗身殃，是为袭常。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "灯照屋子，屋子照亮了；灯一关，屋子黑，灯还在。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "光是照东西的，明是那个照本身；光一直在外面，人就一直在外面。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "一、用其光：开灯，照见屋里的东西", 5.4, SEAL))
    ry1 = t1 + 26
    s.append(box(56, ry1, 268, 118, fill="#FDFAF2", stroke=INK, width=1.0))
    s.append(f'<polygon points="86,{ry1+22} 62,{ry1+118} 318,{ry1+118} 236,{ry1+22}" fill="#F6E9B8" opacity="0.55" stroke="none"/>')
    s.append(f'<path d="M74,{ry1+22} L100,{ry1+22} L96,{ry1+8} L78,{ry1+8} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="87" cy="{ry1+31}" r="5" fill="#F2C46B" stroke="{INK}" stroke-width="0.6"/>')
    s.append(f'<line x1="87" y1="{ry1+22}" x2="87" y2="{ry1+26}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(box(150, ry1 + 92, 46, 14, fill="#EFE6D4", stroke=INK, width=0.7))
    s.append(box(206, ry1 + 86, 60, 20, fill="#F2EADA", stroke=INK, width=0.7))
    s.append(f'<line x1="228" y1="{ry1+90}" x2="244" y2="{ry1+90}" stroke="{LINE2}" stroke-width="0.5"/>')
    s.append(txt(87, ry1 - 4, "光：照出去", 4.6, SEAL, "middle"))
    s.append(txt(190, ry1 + 134, "开灯：屋里每样东西都看得见——这就是「用其光」", 4.6, "#6E6459", "middle"))

    # 二、复归其明
    t2 = ry1 + 168
    s.append(txt(24, t2, "二、复归其明：灯一关，屋子黑，灯还在", 5.4, GREEN))
    ry2 = t2 + 26
    s.append(box(56, ry2, 268, 118, fill="#EFE8D8", stroke=INK, width=1.0))
    s.append(f'<path d="M74,{ry2+22} L100,{ry2+22} L96,{ry2+8} L78,{ry2+8} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="87" cy="{ry2+31}" r="5" fill="#FBF6EC" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<line x1="87" y1="{ry2+22}" x2="87" y2="{ry2+26}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(box(150, ry2 + 92, 46, 14, fill="#E6DDC9", stroke=INK, width=0.7))
    s.append(box(206, ry2 + 86, 60, 20, fill="#E6DDC9", stroke=INK, width=0.7))
    s.append(txt(151, ry2 + 60, "东西还在这儿，只是看不清了", 4.4, "#8A7E70"))
    s.append(txt(110, ry2 - 4, "灯还在：这就是「明」", 4.6, GREEN, "middle"))

    b = ry2 + 148
    s.append(txt(24, b, "人最常见的病，是把「光」当成自己：光照到哪儿，人就以为自己在哪儿。", 5.2, INK))
    s.append(txt(24, b + 16, "照得越远，人越散；「复归其明」就是：光收回来，人还在原处。", 5.2, INK))
    s.append(txt(24, b + 32, "「袭」是左衽袍，一层层穿上：那件「常」，是要天天穿，穿到长在身上。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "光是照东西的，明是那个照本身；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "光一直在外面，人就一直在外面。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch52c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十三章 · 两条路 ============
def ch53a_liang_tiao_lu():
    W, H = 380, 606
    body, y = head(W, H, "大道甚夷，而人好径：径是步道，窄到只容一个人过",
                   "第 五 十 三 章 · 路", "两条路", "大道甚夷，而人好径。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「夷」，《说文》「平也」；「径」，《说文》「步道也」——只能步行、容不下车的小路。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "古时路分等级：容得下车马的叫「道」，只容人走的叫「径」。", 5.2, "#6E6459", "middle"))

    # 一、大道
    t1 = y + 46
    s.append(txt(24, t1, "一、大道：平、宽，谁都能走，谁也不快", 5.4, GREEN))
    gy1 = t1 + 78
    s.append(box(24, gy1 - 46, 332, 46, fill="#FBF6EC", stroke=INK, width=0.9))
    for k in range(3):
        s.append(f'<line x1="24" y1="{gy1-46+11*(k+1)}" x2="356" y2="{gy1-46+11*(k+1)}" stroke="{LINE}" stroke-width="0.45"/>')
    for xx in (70, 130, 200, 268, 320):
        s.append(f'<circle cx="{xx}" cy="{gy1-36}" r="3.4" fill="none" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<line x1="{xx}" y1="{gy1-33}" x2="{xx}" y2="{gy1-22}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(190, gy1 - 56, "夷：没有高低，没有转弯，没有一处要你显本事", 4.6, GREEN, "middle"))

    # 二、小径
    t2 = gy1 + 30
    s.append(txt(24, t2, "二、小径：放着大道不走，偏去挤那一条", 5.4, SEAL))
    gy2 = t2 + 86
    s.append(box(24, gy2 - 46, 332, 46, fill="#FBF6EC", stroke=INK, width=0.9))
    for k in range(3):
        s.append(f'<line x1="24" y1="{gy2-46+11*(k+1)}" x2="356" y2="{gy2-46+11*(k+1)}" stroke="{LINE}" stroke-width="0.45"/>')
    # 斜穿的窄径
    s.append(f'<path d="M40,{gy2-72} L336,{gy2+16}" stroke="{SEAL}" stroke-width="3.2" opacity="0.55"/>')
    s.append(f'<path d="M40,{gy2-72} L336,{gy2+16}" stroke="{SEAL}" stroke-width="0.45"/>')
    s.append(f'<circle cx="196" cy="{gy2-40}" r="3.4" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<line x1="196" y1="{gy2-37}" x2="196" y2="{gy2-28}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(242, gy2 - 80, "径：只容一人过", 4.8, SEAL, "middle"))
    s.append(f'<line x1="242" y1="{gy2-76}" x2="242" y2="{gy2-36}" stroke="{SEAL}" stroke-width="0.35" stroke-dasharray="3 3" opacity="0.7"/>')
    s.append(txt(300, gy2 + 28, "快，是因为窄", 4.6, SEAL))
    s.append(txt(300, gy2 + 38, "窄，是因为只打算", 4.4, "#6E6459"))
    s.append(txt(300, gy2 + 47, "一个人过", 4.4, "#6E6459"))

    b = gy2 + 62
    s.append(txt(24, b, "一条路宽不宽，看的不是石头，是走的人打算带几个一起走。", 5.2, INK))
    s.append(txt(24, b + 16, "大道是公共的：谁都走得，谁都不快；小路是私的：只容一人，所以快，也只利一人。", 5.0, INK))
    s.append(txt(24, b + 32, "窄的路走多了，就成了窄的人——这就是「私」的全部形状：不是坏，是窄。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「径」是步道：快，是因为窄；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "窄，是因为只打算一个人过。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch53a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十三章 · 一座台 ============
def ch53b_yi_zuo_tai():
    W, H = 380, 476
    body, y = head(W, H, "朝甚除，田甚芜，仓甚虚：三句话，一件事的三个刻度",
                   "第 五 十 三 章 · 台", "一座台", "朝甚除，田甚芜，仓甚虚。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「除」，《说文》「殿陛也」——不是朝堂很干净，是台阶修得很讲究。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "一个社会的力气是有数的：力气往台阶上使，田里就没有力气。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "同一年的两件事：台在修，田在荒", 5.4, SEAL))
    gy = t1 + 108

    # 田（荒）
    s.append(f'<line x1="24" y1="{gy}" x2="130" y2="{gy}" stroke="{INK}" stroke-width="1"/>')
    for k, xx in enumerate((34, 50, 66, 82, 98, 114)):
        hh = 14 if k % 2 == 0 else 20
        s.append(f'<line x1="{xx}" y1="{gy}" x2="{xx-3}" y2="{gy-hh}" stroke="{GREEN}" stroke-width="0.7"/>')
        s.append(f'<line x1="{xx}" y1="{gy}" x2="{xx+3}" y2="{gy-hh+4}" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(74, gy + 14, "田甚芜", 5.0, GREEN, "middle"))
    s.append(txt(74, gy + 24, "秽也：长满荒草", 4.4, "#6E6459", "middle"))

    # 台阶（三级）
    for k in range(3):
        s.append(box(146 + k * 48, gy - 24 * (k + 1), 48, 24 * (k + 1), fill="#EFE6D4" if k == 2 else "#F2EADA", stroke=INK, width=1.0))
    s.append(txt(194, gy - 78, "朝甚除", 5.0, SEAL, "middle"))
    # 台上的人：锦衣、佩剑
    s.append(f'<circle cx="248" cy="{gy-92}" r="4" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="248" y1="{gy-88}" x2="248" y2="{gy-72}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M240,{gy-76} L248,{gy-84} L256,{gy-76}" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="254" y1="{gy-86}" x2="264" y2="{gy-70}" stroke="{SEAL}" stroke-width="0.8"/>')

    # 仓（空）
    s.append(txt(326, gy - 80, "仓甚虚", 5.0, SEAL, "middle"))
    s.append(box(300, gy - 62, 52, 62, fill="#FBF6EC", stroke=INK, width=1.0))
    s.append(f'<path d="M296,{gy-62} L326,{gy-80} L356,{gy-62}" fill="none" stroke="{INK}" stroke-width="1"/>')
    for k in range(3):
        s.append(f'<line x1="306" y1="{gy-44+k*12}" x2="346" y2="{gy-44+k*12}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="3 3"/>')
    s.append(txt(326, gy - 18, "空", 5.0, "#8A7E70", "middle"))

    # 力气：往台阶使
    s.append(arrow(122, gy - 30, 168, gy - 44, SEAL, 1.0, head="arrS"))
    s.append(txt(126, gy - 46, "力气", 4.6, SEAL))
    s.append(txt(126, gy - 36, "往这儿使", 4.4, "#6E6459"))

    b = gy + 44
    s.append(txt(24, b, "三句是一个动作的三处痕迹：台阶往上修，田往下荒，仓往空走。", 5.2, INK))
    s.append(txt(24, b + 16, "这不是道德问题，是算术问题：力气往台阶上使，田里就没有力气；田里没力气，仓里就空。", 5.0, INK))
    s.append(txt(24, b + 32, "站在上面的人看不见下面；站在下面的人数得清上面有几级。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "台阶越高，田越荒，仓越虚；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "这三句不是三件事，是一件事的三个刻度。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch53b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十三章 · 一只杯 ============
def ch53c_yi_zhi_bei():
    W, H = 380, 628
    body, y = head(W, H, "盗夸：把看得见的那面堆到极处，把看不见的那面掏到极处",
                   "第 五 十 三 章 · 杯", "一只杯", "服文采，带利剑，厌饮食，财货有余；是谓盗夸。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「盗」，《说文》「私利物也」——从次从皿：羡慕人家那件器物；「夸」从大从亏：往大里说，说到亏。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "杯壁越厚，中间越空；可这个空不是有用的空，是被抽干的空。", 5.2, "#6E6459", "middle"))

    # 一、留出来的空
    t1 = y + 46
    s.append(txt(24, t1, "一、留出来的空：壁在里面，空能装", 5.4, GREEN))
    gy1 = t1 + 104
    s.append(box(96, gy1 - 88, 188, 88, fill="#EFE6D4", stroke=INK, width=1.0))
    s.append(box(110, gy1 - 74, 160, 66, fill="#FDFAF2", stroke="none", width=0))
    s.append(box(110, gy1 - 42, 160, 34, fill="#DCE6DE", stroke="none", width=0))
    s.append(f'<line x1="110" y1="{gy1-42}" x2="270" y2="{gy1-42}" stroke="{GREEN}" stroke-width="0.6"/>')
    s.append(txt(190, gy1 - 18, "水", 4.8, GREEN, "middle"))
    s.append(txt(190, gy1 - 68, "空腔", 4.6, "#8A7E70", "middle"))
    s.append(txt(190, gy1 + 16, "壁：我自己留出来的厚度", 4.6, "#6E6459", "middle"))

    # 二、抽走的空
    t2 = gy1 + 40
    s.append(txt(24, t2, "二、抽走的空：壁被掏薄（虚线是原来的腔），底穿了洞", 5.4, SEAL))
    gy2 = t2 + 100
    s.append(box(96, gy2 - 88, 188, 88, fill="#FBF6EC", stroke=INK, width=1.0))
    s.append(box(110, gy2 - 74, 160, 74, fill="none", stroke=SEAL, dash="4 3", width=0.5, ))
    s.append(f'<polygon points="110,{gy2-74} 270,{gy2-74} 200,{gy2+2} 180,{gy2+2}" fill="#EFE8D8" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<line x1="96" y1="{gy2}" x2="176" y2="{gy2}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="204" y1="{gy2}" x2="284" y2="{gy2}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="180" y1="{gy2+2}" x2="200" y2="{gy2+2}" stroke="{SEAL}" stroke-width="0.5" stroke-dasharray="3 3"/>')
    s.append(arrow(190, gy2 + 8, 190, gy2 + 34, SEAL, 0.9, head="arrS"))
    s.append(txt(190, gy2 - 22, "被抽干", 4.6, SEAL, "middle"))
    s.append(txt(190, gy2 - 36, "看不见的那面：田与仓", 4.4, "#6E6459", "middle"))
    s.append(txt(300, gy2 - 66, "看得见", 4.4, "#6E6459"))
    s.append(txt(300, gy2 - 56, "的那面：锦衣", 4.4, "#6E6459"))
    s.append(txt(300, gy2 - 46, "利剑财货", 4.4, "#6E6459"))
    s.append(txt(190, gy2 + 46, "底一穿，就只剩响了", 4.6, SEAL, "middle"))

    b = gy2 + 66
    s.append(txt(24, b, "四样全在明处，两样全在暗处；明处越亮，暗处越黑。", 5.2, INK))
    s.append(txt(24, b + 16, "同样是空，一种是留出来的，一种是被抽走的：留出来的能装，抽走的那只剩响。", 5.2, INK))
    s.append(txt(24, b + 32, "一个是杯，一个是坑。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "留出来的空能装，抽出来的空只剩响；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "两个都是空，一个是杯，一个是坑。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch53c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十四章 · 一条线 ============
def ch54a_yi_tiao_xian():
    W, H = 380, 596
    body, y = head(W, H, "善建者不拔：楼是立在地方的，律是立在人心里的",
                   "第 五 十 四 章 · 线", "一条线", "善建者不拔，善抱者不脱。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「建」，《说文》「立朝律也」——立一条律；「拔」，《说文》「擢也」——往上抽。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "不是「会盖房子的人，房子不被推倒」，是「会立律的人，那条律抽不走」。", 5.2, "#6E6459", "middle"))

    # 一、楼：有位置，所以拔得走
    t1 = y + 46
    s.append(txt(24, t1, "一、楼：立在一个地方，所以抽得走", 5.4, SEAL))
    gy1 = t1 + 126
    s.append(f'<line x1="24" y1="{gy1}" x2="180" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s.append(box(84, gy1 - 60, 48, 20, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(box(84, gy1 - 40, 48, 20, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(box(84, gy1 - 20, 48, 20, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(f'<path d="M76,{gy1-60} L108,{gy1-78} L140,{gy1-60}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(arrow(108, gy1 - 82, 108, gy1 - 112, SEAL, 1.0, head="arrS"))
    s.append(txt(116, gy1 - 96, "拔：往上抽", 4.8, SEAL))
    s.append(txt(108, gy1 + 14, "它有位置，就有个地儿可以抓", 4.6, "#6E6459", "middle"))

    # 二、律：没有端点，抓不住
    t2 = gy1 + 34
    s.append(txt(24, t2, "二、律：立在人心里，没有端点可抓", 5.4, GREEN))
    cy2 = t2 + 100
    s.append(box(96, cy2 - 84, 188, 76, fill="#FBF6EC", stroke=INK, width=0.8))
    s.append(f'<line x1="190" y1="{cy2-88}" x2="190" y2="{cy2-2}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(txt(190, cy2 - 90, "上不见头", 4.4, "#6E6459", "middle"))
    s.append(txt(190, cy2 + 10, "下不见底", 4.4, "#6E6459", "middle"))
    s.append(arrow(120, cy2 - 26, 156, cy2 - 26, SEAL, 0.9, head="arrS"))
    s.append(txt(112, cy2 - 40, "同样去抽", 4.6, SEAL, "middle"))
    s.append(txt(112, cy2 - 30, "抓了个空", 4.4, "#6E6459", "middle"))

    b = cy2 + 30
    s.append(txt(24, b, "一座楼可以拔，一堵墙可以拆，一个人可以调走；一条立对了的律，抽不走。", 5.2, INK))
    s.append(txt(24, b + 16, "因为它不在某个位置上，它在人心里。", 5.2, INK))
    s.append(txt(24, b + 32, "第五十三章的台阶，可以修得更高，也可以被推得更低；律立住了，就一直在那儿。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "楼是立在地方的，律是立在人心里的；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "地方会被换，人心不容易。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch54a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十四章 · 一副衣襟 ============
def ch54b_yi_fu_yi_jin():
    W, H = 380, 556
    body, y = head(W, H, "善抱者不脱：手会松，怀不会",
                   "第 五 十 四 章 · 怀", "一副衣襟", "善抱者不脱，子孙以祭祀不辍。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「抱」古字作「袌」，《说文》「褱也」——从衣：把东西放进衣襟里兜着。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "兜住的东西，是靠衣裳的重量压着，不是靠手臂箍着。", 5.2, "#6E6459", "middle"))

    # 一、端在手上
    t1 = y + 46
    s.append(txt(24, t1, "一、端在手上：手会累，会松", 5.4, SEAL))
    gy1 = t1 + 92
    s.append(box(36, gy1 - 62, 84, 13, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(f'<ellipse cx="126" cy="{gy1-56}" rx="10" ry="8" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M136,{gy1-62} C142,{gy1-70} 136,{gy1-72} 132,{gy1-66}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="126" cy="{gy1-74}" r="10" fill="#FBF6EC" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="140" y1="{gy1-80}" x2="176" y2="{gy1-80}" stroke="{SEAL}" stroke-width="0.5" stroke-dasharray="4 3"/>')
    s.append(arrow(150, gy1 - 92, 150, gy1 - 66, SEAL, 0.6, head="arrS"))
    s.append(txt(196, gy1 - 88, "手臂一累就松", 4.6, SEAL))
    s.append(txt(196, gy1 - 78, "端着的早晚要掉", 4.6, "#6E6459"))
    s.append(txt(78, gy1 - 40, "端：靠的是力", 4.6, "#6E6459", "middle"))

    # 二、放进怀里
    t2 = gy1 + 8
    s.append(txt(24, t2, "二、放进怀里：衣裳压着，不用手", 5.4, GREEN))
    gy2 = t2 + 112
    s.append(f'<path d="M74,{gy2-96} C64,{gy2-30} 100,{gy2-4} 160,{gy2-4} C220,{gy2-4} 256,{gy2-30} 246,{gy2-96}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M74,{gy2-96} C110,{gy2-40} 210,{gy2-40} 246,{gy2-96}" fill="none" stroke="{INK}" stroke-width="0.6" stroke-dasharray="5 4"/>')
    s.append(f'<circle cx="160" cy="{gy2-26}" r="12" fill="#FBF6EC" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(txt(160, gy2 + 18, "怀：靠的是衣裳的重量", 4.6, GREEN, "middle"))
    s.append(f'<line x1="266" y1="{gy2-60}" x2="296" y2="{gy2-60}" stroke="{GREEN}" stroke-width="0.4" stroke-dasharray="3 3"/>')
    s.append(txt(300, gy2 - 58, "不用手", 4.4, GREEN))

    b = gy2 + 30
    s.append(txt(24, b, "「脱」是从怀里滑出去——说的不是「不离」，是「放对了地方」。", 5.2, INK))
    s.append(txt(24, b + 16, "这里抱的不是外物，是那份生机、那条道脉。", 5.2, INK))
    s.append(txt(24, b + 32, "「辍」，《说文》「车小缺复合者也」——断了一段又接上；不辍，是一次也没断过。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "手会松，怀不会；所以抱得住的东西，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "都是放进怀里的，不是端在手上的。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch54b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十四章 · 一圈涟漪 ============
def ch54c_yi_quan_lian_yi():
    W, H = 380, 604
    body, y = head(W, H, "修之于身，其德乃真……其德乃普：五级不是爬上去的，是渗上去的",
                   "第 五 十 四 章 · 渗", "一圈涟漪", "修之于身……修之于天下，其德乃普。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "五个字不是四句好话，是四个刻度：余是量（多到溢出来）／长是时／丰是厚／普是匀。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "「普」，《说文》「日无色也」——太阳没有颜色的时候，才是匀的。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "一滴落下去，一圈一圈往外渗", 5.4, SEAL))

    cx, cy = 190, t1 + 152
    rings = [(120, "#D8CBB2", 0.6, "普", "天下"),
             (96, "#B9A98C", 0.7, "丰", "邦"),
             (72, GREEN, 0.85, "长", "乡"),
             (48, "#7A8C7C", 0.9, "余", "家"),
             (24, SEAL, 1.1, "真", "身")]
    for r, col, w, ch, where in rings:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}"/>')
        s.append(txt(cx, cy - r - 6, f"{ch}·{where}", 4.8, col if ch != "真" else SEAL, "middle"))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>')
    s.append(txt(cx, cy + 16, "身", 5.0, INK, "middle"))

    # 右侧用一句话压住「不是征服」
    b = cy + 136
    s.append(txt(24, b, "「修之于天下」不是「把天下修好」：不是你去修它，是它被渗到。", 5.2, INK))
    s.append(txt(24, b + 16, "你去改一个家，那个家就被你压住；你身上有余，那个家就自己松一点。", 5.2, INK))
    s.append(txt(24, b + 32, "从身上长出来的，会渗过去；从外面压过去的，会被顶回来。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "德往外走，先多，再久，再厚，最后匀；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "匀了才叫普，不是到处都有，是到处一样。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch54c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十五章 · 一张嘴 ============
def ch55a_yi_zhang_zui():
    W, H = 380, 620
    body, y = head(W, H, "含德之厚：含是衔在口里，不咽也不吐",
                   "第 五 十 五 章 · 含", "一张嘴", "含德之厚，比于赤子。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「含」，《说文》「嗛也」——嗛就是衔：东西在嘴里，不咽下去，也不吐出来。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "不是「心里藏着一份德」：藏是往里放，含是含在嘴边。", 5.2, "#6E6459", "middle"))

    # 一、含
    t1 = y + 46
    s.append(txt(24, t1, "一、含着：在嘴边上，没咽下去，也没吐掉", 5.4, GREEN))
    cy1 = t1 + 92
    s.append(f'<ellipse cx="150" cy="{cy1-16}" rx="34" ry="12" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="150" cy="{cy1+16}" rx="34" ry="12" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="150" cy="{cy1}" r="14" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(arrow(150, cy1 + 34, 150, cy1 + 60, SEAL, 0.8, head="arrS"))
    s.append(f'<line x1="138" y1="{cy1+48}" x2="162" y2="{cy1+48}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(150, cy1 + 76, "咽：咽下去就没了", 4.6, SEAL, "middle"))
    s.append(arrow(196, cy1, 246, cy1, SEAL, 0.8, head="arrS"))
    s.append(f'<line x1="236" y1="{cy1-10}" x2="236" y2="{cy1+10}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(248, cy1 - 6, "吐：吐出来", 4.6, SEAL))
    s.append(txt(248, cy1 + 6, "就散了", 4.4, "#6E6459"))
    s.append(txt(60, cy1 - 34, "含：不咽不吐", 5.0, GREEN))

    # 二、吐
    t2 = cy1 + 92
    s.append(txt(24, t2, "二、吐出来：那是第五十三章的「夸」", 5.4, SEAL))
    cy2 = t2 + 76
    s.append(f'<ellipse cx="96" cy="{cy2-30}" rx="30" ry="10" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="96" cy="{cy2+30}" rx="30" ry="10" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(arrow(130, cy2, 186, cy2, SEAL, 1.0, head="arrS"))
    s.append(f'<circle cx="204" cy="{cy2}" r="12" fill="#EFE6D4" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(236, cy2 - 6, "摆出来", 4.8, SEAL))
    s.append(txt(236, cy2 + 6, "给人看", 4.4, "#6E6459"))
    s.append(txt(96, cy2 + 52, "张口给人看：吐一次，就少一点", 4.6, "#6E6459", "middle"))

    b = cy2 + 72
    s.append(txt(24, b, "第四十四章说「多藏必厚亡」；本章说「含」——藏是往里放，含是含在嘴边。", 5.2, INK))
    s.append(txt(24, b + 16, "藏起来的东西会忘，含在嘴里的忘不掉：它离得很近，一直在。", 5.2, INK))
    s.append(txt(24, b + 32, "含着的人，安稳；一松开，就哭。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "藏是往里放，含是含在嘴边；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "藏起来的东西会忘，含在嘴里的忘不掉。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch55a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十五章 · 一只拳 ============
def ch55b_yi_zhi_quan():
    W, H = 380, 630
    body, y = head(W, H, "骨弱筋柔而握固：婴儿攥拳是为了收，成人攥拳是为了抓",
                   "第 五 十 五 章 · 拳", "一只拳", "骨弱筋柔而握固。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「握」，《说文》「搤持也」——搤，掐住；婴儿那只拳，拇指是扣在四指里面的。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "骨弱筋柔是外面软，握固是里面紧：边界柔，生机实。", 5.2, "#6E6459", "middle"))

    def fist(cx, cy):
        o = [f'<ellipse cx="{cx}" cy="{cy}" rx="42" ry="34" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>']
        for xx in (cx - 24, cx - 10, cx + 4, cx + 18):
            o.append(f'<path d="M{xx},{cy-30} C{xx-4},{cy-12} {xx-4},{cy+6} {xx+2},{cy+20}" fill="none" stroke="{INK}" stroke-width="0.6"/>')
        o.append(f'<path d="M{cx-38},{cy-4} C{cx-24},{cy+14} {cx-2},{cy+20} {cx+18},{cy+16} C{cx+28},{cy+14} {cx+30},{cy+4} {cx+24},{cy-4}" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
        return o

    # 一、婴儿的拳：往里收
    t1 = y + 46
    s.append(txt(24, t1, "一、婴儿的拳：拇指扣在里面，把自己握住", 5.4, GREEN))
    cy1 = t1 + 96
    for part in fist(126, cy1):
        s.append(part)
    s.append(arrow(214, cy1 + 6, 178, cy1 + 6, GREEN, 1.0, head="arrL"))
    s.append(txt(216, cy1 + 22, "收：往里", 4.8, GREEN))
    s.append(txt(126, cy1 + 50, "不抓外面的东西，就是收着", 4.4, "#6E6459", "middle"))
    s.append(txt(268, cy1 - 24, "外面软", 4.8, GREEN))
    s.append(txt(268, cy1 - 12, "（骨弱筋柔）", 4.4, "#6E6459"))
    s.append(txt(268, cy1 + 14, "里面紧", 4.8, GREEN))
    s.append(txt(268, cy1 + 26, "（握固）", 4.4, "#6E6459"))

    # 二、成人的手：往外抓
    t2 = cy1 + 82
    s.append(txt(24, t2, "二、成人的拳：同一只手，方向朝外", 5.4, SEAL))
    cy2 = t2 + 84
    for part in fist(126, cy2):
        s.append(part)
    s.append(arrow(172, cy2 + 6, 210, cy2 + 6, SEAL, 1.0, head="arrS"))
    s.append(box(216, cy2 - 10, 42, 34, fill="#FBF6EC", stroke=SEAL, width=0.8))
    s.append(txt(237, cy2 + 8, "物", 4.8, SEAL, "middle"))
    s.append(txt(126, cy2 + 50, "抓：往外；一放下就没了", 4.4, SEAL, "middle"))
    s.append(txt(237, cy2 + 44, "攥拳是为了抓", 4.4, "#6E6459", "middle"))

    b = cy2 + 72
    s.append(txt(24, b, "同一只手，两个方向：一只往里收，一只往外抓。", 5.2, INK))
    s.append(txt(24, b + 16, "第五十二章讲「塞其兑，闭其门」，讲的就是这个「收」；只不过一个是功夫，一个是天生。", 5.0, INK))
    s.append(txt(24, b + 32, "收的那只，不用力就一直在；抓的那只，一放下就没了。", 5.4, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "成年人攥拳是为了抓，婴儿攥拳是为了收；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "抓是往外，收是往里，一只是同一只手。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch55b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十五章 · 一根管 ============
def ch55c_yi_gen_guan():
    W, H = 380, 616
    body, y = head(W, H, "终日号而不嗄：婴儿哭一天嗓子不坏，不是嗓子好，是他从不憋气",
                   "第 五 十 五 章 · 气", "一根管", "终日号而不嗄，和之至也。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「嗄」，声败。婴儿哭是气出尽了就吸，吸满了再哭；他不存气，也不压气。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "「和」不是平和这个状态，是进出的量对得上——中点一直在被穿过。", 5.2, "#6E6459", "middle"))

    # 一、不憋
    t1 = y + 46
    s.append(txt(24, t1, "一、不憋：两头通着，出尽了就进", 5.4, GREEN))
    gy1 = t1 + 92
    s.append(box(48, gy1 - 56, 284, 40, fill="#FBF6EC", stroke=INK, width=1.0))
    s.append(f'<line x1="48" y1="{gy1-36}" x2="332" y2="{gy1-36}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="4 4"/>')
    s.append(arrow(56, gy1 - 46, 316, gy1 - 46, GREEN, 1.0, head="arr2"))
    s.append(arrow(316, gy1 - 26, 56, gy1 - 26, SEAL, 1.0, head="arrS"))
    s.append(txt(190, gy1 - 70, "进：吸到满", 4.6, GREEN, "middle"))
    s.append(txt(190, gy1 - 8, "出：哭到尽", 4.6, SEAL, "middle"))
    s.append(txt(190, gy1 + 18, "中间没有闸：两头一直在换", 4.8, GREEN, "middle"))

    # 二、憋
    t2 = gy1 + 46
    s.append(txt(24, t2, "二、憋着：中间装一道闸，管就鼓起来", 5.4, SEAL))
    gy2 = t2 + 92
    s.append(box(48, gy2 - 56, 284, 40, fill="#FBEEE8", stroke=INK, width=1.0))
    s.append(f'<path d="M48,{gy2-56} C110,{gy2-86} 270,{gy2-86} 332,{gy2-56}" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<path d="M48,{gy2-56} C110,{gy2-84} 270,{gy2-84} 332,{gy2-56}" fill="none" stroke="{SEAL}" stroke-width="0.4" opacity="0.6"/>')
    s.append(box(178, gy2 - 58, 12, 44, fill="#EFE6D4", stroke=SEAL, width=1.0))
    s.append(arrow(66, gy2 - 36, 168, gy2 - 36, SEAL, 1.0, head="arrS"))
    s.append(f'<line x1="160" y1="{gy2-46}" x2="160" y2="{gy2-26}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(74, gy2 - 46, "进不去", 4.6, SEAL))
    s.append(txt(248, gy2 - 30, "出不来", 4.6, SEAL))
    s.append(txt(190, gy2 + 18, "「存」起来了：有了存，就有了伤", 4.8, SEAL, "middle"))

    b = gy2 + 46
    s.append(txt(24, b, "婴儿哭一整天，嗓子不沙，不是嗓子好，是他从不憋气。", 5.2, INK))
    s.append(txt(24, b + 16, "成年人哭，多半是憋着的：一边哭一边忍，气出不尽，也吸不满。", 5.2, INK))
    s.append(txt(24, b + 32, "「心使气」就是往这管子里装闸，派气去做事；一装，它就不按自己的节奏走了。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "婴儿哭一天嗓子不坏，不是嗓子好，是他从不憋气；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一憋，就有了「存」，就有了「伤」。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch55c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十六章 · 一根芒 ============
def ch56a_yi_gen_mang():
    W, H = 380, 600
    body, y = head(W, H, "挫其锐：锐是芒，不是刀；芒不伤人，只扎人",
                   "第 五 十 六 章 · 芒", "一根芒", "挫其锐，解其纷。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「锐」，《说文》「芒也」——芒是禾本科植物尖端那一根细刺。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "它不伤人，它只是扎人；人身上的芒，就是那点「我比你明白」的尖。", 5.2, "#6E6459", "middle"))

    def leaf(gy):
        o = []
        o.append(f'<line x1="38" y1="{gy}" x2="130" y2="{gy}" stroke="{INK}" stroke-width="1"/>')
        o.append(f'<path d="M50,{gy} C66,{gy-26} 76,{gy-40} 84,{gy-50}" fill="none" stroke="{GREEN}" stroke-width="2.8"/>')
        return o

    # 一、没磨过
    t1 = y + 46
    s.append(txt(24, t1, "一、没磨过：尖还在，一碰就扎", 5.4, SEAL))
    gy1 = t1 + 120
    s += leaf(gy1)
    s.append(f'<line x1="84" y1="{gy1-50}" x2="112" y2="{gy1-68}" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(f'<circle cx="122" cy="{gy1-72}" r="5.5" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="126" y1="{gy1-74}" x2="162" y2="{gy1-62}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(txt(128, gy1 - 82, "一碰就扎", 4.8, SEAL))
    s.append(txt(44, gy1 + 12, "芒：草尖上那一根细刺", 4.4, "#6E6459"))

    # 二、磨过
    t2 = gy1 + 28
    s.append(txt(24, t2, "二、磨过：尖磨平了，才不扎", 5.4, GREEN))
    gy2 = t2 + 120
    s += leaf(gy2)
    s.append(f'<line x1="84" y1="{gy2-50}" x2="106" y2="{gy2-64}" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(f'<line x1="102" y1="{gy2-67}" x2="112" y2="{gy2-64}" stroke="{SEAL}" stroke-width="2.2"/>')
    s.append(f'<line x1="106" y1="{gy2-64}" x2="116" y2="{gy2-71}" stroke="{SEAL}" stroke-width="0.4" stroke-dasharray="3 3"/>')
    s.append(f'<circle cx="124" cy="{gy2-74}" r="5.5" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(130, gy2 - 80, 168, gy2 - 90, GREEN, 0.7, head="arr2"))
    s.append(txt(140, gy2 - 96, "滑过去", 4.8, GREEN))
    s.append(txt(40, gy2 + 12, "虚线：原来那根尖", 4.4, "#6E6459"))

    b = gy2 + 40
    s.append(txt(24, b, "「挫」是磨，不是砍——砍是断，磨是平；断了的还会再长，磨平了才不扎。", 5.2, INK))
    s.append(txt(24, b + 16, "而人身上那根芒，多半长在「我比你明白」这句话上。", 5.2, INK))
    s.append(txt(24, b + 32, "它不刺人，可一碰就扎；扎的不是对方，是那点不肯放的明白。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "锐是芒，不是刀；芒不伤人，只扎人；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "所以要磨，不要砍。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch56a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十六章 · 一个套 ============
def ch56b_yi_ge_tao():
    W, H = 380, 676
    body, y = head(W, H, "解其纷：纷是马尾韬，是那个套子，不是那团乱",
                   "第 五 十 六 章 · 套", "一个套", "解其纷，和其光，同其尘。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「纷」，《说文》「马尾韬也」——韬是套子，缠在马尾上，防它跑起来乱甩。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以纷的本义不是「乱」，是「用来对付乱的那个东西」。", 5.2, "#6E6459", "middle"))

    def strands(cx, cy, spread):
        o = []
        for k in range(6):
            t = (k - 2.5)
            xs = cx + t * 2.6
            xb = cx + t * spread
            o.append(f'<path d="M{xs:.1f},{cy-54} C{xs:.1f},{cy-16} {xb:.1f},{cy+16} {xb:.1f},{cy+54}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        return o

    # 一、缠着
    t1 = y + 46
    s.append(txt(24, t1, "一、缠着：为了不乱，先缠上一个套", 5.4, SEAL))
    cy1 = t1 + 84
    for part in strands(150, cy1, 3.2):
        s.append(part)
    s.append(box(120, cy1 - 9, 60, 18, fill="#EFE6D4", stroke=SEAL, width=0.8))
    s.append(f'<line x1="120" y1="{cy1-9}" x2="118" y2="{cy1-14}" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<line x1="180" y1="{cy1-9}" x2="182" y2="{cy1-14}" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(206, cy1 - 6, "套：缠住了，尾巴不敢甩", 4.8, SEAL))
    s.append(txt(206, cy1 + 6, "缠久了，它就长在尾巴上", 4.4, "#6E6459"))
    s.append(txt(150, cy1 + 70, "一套规矩、一句座右铭、一个「我一向如此」", 4.6, "#6E6459", "middle"))

    # 二、解开
    t2 = cy1 + 92
    s.append(txt(24, t2, "二、解开：放开那个缠，让它自己顺", 5.4, GREEN))
    cy2 = t2 + 84
    for part in strands(150, cy2, 24):
        s.append(part)
    s.append(f'<path d="M92,{cy2-2} C96,{cy2-12} 106,{cy2-14} 112,{cy2-6}" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<path d="M208,{cy2-2} C204,{cy2-12} 194,{cy2-14} 188,{cy2-6}" fill="none" stroke="{GREEN}" stroke-width="1"/>')
    s.append(txt(94, cy2 - 44, "套松脱了", 4.8, GREEN, "end"))
    s.append(txt(206, cy2 + 18, "尾巴会甩一阵", 4.8, GREEN))
    s.append(txt(206, cy2 + 30, "甩过之后，它自己会顺", 4.4, "#6E6459"))
    s.append(txt(150, cy2 + 70, "解：不是理顺，是松绑", 4.8, GREEN, "middle"))

    b = cy2 + 92
    s.append(txt(24, b, "「纷」是套，不是乱；乱能理，套只能解。", 5.2, INK))
    s.append(txt(24, b + 16, "人心里那些「为了不让自己乱」的规矩，缠久了，就是新的乱。", 5.2, INK))
    s.append(txt(24, b + 32, "放了，尾巴会甩一阵；甩过之后，它自己会顺。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "纷是套，不是乱；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "乱能理，套只能解。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch56b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十六章 · 六把尺 ============
def ch56c_liu_ba_chi():
    W, H = 380, 588
    body, y = head(W, H, "不可得而亲……不可得而贱：六把尺都要一个「我」在中间才量得动",
                   "第 五 十 六 章 · 尺", "六把尺", "是谓玄同……故为天下贵。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "亲疏、利害、贵贱，是世人最核心的六把尺；三组都建立在一个前提上：有一个「我」在中间。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "「不可得而」四个字，说的是：拿不到——那六把尺，在他身上找不到落脚的地方。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "六把尺朝中间伸，中间那个位置空了", 5.4, SEAL))

    cx, cy, r0, r1 = 190, t1 + 150, 30, 78
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(txt(cx, cy + 4, "空", 7.0, SEAL, "middle"))

    import math
    labels = ["亲", "利", "贵", "害", "疏", "贱"]
    for k in range(6):
        ang = -90 + k * 60
        ax, ay = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        x1, y1 = cx + ax * (r0 + 4), cy + ay * (r0 + 4)
        x2, y2 = cx + ax * r1, cy + ay * r1
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="2.6"/>')
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{LINE2}" stroke-width="0.4" stroke-dasharray="2 3"/>')
        lx, ly = cx + ax * (r1 + 16), cy + ay * (r1 + 16)
        s.append(txt(round(lx, 1), round(ly + 3, 1), labels[k], 5.4, INK, "middle"))
    s.append(txt(cx, cy + 112, "尺都悬在外面：落不下来", 4.8, GREEN, "middle"))

    b = cy + 128
    s.append(txt(24, b, "合我意则亲、则利、则贵；逆我意则疏、则害、则贱——尺一动，都要那个「我」在中间。", 5.0, INK))
    s.append(txt(24, b + 16, "不是他没有亲疏，是那六把尺在他身上找不到落脚的地方。", 5.2, INK))
    s.append(txt(24, b + 32, "「玄同」也不是大家都一样：一样是抹平，玄同是接上而看不出接头。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "六把尺都要一个「我」在中间才量得动；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "中间空了，尺就落不下来。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch56c"))
    s.append('</svg>')
    return "\n".join(s)


FIGS = {
    "ch01-wu-you": ("第一章", "无有同出", ch01_wu_you),
    "ch01-zhi-yue": ("第一章", "指月三境", ch01_zhi_yue),
    "ch01-miao-jiao": ("第一章", "观妙观徼", ch01_miao_jiao),
    "ch02-liu-zu": ("第二章", "六组对偶", ch02_liu_zu),
    "ch11-li-yong": ("第十一章", "利与用", ch11_li_yong),
    "ch24-qi-zhe-bu-li": ("第二十四章", "企者不立", ch24_qi_zhe_bu_li),
    "ch23-xi-yan-zi-ran": ("第二十三章", "希言自然", ch23_xi_yan_zi_ran),
    "ch22-qu-ze-quan": ("第二十二章", "曲则全", ch22_qu_ze_quan),
    "ch26-zhong-wei-qing-gen": ("第二十六章", "重为轻根", ch26_zhong_wei_qing_gen),
    "ch27-shan-xing-wu-zhe-ji": ("第二十七章", "善行无辙迹", ch27_shan_xing_wu_zhe_ji),
    "ch25-dao-fa": ("第二十五章", "道法自然", ch25_dao_fa),
    "ch38-wu-ji": ("第三十八章", "五级滑落", ch38_wu_ji),
    "ch40-fan-zhe": ("第四十章", "反向的机器", ch40_fan_zhe),
    "ch42-dao-sheng": ("第四十二章", "生发总图", ch42_dao_sheng),
    "ch51-sheng-bu-you": ("第五十一章", "生而不有", ch51_sheng_bu_you),
    "ch67-san-bao": ("第六十七章", "三宝", ch67_san_bao),
    "ch77-zhang-gong": ("第七十七章", "张弓", ch77_zhang_gong),
    "ch81-bu-ji": ("第八十一章", "九个不", ch81_bu_ji),
    "ch40-san-dong": ("第四十章", "一次动，三次翻", ch40_san_dong),
    "ch41b-fan-guo-lai": ("第四十一章", "翻过来，全是反面", ch41b_fan_guo_lai),
    "ch41c-san-zhong-kan-bei": ("第四十一章", "三种看杯", ch41c_san_zhong_kan_bei),
    "ch41d-da-qi-mian-cheng": ("第四十一章", "大器免成", ch41d_da_qi_mian_cheng),
    "ch42b-he-yu-ge": ("第四十二章", "和，不是合", ch42b_he_yu_ge),
    "ch42c-zheng-fan-he": ("第四十二章", "正 · 分 · 散 · 和", ch42c_zheng_fan_he),
    "ch43a-rou-bu-shi-ruan": ("第四十三章", "柔不是软", ch43a_rou_bu_shi_ruan),
    "ch43b-bu-zhuang-shi-pao": ("第四十三章", "不撞，是跑", ch43b_bu_zhuang_shi_pao),
    "ch44a-san-wen": ("第四十四章", "三问，越问越近", ch44a_san_wen),
    "ch44b-yue-gong-yu-tao": ("第四十四章", "月供与逃跑", ch44b_yue_gong_yu_tao),
    "ch44c-jiao-yu-zhi": ("第四十四章", "站住，停脚", ch44c_jiao_yu_zhi),
    "ch45a-liu-yi-dao-feng": ("第四十五章", "留一道缝", ch45a_liu_yi_dao_feng),
    "ch45b-jing-ying-chong": ("第四十五章", "井口看着是空的", ch45b_jing_ying_chong),
    "ch45c-yin-er-bu-fa": ("第四十五章", "引而不发", ch45c_yin_er_bu_fa),
    "ch46a-lu-shang-yin-zi": ("第四十六章", "路上的印子", ch46a_lu_shang_yin_zi),
    "ch46b-dao-gai-li": ("第四十六章", "刀改成犁", ch46b_dao_gai_li),
    "ch46c-san-ge-zu": ("第四十六章", "一句话里三个「足」", ch46c_san_ge_zu),
    "ch47a-you-ge-de-chuang": ("第四十七章", "一扇有格的窗", ch47a_you_ge_de_chuang),
    "ch47b-wang-yue-mi": ("第四十七章", "网越密，越看不见", ch47b_wang_yue_mi),
    "ch47c-shi-zi-lu-kou": ("第四十七章", "十字路口", ch47c_shi_zi_lu_kou),
    "ch48a-yi-yu-sun": ("第四十八章", "一只器，两只手", ch48a_yi_yu_sun),
    "ch48b-ceng-ke": ("第四十八章", "一图两观", ch48b_ceng_ke),
    "ch48c-guan-qia": ("第四十八章", "一道关，一道关", ch48c_guan_qia),
    "ch49a-yi-ba-chi": ("第四十九章", "一把尺", ch49a_yi_ba_chi),
    "ch49b-yi-xi-yi-guan": ("第四十九章", "一吸一灌", ch49b_yi_xi_yi_guan),
    "ch49c-hun-shui-sheng": ("第四十九章", "浑，是水声", ch49c_hun_shui_sheng),
    "ch50a-yi-tiao-lu": ("第五十章", "一条路的两头", ch50a_yi_tiao_lu),
    "ch50b-yi-ba-tu": ("第五十章", "一把土", ch50b_yi_ba_tu),
    "ch50c-yi-zhi-jiao": ("第五十章", "一只角", ch50c_yi_zhi_jiao),
    "ch51a-si-ceng-lian-tiao": ("第五十一章", "四层链条", ch51a_si_ceng_lian_tiao),
    "ch51b-yi-jian-wu": ("第五十一章", "一间屋", ch51b_yi_jian_wu),
    "ch51c-yi-ben-zhang": ("第五十一章", "一本账", ch51c_yi_ben_zhang),
    "ch52a-yi-ge-quan": ("第五十二章", "一个圈", ch52a_yi_ge_quan),
    "ch52b-yi-zhang-lian": ("第五十二章", "一张脸", ch52b_yi_zhang_lian),
    "ch52c-yi-zhan-deng": ("第五十二章", "一盏灯", ch52c_yi_zhan_deng),
    "ch53a-liang-tiao-lu": ("第五十三章", "两条路", ch53a_liang_tiao_lu),
    "ch53b-yi-zuo-tai": ("第五十三章", "一座台", ch53b_yi_zuo_tai),
    "ch53c-yi-zhi-bei": ("第五十三章", "一只杯", ch53c_yi_zhi_bei),
    "ch54a-yi-tiao-xian": ("第五十四章", "一条线", ch54a_yi_tiao_xian),
    "ch54b-yi-fu-yi-jin": ("第五十四章", "一副衣襟", ch54b_yi_fu_yi_jin),
    "ch54c-yi-quan-lian-yi": ("第五十四章", "一圈涟漪", ch54c_yi_quan_lian_yi),
    "ch55a-yi-zhang-zui": ("第五十五章", "一张嘴", ch55a_yi_zhang_zui),
    "ch55b-yi-zhi-quan": ("第五十五章", "一只拳", ch55b_yi_zhi_quan),
    "ch55c-yi-gen-guan": ("第五十五章", "一根管", ch55c_yi_gen_guan),
    "ch56a-yi-gen-mang": ("第五十六章", "一根芒", ch56a_yi_gen_mang),
    "ch56b-yi-ge-tao": ("第五十六章", "一个套", ch56b_yi_ge_tao),
    "ch56c-liu-ba-chi": ("第五十六章", "六把尺", ch56c_liu_ba_chi),
    "ch12-wu-se": ("第十二章", "门开五处", ch12_wu_se),
    "ch13-chong-ru": ("第十三章", "惊的是我", ch13_chong_ru),
    "ch14-yi-xi-wei": ("第十四章", "三样工具探不到", ch14_yi_xi_wei),
    "ch15-shan-wei-dao": ("第十五章", "七个比喻", ch15_shan_wei_dao),
    "ch16-zhi-xu-ji": ("第十六章", "归根", ch16_zhi_xu_ji),
    "ch17-tai-shang": ("第十七章", "四级台阶", ch17_tai_shang),
    "ch18-da-dao-fei": ("第十八章", "四对因果", ch18_da_dao_fei),
    "ch19-jue-sheng": ("第十九章", "三绝三弃", ch19_jue_sheng),
    "ch20-wei-zhi-yu-e": ("第二十章", "两把尺子", ch20_wei_zhi_yu_e),
    "ch21-kong-de": ("第二十一章", "由粗到细", ch21_kong_de),
    "ch03-shang-ji-guo-du": ("第三章", "尚即过度", ch03_shang_ji_guo_du),
    "ch04-dao-chong": ("第四章", "装不满的空", ch04_dao_chong),
    "ch05-tuo-yue": ("第五章", "中不是点，是枢", ch05_tuo_yue),
    "ch06-gu-shen": ("第六章", "谷神不死", ch06_gu_shen),
    "ch07-bu-zi-sheng": ("第七章", "不自生", ch07_bu_zi_sheng),
    "ch08-shang-shan": ("第八章", "上善若水", ch08_shang_shan),
    "ch09-ying-man": ("第九章", "持而盈之", ch09_ying_man),
    "ch10-bao-yi": ("第十章", "载营魄抱一", ch10_bao_yi),
    "ch28-zhi-xiong": ("第二十八章", "知其雄", ch28_zhi_xiong),
    "ch29-tian-xia-shen-qi": ("第二十九章", "天下神器", ch29_tian_xia_shen_qi),
    "ch30-wu-zhuang-ze-lao": ("第三十章", "物壮则老", ch30_wu_zhuang_ze_lao),
    "ch31-bing-zhe-bu-xiang": ("第三十一章", "兵者不祥之器", ch31_bing_zhe_bu_xiang),
    "ch32a-ming-zhi": ("第三十二章", "名与止", ch32a_ming_zhi),
    "ch32b-chuan-gu": ("第三十二章", "川谷与江海", ch32b_chuan_gu),
    "ch33-zi-zhi-zhe-ming": ("第三十三章", "自知者明", ch33_zi_zhi_zhe_ming),
    "ch34-bu-zhu": ("第三十四章", "不主故能成其大", ch34_bu_zhu_wei_da),
    "ch34b-yi-ju-liang-du": ("第三十四章", "一句两读：小与大", ch34b_yi_ju_liang_du),
    "ch35a-zhi-yu-chang": ("第三十五章", "执与场", ch35a_zhi_yu_chang),
    "ch35b-dan-bai-shui": ("第三十五章", "淡：一碗白水", ch35b_dan_bai_shui),
    "ch36a-si-dui-jie-lv": ("第三十六章", "四对：一张一阖", ch36a_si_dui_jie_lv),
    "ch36b-wei-ming-yuan": ("第三十六章", "微明 · 渊 · 利器", ch36b_wei_ming_yuan),
    "ch37a-wei-shou-xiang": ("第三十七章", "手牵象，与自化", ch37a_wei_shou_xiang),
    "ch37b-pu-yu-jing": ("第三十七章", "朴 · 静 · 自正", ch37b_pu_yu_jing),
    "ch38-wu-ji-tai-jie": ("第三十八章", "五级滑落", ch38_wu_ji_tai_jie),
    "ch39a-liu-de-yi": ("第三十九章", "六样东西，各自不裂", ch39a_liu_de_yi),
    "ch39b-di-xia-san-zhi-jiao": ("第三十九章", "底下那三只脚", ch39b_di_xia_san_zhi_jiao),
}


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    want = argv[1] if len(argv) > 1 else None
    made = []
    for key, (ch, name, fn) in FIGS.items():
        if want and want.lower() not in (key, ch.replace("第", "ch").replace("章", "")):
            continue
        path = os.path.join(OUT, f"{key}.svg")
        svg = fn()
        with open(path, "w") as f:
            f.write(svg)
        made.append((path, len(svg)))
    for p, n in made:
        print(f"{os.path.relpath(p, ROOT)}  {n} B")
    print(f"共 {len(made)} 张")


if __name__ == "__main__":
    main(sys.argv)
