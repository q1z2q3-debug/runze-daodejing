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
    W, H = 380, 512
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
    W, H = 380, 540
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
    W, H = 380, 512
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
    W, H = 380, 460
    body, y = head(W, H, "一级比一级低：不是台阶，是滑落", "第 三 十 八 章 · 滑 落",
                   "五级滑落", "一失再失，靠的不是走，是滑。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 16, "上德不德，是以有德；下德不失德，是以无德。", 7.2, INK, "middle"))
    s.append(txt(190, y + 30, "失道而后德，失德而后仁，失仁而后义，失义而后礼。", 7.2, INK, "middle"))

    a = y + 44
    base = a + 122
    bnd = [24, 76.3, 128.7, 181, 233.3, 285.7, 338]
    offs = [10, 28, 46, 64, 82, 96]
    d = f'M{bnd[0]},{a+offs[0]} '
    for i in range(6):
        d += f'L{bnd[i+1]},{a+offs[i]} '
        if i < 5:
            d += f'L{bnd[i+1]},{a+offs[i+1]} '
    d += f'L{bnd[6]},{base} L{bnd[0]},{base} Z'
    s.append(f'<path d="{d}" fill="#F7F1E3" stroke="{INK}" stroke-width="1"/>')

    levels = [("道", GREEN), ("上德", INK), ("下德", SEAL), ("仁", INK), ("义", SEAL), ("礼", SEAL)]
    for i, (nm, col) in enumerate(levels):
        cx = (bnd[i] + bnd[i+1]) / 2
        s.append(txt(cx, a + offs[i] + (16 if i < 5 else 13), nm, 8.4 if len(nm) == 1 else 7.8, col, "middle"))

    s.append(txt(190, base + 14, "失道而后德，失德而后仁，失仁而后义，失义而后礼", 5.9, SEAL, "middle"))

    lg = base + 20
    s.append(f'<line x1="24" y1="{lg-4}" x2="338" y2="{lg-4}" stroke="{LINE}" stroke-width="0.6"/>')
    judges = [("无", "万物自化"), ("无以为", "不自知"), ("有以为", "守着怕丢"),
              ("为之", "体恤不图报"), ("为之", "带是非立场"), ("莫之应", "强引使从")]
    for i, (j, mark) in enumerate(judges):
        cx = (bnd[i] + bnd[i+1]) / 2
        s.append(txt(cx, lg + 11, j, 6.0, INK, "middle"))
        s.append(txt(cx, lg + 23, mark, 5.4, "#6E6459", "middle"))
    s.append(f'<line x1="24" y1="{lg+32}" x2="338" y2="{lg+32}" stroke="{LINE}" stroke-width="0.6"/>')

    y3 = lg + 40
    s.append(box(20, y3, 340, 54, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y3 + 17, "大丈夫处其厚，不居其薄；处其实，不居其华。", 7.6, INK, "middle"))
    s.append(txt(190, y3 + 33, "这张表不是分出谁高谁低，是认出自己此刻站在第几级。", 7.0, "#6E6459", "middle"))
    s.append(txt(190, y3 + 47, "越往下，越靠作意撑；作意越重，越要靠强制。", 6.6, SEAL, "middle"))
    s.append(gold(y3 + 64, "ch38"))
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
    "ch38-wu-ji-tai-jie": ("第三十八章", "五级台阶", ch38_wu_ji_tai_jie),
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
