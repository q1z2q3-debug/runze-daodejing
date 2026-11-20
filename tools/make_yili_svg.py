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
import re
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
def ch11b_san_shi_fu_yi_gu():
    body, y = head(380, 999, "辐条再漂亮，毂是实心木坨，也转不起来",
                   "第 十 一 章 · 毂", "三十辐共一毂", "三十辐共一毂，当其无，有车之用。", 999)
    s = [body]
    import math

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "辐、毂，全是「有」：木料、骨架、硬边界；毂心那处虚位，才是「用」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "不是先造一个空，再堆辐条；是用一圈骨架，把一个能转的虚场放出来。", 4.9, "#6E6459", "middle"))

    def wheel(cx, cy, r, solid=False, hole=True):
        for k in range(20):
            a = math.radians(k * 18)
            s.append(f'<line x1="{cx + 9 * math.cos(a):.1f}" y1="{cy + 9 * math.sin(a):.1f}" x2="{cx + (r - 2) * math.cos(a):.1f}" y2="{cy + (r - 2) * math.sin(a):.1f}" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" fill="none" stroke="{LINE}" stroke-width="0.6"/>')
        if solid:
            s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#B9A98F" stroke="{INK}" stroke-width="1.0"/>')
            for k in range(3):
                s.append(f'<line x1="{cx - 6}" y1="{cy - 4 + k * 4}" x2="{cx + 6}" y2="{cy - 6 + k * 4}" stroke="{INK}" stroke-width="0.4"/>')
        else:
            s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
            if hole:
                s.append(f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="#F6EFE0" stroke="{INK}" stroke-width="0.8"/>')

    # 一、实心毂
    s.append(txt(24, y + 52, "一、毂是实心的：辐条再多，轴穿不进去", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy = gy + 80
    wheel(132, cy, 44, solid=True)
    s.append(f'<line x1="34" y1="{cy}" x2="116" y2="{cy}" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(arrow(116, cy, 126, cy, SEAL, 1.4, None, "arrS"))
    s.append(txt(40, cy - 7, "轴", 4.2, SEAL))
    s.append(txt(200, gy + 44, "辐：二十根都在这儿", 4.3, "#6E6459"))
    s.append(f'<line x1="196" y1="{gy + 48}" x2="176" y2="{cy - 32}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="3 2"/>')
    s.append(txt(132, cy + 56, "毂心填实：木坨一块", 4.5, SEAL, "middle"))
    s.append(txt(36, gy + 152, "辐条是「利」：给骨架、给定型、给抓手", 4.3, "#6E6459"))
    s.append(txt(36, gy + 166, "毂心是「用」：填实了，转动的可能就没了", 4.3, SEAL))

    # 二、空毂
    s.append(txt(24, gy + 196, "二、毂心留虚：轴一穿进去，轮就转了", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy2 = gy2 + 76
    wheel(132, cy2, 44, solid=False, hole=True)
    s.append(f'<line x1="40" y1="{cy2}" x2="226" y2="{cy2}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(txt(46, cy2 - 8, "轴穿过", 4.2, GREEN))
    s.append(f'<path d="M168,{cy2 + 16} A 40 40 0 0 1 144,{cy2 + 38}" fill="none" stroke="{GREEN}" stroke-width="1.1" marker-end="url(#arr2)"/>')
    s.append(txt(178, cy2 + 32, "转", 4.8, GREEN))
    s.append(txt(132, cy2 + 52, "毂心空着，轴才进得去，轮才滚得动", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 156, "同一圈骨架，只差中间那处空：有给利，无给用", 4.3, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「当其无」，不是毂里有一团空气，是毂中心留出的那个虚位——轴进得去，力传得开。", 5.2, INK))
    s.append(txt(24, a + 16, "骨架不是为了堆木头，是为了撑开一个可以流转的虚场；骨架越定，虚场越清。", 5.2, INK))
    s.append(txt(24, a + 34, "所以利不是目的，是条件：有立得住，无才用得起来。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "辐聚而成毂，毂虚而轴可穿；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "有给你抓手，无给你生机。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch11b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch11c_zao_hu_you():
    body, y = head(380, 999, "墙再厚再华丽，封死填满，就只是一座土堆",
                   "第 十 一 章 · 室", "凿户牖", "凿户牖以为室，当其无，有室之用。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "户是门，牖是窗；墙、梁、屋顶、地基，全部是「有」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "房子的目标不是墙，是墙围出来那一片能让人活在里面的空间。", 4.9, "#6E6459", "middle"))

    # 一、封死
    s.append(txt(24, y + 52, "一、封死：四面墙，一堵不漏", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px, py = 150, gy + 84
    s.append(f'<path d="M{px - 58},{py} L{px},{py - 34} L{px + 58},{py} z" fill="#E4D8BF" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="{px - 54}" y="{py}" width="108" height="46" fill="#E4D8BF" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(3):
        s.append(f'<line x1="{px - 54}" y1="{py + 12 + k * 14}" x2="{px + 54}" y2="{py + 12 + k * 14}" stroke="{INK}" stroke-width="0.4" opacity="0.5"/>')
    s.append(txt(px, py + 28, "无门无窗", 4.6, SEAL, "middle"))
    s.append(arrow(232, py + 24, 208, py + 24, SEAL, 0.9, None, "arrS"))
    s.append(txt(236, py + 28, "进不去", 4.3, SEAL))
    s.append(txt(px, gy + 160, "墙立着，屋子却没生出来：只剩一座土堆", 4.3, SEAL, "middle"))

    # 二、开
    s.append(txt(24, gy + 196, "二、开户牖：门窗是那两处「无」", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px2, py2 = 150, gy2 + 62
    s.append(f'<path d="M{px2 - 58},{py2} L{px2},{py2 - 34} L{px2 + 58},{py2} z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="{px2 - 54}" y="{py2}" width="108" height="52" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    # 户（门，开着的口）与牖（窗）
    s.append(f'<rect x="{px2 - 26}" y="{py2 + 20}" width="30" height="32" fill="#E4EAE0" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px2 - 11}" y1="{py2 + 20}" x2="{px2 - 11}" y2="{py2 + 52}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(f'<rect x="{px2 + 18}" y="{py2 + 14}" width="28" height="20" fill="#E4EAE0" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px2 + 32}" y1="{py2 + 14}" x2="{px2 + 32}" y2="{py2 + 34}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(txt(px2 - 30, py2 + 26, "户", 3.9, GREEN, "end"))
    s.append(txt(px2 + 32, py2 + 8, "牖", 3.9, GREEN, "middle"))
    # 人立在堂中
    hx, hy = px2 - 4, py2 + 30
    s.append(f'<circle cx="{hx}" cy="{hy - 12}" r="2.8" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{hx}" y1="{hy - 9}" x2="{hx}" y2="{hy + 2}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{hx}" y1="{hy + 2}" x2="{hx - 3}" y2="{hy + 10}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{hx}" y1="{hy + 2}" x2="{hx + 3}" y2="{hy + 10}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(px2 - 68, py2 + 40, px2 - 28, py2 + 40, GREEN, 0.9, None, "arr2"))
    s.append(txt(px2 - 70, py2 + 33, "人", 4.2, GREEN, "end"))
    s.append(txt(px2, gy2 + 152, "门窗不是墙的缺口，是「无」被开出来的地方", 4.3, GREEN, "middle"))
    s.append(txt(px2, gy2 + 166, "人在里面住、呼吸、往来——用，就发生在这片空里", 4.3, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "墙、梁、门窗框是「有」：划出领地、遮风挡雨、给一个稳定框架——这是「利」。", 5.2, INK))
    s.append(txt(24, a + 16, "室内那片虚空是「无」：居住、停留、往来、生活发生的地方——这才是「用」。", 5.2, INK))
    s.append(txt(24, a + 34, "所以先立界，再开门；介不是墙，是墙围出来的那口空。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "墙立而成室，室空而人可居；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "封死填满，就只是一座土堆。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch11c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch22b_qu_mu_cao():
    body, y = head(380, 999, "曲不是委屈迎合，是弯出一个能受的弧度",
                   "第 二 十 二 章 · 一 只 曲 木 槽", "一只曲木槽", "曲，象器曲受物之形。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「曲」的本义是器物弯而能受：不是委屈自己去迎合别人。", 4.8, INK, "middle"))
    s.append(txt(190, y + 27, "直木板接不住东西，曲木槽才盛得住水。", 4.8, "#6E6459"))

    # 一、直板
    s.append(txt(24, y + 52, "一、直板：水落上去，从两头走光", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<rect x="72" y="{gy + 62}" width="180" height="12" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="72" y1="{gy + 62}" x2="72" y2="{gy + 74}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="252" y1="{gy + 62}" x2="252" y2="{gy + 74}" stroke="{INK}" stroke-width="1.1"/>')
    for xx in [126, 152, 178]:
        s.append(f'<line x1="{xx}" y1="{gy + 14}" x2="{xx}" y2="{gy + 48}" stroke="#8A7C69" stroke-width="0.7"/>')
        s.append(f'<path d="M{xx - 3},{gy + 52} q3,4 6,0" fill="none" stroke="#8A7C69" stroke-width="0.7"/>')
    s.append(f'<path d="M74,{gy + 60} q-14,4 -24,16 M250,{gy + 60} q14,4 24,16" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 2"/>')
    s.append(txt(190, gy + 106, "两头走光：受不住", 4.2, SEAL, "middle"))

    # 二、曲槽
    s.append(txt(24, gy + 158, "二、曲槽：中间凹下去，水留得住", 5.2, GREEN))
    gy2 = gy + 170
    s.append(f'<rect x="26" y="{gy2}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M64,{gy2 + 50} L110,{gy2 + 92} L230,{gy2 + 92} L276,{gy2 + 50} L278,{gy2 + 60} L232,{gy2 + 102} L108,{gy2 + 102} L62,{gy2 + 60} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M74,{gy2 + 62} L112,{gy2 + 88} L228,{gy2 + 88} L266,{gy2 + 62} Z" fill="#E9F0E6" stroke="none"/>')
    for xx in [128, 152, 176]:
        s.append(f'<line x1="{xx}" y1="{gy2 + 2}" x2="{xx}" y2="{gy2 + 46}" stroke="#8A7C69" stroke-width="0.7"/>')
        s.append(f'<path d="M{xx - 3},{gy2 + 50} q3,4 6,0" fill="none" stroke="#8A7C69" stroke-width="0.7"/>')
    s.append(f'<line x1="92" y1="{gy2 + 62}" x2="248" y2="{gy2 + 62}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    s.append(txt(190, gy2 + 30, "水位停在槽口，不再往下", 3.9, GREEN, "middle"))
    s.append(txt(190, gy2 + 112, "弯出来的那道槽，就是它「能受」的地方", 4.2, GREEN, "middle"))

    # 三、洼
    s.append(txt(24, gy2 + 158, "三、洼：水不往高处流，这是物理，不是道德", 5.2, SEAL))
    gy3 = gy2 + 170
    s.append(f'<rect x="26" y="{gy3}" width="328" height="116" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M40,{gy3 + 34} L112,{gy3 + 34} Q170,{gy3 + 96} 228,{gy3 + 34} L340,{gy3 + 34}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M116,{gy3 + 50} L112,{gy3 + 34} Q170,{gy3 + 96} 228,{gy3 + 34} L224,{gy3 + 50} Q170,{gy3 + 84} 116,{gy3 + 50} Z" fill="#E9F0E6" stroke="none"/>')
    s.append(f'<line x1="116" y1="{gy3 + 50}" x2="224" y2="{gy3 + 50}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M170,{gy3 + 30} L170,{gy3 + 62}" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(f'<path d="M164,{gy3 + 54} L170,{gy3 + 62} L176,{gy3 + 54}" fill="none" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(txt(176, gy3 + 100, "低处聚水：洼则盈", 4.2, GREEN, "middle"))

    a = gy3 + 138
    s.append(txt(24, a, "六句是规律，不是策略：一个拿「曲」换「全」，一个在「曲」里，「全」自己到了。", 4.8, INK))
    s.append(txt(24, a + 16, "「枉」是就木说，木不直，不直才有伸直的可能——屈而后伸。", 4.8, INK))
    s.append(txt(24, a + 34, "老子把「曲」从姿态的词，改成了容器的词。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "曲则全，枉则直，洼则盈，敝则新。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "弯的能受，所以能全；低的能聚，所以能盈。", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch22b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch22c_bao_yi():
    body, y = head(380, 999, "抱一：不是统一别人，是不让自己裂开",
                   "第 二 十 二 章 · 抱 一 与 五 牌", "抱一与五牌", "圣人抱一，为天下式。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「抱」不是「守」：守是防它跑掉，抱是它就贴在你身上。", 4.8, INK, "middle"))
    s.append(txt(190, y + 27, "儒者以仁义礼乐为天下式，圣人以抱一为天下式。", 4.8, "#6E6459"))

    # 一、抱一
    s.append(txt(24, y + 52, "一、抱一：一根木简揣在怀里，身上不再挂别的", 5.2, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="156" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px, py = 150, gy + 40
    s.append(f'<circle cx="{px}" cy="{py}" r="7" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="{px}" y1="{py + 7}" x2="{px}" y2="{py + 56}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{px}" y1="{py + 56}" x2="{px - 11}" y2="{py + 78}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 56}" x2="{px + 11}" y2="{py + 78}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<rect x="{px - 6}" y="{py + 15}" width="12" height="26" fill="#F2EADA" stroke="{INK}" stroke-width="1.0"/>')
    s.append(txt(px, py + 33, "一", 5.2, SEAL, "middle"))
    s.append(f'<path d="M{px - 14},{py + 14} Q{px - 12},{py + 28} {px + 4},{py + 30}" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M{px + 14},{py + 14} Q{px + 12},{py + 28} {px - 4},{py + 30}" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<circle cx="{px + 4}" cy="{py + 30}" r="1.6" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<circle cx="{px - 4}" cy="{py + 30}" r="1.6" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(px, gy + 120, "揣着的东西，本来就贴着，不必看住", 4.2, GREEN, "middle"))
    s.append(f'<line x1="120" y1="{gy + 140}" x2="180" y2="{gy + 140}" stroke="{LINE}" stroke-width="0.7"/>')

    # 二、五牌
    s.append(txt(24, gy + 182, "二、五牌：五套标准各拽一边，人就裂成几截", 5.2, SEAL))
    gy2 = gy + 194
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    qx, qy = 190, gy2 + 52
    s.append(f'<circle cx="{qx}" cy="{qy}" r="7" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M{qx},{qy + 7} L{qx - 4},{qy + 30} L{qx + 5},{qy + 46} L{qx - 3},{qy + 62} L{qx + 4},{qy + 76}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="{qx - 2}" y1="{qy + 22}" x2="{qx - 16}" y2="{qy + 40}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{qx + 2}" y1="{qy + 24}" x2="{qx + 18}" y2="{qy + 38}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{qx}" y1="{qy + 76}" x2="{qx - 10}" y2="{qy + 92}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{qx}" y1="{qy + 76}" x2="{qx + 10}" y2="{qy + 92}" stroke="{INK}" stroke-width="0.9"/>')
    plates = [("仁", 52, gy2 + 34), ("义", 52, gy2 + 96), ("礼", 300, gy2 + 34), ("智", 300, gy2 + 96), ("信", 236, gy2 + 6)]
    for name, bx, by in plates:
        s.append(f'<rect x="{bx}" y="{by}" width="34" height="22" fill="#F2EADA" stroke="{SEAL}" stroke-width="0.9"/>')
        s.append(txt(bx + 17, by + 16, name, 4.6, SEAL, "middle"))
        tx = qx - 16 if bx < qx else (qx + 18 if bx > qx else qx)
        ty = qy + (22 if bx < qx else (24 if bx > qx else 0))
        s.append(f'<line x1="{bx + (34 if bx < qx else 0)}" y1="{by + 11}" x2="{tx}" y2="{ty}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="4 2"/>')
    s.append(txt(190, gy2 + 132, "五套标准一齐拽：不是我不够好，是我把自己分成了几套", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 152, "「自见、自是、自伐、自矜」，每一个都是把「我」举起来", 4.2, "#6E6459", "middle"))

    a = gy2 + 200
    s.append(txt(24, a, "第十章「载营魄抱一」讲身：魂与魄不分成两截；此处讲法：不把自己分成好几套标准。", 4.8, INK))
    s.append(txt(24, a + 16, "一在内，一在外，说的是同一件事：不裂。身不裂，则神全；法不裂，则不摇摆。", 4.8, INK))
    s.append(txt(24, a + 34, "儒者教你把举起来的手放低，老子问你为什么非要举。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "圣人抱一，为天下式。", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "夫唯不争，故天下莫能与之争。", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch22c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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


# ============ 第五章 · 一只刍狗 ============
def ch05b_yi_zhi_chu_gou():
    body, y = head(380, 999, "刍狗祭时陈设、祭毕回草堆：天地没有那本账，用完就归位",
                   "第 五 章 · 刍 狗", "一只刍狗", "天地不仁，以万物为刍狗。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "刍狗是束草扎成的狗：祭时郑重陈设，事毕回草堆，任人践踏或当柴烧。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "天地不记账：不因你敬它而应，也不因你不敬而罚——它只是让万物各复其位。", 5.0, "#6E6459", "middle"))

    def dog(cx, cy, rot=0, w=54):
        out = [f'<g transform="translate({cx},{cy}) rotate({rot})">']
        out.append(f'<rect x="{-w / 2}" y="-13" width="{w}" height="15" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        out.append(f'<rect x="{w / 2 - 2}" y="-20" width="9" height="13" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
        out.append(f'<rect x="{w / 2 + 6}" y="-25" width="15" height="10" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        out.append(f'<path d="M{w / 2 + 8},-25 l-2,-6 l6,3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
        out.append(f'<line x1="{w / 2 + 21}" y1="-21" x2="{w / 2 + 26}" y2="-21" stroke="{INK}" stroke-width="0.7"/>')
        out.append(f'<circle cx="{w / 2 + 15}" cy="-22" r="1.1" fill="{INK}"/>')
        for k in range(4):
            xk = -w / 2 + 9 + k * 12
            out.append(f'<line x1="{xk}" y1="2" x2="{xk}" y2="10" stroke="{INK}" stroke-width="0.9"/>')
        out.append(f'<path d="M{-w / 2},-10 q-8,-3 -10,-9" fill="none" stroke="{INK}" stroke-width="0.8"/>')
        for k in range(8):
            xk = -w / 2 + 4 + k * 6.2
            out.append(f'<line x1="{xk}" y1="-11" x2="{xk + 1.6}" y2="-2" stroke="#B9A98F" stroke-width="0.5"/>')
        out.append('</g>')
        return "".join(out)

    # 一、陈：有位次
    s.append(txt(24, y + 52, "一、陈：祭时它有位次，被郑重摆着", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    table = gy + 104
    s.append(f'<line x1="76" y1="{table}" x2="304" y2="{table}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="100" y1="{table}" x2="94" y2="{gy + 142}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="280" y1="{table}" x2="286" y2="{gy + 142}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M160,{table} L164,{table - 12} L216,{table - 12} L220,{table} z" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M156,{table - 12} L224,{table - 12} L230,{table - 7} L150,{table - 7} z" fill="#EFE6D4" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(dog(190, table - 20, rot=0))
    for hx in (106, 274):
        s.append(f'<line x1="{hx}" y1="{table}" x2="{hx}" y2="{table - 26}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<circle cx="{hx}" cy="{table - 26}" r="1.6" fill="{SEAL}"/>')
        s.append(f'<path d="M{hx},{table - 30} q6,-9 0,-17" fill="none" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(190, gy + 26, "陈：有位次", 4.6, GREEN, "middle"))
    s.append(f'<line x1="190" y1="{gy + 30}" x2="190" y2="{table - 34}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(250, table - 40, "被恭敬摆着的还是那把草", 4.4, "#6E6459"))
    s.append(txt(190, gy + 142, "天地给的只是位次，没给主人", 4.5, GREEN, "middle"))

    # 二、复归
    s.append(txt(24, gy + 172, "二、复归：祭毕回草堆，还是那把草", 5.2, SEAL))
    gy2 = gy + 184
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy2 + 116
    s.append(f'<line x1="40" y1="{base}" x2="330" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M98,{base} q24,-26 54,-24 q30,4 44,24 z" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
    for k in range(8):
        s.append(f'<line x1="{104 + k * 11}" y1="{base - 3}" x2="{100 + k * 12}" y2="{base - 16 + (k % 3) * 5}" stroke="#B9A98F" stroke-width="0.5"/>')
    s.append(dog(154, base - 28, rot=-16, w=48))
    s.append(f'<ellipse cx="168" cy="{base - 22}" rx="4.2" ry="2.4" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<ellipse cx="180" cy="{base - 20}" rx="4.2" ry="2.4" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(208, base - 40, "践其首脊", 4.4, SEAL))
    # 柴捆：一束草，中间一道红绳
    for k in range(5):
        s.append(f'<line x1="{262 + k * 5}" y1="{base - 26 + k}" x2="{282 + k * 5}" y2="{base - 6 + k}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="{270}" y1="{base - 22}" x2="{290}" y2="{base - 8}" stroke="{SEAL}" stroke-width="1.0"/>')
    s.append(f'<line x1="{268}" y1="{base - 20}" x2="{276}" y2="{base - 26}" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(300, base - 38, "取而爨之", 4.4, SEAL, "end"))
    s.append(txt(190, gy2 + 140, "位次用完了，它就回草堆——不是被弃，是用完了", 4.5, GREEN, "middle"))

    a = gy2 + 168
    s.append(txt(24, a, "「不仁」不是狠心，是天地根本没有「我敬了你，你就该应我」那一本账。", 5.4, INK))
    s.append(txt(24, a + 16, "祭祀有定时，祷无定时；人一祷就记账，天地却只按自己的节律转。", 5.4, INK))
    s.append(txt(24, a + 34, "刍狗在祭时被敬、祭毕被践，不是天在赏罚它，是它该回草堆了。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "天地不仁，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "不是不慈，是不替你作主。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch05b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第五章 · 一把锁（旧稿 ch05c-yi-jia-tian-ping 已撤，存 old/） ============
def ch05c_yi_ba_suo():
    body, y = head(380, 999, "多言就是锁支点：锁在 0、锁在 1、锁在自己以为稳的中间，锁住即穷",
                   "第 五 章 · 锁", "一把锁", "多言数穷，不如守中。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "多言不只是话多：一切定义、评判、谋划、控制，都是把支点钉死。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "钉在 0 的空寂、钉在 1 的驰求、或钉在自以为稳妥的中间——三种钉法，一个结果。", 5.0, "#6E6459", "middle"))

    def box5(gy, locked):
        out = []
        bx1, bx2, ty, by = 112, 260, gy + 34, gy + 130
        out.append(f'<rect x="{bx1}" y="{ty}" width="{bx2 - bx1}" height="{by - ty}" fill="#FBF6EC" stroke="{INK}" stroke-width="1.2"/>')
        # 活塞杆
        out.append(f'<rect x="{bx1 + 18}" y="{ty + 10}" width="11" height="{by - ty - 20}" fill="{INK}" opacity="0.45"/>')
        out.append(f'<line x1="{bx1 + 23}" y1="{ty + 6}" x2="{bx1 + 23}" y2="{ty - 16}" stroke="{INK}" stroke-width="1.3"/>')
        out.append(f'<line x1="{bx1 + 10}" y1="{ty - 16}" x2="{bx1 + 36}" y2="{ty - 16}" stroke="{INK}" stroke-width="1.3"/>')
        # 枢：腔心那一点
        out.append(f'<circle cx="{bx1 + 78}" cy="{gy + 82}" r="3.2" fill="none" stroke="{GREEN}" stroke-width="1.0"/>')
        out.append(txt(bx1 + 78, gy + 72, "枢", 4.6, GREEN, "middle"))
        if locked:
            out.append(f'<rect x="{bx1 + 70}" y="{gy + 88}" width="16" height="12" fill="{SEAL}" stroke="{SEAL}" stroke-width="0.8"/>')
            out.append(f'<path d="M{bx1 + 74},{gy + 88} q4,-9 8,0" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
            out.append(f'<line x1="{bx1 + 23}" y1="{gy + 94}" x2="{bx1 + 68}" y2="{gy + 94}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 2"/>')
        else:
            out.append(f'<line x1="{bx1 + 62}" y1="{gy + 96}" x2="{bx1 + 112}" y2="{gy + 96}" stroke="{GREEN}" stroke-width="1.1" marker-end="url(#arr2)"/>')
            out.append(f'<line x1="{bx1 + 112}" y1="{gy + 114}" x2="{bx1 + 62}" y2="{gy + 114}" stroke="{GREEN}" stroke-width="1.1" marker-end="url(#arrL)"/>')
            out.append(txt(bx1 + 87, gy + 124, "往复", 4.4, GREEN, "middle"))
            for k in range(3):
                out.append(f'<line x1="{bx2}" y1="{gy + 62 + k * 12}" x2="{bx2 + 22}" y2="{gy + 62 + k * 12}" stroke="{GREEN}" stroke-width="0.9"/>')
                out.append(f'<path d="M{bx2 + 22},{gy + 62 + k * 12} l-4,-2.4 M{bx2 + 22},{gy + 62 + k * 12} l-4,2.4" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
            out.append(txt(bx2 + 6, gy + 52, "出风", 4.4, GREEN))
        return "".join(out)

    # 一、锁住
    s.append(txt(24, y + 52, "一、锁住：器还在，机死了", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="162" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(box5(gy, True))
    s.append(txt(190, gy + 152, "枢一锁，开合即停：出风断在这里，一停就竭", 4.5, SEAL, "middle"))

    # 二、松开
    s.append(txt(24, gy + 182, "二、松开：枢自己走，越动愈出", 5.2, GREEN))
    gy2 = gy + 194
    s.append(f'<rect x="26" y="{gy2}" width="328" height="162" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(box5(gy2, False))
    s.append(txt(190, gy2 + 152, "虚而不屈，动而愈出：不是越拉越满，是一直能开合", 4.5, GREEN, "middle"))

    a = gy2 + 190
    s.append(txt(24, a, "锁不是外物，是人自己那本账：要他一定这样、一定那样，把活的支点浇成死的刻度。", 5.4, INK))
    s.append(txt(24, a + 16, "「数穷」不是没钱，是路走到头——支点不动，器再贵也只是个壳。", 5.4, INK))
    s.append(txt(24, a + 34, "守中不是找一个好位置站住，是随时肯挪；能挪的，才叫中。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "执一则穷，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "守中则通——枢不死，机才活。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch05c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))



# ============ 第六章 · 一口谷 ============
def ch06b_yi_kou_gu():
    body, y = head(380, 999, "生机不在满处，在空处：满缸不受，空谷能受",
                   "第 六 章 · 谷", "一口谷", "谷神不死，是谓玄牝。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「谷」不是稻谷，是山谷：两山之间的空处，水深所归，风所过，草木所生。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "谷不生产什么，它只是深、只是空；正因为空，水才往那里走。", 5.0, "#6E6459", "middle"))

    # 一、满缸：不受
    s.append(txt(24, y + 52, "一、满缸：装满了，再倒就往外淌", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy + 148
    s.append(f'<line x1="60" y1="{base}" x2="320" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    cx = 190
    ym = base - 92
    s.append(f'<path d="M{cx - 58},{ym} q6,58 14,74 q30,16 74,0 q8,-16 14,-74 z" fill="#D8CBAC" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<ellipse cx="{cx}" cy="{ym}" rx="58" ry="9" fill="#D8CBAC" stroke="{INK}" stroke-width="1"/>')
    for k in range(3):
        s.append(f'<path d="M{cx - 44 + k * 10},{ym + 4} q14,-6 28,0" fill="none" stroke="#B39A72" stroke-width="0.6"/>')
    # 溢
    s.append(f'<path d="M{cx + 58},{ym + 3} q13,20 6,38" fill="none" stroke="{SEAL}" stroke-width="1.0"/>')
    s.append(f'<path d="M{cx - 58},{ym + 3} q-13,18 -6,34" fill="none" stroke="{SEAL}" stroke-width="1.0"/>')
    s.append(txt(cx + 80, ym + 26, "倒不进", 4.4, SEAL))
    s.append(txt(cx - 80, ym + 26, "往下淌", 4.4, SEAL, "end"))
    # 勺与注水
    s.append(f'<path d="M{cx - 6},{ym - 52} q-14,10 0,14 q14,-4 0,-14 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx - 6}" y1="{ym - 52}" x2="{cx + 12}" y2="{ym - 68}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M{cx - 2},{ym - 40} q3,10 2,16" fill="none" stroke="{LINE2}" stroke-width="0.8"/>')
    s.append(txt(190, gy + 168, "满了就是满了：再多一勺，也只是从口沿淌下去", 4.5, GREEN, "middle"))

    # 二、空谷：能受
    s.append(txt(24, gy + 196, "二、空谷：它什么都不装，水自来聚", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    gb = gy2 + 150
    s.append(f'<path d="M26,{gb} q56,-96 118,-30 q18,12 32,30 z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M354,{gb} q-56,-96 -118,-30 q-18,12 -32,30 z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="26" y1="{gb}" x2="354" y2="{gb}" stroke="{INK}" stroke-width="1"/>')
    # 谷底水与草
    s.append(f'<path d="M150,{gb} q40,-8 80,0" fill="none" stroke="#8FA6A0" stroke-width="2.0" opacity="0.5"/>')
    for k in range(4):
        xk = 166 + k * 14
        s.append(f'<path d="M{xk},{gb - 2} q3,-10 7,-14" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    # 水自上入谷
    for k in range(3):
        s.append(f'<line x1="{176 + k * 12}" y1="{gy2 + 4}" x2="{176 + k * 12 + 2}" y2="{gy2 + 78 + k * 8}" stroke="#8FA6A0" stroke-width="0.9" opacity="0.8"/>')
    s.append(arrow(190, gy2 + 96, 190, gb - 8, "#8FA6A0", 1.0, None, "arr2"))
    s.append(txt(254, gy2 + 34, "水往低处走", 4.4, "#6E6459"))
    # 风在谷里回
    for k in range(2):
        s.append(f'<path d="M96,{gy2 + 70 + k * 10} q40,-8 78,-2" fill="none" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(96, gy2 + 58, "风在谷里回", 4.4, "#8A7C69"))
    s.append(txt(190, gy2 + 168, "谷不去装，也不去留：能受，所以能生", 4.5, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "生机不在满处，在空处；不在取处，在受处——这是全章第一句的落点。", 5.4, INK))
    s.append(txt(24, a + 16, "谷填平了就没有谷；能让它一直生的，不是哪一汪水，是那处空一直在。", 5.4, INK))
    s.append(txt(24, a + 34, "「不死」不是哪一样东西活得久，是「空而能受」这个结构从来不断。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "满的，倒不进；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "空的，水自来。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch06b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第六章 · 一扇门轴 ============
def ch06c_yi_shan_men_zhou():
    body, y = head(380, 999, "门在开合处，不在门板上；一着手去推，它就成了一堵墙",
                   "第 六 章 · 门", "一扇门轴", "玄牝之门，是谓天地根。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「门」不是门框门扇：门是出入处，在开合之间。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "玄牝之门不是某个固定点位，是牡牝两端交互出入的那处枢机。", 5.0, "#6E6459", "middle"))

    # 一、门在开合处
    s.append(txt(24, y + 52, "一、开：门缝里出得来东西", 5.2, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ft, fb = gy + 30, gy + 150
    s.append(f'<rect x="126" y="{ft}" width="128" height="{fb - ft}" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>')
    # 左扇稍开，右扇合着；缝中是光
    s.append(f'<path d="M126,{ft} L186,{ft + 6} L186,{fb - 6} L126,{fb} z" fill="#EBD9CE" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M254,{ft} L200,{ft + 6} L200,{fb - 6} L254,{fb} z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    for k in range(3):
        s.append(f'<line x1="{384 + 0}" y1="0" x2="0" y2="0" stroke="none"/>')
    s.append(f'<path d="M193,{ft + 8} L193,{fb - 8} L200,{fb - 6} L200,{ft + 6} z" fill="#F6E9BF" stroke="none"/>')
    # 光与出物
    for k in range(3):
        s.append(f'<line x1="202" y1="{ft + 44 + k * 30}" x2="222" y2="{ft + 40 + k * 30}" stroke="#D9C07A" stroke-width="0.8" opacity="0.85"/>')
    s.append(f'<circle cx="232" cy="{ft + 58}" r="2.6" fill="none" stroke="{GREEN}" stroke-width="0.6"/>')
    s.append(f'<circle cx="240" cy="{ft + 92}" r="2.0" fill="none" stroke="{GREEN}" stroke-width="0.6"/>')
    s.append(txt(300, ft + 16, "门缝：显化从这里出去", 4.3, GREEN, "end"))
    s.append(txt(190, gy + 168, "门不在门板上，在两扇之间那道还没合死的缝", 4.5, GREEN, "middle"))

    # 二、推它，就成了墙
    s.append(txt(24, gy + 200, "二、推：一着手去定位，缝就没了", 5.2, SEAL))
    gy2 = gy + 212
    s.append(f'<rect x="26" y="{gy2}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ft2, fb2 = gy2 + 30, gy2 + 150
    s.append(f'<rect x="126" y="{ft2}" width="128" height="{fb2 - ft2}" fill="#E4D8BF" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="190" y1="{ft2}" x2="190" y2="{fb2}" stroke="{INK}" stroke-width="0.6" stroke-dasharray="2 3"/>')
    for k in range(5):
        s.append(f'<line x1="{132 + k * 24}" y1="{ft2}" x2="{132 + k * 24}" y2="{fb2}" stroke="#B9A98F" stroke-width="0.4"/>')
    # 手：掌＋四指＋拇指
    hx, hy = 216, gy2 + 100
    s.append(f'<rect x="{hx - 12}" y="{hy - 9}" width="24" height="18" rx="5" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    for k in range(4):
        s.append(f'<rect x="{hx - 10 + k * 5.6}" y="{hy - 20 - (1 - abs(1.5 - k)) * 2}" width="4" height="12" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{hx - 18}" y="{hy - 6}" width="9" height="4.4" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="{hx + 12}" y1="{hy + 2}" x2="{hx + 24}" y2="{hy + 10}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(258, hy - 26, "推住了", 4.4, SEAL))
    s.append(f'<line x1="254" y1="{hy - 24}" x2="236" y2="{hy - 16}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(190, gy2 + 168, "一遇定位、占有，门当场变成了墙：通道闭塞", 4.5, SEAL, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "门是出入处：不在门板，在开合。所以「玄牝之门」不是可找到、可占住的地方。", 5.4, INK))
    s.append(txt(24, a + 16, "凡从隐到显、从无到有，都经由这道门流出；可它不在天地之外，就在冲虚本身。", 5.4, INK))
    s.append(txt(24, a + 34, "「绵绵若存」的「若」，正是不许你把「存」把持成一个可守的东西——一守，就没了。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "门在开合处，不在门板上；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一着手去推，它就成了一堵墙。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch06c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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


# ============ 第七章 · 一个环 ============
def ch07b_yi_ge_huan():
    body, y = head(380, 999, "为己是一条通道，尽头是枯；不为己是一个环，通了就能久",
                   "第 七 章 · 环", "一个环", "天地所以能长且久者，以其不自生，故能长生。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "两种活法的差别不在善恶，在闭环：为己的是一条单向通道，不为己的是一个循环。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "取进来、堵在里头，越堵越紧；生出去、收回来、再出去，通了就能久。", 5.0, "#6E6459", "middle"))

    # 一、为己：一条通道
    s.append(txt(24, y + 52, "一、为己：取进来，堵在里头", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="164" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy = gy + 84
    s.append(f'<line x1="52" y1="{cy - 26}" x2="286" y2="{cy - 26}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="52" y1="{cy + 26}" x2="286" y2="{cy + 26}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="286" y1="{cy - 26}" x2="286" y2="{cy + 26}" stroke="{INK}" stroke-width="3.0"/>')
    for k in range(4):
        s.append(f'<line x1="{238 + k * 10}" y1="{cy - 22}" x2="{238 + k * 10}" y2="{cy + 22}" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(arrow(66, cy, 128, cy, SEAL, 1.2, None, "arrS"))
    s.append(txt(74, cy - 34, "取", 5.0, SEAL))
    s.append(arrow(140, cy, 196, cy, SEAL, 1.0, None, "arrS"))
    s.append(txt(214, cy - 34, "堵", 5.0, SEAL, "middle"))
    s.append(txt(304, cy - 6, "尽头", 4.4, SEAL, "end"))
    s.append(txt(304, cy + 6, "是枯", 4.4, SEAL, "end"))
    s.append(txt(190, gy + 154, "通道只进不出：越堵越紧，紧到某处就尽", 4.5, SEAL, "middle"))

    # 二、不为己：一个环
    s.append(txt(24, gy + 192, "二、不为己：生出去，再回来", 5.2, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="164" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, ccy, rx, ry = 190, gy2 + 84, 92, 54
    s.append(f'<ellipse cx="{cx}" cy="{ccy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
    for k in range(4):
        ang = -90 + k * 90
        import math
        px = cx + rx * math.cos(math.radians(ang))
        py = ccy + ry * math.sin(math.radians(ang))
        s.append(f'<circle cx="{px}" cy="{py}" r="2.2" fill="{GREEN}"/>')
    s.append(f'<path d="M{cx-80:.0f},{ccy-27:.0f} Q{cx},{ccy-72:.0f} {cx+80:.0f},{ccy-27:.0f}" fill="none" stroke="{GREEN}" stroke-width="1.3" marker-end="url(#arr2)"/>')
    s.append(f'<path d="M{cx+80:.0f},{ccy+27:.0f} Q{cx},{ccy+72:.0f} {cx-80:.0f},{ccy+27:.0f}" fill="none" stroke="{GREEN}" stroke-width="1.3" marker-end="url(#arr2)"/>')
    s.append(txt(cx, ccy - 6, "空", 5.0, GREEN, "middle"))
    s.append(txt(cx + 104, ccy - 44, "生出去", 4.4, GREEN))
    s.append(txt(cx - 104, ccy + 52, "收回来", 4.4, GREEN, "end"))
    s.append(txt(190, gy2 + 154, "环里始终空着：不占住哪一段，才转得下去", 4.5, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "天地没有一颗「为我」的心，所以不被「取—耗」这条闭环困住。", 5.4, INK))
    s.append(txt(24, a + 16, "生发与归根往复流通，不滞一处，所以长久——这叫长生，不是求来的。", 5.4, INK))
    s.append(txt(24, a + 34, "不是先有一个长久的目标再去不自生；是先不自生，长久自己来。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "为己者，取而入，入而塞；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "不为己者，生而出，出而复。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch07b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第七章 · 一扇窄门 ============
def ch07c_yi_shan_zhai_men():
    body, y = head(380, 999, "后其身而身先：不是让出位置，是先让开门口",
                   "第 七 章 · 窄 门", "一扇窄门", "是以圣人后其身而身先，外其身而身存。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "窄门只容一人：两头同时挤，谁也过不去。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "后其身不是退到队尾等着后来居上，是先把门口让开——这一让，两个人都过去了。", 5.0, "#6E6459", "middle"))

    def gate(gx, gtop, gbot):
        out = []
        out.append(f'<rect x="{gx - 30}" y="{gtop}" width="9" height="{gbot - gtop}" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
        out.append(f'<rect x="{gx + 21}" y="{gtop}" width="9" height="{gbot - gtop}" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
        out.append(f'<line x1="{gx - 30}" y1="{gtop}" x2="{gx + 30}" y2="{gtop}" stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<line x1="{gx - 21}" y1="{gtop}" x2="{gx - 21}" y2="{gbot}" stroke="{INK}" stroke-width="0.7" stroke-dasharray="3 3"/>')
        out.append(f'<line x1="{gx + 12}" y1="{gtop}" x2="{gx + 12}" y2="{gbot}" stroke="{INK}" stroke-width="0.7" stroke-dasharray="3 3"/>')
        return "".join(out)

    # 一、挤
    s.append(txt(24, y + 52, "一、挤：两头同时抢，门卡住了", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    gx = 190
    s.append(gate(gx, gy + 40, gy + 128))
    s.append(f'<line x1="{gx - 21}" y1="{gy + 40}" x2="{gx - 21}" y2="{gy + 128}" stroke="{SEAL}" stroke-width="1.6"/>')
    s.append(f'<line x1="{gx + 12}" y1="{gy + 40}" x2="{gx + 12}" y2="{gy + 128}" stroke="{SEAL}" stroke-width="1.6"/>')
    # 两只手同时抓门
    for hx in (gx - 34, gx + 26):
        s.append(f'<rect x="{hx - 8}" y="{gy + 92}" width="16" height="13" rx="4" fill="#EFE6D4" stroke="{SEAL}" stroke-width="0.9"/>')
        for k in range(3):
            s.append(f'<rect x="{hx - 7 + k * 5}" y="{gy + 85}" width="3.4" height="8" rx="1.6" fill="#EFE6D4" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(arrow(gx - 76, gy + 70, gx - 34, gy + 96, SEAL, 0.9, None, "arrS"))
    s.append(arrow(gx + 76, gy + 70, gx + 34, gy + 96, SEAL, 0.9, None, "arrS"))
    s.append(txt(gx, gy + 150, "门只有一扇的宽：两人同时抓，谁也进不去", 4.5, SEAL, "middle"))

    # 二、让
    s.append(txt(24, gy + 196, "二、让：一人先松手，两个人都过去了", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(gate(gx, gy2 + 40, gy2 + 128))
    # 一人退半步（把门口让开）
    s.append(f'<path d="M{gx - 60},{gy2 + 128} q-16,4 -20,-12 q-3,-14 12,-16" fill="none" stroke="{GREEN}" stroke-width="1.0" marker-end="url(#arr2)"/>')
    s.append(txt(gx - 52, gy2 + 136, "退半步", 4.4, GREEN, "middle"))
    # 另一人先过
    s.append(arrow(gx - 100, gy2 + 90, gx + 74, gy2 + 90, GREEN, 1.1, None, "arr2"))
    s.append(txt(gx + 104, gy2 + 82, "先过", 4.4, GREEN, "middle"))
    # 让的人随后跟上
    s.append(arrow(gx - 100, gy2 + 112, gx + 46, gy2 + 112, GREEN, 1.0, None, "arr2"))
    s.append(txt(gx + 104, gy2 + 108, "跟上", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 150, "让开的不是位置，是门口：一让，路就通了", 4.5, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「后其身」不是装出一副退让的样子、心里等着后来居上——那是另一种抢。", 5.4, INK))
    s.append(txt(24, a + 16, "它说的是放下「我要争先、我要凸显」的那只手；手一松，门口就通了。", 5.4, INK))
    s.append(txt(24, a + 34, "这个「先」不是争来的，是人心自归的：争来的位置要守，推上来的位置不必守。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "退不是姿态，是把手松开；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "松开了，位置在哪，看势。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch07c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch08b_yi_chu_di_chu():
    body, y = head(380, 999, "位置低一点，对它没有分别——因为它有别的东西可以立",
                   "第 八 章 · 低 处", "一处低处", "处众人之所恶，故几于道。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「处众人之所恶」不是自苦，是把自己放在别人不要的位置上，而且安。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "一处是争来的位，一处是流到的位——位次要用力气守，归宿不必。", 4.9, "#6E6459", "middle"))

    # 一、争高与就下
    s.append(txt(24, y + 52, "一、争高与就下：人往上挤，水往下流", 5.2, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="190" y1="{gy + 12}" x2="190" y2="{gy + 168}" stroke="{LINE}" stroke-width="0.5" stroke-dasharray="2 3"/>')
    # 左：一道坡，三个人往上走
    sx0, sy0, sx1, sy1 = 36, gy + 152, 168, gy + 78
    s.append(f'<line x1="{sx0}" y1="{sy0}" x2="{sx1}" y2="{sy1}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{sx1}" y1="{sy1}" x2="{sx1}" y2="{sy0}" stroke="{LINE}" stroke-width="0.6" stroke-dasharray="2 3"/>')
    for fx in (66, 98, 130):
        fy = sy0 - (fx - sx0) * (sy0 - sy1) / (sx1 - sx0)
        s.append(f'<circle cx="{fx}" cy="{fy - 13}" r="2.6" fill="none" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx}" y1="{fy - 10.4}" x2="{fx}" y2="{fy - 3}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{fx}" y1="{fy - 3}" x2="{fx - 3.5}" y2="{fy}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx}" y1="{fy - 3}" x2="{fx + 3.5}" y2="{fy}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx - 4}" y1="{fy - 7}" x2="{fx + 4}" y2="{fy - 9}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(arrow(48, sy0 - 6, 84, sy0 - 27, SEAL, 0.9, None, "arr2"))
    s.append(txt(172, gy + 42, "争高", 4.6, SEAL, "end"))
    s.append(txt(172, gy + 54, "位越高，越要守", 4.2, "#6E6459", "end"))
    s.append(txt(100, gy + 168, "越往上，站的人越少，扶的人也越少", 4.2, "#6E6459", "middle"))
    # 右：一谷，两股水往下流
    s.append(f'<path d="M204,{gy + 58} L266,{gy + 134} L328,{gy + 58}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M238,{gy + 128} q14,-4 28,0 q14,4 28,0" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="240" y="{gy + 129}" width="52" height="4.5" fill="#E4EAE0" stroke="none"/>')
    s.append(arrow(212, gy + 48, 254, gy + 112, GREEN, 1.0, None, "arr2"))
    s.append(arrow(320, gy + 48, 278, gy + 112, GREEN, 1.0, None, "arr2"))
    s.append(txt(266, gy + 34, "就下", 4.6, GREEN, "middle"))
    s.append(txt(266, gy + 152, "众人所恶：没人要的低处", 4.2, "#6E6459", "middle"))
    s.append(txt(266, gy + 166, "安得住，是因为不靠位置定义自己", 4.2, GREEN, "middle"))

    # 二、江海为百谷王
    s.append(txt(24, gy + 196, "二、江海：把自己放在最低处，百川自来", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 水面
    s.append(f'<rect x="40" y="{gy2 + 120}" width="300" height="40" fill="#E4EAE0" stroke="none"/>')
    s.append(f'<path d="M40,{gy2 + 120} q20,-5 40,0 q20,5 40,0 q20,-5 40,0 q20,5 40,0 q20,-5 40,0 q20,5 40,0 q20,-5 40,0" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="40" y1="{gy2 + 160}" x2="340" y2="{gy2 + 160}" stroke="{LINE}" stroke-width="0.6"/>')
    # 五条川，自高处归下
    for rx in (66, 124, 190, 256, 314):
        s.append(f'<path d="M{rx},{gy2 + 18} C {rx + 8},{gy2 + 56} {rx + 4},{gy2 + 92} {rx},{gy2 + 116}" fill="none" stroke="{GREEN}" stroke-width="1.0"/>')
        s.append(arrow(rx, gy2 + 92, rx, gy2 + 114, GREEN, 0.9, None, "arr2"))
        s.append(f'<line x1="{rx - 8}" y1="{gy2 + 24}" x2="{rx + 8}" y2="{gy2 + 24}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(txt(54, gy2 + 146, "江海", 5.4, INK))
    s.append(txt(334, gy2 + 146, "百川归之", 4.4, GREEN, "end"))
    s.append(txt(190, gy2 + 168, "它不召、不催、不争——只在最低处，水自然来", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「恶」读 wù：厌弃、嫌弃。低处是人人躲开的地方，水偏偏在那里聚。", 5.2, INK))
    s.append(txt(24, a + 16, "它能安，是因为不靠位置来定义自己：位置高一点低一点，对它没有分别。", 5.2, INK))
    s.append(txt(24, a + 34, "学水不是学它的德，是学它把自己放到哪儿——先挪身，再谈修德。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "低处不是惩罚，是不必守的位置；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "水往那里去，是不争。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch08b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch08c_qi_jie_tong_guan():
    body, y = head(380, 999, "七善是一条链：不是七条戒律；链底是同一个本体",
                   "第 八 章 · 七 善", "一根七节管", "居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "七句常被读成七条并列的品德，各自打分。不是：它有次序，也有同一个底。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "先安身，再安心；心安了才有仁、有信；仁信立住，才谈得上理事、处事、动止。", 4.9, "#6E6459", "middle"))

    # 一、七只并排的短管
    s.append(txt(24, y + 52, "一、劈成七节：各盛一点，各打一个勾", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    names = ["地", "渊", "仁", "信", "治", "能", "时"]
    for i, nm in enumerate(names):
        cx = 26 + 24 + i * 45.5
        s.append(f'<rect x="{cx - 15:.0f}" y="{gy + 66}" width="30" height="46" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<rect x="{cx - 13:.0f}" y="{gy + 82}" width="26" height="28" fill="#E4EAE0" stroke="none"/>')
        s.append(f'<line x1="{cx - 13:.0f}" y1="{gy + 82}" x2="{cx + 13:.0f}" y2="{gy + 82}" stroke="{LINE}" stroke-width="0.6"/>')
        s.append(f'<line x1="{cx - 3:.0f}" y1="{gy + 40}" x2="{cx + 1:.0f}" y2="{gy + 50}" stroke="{SEAL}" stroke-width="1.0"/>')
        s.append(f'<line x1="{cx + 1:.0f}" y1="{gy + 50}" x2="{cx + 9:.0f}" y2="{gy + 34}" stroke="{SEAL}" stroke-width="1.1"/>')
        s.append(txt(cx, gy + 130, nm, 4.4, INK, "middle"))
        s.append(txt(cx, gy + 142, "一勾", 3.9, "#6E6459", "middle"))
    s.append(txt(190, gy + 166, "分开摆：各自打分，水在每一节停着——七善成了七条互不相干的戒律", 4.3, SEAL, "middle"))

    # 二、一根七节通管
    s.append(txt(24, gy + 196, "二、接成一根：一节通了，下一节才满", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    tx0, tx1 = 40, 340
    ty0, ty1 = gy2 + 54, gy2 + 78
    s.append(f'<rect x="{tx0}" y="{ty0}" width="{tx1 - tx0}" height="{ty1 - ty0}" fill="#E4EAE0" stroke="{INK}" stroke-width="1.2"/>')
    seg = (tx1 - tx0) / 7.0
    for i in range(1, 7):
        nx = tx0 + seg * i
        s.append(f'<line x1="{nx:.0f}" y1="{ty0 - 3}" x2="{nx:.0f}" y2="{ty1 + 3}" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<line x1="{nx + 3:.0f}" y1="{ty0 - 3}" x2="{nx + 3:.0f}" y2="{ty1 + 3}" stroke="{INK}" stroke-width="1.0"/>')
    for i, nm in enumerate(names):
        cx = tx0 + seg * (i + 0.5)
        s.append(txt(cx, ty0 - 12, nm, 4.4, INK, "middle"))
        s.append(arrow(cx - 8, ty0 + 11, cx + 10, ty0 + 11, GREEN, 0.8, None, "arr2"))
    s.append(arrow(tx0 - 12, ty0 + 11, tx0 - 2, ty0 + 11, GREEN, 1.0, None, "arr2"))
    s.append(arrow(tx1 + 2, ty0 + 11, tx1 + 12, ty0 + 11, GREEN, 1.0, None, "arr2"))
    s.append(txt(30, ty0 - 12, "身", 4.2, SEAL))
    s.append(txt(350, ty0 - 12, "事", 4.2, SEAL, "end"))
    s.append(f'<rect x="30" y="{gy2 + 126}" width="320" height="26" fill="#E4EAE0" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="{tx0 + 6}" y1="{ty1 + 4}" x2="{tx0 + 6}" y2="{gy2 + 126}" stroke="{GREEN}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(f'<line x1="{tx1 - 6}" y1="{ty1 + 4}" x2="{tx1 - 6}" y2="{gy2 + 126}" stroke="{GREEN}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(txt(190, gy2 + 144, "同一底层：本体不变，才随缘应化", 4.5, INK, "middle"))
    s.append(txt(190, gy2 + 166, "不跟容器较劲的不是没原则，是先把身、心、存心摆正，手段才接得上", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "第一组居与心，一外一内；第二组与与言，存心与兑现；第三组政、事、动，落地的一环。", 5.0, INK))
    s.append(txt(24, a + 16, "三者互相咬合：事与能互为支撑，动与时互为约束，政与治互为表里。", 5.0, INK))
    s.append(txt(24, a + 34, "存心不正而先学手段，学到的只是技巧——七善不是七处各自使劲。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "七善是一条链，不是七条戒律；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "链底是同一个本体：不变，才随缘。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch08c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))

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


def ch09b_yi_zhi_qi_qi():
    body, y = head(380, 999, "同一只器，只随水量改姿态——不是器坏，是水多了",
                   "第 九 章 · 欹 器", "一只欹器", "持而盈之，不如其已；揣而锐之，不可长保。", 999)
    s = [body]
    import math

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "鲁桓公之庙有一只器：虚则欹，中则正，满则覆。孔子叹：「恶有满而不覆者哉！」", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "器没有变，水也没有变——只是水多了一点，姿态就翻了。", 4.9, "#6E6459", "middle"))

    def vessel(px, py, ang, level, pour=False):
        """画一只挂在横梁上的欹器：ang 为倾角，level 为水量（0-26）。"""
        s.append(f'<g transform="rotate({ang},{px},{py})">')
        s.append(f'<path d="M{px - 16},{py - 14} L{px + 16},{py - 14} L{px + 10},{py + 12} L{px - 10},{py + 12} z" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{px - 16}" y1="{py - 14}" x2="{px + 16}" y2="{py - 14}" stroke="{INK}" stroke-width="1.4"/>')
        if level:
            wy = py + 12 - level
            half = 10 + (wy - (py + 12)) / -26 * 6
            s.append(f'<path d="M{px - half:.1f},{wy:.1f} L{px + half:.1f},{wy:.1f} L{px + 10},{py + 12} L{px - 10},{py + 12} z" fill="#E4EAE0" stroke="none"/>')
            s.append(f'<line x1="{px - half:.1f}" y1="{wy:.1f}" x2="{px + half:.1f}" y2="{wy:.1f}" stroke="{LINE}" stroke-width="0.7"/>')
        s.append(f'<circle cx="{px - 16}" cy="{py - 2}" r="2.2" fill="none" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<circle cx="{px + 16}" cy="{py - 2}" r="2.2" fill="none" stroke="{INK}" stroke-width="0.8"/>')
        s.append('</g>')
        s.append(f'<line x1="{px}" y1="{py - 45}" x2="{px}" y2="{py - 2}" stroke="{INK}" stroke-width="0.6"/>')
        s.append(f'<line x1="{px - 7}" y1="{py - 2}" x2="{px + 7}" y2="{py - 2}" stroke="{INK}" stroke-width="1.2"/>')
        if pour:
            a = math.radians(ang)
            lx, ly = 16, -14
            mx = px + lx * math.cos(a) - ly * math.sin(a)
            my = py + lx * math.sin(a) + ly * math.cos(a)
            s.append(f'<path d="M{mx:.0f},{my:.0f} C {mx + 3:.0f},{my + 4:.0f} {mx - 1:.0f},{my + 7:.0f} {mx - 4:.0f},{my + 11:.0f}" fill="none" stroke="{GREEN}" stroke-width="1.0"/>')

    # 一、三态
    s.append(txt(24, y + 52, "一、一只器，三种量", 5.2, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="42" y1="{gy + 28}" x2="348" y2="{gy + 28}" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(1, 8):
        s.append(f'<line x1="{42 + k * 40}" y1="{gy + 28}" x2="{42 + k * 40}" y2="{gy + 32}" stroke="{INK}" stroke-width="0.5"/>')
    vessel(88, gy + 104, -32, 0)
    vessel(190, gy + 104, 0, 13)
    vessel(292, gy + 104, 104, 26, True)
    s.append(txt(88, gy + 154, "虚则欹", 4.8, "#6E6459", "middle"))
    s.append(txt(190, gy + 154, "中则正", 4.8, INK, "middle"))
    s.append(txt(292, gy + 154, "满则覆", 4.8, SEAL, "middle"))
    s.append(txt(88, gy + 170, "空着，它自己斜", 4.1, "#6E6459", "middle"))
    s.append(txt(190, gy + 170, "半下，它自己正", 4.1, "#6E6459", "middle"))
    s.append(txt(292, gy + 170, "多一点，它就翻", 4.1, SEAL, "middle"))

    # 二、儒守道退
    s.append(txt(24, gy + 196, "二、同一只器，两种做法", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="190" y1="{gy2 + 12}" x2="190" y2="{gy2 + 164}" stroke="{LINE}" stroke-width="0.5" stroke-dasharray="2 3"/>')
    # 左：守——一手扶壁，水只到半
    s.append(f'<line x1="48" y1="{gy2 + 28}" x2="170" y2="{gy2 + 28}" stroke="{INK}" stroke-width="1.2"/>')
    vessel(96, gy2 + 104, 0, 13)
    s.append(f'<rect x="112" y="{gy2 + 84}" width="22" height="15" rx="5" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="126" y1="{gy2 + 88}" x2="134" y2="{gy2 + 92}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(96, gy2 + 138, "守：扶着它别倒", 4.6, INK, "middle"))
    s.append(txt(96, gy2 + 152, "水不加，手不松——日日用力", 4.2, "#6E6459", "middle"))
    # 右：退——手撤开，器自斜
    s.append(f'<line x1="210" y1="{gy2 + 28}" x2="332" y2="{gy2 + 28}" stroke="{INK}" stroke-width="1.2"/>')
    vessel(258, gy2 + 104, -30, 0)
    s.append(f'<rect x="300" y="{gy2 + 96}" width="22" height="15" rx="5" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(296, gy2 + 104, 322, gy2 + 104, SEAL, 0.9, None, "arrS"))
    s.append(txt(258, gy2 + 138, "退：不扶，也不加满", 4.6, SEAL, "middle"))
    s.append(txt(258, gy2 + 152, "空着，就自己斜着——一次决心", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「持」是攥住不放，「盈」是填到饱和：不是不能积累，是非要抵达圆满。", 5.2, INK))
    s.append(txt(24, a + 16, "虚，才有继续容纳的余地；满，就是循环的终点，紧跟着是散。", 5.2, INK))
    s.append(txt(24, a + 34, "孔子在庙里说要守，老子看着同一只器说要走——守是扶着别倒，退是根本不去扶。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "持满则溢，不如早止；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "揣锐则折，难以长保。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch09b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch09c_zan_yu_song():
    body, y = head(380, 999, "攥着，就先被它绑住；松开，功还是功",
                   "第 九 章 · 攥 与 松", "攥与松", "金玉满堂，莫之能守；富贵而骄，自遗其咎。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "四样东西都不是你的错，攥才是：攥着满的，满会溢；攥着锋的，锋会折。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "「功」是向外显的果，「身」是向内的根——退的不是事，是把根挪出果的那一下。", 4.9, "#6E6459", "middle"))

    # 一、攥
    s.append(txt(24, y + 52, "一、攥：越攥越紧，指节都白了", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 190, gy + 84
    # 印（被攥住的功）
    s.append(f'<rect x="{cx - 10}" y="{cy - 10}" width="20" height="15" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="{cx - 4}" y="{cy - 17}" width="8" height="7" fill="#E4D8BF" stroke="{INK}" stroke-width="0.8"/>')
    # 拳：掌＋四指横叠＋拇指
    s.append(f'<rect x="{cx - 17}" y="{cy - 12}" width="34" height="34" rx="7" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    for k in range(4):
        s.append(f'<rect x="{cx - 14}" y="{cy - 6 + k * 8}" width="28" height="6" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{cx - 22}" y="{cy - 4}" width="10" height="6" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx + 17}" y1="{cy + 2}" x2="{cx + 26}" y2="{cy + 10}" stroke="{INK}" stroke-width="0.8"/>')
    # 用力痕
    for k in range(2):
        s.append(f'<path d="M{cx + 30},{cy - 14 + k * 10} q6,4 0,8" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(cx + 30, cy - 20, "印", 4.4, SEAL))
    s.append(f'<line x1="{cx + 28}" y1="{cy - 18}" x2="{cx + 12}" y2="{cy - 14}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="3 2"/>')
    s.append(arrow(cx - 70, cy + 2, cx - 40, cy + 2, SEAL, 0.9, None, "arrS"))
    s.append(txt(cx - 74, cy + 2, "攥", 5.0, SEAL, "end"))
    s.append(txt(190, gy + 128, "攥住的是印，绑住的是手", 4.6, SEAL, "middle"))
    s.append(txt(190, gy + 146, "金玉满堂，莫之能守：相会散，守着它的人先被它锁住", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy + 160, "富贵而骄，自遗其咎：咎不是外面给的，是心里那口气招的", 4.2, "#6E6459", "middle"))

    # 二、松
    s.append(txt(24, gy + 196, "二、松：手摊开，印还在", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    hx, hy = 190, gy2 + 104
    # 摊开的手掌：掌＋四指向上＋拇指
    s.append(f'<rect x="{hx - 24}" y="{hy - 8}" width="48" height="26" rx="8" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    for k in range(4):
        fx = hx - 18 + k * 11
        s.append(f'<rect x="{fx}" y="{hy - 32}" width="8" height="26" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{hx + 24}" y="{hy - 14}" width="14" height="8" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    # 印落在掌上
    s.append(f'<rect x="{hx - 10}" y="{hy - 14}" width="20" height="15" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="{hx - 4}" y="{hy - 21}" width="8" height="7" fill="#E4D8BF" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(hx + 26, hy - 16, "印", 4.4, GREEN))
    s.append(arrow(hx + 76, hy - 40, hx + 40, hy - 30, GREEN, 0.9, None, "arr2"))
    s.append(txt(hx + 80, hy - 42, "松开", 4.4, GREEN))
    s.append(txt(190, gy2 + 128, "功还是功，人还是人：印没掉，手也不抖", 4.6, GREEN, "middle"))
    s.append(txt(190, gy2 + 146, "退的不是事，是恋；收的不是手，是心", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy2 + 160, "先功遂，再身退——没做成而先退，多半是给退缩找个好名字", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「退」，旧注多解作隐居避世。这一章不是：功成了，心不跟着功走，才是退。", 5.2, INK))
    s.append(txt(24, a + 16, "能进也能退，能显也能藏：下一段因缘来了，照样出来做事。", 5.2, INK))
    s.append(txt(24, a + 34, "四时春生夏长、秋收冬藏——收不是失败，是节律；只生不收，才是逆天。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "退的不是事，是恋；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "收的不是手，是心。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch09c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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


def ch10b_liang_lun_yi_zhou():
    body, y = head(380, 999, "一根轴，两轮同转；轴一断，两轮各自倒",
                   "第 十 章 · 抱 一", "两轮一轴", "载营魄抱一，能无离乎？", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「营魄」是魂与魄：魂气轻清，魄重浊；生时二者相合，死则相离。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "「载」是车载之载：一辆车，两根轮子穿在一根轴上，才走得动。", 4.9, "#6E6459", "middle"))

    def wheel(cx, cy, r=15):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
        for k in range(4):
            a = k * 45
            s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * 0.94:.0f}" y2="{cy}" stroke="{INK}" stroke-width="0.7" transform="rotate({a},{cx},{cy})"/>')

    # 一、抱一
    s.append(txt(24, y + 52, "一、抱一：一根轴，两轮同转", 5.2, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy = gy + 108
    s.append(f'<line x1="112" y1="{cy}" x2="268" y2="{cy}" stroke="{INK}" stroke-width="1.6"/>')
    wheel(112, cy)
    wheel(268, cy)
    s.append(f'<rect x="104" y="{cy - 44}" width="172" height="24" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="122" y1="{cy - 20}" x2="122" y2="{cy}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="258" y1="{cy - 20}" x2="258" y2="{cy}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="150" y1="{cy - 44}" x2="150" y2="{cy - 54}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="230" y1="{cy - 44}" x2="230" y2="{cy - 54}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="142" y1="{cy - 54}" x2="238" y2="{cy - 54}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(txt(190, cy - 62, "载：车上一副身，轴下一根一", 4.4, INK, "middle"))
    s.append(txt(112, cy + 30, "魂", 4.6, GREEN, "middle"))
    s.append(txt(268, cy + 30, "魄", 4.6, "#6E6459", "middle"))
    s.append(txt(190, cy - 7, "一＝轴", 4.4, GREEN, "middle"))
    s.append(txt(190, gy + 168, "两轮一轴：魂不出走，魄不自沉，人在此时此地", 4.3, GREEN, "middle"))

    # 二、离
    s.append(txt(24, gy + 196, "二、离：轴一断，两轮各归其处", 5.2, SEAL))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy2 = gy2 + 84
    s.append(f'<line x1="112" y1="{cy2}" x2="176" y2="{cy2}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="204" y1="{cy2}" x2="268" y2="{cy2}" stroke="{INK}" stroke-width="1.6"/>')
    for k in range(3):
        s.append(f'<line x1="{180 + k * 2}" y1="{cy2 + 5}" x2="{184 + k * 3}" y2="{cy2 - 8}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{198 + k * 2}" y1="{cy2 + 5}" x2="{202 + k * 3}" y2="{cy2 - 8}" stroke="{INK}" stroke-width="0.9"/>')
    wheel(112, cy2)
    wheel(268, cy2)
    s.append(arrow(112, cy2 - 24, 112, cy2 - 46, SEAL, 1.0, None, "arrS"))
    s.append(arrow(268, cy2 + 24, 268, cy2 + 44, SEAL, 1.0, None, "arrS"))
    s.append(txt(112, cy2 - 54, "魂：轻清，上归于天", 4.2, SEAL, "middle"))
    s.append(txt(268, cy2 + 54, "魄：重浊，下归于地", 4.2, SEAL, "middle"))
    s.append(txt(190, cy2 - 20, "断", 4.4, SEAL, "middle"))
    s.append(txt(190, gy2 + 160, "轴断了才招魂，人已经走了——老子问的是生前合不合得住", 4.3, "#6E6459", "middle"))
    s.append(txt(190, gy2 + 172, "《礼记》：「魂气归于天，形魄归于地」", 4.1, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "凡人最大的分裂在这里：肉身活在当下，心神活在别处——活在评判里、活在掌控里。", 5.2, INK))
    s.append(txt(24, a + 16, "「抱一」不是把两样捏成一样，是让它们回到同一根轴上：身在此时，心也回到此时。", 5.2, INK))
    s.append(txt(24, a + 34, "一分开，两头都空：身体在做这件事，心已经在算下一件。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "身在此时，心也回到此时；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一分开，两头都空。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch10b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch10c_yi_jian_jie_zhu_de_wu():
    body, y = head(380, 999, "对外做租客，对内做主人——这两句是一句",
                   "第 十 章 · 玄 德", "一间借住的屋", "生而不有，为而不恃，长而不宰，是谓玄德。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「爱民治国，能无为乎」：无为不是不做，是不主宰；管理是顺势成全，主宰是强行改造。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "租客也扫地、也浇花、也修瓦——只是知道屋子不是自己的。", 4.9, "#6E6459", "middle"))

    def house(px, py, plaque=False, repaint=False):
        s.append(f'<path d="M{px - 62},{py} L{px},{py - 40} L{px + 62},{py} z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<rect x="{px - 56}" y="{py}" width="112" height="58" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<rect x="{px - 12}" y="{py + 26}" width="24" height="32" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<circle cx="{px + 6}" cy="{py + 42}" r="1.6" fill="{INK}"/>')
        s.append(f'<rect x="{px - 44}" y="{py + 14}" width="22" height="18" fill="none" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{px - 33}" y1="{py + 14}" x2="{px - 33}" y2="{py + 32}" stroke="{INK}" stroke-width="0.5"/>')
        s.append(f'<line x1="{px - 44}" y1="{py + 23}" x2="{px - 22}" y2="{py + 23}" stroke="{INK}" stroke-width="0.5"/>')
        if plaque:
            s.append(f'<rect x="{px + 18}" y="{py + 12}" width="26" height="14" fill="{SEAL}" stroke="none" opacity="0.14"/>')
            s.append(f'<rect x="{px + 18}" y="{py + 12}" width="26" height="14" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
            s.append(txt(px + 31, py + 22, "我", 4.2, SEAL, "middle"))
            s.append(f'<line x1="{px + 44}" y1="{py + 19}" x2="{px + 52}" y2="{py + 19}" stroke="{SEAL}" stroke-width="0.7"/>')
        if repaint:
            s.append(f'<path d="M{px - 56},{py + 40} L{px - 12},{py + 40} L{px - 12},{py + 58} L{px - 56},{py + 58} z" fill="{SEAL}" stroke="none" opacity="0.12"/>')

    # 一、当主人
    s.append(txt(24, y + 52, "一、当主人：拆房改地，挂牌作主", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    house(112, gy + 62, plaque=True, repaint=True)
    s.append(txt(186, gy + 44, "主人三件事", 4.6, SEAL))
    s.append(txt(186, gy + 60, "① 墙上挂牌：「我」", 4.3, SEAL))
    s.append(txt(186, gy + 74, "② 墙刷成我的颜色", 4.3, SEAL))
    s.append(txt(186, gy + 88, "③ 手里攥着契", 4.3, SEAL))
    s.append(f'<rect x="286" y="{gy + 82}" width="24" height="14" fill="{PAPER}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(298, gy + 92, "契", 4.2, SEAL, "middle"))
    s.append(f'<line x1="282" y1="{gy + 89}" x2="252" y2="{gy + 89}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="3 2"/>')
    s.append(txt(186, gy + 104, "房不是他的，人先被房绑住", 4.2, "#6E6459"))
    s.append(txt(112, gy + 146, "当主人：拆房改地，挂牌作主", 4.3, SEAL, "middle"))
    s.append(txt(112, gy + 160, "生而不有：你可以建，它不属于你", 4.1, "#6E6459", "middle"))

    # 二、当租客
    s.append(txt(24, gy + 196, "二、当租客：扫、养、修，走时不拆房", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    house(112, gy2 + 60)
    s.append(f'<rect x="130" y="{gy2 + 72}" width="26" height="14" fill="none" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(143, gy2 + 82, "空", 4.0, "#A89577", "middle"))
    s.append(txt(186, gy2 + 46, "当租客：三样都做", 4.6, GREEN))
    s.append(txt(186, gy2 + 62, "扫屋、浇花、修瓦", 4.3, GREEN))
    s.append(txt(186, gy2 + 78, "不挂牌、不拆改、不作主", 4.3, GREEN))
    s.append(txt(186, gy2 + 92, "走时屋还是那间屋", 4.2, "#6E6459"))
    s.append(txt(112, gy2 + 146, "当租客：扫、养、修，走时不拆房", 4.3, GREEN, "middle"))
    s.append(txt(112, gy2 + 160, "生之畜之：能养，却不作它的主", 4.1, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "对外当主人，是妄；对内当租客，是逃——同一个病的两头。", 5.2, INK))
    s.append(txt(24, a + 16, "天地借我们暂住：能做的，是住得好一点，走时别拆房。", 5.2, INK))
    s.append(txt(24, a + 34, "做得多，占得少：这不是又一套要修成的德，就是那四句本身。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "生它、养它、让它长；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "不占有、不恃功、不作主。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch10c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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



def ch12b_tian_men_wu_lu():
    body, y = head(380, 999, "门照开，权收回：受于身，不如治于身",
                   "第 十 二 章 · 天 门", "五路进门", "五色令人目盲；五音令人耳聋；五味令人口爽。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "失守不是外物打进来，是接收那一头自己垮了：色、声、味本无善恶。", 4.9, INK, "middle"))
    s.append(txt(190, y + 28, "「天门」是耳目口鼻那道门；门可以开，权要在自己手里。", 4.9, "#6E6459", "middle"))

    names = ["色", "声", "味", "驰", "货"]

    def goods(x, gy):
        for i, nm in enumerate(names):
            yy = gy + 46 + i * 19
            s.append(f'<rect x="{x}" y="{yy}" width="26" height="13" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
            s.append(txt(x + 13, yy + 9.6, nm, 3.9, INK, "middle"))

    def door(gy):
        s.append(f'<line x1="74" y1="{gy + 28}" x2="74" y2="{gy + 150}" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<line x1="98" y1="{gy + 28}" x2="98" y2="{gy + 150}" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<line x1="66" y1="{gy + 26}" x2="106" y2="{gy + 26}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(txt(86, gy + 20, "天门", 4.0, "#A89577", "middle"))

    def boundary(gy):
        s.append(f'<line x1="216" y1="{gy + 22}" x2="216" y2="{gy + 158}" stroke="{LINE2}" stroke-width="0.7" stroke-dasharray="4 3"/>')
        s.append(txt(216, gy + 16, "内", 4.0, "#A89577", "middle"))

    # 一、受于身：身内塞满
    s.append(txt(24, y + 52, "一、受于身：五样一律进到身里，人成了货架", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    door(gy)
    goods(32, gy)
    boundary(gy)
    for i in range(5):
        yy = gy + 52 + i * 19
        s.append(arrow(104, yy + 6, 252, yy + 6, SEAL, 0.8, None, "arrS"))
    # 身：一个框，里面挤满
    sx, sy = 258, gy + 40
    s.append(f'<rect x="{sx}" y="{sy}" width="60" height="80" rx="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(5):
        xx = sx + 4 + (k % 2) * 30
        yy = sy + 4 + (k // 2) * 15
        if k == 4:
            xx, yy = sx + 16, sy + 64
        s.append(f'<rect x="{xx}" y="{yy}" width="26" height="13" fill="#EFE6D4" stroke="{INK}" stroke-width="0.6"/>')
        s.append(txt(xx + 13, yy + 9.4, names[k], 3.6, INK, "middle"))
    s.append(txt(sx + 30, sy + 94, "身", 4.4, INK, "middle"))
    s.append(txt(292, gy + 160, "塞满了：里头没有一处是自己的", 4.2, SEAL, "middle"))
    s.append(txt(292, gy + 172, "以物役己：他被物占着", 4.2, "#6E6459", "middle"))

    # 二、治于身：门口过一手
    s.append(txt(24, gy + 196, "二、治于身：门照开，东西先在门口过一手", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    door(gy2)
    goods(32, gy2)
    boundary(gy2)
    # 手
    hx, hy = 106, gy2 + 92
    s.append(f'<rect x="{hx}" y="{hy - 8}" width="19" height="17" rx="5" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
    for k in range(4):
        s.append(f'<rect x="{hx + 2 + k * 4.4}" y="{hy - 17}" width="3.4" height="10" rx="1.7" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(120, hy - 20, "接住", 4.0, GREEN, "middle"))
    # 架：两层
    for k in range(2):
        yy = gy2 + 58 + k * 38
        s.append(f'<line x1="132" y1="{yy}" x2="206" y2="{yy}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="134" y1="{yy}" x2="134" y2="{yy + 16}" stroke="{LINE}" stroke-width="0.6"/>')
        s.append(f'<line x1="204" y1="{yy}" x2="204" y2="{yy + 16}" stroke="{LINE}" stroke-width="0.6"/>')
    for k, nm in enumerate(["色", "味", "声"]):
        xx = 138 + k * 24
        yy = gy2 + 44 if k < 2 else gy2 + 82
        if k == 2:
            xx = 152
        s.append(f'<rect x="{xx}" y="{yy}" width="22" height="13" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
        s.append(txt(xx + 11, yy + 9.4, nm, 3.6, INK, "middle"))
    # 身：空
    sx2, sy2 = 262, gy2 + 40
    s.append(f'<rect x="{sx2}" y="{sy2}" width="56" height="80" rx="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{sx2 + 28}" cy="{sy2 + 42}" r="9" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(sx2 + 28, sy2 + 45, "心", 3.8, GREEN, "middle"))
    s.append(txt(sx2 + 28, sy2 + 94, "身", 4.4, INK, "middle"))
    s.append(txt(292, gy2 + 148, "身上是空的，心口那一处是静的", 4.2, GREEN, "middle"))
    s.append(txt(292, gy2 + 162, "以物养己：拿它养身，不让它役心", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「受于身」，是外物到来、感官被动接住，这一步不由人做主；「治于身」是接住之后怎么办。", 5.1, INK))
    s.append(txt(24, a + 16, "门照开，权收回：色、声、味是天地本来就有的景致，可以欣赏，不可以占有、绑架。", 5.1, INK))
    s.append(txt(24, a + 34, "一旦把「体验」变成「我要留住、独享」，就从观物变成了执物——明明还在看，其实已经看不见。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "色不盲人，逐色者自盲；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "门照开，权收回。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch12b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch12c_wei_fu_bu_wei_mu():
    body, y = head(380, 999, "为腹者，以物养己；为目者，以物役己",
                   "第 十 二 章 · 腹 与 目", "为腹不为目", "是以圣人为腹不为目，故去彼取此。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "王弼注：为腹者，以物养己；为目者，以物役己。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "同一件外物，可以养你，也可以役你；分别不在物，在谁牵着谁。", 4.8, "#6E6459", "middle"))

    def stick(hx, hy, lean=0):
        """一个不带脸的简笔身：hx,hy 为颈根，lean>0 则头偏向左侧。"""
        s.append(f'<circle cx="{hx - lean}" cy="{hy - 8}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{hx - lean}" y1="{hy - 2}" x2="{hx + (2 if lean else 0)}" y2="{hy + 28}" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<line x1="{hx}" y1="{hy + 28}" x2="{hx - 7}" y2="{hy + 40}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{hx}" y1="{hy + 28}" x2="{hx + 7}" y2="{hy + 40}" stroke="{INK}" stroke-width="1.0"/>')

    # 一、为目：以物役己
    s.append(txt(24, y + 52, "一、为目：一只眼占满，人被一条线牵着往前跑", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    for k, nm in enumerate(["色", "声", "货"]):
        yy = gy + 46 + k * 28
        s.append(f'<rect x="34" y="{yy}" width="26" height="14" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
        s.append(txt(47, yy + 10.4, nm, 3.9, INK, "middle"))
        s.append(arrow(64, yy + 8, 108, gy + 84 + (k - 1) * 16, SEAL, 0.8, None, "arrS"))
    # 大眼
    ex, ey = 150, gy + 84
    s.append(f'<path d="M{ex - 42},{ey} Q{ex},{ey - 27} {ex + 42},{ey} Q{ex},{ey + 27} {ex - 42},{ey} z" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<circle cx="{ex}" cy="{ey}" r="11" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="{ex}" cy="{ey}" r="5" fill="{SEAL}" stroke={'"' + INK + '"'} stroke-width="0.7"/>')
    s.append(txt(ex, ey + 44, "眼越大，越看不见", 4.2, SEAL, "middle"))
    # 人：颈上系线，身子前倾
    px, py = 296, gy + 66
    stick(px, py, lean=12)
    s.append(f'<path d="M{ex + 40},{ey} Q{ex + 92},{ey - 26} {px - 8},{py + 1}" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(f'<circle cx="{px - 8}" cy="{py + 1}" r="2.3" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(px - 14, gy + 152, "人被牵着，脚在动，眼不在自己", 4.2, SEAL, "middle"))
    s.append(txt(px - 14, gy + 166, "以物役己：他是物的奴", 4.2, "#6E6459", "middle"))

    # 二、为腹：以物养己
    s.append(txt(24, gy + 196, "二、为腹：一点食进了肚，人立定不动", 5.2, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    bx, by = 112, gy2 + 86
    s.append(f'<path d="M{bx - 30},{by} q30,32 60,0 z" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="{bx}" cy="{by}" rx="30" ry="6" fill="#E4EAE0" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{bx - 9}" cy="{by - 2}" r="2.6" fill="#D8C6A0" stroke="{INK}" stroke-width="0.5"/>')
    s.append(f'<circle cx="{bx + 7}" cy="{by - 3}" r="2.2" fill="#D8C6A0" stroke="{INK}" stroke-width="0.5"/>')
    s.append(txt(bx, by + 38, "甘其食：安于本味", 4.2, GREEN, "middle"))
    # 人：立定，腹有一点
    px2, py2 = 288, gy2 + 62
    stick(px2, py2, lean=0)
    s.append(f'<circle cx="{px2}" cy="{py2 + 16}" r="6" fill="#E4EAE0" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(arrow(bx + 32, by - 2, px2 - 12, py2 + 16, GREEN, 0.9, None, "arr2"))
    s.append(f'<line x1="40" y1="{gy2 + 104}" x2="302" y2="{gy2 + 104}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(txt(px2, gy2 + 148, "养身：一口够了，心不必跟着食跑", 4.2, GREEN, "middle"))
    s.append(txt(px2, gy2 + 162, "以物养己：东西进来，人还在自己这儿", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「为腹」不是不吃不喝，是重心放在内里的足；「为目」不是不要眼睛，是把重心交给不断变化的外表。", 5.0, INK))
    s.append(txt(24, a + 16, "外物只给短暂刺激，刺激会钝化，钝化就要求加码——加到最后，人被牵着跑，成了物的奴。", 5.0, INK))
    s.append(txt(24, a + 34, "所以不是拒绝刺激，是换一个主人：外物来，坦然接纳；外物去，安然放手。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "为腹者，以物养己；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "为目者，以物役己。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch12c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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



def ch13b_ding_zai_bi_shang():
    body, y = head(380, 999, "惊的不是宠辱，是那个钉在壁上的我",
                   "第 十 三 章 · 壁 与 钉", "一枚钉", "宠辱皆外影，忧患由执我，根在此身藏。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "标签本无力量；它要惊动人，先得人自己把它接上身。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "「宠为下」：一求它，评判的权柄就交到别人手里了。", 4.8, "#6E6459", "middle"))

    def wall(gy, label=True, top=26, bot=150):
        s.append(f'<path d="M140,{gy + top} Q116,{gy + (top + bot) / 2} 140,{gy + bot}" fill="none" stroke="{INK}" stroke-width="2.0"/>')
        s.append(f'<path d="M154,{gy + top} Q130,{gy + (top + bot) / 2} 154,{gy + bot}" fill="none" stroke="{LINE}" stroke-width="1.0" stroke-dasharray="4 3"/>')
        if label:
            s.append(txt(164, gy + 42, "壁＝身", 4.1, "#8A7C69"))
            s.append(txt(164, gy + 52, "血肉之身，也是执念之我", 3.6, "#8A7C69"))

    # 一、钉在壁上
    s.append(txt(24, y + 52, "一、钉在壁上：牌子挂在钉上，风一吹就两头摇", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="184" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    wall(gy)
    # 钉 + 牌
    px0, py0 = 146, gy + 78
    s.append(f'<circle cx="{px0 + 4}" cy="{py0}" r="2.3" fill="{INK}"/>')
    s.append(f'<line x1="{px0 + 4}" y1="{py0}" x2="{px0 + 10}" y2="{py0 + 6}" stroke="#8A7C69" stroke-width="0.7"/>')
    s.append(f'<rect x="{px0 + 8}" y="{py0 + 6}" width="34" height="40" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(px0 + 25, py0 + 33, "我", 9.2, SEAL, "middle"))
    # 摆动虚弧
    s.append(f'<path d="M{px0 + 8},{py0 + 46} q-12,7 -15,-4" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(f'<path d="M{px0 + 42},{py0 + 46} q12,7 15,-4" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    # 宠（左）/ 辱（右），各得、失两箭，直抵牌缘
    s.append(arrow(42, gy + 62, px0 + 6, py0 + 16, GREEN, 0.9, None, "arr2"))
    s.append(arrow(42, gy + 122, px0 + 6, py0 + 34, GREEN, 0.9, None, "arr2"))
    s.append(arrow(338, gy + 62, px0 + 44, py0 + 16, SEAL, 0.9, None, "arrS"))
    s.append(arrow(338, gy + 122, px0 + 44, py0 + 34, SEAL, 0.9, None, "arrS"))
    s.append(txt(44, gy + 58, "宠·得", 4.3, GREEN))
    s.append(txt(44, gy + 136, "宠·失", 4.3, GREEN))
    s.append(txt(336, gy + 58, "辱·加", 4.3, SEAL, "end"))
    s.append(txt(336, gy + 136, "辱·夺", 4.3, SEAL, "end"))
    s.append(txt(190, gy + 178, "得也惊，失也惊：同一根钉，两头都晃", 4.4, SEAL, "middle"))

    # 二、揭下来
    s.append(txt(24, gy + 200, "二、揭下来：钉子拔了，壁还在，人不跟着晃", 5.2, GREEN))
    gy2 = gy + 212
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    wall(gy2, label=False, top=18, bot=124)
    s.append(f'<line x1="{px0 + 2}" y1="{py0 - gy + gy2}" x2="{px0 + 8}" y2="{py0 - gy + gy2}" stroke="#A89577" stroke-width="0.7"/>')
    s.append(f'<circle cx="{px0 + 8}" cy="{py0 - gy + gy2}" r="3.4" fill="none" stroke="#A89577" stroke-width="0.7" stroke-dasharray="2 2"/>')
    s.append(txt(px0 + 16, py0 - gy + gy2 + 4, "钉孔还在，钉子不在了", 3.9, "#8A7C69"))
    # 牌子搁在地上
    s.append(f'<ellipse cx="216" cy="{gy2 + 124}" rx="27" ry="3.4" fill="#E6D8C2" stroke="none"/>')
    s.append(f'<rect x="196" y="{gy2 + 106}" width="40" height="14" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(txt(216, gy2 + 117, "我", 6.0, SEAL, "middle"))
    s.append(txt(244, gy2 + 118, "牌子搁下了，壁不动", 4.1, "#6E6459"))
    s.append(txt(190, gy2 + 150, "壁不可碎，执壁为我才碎；身不可弃，执身为我方困", 4.4, GREEN, "middle"))

    a = gy2 + 184
    s.append(txt(24, a, "宠辱是外影，随光而变；忧患由执我，因壁而立。", 5.1, INK))
    s.append(txt(24, a + 16, "养这个身，不据这个身：壁要养厚，却不必把「我」钉在上面。", 5.1, INK))
    s.append(txt(24, a + 34, "钉子一拔，风还在吹，壁不晃了——荣辱找不到落脚的地方。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "壁不可碎，执壁为我才碎；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "身不可弃，执身为我方困。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch13b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch13c_bao_yu_tuo():
    body, y = head(380, 999, "养这个身，不据这个身：抱紧了是执，托平了才是器",
                   "第 十 三 章 · 抱 与 托", "抱与托", "贵以身为天下，若可寄天下；爱以身为天下，若可托天下。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「若」旧训为「乃」，作「才能」解，不是「好像」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "天下不是交给他去占有，是寄放、托付。", 4.8, "#6E6459", "middle"))

    def bowl(cx, cy, w):
        s.append(f'<path d="M{cx - w},{cy} q{w},32 {w * 2},0 z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="5" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')

    def man(hx, hy, look=0):
        """简笔人：hx,hy 为颈根；look>0 头偏右（抬头向前），look<0 头偏左（低头）。"""
        s.append(f'<circle cx="{hx + look}" cy="{hy - 8}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{hx + look}" y1="{hy - 2}" x2="{hx}" y2="{hy + 28}" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<line x1="{hx}" y1="{hy + 28}" x2="{hx - 7}" y2="{hy + 40}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{hx}" y1="{hy + 28}" x2="{hx + 7}" y2="{hy + 40}" stroke="{INK}" stroke-width="1.0"/>')

    # 一、抱：执身
    s.append(txt(24, y + 52, "一、抱：双臂环住往里收，杯子被挤得变形", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 128, gy + 52
    bowl(cx, cy, 26)
    # 双臂：自两侧收拢、在杯下交抱的一道弧
    s.append(f'<path d="M{cx - 50},{cy + 2} Q{cx - 54},{cy + 40} {cx},{cy + 46} Q{cx + 54},{cy + 40} {cx + 50},{cy + 2}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    # 挤压：两侧小箭头向内
    s.append(arrow(cx - 24, cy + 12, cx - 10, cy + 12, SEAL, 0.8, None, "arrS"))
    s.append(arrow(cx + 24, cy + 12, cx + 10, cy + 12, SEAL, 0.8, None, "arrS"))
    s.append(txt(cx, gy + 132, "抱得越紧，杯壁越薄：越怕失，越易碎", 4.2, SEAL, "middle"))
    man(292, gy + 60, look=-5)
    s.append(txt(292, gy + 132, "低着头，只看见自己这一只", 4.2, SEAL, "middle"))
    s.append(txt(292, gy + 146, "贵身成了执身：又落回攀缘", 4.2, "#6E6459", "middle"))

    # 二、托：器不自贵
    s.append(txt(24, gy + 192, "二、托：双手摊平往上承，杯子立在掌心，人抬头看前头", 5.2, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx2, cy2 = 122, gy2 + 44
    bowl(cx2, cy2, 24)
    # 掌：一片摊平的手，杯立在掌心
    py0 = cy2 + 34
    s.append(f'<path d="M{cx2 - 40},{py0 - 4} Q{cx2},{py0 + 18} {cx2 + 40},{py0 - 4}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<path d="M{cx2 - 40},{py0 - 4} q-6,-8 0,-12 M{cx2 + 40},{py0 - 4} q6,-8 0,-12" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(cx2, py0 + 34, "器不自贵，才能受重", 4.2, GREEN, "middle"))
    man(268, gy2 + 42, look=6)
    s.append(arrow(300, gy2 + 22, 324, gy2 + 22, GREEN, 0.9, None, "arr2"))
    s.append(txt(326, gy2 + 25, "天下", 4.0, GREEN))
    s.append(txt(268, gy2 + 126, "抬起头来，眼里有别人那具身", 4.2, GREEN, "middle"))
    s.append(txt(268, gy2 + 140, "先能自护自明，才不拿标尺去伤别人", 4.2, "#6E6459", "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "向外追荣辱是执，向内抱紧「我要贵身」也是执：前者把壁加厚，后者把壁擦亮再抱住不放。", 5.0, INK))
    s.append(txt(24, a + 16, "贵身是顺其自然的护持，不是刻意的抓取；无身是放下执念，不是厌弃生命。", 5.0, INK))
    s.append(txt(24, a + 34, "能养此身而不据此身的人，天下才敢寄在他手里——他既不拿自己去换什么，也不会拿别人去换什么。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "养身如养器，护壁不据壁；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "惜命不惜执，空心不弃生。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch13c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch14b_san_zhi_tan_zhen():
    body, y = head(380, 999, "眼耳手探不到，不等于没有：把标准降回工具",
                   "第 十 四 章 · 三 样 工 具", "三支探针", "视之不见名曰夷，听之不闻名曰希，搏之不得名曰微。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "人能感知的就算有、感知不到的就算无——这是习惯，不是标准。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "夷：无色；希：无声；微：无质。三样都不是「没有」，是「不及」。", 4.8, "#6E6459", "middle"))

    def field(x, gy, h, cap="道·场：不在三样工具的射程里"):
        s.append(f'<rect x="{x}" y="{gy + 18}" width="{330 - x}" height="{h - 26}" fill="#F1EDE2" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="5 4"/>')
        s.append(txt((x + 330) / 2, gy + 32, cap, 3.9, "#8A7C69", "middle"))

    # 一、三支探针
    s.append(txt(24, y + 52, "一、三支探针伸进去：各探一段，都在半路上断了", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="202" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    field(150, gy, 196)
    rows = [("眼", "视之不见：夷", 4), ("耳", "听之不闻：希", 5), ("手", "搏之不得：微", 6)]
    for i, (g, note, k) in enumerate(rows):
        yy = gy + 52 + i * 34
        s.append(f'<circle cx="40" cy="{yy}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(txt(40, yy + 3, g, 4.2, INK, "middle"))
        s.append(f'<line x1="48" y1="{yy}" x2="{150 + k * 14}" y2="{yy}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{150 + k * 14}" y1="{yy}" x2="{158 + k * 14}" y2="{yy}" stroke="{LINE}" stroke-width="1.0" stroke-dasharray="2 3"/>')
        s.append(f'<circle cx="{162 + k * 14}" cy="{yy}" r="4.5" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="2 2"/>')
        s.append(txt(200, yy + 10, note, 4.1, SEAL))
    s.append(txt(190, gy + 194, "探不到的地方不是空的，是探针够不着", 4.3, SEAL, "middle"))

    # 二、收针归场
    s.append(txt(24, gy + 216, "二、收针：遇不到，只能归；遇见要伸手，归依要收手", 5.2, GREEN))
    gy2 = gy + 228
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    field(120, gy2, 150, "道·场")
    for i in range(3):
        s.append(f'<line x1="36" y1="{gy2 + 122 + i * 8}" x2="70" y2="{gy2 + 122 + i * 8}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(txt(52, gy2 + 154, "三支针搁下", 3.9, "#8A7C69", "middle"))
    # 人立，一箭向内
    px, py = 84, gy2 + 54
    s.append(f'<circle cx="{px}" cy="{py}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 6}" x2="{px}" y2="{py + 34}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px - 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px + 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(arrow(px + 14, gy2 + 66, 118, gy2 + 66, GREEN, 1.0, None, "arr2"))
    s.append(txt(px + 16, gy2 + 60, "归", 4.6, GREEN))
    s.append(txt(190, gy2 + 168, "物可遇，道只能归：方向不同，姿势也不同", 4.3, GREEN, "middle"))

    a = gy2 + 188
    s.append(txt(24, a, "眼耳手是工具，不是真理的裁判；探得到的是万象，探不到的是万象的背景。", 5.0, INK))
    s.append(txt(24, a + 16, "「不可致诘」不是问不出来，是问的人与所问之物本不在一个层面。", 5.0, INK))
    s.append(txt(24, a + 34, "混而为一的「一」，不是数量的一，是分别还没有生起时的那个整全。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "探不到不等于没有，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "探得到也不等于全部。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch14b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch14c_gu_sheng_yu_jin():
    body, y = head(380, 999, "执古之道，以御今之有：一根准绳，量得住今天的手",
                   "第 十 四 章 · 准 绳", "一根准绳", "执古之道，以御今之有；能知古始，是谓道纪。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "今之尺各说各话：同一样东西，谁量谁是数。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "古始是一切存在共同的源头；执古，是用那根共同的绳去量。", 4.8, "#6E6459", "middle"))

    # 一、三把尺
    s.append(txt(24, y + 52, "一、三把今尺：同一只箱，量出三个数", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 箱
    bx, by = 60, gy + 44
    s.append(f'<rect x="{bx}" y="{by}" width="56" height="48" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{bx}" y1="{by + 16}" x2="{bx + 56}" y2="{by + 16}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<line x1="{bx}" y1="{by + 32}" x2="{bx + 56}" y2="{by + 32}" stroke="{LINE}" stroke-width="0.7"/>')
    for i, (L, num, nm) in enumerate([(78, "三", "甲尺"), (94, "五", "乙尺"), (110, "七", "丙尺")]):
        yy = by + 6 + i * 16
        s.append(f'<line x1="{bx + 60}" y1="{yy}" x2="{bx + 60 + L}" y2="{yy}" stroke="{INK}" stroke-width="1.0"/>')
        for k in range(1, 5):
            xx = bx + 60 + L * k / 5
            s.append(f'<line x1="{xx}" y1="{yy - 3}" x2="{xx}" y2="{yy + 3}" stroke="{LINE}" stroke-width="0.8"/>')
        s.append(txt(bx + 74 + L, yy + 2, num, 4.4, SEAL))
    s.append(txt(190, gy + 138, "甲、乙、丙三把今尺，各有各的刻：同一只箱，量出三个数", 4.3, SEAL, "middle"))

    # 二、一根古绳
    s.append(txt(24, gy + 166, "二、一根古绳：拉直了，箱子挂上去，只得一个数", 5.2, GREEN))
    gy2 = gy + 178
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    hy = gy2 + 66
    s.append(f'<path d="M52,{hy} q140,8 276,0" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    for k in range(13):
        xx = 52 + k * 23
        s.append(f'<circle cx="{xx}" cy="{hy + 3}" r="2.0" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(52, gy2 + 56, "古·本始", 4.2, GREEN))
    s.append(txt(328, gy2 + 56, "今·有", 4.2, GREEN, "end"))
    # 箱挂在绳上
    s.append(f'<line x1="166" y1="{hy + 2}" x2="166" y2="{hy + 22}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="140" y="{hy + 22}" width="52" height="46" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="140" y1="{hy + 37}" x2="192" y2="{hy + 37}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<line x1="140" y1="{hy + 53}" x2="192" y2="{hy + 53}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(txt(196, hy + 44, "一个数：同一根绳上的同一个结", 4.1, GREEN))
    s.append(txt(52, gy2 + 164, "绳绳兮不可名：它一直在起作用，却始终没有名字", 4.3, GREEN))

    a = gy2 + 196
    s.append(txt(24, a, "古不是过去，是本始：一切存在共同的源头。执古不是复古，是拿那根共同的绳来量今天。", 4.9, INK))
    s.append(txt(24, a + 16, "御不是驭世，是安己：手里的物有了定数，人就不必再拿自己的尺去争一个高低。", 4.9, INK))
    s.append(txt(24, a + 34, "能知古始，是谓道纪——知道了万物的来处，才有一根不被风向吹弯的准绳。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "执古之道，以御今之有；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "不是驭世，是安己。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch14c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch15b_dong_chuan():
    body, y = head(380, 999, "豫兮若冬涉川：不是不敢过，是不肯踏碎它",
                   "第 十 五 章 · 涉 川", "冬涉川", "豫兮若冬涉川，犹兮若畏四邻。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "七喻皆是一「不」：不抢先、不逼近、不占满。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "冰薄，脚重；心一急，先碎的是脚下的路。", 4.8, "#6E6459", "middle"))

    def ice(gy):
        s.append(f'<rect x="26" y="{gy + 96}" width="328" height="52" fill="#EDEFEA" stroke="none"/>')
        s.append(f'<line x1="26" y1="{gy + 96}" x2="354" y2="{gy + 96}" stroke="#8A9A92" stroke-width="0.9"/>')
        for k in range(9):
            xx = 44 + k * 36
            s.append(f'<line x1="{xx}" y1="{gy + 100}" x2="{xx - 6}" y2="{gy + 118}" stroke="#B9C4BC" stroke-width="0.6"/>')
        s.append(txt(40, gy + 164, "冬河·薄冰", 4.1, "#6E6459"))

    # 一、一步试
    s.append(txt(24, y + 52, "一、一步试：脚尖先点一下，冰上裂一圈", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="184" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ice(gy)
    # 一条腿自上方来，脚尖点在冰上
    fx, fy = 176, gy + 96
    s.append(f'<line x1="{fx - 4}" y1="{gy + 26}" x2="{fx - 1}" y2="{fy - 8}" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<path d="M{fx - 11},{fy - 8} q12,-3 21,2 q7,3 3,6 q-12,3 -24,1 z" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
    for dx in (-22, -14, -5, 6, 15):
        s.append(f'<line x1="{fx + dx}" y1="{fy + 1}" x2="{fx + dx + (4 if dx > 0 else -4)}" y2="{fy + 11}" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(fx + 44, fy - 10, "点一下：听它响不响", 4.1, SEAL))
    s.append(txt(190, gy + 176, "豫：不是慢，是先把脚下的实虚探清", 4.3, SEAL, "middle"))

    # 二、轻步过
    s.append(txt(24, gy + 200, "二、轻步过：人到了对岸，冰面还是完的", 5.2, GREEN))
    gy2 = gy + 212
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ice(gy2)
    for k in range(5):
        s.append(f'<ellipse cx="{84 + k * 24}" cy="{gy2 + 96}" rx="4" ry="1.8" fill="#C9D2CA" stroke="none"/>')
    # 两岸：左小滩、右岸
    s.append(f'<path d="M26,{gy2 + 96} L64,{gy2 + 96} L64,{gy2 + 78} L26,{gy2 + 82} z" fill="#E4E7E0" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M296,{gy2 + 96} L354,{gy2 + 96} L354,{gy2 + 74} L296,{gy2 + 80} z" fill="#E4E7E0" stroke="{LINE}" stroke-width="0.8"/>')
    px, py = 322, gy2 + 40
    s.append(f'<circle cx="{px}" cy="{py}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 6}" x2="{px}" y2="{py + 34}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px - 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px + 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(arrow(px - 10, gy2 + 82, 274, gy2 + 82, GREEN, 0.9, "5 3", "arrL"))
    s.append(txt(150, gy2 + 76, "一路轻过：冰面不留痕", 4.1, GREEN))
    s.append(txt(190, gy2 + 166, "犹兮若畏四邻：畏不是怕，是不肯把路走成别人的路", 4.3, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "豫与犹，都是「先看后动」：先探实虚，再定脚步；不是迟疑，是不莽撞。", 5.0, INK))
    s.append(txt(24, a + 16, "冰薄，脚重；心一急，先碎的是脚下的路，摔的是自己。", 5.0, INK))
    s.append(txt(24, a + 34, "善为道者，走路像过冬河：每一步都自带敬意。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "豫兮若冬涉川，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "犹兮若畏四邻。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch15b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch15c_bu_yu_ying():
    body, y = head(380, 999, "夫唯不盈，故能蔽而新成：旧罐不满，反而常新",
                   "第 十 五 章 · 不 欲 盈", "旧罐", "夫唯不盈，故能蔽而新成。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "盈不是「多」，是「没有再往里的余地」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "不盈：留一处空，器物才换得动、久得住。", 4.8, "#6E6459", "middle"))

    def jar(cx, top, w, h, fill, crack=False, muddy=False):
        body_cy = top + 26 + (h - 26) / 2
        s.append(f'<ellipse cx="{cx}" cy="{body_cy}" rx="{w}" ry="{(h - 26) / 2}" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<rect x="{cx - w * 0.58}" y="{top}" width="{w * 1.16}" height="28" fill="{fill}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w * 0.58}" ry="4" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<path d="M{cx - w},{body_cy + (h - 26) / 2} a{w},9 0 0 0 {w * 2},0" fill="none" stroke="{INK}" stroke-width="0.0"/>')
        if crack:
            s.append(f'<path d="M{cx + 6},{top + 30} l5,12 l-4,9 l6,10" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
        if muddy:
            s.append(f'<circle cx="{cx - 9}" cy="{top + 40}" r="1.6" fill="#C9B79A"/>')
            s.append(f'<circle cx="{cx + 7}" cy="{top + 54}" r="1.4" fill="#C9B79A"/>')

    # 一、新罐盛满
    s.append(txt(24, y + 52, "一、新罐盛满：一次就要盛到头，罐口溢、罐身裂", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="172" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx = 110
    jar(cx, gy + 54, 30, 74, PAPER, crack=True)
    # 水溢
    s.append(f'<path d="M{cx - 16},{gy + 58} q-5,8 -8,13 M{cx + 16},{gy + 58} q5,8 8,13" fill="none" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{cx - 26}" cy="{gy + 74}" r="1.6" fill="{GREEN}"/>')
    s.append(f'<circle cx="{cx + 26}" cy="{gy + 74}" r="1.6" fill="{GREEN}"/>')
    s.append(txt(cx, gy + 150, "满到没处可加：脆", 4.2, SEAL, "middle"))
    s.append(txt(258, gy + 92, "新的、满的、不碰就裂的", 4.2, SEAL, "middle"))
    s.append(txt(258, gy + 112, "盈则无余地：换不动，也久不住", 4.1, "#6E6459", "middle"))

    # 二、旧罐七分
    s.append(txt(24, gy + 190, "二、旧罐七分：斑驳却完好，留三口空在里头", 5.2, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    jar(cx, gy2 + 50, 27, 70, "#EFE6D4", muddy=True)
    # 内壁水位线
    s.append(f'<line x1="{cx - 24}" y1="{gy2 + 84}" x2="{cx + 24}" y2="{gy2 + 84}" stroke="{GREEN}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(txt(cx + 30, gy2 + 84, "只到七分：留三口空", 4.0, GREEN))
    s.append(txt(cx, gy2 + 148, "旧而不坏：蔽而新成", 4.2, GREEN, "middle"))
    s.append(txt(262, gy2 + 90, "旧了、不满、还在用", 4.2, GREEN, "middle"))
    s.append(txt(262, gy2 + 110, "留白处换得动气，故常新", 4.1, "#6E6459", "middle"))

    a = gy2 + 188
    s.append(txt(24, a, "「蔽」是旧、是覆着的那层旧相；「新成」是它仍能成事。留一处不满，旧物就还在生长。", 4.9, INK))
    s.append(txt(24, a + 16, "人不肯留空，是怕不够；越怕不够，越先裂。", 4.9, INK))
    s.append(txt(24, a + 34, "不欲盈：不是不要，是不肯盛到没有余地的那一步。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "夫唯不盈，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "故能蔽而新成。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch15c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch16b_yi_gang_shui():
    body, y = head(380, 999, "归根曰静：水一动就浑，一静就清",
                   "第 十 六 章 · 守 静", "一缸浊水", "致虚极，守静笃；万物并作，吾以观复。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "虚不是空掉，是把搅动的那只手先放下。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "静不是不动，是不再自己去搅。", 4.8, "#6E6459", "middle"))

    def vat(cx, top, w, h, water, murk=0):
        s.append(f'<path d="M{cx - w},{top} L{cx - w * 0.68},{top + h} q{w * 0.68},{6} {w * 1.36},0 L{cx + w},{top} z" fill="{water}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w}" ry="5" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w - 3}" ry="3.6" fill="{water}" stroke="none"/>')
        span = w * 1.2
        if murk:
            for k in range(14):
                s.append(f'<circle cx="{cx - w * 0.6 + (k * 29) % int(span)}" cy="{top + 12 + (k * 15) % int(h - 20)}" r="1.5" fill="#B7ADA0"/>')
        else:
            for k in range(9):
                s.append(f'<circle cx="{cx - w * 0.55 + (k * 27) % int(span)}" cy="{top + h - 10 - (k % 2) * 3}" r="1.5" fill="#A8A091"/>')

    # 一、搅：浑
    s.append(txt(24, y + 52, "一、搅：手一搅，沙全浮起来，水就浑了", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="172" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx = 132
    vat(cx, gy + 46, 40, 74, "#D9D3C6", murk=1)
    # 搅棒与回旋
    s.append(f'<line x1="{cx}" y1="{gy + 20}" x2="{cx + 8}" y2="{gy + 74}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M{cx - 34},{gy + 58} q34,26 68,0" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M{cx + 34},{gy + 66} q-34,26 -68,0" fill="none" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(txt(cx, gy + 152, "搅动：沙起，水浊，看不见底", 4.2, SEAL, "middle"))
    s.append(txt(266, gy + 90, "不知常，妄作凶", 4.5, SEAL, "middle"))
    s.append(txt(266, gy + 108, "越搅越浑，越急越看不见", 4.1, "#6E6459", "middle"))

    # 二、静：清
    s.append(txt(24, gy + 190, "二、静：手放下，沙自己沉，水自己清", 5.2, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    vat(cx, gy2 + 40, 40, 74, "#DCEAE2", murk=0)
    # 沉沙层
    s.append(f'<path d="M{cx - 26},{gy2 + 106} q26,8 52,0" fill="none" stroke="#A8A091" stroke-width="1.2"/>')
    s.append(txt(cx + 54, gy2 + 108, "沙沉到底：根在这里", 4.0, GREEN))
    s.append(f'<line x1="{cx - 44}" y1="{gy2 + 66}" x2="{cx + 44}" y2="{gy2 + 66}" stroke="{GREEN}" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(txt(cx + 54, gy2 + 68, "水自清：上面那层不用管", 4.0, GREEN))
    s.append(txt(cx, gy2 + 150, "静曰复命：浑是暂时的，清是本来的", 4.2, GREEN, "middle"))

    a = gy2 + 188
    s.append(txt(24, a, "万物并作，吾以观复：不去推动，只看着它自己回去。", 5.0, INK))
    s.append(txt(24, a + 16, "归根曰静——静不是把人按住，是把那只搅动的手放下。", 5.0, INK))
    s.append(txt(24, a + 34, "知常曰明：知道它会自己清，就不必急着去搅。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "归根曰静，静曰复命；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "知常曰明，不知常妄作凶。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch16b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch16c_luo_ye_gui_gen():
    body, y = head(380, 999, "万物并作，吾以观复：长出去，都要落回来",
                   "第 十 六 章 · 归 根", "落叶归根", "万物并作，吾以观复；夫物芸芸，各复归其根。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「复」不是回到原样，是回到那个能再长出来的地方。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "看的是循环，不是终点。", 4.8, "#6E6459"))

    def ground(gy):
        s.append(f'<line x1="26" y1="{gy + 138}" x2="354" y2="{gy + 138}" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<rect x="26" y="{gy + 138}" width="328" height="12" fill="#EFE9DA" stroke="none"/>')

    def root(cx, gy):
        s.append(f'<line x1="{cx}" y1="{gy + 138}" x2="{cx}" y2="{gy + 96}" stroke="{INK}" stroke-width="2.0"/>')
        s.append(f'<path d="M{cx},{gy + 138} q-14,10 -22,12 M{cx},{gy + 138} q14,10 22,12 M{cx},{gy + 138} l0,14" fill="none" stroke="{INK}" stroke-width="1.0"/>')

    # 一、并作
    s.append(txt(24, y + 52, "一、并作：一时齐发，各往各的方向长", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="160" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ground(gy)
    cx = 150
    root(cx, gy)
    for k, (dx, up, lab) in enumerate([(-44, 34, "枝"), (-20, 52, "花"), (6, 66, "实"), (30, 44, "叶"), (52, 26, "")]):
        x2, y2 = cx + dx, gy + 96 - up
        s.append(f'<line x1="{cx}" y1="{gy + 96}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<ellipse cx="{x2}" cy="{y2 - 3}" rx="4.4" ry="6.4" fill="#E4EAE0" stroke="{GREEN}" stroke-width="0.6"/>')
        if lab:
            s.append(txt(x2, y2 - 14, lab, 3.9, GREEN, "middle"))
        s.append(arrow(x2, y2 - 12, x2 + (6 if dx > 0 else -6), y2 - 26, GREEN, 0.7, None, "arr2"))

    # 二、复归
    s.append(txt(24, gy + 176, "二、观复：看久了，叶子还是要落回脚下", 5.2, GREEN))
    gy2 = gy + 188
    s.append(f'<rect x="26" y="{gy2}" width="328" height="160" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ground(gy2)
    root(cx, gy2)
    s.append(f'<line x1="{cx}" y1="{gy2 + 96}" x2="{cx}" y2="{gy2 + 50}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="{cx}" y1="{gy2 + 74}" x2="{cx - 18}" y2="{gy2 + 62}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx}" y1="{gy2 + 66}" x2="{cx + 20}" y2="{gy2 + 56}" stroke="{INK}" stroke-width="0.9"/>')
    for dx, hy in [(-46, 122), (-32, 112), (-14, 126), (2, 118), (20, 124), (38, 114)]:
        lx = cx + dx
        s.append(f'<ellipse cx="{lx}" cy="{gy2 + hy + 8}" rx="4.2" ry="2.4" fill="#E4EAE0" stroke="{GREEN}" stroke-width="0.6"/>')
        s.append(arrow(lx, gy2 + hy - 8, lx, gy2 + hy + 3, GREEN, 0.7, None, "arr2"))
    s.append(txt(cx + 56, gy2 + 74, "各自落回脚下", 4.0, GREEN))

    a = gy2 + 180
    s.append(txt(24, a, "生发是「作」，回收是「复」；只看见作，看不见复，人就以为一直往前是对的。", 4.9, INK))
    s.append(txt(24, a + 16, "复归其根，不是退步，是把今年长出来的、重新变成明年的底。", 4.9, INK))
    s.append(txt(24, a + 34, "观复的人不急：他知道每一轮落下来的，都在根那里等着。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "万物并作，吾以观复；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "夫物芸芸，各复归其根。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch16c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch17b_si_shan_men():
    body, y = head(380, 999, "太上，下知有之：最好的管法，是让人几乎忘了你在",
                   "第 十 七 章 · 四 扇 门", "四扇门", "太上，下知有之；其次亲而誉之；其次畏之；其次侮之。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "四级不是四种人，是同一件事的四个火候：越用力，越往下走。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "信不足焉，有不信焉：话多了，信就薄了。", 4.8, "#6E6459"))

    def door(x, gy, h=86, w=44):
        s.append(f'<rect x="{x}" y="{gy + 40}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<line x1="{x + w - 10}" y1="{gy + 40 + h / 2}" x2="{x + w - 10}" y2="{gy + 40 + h / 2}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<circle cx="{x + w - 9}" cy="{gy + 40 + h / 2}" r="1.6" fill="{INK}"/>')

    # 一、四扇门
    s.append(txt(24, y + 52, "一、四扇门：从「知有」到「侮之」，痕迹一路加重", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="186" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    xs = [38, 116, 194, 272]
    labels = [("太上", "下知有之"), ("其次", "亲而誉之"), ("其次", "畏之"), ("其次", "侮之")]
    for i, x in enumerate(xs):
        door(x, gy, 82, 42)
        s.append(txt(x + 21, gy + 136, labels[i][0], 3.9, "#8A7C69", "middle"))
        s.append(txt(x + 21, gy + 148, labels[i][1], 4.1, INK, "middle"))
    # 门槛前的痕迹：依次加重
    s.append(f'<ellipse cx="59" cy="{gy + 128}" rx="7" ry="2.4" fill="#DCD2BF" stroke="none"/>')
    # 亲誉：门楣上挂匾
    s.append(f'<rect x="112" y="{gy + 26}" width="50" height="12" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(137, gy + 35, "誉", 4.2, INK, "middle"))
    # 畏：门上插一柄刀
    s.append(f'<line x1="215" y1="{gy + 92}" x2="215" y2="{gy + 126}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M211,{gy + 92} l4,-10 l4,10 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.8"/>')
    # 侮：门上一串涂痕
    for k in range(3):
        s.append(f'<path d="M{290 + k * 8},{gy + 124} l4,6 l-4,6" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(txt(190, gy + 172, "同一件事的四个火候：越插手，越往下掉", 4.3, SEAL, "middle"))

    # 二、贵言
    s.append(txt(24, gy + 202, "二、贵言：话少的门都开着，话多的门全关上", 5.2, GREEN))
    gy2 = gy + 214
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 左：话多
    s.append(f'<circle cx="70" cy="{gy2 + 54}" r="7" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M64,{gy2 + 54} q6,3 12,0" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="70" y1="{gy2 + 61}" x2="70" y2="{gy2 + 86}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="70" y1="{gy2 + 86}" x2="63" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="70" y1="{gy2 + 86}" x2="77" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.9"/>')
    for k in range(4):
        s.append(f'<circle cx="{84 + k * 9}" cy="{gy2 + 50 - k * 4}" r="1.5" fill="{SEAL}"/>')
    s.append(f'<rect x="112" y="{gy2 + 46}" width="34" height="56" fill="none" stroke="{LINE}" stroke-width="1.0"/>')
    s.append(f'<line x1="112" y1="{gy2 + 60}" x2="146" y2="{gy2 + 74}" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(f'<line x1="146" y1="{gy2 + 60}" x2="112" y2="{gy2 + 74}" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(txt(70, gy2 + 120, "话多：门一道道关上", 4.1, SEAL, "middle"))
    s.append(txt(70, gy2 + 134, "信不足，有不信", 4.1, SEAL, "middle"))
    # 右：话少
    s.append(f'<line x1="190" y1="{gy2 + 30}" x2="190" y2="{gy2 + 148}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="6 5"/>')
    s.append(f'<circle cx="238" cy="{gy2 + 54}" r="7" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="238" y1="{gy2 + 61}" x2="238" y2="{gy2 + 86}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="238" y1="{gy2 + 86}" x2="231" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="238" y1="{gy2 + 86}" x2="245" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="286" y="{gy2 + 46}" width="34" height="56" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M286,{gy2 + 46} L302,{gy2 + 52} L302,{gy2 + 96} L286,{gy2 + 102}" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<circle cx="317" cy="{gy2 + 74}" r="1.6" fill="{INK}"/>')
    s.append(txt(238, gy2 + 120, "话少：门开着，人自己走", 4.1, GREEN, "middle"))
    s.append(txt(238, gy2 + 134, "悠兮其贵言", 4.1, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "太上不是最高明的手腕，是最少的手：下知有之——百姓只知道有这么一个人，日子是自己的。", 4.8, INK))
    s.append(txt(24, a + 16, "亲而誉之，已经有恩情在；畏之，已经有刀在；侮之，连刀都不管用了。", 4.8, INK))
    s.append(txt(24, a + 34, "贵言：不是不说，是不拿话去替代事。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "太上，下知有之；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "悠兮其贵言。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch17b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch17c_gong_cheng():
    body, y = head(380, 999, "功成事遂，百姓皆谓我自然",
                   "第 十 七 章 · 功 成", "功成之后", "功成事遂，百姓皆谓我自然。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "最难的不是把事做成，是做成之后站在哪儿。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "站在中间，事就成了他的；退到边上，事才是大家的。", 4.8, "#6E6459"))

    def field(gy, h=110):
        s.append(f'<rect x="26" y="{gy + 96}" width="328" height="{h}" fill="#EFE9DA" stroke="none"/>')
        s.append(f'<line x1="26" y1="{gy + 96}" x2="354" y2="{gy + 96}" stroke="{INK}" stroke-width="1.0"/>')
        for k in range(7):
            x = 52 + k * 44
            s.append(f'<line x1="{x}" y1="{gy + 96}" x2="{x}" y2="{gy + 80}" stroke="{GREEN}" stroke-width="0.9"/>')
            s.append(f'<path d="M{x},{gy + 82} l-5,-6 M{x},{gy + 82} l5,-6 M{x},{gy + 88} l-5,-5 M{x},{gy + 88} l5,-5" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')

    # 一、站在中间
    s.append(txt(24, y + 52, "一、站在中间：旗子一举，功都算在他头上", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    field(gy, 58)
    px, py = 190, gy + 40
    s.append(f'<circle cx="{px}" cy="{py}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 6}" x2="{px}" y2="{py + 34}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px - 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 34}" x2="{px + 7}" y2="{py + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px + 4}" y1="{py + 14}" x2="{px + 26}" y2="{py - 6}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<path d="M{px + 26},{py - 6} l12,4 l-12,10 z" fill="{SEAL}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(txt(190, gy + 146, "众人围着他：这是他做成的", 4.2, SEAL, "middle"))

    # 二、退到边上
    s.append(txt(24, gy + 192, "二、退到边上：事还是成了，只是没人记得谁做的", 5.2, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    field(gy2, 76)
    # 退到树下的那个人
    tx, ty = 322, gy2 + 42
    s.append(f'<line x1="{tx}" y1="{gy2 + 96}" x2="{tx}" y2="{gy2 + 54}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M{tx},{gy2 + 54} q-16,-8 -22,2 M{tx},{gy2 + 54} q16,-8 22,2 M{tx},{gy2 + 58} q-12,-4 -18,4 M{tx},{gy2 + 58} q12,-4 18,4" fill="none" stroke="{GREEN}" stroke-width="0.9"/>')
    px2, py2 = 296, gy2 + 52
    s.append(f'<circle cx="{px2}" cy="{py2}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px2}" y1="{py2 + 6}" x2="{px2}" y2="{py2 + 34}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="{px2}" y1="{py2 + 34}" x2="{px2 - 7}" y2="{py2 + 46}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px2}" y1="{py2 + 34}" x2="{px2 + 7}" y2="{py2 + 46}" stroke="{INK}" stroke-width="1.0"/>')
    # 田中之人抬头
    for k, x in enumerate([96, 168, 240]):
        s.append(f'<circle cx="{x}" cy="{gy2 + 60}" r="4.4" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy2 + 64}" x2="{x}" y2="{gy2 + 86}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(96, gy2 + 112, "我自然", 4.3, GREEN))
    s.append(txt(168, gy2 + 134, "没人记得谁做成的，事却成了", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 160, "功成事遂，百姓皆谓我自然", 4.4, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "举旗的人，把众人的力气记成自己的功劳；退到树下的人，把功劳还给做事的人。", 4.9, INK))
    s.append(txt(24, a + 16, "「我自然」不是百姓不知情，是他们不必知道——这正是太上该有的样子。", 4.9, INK))
    s.append(txt(24, a + 34, "功成之后最难的一步：从中间退到边上，让事自己站着。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "功成事遂，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "百姓皆谓我自然。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch17c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch18b_yi_kuai_bu():
    body, y = head(380, 999, "大道废，有仁义：补丁不是坏东西，是布破了才需要它",
                   "第 十 八 章 · 补 丁", "一块补丁", "大道废，有仁义；智慧出，有大伪。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "补丁本身是好的；它出现，说明衣裳已经破了。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "夸补丁的人，往往不肯说布是怎么破的。", 4.8, "#6E6459"))

    def cloth(gy, w=252, h=96, holes=0):
        x0 = (380 - w) / 2
        s.append(f'<rect x="{x0}" y="{gy + 30}" width="{w}" height="{h}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
        for k in range(6):
            s.append(f'<line x1="{x0 + 6}" y1="{gy + 40 + k * 14}" x2="{x0 + w - 6}" y2="{gy + 40 + k * 14}" stroke="#DCC9A8" stroke-width="0.5"/>')
        return x0

    # 一、一匹完整的布
    s.append(txt(24, y + 52, "一、一匹完整的布：没有人需要被称赞", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cloth(gy, holes=0)
    s.append(txt(190, gy + 146, "大道行：父慈子孝是日常，不必立名", 4.3, SEAL, "middle"))

    # 二、补丁
    s.append(txt(24, gy + 172, "二、布破了，才打上三块补丁", 5.2, GREEN))
    gy2 = gy + 184
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    x0 = cloth(gy2, holes=3)
    patches = [(x0 + 40, gy2 + 46, "仁", 44, 34), (x0 + 118, gy2 + 62, "孝", 40, 30), (x0 + 194, gy2 + 44, "忠", 40, 34)]
    for px, py, lab, w, h in patches:
        tx = px + w / 2
        s.append(f'<path d="M{tx},{py - 8} l5,9 l-6,8 l6,9 l-5,9 l4,10" fill="none" stroke="{SEAL}" stroke-width="1.4"/>')
        s.append(f'<rect x="{px}" y="{py}" width="{w}" height="{h}" fill="#E4EAE0" stroke="{GREEN}" stroke-width="0.9"/>')
        for k in range(4):
            s.append(f'<line x1="{px + 4}" y1="{py + 7 + k * 7}" x2="{px + w - 4}" y2="{py + 7 + k * 7}" stroke="#CBD8CB" stroke-width="0.5"/>')
        s.append(txt(px + w / 2, py + h - 6, lab, 5.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 160, "补得再好，也还是补丁；布上的口子才是真事", 4.3, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "老子不是骂仁义，是提醒：当仁义要被大张旗鼓地表彰，说明它已经不平常了。", 4.8, INK))
    s.append(txt(24, a + 16, "智慧出，有大伪：越是需要机巧，越说明正路走不通了。", 4.8, INK))
    s.append(txt(24, a + 34, "六亲不和才有孝慈，国家昏乱才有忠臣——名号越亮，底子越薄。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "大道废，有仁义；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "智慧出，有大伪。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch18b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch18c_san_kuai_bu_ding():
    body, y = head(380, 999, "孝慈、忠臣、仁义：三块补丁，各补一处破",
                   "第 十 八 章 · 三 处 破", "三处破", "六亲不和，有孝慈；国家昏乱，有忠臣。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "每一块补丁，都对应一个具体的破处；先看破处，再看补丁。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "补丁的名字越响，破口就越深。", 4.8, "#6E6459"))

    rows = [("六亲不和", "孝慈", "一家子冷了，才需要有人出来做孝子"),
            ("国家昏乱", "忠臣", "朝堂乱了，才需要有人出来做忠臣"),
            ("大道废", "仁义", "路走不通了，才需要有人出来讲仁义")]
    for i, (huai, ming, note) in enumerate(rows):
        gy = y + 66 + i * 84
        s.append(txt(24, gy, "破处：%s" % huai, 5.2, SEAL))
        # 布片：左破口，右补丁
        s.append(f'<rect x="30" y="{gy + 12}" width="130" height="56" fill="#EFE6D4" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<path d="M84,{gy + 12} l6,14 l-8,12 l7,16 l-9,14" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
        s.append(arrow(166, gy + 40, 196, gy + 40, GREEN, 0.9, None, "arr2"))
        s.append(f'<rect x="200" y="{gy + 16}" width="66" height="48" fill="#E4EAE0" stroke="{GREEN}" stroke-width="1.0"/>')
        s.append(txt(233, gy + 46, ming, 6.4, GREEN, "middle"))
        s.append(txt(272, gy + 36, "补上", 4.0, "#6E6459"))
        s.append(txt(272, gy + 47, note, 3.8, "#6E6459"))

    a = y + 66 + 3 * 84 + 8
    s.append(txt(24, a, "三处破，三种补：不是三件德目，是同一件事在人情、朝堂、大道上的三次显影。", 4.8, INK))
    s.append(txt(24, a + 16, "补丁可以救命，却不能代替布——把补丁当成布，破处就永远好不了。", 4.8, INK))

    c = a + 40
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "六亲不和，有孝慈；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "国家昏乱，有忠臣。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch18c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch19b_yi_ju_qi_qi():
    body, y = head(380, 999, "刮掉三层漆，才见木头本色",
                   "第 十 九 章 · 漆 与 素", "一具漆器", "见素抱朴，少私寡欲。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "漆不是脏东西；只是漆久了，人就忘了底下是木头。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "绝圣弃智、绝仁弃义、绝巧弃利：刮的是漆，不是木头。", 4.8, "#6E6459"))

    # 一、三层漆
    s.append(txt(24, y + 52, "一、三层漆：一层一层刷上去，越刷越亮，也越厚", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    bx, bw = 70, 130
    layers = [("圣", "智", 20, "#D9C7A8"), ("仁", "义", 18, "#C9B79A"), ("巧", "利", 16, "#B7A184")]
    ty = gy + 40
    s.append(f'<rect x="{bx}" y="{ty + 54}" width="{bw}" height="52" fill="#E8DCC4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(txt(bx + bw / 2, ty + 84, "木", 6.4, INK, "middle"))
    yy = ty + 54
    for a1, a2, hh, col in layers:
        yy -= hh
        s.append(f'<rect x="{bx}" y="{yy}" width="{bw}" height="{hh}" fill="{col}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(txt(bx + 10, yy + hh - 5, a1 + a2, 4.4, INK))
    s.append(txt(bx + bw + 12, ty + 22, "三层漆：光可鉴人", 4.2, SEAL))
    s.append(txt(bx + bw + 12, ty + 36, "漆越厚，越看不见木", 4.1, "#6E6459"))
    s.append(txt(190, gy + 158, "漆是一层层加上去的：加得越多，本色越埋得深", 4.3, SEAL, "middle"))

    # 二、刮漆
    s.append(txt(24, gy + 186, "二、刮漆：刮到木头，才叫见素抱朴", 5.2, GREEN))
    gy2 = gy + 198
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ty2 = gy2 + 40
    s.append(f'<rect x="{bx}" y="{ty2 + 54}" width="{bw}" height="52" fill="#E8DCC4" stroke="{INK}" stroke-width="1.0"/>')
    s.append(txt(bx + bw / 2, ty2 + 84, "素木", 6.0, GREEN, "middle"))
    # 残留半层漆（右侧）
    s.append(f'<rect x="{bx + bw - 34}" y="{ty2 + 34}" width="34" height="20" fill="#C9B79A" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(bx + bw - 17, ty2 + 48, "余漆", 3.9, INK, "middle"))
    # 刮刀
    s.append(f'<path d="M{bx + 6},{ty2 + 20} l54,-6 l0,8 l-54,6 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{bx + 60}" y1="{ty2 + 22}" x2="{bx + 96}" y2="{ty2 + 16}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(arrow(bx + 100, ty2 + 16, bx + bw + 26, ty2 + 16, GREEN, 0.9, None, "arr2"))
    s.append(txt(bx + bw + 30, ty2 + 12, "刮下来的漆", 4.0, GREEN))
    s.append(txt(bx + bw + 12, ty2 + 84, "木在，器还在用", 4.1, GREEN))
    s.append(txt(bx + bw + 12, ty2 + 98, "少一层漆，多一分真", 4.0, "#6E6459"))
    s.append(txt(190, gy2 + 158, "见素：不必再刷；抱朴：木本来就够用", 4.3, GREEN, "middle"))

    a = gy2 + 188
    s.append(txt(24, a, "「绝」「弃」不是焚书毁器，是刮漆：把后来刷上去的那几层剥下来。", 4.9, INK))
    s.append(txt(24, a + 16, "少私寡欲：不是不要，是不再把「多一层」当成本事。", 4.9, INK))
    s.append(txt(24, a + 34, "素不是简陋，是不必再靠外加的东西来证明自己。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "见素抱朴，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "少私寡欲。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch19b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch19c_ban_chu_qu():
    body, y = head(380, 999, "把三样搬到门外，屋里才空得下饭香",
                   "第 十 九 章 · 搬 出 去", "搬出去", "绝圣弃智，民利百倍；绝仁弃义，民复孝慈；绝巧弃利，盗贼无有。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "三句「绝弃」，都是往外搬，不是往里加。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "搬空了，人自己会坐下来吃饭。", 4.8, "#6E6459"))

    def room(gy, h=118):
        s.append(f'<path d="M40,{gy + 24} L40,{gy + 24 + h} L340,{gy + 24 + h} L340,{gy + 24} L300,{gy + 12} L80,{gy + 10} z" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.9"/>')
        s.append(f'<line x1="40" y1="{gy + 24 + h}" x2="340" y2="{gy + 24 + h}" stroke="{INK}" stroke-width="1.0"/>')

    # 一、屋里堆着
    s.append(txt(24, y + 52, "一、屋里三样：书简、牌位、巧器，堆在正中", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="182" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    room(gy, 118)
    s.append(f'<rect x="140" y="{gy + 96}" width="46" height="30" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="140" y1="{gy + 106}" x2="186" y2="{gy + 106}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(163, gy + 120, "简", 4.0, INK, "middle"))
    s.append(f'<rect x="196" y="{gy + 84}" width="26" height="42" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(209, gy + 110, "牌", 4.0, INK, "middle"))
    s.append(f'<circle cx="238" cy="{gy + 112}" r="9" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="238" y1="{gy + 106}" x2="238" y2="{gy + 118}" stroke="{INK}" stroke-width="0.6"/>')
    s.append(txt(238, gy + 132, "巧器", 3.9, INK, "middle"))
    s.append(txt(190, gy + 172, "屋里满满当当，人却没地方坐", 4.3, SEAL, "middle"))

    # 二、搬出去
    s.append(txt(24, gy + 200, "二、搬到门外：屋里只剩一张素几、一只碗", 5.2, GREEN))
    gy2 = gy + 212
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    room(gy2, 118)
    s.append(f'<rect x="130" y="{gy2 + 106}" width="80" height="8" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="140" y1="{gy2 + 114}" x2="140" y2="{gy2 + 132}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="200" y1="{gy2 + 114}" x2="200" y2="{gy2 + 132}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<ellipse cx="222" cy="{gy2 + 104}" rx="9" ry="3.4" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M213,{gy2 + 104} q9,12 18,0" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(145, gy2 + 96, "素几", 3.9, GREEN))
    s.append(txt(244, gy2 + 108, "一碗饭", 3.9, GREEN))
    # 门外的三样
    s.append(f'<rect x="236" y="{gy2 + 148}" width="46" height="16" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(259, gy2 + 159, "简·牌·器", 3.4, "#6E6459", "middle"))
    s.append(arrow(196, gy2 + 156, 230, gy2 + 156, GREEN, 0.8, None, "arr2"))
    s.append(txt(196, gy2 + 170, "搬出门外", 4.0, GREEN))

    a = gy2 + 196
    s.append(txt(24, a, "搬出去不是为了苦修，是为了腾出地方：地方一空，人就坐得下、吃得香。", 4.9, INK))
    s.append(txt(24, a + 16, "民利百倍、民复孝慈、盗贼无有——不是靠加法，是靠把多余的那几层搬走。", 4.9, INK))
    s.append(txt(24, a + 34, "绝弃是减法：减到够用，事就成了。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "绝圣弃智，民利百倍；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "绝巧弃利，盗贼无有。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch19c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
def ch20b_shi_ji_yu_jiao_luo():
    body, y = head(380, 999, "众人熙熙，我独泊兮：不是不合群，是不必挤进去",
                   "第 二 十 章 · 两 种 站 法", "市集与角落", "众人熙熙，如享太牢，如春登台；我独泊兮其未兆。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "同一套标准之前，有两种站法：一种是挤进去，一种是站在外头看。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "「泊」不是冷，是停在没起念的那一处。", 4.8, "#6E6459"))

    # 一、市集
    s.append(txt(24, y + 52, "一、熙熙：众人举杯、争先，谁也不肯落后", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="172" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<rect x="54" y="{gy + 100}" width="272" height="9" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="70" y1="{gy + 109}" x2="70" y2="{gy + 128}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="310" y1="{gy + 109}" x2="310" y2="{gy + 128}" stroke="{INK}" stroke-width="0.8"/>')
    for k in range(6):
        x = 82 + k * 42
        s.append(f'<ellipse cx="{x}" cy="{gy + 98}" rx="8" ry="3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<path d="M{x - 8},{gy + 98} q8,10 16,0" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    for x in [70, 118, 166, 226, 292]:
        s.append(f'<circle cx="{x}" cy="{gy + 54}" r="5" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy + 59}" x2="{x}" y2="{gy + 82}" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<line x1="{x}" y1="{gy + 82}" x2="{x - 6}" y2="{gy + 94}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy + 82}" x2="{x + 6}" y2="{gy + 94}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy + 64}" x2="{x + 15}" y2="{gy + 58}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<path d="M{x + 15},{gy + 52.6} L{x + 23},{gy + 52.6} L{x + 21.4},{gy + 59.4} L{x + 16.6},{gy + 59.4} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.7"/>')
    s.append(txt(190, gy + 162, "如享太牢，如春登台：人人都在席上", 4.3, SEAL, "middle"))

    # 二、角落
    s.append(txt(24, gy + 190, "二、独泊：同席之外，一个人停在没起念处", 5.2, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="172" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    for x in [64, 104, 144, 184]:
        s.append(f'<circle cx="{x}" cy="{gy2 + 62}" r="3.4" fill="none" stroke="{LINE}" stroke-width="0.7"/>')
        s.append(f'<line x1="{x}" y1="{gy2 + 65}" x2="{x}" y2="{gy2 + 88}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<rect x="50" y="{gy2 + 100}" width="152" height="6" fill="#F1EADA" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(126, gy2 + 124, "远处的席，与自己无关了", 3.9, "#8A7C69", "middle"))
    px, py = 258, gy2 + 56
    s.append(f'<circle cx="{px}" cy="{py}" r="5.4" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 6}" x2="{px}" y2="{py + 30}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{px}" y1="{py + 30}" x2="{px - 9}" y2="{py + 38}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px - 9}" y1="{py + 38}" x2="{px + 6}" y2="{py + 40}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 30}" x2="{px + 10}" y2="{py + 38}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px + 10}" y1="{py + 38}" x2="{px + 20}" y2="{py + 40}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 12}" x2="{px - 12}" y2="{py + 24}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px}" y1="{py + 12}" x2="{px + 12}" y2="{py + 24}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px - 34}" y1="{py + 42}" x2="{px + 34}" y2="{py + 42}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M{px - 26},{py + 42} q10,-5 20,0 M{px - 6},{py + 42} q10,-5 20,0" fill="none" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(txt(px, gy2 + 154, "泊兮其未兆：水面未起波，念还未动", 4.2, GREEN, "middle"))

    a = gy2 + 190
    s.append(txt(24, a, "「熙熙」不是错，只是热闹有个尽头：散席之后，还是各自回家。", 4.9, INK))
    s.append(txt(24, a + 16, "「独泊」也不是清高：是知道自己在哪一处不必挤，就不挤了。", 4.9, INK))
    s.append(txt(24, a + 34, "未兆：念头还没有起，就先把脚收住。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "众人熙熙，如享太牢；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "我独泊兮其未兆。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch20b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch20c_kong_dai():
    body, y = head(380, 999, "众人皆有余，而我独若遗",
                   "第 二 十 章 · 有 余 与 若 遗", "一只空袋", "众人皆有余，而我独若遗。我愚人之心也哉！", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「有余」是袋里装满，「若遗」是袋空着。", 4.9, INK, "middle"))
    s.append(txt(190, y + 27, "不是没有，是不必什么都带着。", 4.8, "#6E6459"))

    def man(x, gy, bag=None):
        s.append(f'<circle cx="{x}" cy="{gy + 30}" r="6" fill="none" stroke="{INK}" stroke-width="1.0"/>')
        s.append(f'<line x1="{x}" y1="{gy + 36}" x2="{x}" y2="{gy + 64}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<line x1="{x}" y1="{gy + 64}" x2="{x - 7}" y2="{gy + 78}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy + 64}" x2="{x + 7}" y2="{gy + 78}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{x}" y1="{gy + 44}" x2="{x - 14}" y2="{gy + 56}" stroke="{INK}" stroke-width="0.9"/>')
        if bag == "full":
            s.append(f'<path d="M{x + 6},{gy + 42} q16,2 13,18 q-2,11 -13,9 z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
            for k in range(3):
                s.append(f'<circle cx="{x + 10 + k * 3}" cy="{gy + 56}" r="1.6" fill="#C9B79A"/>')
        elif bag == "empty":
            s.append(f'<path d="M{x + 4},{gy + 46} q16,2 14,18 q-2,12 -14,10 z" fill="none" stroke="{INK}" stroke-width="0.9" stroke-dasharray="3 2"/>')
            s.append(f'<line x1="{x + 26}" y1="{gy + 44}" x2="{x + 40}" y2="{gy + 56}" stroke="{GREEN}" stroke-width="0.8"/>')

    # 一、皆有余
    s.append(txt(24, y + 52, "一、皆有余：人人挎一只鼓囊，走一步都带着全部家当", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="120" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    for x in [80, 152, 224, 296]:
        man(x, gy, "full")
    s.append(f'<line x1="46" y1="{gy + 80}" x2="336" y2="{gy + 80}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(190, gy + 104, "袋满，肩沉：没有人是空手来的", 4.2, SEAL, "middle"))

    # 二、独若遗
    s.append(txt(24, gy + 142, "二、独若遗：一只空袋，风穿得过去", 5.2, GREEN))
    gy2 = gy + 154
    s.append(f'<rect x="26" y="{gy2}" width="328" height="124" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    man(160, gy2, None)
    s.append(f'<path d="M182,{gy2 + 34} q-8,26 2,44 q10,4 22,-2 q10,-20 2,-42 z" fill="none" stroke="{INK}" stroke-width="0.9" stroke-dasharray="4 2.5"/>')
    s.append(f'<path d="M184,{gy2 + 36} q10,-4 20,0" fill="none" stroke="{LINE}" stroke-width="0.7"/>')
    for k in range(3):
        yy = gy2 + 50 + k * 8
        s.append(f'<line x1="206" y1="{yy}" x2="246" y2="{yy}" stroke="{GREEN}" stroke-width="0.6"/>')
        s.append(f'<line x1="206" y1="{yy}" x2="246" y2="{yy}" stroke="none"/>')
    s.append(arrow(212, gy2 + 74, 252, gy2 + 74, GREEN, 0.7, None, "arr2"))
    s.append(txt(254, gy2 + 50, "风穿过去，什么都不留在里面", 4.0, GREEN))
    s.append(txt(196, gy2 + 100, "空袋", 4.1, INK, "middle"))
    s.append(f'<line x1="60" y1="{gy2 + 80}" x2="320" y2="{gy2 + 80}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(150, gy2 + 100, "袋空，肩轻", 4.2, GREEN, "middle"))
    s.append(txt(160, gy2 + 116, "留下的地方，装得下别的事；我愚人之心也哉，沌沌兮", 4.1, "#6E6459", "middle"))

    a = gy2 + 146
    s.append(txt(24, a, "「有余」的人，走着走着就被自己的家当拖住；「若遗」的人，反倒走得远。", 4.9, INK))
    s.append(txt(24, a + 16, "沌沌不是糊涂，是不把每件事都先算成得失。", 4.9, INK))
    s.append(txt(24, a + 34, "空着的那只袋，看上去是缺，其实是余地。", 4.9, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "众人皆有余，而我独若遗；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "我愚人之心也哉！", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch20c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch21b_kong_de_zhi_rong():
    body, y = head(380, 999, "孔德之容，惟道是从：德不占地方，道才进得来",
                   "第 二 十 一 章 · 一 枚 带 孔 的 璧", "一枚带孔的璧", "孔，大也、空也、通也：三读各异，落处是一处。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「孔」有三读：河上公读「大」，王弼读「空」，《说文》本义是「通」。", 4.8, INK, "middle"))
    s.append(txt(190, y + 27, "三个读法落在一件东西上：一枚中间穿孔的玉璧。", 4.8, "#6E6459"))

    # 一、璧
    s.append(txt(24, y + 52, "一、璧：环体是「大」，孔里是「空」，孔穿过去是「通」", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 150, gy + 88
    s.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="#F6EEE0" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{LINE2}" stroke-width="0.6"/>')
    for k in range(24):
        import math as _m
        a = k * 15 * _m.pi / 180
        s.append(f'<circle cx="{cx + 34 * _m.cos(a):.1f}" cy="{cy + 34 * _m.sin(a):.1f}" r="1.6" fill="#C9B79A"/>')
    s.append(txt(252, gy + 40, "环体宽厚：大", 4.3, SEAL))
    s.append(txt(252, gy + 56, "孔里虚着：空", 4.3, GREEN))
    s.append(txt(252, gy + 72, "孔能穿过：通", 4.3, INK))
    s.append(f'<line x1="262" y1="{gy + 44}" x2="{cx + 20}" y2="{cy - 6}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(f'<line x1="262" y1="{gy + 60}" x2="{cx + 18}" y2="{cy + 2}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(f'<line x1="262" y1="{gy + 76}" x2="{cx + 22}" y2="{cy + 12}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(150, gy + 168, "三句话说的是同一件事：德之所以能容，正因它不占地方", 4.2, SEAL, "middle"))

    # 二、杯
    s.append(txt(24, gy + 194, "二、一只杯：壁若自己占满了，水就进不来", 5.2, GREEN))
    gy2 = gy + 206
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')

    def cup(x, solid):
        top, bot, w = gy2 + 34, gy2 + 96, 30
        s.append(f'<path d="M{x - w},{top} L{x - w + 8},{bot} L{x + w - 8},{bot} L{x + w},{top}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        if solid:
            s.append(f'<path d="M{x - w + 2},{top + 2} L{x - w + 6},{bot - 3} L{x + w - 6},{bot - 3} L{x + w - 2},{top + 2}" fill="#D9CBAA" stroke="none"/>')
            s.append(txt(x, top + 30, "德占满", 4.2, INK, "middle"))
        else:
            s.append(f'<path d="M{x - w + 2},{top + 2} L{x - w + 6},{bot - 3} L{x + w - 6},{bot - 3} L{x + w - 2},{top + 2}" fill="#E4EFE4" stroke="none"/>')
            s.append(f'<line x1="{x - w + 3}" y1="{top + 10}" x2="{x + w - 3}" y2="{top + 10}" stroke="{GREEN}" stroke-width="0.7"/>')
        s.append(f'<ellipse cx="{x}" cy="{top}" rx="{w}" ry="5" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')

    cup(120, True)
    cup(258, False)
    for k in range(3):
        s.append(f'<line x1="{108 + k * 12}" y1="{gy2 + 8}" x2="{108 + k * 12}" y2="{gy2 + 24}" stroke="#8A7C69" stroke-width="0.7" stroke-dasharray="3 2"/>')
    s.append(f'<path d="M100,{gy2 + 6} q8,-8 16,0 M132,{gy2 + 6} q8,-8 16,0" fill="none" stroke="#8A7C69" stroke-width="0.6"/>')
    s.append(txt(120, gy2 + 118, "水在口上打住", 4.1, "#8A7C69", "middle"))
    for k in range(3):
        s.append(f'<line x1="{246 + k * 12}" y1="{gy2 + 8}" x2="{246 + k * 12}" y2="{gy2 + 26}" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(258, gy2 + 118, "水一直进得去", 4.1, GREEN, "middle"))
    s.append(txt(190, gy2 + 140, "空不是没有，是留出可以进的那处", 4.2, INK, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "「孔德之容」：不是先修出一份德、再去从道；是德的一切呈现，本来就只从道出。", 4.8, INK))
    s.append(txt(24, a + 16, "「容」是描摹，不是定义——第十五章「强为之容」也是描摹。", 4.8, INK))
    s.append(txt(24, a + 34, "德若自己占满了，道就进不来。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "孔德之容，惟道是从。", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "德之所以能容，正因它不占地方。", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch21b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch21c_men_nei_dian_shu():
    body, y = head(380, 999, "以阅众甫：在门内把万物的开端一一点过",
                   "第 二 十 一 章 · 门 内 点 数", "门内点数", "阅，具数于门中也。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「名」是指向实相的符号，不是实相；符号留得住，地方留不住。", 4.8, INK, "middle"))
    s.append(txt(190, y + 27, "「阅」是门里逐个点数——比空说的「观照」具体得多。", 4.8, "#6E6459"))

    # 一、路标
    s.append(txt(24, y + 52, "一、路标：名不去，是路标一直在；路标不是那个地方", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="164" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M40,{gy + 132} q60,-6 120,4 q60,10 120,2 q40,-5 52,0" fill="none" stroke="{LINE2}" stroke-width="1.0"/>')
    s.append(f'<line x1="120" y1="{gy + 128}" x2="120" y2="{gy + 62}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M92,{gy + 40} L150,{gy + 40} L166,{gy + 54} L150,{gy + 68} L92,{gy + 68} Z" fill="#F2EADA" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(122, gy + 56, "道", 5.6, SEAL, "middle"))
    s.append(f'<line x1="170" y1="{gy + 54}" x2="196" y2="{gy + 54}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="4 2"/>')
    s.append(arrow(198, gy + 54, 222, gy + 54, SEAL, 0.9, None, "arr2"))
    s.append(txt(224, gy + 48, "所指：那边", 4.1, SEAL))
    for k, (rx, ry, op) in enumerate([(48, 26, 0.5), (38, 20, 0.6), (28, 14, 0.7)]):
        s.append(f'<ellipse cx="288" cy="{gy + 70}" rx="{rx}" ry="{ry}" fill="#F3EBDD" opacity="{op}" stroke="none"/>')
    for yy in [gy + 60, gy + 70, gy + 80]:
        s.append(f'<path d="M262,{yy} q13,-4 26,0 q13,4 26,0" fill="none" stroke="#DCCFBB" stroke-width="0.6"/>')
    s.append(txt(286, gy + 108, "那处本身，看不见也说不全", 3.9, "#8A7C69", "middle"))
    s.append(txt(127, gy + 148, "路标写着名，不等于名就是那处", 4.1, "#8A7C69", "middle"))
    # 二、门内点数
    s.append(txt(24, gy + 182, "二、门内点数：一器一器点过，点名的是开端，不是器物", 5.2, GREEN))
    gy2 = gy + 194
    s.append(f'<rect x="26" y="{gy2}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="70" y1="{gy2 + 26}" x2="70" y2="{gy2 + 150}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="310" y1="{gy2 + 26}" x2="310" y2="{gy2 + 150}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="70" y1="{gy2 + 26}" x2="310" y2="{gy2 + 26}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="70" y1="{gy2 + 150}" x2="310" y2="{gy2 + 150}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="140" y="{gy2 + 16}" width="100" height="14" fill="#F2EADA" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(txt(190, gy2 + 26, "道", 4.4, SEAL, "middle"))
    s.append(txt(252, gy2 + 12, "名不去：路标一直在", 3.9, "#8A7C69"))
    for k, w in enumerate([16, 22, 14, 18, 12]):
        x = 92 + k * 44
        s.append(f'<line x1="{x}" y1="{gy2 + 150}" x2="{x}" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1.0"/>')
        if k % 2 == 0:
            s.append(f'<path d="M{x - w / 2},{gy2 + 116} q{w / 2},-14 {w},0 q-{w / 2},6 -{w},0" fill="none" stroke="{INK}" stroke-width="1.0"/>')
        else:
            s.append(f'<rect x="{x - w / 2}" y="{gy2 + 104}" width="{w}" height="12" fill="none" stroke="{INK}" stroke-width="1.0"/>')
        s.append(txt(x, gy2 + 166, ["一", "二", "三", "四", "五"][k], 3.6, GREEN, "middle"))
    s.append(f'<circle cx="200" cy="{gy2 + 78}" r="5" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="200" y1="{gy2 + 83}" x2="200" y2="{gy2 + 108}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="200" y1="{gy2 + 108}" x2="194" y2="{gy2 + 128}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="200" y1="{gy2 + 108}" x2="206" y2="{gy2 + 128}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="200" y1="{gy2 + 90}" x2="230" y2="{gy2 + 96}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="200" y1="{gy2 + 90}" x2="170" y2="{gy2 + 96}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(236, gy2 + 98, 268, gy2 + 98, GREEN, 0.8, None, "arr2"))
    s.append(txt(190, gy2 + 44, "自今及古，其名不去", 4.0, "#8A7C69", "middle"))

    a = gy2 + 200
    s.append(txt(24, a, "「阅」的本义是在门内逐一点数：不是抽象地观照万物的开端，是把开端一一点过。", 4.8, INK))
    s.append(txt(24, a + 16, "自今及古：从当下回溯上古，这个可以被名为「道」的存在，从来不曾消失。", 4.8, INK))
    s.append(txt(24, a + 34, "「以此」二字，把「知」的来源说尽了：不是知道得多，是站对了地方。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "惚兮恍兮，其中有象；恍兮惚兮，其中有物。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "吾何以知众甫之状哉？以此。", 5.4, GREEN, "middle"))
    s.append(gold(c + 62, "ch21c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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



# ============ 第六十六章 · 一条水路 ============
def ch66a_yi_tiao_shui_lu():
    W, H = 380, 656
    body, y = head(W, H, "谷是水的路，不是山的凹：低处的好处不在低，在水都往这儿走",
                   "第 六 十 六 章 · 谷", "一条水路", "以其善下之，故能为百谷王。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「谷」，《说文》「泉出通川为谷」——泉水出地，流出去通到川，这一段叫谷。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "谷不吸引水：谷只是低，水自己往低处走。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、剖开看：泉出来，沿低处走，通到川", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="126" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M26,{gy + 24} L92,{gy + 24} L154,{gy + 60} L236,{gy + 94} L354,{gy + 94} L354,{gy + 126} L26,{gy + 126} Z" fill="#F2EADA" stroke="none"/>')
    s.append(f'<path d="M26,{gy + 24} L92,{gy + 24} L154,{gy + 60} L236,{gy + 94} L354,{gy + 94}" fill="none" stroke="{INK}" stroke-width="1"/>')
    # 泉
    s.append(f'<circle cx="58" cy="{gy + 26}" r="3.4" fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
    for k in range(3):
        s.append(f'<line x1="{52 + k * 5}" y1="{gy + 14}" x2="{52 + k * 5}" y2="{gy + 7}" stroke="{GREEN}" stroke-width="0.8"/>')
    s.append(txt(76, gy + 16, "泉", 4.4, GREEN))
    # 水路：贴着地面往下走
    s.append(f'<path d="M62,{gy + 23} Q78,{gy + 20} 92,{gy + 21} L150,{gy + 57} L232,{gy + 90} L318,{gy + 90}" '
             f'fill="none" stroke="{GREEN}" stroke-width="1.6"/>')
    s.append(arrow(302, gy + 90, 324, gy + 90, GREEN, 1.2, head="arr2"))
    # 川
    s.append(f'<path d="M236,{gy + 94} L354,{gy + 94} L354,{gy + 104} L236,{gy + 104} Z" fill="{GREEN}" opacity="0.18" stroke="none"/>')
    s.append(txt(330, gy + 88, "川", 4.6, GREEN, "middle"))
    s.append(txt(126, gy + 34, "谷：水走的那一段", 4.4, SEAL))
    s.append(f'<line x1="168" y1="{gy + 38}" x2="150" y2="{gy + 56}" stroke="{SEAL}" stroke-width="0.6" stroke-dasharray="2 2"/>')
    s.append(txt(190, gy + 118, "谷不是两山夹出的凹：是水往下走的那一段路", 4.6, "#6E6459", "middle"))

    s.append(txt(24, y + 204, "二、俯看：百条水路，各自往一处走", 4.8, GREEN))
    gy2 = y + 216
    s.append(f'<rect x="26" y="{gy2}" width="328" height="126" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    xs = [58, 108, 162, 222, 282, 326]
    for i, xx in enumerate(xs):
        s.append(f'<path d="M{xx},{gy2 + 10} Q{xx + 4},{gy2 + 30} {xx},{gy2 + 48} Q{xx - 4},{gy2 + 62} '
                 f'{190 + (xx - 190) * 0.45},{gy2 + 74}" fill="none" stroke="{GREEN}" stroke-width="1.1" stroke-dasharray="3 2"/>')
    s.append(f'<path d="M44,{gy2 + 80} L336,{gy2 + 80} L306,{gy2 + 118} L74,{gy2 + 118} Z" fill="{GREEN}" opacity="0.16" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(190, gy2 + 104, "江 海", 6.4, GREEN, "middle", spacing="3"))
    s.append(txt(190, gy2 + 40, "百 谷", 4.8, "#6E6459", "middle", spacing="2"))
    s.append(arrow(190, gy2 + 58, 190, gy2 + 74, GREEN, 1.0, head="arr2"))
    s.append(txt(190, gy2 + 52, "王：天下所归往", 4.4, SEAL, "middle"))
    s.append(txt(190, gy2 + 140, "海不以大名，以纳百川：低处的好处，在所有的水都往这儿走", 4.6, "#6E6459", "middle"))

    a = gy2 + 158
    s.append(txt(24, a, "「王」，《说文》「天下所归往也」：往，不是管。", 4.9, INK))
    s.append(txt(24, a + 16, "江海能王百谷，不是因为管着百川，是因为百川往它那儿去。", 4.9, INK))
    s.append(txt(24, a + 34, "水不是被叫来的，是自己走来的。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "谷不是山的凹，是水的路；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "不是谷招水，是水自己往低处走。", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch66a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十六章 · 一只口袋 ============
def ch66b_yi_zhi_kou_dai():
    W, H = 380, 724
    body, y = head(W, H, "重不是东西多，是压在身上：上位者最容易变成那只口袋",
                   "第 六 十 六 章 · 重", "一只口袋", "处上而民不重。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「重」，《说文》「厚也」，金文从人从东——东是两头扎起的囊橐。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "一个人背着口袋，这就是重：不是东西多，是压在身上。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、背着：每加一件，背上沉一分", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="160" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 148}" x2="346" y2="{gy + 148}" stroke="{INK}" stroke-width="1.1"/>')
    # 侧身的人：向前倾
    s.append(f'<circle cx="176" cy="{gy + 40}" r="6.4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M170,{gy + 47} L184,{gy + 45} L196,{gy + 104} L176,{gy + 108} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="182" y1="{gy + 108}" x2="186" y2="{gy + 148}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="192" y1="{gy + 106}" x2="200" y2="{gy + 148}" stroke="{INK}" stroke-width="1.2"/>')
    # 背后的口袋：两头扎起
    s.append(f'<path d="M164,{gy + 56} Q148,{gy + 58} 150,{gy + 76} Q152,{gy + 94} 166,{gy + 94} '
             f'Q180,{gy + 94} 182,{gy + 76} Q184,{gy + 58} 168,{gy + 56} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="166" cy="{gy + 53}" r="4.6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="166" cy="{gy + 97}" r="4.6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # 压：三条短下箭头
    for k in range(3):
        xx = 158 + k * 5
        s.append(arrow(xx, gy + 36, xx, gy + 50, SEAL, 0.9, head="arrS"))
    s.append(txt(120, gy + 138, "东：两头扎起的囊橐", 4.4, SEAL, "middle"))
    # 右：加的东西
    labs = ["赋税", "劳役", "仪仗"]
    for i, lb in enumerate(labs):
        yy = gy + 84 - i * 14
        s.append(box(250, yy, 58, 12, fill="#F2EADA", stroke="#C9B79A"))
        s.append(txt(279, yy + 8.4, lb, 4.0, INK, "middle"))
    s.append(txt(279, gy + 40, "每加一件", 4.2, SEAL, "middle"))
    s.append(txt(279, gy + 50, "背上沉一分", 4.2, SEAL, "middle"))
    s.append(arrow(246, gy + 72, 186, gy + 60, SEAL, 0.9, dash="3 3", head="arrS"))
    s.append(txt(190, gy + 174, "背上的东西越多，底下越觉得沉", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 254, "二、放下：背着空，底下就不觉得沉", 4.8, GREEN))
    gy2 = y + 266
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 128}" x2="346" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1.1"/>')
    # 站直的人，背空
    s.append(f'<circle cx="176" cy="{gy2 + 30}" r="6.4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(box(169, gy2 + 38, 14, 58, fill="#EFE6D4", stroke=INK))
    s.append(f'<line x1="172" y1="{gy2 + 96}" x2="170" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="180" y1="{gy2 + 96}" x2="182" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1.2"/>')
    # 口袋放在地上
    s.append(f'<path d="M236,{gy2 + 92} Q226,{gy2 + 94} 228,{gy2 + 108} Q230,{gy2 + 122} 242,{gy2 + 122} '
             f'Q254,{gy2 + 122} 256,{gy2 + 108} Q258,{gy2 + 94} 248,{gy2 + 92} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1" stroke-dasharray="2 2"/>')
    s.append(f'<circle cx="242" cy="{gy2 + 89}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(f'<circle cx="242" cy="{gy2 + 125}" r="4.2" fill="none" stroke="{INK}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(txt(306, gy2 + 112, "口袋放在地上", 4.4, GREEN, "middle"))
    s.append(f'<circle cx="176" cy="{gy2 + 66}" r="13" fill="none" stroke="{GREEN}" stroke-width="0.9" opacity="0.7"/>')
    s.append(txt(176, gy2 + 68, "背空", 4.2, GREEN, "middle"))
    s.append(txt(190, gy2 + 154, "民不重：背上不多一个口袋", 4.6, GREEN, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "重不是东西多，是压在身上：赋税、劳役、仪仗、供应，每加一件沉一分。", 4.8, INK))
    s.append(txt(24, a + 16, "害是抢走本该属于他的：一手举旗，一手在旗下取物。", 4.8, INK))
    s.append(txt(24, a + 34, "处上不重，管的是压；处前不害，管的是抢。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "重者，人背一囊；害者，旗下取物。", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "上位者最该怕的，就这两件。", 4.8, GREEN, "middle"))
    s.append(gold(c + 62, "ch66b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十六章 · 一口气 ============
def ch66c_yi_kou_qi():
    W, H = 380, 706
    body, y = head(W, H, "厌是又撑又压，不是嫌弃：一只吃饱的兽，被压在崖底下",
                   "第 六 十 六 章 · 厌", "一口气", "天下乐推而不厌。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「厌」，《说文》「笮也」，笮是压；从厂从猒——厂是山崖，猒是「饱也」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "一只吃饱的兽，被压在崖底下：又撑，又压。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、压在崖下：先觉闷，后觉满", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 崖：厂形
    s.append(f'<path d="M58,{gy + 12} L312,{gy + 12} L312,{gy + 44} L96,{gy + 44} L58,{gy + 72} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(76, gy + 32, "厂 · 崖", 4.6, INK))
    for k in range(3):
        s.append(f'<line x1="{112 + k * 34}" y1="{gy + 20}" x2="{132 + k * 34}" y2="{gy + 34}" stroke="{INK}" stroke-width="0.6" opacity="0.5"/>')
    # 兽：饱腹
    s.append(f'<ellipse cx="182" cy="{gy + 84}" rx="34" ry="20" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M158,{gy + 92} Q182,{gy + 80} 206,{gy + 92} Q182,{gy + 100} 158,{gy + 92} Z" fill="#DED2B8" stroke="none"/>')
    s.append(f'<circle cx="222" cy="{gy + 66}" r="9" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M218,{gy + 57} Q222,{gy + 51} 226,{gy + 57}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="228" cy="{gy + 63}" r="1.4" fill="{INK}" stroke="none"/>')
    s.append(f'<path d="M228,{gy + 72} L236,{gy + 70}" stroke="{INK}" stroke-width="0.7" fill="none"/>')
    for xx in (162, 176, 190, 204):
        s.append(f'<line x1="{xx}" y1="{gy + 102}" x2="{xx}" y2="{gy + 122}" stroke="{INK}" stroke-width="1.1"/>')

    # 压：三条箭头下来
    for k in range(3):
        xx = 164 + k * 20
        s.append(arrow(xx, gy + 46, xx, gy + 62, SEAL, 1.0, head="arrS"))
    s.append(txt(176, gy + 79, "饱", 4.4, SEAL, "middle"))
    s.append(txt(104, gy + 58, "压", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 140, "又撑又压，动弹不得：连话都不想说", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 234, "二、出到崖外：那口气还喘得动", 4.8, GREEN))
    gy2 = y + 246
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 124}" x2="346" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1.1"/>')
    # 兽站着，腹仍饱
    s.append(f'<ellipse cx="156" cy="{gy2 + 76}" rx="30" ry="19" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="194" cy="{gy2 + 56}" r="9" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="200" cy="{gy2 + 53}" r="1.4" fill="{INK}" stroke="none"/>')
    for xx in (140, 152, 166, 178):
        s.append(f'<line x1="{xx}" y1="{gy2 + 93}" x2="{xx}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1.1"/>')
    # 一口气：从嘴出来，往上散
    s.append(f'<path d="M204,{gy2 + 60} Q224,{gy2 + 52} 240,{gy2 + 44} Q258,{gy2 + 36} 276,{gy2 + 38}" fill="none" stroke="{GREEN}" stroke-width="1.0"/>')
    s.append(f'<path d="M206,{gy2 + 64} Q226,{gy2 + 62} 246,{gy2 + 56} Q264,{gy2 + 50} 282,{gy2 + 52}" fill="none" stroke="{GREEN}" stroke-width="0.8" opacity="0.7"/>')
    s.append(txt(290, gy2 + 36, "一口气", 4.4, GREEN, "middle"))
    for k in range(3):
        s.append(f'<circle cx="{286 + k * 7}" cy="{gy2 + 50 + k * 3}" r="1.3" fill="{GREEN}" stroke="none" opacity="0.7"/>')
    # 推：几只手往上送
    for k in range(3):
        xx = 96 + k * 0
        pass
    s.append(txt(56, gy2 + 44, "乐推：不是被挤上去", 4.3, GREEN))
    s.append(txt(56, gy2 + 54, "是自己愿意送他上去", 4.3, GREEN))
    s.append(txt(190, gy2 + 150, "不厌：不觉得他压得慌，气还喘得动", 4.6, GREEN, "middle"))

    a = gy2 + 170
    s.append(txt(24, a, "厌不是情绪，是体感：一个上位者好不好，看底下人觉得轻不觉得轻。", 4.8, INK))
    s.append(txt(24, a + 16, "乐推的推，《说文》「排也」——用手往外送：不是被挤上去，是自己愿意送上去。", 4.8, INK))
    s.append(txt(24, a + 34, "不争不是打赢所有人，是对手不存在：他不拽那件东西。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "厭从厂从猒，饱兽压崖；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "非嫌其人也，乃觉其沉。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch66c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十七章 · 一丛草 ============
def ch67a_yi_cong_cao():
    W, H = 380, 684
    body, y = head(W, H, "慈从心兹，兹是草木多益：心里长草，草不问落在哪儿",
                   "第 六 十 七 章 · 慈", "一丛草", "一曰慈，二曰俭，三曰不敢为天下先。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「慈」，《说文》「爱也」，从心、兹声；兹是「草木多益」——草越长越多。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "爱有对象，慈没有：它是那片草，草长出来，不管落在哪儿。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、心里长草：不圈、不指，四面都长", 4.8, GREEN))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 190, gy + 66
    s.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(cx, cy + 3, "心", 9.5, INK, "middle"))
    # 心里的草：从心里长出去
    for bx, by, bh, dx in ((-8, -4, 30, -6), (0, -8, 40, 0), (7, -5, 28, 6)):
        s.append(f'<path d="M{cx + bx},{cy + by} Q{cx + bx + dx * 0.6},{cy + by - bh * 0.55} {cx + bx + dx},{cy + by - bh}" '
                 f'fill="none" stroke="{GREEN}" stroke-width="1.3"/>')
        my = cy + by - bh * 0.5
        s.append(f'<path d="M{cx + bx + dx * 0.35},{my} q{dx * 0.9 - 4},-5 {dx * 2 - 6},-9" fill="none" '
                 f'stroke="{GREEN}" stroke-width="0.8" opacity="0.8"/>')
    # 四面也长：贴着圆边再冒几丛
    for (bx, by, ang) in ((-30, -6, -1), (-26, 14, -1), (30, -6, 1), (26, 14, 1), (-8, 30, 0), (10, 30, 0)):
        for k in (-3, 3):
            s.append(f'<path d="M{cx + bx},{cy + by} Q{cx + bx + ang * 10 + k},{cy + by + (8 if ang == 0 else -8)} '
                     f'{cx + bx + ang * 16 + k},{cy + by + (18 if ang == 0 else -16)}" '
                     f'fill="none" stroke="{GREEN}" stroke-width="1.0" opacity="0.75"/>')
    s.append(txt(190, gy + 148, "草往外长，四面都有：不圈定一个对象", 4.6, GREEN, "middle"))

    s.append(txt(24, y + 228, "二、圈住一棵：那是爱，不是慈", 4.8, SEAL))
    gy2 = y + 240
    s.append(f'<rect x="26" y="{gy2}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 104}" x2="340" y2="{gy2 + 104}" stroke="{INK}" stroke-width="1"/>')
    for i, px in enumerate((100, 190, 280)):
        for k in (-6, 0, 6):
            s.append(f'<path d="M{px + k},{gy2 + 104} Q{px + k + 3},{gy2 + 74} {px + k - 2},{gy2 + 52 + abs(k) * 2}" '
                     f'fill="none" stroke="{GREEN}" stroke-width="1.1" opacity="{0.85 if px == 190 else 0.45}"/>')
    s.append(f'<circle cx="190" cy="{gy2 + 80}" r="34" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(txt(190, gy2 + 40, "圈住这一棵", 4.4, SEAL, "middle"))
    s.append(txt(100, gy2 + 120, "其余在外", 4.2, "#A89577", "middle"))
    s.append(txt(280, gy2 + 120, "其余在外", 4.2, "#A89577", "middle"))
    s.append(txt(190, gy2 + 148, "爱护一棵，护不住就拼命；慈护一片，护的时候极稳", 4.6, "#6E6459", "middle"))

    a = gy2 + 166
    s.append(txt(24, a, "慈不是「心里有个喜欢的人」，是「心里有一片自己在长的东西」。", 4.8, INK))
    s.append(txt(24, a + 16, "草不会因为护一棵，就把别的拔掉。", 4.8, INK))
    s.append(txt(24, a + 34, "慈故能勇：护的是一片生机，不用拼命，反而极稳。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "慈从心兹，兹者草木多益；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "心中自有草长，不问其落于何处。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch67a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十七章 · 一束绳 ============
def ch67b_yi_shu_sheng():
    W, H = 380, 684
    body, y = head(W, H, "俭是约，约是绳缠束：收十处为一束，一束可推千里",
                   "第 六 十 七 章 · 俭", "一束绳", "俭，故能广。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「俭」，《说文》「约也」——约是绳缠束：把散着的收拢成一束。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "俭的反面不是奢侈，是散：语言散出去收不回，心神散出去聚不拢。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、散在十处：十处都不深", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 十根散线，从一处散开
    for i in range(9):
        ex = 150 + i * 21
        ey = gy + 34 + (14 if i % 2 else 0)
        s.append(f'<path d="M68,{gy + 92} L{ex},{ey}" fill="none" stroke="#B9A98F" stroke-width="0.9" stroke-dasharray="3 3"/>')
        s.append(f'<circle cx="{ex}" cy="{ey}" r="2" fill="#B9A98F" stroke="none"/>')
    s.append(f'<circle cx="68" cy="{gy + 92}" r="4.2" fill="{SEAL}" stroke="none"/>')
    s.append(txt(68, gy + 110, "一处力气", 4.2, SEAL, "middle"))
    s.append(txt(190, gy + 148, "散在十处：每一处都只落一点", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 228, "二、收成一束：一股能推很远", 4.8, GREEN))
    gy2 = y + 240
    s.append(f'<rect x="26" y="{gy2}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 一束：十根并拢 + 三道缠绳
    mid = gy2 + 64
    for i in range(10):
        yy = gy2 + 46 + i * 3.6
        s.append(f'<line x1="66" y1="{mid + (yy - mid) * 0.78}" x2="200" y2="{mid + (yy - mid) * 0.62}" '
                 f'stroke="#C9B79A" stroke-width="1"/>')
    for k in range(3):
        xx = 96 + k * 32
        s.append(f'<rect x="{xx}" y="{gy2 + 42}" width="7" height="38" rx="2" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(90, gy2 + 96, "绳缠束：约", 4.4, SEAL))
    # 推得很远
    s.append(arrow(210, gy2 + 64, 320, gy2 + 64, GREEN, 1.2, head="arr2"))
    s.append(txt(316, gy2 + 52, "推千里", 4.4, GREEN, "end"))
    s.append(txt(190, gy2 + 148, "收得越紧，铺得越开：广不是多，是有余地", 4.6, GREEN, "middle"))

    a = gy2 + 166
    s.append(txt(24, a, "收得紧，不是省着不花，是知道什么值得攥住。", 4.8, INK))
    s.append(txt(24, a + 16, "多言数穷，多藏厚亡——都不是骂奢侈，是说散。", 4.8, INK))
    s.append(txt(24, a + 34, "俭是第一等的节流：它存的不是钱，是精气神。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "俭者约也，约者绳缠束；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "收十处为一束，一束可推千里。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch67b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十七章 · 一圈墙 ============
def ch67c_yi_quan_qiang():
    W, H = 380, 684
    body, y = head(W, H, "慈不是盾，是墙：盾挡一面，墙围一圈",
                   "第 六 十 七 章 · 卫", "一圈墙", "天将救之，以慈卫之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「卫」，《说文》「宿卫也」，从行、从帀——帀是「周也」，绕一圈。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "帛书作「如以慈垣之」：垣是墙。挡是一面盾，围是一圈墙。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、一面盾：只挡得住一面", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    pxx, pyy = 200, gy + 74
    s.append(f'<circle cx="{pxx}" cy="{pyy - 26}" r="6.2" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(box(pxx - 7, pyy - 18, 14, 34, fill="#EFE6D4", stroke=INK))
    s.append(f'<line x1="{pxx - 4}" y1="{pyy + 16}" x2="{pxx - 5}" y2="{pyy + 42}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{pxx + 4}" y1="{pyy + 16}" x2="{pxx + 5}" y2="{pyy + 42}" stroke="{INK}" stroke-width="1.2"/>')
    # 盾在左侧
    s.append(f'<path d="M{pxx - 30},{pyy - 40} L{pxx - 16},{pyy - 40} L{pxx - 16},{pyy + 26} L{pxx - 23},{pyy + 38} '
             f'L{pxx - 30},{pyy + 26} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    # 左边的箭被挡住
    for k in (-1, 0, 1):
        s.append(arrow(58, pyy - 20 + k * 16, pxx - 34, pyy - 20 + k * 16, "#B9A98F", 1.0, head="arr"))
    # 右边、后面的箭打到身上
    s.append(arrow(330, pyy - 30, pxx + 16, pyy - 26, SEAL, 1.0, head="arrS"))
    s.append(arrow(330, pyy + 18, pxx + 12, pyy + 14, SEAL, 1.0, head="arrS"))
    s.append(txt(64, pyy - 44, "挡得住", 4.2, "#A89577"))
    s.append(txt(300, pyy + 40, "挡不住", 4.2, SEAL, "middle"))
    s.append(txt(190, gy + 148, "一面盾只有一面：其余三面都空着", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 228, "二、一圈墙：四面八方都在里面", 4.8, GREEN))
    gy2 = y + 240
    s.append(f'<rect x="26" y="{gy2}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    qx, qy = 190, gy2 + 72
    s.append(f'<circle cx="{qx}" cy="{qy - 20}" r="6.2" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(box(qx - 7, qy - 12, 14, 30, fill="#EFE6D4", stroke=INK))
    s.append(f'<line x1="{qx - 4}" y1="{qy + 18}" x2="{qx - 5}" y2="{qy + 40}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{qx + 4}" y1="{qy + 18}" x2="{qx + 5}" y2="{qy + 40}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{qx}" cy="{qy - 6}" r="58" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<circle cx="{qx}" cy="{qy - 6}" r="62" fill="none" stroke="{GREEN}" stroke-width="0.5" opacity="0.5"/>')
    # 四面来的箭，都停在墙上
    for k in range(4):
        a0 = k * 90 + 45
        import math
        dx = math.cos(math.radians(a0))
        dy = math.sin(math.radians(a0))
        sx, sy = qx + dx * 84, qy - 6 + dy * 84
        ex, ey = qx + dx * 64, qy - 6 + dy * 64
        s.append(arrow(sx, sy, ex, ey, SEAL, 1.0, head="arrS"))
    s.append(txt(190, gy2 + 148, "围住的里面，伤不着：以战则胜，以守则固", 4.6, GREEN, "middle"))

    a = gy2 + 166
    s.append(txt(24, a, "天将救之，不是天伸一只手来拉他，是天让他自己被慈围住。", 4.8, INK))
    s.append(txt(24, a + 16, "战是把这圈往前推，守是把这圈收紧——都不是打，是围。", 4.8, INK))
    s.append(txt(24, a + 34, "挡是防着一个方向，围是四面都在里面。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "慈是围墙，不是盾牌；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "盾挡一面，墙围一圈。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch67c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十八章 · 一只脚 ============
def ch68a_yi_zhi_jiao():
    W, H = 380, 690
    body, y = head(W, H, "武从止从戈：不是扔下戈，是脚停在戈前",
                   "第 六 十 八 章 · 武", "一只脚", "善为士者，不武。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「武」，《说文》引楚庄王「夫武，定功戢兵。故止戈为武」。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "止是脚：脚走到戈跟前，停住——不是把戈扔了。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、脚停在戈前：有戈，脚不动", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 戈：竖柲 + 横刃
    s.append(f'<line x1="236" y1="{gy + 24}" x2="236" y2="{gy + 126}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M236,{gy + 22} L168,{gy + 30} L236,{gy + 37} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="228" y="{gy + 37}" width="8" height="18" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="236" cy="{gy + 118}" r="2.6" fill="{SEAL}" stroke="none"/>')
    s.append(txt(214, gy + 18, "戈", 5.0, INK))
    # 脚：脚掌 + 四趾，趾尖朝右，停在戈前
    s.append(f'<path d="M176,{gy + 120} Q174,{gy + 111} 184,{gy + 109} L202,{gy + 108} '
             f'Q212,{gy + 108} 213,{gy + 116} Q214,{gy + 125} 202,{gy + 126} L184,{gy + 126} Q176,{gy + 126} 176,{gy + 120} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for dy in (-7, -3, 1, 5):
        s.append(f'<line x1="213" y1="{gy + 118 + dy}" x2="220" y2="{gy + 118 + dy}" stroke="{INK}" stroke-width="1" stroke-linecap="round"/>')
    s.append(txt(176, gy + 136, "脚", 5.0, SEAL))
    # 停住的那条界
    s.append(f'<line x1="222" y1="{gy + 96}" x2="222" y2="{gy + 128}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    s.append(txt(222, gy + 92, "停", 4.4, SEAL, "middle"))
    s.append(f'<line x1="40" y1="{gy + 126}" x2="340" y2="{gy + 126}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 156, "不是没有戈，是脚不动：趾尖离柲一寸，停在那儿", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 258, "二、戈收进鞘：功定，兵戢", 4.8, GREEN))
    gy2 = y + 270
    s.append(f'<rect x="26" y="{gy2}" width="328" height="130" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 116}" x2="340" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1"/>')
    # 鞘：包住刃
    s.append(f'<path d="M236,{gy2 + 22} L168,{gy2 + 30} L236,{gy2 + 37} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(f'<rect x="150" y="{gy2 + 20}" width="94" height="18" rx="9" fill="{GREEN}" opacity="0.18" stroke="{GREEN}" stroke-width="1"/>')
    for xx in (176, 216):
        s.append(f'<rect x="{xx}" y="{gy2 + 24}" width="4" height="16" rx="1.5" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="236" y1="{gy2 + 32}" x2="236" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(txt(196, gy2 + 18, "鞘", 4.8, GREEN))
    # 脚仍停在原处
    s.append(f'<path d="M176,{gy2 + 110} Q174,{gy2 + 101} 184,{gy2 + 99} L202,{gy2 + 98} '
             f'Q212,{gy2 + 98} 213,{gy2 + 106} Q214,{gy2 + 115} 202,{gy2 + 116} L184,{gy2 + 116} Q176,{gy2 + 116} 176,{gy2 + 110} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for dy in (-7, -3, 1, 5):
        s.append(f'<line x1="213" y1="{gy2 + 108 + dy}" x2="220" y2="{gy2 + 108 + dy}" stroke="{INK}" stroke-width="1" stroke-linecap="round"/>')
    s.append(txt(190, gy2 + 132, "刃收进鞘，脚还在原地：这就是止戈", 4.6, GREEN, "middle"))

    a = gy2 + 150
    s.append(txt(24, a, "邲之战后潘党要筑京观，楚庄王不肯：打赢的人先说的是「戢兵」。", 4.8, INK))
    s.append(txt(24, a + 16, "定功戢兵——功先定，刀后收；胜而不收者，犹未胜也。", 4.8, INK))
    s.append(txt(24, a + 34, "打输的人说收刀，是自慰；打赢的人说收刀，才算赢。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "武从止从戈，止者足也；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "非扔其戈，乃停其足。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch68a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十八章 · 一道缝 ============
def ch68b_yi_dao_feng():
    W, H = 380, 706
    body, y = head(W, H, "与是党与：四手抬一物就成一对；不与，是留住那条缝",
                   "第 六 十 八 章 · 与", "一道缝", "善胜敌者，不与。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「与」，《说文》「党与也」；争是两手引一物——两个动作都要有一个对手。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "不给对手，就没有争：不与不是避战，是不成对。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、四手抬一物：成了对，就只剩输赢", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 中间一件物
    s.append(box(160, gy + 52, 60, 42, fill="#EFE6D4", stroke=INK))
    s.append(txt(190, gy + 78, "一物", 4.8, INK, "middle"))
    # 四只手：左二右二
    for yy in (gy + 46, gy + 84):
        s.append(f'<line x1="56" y1="{yy + 12}" x2="138" y2="{yy + 2}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<path d="M138,{yy + 2} q6,-6 14,0 q4,4 0,8 q-8,5 -14,0 Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        for k in range(3):
            s.append(f'<line x1="{138 + k * 1}" y1="{yy - 2 + k * 3}" x2="{144 + k * 1}" y2="{yy - 3 + k * 3}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="324" y1="{yy + 12}" x2="242" y2="{yy + 2}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<path d="M242,{yy + 2} q-6,-6 -14,0 q-4,4 0,8 q8,5 14,0 Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        for k in range(3):
            s.append(f'<line x1="{242 - k * 1}" y1="{yy - 2 + k * 3}" x2="{236 - k * 1}" y2="{yy - 3 + k * 3}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(96, gy + 40, "我们", 4.4, "#6E6459", "middle"))
    s.append(txt(284, gy + 40, "他们", 4.4, "#6E6459", "middle"))
    s.append(txt(190, gy + 156, "四手抬一物：两边成了一对，中间没有缝", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 244, "二、手收回来：缝留着，两边才还是两边", 4.8, GREEN))
    gy2 = y + 256
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 中间：缝（一条留白的通道）
    s.append(f'<rect x="178" y="{gy2 + 26}" width="24" height="86" fill="#F2EADA" stroke="none"/>')
    s.append(f'<line x1="178" y1="{gy2 + 26}" x2="178" y2="{gy2 + 112}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="202" y1="{gy2 + 26}" x2="202" y2="{gy2 + 112}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    for yy in (gy2 + 46, gy2 + 84):
        s.append(f'<line x1="60" y1="{yy + 10}" x2="116" y2="{yy + 2}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="124" cy="{yy + 1}" rx="8" ry="5" fill="none" stroke="{INK}" stroke-width="0.9" stroke-dasharray="2 2"/>')
        s.append(f'<line x1="320" y1="{yy + 10}" x2="264" y2="{yy + 2}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="256" cy="{yy + 1}" rx="8" ry="5" fill="none" stroke="{INK}" stroke-width="0.9" stroke-dasharray="2 2"/>')
    s.append(txt(190, gy2 + 124, "缝", 4.6, SEAL, "middle"))
    s.append(txt(96, gy2 + 40, "我们", 4.4, "#6E6459", "middle"))
    s.append(txt(284, gy2 + 40, "他们", 4.4, "#6E6459", "middle"))
    s.append(txt(190, gy2 + 156, "手停在半路，缝里没有东西：谁也拽不进谁", 4.6, GREEN, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "争要成对，与也要成对：两个动作的前提，是有一个对手。", 4.8, INK))
    s.append(txt(24, a + 16, "不给对手，就没有争；没有争，才谈得上胜。", 4.8, INK))
    s.append(txt(24, a + 34, "不跟敌人配对，却跟天配上了：是谓配天。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "与者党与，四手抬一物；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "缝留着，两边才还是两边。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch68b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十八章 · 一根筋 ============
def ch68c_yi_gen_jin():
    W, H = 380, 706
    body, y = head(W, H, "力是筋：筋不使劲，筋是连——连上了，劲自然传过去",
                   "第 六 十 八 章 · 力", "一根筋", "善用人者，为之下。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「力」，《说文》「筋也」——筋连骨，不使劲；力是传过去的，不是攒出来的。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "「为之下」：站到下面，筋才连得上。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、各站各的高处：筋搭不上", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 两根骨，一高一低
    s.append(box(78, gy + 34, 26, 12, fill="#EFE6D4", stroke=INK))
    s.append(box(78, gy + 108, 26, 12, fill="#EFE6D4", stroke=INK))
    # 两段筋，断着
    s.append(f'<path d="M104,{gy + 40} Q136,{gy + 52} 150,{gy + 62}" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(f'<path d="M104,{gy + 114} Q136,{gy + 100} 150,{gy + 88}" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(f'<line x1="152" y1="{gy + 58}" x2="152" y2="{gy + 92}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    s.append(txt(160, gy + 78, "断", 4.4, SEAL))
    s.append(txt(60, gy + 40, "骨", 4.4, "#6E6459", "end"))
    s.append(txt(60, gy + 114, "骨", 4.4, "#6E6459", "end"))
    s.append(txt(230, gy + 46, "一人站高", 4.4, "#6E6459"))
    s.append(txt(230, gy + 112, "一人站低", 4.4, "#6E6459"))
    s.append(arrow(300, gy + 60, 300, gy + 96, "#B9A98F", 1.0))
    s.append(txt(190, gy + 156, "高低差着，筋搭不上：各使各的劲，谁也不传", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 244, "二、站到下面：两端齐了，筋一连，劲就传过去", 4.8, GREEN))
    gy2 = y + 256
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 两骨在一线上
    s.append(box(50, gy2 + 64, 26, 12, fill="#EFE6D4", stroke=INK))
    s.append(box(304, gy2 + 64, 26, 12, fill="#EFE6D4", stroke=INK))
    s.append(txt(44, gy2 + 70, "骨", 4.2, "#6E6459", "end"))
    s.append(txt(336, gy2 + 70, "骨", 4.2, "#6E6459", "end"))
    # 筋：一根绷直的线
    s.append(f'<line x1="76" y1="{gy2 + 70}" x2="304" y2="{gy2 + 70}" stroke="{GREEN}" stroke-width="1.8"/>')
    # 支点在下面
    s.append(f'<path d="M172,{gy2 + 108} L190,{gy2 + 74} L208,{gy2 + 108} Z" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="164" y1="{gy2 + 108}" x2="216" y2="{gy2 + 108}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy2 + 124, "为之下：支点在下面", 4.4, GREEN, "middle"))
    # 劲两头传开
    s.append(arrow(190, gy2 + 64, 96, gy2 + 64, GREEN, 1.0, head="arrL"))
    s.append(arrow(190, gy2 + 64, 284, gy2 + 64, GREEN, 1.0, head="arr2"))
    s.append(txt(190, gy2 + 156, "一端在下面托住，筋才绷得直：两头的劲接上了", 4.6, GREEN, "middle"))


    a = gy2 + 174
    s.append(txt(24, a, "力不是攒出来的，是传过去的：士是推十合一，不是一人当十。", 4.8, INK))
    s.append(txt(24, a + 16, "烛之武推辞，郑伯认错「是寡人之过也」——一句低头，换回一国。", 4.8, INK))
    s.append(txt(24, a + 34, "站低一处，众人的劲才连成一根筋。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "力者，筋也；筋不使劲，筋是连。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "连上了，劲自然传过去。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch68c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十九章 · 一盏灯 ============
def ch69a_yi_zhan_deng():
    W, H = 380, 714
    body, y = head(W, H, "主是灯里那一星火，众物绕着它转；客是寄居，时辰在人",
                   "第 六 十 九 章 · 主", "一盏灯", "吾不敢为主，而为客。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「客」，《说文》「寄也」，从宀从各——寄居在别人家里。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "为主：时辰、地点、开头、收场都归我；为客：这四样全归他。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、为主：灯在当中，众物绕着它转", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 190, gy + 66
    # 灯
    s.append(f'<path d="M180,{cy - 14} L200,{cy - 14} L196,{cy - 22} L184,{cy - 22} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="190" cy="{cy - 9}" r="4.4" fill="{SEAL}" stroke="none"/>')
    s.append(f'<circle cx="190" cy="{cy - 9}" r="8" fill="none" stroke="{SEAL}" stroke-width="0.6" opacity="0.5"/>')
    s.append(txt(190, cy + 8, "主", 6.0, SEAL, "middle"))
    # 四件东西，绕着转
    pos = ((190, cy - 46), (246, cy - 6), (190, cy + 34), (134, cy - 6))
    for i, (px, py) in enumerate(pos):
        if i % 2 == 0:
            s.append(box(px - 9, py - 8, 18, 16, fill="#EFE6D4", stroke=INK))
        else:
            s.append(f'<circle cx="{px}" cy="{py}" r="9" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
        s.append(txt(px, py + 3, "物", 4.2, "#6E6459", "middle"))
    # 绕的轨：一圈虚线 + 两个切向箭头
    s.append(f'<circle cx="190" cy="{cy - 6}" r="54" fill="none" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="4 4" opacity="0.8"/>')
    s.append(arrow(232, cy + 24, 238, cy + 14, GREEN, 1.0, head="arr2"))
    s.append(arrow(148, cy - 36, 142, cy - 26, GREEN, 1.0, head="arr2"))
    s.append(txt(190, gy + 156, "一切从它这儿起：定时间、定地点的人，就是主人", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 250, "二、为客：宿在人家的屋里，时辰在他", 4.8, GREEN))
    gy2 = y + 262
    s.append(f'<rect x="26" y="{gy2}" width="328" height="130" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 屋
    s.append(f'<path d="M70,{gy2 + 56} L170,{gy2 + 20} L270,{gy2 + 56} L270,{gy2 + 116} L70,{gy2 + 116} Z" '
             f'fill="none" stroke="{INK}" stroke-width="1"/>')
    # 右墙上一道门：客人立在门口
    s.append(f'<line x1="270" y1="{gy2 + 116}" x2="270" y2="{gy2 + 72}" stroke="{INK}" stroke-width="2.2" opacity="0.55"/>')
    s.append(f'<path d="M70,{gy2 + 56} L170,{gy2 + 20} L270,{gy2 + 56}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # 主人的灯
    s.append(f'<path d="M138,{gy2 + 66} L156,{gy2 + 66} L152,{gy2 + 58} L142,{gy2 + 58} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="147" cy="{gy2 + 62}" r="3.6" fill="{SEAL}" stroke="none"/>')
    s.append(txt(147, gy2 + 84, "主人家的灯", 4.2, "#6E6459", "middle"))
    # 客人：站在门边
    s.append(f'<circle cx="243" cy="{gy2 + 60}" r="5.2" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(box(238, gy2 + 66, 10, 22, fill="#EFE6D4", stroke=INK))
    s.append(f'<line x1="241" y1="{gy2 + 88}" x2="239" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="246" y1="{gy2 + 88}" x2="247" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1"/>')
    s.append(box(252, gy2 + 98, 13, 11, fill="#F2EADA", stroke="#C9B79A", dash="2 2"))
    s.append(txt(222, gy2 + 58, "客", 4.6, GREEN, "middle"))
    s.append(txt(190, gy2 + 146, "寄居：屋是他的，灯是他的，什么时候走也是他定", 4.6, GREEN, "middle"))

    a = gy2 + 164
    s.append(txt(24, a, "主是灯里那一星火，别的东西围着它转：当主人，就是让所有事从你这儿起。", 4.8, INK))
    s.append(txt(24, a + 16, "让出去的不是那块地，是「谁先动」这个权力。", 4.8, INK))
    s.append(txt(24, a + 34, "不敢为主者，非不能战，乃不敢使此战归我所有。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "主者，灯中一火，众物绕之；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "客者，寄也，宿于人家之屋。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch69a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十九章 · 一双抬高的脚 ============
def ch69b_yi_shuang_jiao():
    W, H = 380, 720
    body, y = head(W, H, "轻敌不是一个念头，是一个姿势：举趾高，心不固矣",
                   "第 六 十 九 章 · 轻", "一双抬高的脚", "祸莫大于轻敌，轻敌几丧吾宝。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "《左传》斗伯比只看了一眼屈瑕走路：「举趾高，心不固矣」——莫敖必败。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "轻敌先长在脚上：脚一抬，三宝先落。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、趾抬得高：脚下虚，心就没落处", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy + 128}" x2="340" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    # 侧身的人：前脚高抬
    s.append(f'<circle cx="176" cy="{gy + 34}" r="6.4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M170,{gy + 42} L184,{gy + 41} L190,{gy + 84} L174,{gy + 86} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    # 后腿：踩实
    s.append(f'<line x1="177" y1="{gy + 86}" x2="168" y2="{gy + 122}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M160,{gy + 122} L176,{gy + 122} Q180,{gy + 126} 174,{gy + 128} L160,{gy + 128} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    # 前腿：抬得很高
    s.append(f'<line x1="188" y1="{gy + 84}" x2="206" y2="{gy + 62}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="206" y1="{gy + 62}" x2="216" y2="{gy + 76}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<g transform="translate(219,{gy + 71}) rotate(-32)">'
             f'<ellipse cx="0" cy="0" rx="9" ry="4.6" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>'
             f'<line x1="7" y1="-2" x2="11" y2="-3" stroke="{INK}" stroke-width="0.8"/>'
             f'<line x1="8" y1="0" x2="12" y2="0" stroke="{INK}" stroke-width="0.8"/>'
             f'<line x1="7" y1="2" x2="11" y2="3" stroke="{INK}" stroke-width="0.8"/></g>')
    # 脚下空
    s.append(f'<line x1="212" y1="{gy + 84}" x2="212" y2="{gy + 126}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="2 2"/>')
    s.append(f'<line x1="230" y1="{gy + 86}" x2="230" y2="{gy + 126}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="2 2"/>')
    s.append(txt(221, gy + 110, "虚", 4.4, SEAL, "middle"))
    s.append(arrow(258, gy + 118, 238, gy + 88, SEAL, 0.9, head="arrS"))
    s.append(txt(262, gy + 122, "举趾高", 4.4, SEAL))
    s.append(txt(190, gy + 162, "趾离地一寸，整只脚就没了根：心也跟着浮起来", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 266, "二、脚放平：根落在土里，心才稳", 4.8, GREEN))
    gy2 = y + 278
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 124}" x2="340" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="176" cy="{gy2 + 34}" r="6.4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M170,{gy2 + 42} L184,{gy2 + 41} L184,{gy2 + 86} L170,{gy2 + 86} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for xx, dxx in ((166, -1), (188, 1)):
        s.append(f'<line x1="{xx}" y1="{gy2 + 86}" x2="{xx + dxx * 3}" y2="{gy2 + 118}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<path d="M{xx + dxx * 3 - 9},{gy2 + 118} L{xx + dxx * 3 + 9},{gy2 + 118} Q{xx + dxx * 3 + 13},{gy2 + 122} {xx + dxx * 3 + 7},{gy2 + 124} '
                 f'L{xx + dxx * 3 - 9},{gy2 + 124} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M160,{gy2 + 126} L200,{gy2 + 126} L196,{gy2 + 132} L164,{gy2 + 132} Z" '
             f'fill="{GREEN}" opacity="0.16" stroke="none"/>')
    s.append(txt(190, gy2 + 144, "两只脚都落在土上：脚一放平，三宝才拿得住", 4.6, GREEN, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "轻敌不是心里的一个念头，它先长在脚上：步子一浮，人就先浮了。", 4.8, INK))
    s.append(txt(24, a + 16, "轻敌几丧吾宝——三宝先落：慈落了，俭落了，不敢为先也落了。", 4.8, INK))
    s.append(txt(24, a + 34, "脚底有没有土，别人一眼就看得见。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "斗伯比一眼而知其败：举趾高，心不固矣。", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "轻敌先长在脚上，脚一抬，三宝先落。", 4.9, GREEN, "middle"))
    s.append(gold(c + 62, "ch69b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十九章 · 一扇门 ============
def ch69c_yi_shan_men():
    W, H = 380, 720
    body, y = head(W, H, "闵是吊者站在门：哀是站在那儿，不进去，也不走",
                   "第 六 十 九 章 · 哀", "一扇门", "故抗兵相若，哀者胜矣。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「哀」，《说文》「闵也」；闵，又解「吊者在门也」——吊丧的人站在门口。", 4.9, INK, "middle"))
    s.append(txt(190, y + 26, "不是「我很伤心」，是「我看见有人死了，我站在他家门口」。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、站在门外：不进去，也不走", 4.8, SEAL))
    gy = y + 60
    s.append(f'<rect x="26" y="{gy}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 门与墙
    s.append(f'<line x1="40" y1="{gy + 128}" x2="340" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M214,{gy + 128} L214,{gy + 30} L296,{gy + 30} L296,{gy + 128}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="222" y="{gy + 38}" width="66" height="90" fill="none" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="255" y1="{gy + 38}" x2="255" y2="{gy + 128}" stroke="{LINE}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    s.append(txt(255, gy + 24, "门", 4.8, INK, "middle"))
    # 靠在墙上的人
    s.append(f'<circle cx="196" cy="{gy + 52}" r="6.4" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M190,{gy + 60} L202,{gy + 59} L204,{gy + 104} L190,{gy + 105} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="192" y1="{gy + 105}" x2="190" y2="{gy + 128}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="202" y1="{gy + 105}" x2="204" y2="{gy + 128}" stroke="{INK}" stroke-width="1.2"/>')
    # 倚墙的手
    s.append(f'<line x1="204" y1="{gy + 66}" x2="218" y2="{gy + 64}" stroke="{INK}" stroke-width="1.1"/>')
    # 泪：几粒小点
    for k in range(3):
        s.append(f'<circle cx="{190 - k * 2}" cy="{gy + 58 + k * 5}" r="1.2" fill="{SEAL}" stroke="none" opacity="0.8"/>')
    s.append(txt(180, gy + 46, "吊者", 4.2, SEAL))
    s.append(txt(190, gy + 144, "立在庭墙边哭：不进门，也不离开", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 266, "二、门里：还有人活着", 4.8, GREEN))
    gy2 = y + 278
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 122}" x2="340" y2="{gy2 + 122}" stroke="{INK}" stroke-width="1"/>')
    # 屋里：几个人围一盏暗灯
    s.append(f'<path d="M50,{gy2 + 50} L120,{gy2 + 22} L190,{gy2 + 50} L190,{gy2 + 122} L50,{gy2 + 122} Z" '
             f'fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="174" y="{gy2 + 68}" width="16" height="54" fill="#FBF6EC" stroke="none"/>')
    s.append(f'<rect x="174" y="{gy2 + 68}" width="16" height="54" fill="none" stroke="{SEAL}" stroke-width="0.6" stroke-dasharray="2 2"/>')
    s.append(f'<path d="M106,{gy2 + 66} L122,{gy2 + 66} L119,{gy2 + 58} L109,{gy2 + 58} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="114" cy="{gy2 + 62}" r="3" fill="{SEAL}" stroke="none" opacity="0.7"/>')
    for px in (76, 150):
        s.append(f'<circle cx="{px}" cy="{gy2 + 74}" r="4.6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        s.append(box(px - 4.5, gy2 + 79, 9, 18, fill="#EFE6D4", stroke=INK))
        s.append(f'<line x1="{px - 2}" y1="{gy2 + 97}" x2="{px - 3}" y2="{gy2 + 114}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{px + 2}" y1="{gy2 + 97}" x2="{px + 3}" y2="{gy2 + 114}" stroke="{INK}" stroke-width="1"/>')
    # 门外的人影
    s.append(f'<path d="M206,{gy2 + 122} L206,{gy2 + 88} Q206,{gy2 + 76} 214,{gy2 + 74} Q222,{gy2 + 76} 222,{gy2 + 88} L222,{gy2 + 122}" '
             f'fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(f'<circle cx="214" cy="{gy2 + 66}" r="6" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(214, gy2 + 136, "门外", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 156, "哭不是为打赢，是为存亡：门里的人还活着", 4.6, GREEN, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "申包胥立依于庭墙而哭，日夜不绝声，七日不入口：秦哀公因此出兵。", 4.8, INK))
    s.append(txt(24, a + 16, "哀兵必胜把老子说反了：哀不是憋着一口气，是不忍。", 4.8, INK))
    s.append(txt(24, a + 34, "怒是气往外烧，哀是把眼睛留在那个还活着的人身上。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "哀者，闵也；闵者，吊者在门。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "不是悲愤的一方胜，是还肯站在门口的一方胜。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch69c"))
    s.append('</svg>')
    return "\n".join(s)


def ch70a_yi_dao_ke_xian():
    W, H = 380, 676
    body, y = head(W, H, "鼎上划一道线，长短不齐的东西都拿来比；它不是道理，是尺子",
                   "第 七 十 章 · 则", "一道刻线", "知我者希，则我者贵。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「则」，《说文》「等画物也」，金文从鼎从刀——在鼎上划一道线，用来把东西比齐。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "比齐的不是东西，是那道刻痕；把我当成它，才叫「则我」。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、比齐：长短不齐的木，对着同一道线", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="134" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 鼎
    cx, cy = 92, gy + 30
    s.append(f'<path d="M{cx - 28},{cy} L{cx + 28},{cy} L{cx + 25},{cy + 38} L{cx - 25},{cy + 38} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for ex in (cx - 20, cx + 20):
        s.append(f'<path d="M{ex - 5},{cy} L{ex - 5},{cy - 7} L{ex + 5},{cy - 7} L{ex + 5},{cy}" fill="none" stroke="{INK}" stroke-width="1"/>')
    for lx, ldx in ((cx - 17, -5), (cx, 0), (cx + 17, 5)):
        s.append(f'<line x1="{lx}" y1="{cy + 38}" x2="{lx + ldx}" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(cx, cy + 32, "鼎", 4.4, "#6E6459", "middle"))
    # 刻线：自鼎腹划出，向右延伸
    s.append(f'<line x1="{cx - 22}" y1="{cy + 14}" x2="330" y2="{cy + 14}" stroke="{SEAL}" stroke-width="1.6"/>')
    s.append(txt(330, cy + 9, "则", 4.8, SEAL, "end"))
    # 三根长短不齐的木，各引虚线到同一道线
    for rx, top in ((168, cy + 40), (218, cy + 58), (268, cy + 78)):
        s.append(box(rx, top, 13, gy + 128 - top, fill="#EFE6D4", stroke=INK))
        s.append(f'<line x1="{rx + 6.5}" y1="{top - 2}" x2="{rx + 6.5}" y2="{cy + 14}" stroke="{GREEN}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="34" y1="{gy + 128}" x2="346" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 148, "线不评价长短：它只把长短显出来，比齐了，谁长谁短自己看见", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 168, "二、一垂一刻：天上那道，刻到鼎上这道", 4.8, SEAL))
    gy2 = gy + 180
    s.append(f'<rect x="26" y="{gy2}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 天垂象
    s.append(f'<path d="M52,{gy2 + 44} Q190,{gy2 + 8} 328,{gy2 + 44}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(58, gy2 + 38, "天", 4.6, "#6E6459", "middle"))
    for dx in (152, 190, 228):
        s.append(f'<line x1="{dx}" y1="{gy2 + 26}" x2="{dx}" y2="{gy2 + 48}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(190, gy2 + 20, "垂 象", 4.2, SEAL, "middle"))
    # 鼎与刻线
    cx2, cy2 = 190, gy2 + 66
    s.append(f'<path d="M{cx2 - 26},{cy2} L{cx2 + 26},{cy2} L{cx2 + 23},{cy2 + 34} L{cx2 - 23},{cy2 + 34} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for ex in (cx2 - 18, cx2 + 18):
        s.append(f'<path d="M{ex - 5},{cy2} L{ex - 5},{cy2 - 7} L{ex + 5},{cy2 - 7} L{ex + 5},{cy2}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="60" y1="{gy2 + 122}" x2="320" y2="{gy2 + 122}" stroke="{INK}" stroke-width="1"/>')
    for lx, ldx in ((cx2 - 15, -5), (cx2, 0), (cx2 + 15, 5)):
        s.append(f'<line x1="{lx}" y1="{cy2 + 34}" x2="{lx + ldx}" y2="{gy2 + 122}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx2 - 20}" y1="{cy2 + 13}" x2="{cx2 + 20}" y2="{cy2 + 13}" stroke="{SEAL}" stroke-width="1.6"/>')
    s.append(arrow(190, gy2 + 50, 190, gy2 + 62, GREEN, 1.0, head="arr2"))
    s.append(txt(200, gy2 + 58, "刻", 4.0, GREEN))
    s.append(txt(292, cy2 + 16, "圣人则之", 4.2, GREEN, "middle"))
    s.append(txt(190, gy2 + 156, "天先垂了一道，圣人把它刻下来：一垂一刻，是同一个动作的两半", 4.6, GREEN, "middle"))

    a = gy2 + 172
    s.append(txt(24, a, "则不是效仿。效仿是照着做，则是在自己这口鼎上划同一道线。", 4.8, INK))
    s.append(txt(24, a + 16, "线一划下，长短就显出来；人一站上去，自己就知道差在哪。", 4.8, INK))
    s.append(txt(24, a + 34, "故曰「则我者贵」：贵不在人多，在那道线被当真过。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "则不评价，只显出来；天垂一道，人刻一道。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "把我当成那道刻线：不是学我，是拿我比。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch70a"))
    s.append('</svg>')
    return "\n".join(s)


def ch70b_yi_jian_ma_yi():
    W, H = 380, 692
    body, y = head(W, H, "褐是贱者之服；披上它不是穷，是不打算靠这个说话",
                   "第 七 十 章 · 褐", "一件麻衣", "是以圣人被褐而怀玉。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「褐」，《说文》「编枲袜也，一曰粗衣」——麻编的粗衣，贱者的衣裳。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "「被」读为「披」：是穿上去的动作，不是落到身上的境遇。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、褐：麻编的粗衣，面上没有话", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="142" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, top = 148, gy + 24
    # 衣架：横杆在上，衣自杆上垂下
    s.append(f'<line x1="{cx - 46}" y1="{top}" x2="{cx + 46}" y2="{top}" stroke="{INK}" stroke-width="1.1"/>')
    for hx, d in ((cx - 44, 6), (cx + 44, -6)):
        s.append(f'<line x1="{hx}" y1="{top}" x2="{hx + d}" y2="{top + 12}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{top + 10}" stroke="{INK}" stroke-width="1"/>')
    # 麻衣
    s.append(f'<path d="M{cx - 10},{top + 10} L{cx},{top + 24} L{cx + 10},{top + 10} '
             f'L{cx + 19},{top + 18} L{cx + 24},{top + 46} L{cx + 15},{top + 46} '
             f'L{cx + 17},{gy + 112} L{cx - 17},{gy + 112} L{cx - 15},{top + 46} '
             f'L{cx - 24},{top + 46} L{cx - 19},{top + 18} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(5):
        yy = top + 34 + i * 11
        s.append(f'<line x1="{cx - 14}" y1="{yy}" x2="{cx + 14}" y2="{yy}" stroke="#7A6E60" stroke-width="0.5" opacity="0.75"/>')
    for i in range(4):
        yy = top + 40 + i * 13
        s.append(f'<line x1="{cx - 9}" y1="{yy}" x2="{cx - 9}" y2="{yy + 5}" stroke="#7A6E60" stroke-width="0.5" opacity="0.55"/>')
        s.append(f'<line x1="{cx + 9}" y1="{yy}" x2="{cx + 9}" y2="{yy + 5}" stroke="#7A6E60" stroke-width="0.5" opacity="0.55"/>')
    s.append(txt(cx + 40, top + 30, "褐：编枲，", 4.4, GREEN))
    s.append(txt(cx + 40, top + 42, "贱者之服", 4.4, GREEN))
    s.append(txt(cx + 40, top + 62, "面上没有话", 4.4, "#6E6459"))
    s.append(txt(190, gy + 156, "麻衣不亮，也不拦：它只是让人看不出他带着什么", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 176, "二、被：主动披上，不是穷得只剩这件", 4.8, SEAL))
    gy2 = gy + 188
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 左：锦袍挂在架上
    s.append(f'<line x1="60" y1="{gy2 + 30}" x2="132" y2="{gy2 + 30}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="96" y1="{gy2 + 30}" x2="96" y2="{gy2 + 36}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M86,{gy2 + 36} L96,{gy2 + 50} L106,{gy2 + 36} L116,{gy2 + 44} L121,{gy2 + 72} '
             f'L112,{gy2 + 72} L114,{gy2 + 124} L78,{gy2 + 124} L80,{gy2 + 72} L71,{gy2 + 72} L76,{gy2 + 44} Z" '
             f'fill="{SEAL}" fill-opacity="0.14" stroke="{SEAL}" stroke-width="1.1"/>')
    for i in range(3):
        yy = gy2 + 66 + i * 18
        s.append(f'<path d="M84,{yy} q6,-5 12,0 q6,5 12,0" fill="none" stroke="{SEAL}" stroke-width="0.7" opacity="0.8"/>')
    s.append(txt(96, gy2 + 140, "锦：挂出来说话", 4.2, SEAL, "middle"))
    # 中：脱下
    s.append(f'<line x1="126" y1="{gy2 + 62}" x2="158" y2="{gy2 + 84}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="158,{gy2 + 84} 150,{gy2 + 82} 153,{gy2 + 90}" fill="{SEAL}"/>')
    s.append(txt(142, gy2 + 100, "脱下", 4.0, SEAL, "middle"))
    # 右：披麻衣的人
    px = 246
    s.append(f'<circle cx="{px}" cy="{gy2 + 52}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 12},{gy2 + 62} L{px + 12},{gy2 + 62} L{px + 14},{gy2 + 100} L{px - 14},{gy2 + 100} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(4):
        yy = gy2 + 68 + i * 8
        s.append(f'<line x1="{px - 10}" y1="{yy}" x2="{px + 10}" y2="{yy}" stroke="#7A6E60" stroke-width="0.5" opacity="0.7"/>')
    s.append(f'<line x1="{px - 12}" y1="{gy2 + 66}" x2="{px - 20}" y2="{gy2 + 88}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 12}" y1="{gy2 + 66}" x2="{px + 20}" y2="{gy2 + 88}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px - 6}" y1="{gy2 + 100}" x2="{px - 13}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 6}" y1="{gy2 + 100}" x2="{px + 13}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(px, gy2 + 140, "被褐：跟他一样", 4.2, GREEN, "middle"))
    s.append(txt(190, gy2 + 162, "披上麻衣，是不靠衣裳说话；站进同一排，才听得见同一句话", 4.6, GREEN, "middle"))

    a = gy2 + 178
    s.append(txt(24, a, "褐不是穷的记号。穷是只剩这件，被褐是还有别的，故意不穿出来。", 4.8, INK))
    s.append(txt(24, a + 16, "老子那个时代，多得是只做到前半句的人：一身麻衣，走得很响。", 4.8, INK))
    s.append(txt(24, a + 34, "所以下一句才要紧：衣是贱者的，怀里那块是贵者的。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "褐是贱者之服，被是主动披上。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "外面一样，是「跟他们一样」；不一样的那一点，揣着。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch70b"))
    s.append('</svg>')
    return "\n".join(s)


def ch70c_yi_kuai_hui_yu():
    W, H = 380, 692
    body, y = head(W, H, "玉挂出来是装饰，揣在怀里是信物：一个给人看，一个给人用",
                   "第 七 十 章 · 玉", "一块揣着的玉", "是以圣人被褐而怀玉。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "玉不是装饰。挂着，是让人看见；揣着，是带着一件要来办的事。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "同一块玉，位置一换，意思就换：佩是招牌，怀是凭证。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、佩：挂在人前，先被看见，再被估价", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="142" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 佩：钩、绳、玉
    s.append(f'<line x1="152" y1="{gy + 24}" x2="228" y2="{gy + 24}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M172,{gy + 24} L190,{gy + 44} L208,{gy + 24}" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<line x1="190" y1="{gy + 44}" x2="190" y2="{gy + 54}" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<path d="M190,{gy + 54} L197,{gy + 60} L190,{gy + 78} L183,{gy + 60} Z" '
             f'fill="{GREEN}" fill-opacity="0.35" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<line x1="183" y1="{gy + 62}" x2="197" y2="{gy + 62}" stroke="{GREEN}" stroke-width="0.6" opacity="0.8"/>')
    # 三道目光
    for (ax, ay, bx, by_) in ((96, gy + 54, 178, gy + 64), (284, gy + 54, 202, gy + 64), (190, gy + 112, 190, gy + 84)):
        s.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by_}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="4 3"/>')
        s.append(f'<polygon points="{bx},{by_} {bx - 7},{by_ - 3} {bx - 3},{by_ + 6}" fill="{SEAL}"/>')
    for hx, hy in ((88, gy + 44), (292, gy + 44), (190, gy + 124)):
        s.append(f'<circle cx="{hx}" cy="{hy}" r="6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(190, gy + 140, "佩：挂着的是招牌，人先看见它，再给你定价", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 160, "二、怀：揣在衣襟里，外面看不出，里面是一件要来办的事", 4.8, SEAL))
    gy2 = gy + 172
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px = 170
    s.append(f'<circle cx="{px}" cy="{gy2 + 40}" r="8" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 14},{gy2 + 50} L{px + 14},{gy2 + 50} L{px + 16},{gy2 + 100} L{px - 16},{gy2 + 100} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    # 衣襟：一道斜开口
    s.append(f'<path d="M{px - 6},{gy2 + 50} Q{px + 6},{gy2 + 68} {px + 4},{gy2 + 98}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # 怀里那块玉：虚线勾出，藏在襟口内
    s.append(f'<path d="M{px - 5},{gy2 + 72} L{px + 2},{gy2 + 78} L{px - 5},{gy2 + 94} L{px - 12},{gy2 + 78} Z" '
             f'fill="{GREEN}" fill-opacity="0.22" stroke="{GREEN}" stroke-width="1" stroke-dasharray="2 2"/>')
    # 手：自肩而下，掌按在襟上
    s.append(f'<path d="M{px + 15},{gy2 + 56} Q{px + 21},{gy2 + 72} {px + 13},{gy2 + 78}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px + 13},{gy2 + 78} Q{px + 9},{gy2 + 82} {px + 4},{gy2 + 80}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M{px + 13},{gy2 + 78} Q{px + 10},{gy2 + 86} {px + 5},{gy2 + 86}" fill="none" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="{px - 6}" y1="{gy2 + 100}" x2="{px - 14}" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 6}" y1="{gy2 + 100}" x2="{px + 14}" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(px + 44, gy2 + 66, "怀：带着一件", 4.4, GREEN))
    s.append(txt(px + 44, gy2 + 78, "要来办的事", 4.4, GREEN))
    s.append(txt(px + 44, gy2 + 96, "外头看不出", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 162, "同一块玉，一换位置就换了意思：挂着是招牌，揣着是凭证", 4.6, GREEN, "middle"))

    a = gy2 + 178
    s.append(txt(24, a, "佩玉的人，走到哪儿都在报自己的价；怀玉的人，走到哪儿都在等那件事。", 4.8, INK))
    s.append(txt(24, a + 16, "老子说「不贵难得之货」——不是嫌玉，是不把玉挂出去当话使。", 4.8, INK))
    s.append(txt(24, a + 34, "所以末句是三层：麻衣是壳，玉是里子，揣是那个「我来有事」。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "玉挂出来是装饰，揣在怀里是信物。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "被褐是我跟你一样，怀玉是我不一样的那一点。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch70c"))
    s.append('</svg>')
    return "\n".join(s)

def ch71a_yi_zhi_jian():
    W, H = 380, 708
    body, y = head(W, H, "知从矢从口：箭出而中，报之于口；箭还在弦上，不叫知",
                   "第 七 十 一 章 · 知", "一支箭", "知不知，尚矣；不知知，病也。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「知」从矢从口：矢是箭，口是报靶的那个口——射中了，喊一声，才叫知。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "所以知是「命中」这件事，不是一个揣在胸里的「有」。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、未出弦：箭在手，靶还没验", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy = gy + 66
    # 弓
    s.append(f'<path d="M78,{cy - 38} Q110,{cy} 78,{cy + 38}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="78" y1="{cy - 38}" x2="78" y2="{cy + 38}" stroke="{INK}" stroke-width="0.9" opacity="0.85"/>')
    # 箭在弦上
    s.append(f'<line x1="60" y1="{cy}" x2="158" y2="{cy}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<polygon points="158,{cy} 148,{cy - 4} 148,{cy + 4}" fill="{INK}"/>')
    for fx in (64, 70):
        s.append(f'<line x1="{fx}" y1="{cy - 6}" x2="{fx + 6}" y2="{cy}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx}" y1="{cy + 6}" x2="{fx + 6}" y2="{cy}" stroke="{INK}" stroke-width="0.8"/>')
    # 远处的靶（虚线，还没验）
    s.append(f'<circle cx="290" cy="{cy}" r="16" fill="none" stroke="#B9A98F" stroke-width="0.9" stroke-dasharray="3 3"/>')
    s.append(f'<circle cx="290" cy="{cy}" r="7" fill="none" stroke="#B9A98F" stroke-width="0.7" stroke-dasharray="3 3"/>')
    s.append(txt(290, cy + 30, "靶还在远处", 4.2, "#6E6459", "middle"))
    s.append(txt(118, cy - 14, "箭搭在弦上", 4.4, SEAL))
    s.append(txt(190, gy + 156, "没射出去的，是打算，不是知：靶还没说话", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 178, "二、已出弦：箭在靶上，这一下才叫知", 4.8, SEAL))
    gy2 = gy + 190
    s.append(f'<rect x="26" y="{gy2}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cy2 = gy2 + 68
    # 松了的弓
    s.append(f'<path d="M72,{cy2 - 34} Q104,{cy2} 72,{cy2 + 34}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="72" y1="{cy2 - 34}" x2="72" y2="{cy2 + 34}" stroke="{INK}" stroke-width="0.9" opacity="0.85"/>')
    s.append(txt(84, cy2 + 34, "弦松了", 4.2, "#6E6459"))
    # 靶
    tx = 264
    s.append(f'<circle cx="{tx}" cy="{cy2}" r="26" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="{tx}" cy="{cy2}" r="17" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{tx}" cy="{cy2}" r="7" fill="{SEAL}" fill-opacity="0.35" stroke="{SEAL}" stroke-width="0.8"/>')
    # 扎进去的箭
    s.append(f'<line x1="196" y1="{cy2 - 6}" x2="{tx - 4}" y2="{cy2 + 1}" stroke="{INK}" stroke-width="1.3"/>')
    for fx in (202, 208):
        s.append(f'<line x1="{fx}" y1="{cy2 - 12}" x2="{fx + 6}" y2="{cy2 - 6}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx}" y1="{cy2}" x2="{fx + 6}" y2="{cy2 - 6}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(tx, cy2 + 40, "靶", 4.4, INK, "middle"))
    s.append(txt(150, cy2 - 22, "箭出而中", 4.4, SEAL))
    s.append(txt(190, gy2 + 164, "射中了才知道中没中：知是箭与靶碰上的那一下，不是想出来的", 4.6, GREEN, "middle"))

    a = gy2 + 180
    s.append(txt(24, a, "所以「知不知」不是谦虚话：他知道自己这一箭偏了——偏在哪儿，也说得出来。", 4.8, INK))
    s.append(txt(24, a + 16, "而「不知知」是另一回事：箭在靶外，他嘴上说中。", 4.8, INK))
    s.append(txt(24, a + 34, "《说文》「病，疾加也」：疾是小病，病是加重了的——报错靶，是会加重的。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "知从矢从口：箭出去，中了，才报得出口。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "胸中之知不必有靶；矢口之知，先得有一张靶。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch71a"))
    s.append('</svg>')
    return "\n".join(s)


def ch71b_yi_zhang_ba():
    W, H = 380, 714
    body, y = head(W, H, "靶在那儿，不由你说：有环才有落点，没环说什么都不算",
                   "第 七 十 一 章 · 靶", "一张靶", "知不知，尚矣；不知知，病也。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "靶不在你手里：它立在那儿，环纹是它自己带的，箭落在几环由它说。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "这是「知」可验的全部理由——靶一挪，就没有靶了。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、有环：落点由靶说", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="142" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    tx, cy = 176, gy + 62
    s.append(f'<circle cx="{tx}" cy="{cy}" r="40" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="{tx}" cy="{cy}" r="27" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{tx}" cy="{cy}" r="14" fill="#F2EADA" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{tx}" cy="{cy}" r="4.4" fill="{SEAL}" stroke="none"/>')
    s.append(txt(tx + 54, cy - 6, "环是靶自带的", 4.2, "#6E6459"))
    # 箭落在二环外
    s.append(f'<line x1="90" y1="{cy + 34}" x2="{tx - 26}" y2="{cy + 28}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<polygon points="{tx - 26},{cy + 28} {tx - 36},{cy + 22} {tx - 32},{cy + 31}" fill="{INK}"/>')
    for fx in (98, 104):
        s.append(f'<line x1="{fx}" y1="{cy + 28}" x2="{fx + 6}" y2="{cy + 34}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{fx}" y1="{cy + 40}" x2="{fx + 6}" y2="{cy + 34}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(116, cy + 50, "箭在二环外", 4.4, SEAL))
    s.append(f'<line x1="{tx + 44}" y1="{cy}" x2="{tx + 40}" y2="{cy}" stroke="{GREEN}" stroke-width="0.1"/>')
    s.append(txt(190, gy + 158, "靶不动，箭动：中不中，是靶说的，不是射的人说的", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 180, "二、无环：说什么都不算数", 4.8, SEAL))
    gy2 = gy + 192
    s.append(f'<rect x="26" y="{gy2}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    tx2, cy2 = 176, gy2 + 64
    s.append(f'<circle cx="{tx2}" cy="{cy2}" r="40" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="{tx2 - 28}" y1="{cy2 - 28}" x2="{tx2 + 28}" y2="{cy2 + 28}" stroke="{LINE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    s.append(f'<line x1="{tx2 + 28}" y1="{cy2 - 28}" x2="{tx2 - 28}" y2="{cy2 + 28}" stroke="{LINE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    s.append(f'<circle cx="{tx2}" cy="{cy2}" r="41" fill="none" stroke="#B9A98F" stroke-width="0.8"/>')
    # 箭乱落在各处（三支）
    for (ex, ey, hx, hy) in ((tx2 - 20, cy2 - 12, -4, -2), (tx2 + 18, cy2 + 6, 3, 4), (tx2 - 4, cy2 + 24, -1, 5)):
        s.append(f'<line x1="{ex - 34}" y1="{ey - 10}" x2="{ex}" y2="{ey}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<polygon points="{ex},{ey} {ex - 8},{ey - 5} {ex - 7},{ey + 3}" fill="{INK}"/>')
    s.append(txt(tx2 + 54, cy2 - 10, "没有环", 4.4, SEAL))
    s.append(txt(tx2 + 54, cy2 + 4, "落在哪儿都", 4.2, "#6E6459"))
    s.append(txt(tx2 + 54, cy2 + 16, "可以叫「中」", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 164, "环是靶的，不是你画的：环一擦掉，箭就成了自己给自己判的", 4.6, GREEN, "middle"))

    a = gy2 + 180
    s.append(txt(24, a, "所以「知不知」的「不知」，是有靶可对的不知：他知道自己偏了，靶还在。", 4.8, INK))
    s.append(txt(24, a + 16, "而「不知知」先把环擦掉，再说「都在里圈」。", 4.8, INK))
    s.append(txt(24, a + 34, "靶一旦成了随身之物，箭就再也没有偏过——这不是本事，是病。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "靶在彼，不由我说。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "验证的意思是：有一件东西，你说不动它。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch71b"))
    s.append('</svg>')
    return "\n".join(s)


def ch71c_yi_bao_ba():
    W, H = 380, 720
    body, y = head(W, H, "报靶的三种人：不报、照实报、把靶画在箭落的地方",
                   "第 七 十 一 章 · 病", "一个报靶的人", "圣人不病，以其病病。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「病」，《说文》「疾加也」：疾是小病，病是加重了的——报错一次，往后每箭都「中」。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "不报的还没射；照实报的说偏了；报错的，把靶画在箭落的地方。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、照实报：箭在靶外，曰「偏矣」——此为上等", 4.8, GREEN))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="142" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    tx, cy = 232, gy + 58
    s.append(f'<circle cx="{tx}" cy="{cy}" r="32" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="{tx}" cy="{cy}" r="20" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{tx}" cy="{cy}" r="6" fill="{SEAL}" fill-opacity="0.35" stroke="{SEAL}" stroke-width="0.8"/>')
    # 箭落在靶外的地上
    s.append(f'<line x1="124" y1="{gy + 110}" x2="176" y2="{gy + 112}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<polygon points="176,{gy + 112} 166,{gy + 108} 166,{gy + 116}" fill="{INK}"/>')
    s.append(f'<line x1="128" y1="{gy + 106}" x2="134" y2="{gy + 110}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="128" y1="{gy + 114}" x2="134" y2="{gy + 110}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="70" y1="{gy + 118}" x2="330" y2="{gy + 118}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(214, gy + 106, "箭落在靶外", 4.2, GREEN))
    # 报靶人
    px = 84
    s.append(f'<circle cx="{px}" cy="{gy + 62}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 11},{gy + 72} L{px + 11},{gy + 72} L{px + 12},{gy + 104} L{px - 12},{gy + 104} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px - 12}" y1="{gy + 76}" x2="{px - 26}" y2="{gy + 96}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 12}" y1="{gy + 76}" x2="{px + 26}" y2="{gy + 66}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px - 5}" y1="{gy + 104}" x2="{px - 8}" y2="{gy + 118}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 5}" y1="{gy + 104}" x2="{px + 8}" y2="{gy + 118}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(px + 44, gy + 56, "「偏矣」", 5.0, GREEN))
    s.append(txt(190, gy + 158, "他不改靶，只改口：说偏，就是把自己的箭让给靶去判", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 180, "二、报错：把靶套在箭落处，曰「中矣」——此为病", 4.8, SEAL))
    gy2 = gy + 192
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 靶已被提起来，套在箭落处
    ex, ey = 196, gy2 + 52
    s.append(f'<circle cx="{ex}" cy="{ey}" r="30" fill="#FBF6EC" fill-opacity="0.6" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<circle cx="{ex}" cy="{ey}" r="4" fill="{SEAL}" fill-opacity="0.4" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<line x1="{ex - 34}" y1="{ey + 4}" x2="{ex + 4}" y2="{ey}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(ex - 40, ey - 34, "箭", 4.0, INK))
    s.append(txt(ex + 40, ey - 34, "靶被拎过来", 4.2, SEAL))
    # 原来的靶位（虚线空位）
    s.append(f'<circle cx="292" cy="{gy2 + 44}" r="20" fill="none" stroke="#B9A98F" stroke-width="0.8" stroke-dasharray="3 3"/>')
    s.append(txt(292, gy2 + 76, "原位空了", 4.0, "#6E6459", "middle"))
    # 报靶人，双手把靶托在箭落处
    px2 = 120
    s.append(f'<circle cx="{px2}" cy="{gy2 + 52}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px2 - 11},{gy2 + 62} L{px2 + 11},{gy2 + 62} L{px2 + 12},{gy2 + 96} L{px2 - 12},{gy2 + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 + 11}" y1="{gy2 + 66}" x2="{ex - 26}" y2="{ey + 14}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 - 6}" y1="{gy2 + 96}" x2="{px2 - 9}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 + 6}" y1="{gy2 + 96}" x2="{px2 + 9}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(px2 + 6, gy2 + 44, "「中矣」", 5.0, SEAL))
    s.append(txt(190, gy2 + 168, "靶一挪，箭就永远中：此后每一箭都由他这双手判", 4.6, GREEN, "middle"))

    a = gy2 + 184
    s.append(txt(24, a, "第三种最危险，不是因为他撒谎。撒谎的人知道自己撒。", 4.8, INK))
    s.append(txt(24, a + 16, "病是另一种：眼里看见靶外的箭，胸里那支还在靶心——两样都在，他信后者。", 4.8, INK))
    s.append(txt(24, a + 34, "「病病」不是治病，是认病：把「自以为知」当成病来盯，才不染这个病。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "病病者，以之为病也，非治之也，乃认之也。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "先认这一句「我可能报错了」，靶才回得来。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch71c"))
    s.append('</svg>')
    return "\n".join(s)


def ch72a_yi_wei_po_po():
    W, H = 380, 712
    body, y = head(W, H, "威从女从戌：一位坐堂的婆婆，斧备着不用；斧一落下，威就没了",
                   "第 七 十 二 章 · 威", "一位坐堂的婆婆", "民不畏威，则大威至。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「威」，《说文》「姑也」，从女从戌——戌是斧：一个女人，手里备着一把斧。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "她不说话，全家不敢出声：这就是威的原型。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、备而不用：堂上不动，屋里自静", 4.8, GREEN))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 堂：三级台阶
    for i in range(3):
        s.append(f'<rect x="{88 - i * 10}" y="{gy + 106 - i * 8}" width="{110 + i * 20}" height="8" fill="#DED2B8" stroke="{INK}" stroke-width="0.7"/>')
    # 坐者
    cx, top = 148, gy + 56
    s.append(f'<circle cx="{cx}" cy="{top}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx - 12},{top + 10} L{cx + 12},{top + 10} L{cx + 14},{top + 40} L{cx - 14},{top + 40} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(150, gy + 136, "坐堂", 4.2, "#6E6459", "middle"))
    # 斧：备着，拄在堂上
    ax = 212
    s.append(f'<line x1="{ax}" y1="{gy + 116}" x2="{ax}" y2="{gy + 60}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M{ax - 2},{gy + 52} L{ax + 20},{gy + 48} Q{ax + 32},{gy + 62} {ax + 20},{gy + 80} L{ax - 2},{gy + 74} Z" '
             f'fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{ax + 18}" y1="{gy + 50}" x2="{ax + 18}" y2="{gy + 78}" stroke="{INK}" stroke-width="0.6" opacity="0.7"/>')
    s.append(txt(ax + 4, gy + 138, "斧备着", 4.2, SEAL, "middle"))
    # 堂下三人，低头静着
    for px in (238, 268, 298):
        s.append(f'<circle cx="{px}" cy="{gy + 84}" r="5" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<path d="M{px - 8},{gy + 91} L{px + 8},{gy + 91} L{px + 9},{gy + 112} L{px - 9},{gy + 112} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(286, gy + 132, "不出一声", 4.2, "#6E6459", "middle"))
    s.append(f'<line x1="34" y1="{gy + 116}" x2="330" y2="{gy + 116}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 162, "斧没动，声先低：不说话的那位，才让满屋的人不敢出声", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 184, "二、斧一落：就只剩打人，威也就没了", 4.8, SEAL))
    gy2 = gy + 196
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    for i in range(3):
        s.append(f'<rect x="{88 - i * 10}" y="{gy2 + 106 - i * 8}" width="{110 + i * 20}" height="8" fill="#DED2B8" stroke="{INK}" stroke-width="0.7"/>')
    # 站起来、举斧的人
    cx2, top2 = 148, gy2 + 44
    s.append(f'<circle cx="{cx2}" cy="{top2}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx2 - 12},{top2 + 10} L{cx2 + 12},{top2 + 10} L{cx2 + 14},{top2 + 40} L{cx2 - 14},{top2 + 40} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx2 + 12}" y1="{top2 + 14}" x2="{cx2 + 34}" y2="{top2 - 6}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx2 + 34}" y1="{top2 - 6}" x2="{cx2 + 40}" y2="{top2 - 30}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M{cx2 + 38},{top2 - 36} L{cx2 + 58},{top2 - 40} Q{cx2 + 72},{top2 - 24} {cx2 + 58},{top2 - 8} L{cx2 + 38},{top2 - 14} Z" '
             f'fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="1"/>')
    # 台下的人散开、回头
    for px, dx in ((236, -1), (274, 1), (306, 1)):
        s.append(f'<circle cx="{px}" cy="{gy2 + 80}" r="5" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<path d="M{px - 8},{gy2 + 87} L{px + 8},{gy2 + 87} L{px + 9},{gy2 + 108} L{px - 9},{gy2 + 108} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{px + dx * 12}" y1="{gy2 + 92}" x2="{px + dx * 22}" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(arrow(220, gy2 + 62, 232, gy2 + 54, SEAL, 1.0, head="arrS"))
    s.append(f'<line x1="34" y1="{gy2 + 112}" x2="330" y2="{gy2 + 112}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy2 + 168, "斧一落下，屋里就只剩躲与还手：被怕的那位，不再坐得住", 4.6, GREEN, "middle"))

    a = gy2 + 184
    s.append(txt(24, a, "「民不畏威，则大威至」：不是他们要来打，是那个家自己在散。", 4.8, INK))
    s.append(txt(24, a + 16, "威靠的是「我在这儿」这一件事；一动手，就换成「我打得过你」。", 4.8, INK))
    s.append(txt(24, a + 34, "前者不用斧，后者只剩斧——所以威亡在用斧那一年。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "威从女从戌，戌者斧也；斧备而不用，用则威亡。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "坐在那儿不动的那位，才叫威；一动，就只剩打。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch72a"))
    s.append('</svg>')
    return "\n".join(s)


def ch72b_yi_wo_gou():
    W, H = 380, 716
    body, y = head(W, H, "狎是犬可习——熟到贴人；不是屋窄，是没有了距离",
                   "第 七 十 二 章 · 狎", "一窝挤着的狗", "无狎其所居，无厌其所生。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「狎」，《说文》「犬可习也」——狗熟到能贴在人身上，就是狎。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "所以狎不是说屋子小，是说人跟人之间没有一寸距离。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、贴成一窝：屋子不小，都挤在一个角上", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 屋
    s.append(f'<path d="M46,{gy + 42} L176,{gy + 10} L306,{gy + 42} L306,{gy + 122} L46,{gy + 122} Z" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="46" y1="{gy + 122}" x2="330" y2="{gy + 122}" stroke="{INK}" stroke-width="1"/>')
    # 一个人蹲着
    px = 96
    s.append(f'<circle cx="{px}" cy="{gy + 56}" r="6" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 10},{gy + 64} L{px + 10},{gy + 64} L{px + 12},{gy + 96} L{px - 12},{gy + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    # 四只狗挤贴
    for i, (dx, dy) in enumerate(((18, 84), (26, 98), (-4, 94), (12, 110))):
        s.append(f'<ellipse cx="{px + dx}" cy="{gy + dy}" rx="15" ry="8" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<circle cx="{px + dx - 15}" cy="{gy + dy - 5}" r="4.6" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(214, gy + 82, "一窝挤在一角", 4.4, SEAL))
    s.append(txt(214, gy + 94, "屋还空着大半", 4.2, "#6E6459"))
    s.append(txt(190, gy + 166, "房子并没变小：是身与身之间先没了空", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 188, "二、让开一线：狗各归一处，人才住得下", 4.8, GREEN))
    gy2 = gy + 200
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M46,{gy2 + 42} L176,{gy2 + 10} L306,{gy2 + 42} L306,{gy2 + 122} L46,{gy2 + 122} Z" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="46" y1="{gy2 + 122}" x2="330" y2="{gy2 + 122}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="96" cy="{gy2 + 56}" r="6" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M86,{gy2 + 64} L106,{gy2 + 64} L108,{gy2 + 96} L84,{gy2 + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for (dx, dy) in ((64, 96), (104, 104), (154, 96), (128, 110)):
        s.append(f'<ellipse cx="{dx}" cy="{gy2 + dy}" rx="14" ry="7.5" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<circle cx="{dx - 14}" cy="{gy2 + dy - 4}" r="4.4" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(214, gy2 + 82, "各归一处", 4.4, GREEN))
    s.append(txt(214, gy2 + 94, "中间留出一条", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 166, "不狎不是赶走谁，是让每一头都有一处自己的地方", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "「无狎其所居」：住的地方，先得留出一寸不属于任何人的空。", 4.8, INK))
    s.append(txt(24, a + 16, "挤到贴人，看着是亲，其实是没处可退：退无可退，话就不好说。", 4.8, INK))
    s.append(txt(24, a + 34, "所以这一句跟上一句连着：威要有堂上的距离，居要有身间的距离。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "狎者，犬可习也，熟而贴人；非屋之窄，乃无距也。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "让开一寸，人才住得下去。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch72b"))
    s.append('</svg>')
    return "\n".join(s)


def ch72c_yi_gan_cheng():
    W, H = 380, 716
    body, y = head(W, H, "贵从贝，是价钱：自贵是给自己贴价签，自爱是不把自己当货",
                   "第 七 十 二 章 · 贵", "一杆秤", "自知不自见，自爱不自贵。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「贵」，《说文》「物不贱也」，从贝——贵是价钱，不是德性。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "自爱是同一杆秤的另一头：不把自己贱卖。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、自贵：先给自己贴一张价签", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 秤
    pole = 196
    s.append(f'<line x1="{pole}" y1="{gy + 34}" x2="{pole}" y2="{gy + 120}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="{pole - 46}" y1="{gy + 30}" x2="{pole + 52}" y2="{gy + 38}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{pole - 46}" y1="{gy + 30}" x2="{pole - 46}" y2="{gy + 40}" stroke="{INK}" stroke-width="0.8"/>')
    # 秤钩与货
    s.append(f'<path d="M{pole - 46},{gy + 40} q0,6 -6,8 q6,2 6,8" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="{pole - 62}" y="{gy + 56}" width="34" height="30" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(pole - 45, gy + 68, "我", 5.6, INK, "middle"))
    # 价签（大）
    s.append(f'<rect x="{pole + 6}" y="{gy + 52}" width="46" height="26" fill="{SEAL}" fill-opacity="0.16" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(pole + 29, gy + 62, "价签", 4.2, SEAL, "middle"))
    s.append(txt(pole + 29, gy + 72, "很贵", 4.2, SEAL, "middle"))
    s.append(f'<line x1="{pole - 30}" y1="{gy + 56}" x2="{pole + 6}" y2="{gy + 56}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    # 秤砣
    s.append(f'<path d="M{pole + 52},{gy + 34} l8,10 l-16,0 Z" fill="{INK}" fill-opacity="0.4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="60" y1="{gy + 120}" x2="322" y2="{gy + 120}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 166, "货上贴价签，秤就只称价钱：先标了，剩下的都是比价", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 188, "二、自爱：不上秤盘，不把自己当货", 4.8, GREEN))
    gy2 = gy + 200
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="{pole}" y1="{gy2 + 34}" x2="{pole}" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="{pole - 46}" y1="{gy2 + 30}" x2="{pole + 52}" y2="{gy2 + 38}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M{pole - 46},{gy2 + 38} q0,6 -6,8 q6,2 6,8" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M{pole + 52},{gy2 + 34} l8,10 l-16,0 Z" fill="{INK}" fill-opacity="0.4" stroke="{INK}" stroke-width="0.8"/>')
    # 空秤盘
    s.append(f'<path d="M{pole - 62},{gy2 + 54} Q{pole - 46},{gy2 + 66} {pole - 30},{gy2 + 54}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{pole - 62}" y1="{gy2 + 54}" x2="{pole - 46}" y2="{gy2 + 52}" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(f'<line x1="{pole - 30}" y1="{gy2 + 54}" x2="{pole - 46}" y2="{gy2 + 52}" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(pole - 46, gy2 + 74, "空盘", 4.0, "#6E6459", "middle"))
    # 人站在秤旁，手摊开
    px = 108
    s.append(f'<circle cx="{px}" cy="{gy2 + 46}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 12},{gy2 + 56} L{px + 12},{gy2 + 56} L{px + 14},{gy2 + 96} L{px - 14},{gy2 + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 12}" y1="{gy2 + 62}" x2="{px + 26}" y2="{gy2 + 82}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 22}" y1="{gy2 + 82}" x2="{px + 38}" y2="{gy2 + 82}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 22}" y1="{gy2 + 86}" x2="{px + 36}" y2="{gy2 + 86}" stroke="{INK}" stroke-width="0.6" opacity="0.6"/>')
    s.append(txt(px + 2, gy2 + 30, "手摊着，不上秤", 4.2, GREEN))
    s.append(f'<line x1="{px - 5}" y1="{gy2 + 96}" x2="{px - 9}" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 5}" y1="{gy2 + 96}" x2="{px + 9}" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1"/>')

    s.append(f'<line x1="60" y1="{gy2 + 120}" x2="322" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy2 + 166, "自爱不是抬价，是不把自己挂上去：不上盘，就不必被人称", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "自见是把自己摆出来给人看；自知是知道自己在哪儿。", 4.8, INK))
    s.append(txt(24, a + 16, "自贵是贴价签；自爱是惜身。一杆秤，两头的话不一样。", 4.8, INK))
    s.append(txt(24, a + 34, "「去彼取此」：把价签取下，把身子留住。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "自知不自见，自爱不自贵；故去彼取此。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "取的是身子，去的是那张价签。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch72c"))
    s.append('</svg>')
    return "\n".join(s)


def ch73a_yi_gu_qi():
    W, H = 380, 712
    body, y = head(W, H, "勇从力，是一股气；气没有方向，方向由敢给",
                   "第 七 十 三 章 · 勇", "一股气", "勇于敢则杀，勇于不敢则活。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「勇」，《说文》「气也」，从力；「敢」，「进取也」——气是力气，敢是往前拿。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "同一股气：冲出去叫勇于敢，按住不放叫勇于不敢。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、气本身：没有方向，四下都吹", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, cy = 150, gy + 66
    # 人
    s.append(f'<circle cx="{cx}" cy="{gy + 32}" r="8" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx - 14},{gy + 44} L{cx + 14},{gy + 44} L{cx + 16},{gy + 92} L{cx - 16},{gy + 92} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx - 7}" y1="{gy + 92}" x2="{cx - 11}" y2="{gy + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{cx + 7}" y1="{gy + 92}" x2="{cx + 11}" y2="{gy + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="0.8"/>')
    # 四下吹的气
    for deg, ln in ((-150, 46), (-90, 40), (-30, 46), (150, 40), (30, 40), (90, 44)):
        import math
        dx = math.cos(math.radians(deg)) * ln
        dy = math.sin(math.radians(deg)) * ln
        sx, sy2 = cx + dx * 0.34, cy + dy * 0.34
        s.append(f'<path d="M{sx},{sy2} Q{cx + dx * 0.7},{cy + dy * 0.45} {cx + dx},{cy + dy}" fill="none" stroke="{SEAL}" stroke-width="0.9" opacity="0.75"/>')
    s.append(txt(190, gy + 162, "气在胸中，四面都吹：它有力气，没有去处", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 184, "二、同一股气，两个去处：冲出去，或按住", 4.8, GREEN))
    gy2 = gy + 196
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px, py = 106, gy2 + 66
    s.append(f'<circle cx="{px}" cy="{gy2 + 32}" r="8" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 14},{gy2 + 44} L{px + 14},{gy2 + 44} L{px + 16},{gy2 + 92} L{px - 16},{gy2 + 92} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px - 7}" y1="{gy2 + 92}" x2="{px - 11}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 7}" y1="{gy2 + 92}" x2="{px + 11}" y2="{gy2 + 124}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="0.8"/>')
    # 一股冲出去
    s.append(f'<path d="M{px + 6},{py - 6} Q{px + 60},{py - 34} {px + 132},{py - 40}" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<polygon points="{px + 132},{py - 40} {px + 120},{py - 46} {px + 122},{py - 34}" fill="{SEAL}"/>')
    s.append(txt(px + 78, py - 52, "勇于敢：冲出去", 4.3, SEAL))
    # 一股按住：挡板与回卷
    s.append(f'<ellipse cx="{px + 54}" cy="{py + 22}" rx="15" ry="7" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(4):
        s.append(f'<line x1="{px + 42}" y1="{py + 16 + i * 4}" x2="{px + 32}" y2="{py + 16 + i * 4}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<path d="M{px + 6},{py + 10} Q{px + 22},{py + 16} {px + 31},{py + 20}" fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<path d="M{px + 31},{py + 24} Q{px + 20},{py + 34} {px + 12},{py + 30}" fill="none" stroke="{GREEN}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="{px + 14},{py + 30} {px + 24},{py + 26} {px + 22},{py + 34}" fill="{GREEN}"/>')
    s.append(txt(px + 4, py + 50, "勇于不敢：按住，气回旋", 4.3, GREEN))
    s.append(txt(190, gy2 + 166, "按住不比冲出省力：同一股气，只是没有往前拿", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "所以「勇于不敢」四个字，勇字不可省：缩手的人不必费这个力。", 4.8, INK))
    s.append(txt(24, a + 16, "敢是方向：冲出去是一个方向，按住也是一个方向——都用这股气。", 4.8, INK))
    s.append(txt(24, a + 34, "气无方向，向由敢定；按亦须力，按错其处，气则白按。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "勇者，气也，从力甬声；敢者，进取也，从攴。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "气留着，方向自己给；不给方向的气，只是乱撞。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch73a"))
    s.append('</svg>')
    return "\n".join(s)


def ch73b_yi_gen_dai_zi():
    W, H = 380, 728
    body, y = head(W, H, "繟是带缓：松着，衣服照样在；系紧，勒出痕",
                   "第 七 十 三 章 · 繟", "一根松带子", "繟然而善谋。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「繟」，《说文》「带缓也」，从糸——带子系得松。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "松着不掉，紧着就勒；勒的那一处，就是崩的那一处。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、松：带垂着，衣服还在身上", 4.8, GREEN))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="146" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    cx, top = 150, gy + 26
    s.append(f'<path d="M{cx - 26},{top} L{cx + 26},{top} L{cx + 30},{gy + 96} L{cx - 30},{gy + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx - 8},{top} L{cx},{top + 14} L{cx + 8},{top}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # 松带：两道下垂弧
    s.append(f'<path d="M{cx - 27},{gy + 52} Q{cx},{gy + 66} {cx + 27},{gy + 52}" fill="none" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(f'<path d="M{cx - 2},{gy + 58} q4,10 -2,18" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<path d="M{cx + 10},{gy + 57} q5,8 1,16" fill="none" stroke="{SEAL}" stroke-width="1.1" opacity="0.8"/>')
    s.append(txt(cx + 58, gy + 58, "带缓：" , 4.4, SEAL))
    s.append(txt(cx + 58, gy + 70, "垂着，不掉", 4.4, "#6E6459"))
    s.append(txt(190, gy + 162, "松不是散：衣还在身上，气还在腰里", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 184, "二、紧：带子勒进去，那一处先崩", 4.8, SEAL))
    gy2 = gy + 196
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    p2 = gy2 + 26
    s.append(f'<path d="M{cx - 26},{p2} L{cx + 26},{p2} L{cx + 30},{gy2 + 96} L{cx - 30},{gy2 + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx - 8},{p2} L{cx},{p2 + 14} L{cx + 8},{p2}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # 紧带：直线勒在腰间，两侧压痕
    s.append(f'<line x1="{cx - 27}" y1="{gy2 + 54}" x2="{cx + 27}" y2="{gy2 + 54}" stroke="{SEAL}" stroke-width="1.6"/>')
    for dx in (-27, 27):
        s.append(f'<line x1="{cx + dx}" y1="{gy2 + 48}" x2="{cx + dx}" y2="{gy2 + 62}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<path d="M{cx - 27},{gy2 + 44} q-6,10 0,20" fill="none" stroke="#B9A98F" stroke-width="0.8"/>')
    s.append(f'<path d="M{cx + 27},{gy2 + 44} q6,10 0,20" fill="none" stroke="#B9A98F" stroke-width="0.8"/>')
    s.append(txt(cx + 58, gy2 + 50, "系紧：", 4.4, SEAL))
    s.append(txt(cx + 58, gy2 + 62, "勒出痕", 4.4, "#6E6459"))
    s.append(txt(190, gy2 + 166, "紧处就是崩处：一处勒死，四下都跟着断", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "人之谋也系紧：把每一步都钉住，钉不住的那一步就是全盘。", 4.8, INK))
    s.append(txt(24, a + 16, "天之谋也系松：松而不掉——掉不下来，是因为它不靠一处系着。", 4.8, INK))
    s.append(txt(24, a + 34, "故善谋者，使人不觉其谋：带子松着，衣服自己就在。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "繟者，《说文》曰「带缓也」，从糸——带系之松也。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "松着，是让每一处都留一点回旋的余地。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch73b"))
    s.append('</svg>')
    return "\n".join(s)


def ch73c_yi_zhang_wang():
    W, H = 380, 716
    body, y = head(W, H, "疏是通，不失是不漏：网眼大，但网有方向",
                   "第 七 十 三 章 · 网", "一张通着的网", "天网恢恢，疏而不失。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「疏」，《说文》「通也」，不是稀：网眼大，所以穿得过去。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "而「不失」：该过的过去，不该过的落在网里——网有方向。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、疏：网眼大，不拦一切", 4.8, GREEN))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="148" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    x0, y0, w, h = 76, gy + 26, 216, 96
    for i in range(5):
        xx = x0 + i * (w / 4)
        s.append(f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y0 + h}" stroke="#B9A98F" stroke-width="0.9"/>')
    for j in range(3):
        yy = y0 + j * (h / 2)
        s.append(f'<line x1="{x0}" y1="{yy}" x2="{x0 + w}" y2="{yy}" stroke="#B9A98F" stroke-width="0.9"/>')
    # 一只小东西从网眼穿过
    bx, by = x0 + w * 0.375, y0 + h * 0.5
    s.append(f'<ellipse cx="{bx}" cy="{by}" rx="9" ry="5.5" fill="{GREEN}" fill-opacity="0.25" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(f'<line x1="{bx + 9}" y1="{by}" x2="{bx + 26}" y2="{by - 14}" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<polygon points="{bx + 26},{by - 14} {bx + 16},{by - 12} {bx + 20},{by - 3}" fill="{GREEN}"/>')
    s.append(txt(bx + 34, by + 10, "穿过去", 4.2, GREEN))
    s.append(txt(190, gy + 164, "网眼大得能穿过：疏不是拦，是先让人有路", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 186, "二、不失：过的过去，过界的那一个落在网里", 4.8, SEAL))
    gy2 = gy + 198
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 一张斜罩的网
    s.append(f'<path d="M70,{gy2 + 26} L300,{gy2 + 20} L286,{gy2 + 108} L84,{gy2 + 112} Z" fill="none" stroke="#B9A98F" stroke-width="1.1"/>')
    for i in range(1, 5):
        t = i / 5
        s.append(f'<line x1="{70 + 230 * t}" y1="{gy2 + 26 - 6 * t}" x2="{84 + 202 * t}" y2="{gy2 + 112 - 4 * t}" stroke="#DCCBB0" stroke-width="0.8"/>')
    for j in range(1, 3):
        t2 = j / 3
        s.append(f'<line x1="{70 + 14 * t2}" y1="{gy2 + 26 + 86 * t2}" x2="{300 - 14 * t2}" y2="{gy2 + 20 + 88 * t2}" stroke="#DCCBB0" stroke-width="0.8"/>')
    # 网内一个（过界者）
    s.append(f'<ellipse cx="176" cy="{gy2 + 74}" rx="10" ry="6" fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(176, gy2 + 96, "过者：入网", 4.2, SEAL, "middle"))
    # 网眼穿过的另一个
    s.append(f'<ellipse cx="248" cy="{gy2 + 56}" rx="8" ry="5" fill="{GREEN}" fill-opacity="0.25" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(232, gy2 + 44, "不过者自网眼去", 4.0, GREEN))
    s.append(txt(190, gy2 + 166, "同是一张网：该留的留下，该走的从眼子里走", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "「天网恢恢」：网是大的，不是密的；大才容得下走。", 4.8, INK))
    s.append(txt(24, a + 16, "「疏而不失」：疏的那一半让它通，不失的那一半让它有方向。", 4.8, INK))
    s.append(txt(24, a + 34, "通而不漏，两者兼有，才叫网；只剩一边的，是筛，或者墙。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "疏者，《说文》曰「通也」，非稀也；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "通者必漏，不漏者必不通，而天兼之。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch73c"))
    s.append('</svg>')
    return "\n".join(s)


def ch74a_yi_ge_fan_zi():
    W, H = 380, 720
    body, y = head(W, H, "司从反后：把君这个字翻过来，才是办事的那一位",
                   "第 七 十 四 章 · 司", "一个翻过来的字", "常有司杀者杀。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「司」，《说文》「臣司事于外者，从反后」——后是君；君翻过来，才是司。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "所以「司杀者」不是坐堂的那位，是在外面按规矩办事的那位。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、后：君坐堂上", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="148" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 堂：一块台，简立在台上
    s.append(f'<rect x="66" y="{gy + 112}" width="200" height="9" fill="#DED2B8" stroke="{INK}" stroke-width="0.7"/>')
    s.append(f'<line x1="34" y1="{gy + 121}" x2="330" y2="{gy + 121}" stroke="{INK}" stroke-width="1"/>')
    # 竹简
    s.append(f'<rect x="118" y="{gy + 26}" width="86" height="86" fill="#FBF6EC" stroke="{INK}" stroke-width="1.1" rx="3"/>')
    s.append(f'<line x1="130" y1="{gy + 38}" x2="192" y2="{gy + 38}" stroke="#DCCBB0" stroke-width="0.6"/>')
    s.append(f'<line x1="130" y1="{gy + 100}" x2="192" y2="{gy + 100}" stroke="#DCCBB0" stroke-width="0.6"/>')
    s.append(txt(161, gy + 92, "后", 38, INK, "middle"))
    s.append(txt(161, gy + 138, "君：坐堂发令", 4.4, "#6E6459", "middle"))
    s.append(txt(252, gy + 52, "后：一人持口，", 4.3, "#6E6459"))
    s.append(txt(252, gy + 64, "坐而发令", 4.3, "#6E6459"))
    s.append(txt(190, gy + 164, "君在堂上：他发令，不办事", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 186, "二、司：同一个人翻过来，站到外面办事", 4.8, GREEN))
    gy2 = gy + 198
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 简翻过来
    s.append(f'<rect x="104" y="{gy2 + 22}" width="86" height="86" fill="#FBF6EC" stroke="{INK}" stroke-width="1.1" rx="3"/>')
    s.append(txt(147, gy2 + 88, "司", 40, SEAL, "middle"))
    # 翻的箭头
    s.append(f'<path d="M198,{gy2 + 38} Q222,{gy2 + 60} 200,{gy2 + 88}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="200,{gy2 + 88} 206,{gy2 + 78} 194,{gy2 + 78}" fill="{SEAL}"/>')
    s.append(txt(232, gy2 + 60, "翻过来", 4.3, SEAL))
    # 在外面办事的人
    px = 282
    s.append(f'<circle cx="{px}" cy="{gy2 + 62}" r="6" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 9},{gy2 + 70} L{px + 9},{gy2 + 70} L{px + 10},{gy2 + 100} L{px - 10},{gy2 + 100} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 9}" y1="{gy2 + 74}" x2="{px + 22}" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px - 5}" y1="{gy2 + 100}" x2="{px - 8}" y2="{gy2 + 118}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px + 5}" y1="{gy2 + 100}" x2="{px + 8}" y2="{gy2 + 118}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(px, gy2 + 128, "在外办事", 4.2, GREEN, "middle"))
    s.append(f'<line x1="34" y1="{gy2 + 118}" x2="330" y2="{gy2 + 118}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy2 + 166, "同一个字翻过来，堂上就没人了：发令的变成了办事的", 4.6, GREEN, "middle"))

    a = gy2 + 182
    s.append(txt(24, a, "所以「司杀者」这个称呼本身就排除了坐堂的人：他不是掌生杀的，是按规矩办事的。", 4.8, INK))
    s.append(txt(24, a + 16, "人想「代」他，先得把自己那一面翻过来——翻过来，就不是君了。", 4.8, INK))
    s.append(txt(24, a + 34, "字翻过来，堂就空出来：这才是这一章开头那一问的底。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "司者，《说文》曰「臣司事于外者，从反后」；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "后者，君也——君翻其身，乃为司。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch74a"))
    s.append('</svg>')
    return "\n".join(s)


def ch74b_yi_ba_fu():
    W, H = 380, 722
    body, y = head(W, H, "斫从斤，一击而断：这把斧在匠人手里是「成」，在代班人手里是「断」",
                   "第 七 十 四 章 · 斫", "一把斧", "夫代司杀者杀，是谓代大匠斫。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「斫」，《说文》「击也」，从斤——一下而断，断了就不能复。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "「代」，《说文》「更也」，是换班：替班的人手上没有那把斧的本事。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、匠人：斧落在木上，削出一件东西", 4.8, GREEN))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="148" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 128}" x2="330" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    # 木料
    s.append(f'<rect x="146" y="{gy + 96}" width="154" height="32" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="146" y1="{gy + 96}" x2="300" y2="{gy + 96}" stroke="{INK}" stroke-width="1.4"/>')
    # 削出的一片
    s.append(f'<path d="M196,{gy + 96} Q210,{gy + 84} 228,{gy + 88}" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<path d="M228,{gy + 88} L242,{gy + 94} L228,{gy + 98} Z" fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="0.9"/>')
    # 匠人
    px = 90
    s.append(f'<circle cx="{px}" cy="{gy + 48}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px - 11},{gy + 58} L{px + 11},{gy + 58} L{px + 13},{gy + 96} L{px - 13},{gy + 96} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px - 6}" y1="{gy + 96}" x2="{px - 9}" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 6}" y1="{gy + 96}" x2="{px + 9}" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    # 臂与斧
    s.append(f'<line x1="{px + 11}" y1="{gy + 64}" x2="{px + 48}" y2="{gy + 78}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px + 48}" y1="{gy + 78}" x2="176" y2="{gy + 100}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M176,{gy + 100} L188,{gy + 86} Q198,{gy + 98} 190,{gy + 110} L174,{gy + 106} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(px, gy + 142, "匠人", 4.2, "#6E6459", "middle"))
    s.append(txt(272, gy + 78, "只削一片", 4.3, GREEN))
    s.append(txt(272, gy + 90, "器由此成", 4.3, "#6E6459"))
    s.append(txt(190, gy + 164, "斧在匠人手里，是「成」的工具：他知道这一刀要落多深", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 186, "二、代班的人：同一把斧，一落就断，断不可复", 4.8, SEAL))
    gy2 = gy + 198
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 130}" x2="330" y2="{gy2 + 130}" stroke="{INK}" stroke-width="1"/>')
    # 木断成两截
    s.append(f'<rect x="150" y="{gy2 + 98}" width="72" height="32" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="240" y="{gy2 + 102}" width="72" height="28" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M222,{gy2 + 98} L232,{gy2 + 114} L222,{gy2 + 130}" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<path d="M240,{gy2 + 102} L250,{gy2 + 116} L240,{gy2 + 130}" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(240, gy2 + 144, "断了，接不回去", 4.2, SEAL, "middle"))
    # 代班人：同一把斧高举
    px2 = 92
    s.append(f'<circle cx="{px2}" cy="{gy2 + 44}" r="7" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{px2 - 11},{gy2 + 54} L{px2 + 11},{gy2 + 54} L{px2 + 13},{gy2 + 94} L{px2 - 13},{gy2 + 94} Z" fill="#FBF6EC" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 - 6}" y1="{gy2 + 94}" x2="{px2 - 9}" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 + 6}" y1="{gy2 + 94}" x2="{px2 + 9}" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 + 11}" y1="{gy2 + 60}" x2="{px2 + 34}" y2="{gy2 + 36}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="{px2 + 34}" y1="{gy2 + 36}" x2="{px2 + 46}" y2="{gy2 + 18}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M{px2 + 46},{gy2 + 18} L{px2 + 62},{gy2 + 8} Q{px2 + 70},{gy2 + 22} {px2 + 56},{gy2 + 34} L{px2 + 40},{gy2 + 28} Z" fill="{SEAL}" fill-opacity="0.3" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(px2, gy2 + 144, "代班", 4.2, SEAL, "middle"))
    s.append(txt(276, gy2 + 70, "未观其性", 4.3, SEAL))
    s.append(txt(276, gy2 + 82, "先加其手", 4.3, "#6E6459"))
    s.append(txt(190, gy2 + 168, "梓庆斋七日才敢加手；代班的人，一刀下去就断了", 4.6, GREEN, "middle"))

    a = gy2 + 184
    s.append(txt(24, a, "所差的不在力气，在那七日：先看清楚这木头要成什么，才落斧。", 4.8, INK))
    s.append(txt(24, a + 16, "代班的人没有这七日——他手上没有这把斧的本事，只有这道令。", 4.8, INK))
    s.append(txt(24, a + 34, "所以「代大匠斫」不是夺权，是替班；替班的人，先输在手上。", 5.0, GREEN))

    c = a + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "代者，《说文》曰「更也」，换班也；斫者，击也，从斤。", 5.0, INK, "middle"))
    s.append(txt(190, c + 36, "一下而断，不可复也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 62, "ch74b"))
    s.append('</svg>')
    return "\n".join(s)


def ch74c_yi_zhi_shou():
    W, H = 380, 726
    body, y = head(W, H, "斧断的那一下，账不从天上收，从手上收",
                   "第 七 十 四 章 · 手", "一只被斫的手", "希有不伤其手矣。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「伤其手」——这一章把账算在手上：不是天来罚，是斧自己回头。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "不曰「必伤」，曰「希有不伤」：全书最不留余地的一句。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、斧落偏了：刃回头，落在握斧的手上", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 木
    s.append(f'<rect x="112" y="{gy + 100}" width="140" height="30" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="112" y1="{gy + 100}" x2="252" y2="{gy + 100}" stroke="{INK}" stroke-width="1.4"/>')
    # 柄与刃：柄从手上垂到木面，刃口咬进木里
    s.append(f'<line x1="154" y1="{gy + 46}" x2="152" y2="{gy + 96}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M149,{gy + 88} L166,{gy + 90} L172,{gy + 104} L162,{gy + 113} L145,{gy + 108} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="145" y1="{gy + 108}" x2="162" y2="{gy + 113}" stroke="{INK}" stroke-width="1.2"/>')
    # 握柄的手：掌压住柄，四指扣过来
    s.append(f'<line x1="112" y1="{gy + 46}" x2="134" y2="{gy + 46}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="132" y="{gy + 34}" width="42" height="24" rx="9" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="{142 + i * 11}" y1="{gy + 56}" x2="{141 + i * 11}" y2="{gy + 64}" stroke="{INK}" stroke-width="0.7"/>')
    # 刃返：赭色虚线弧回到手背
    s.append(f'<path d="M152,{gy + 116} Q196,{gy + 116} 188,{gy + 78} Q182,{gy + 56} 164,{gy + 48}" fill="none" stroke="{SEAL}" stroke-width="1.1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="164,{gy + 44} 172,{gy + 52} 160,{gy + 56}" fill="{SEAL}"/>')
    s.append(f'<line x1="148" y1="{gy + 42}" x2="159" y2="{gy + 47}" stroke="{SEAL}" stroke-width="2"/>')
    s.append(txt(200, gy + 80, "刃回头", 4.2, SEAL))
    s.append(txt(190, gy + 168, "砍不准的那一下，斧不认人：哪里近，就回哪里", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 190, "二、账在手上：一道口子，收也收不回去", 4.8, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 一只摊开的手：掌＋四指＋拇指
    s.append(f'<rect x="144" y="{gy2 + 54}" width="58" height="46" rx="7" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(4):
        s.append(f'<rect x="{148 + i * 13}" y="{gy2 + 24}" width="9" height="34" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="140" cy="{gy2 + 66}" rx="15" ry="7" fill="#EFE6D4" stroke="{INK}" stroke-width="1" transform="rotate(-26 140 {gy2 + 66})"/>')
    # 口子：掌上一道斜口
    s.append(f'<line x1="152" y1="{gy2 + 62}" x2="190" y2="{gy2 + 90}" stroke="{SEAL}" stroke-width="1.8"/>')
    s.append(f'<circle cx="161" cy="{gy2 + 70}" r="1.8" fill="{SEAL}"/>')
    s.append(f'<circle cx="182" cy="{gy2 + 84}" r="1.5" fill="{SEAL}"/>')
    s.append(txt(212, gy2 + 60, "这道口子", 4.3, SEAL))
    s.append(txt(212, gy2 + 72, "是自己的账", 4.3, "#6E6459"))
    # 天：远处一道弧，不动手
    s.append(f'<path d="M80,{gy2 + 120} Q190,{gy2 + 102} 300,{gy2 + 120}" fill="none" stroke="#B9A98F" stroke-width="0.9" stroke-dasharray="4 3"/>')
    s.append(txt(190, gy2 + 136, "天不与你争这把斧：它只让斧落在你手上", 4.4, "#6E6459", "middle"))
    s.append(txt(190, gy2 + 170, "伤不在天上记，在手上记：这就是「希有不伤」的分量", 4.6, GREEN, "middle"))

    a = gy2 + 188
    s.append(txt(24, a, "「希」不是「少」，是「稀」；稀者疏也：上一章的疏在天为不漏，这里的疏在人必伤。", 4.8, INK))
    s.append(txt(24, a + 16, "所以这一句不说「必伤」，说「希有不伤」——留的那一点余地，是留给匠人的。", 4.8, INK))
    s.append(txt(24, a + 34, "代班的人没有那七日，斧就先替天把账记在他手上。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "夫代大匠斫者，希有不伤其手矣。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "斧不认人，账认手。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch74c"))
    s.append('</svg>')
    return "\n".join(s)


def ch75a_yi_zhi_kong_wan():
    W, H = 380, 706
    body, y = head(W, H, "同是饿，一个字归天，一个字归人",
                   "第 七 十 五 章 · 飢", "一只空碗", "民之饥，以其上食税之多，是以饥。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "飢，《说文》「饿也」——肚子空；饑，《说文》「谷不熟」——年成不好。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "本章用的是飢：老子不给天灾留位置。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、饑：谷不熟，账在天上", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 田垄
    s.append(f'<line x1="34" y1="{gy + 124}" x2="330" y2="{gy + 124}" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="44" y1="{gy + 104 + i * 7}" x2="160" y2="{gy + 102 + i * 7}" stroke="#DCCBB0" stroke-width="0.7"/>')
    # 一株倒伏的禾：秆子折了，穗空着垂在地上
    s.append(f'<path d="M76,{gy + 122} Q84,{gy + 94} 102,{gy + 92} Q120,{gy + 94} 134,{gy + 120}" stroke="{INK}" stroke-width="1.3" fill="none"/>')
    s.append(f'<line x1="96" y1="{gy + 96}" x2="82" y2="{gy + 84}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="110" y1="{gy + 92}" x2="116" y2="{gy + 78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<ellipse cx="136" cy="{gy + 120}" rx="7" ry="4" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    # 一株立着，穗也是空的
    s.append(f'<line x1="228" y1="{gy + 122}" x2="228" y2="{gy + 52}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="228" y1="{gy + 74}" x2="212" y2="{gy + 64}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="228" y1="{gy + 62}" x2="244" y2="{gy + 52}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M228,{gy + 52} q-6,-14 0,-22 q6,8 0,22" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(272, gy + 62, "饑：谷不熟", 4.4, SEAL))
    s.append(txt(272, gy + 74, "穗是空的", 4.4, "#6E6459"))
    s.append(txt(190, gy + 168, "饑是天灾：年成不好，怨不到人身上", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、飢：肚子空，账在人身上", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 138}" x2="330" y2="{gy2 + 138}" stroke="{INK}" stroke-width="1"/>')
    # 碗：空着
    s.append(f'<path d="M64,{gy2 + 74} Q92,{gy2 + 130} 120,{gy2 + 74}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="62" y1="{gy2 + 74}" x2="122" y2="{gy2 + 74}" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<ellipse cx="92" cy="{gy2 + 74}" rx="30" ry="5" fill="none" stroke="#B9A98F" stroke-width="0.6" stroke-dasharray="2 2"/>')
    s.append(txt(92, gy2 + 120, "碗里什么也没有", 4.3, "#6E6459", "middle"))
    # 斗：满得冒尖
    s.append(f'<path d="M224,{gy2 + 46} L286,{gy2 + 46} L276,{gy2 + 112} L234,{gy2 + 112} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M224,{gy2 + 46} q31,-22 62,0" fill="#DED2B8" stroke="{INK}" stroke-width="1.1"/>')
    for i in range(3):
        s.append(f'<line x1="{228 + i * 4}" y1="{gy2 + 60 + i * 14}" x2="{282 - i * 4}" y2="{gy2 + 60 + i * 14}" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(255, gy2 + 84, "食税之多", 4.3, SEAL, "middle"))
    # 从碗到斗：一只手
    s.append(f'<path d="M126,{gy2 + 96} Q168,{gy2 + 82} 220,{gy2 + 62}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="220,{gy2 + 62} 208,{gy2 + 60} 212,{gy2 + 70}" fill="{SEAL}"/>')
    s.append(txt(166, gy2 + 108, "取之于下", 4.2, SEAL))
    s.append(txt(190, gy2 + 168, "碗是空的，斗是满的：这一空一满，都在人的账上", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "《说文》「飢，饿也」，肚子空；「饑，谷不熟」，年成不好——两个字从来不混。", 4.8, INK))
    s.append(txt(24, a + 16, "老子不说「民之饑」，说「民之飢」：他把天灾这个变量拿掉了。", 4.8, INK))
    s.append(txt(24, a + 34, "天灾不在账上，账上只有人。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "民之饥，以其上食税之多，是以饥。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "饿，不是天给的。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch75a"))
    s.append('</svg>')
    return "\n".join(s)


def ch75b_yi_tiao_he():
    W, H = 380, 742
    body, y = head(W, H, "治本来是水名：治水的要诀是疏，不是堵",
                   "第 七 十 五 章 · 治", "一条河", "民之难治，以其上之有为，是以难治。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "治，《说文》「治，水。出东莱曲城阳丘山，南入海」——它先是一条河的名字。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "由河到治水，由治水到治理：治这个字的核心，不是管，是疏。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、一条河：它自己会走", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M40,{gy + 74} Q120,{gy + 66} 200,{gy + 74} Q280,{gy + 82} 340,{gy + 76}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M40,{gy + 112} Q120,{gy + 104} 200,{gy + 112} Q280,{gy + 120} 340,{gy + 114}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M46,{gy + 93} q18,6 36,0 q18,-6 36,0 q18,6 36,0 q18,-6 36,0 q18,6 36,0 q18,-6 36,0 q18,6 36,0 q18,-6 36,0" fill="none" stroke="{'#4A5C55'}" stroke-width="1"/>')
    s.append(f'<polygon points="332,{gy + 92} 322,{gy + 87} 322,{gy + 97}" fill="{'#4A5C55'}"/>')
    s.append(txt(190, gy + 46, "水在两岸之间，自己往下走", 4.3, "#6E6459", "middle"))
    s.append(txt(190, gy + 164, "治者，水名：一条河不需要人来管它", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 188, "二、筑堤：堵一次，水就找一次缝", 4.8, GREEN))
    gy2 = gy + 200
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 河的两岸
    s.append(f'<path d="M40,{gy2 + 56} Q190,{gy2 + 48} 340,{gy2 + 58}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M40,{gy2 + 116} Q190,{gy2 + 108} 340,{gy2 + 118}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # 水：被拦住，涨起来了
    s.append(f'<path d="M46,{gy2 + 78} q20,6 40,0 q20,-6 40,0 q20,6 40,0 q20,-6 40,0 q20,6 40,0" fill="none" stroke="#4A5C55" stroke-width="1"/>')
    s.append(txt(64, gy2 + 94, "水涨上来了", 4.2, "#4A5C55"))
    # 三道堤：横在河上，一层比一层高
    for i in range(3):
        cx = 108 + i * 66
        s.append(f'<rect x="{cx}" y="{gy2 + 62}" width="13" height="{56 - i * 4}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    # 漫过去：越过堤顶
    s.append(f'<path d="M120,{gy2 + 60} Q134,{gy2 + 34} 152,{gy2 + 52}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="152,{gy2 + 56} 144,{gy2 + 46} 158,{gy2 + 44}" fill="{SEAL}"/>')
    s.append(txt(196, gy2 + 34, "漫过去：乱", 4.2, SEAL))
    # 钻出去：从堤底穿出
    s.append(f'<path d="M178,{gy2 + 118} Q192,{gy2 + 140} 214,{gy2 + 126}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="214,{gy2 + 128} 202,{gy2 + 122} 206,{gy2 + 136}" fill="{SEAL}"/>')
    s.append(txt(196, gy2 + 148, "钻出去：逃", 4.2, SEAL, "middle"))
    s.append(txt(258, gy2 + 84, "一层政令", 4.2, "#6E6459"))
    s.append(txt(258, gy2 + 96, "一道堤", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 168, "堵得越多，水越要找缝：堵出来的难，不叫难治", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "帛书作「民之不治」：不是难，是根本治不了——因为病根就在「治」这个动作上。", 4.8, INK))
    s.append(txt(24, a + 16, "一个治水的人，不会去怪水。", 4.8, INK))
    s.append(txt(24, a + 34, "水没有去处，只有两个反应：要么漫过去，要么从底下钻出去。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "民之难治，以其上之有为，是以难治。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "难治者，堵之所致也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch75b"))
    s.append('</svg>')
    return "\n".join(s)


def ch75c_yi_gan_cheng():
    W, H = 380, 742
    body, y = head(W, H, "两个从贝的字：一个算账，一个算反账",
                   "第 七 十 五 章 · 贤", "一杆秤", "夫唯无以生为者，是贤于贵生。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "厚是加量，贵是抬价：贵从贝，贤也从贝。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "老子用一个从贝的字，比较两种活法——在贝的字根上把账算反了。", 4.7, "#6E6459", "middle"))

    # ---------- 一 ----------
    s.append(txt(24, y + 50, "一、一头堆高，一头空落", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="156" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy + 112}" x2="330" y2="{gy + 112}" stroke="{LINE}" stroke-width="0.8"/>')
    # 秤杆：左沉（堆厚）右翘（空）
    s.append(f'<line x1="72" y1="{gy + 86}" x2="308" y2="{gy + 56}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<polygon points="182,{gy + 68} 192,{gy + 69} 187,{gy + 108}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    # 左盘：盛着往上堆的砝码
    s.append(f'<line x1="72" y1="{gy + 86}" x2="54" y2="{gy + 96}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="72" y1="{gy + 86}" x2="90" y2="{gy + 96}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M52,{gy + 96} Q72,{gy + 118} 92,{gy + 96}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        w = 24 - i * 4
        s.append(f'<rect x="{72 - w / 2}" y="{gy + 96 - i * 10}" width="{w}" height="9" fill="#DED2B8" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(40, gy + 132, "求生之厚：往上堆", 4.2, SEAL))
    # 右盘：空
    s.append(f'<line x1="308" y1="{gy + 56}" x2="292" y2="{gy + 72}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="308" y1="{gy + 56}" x2="324" y2="{gy + 72}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M290,{gy + 72} Q308,{gy + 94} 326,{gy + 72}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(308, gy + 108, "民之飢：空下去", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy + 172, "堆高其一端，空落其另一端：肥与飢，一豕之两头", 4.6, GREEN, "middle"))

    # ---------- 二 ----------
    s.append(txt(24, gy + 196, "二、同一杆秤，反过来称一次", 4.8, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="156" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 116}" x2="330" y2="{gy2 + 116}" stroke="{LINE}" stroke-width="0.8"/>')
    # 秤杆：左沉（空的那头胜）
    s.append(f'<line x1="72" y1="{gy2 + 88}" x2="308" y2="{gy2 + 58}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<polygon points="182,{gy2 + 70} 192,{gy2 + 71} 187,{gy2 + 110}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    # 左盘：空着
    s.append(f'<line x1="72" y1="{gy2 + 88}" x2="54" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="72" y1="{gy2 + 88}" x2="90" y2="{gy2 + 98}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M52,{gy2 + 98} Q72,{gy2 + 120} 92,{gy2 + 98}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(40, gy2 + 138, "无以生为：空着", 4.2, "#4A5C55"))
    # 右盘：一张价签
    s.append(f'<line x1="308" y1="{gy2 + 58}" x2="292" y2="{gy2 + 74}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="308" y1="{gy2 + 58}" x2="324" y2="{gy2 + 74}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M290,{gy2 + 74} Q308,{gy2 + 96} 326,{gy2 + 74}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="296" y="{gy2 + 60}" width="24" height="15" fill="#EFE6D4" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(f'<circle cx="303" cy="{gy2 + 65}" r="1.6" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(308, gy2 + 110, "贵生：给命标价", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 140, "贤：从贝而作「胜」用——空的那头，胜了", 4.4, "#4A5C55", "middle"))
    s.append(txt(190, gy2 + 172, "不反对活，反对把活当成一桩事业", 4.6, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "「无以生为」不是不要活，是不拿「生」当一件事去经营：活着是自然，经营活是项目。", 4.8, INK))
    s.append(txt(24, a + 16, "所以这一句不劝人饿着，也不劝人轻生——它反对的是「厚」，不是「生」。", 4.8, INK))
    s.append(txt(24, a + 34, "于贝之字根上，算了一笔反账。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "夫唯无以生为者，是贤于贵生。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "生者自然也，为生者项目也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch75c"))
    s.append('</svg>')
    return "\n".join(s)


def ch76a_yi_gen_zhi_tiao():
    W, H = 380, 724
    body, y = head(W, H, "柔的失败是变形，强的失败是断",
                   "第 七 十 六 章 · 柔", "一根枝条", "人之生也柔弱，其死也坚强。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "柔，《说文》「木曲直也」——曲者可直，直者可曲。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "柔不是软，是可逆；弱不是无力，是桡——曲而能直。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、被风弯了，风过了它回来", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 132}" x2="330" y2="{gy + 132}" stroke="{INK}" stroke-width="1"/>')
    # 风
    for i in range(3):
        s.append(f'<path d="M40,{gy + 40 + i * 22} q26,-6 52,0" fill="none" stroke="#B9A98F" stroke-width="0.9"/>')
    s.append(f'<polygon points="96,{gy + 40} 84,{gy + 36} 86,{gy + 46}" fill="#B9A98F"/>')
    # 弯着的枝条
    s.append(f'<path d="M136,{gy + 132} Q140,{gy + 96} 168,{gy + 78} Q196,{gy + 62} 206,{gy + 40}" fill="none" stroke="{INK}" stroke-width="1.6"/>')

    s.append(f'<path d="M146,{gy + 108} q-16,-2 -22,-12" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(214, gy + 66, "弯", 4.4, SEAL))
    # 回：虚线回到直立
    s.append(f'<path d="M206,{gy + 40} Q198,{gy + 26} 176,{gy + 28}" fill="none" stroke="#4A5C55" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="176,{gy + 28} 186,{gy + 24} 186,{gy + 34}" fill="#4A5C55"/>')
    s.append(txt(176, gy + 18, "风过了：回来", 4.3, "#4A5C55", "middle"))
    s.append(txt(190, gy + 166, "枝条被风弯，风过了它回来：柔的失败，只是变形", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 190, "二、同一根枝，被折断了", 4.8, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 132}" x2="330" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1"/>')
    # 断枝：根上留着断口，梢落在一边
    s.append(f'<path d="M136,{gy2 + 132} L140,{gy2 + 78}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M140,{gy2 + 78} l-6,-10 l8,-2 l-6,-9" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<path d="M142,{gy2 + 76} Q176,{gy2 + 92} 196,{gy2 + 128}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="196" y1="{gy2 + 128}" x2="214" y2="{gy2 + 130}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(228, gy2 + 96, "断口：", 4.3, SEAL))
    s.append(txt(228, gy2 + 108, "接不回去", 4.3, "#6E6459"))
    s.append(txt(228, gy2 + 128, "梢落在地上", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 166, "同样一个力：弯的回来了，断的回不来", 4.6, GREEN, "middle"))

    a = gy2 + 190
    s.append(txt(24, a, "所以柔非软也，可逆也；弱非无力也，桡也——曲而能直。", 4.8, INK))
    s.append(txt(24, a + 16, "坚强则异：坚者土之刚，硬而不动；强者弓有力，满而将断。", 4.8, INK))
    s.append(txt(24, a + 34, "柔的失败是变形，强的失败是断。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "人之生也柔弱，其死也坚强。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "曲者可直，直者可曲。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch76a"))
    s.append('</svg>')
    return "\n".join(s)


def ch76b_yi_zhang_gong():
    W, H = 380, 726
    body, y = head(W, H, "一张弓最强之时，即其最危之时",
                   "第 七 十 六 章 · 强", "一张弓", "故坚强者死之徒，柔弱者生之徒。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "强者，弓有力：满而将断。满不是力量，是离断点只剩一分。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "弓的用处全在「能回」：回弹是放箭，不回就是崩。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、拉满：两头都顶到极限", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="154" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 弓臂
    s.append(f'<path d="M136,{gy + 28} Q104,{gy + 80} 136,{gy + 132}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    # 弦拉满
    s.append(f'<line x1="136" y1="{gy + 28}" x2="228" y2="{gy + 80}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="136" y1="{gy + 132}" x2="228" y2="{gy + 80}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="228" y1="{gy + 72}" x2="262" y2="{gy + 72}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="262,{gy + 72} 250,{gy + 67} 250,{gy + 77}" fill="{SEAL}"/>')
    s.append(txt(250, gy + 92, "满", 4.6, SEAL, "middle"))
    # 断点：上下弓梢赭色
    s.append(f'<circle cx="136" cy="{gy + 28}" r="3.2" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<circle cx="136" cy="{gy + 132}" r="3.2" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(104, gy + 22, "断点", 4.2, SEAL))
    s.append(txt(104, gy + 146, "断点", 4.2, SEAL))
    s.append(txt(190, gy + 168, "满到极处只有两条路：回弹，或者崩断", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、崩断：落下来的那一下", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="154" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 断了的上梢
    s.append(f'<path d="M136,{gy2 + 66} Q118,{gy2 + 44} 132,{gy2 + 22}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'<path d="M136,{gy2 + 66} Q116,{gy2 + 96} 130,{gy2 + 132}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'<path d="M136,{gy2 + 66} l-8,-4 l3,-8 l-9,-2" fill="none" stroke="{SEAL}" stroke-width="1.4"/>')
    # 弦松垂
    s.append(f'<path d="M132,{gy2 + 22} Q186,{gy2 + 84} 130,{gy2 + 132}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(txt(168, gy2 + 96, "弦松了，箭射不出去", 4.3, "#6E6459"))
    s.append(txt(104, gy2 + 76, "断在这里", 4.2, SEAL))
    s.append(txt(190, gy2 + 168, "一张弓最强之时，即其最危之时", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "弓的用处全在「能回」：弯是力存在库里，回才是力放出去。", 4.8, INK))
    s.append(txt(24, a + 16, "断了的弓，力气一分不少，只是再也回不去了。", 4.8, INK))
    s.append(txt(24, a + 34, "强不是力大，是离断点近。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "故坚强者死之徒，柔弱者生之徒。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "徒者，步行也——两条路，不是一个类。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch76b"))
    s.append('</svg>')
    return "\n".join(s)


def ch76c_yi_ba_fu():
    W, H = 380, 726
    body, y = head(W, H, "折是从斤断艸：斧落下来，草弯，木断",
                   "第 七 十 六 章 · 折", "一把斧", "是以兵强则灭，木强则折。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "折，《说文》「断也，从斤断艸」——这个字画的就是斧落于草。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "帛书作「兵强则不勝」：至强之兵，是一支不能输的兵。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、字：从斤断艸", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 132}" x2="330" y2="{gy + 132}" stroke="{INK}" stroke-width="1"/>')
    # 艸：一丛草，草尖断在地上
    for i in range(4):
        cx = 74 + i * 16
        s.append(f'<path d="M{cx},{gy + 132} q-3,-30 2,-46" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<path d="M{cx + 2},{gy + 86} q6,-4 10,-2" fill="none" stroke="{INK}" stroke-width="1"/>')
    # 断落的草尖
    s.append(f'<path d="M112,{gy + 116} q10,-4 18,-10" fill="none" stroke="#B9A98F" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(150, gy + 124, "断落的草尖", 4.2, "#6E6459"))
    # 斤：横向压下来的斧
    s.append(f'<path d="M112,{gy + 72} L174,{gy + 74} L180,{gy + 86} L118,{gy + 88} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="118" y1="{gy + 88}" x2="180" y2="{gy + 86}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="174" y1="{gy + 74}" x2="240" y2="{gy + 24}" stroke="{INK}" stroke-width="2"/>')
    s.append(txt(196, gy + 100, "斤：斧", 4.3, SEAL))
    s.append(txt(88, gy + 146, "艸：草", 4.3, "#6E6459"))
    s.append(txt(190, gy + 166, "折：斧落下来，断了的那一丛草", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 190, "二、同一个力，落在草上／落在木上", 4.8, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 136}" x2="330" y2="{gy2 + 136}" stroke="{INK}" stroke-width="1"/>')
    # 左：风推草，草弯而不断
    s.append(f'<path d="M40,{gy2 + 70} q26,-8 52,0" fill="none" stroke="#4A5C55" stroke-width="0.9"/>')
    s.append(f'<polygon points="96,{gy2 + 70} 84,{gy2 + 65} 84,{gy2 + 75}" fill="#4A5C55"/>')
    for i in range(4):
        cx = 108 + i * 12
        s.append(f'<path d="M{cx},{gy2 + 136} Q{cx + 8},{gy2 + 104} {cx + 34},{gy2 + 86}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(txt(132, gy2 + 66, "草弯了，没断", 4.3, "#4A5C55", "middle"))
    # 右：木被折断成两截
    s.append(f'<rect x="228" y="{gy2 + 106}" width="52" height="30" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="290" y="{gy2 + 110}" width="40" height="26" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M282,{gy2 + 106} l8,8 l-8,8 l8,8" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
    s.append(txt(282, gy2 + 92, "木断了", 4.3, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "柔者见弯，强者见断：弯可复，断不可复", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "柔的失败是变形——弯了还能直回来；强的失败是断——断口没有第二种可能。", 4.8, INK))
    s.append(txt(24, a + 16, "至强之兵，是不能输的兵：一不能赢，则全输——非败于人也，无第二途也。", 4.8, INK))
    s.append(txt(24, a + 34, "故强大处下，柔弱处上。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "是以兵强则灭，木强则折。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "强者见断，柔者见弯。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch76c"))
    s.append('</svg>')
    return "\n".join(s)


def ch77a_yi_zhang_xian():
    W, H = 380, 726
    body, y = head(W, H, "校准是两个方向的：高则抑，低则举",
                   "第 七 十 七 章 · 张", "一张弦", "天之道，其犹张弓与？", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "张，《说文》「施弓弦也」——不是拉弓，是上弦：把两端调齐。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "拉满者只一个方向；调弦者两个方向：高则下之，低则上之。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、一头高了：抑之", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 水平线（校准的准头）
    s.append(f'<line x1="60" y1="{gy + 78}" x2="320" y2="{gy + 78}" stroke="#B9A98F" stroke-width="0.7" stroke-dasharray="5 3"/>')
    s.append(txt(60, gy + 92, "准头", 4.0, "#B9A98F"))
    # 弓臂：左梢高、右梢低
    s.append(f'<path d="M146,{gy + 50} Q92,{gy + 84} 258,{gy + 96}" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    s.append(f'<line x1="146" y1="{gy + 50}" x2="258" y2="{gy + 96}" stroke="#B9A98F" stroke-width="0.9"/>')
    s.append(f'<circle cx="146" cy="{gy + 50}" r="3" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<circle cx="258" cy="{gy + 96}" r="3" fill="none" stroke="#B9A98F" stroke-width="1"/>')
    s.append(txt(196, gy + 46, "左梢高了：弦是斜的", 4.3, SEAL))
    # 一只手按下
    s.append(f'<path d="M104,{gy + 26} Q122,{gy + 36} 140,{gy + 26}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="{114 + i * 7}" y1="{gy + 28}" x2="{114 + i * 7}" y2="{gy + 20}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="118" y1="{gy + 44}" x2="118" y2="{gy + 34}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(f'<polygon points="118,{gy + 44} 113,{gy + 34} 123,{gy + 34}" fill="{SEAL}"/>')
    s.append(txt(190, gy + 34, "抑：一手按下", 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 116, "抑者，《说文》曰「按也」——一手可矣", 4.4, "#6E6459", "middle"))
    s.append(txt(190, gy + 166, "高者抑之：高处只需一只手按住", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 190, "二、一头低了：举之", 4.8, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="60" y1="{gy2 + 84}" x2="320" y2="{gy2 + 84}" stroke="#B9A98F" stroke-width="0.7" stroke-dasharray="5 3"/>')
    s.append(f'<path d="M146,{gy2 + 56} Q92,{gy2 + 90} 258,{gy2 + 116}" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    s.append(f'<line x1="146" y1="{gy2 + 56}" x2="258" y2="{gy2 + 116}" stroke="#B9A98F" stroke-width="0.9"/>')
    s.append(f'<circle cx="146" cy="{gy2 + 56}" r="3" fill="none" stroke="#B9A98F" stroke-width="1"/>')
    s.append(f'<circle cx="258" cy="{gy2 + 116}" r="3" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(196, gy2 + 72, "右梢低了：弦还是斜的", 4.3, SEAL))
    # 两只手往上托
    s.append(f'<path d="M244,{gy2 + 132} Q262,{gy2 + 142} 280,{gy2 + 132}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M244,{gy2 + 118} Q262,{gy2 + 128} 280,{gy2 + 118}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="262" y1="{gy2 + 110}" x2="262" y2="{gy2 + 98}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(f'<polygon points="262,{gy2 + 94} 257,{gy2 + 104} 267,{gy2 + 104}" fill="{SEAL}"/>')
    s.append(txt(176, gy2 + 146, "举：须两手托", 4.3, SEAL, "middle"))
    s.append(txt(190, gy2 + 166, "举者，《说文》曰「对举也」——必须两只手", 4.6, GREEN, "middle"))

    a = gy2 + 190
    s.append(txt(24, a, "故天道之力，大半费于「举」：损有余易，补不足难。", 4.8, INK))
    s.append(txt(24, a + 16, "抑只需一手按住，举则要两只手托起来——这就是「补」的代价。", 4.8, INK))
    s.append(txt(24, a + 34, "不是加总，是配平。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "高者抑之，下者举之。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "损有余易，补不足难。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch77a"))
    s.append('</svg>')
    return "\n".join(s)


def ch77b_yi_jian_po_yi():
    W, H = 380, 726
    body, y = head(W, H, "补是完衣：缝，不是给",
                   "第 七 十 七 章 · 补", "一件破衣", "有余者损之，不足者补之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "补，《说文》「完衣也」——缝，不是给。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "给者移之，缝者复之：移者变其多寡，复者使其可衣。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、一布两处：一处有余，一处有阙", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 衣：身、两袖、交领
    s.append(f'<rect x="152" y="{gy + 52}" width="76" height="58" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="176" y1="{gy + 52}" x2="190" y2="{gy + 70}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="204" y1="{gy + 52}" x2="190" y2="{gy + 70}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="118" y="{gy + 54}" width="34" height="26" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<rect x="228" y="{gy + 54}" width="34" height="40" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    # 阙：左肩一道口子
    s.append(f'<path d="M150,{gy + 56} l-6,8 l6,6 l-4,8" fill="none" stroke="{SEAL}" stroke-width="1.4"/>')
    s.append(txt(112, gy + 44, "阙：破了", 4.3, SEAL))
    # 余：右袖长出一截
    s.append(f'<rect x="262" y="{gy + 56}" width="22" height="34" rx="2" fill="#DED2B8" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(292, gy + 84, "余：多出一块", 4.2, SEAL))
    s.append(txt(190, gy + 148, "同一块布，两处挂着：不缝，则两处皆废", 4.4, GREEN, "middle"))
    s.append(txt(190, gy + 168, "此天之算术也：非加总也，配平也", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、剪此补彼：一件衣，两处都好", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<rect x="152" y="{gy2 + 52}" width="76" height="58" rx="4" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="176" y1="{gy2 + 52}" x2="190" y2="{gy2 + 70}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="204" y1="{gy2 + 52}" x2="190" y2="{gy2 + 70}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="118" y="{gy2 + 54}" width="34" height="26" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<rect x="228" y="{gy2 + 54}" width="34" height="26" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    # 缝：针脚
    for i in range(5):
        s.append(f'<line x1="{144 + i * 5}" y1="{gy2 + 54}" x2="{140 + i * 5}" y2="{gy2 + 68}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(120, gy2 + 44, "缝上了", 4.3, SEAL))
    # 虚线：那一块布挪过来
    s.append(f'<path d="M262,{gy2 + 70} Q222,{gy2 + 40} 176,{gy2 + 48}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="176,{gy2 + 48} 186,{gy2 + 44} 186,{gy2 + 54}" fill="{SEAL}"/>')
    s.append(txt(272, gy2 + 92, "袖口不再多出", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 148, "一布两处：一处有余，一处有阙；缝之，两处皆可用", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 168, "补不是给它添，是让它重新穿得上", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "有余者，同衣之上多出之布也；一布而两处：一处有余，一处有阙。", 4.8, INK))
    s.append(txt(24, a + 16, "给者移之，移完还是两件破的；缝者复之，复完是一件可穿的。", 4.8, INK))
    s.append(txt(24, a + 34, "此天之算术也：非加总也，配平也。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "有余者损之，不足者补之。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "补者，完衣也：缝也，非给也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch77b"))
    s.append('</svg>')
    return "\n".join(s)


def ch77c_liang_zhi_shou():
    W, H = 380, 726
    body, y = head(W, H, "人之道：自空碗里刮其余，捧献于满碗",
                   "第 七 十 七 章 · 奉", "两只捧起的手", "人之道则不然，损不足以奉有余。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "奉，《说文》「承也」，从手从廾——两手捧而献之。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "其象非被夺也，乃自空碗中刮其余，捧而献于满碗。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、人之道：从空的那只刮", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 130}" x2="330" y2="{gy + 130}" stroke="{INK}" stroke-width="1"/>')
    # 空碗
    s.append(f'<path d="M56,{gy + 82} Q78,{gy + 126} 100,{gy + 82}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="54" y1="{gy + 82}" x2="102" y2="{gy + 82}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(78, gy + 144, "不足", 4.3, "#6E6459", "middle"))
    # 满碗
    s.append(f'<path d="M262,{gy + 64} Q288,{gy + 116} 314,{gy + 64}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="258" y1="{gy + 64}" x2="318" y2="{gy + 64}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M258,{gy + 64} q30,-14 60,0" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(288, gy + 144, "有余", 4.3, SEAL, "middle"))
    # 两只手：从空碗刮起，捧向满碗
    s.append(f'<path d="M98,{gy + 52} Q118,{gy + 66} 138,{gy + 52}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="{108 + i * 9}" y1="{gy + 54}" x2="{107 + i * 9}" y2="{gy + 44}" stroke="{INK}" stroke-width="0.8"/>')

    s.append(f'<path d="M140,{gy + 52} Q200,{gy + 26} 258,{gy + 46}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="258,{gy + 46} 246,{gy + 42} 248,{gy + 52}" fill="{SEAL}"/>')
    s.append(txt(190, gy + 24, "捧而献之", 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 166, "夺者含恨，献者含敬；而最冷者，献者自愿也", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 190, "二、唯有道者：倒过来捧", 4.8, GREEN))
    gy2 = gy + 202
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 130}" x2="330" y2="{gy2 + 130}" stroke="{INK}" stroke-width="1"/>')
    # 满碗（源）
    s.append(f'<path d="M56,{gy2 + 64} Q82,{gy2 + 116} 108,{gy2 + 64}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="52" y1="{gy2 + 64}" x2="112" y2="{gy2 + 64}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M52,{gy2 + 64} q30,-14 60,0" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(82, gy2 + 144, "有余", 4.3, SEAL, "middle"))
    # 空碗（受）
    s.append(f'<path d="M262,{gy2 + 82} Q288,{gy2 + 126} 314,{gy2 + 82}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="260" y1="{gy2 + 82}" x2="316" y2="{gy2 + 82}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(288, gy2 + 144, "不足", 4.3, "#6E6459", "middle"))
    s.append(f'<path d="M120,{gy2 + 48} Q200,{gy2 + 26} 260,{gy2 + 62}" fill="none" stroke="#4A5C55" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<polygon points="260,{gy2 + 62} 248,{gy2 + 58} 250,{gy2 + 68}" fill="#4A5C55"/>')
    s.append(f'<path d="M178,{gy2 + 38} Q200,{gy2 + 54} 222,{gy2 + 38}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<line x1="{187 + i * 8}" y1="{gy2 + 40}" x2="{186 + i * 8}" y2="{gy2 + 30}" stroke="{INK}" stroke-width="0.8"/>')

    s.append(txt(196, gy2 + 26, "有余以奉天下", 4.3, "#4A5C55", "middle"))
    s.append(txt(190, gy2 + 166, "孰能有余以奉天下？唯有道者", 4.6, GREEN, "middle"))

    a = gy2 + 190
    s.append(txt(24, a, "人之道非「有人夺我」，乃「令被夺者自捧而献，且以为当然」。", 4.8, INK))
    s.append(txt(24, a + 16, "同一双手，两个方向：向上献，是人之道；向下倒，是道者。", 4.8, INK))
    s.append(txt(24, a + 34, "不欲见贤者，不欲使人见其所有余也。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "人之道则不然，损不足以奉有余。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "奉者，承也：两手捧而献之。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch77c"))
    s.append('</svg>')
    return "\n".join(s)


def ch78a_yi_zhi_qi():
    W, H = 380, 744
    body, y = head(W, H, "器可以换，水不倒：形易万次，体未尝一易",
                   "第 七 十 八 章 · 易", "一只器", "以其无以易之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "易，《说文》曰「蜥蜴」，一说象两器倾水之形。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "倾水者非变也，移也：自此器倒之彼器——器换了，水还是那水。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、倒过来：器换了，水没换", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 132}" x2="330" y2="{gy + 132}" stroke="{INK}" stroke-width="1"/>')
    # 左器：矮口陶罐（倾斜）
    s.append(f'<path d="M96,{gy + 62} Q74,{gy + 104} 96,{gy + 128}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M96,{gy + 62} L130,{gy + 50} Q146,{gy + 92} 130,{gy + 118} L96,{gy + 128}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="96" y1="{gy + 62}" x2="130" y2="{gy + 50}" stroke="{INK}" stroke-width="1.2"/>')
    # 水：从罐口倾出
    s.append(f'<path d="M132,{gy + 56} Q170,{gy + 70} 206,{gy + 64}" fill="none" stroke="#4A5C55" stroke-width="2"/>')
    s.append(f'<path d="M206,{gy + 64} Q214,{gy + 84} 214,{gy + 104}" fill="none" stroke="#4A5C55" stroke-width="2"/>')
    s.append(txt(150, gy + 46, "水在倒", 4.3, "#4A5C55"))
    # 右器：细高瓶（另一个形）
    s.append(f'<path d="M200,{gy + 60} Q186,{gy + 92} 196,{gy + 130}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M232,{gy + 60} Q246,{gy + 92} 236,{gy + 130}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M196,{gy + 130} Q216,{gy + 140} 236,{gy + 130}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="200" y1="{gy + 60}" x2="232" y2="{gy + 60}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(216, gy + 150, "另一只器", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy + 172, "器可易，水不可易：器者形也，水者体也", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 196, "二、都破了：水还在那里", 4.8, GREEN))
    gy2 = gy + 208
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 132}" x2="330" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1"/>')
    # 碎了的陶片
    s.append(f'<path d="M66,{gy2 + 128} l14,-16 l12,6 l-2,10 Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M100,{gy2 + 130} l10,-18 l14,10 l-6,8 Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M124,{gy2 + 118} l6,-14 l10,8 Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(96, gy2 + 100, "器碎了", 4.2, SEAL))
    # 地上那滩水：形状随地
    s.append(f'<path d="M150,{gy2 + 132} Q196,{gy2 + 112} 250,{gy2 + 132} Q200,{gy2 + 142} 150,{gy2 + 132} Z" fill="#4A5C55" fill-opacity="0.25" stroke="#4A5C55" stroke-width="1"/>')
    s.append(txt(200, gy2 + 96, "还是那滩水", 4.3, "#4A5C55", "middle"))
    s.append(txt(190, gy2 + 172, "形易万次，体未尝一易", 4.6, GREEN, "middle"))

    a = gy2 + 196
    s.append(txt(24, a, "故「无以易之」者，非不可变也，乃不可倒也。", 4.8, INK))
    s.append(txt(24, a + 16, "器一次就碎，水一次也不倒：这就是「莫之能胜」的意思。", 4.8, INK))
    s.append(txt(24, a + 34, "弱者非无力，是不可倒。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。", 5.0, INK, "middle"))
    s.append(txt(190, c + 36, "器可易，水不可易。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch78a"))
    s.append('</svg>')
    return "\n".join(s)


def ch78b_yi_peng_tu():
    W, H = 380, 726
    body, y = head(W, H, "受垢者三步：接之、沉之、复清之",
                   "第 七 十 八 章 · 垢", "一捧土", "受国之垢，是谓社稷主。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "垢，《说文》「浊也」，从土——垢即土也。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "水土相遇则浑，静则土沉，土沉则水清。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、接住：一捧土落进水里", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 134}" x2="330" y2="{gy + 134}" stroke="{INK}" stroke-width="1"/>')
    # 杯
    s.append(f'<path d="M148,{gy + 56} Q148,{gy + 122} 190,{gy + 126} Q232,{gy + 122} 232,{gy + 56}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="148" y1="{gy + 56}" x2="232" y2="{gy + 56}" stroke="{INK}" stroke-width="1.3"/>')
    # 浑水
    s.append(f'<path d="M150,{gy + 58} L230,{gy + 58} L228,{gy + 100} Q190,{gy + 110} 152,{gy + 100} Z" fill="#4A5C55" fill-opacity="0.3" stroke="#4A5C55" stroke-width="0.7"/>')
    # 一捧土：从上方撒下
    s.append(f'<path d="M150,{gy + 18} Q190,{gy + 38} 230,{gy + 18}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    for i in range(4):
        s.append(f'<circle cx="{162 + i * 20}" cy="{gy + 46 + (i % 2) * 6}" r="1.6" fill="#B9A98F"/>')
        s.append(f'<circle cx="{168 + i * 18}" cy="{gy + 56 + (i % 2) * 5}" r="1.4" fill="#B9A98F"/>')
    s.append(txt(196, gy + 10, "土落下来", 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 168, "接住：土落进来，水不拒——拒的，就不是受", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、沉之，复清之", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 134}" x2="330" y2="{gy2 + 134}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M148,{gy2 + 56} Q148,{gy2 + 122} 190,{gy2 + 126} Q232,{gy2 + 122} 232,{gy2 + 56}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="148" y1="{gy2 + 56}" x2="232" y2="{gy2 + 56}" stroke="{INK}" stroke-width="1.3"/>')
    # 清水在上
    s.append(f'<path d="M150,{gy2 + 58} L230,{gy2 + 58} L228,{gy2 + 104} Q190,{gy2 + 112} 152,{gy2 + 104} Z" fill="#4A5C55" fill-opacity="0.16" stroke="#4A5C55" stroke-width="0.7"/>')
    # 沉土在下
    s.append(f'<path d="M152,{gy2 + 104} Q190,{gy2 + 112} 228,{gy2 + 104} Q228,{gy2 + 118} 190,{gy2 + 122} Q152,{gy2 + 118} 152,{gy2 + 104} Z" fill="#DED2B8" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(252, gy2 + 74, "上：清", 4.3, "#4A5C55"))
    s.append(txt(252, gy2 + 116, "下：土沉了", 4.3, SEAL))
    s.append(f'<line x1="240" y1="{gy2 + 110}" x2="248" y2="{gy2 + 114}" stroke="#B9A98F" stroke-width="0.7"/>')
    s.append(txt(190, gy2 + 168, "土沉了，水自己就清了：不是吞土，是放土", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "故受垢者三步：接之、沉之、复清之。非吞土也，乃放土也。", 4.8, INK))
    s.append(txt(24, a + 16, "能受者，非力大也，其体不倒也——水不清，是因为它一直在晃。", 4.8, INK))
    s.append(txt(24, a + 34, "垢从土，社亦从土：一污一神，一土之两面。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "受国之垢，是谓社稷主。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "垢者，浊也，从土：垢即土也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch78b"))
    s.append('</svg>')
    return "\n".join(s)


def ch78c_yi_kuai_pai_wei():
    W, H = 380, 726
    body, y = head(W, H, "接过土的，才配当它的主",
                   "第 七 十 八 章 · 社", "一块牌位", "受国不祥，是为天下王。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "社，《说文》「地主也」，从示土——土神也。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "垢从土，社亦从土：一污一神；以污之一面自受，而后为神之一面之主。", 4.4, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、土：先是一捧土", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 134}" x2="330" y2="{gy + 134}" stroke="{INK}" stroke-width="1"/>')
    # 土堆
    s.append(f'<path d="M96,{gy + 134} Q120,{gy + 96} 150,{gy + 92} Q182,{gy + 96} 206,{gy + 134} Z" fill="#DED2B8" stroke="{INK}" stroke-width="1.2"/>')
    for i in range(6):
        s.append(f'<circle cx="{112 + i * 14}" cy="{gy + 120 - (i % 3) * 10}" r="1.3" fill="#B9A98F"/>')
    # 两只手捧起
    s.append(f'<path d="M84,{gy + 112} Q100,{gy + 126} 116,{gy + 112}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M190,{gy + 112} Q206,{gy + 126} 222,{gy + 112}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(2):
        s.append(f'<line x1="{92 + i * 8}" y1="{gy + 114}" x2="{91 + i * 8}" y2="{gy + 106}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{198 + i * 8}" y1="{gy + 114}" x2="{197 + i * 8}" y2="{gy + 106}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(150, gy + 78, "一捧土", 4.4, SEAL, "middle"))
    s.append(txt(252, gy + 104, "垢就是土：", 4.3, SEAL))
    s.append(txt(252, gy + 116, "最脏的那一面", 4.3, "#6E6459"))
    s.append(txt(190, gy + 168, "土是最贱的东西：踩在脚下，也落在衣上", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、同一捧土，立成社主", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 134}" x2="330" y2="{gy2 + 134}" stroke="{INK}" stroke-width="1"/>')
    # 牌位：底座＋竖牌
    s.append(f'<rect x="128" y="{gy2 + 126}" width="64" height="9" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="144" y="{gy2 + 46}" width="32" height="80" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="150" y="{gy2 + 40}" width="20" height="7" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(160, gy2 + 92, "社", 15, SEAL, "middle"))
    # 一抹土色贴在牌上
    s.append(f'<path d="M144,{gy2 + 116} q16,-6 32,0" fill="none" stroke="#B9A98F" stroke-width="1"/>')
    s.append(txt(196, gy2 + 66, "接过土的，", 4.3, SEAL))
    s.append(txt(196, gy2 + 78, "才配当它的主", 4.3, SEAL))
    s.append(txt(190, gy2 + 168, "土神不是另请一位：是把接过的那捧土立起来", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "受垢者不是不脏：是脏过之后还立得住，于是那块土立成了他的位。", 4.8, INK))
    s.append(txt(24, a + 16, "受不祥者，自置于羊之位也：羊在神主之前，先被牵去。", 4.8, INK))
    s.append(txt(24, a + 34, "垢从土，社从土：一污一神，同一块土。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "受国不祥，是为天下王。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "社者，地主也，从示土。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch78c"))
    s.append('</svg>')
    return "\n".join(s)


def ch79a_ban_pian_mu():
    W, H = 380, 728
    body, y = head(W, H, "契剖开了，所以只剩一半；它不响，但它一直在",
                   "第 七 十 九 章 · 契", "半片木", "是以圣人执左契，而不责于人。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "契，刻木为信：一剖两半，债权人执左，负债者执右。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "两半只有并起来才看得出齿；分开时，各自只是一块木。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、一剖两半：齿要对得上", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 两片木，中间剖线
    s.append(f'<rect x="86" y="{gy + 44}" width="46" height="88" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="150" y="{gy + 44}" width="46" height="88" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="134" y1="{gy + 44}" x2="134" y2="{gy + 132}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    for i in range(4):
        yy = gy + 58 + i * 20
        s.append(f'<line x1="132" y1="{yy}" x2="118" y2="{yy}" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<line x1="136" y1="{yy}" x2="150" y2="{yy}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(txt(108, gy + 30, "左契", 4.3, SEAL, "middle"))
    s.append(txt(172, gy + 30, "右契", 4.3, "#6E6459", "middle"))
    s.append(txt(216, gy + 74, "齿对得上，", 4.3, SEAL))
    s.append(txt(216, gy + 86, "才认得出这一份", 4.3, "#6E6459"))
    s.append(txt(190, gy + 168, "剖开过，所以只剩一半：它记得住，是靠那道齿", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、执在手上，但不伸出去", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 134}" x2="330" y2="{gy2 + 134}" stroke="{INK}" stroke-width="1"/>')
    # 人：执左契于胸前
    s.append(f'<circle cx="120" cy="{gy2 + 44}" r="8" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M110,{gy2 + 58} L130,{gy2 + 58} L132,{gy2 + 104} L108,{gy2 + 104} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="110" y1="{gy2 + 104}" x2="108" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="130" y1="{gy2 + 104}" x2="132" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1.2"/>')
    # 那片木，握在手中
    s.append(f'<rect x="122" y="{gy2 + 70}" width="26" height="34" rx="2" fill="#DED2B8" stroke="{INK}" stroke-width="1.1"/>')
    for i in range(3):
        s.append(f'<line x1="122" y1="{gy2 + 76 + i * 9}" x2="134" y2="{gy2 + 76 + i * 9}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(136, gy2 + 66, "左契在手上", 4.2, SEAL))
    # 对面的人（虚影）
    s.append(f'<circle cx="272" cy="{gy2 + 48}" r="7" fill="none" stroke="#B9A98F" stroke-width="1"/>')
    s.append(f'<path d="M264,{gy2 + 60} L280,{gy2 + 60} L282,{gy2 + 100} L262,{gy2 + 100} Z" fill="none" stroke="#B9A98F" stroke-width="1"/>')
    s.append(txt(272, gy2 + 118, "欠他的人", 4.2, "#B9A98F", "middle"))
    # 虚线伸出去又停住
    s.append(f'<path d="M150,{gy2 + 88} L204,{gy2 + 88}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="204" y1="{gy2 + 82}" x2="204" y2="{gy2 + 94}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(204, gy2 + 106, "停在这里", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "执而不责：有凭据，却不用它去索", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "大怨既成，和亦有痕；善者不待其成。", 4.8, INK))
    s.append(txt(24, a + 16, "契不响，账出声：一个只存着，一个天天在算。", 4.8, INK))
    s.append(txt(24, a + 34, "有而不取，是为有德。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "是以圣人执左契，而不责于人。", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "执契而不责。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch79a"))
    s.append('</svg>')
    return "\n".join(s)


def ch79b_yi_zhang_zhang():
    W, H = 380, 728
    body, y = head(W, H, "契只存着，账天天在算",
                   "第 七 十 九 章 · 彻", "一张账", "有德司契，无德司彻。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "彻，通也：通篇算过的账。它每月重算，所以永远有新数。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "契刻着齿，账写着数：一个记得住，一个算得清。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、账摊开着：天天在算", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 摊开的账册：两页
    s.append(f'<path d="M92,{gy + 44} L188,{gy + 52} L188,{gy + 118} L92,{gy + 110} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M284,{gy + 44} L188,{gy + 52} L188,{gy + 118} L284,{gy + 110} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    for i in range(5):
        s.append(f'<line x1="102" y1="{gy + 58 + i * 11}" x2="176" y2="{gy + 62 + i * 11}" stroke="#B9A98F" stroke-width="0.7"/>')
        s.append(f'<line x1="200" y1="{gy + 62 + i * 11}" x2="274" y2="{gy + 58 + i * 11}" stroke="#B9A98F" stroke-width="0.7"/>')
    # 一支笔
    s.append(f'<line x1="228" y1="{gy + 34}" x2="240" y2="{gy + 92}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M240,{gy + 92} l-4,8 l6,-1" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 136, "彻：通篇算过，条条都记得", 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 168, "它不出声，但它天天在动", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、账合上了：只存那一块木", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 合起的册子，绳子系住
    s.append(f'<rect x="112" y="{gy2 + 60}" width="60" height="56" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="112" y1="{gy2 + 74}" x2="172" y2="{gy2 + 74}" stroke="#B9A98F" stroke-width="0.7"/>')
    s.append(f'<line x1="156" y1="{gy2 + 60}" x2="156" y2="{gy2 + 116}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M112,{gy2 + 88} q-12,4 -6,14 q8,-6 6,-14" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(142, gy2 + 136, "账合了，绳子系上", 4.2, "#6E6459", "middle"))
    # 旁边那块契木
    s.append(f'<rect x="222" y="{gy2 + 52}" width="30" height="70" rx="2" fill="#DED2B8" stroke="{INK}" stroke-width="1.1"/>')
    for i in range(3):
        s.append(f'<line x1="222" y1="{gy2 + 62 + i * 12}" x2="236" y2="{gy2 + 62 + i * 12}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(252, gy2 + 136, "只剩这块木", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "司契者只存凭据，不算那一遍", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "账每算一遍，就多一遍的数；契不重算，齿还是那道齿。", 4.8, INK))
    s.append(txt(24, a + 16, "无德司彻：不是算错了，是算得太勤。", 4.8, INK))
    s.append(txt(24, a + 34, "有德司契，无德司彻。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "有德司契，无德司彻。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "契记齿，账记数。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch79b"))
    s.append('</svg>')
    return "\n".join(s)


def ch79c_yi_gan_cheng():
    W, H = 380, 726
    body, y = head(W, H, "天道无亲：它不进门，就挂在门口",
                   "第 七 十 九 章 · 亲", "一杆秤", "天道无亲，常与善人。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "它不挑东西，什么都称；它不进门，就挂在门口。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "「无亲」不是无情，是不认人：两边一样重，它才平。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、什么都称：不分亲疏", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 秤：杆、提纽
    s.append(f'<line x1="72" y1="{gy + 56}" x2="308" y2="{gy + 56}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<polygon points="182,{gy + 54} 192,{gy + 54} 187,{gy + 26}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="34" y1="{gy + 96}" x2="330" y2="{gy + 96}" stroke="{LINE}" stroke-width="0.8"/>')
    # 左盘：一块石
    s.append(f'<line x1="72" y1="{gy + 56}" x2="56" y2="{gy + 78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="72" y1="{gy + 56}" x2="88" y2="{gy + 78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M54,{gy + 78} Q72,{gy + 98} 90,{gy + 78}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="62" y="{gy + 62}" width="20" height="14" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
    # 右盘：一捧谷
    s.append(f'<line x1="308" y1="{gy + 56}" x2="292" y2="{gy + 78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="308" y1="{gy + 56}" x2="324" y2="{gy + 78}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M290,{gy + 78} Q308,{gy + 98} 326,{gy + 78}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M292,{gy + 78} q16,-14 32,0" fill="#DED2B8" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(72, gy + 116, "一块石", 4.2, "#6E6459", "middle"))
    s.append(txt(308, gy + 116, "一捧谷", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy + 116, "什么都称", 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 168, "它不挑东西：石与谷，两盘一样重就平", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、不进门：挂在门口", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 132}" x2="330" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1"/>')
    # 门：门框＋门内
    s.append(f'<rect x="86" y="{gy2 + 40}" width="96" height="92" fill="#F2EADA" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="134" y1="{gy2 + 40}" x2="134" y2="{gy2 + 132}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="126" cy="{gy2 + 88}" r="2" fill="{INK}"/>')
    s.append(f'<circle cx="142" cy="{gy2 + 88}" r="2" fill="{INK}"/>')
    s.append(txt(134, gy2 + 150, "门里", 4.2, "#6E6459", "middle"))
    # 秤挂在门外
    s.append(f'<line x1="238" y1="{gy2 + 28}" x2="238" y2="{gy2 + 52}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="214" y1="{gy2 + 52}" x2="262" y2="{gy2 + 52}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<polygon points="232,{gy2 + 50} 242,{gy2 + 50} 237,{gy2 + 30}" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="212" y1="{gy2 + 52}" x2="206" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="216" y1="{gy2 + 52}" x2="222" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="260" y1="{gy2 + 52}" x2="254" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<line x1="264" y1="{gy2 + 52}" x2="270" y2="{gy2 + 84}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M204,{gy2 + 84} Q214,{gy2 + 98} 224,{gy2 + 84}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M252,{gy2 + 84} Q262,{gy2 + 98} 272,{gy2 + 84}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(238, gy2 + 110, "挂在门外", 4.2, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "不入门者，与善人居：它不进谁家，才称得平", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "「无亲」不是无情：亲是偏向，无亲是不偏向。", 4.8, INK))
    s.append(txt(24, a + 16, "天道不进谁家门，所以它称谁家的东西都一样重。", 4.8, INK))
    s.append(txt(24, a + 34, "天道无亲，故不入门；不入门者，与善人居。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "天道无亲，常与善人。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "无亲者，不偏向也。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch79c"))
    s.append('</svg>')
    return "\n".join(s)


def ch80a_yi_gen_sheng():
    W, H = 380, 728
    body, y = head(W, H, "只有数，没有字：记的是我有多少",
                   "第 八 十 章 · 结", "一根打了结的绳", "使民复结绳而用之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "结绳：大事大结，小事小结。它只有数，没有条款。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "字一出来，绳子就变成了账：记的不再是「我有多少」，是「你欠我多少」。", 4.5, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、绳上只打结", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 一根绳
    s.append(f'<path d="M46,{gy + 84} q20,-10 40,0 q20,10 40,0 q20,-10 40,0 q20,10 40,0 q20,-10 40,0 q20,10 40,0" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    # 大小结
    for cx, r in [(76, 4), (116, 2.6), (156, 5), (196, 2.6), (236, 4), (276, 3)]:
        s.append(f'<circle cx="{cx}" cy="{gy + 84}" r="{r}" fill="{INK}"/>')
    s.append(txt(190, gy + 116, "大事大结，小事小结：只有数", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 168, "没有字，就不必争那个字怎么写", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、结完了，挂在墙上", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 墙与钉
    s.append(f'<line x1="40" y1="{gy2 + 30}" x2="330" y2="{gy2 + 30}" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<circle cx="150" cy="{gy2 + 30}" r="2.2" fill="{INK}"/>')
    # 卷起来的绳，挂在钉上
    s.append(f'<ellipse cx="150" cy="{gy2 + 68}" rx="26" ry="20" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<ellipse cx="150" cy="{gy2 + 68}" rx="16" ry="12" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="150" y1="{gy2 + 30}" x2="150" y2="{gy2 + 48}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M172,{gy2 + 84} q10,10 4,20" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(txt(150, gy2 + 116, "挂着：在，不用", 4.4, SEAL, "middle"))
    s.append(txt(236, gy2 + 68, "绳在，不响；", 4.3, "#6E6459"))
    s.append(txt(236, gy2 + 80, "数在，不算。", 4.3, "#6E6459"))
    s.append(txt(190, gy2 + 168, "都在，都不用：这就是这一章全部的功夫", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "绳上只打结，不刻字：它是数，不是条款。", 4.8, INK))
    s.append(txt(24, a + 16, "刻了字，绳子就从「记我有多少」变成「记你欠我多少」。", 4.8, INK))
    s.append(txt(24, a + 34, "甘其食者，不尝人之食。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "使民复结绳而用之。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "绳上只打结，不刻字。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch80a"))
    s.append('</svg>')
    return "\n".join(s)


def ch80b_yi_tiao_chuan():
    W, H = 380, 728
    body, y = head(W, H, "它每天被人看见，每天不被使用",
                   "第 八 十 章 · 舟", "一条停在岸上的船", "虽有舟舆，无所乘之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "它能走，能载，能到很远的地方；但它停着。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "「无所乘之」不是没有船，是船在而不启动。", 4.7, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、能走：桨在手", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 水
    s.append(f'<path d="M40,{gy + 108} q22,6 44,0 q22,-6 44,0 q22,6 44,0 q22,-6 44,0 q22,6 44,0 q22,-6 44,0" fill="none" stroke="#4A5C55" stroke-width="1"/>')
    # 船
    s.append(f'<path d="M88,{gy + 66} L246,{gy + 66} Q232,{gy + 104} 168,{gy + 104} Q104,{gy + 104} 88,{gy + 66} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="80" y1="{gy + 66}" x2="254" y2="{gy + 66}" stroke="{INK}" stroke-width="1.3"/>')
    # 桨
    s.append(f'<line x1="130" y1="{gy + 46}" x2="216" y2="{gy + 96}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<ellipse cx="222" cy="{gy + 99}" rx="9" ry="4" fill="#DED2B8" stroke="{INK}" stroke-width="1" transform="rotate(14 222 {gy + 99})"/>')
    s.append(txt(190, gy + 128, "船能走，桨在手", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 168, "有而不用：船不破，水不惊", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、不启动：桨横在船里", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M40,{gy2 + 110} q22,6 44,0 q22,-6 44,0 q22,6 44,0 q22,-6 44,0 q22,6 44,0 q22,-6 44,0" fill="none" stroke="#4A5C55" stroke-width="1"/>')
    s.append(f'<path d="M88,{gy2 + 68} L246,{gy2 + 68} Q232,{gy2 + 106} 168,{gy2 + 106} Q104,{gy2 + 106} 88,{gy2 + 68} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<line x1="80" y1="{gy2 + 68}" x2="254" y2="{gy2 + 68}" stroke="{INK}" stroke-width="1.3"/>')
    # 桨平放在船里
    s.append(f'<line x1="112" y1="{gy2 + 78}" x2="212" y2="{gy2 + 78}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<ellipse cx="106" cy="{gy2 + 78}" rx="8" ry="3.4" fill="#DED2B8" stroke="{INK}" stroke-width="1"/>')

    # 系船的绳
    s.append(f'<path d="M246,{gy2 + 74} q18,6 6,18" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(txt(190, gy2 + 130, "桨横着，绳系着：不启动", 4.4, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "每天被人看见，每天不被使用", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "舟在，而不乘：有而不用，不是不能用。", 4.8, INK))
    s.append(txt(24, a + 16, "一条停在岸上的船，比一条在江心的船，少惊动多少人。", 4.8, INK))
    s.append(txt(24, a + 34, "三样都在，三样都不动。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "虽有舟舆，无所乘之。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "舟在，而不乘。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch80b"))
    s.append('</svg>')
    return "\n".join(s)


def ch80c_yi_shan_men():
    W, H = 380, 728
    body, y = head(W, H, "望得见，闻得见，脚不过去",
                   "第 八 十 章 · 门", "一扇开着的门", "邻国相望，鸡犬之声相闻，民至老死不相往来。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "邻国在望，鸡犬在闻，门是开的——但没有人走过去。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "至老死不相往来者，非不能往，是不必往。", 4.7, "#6E6459", "middle"))

    def doorway(gy, leaf=True):
        g = gy + 120
        # 一根门框：两根立柱、一道门楣
        s.append(f'<line x1="138" y1="{g}" x2="138" y2="{gy + 58}" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<line x1="186" y1="{g}" x2="186" y2="{gy + 58}" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<line x1="128" y1="{gy + 58}" x2="196" y2="{gy + 58}" stroke="{INK}" stroke-width="1.3"/>')
        if leaf:
            # 门板敞在左柱外侧：一片斜着的矩形
            s.append(f'<path d="M138,{g} L138,{gy + 62} L120,{gy + 56} L120,{g - 6} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
            s.append(f'<line x1="129" y1="{g - 3}" x2="129" y2="{gy + 59}" stroke="{LINE}" stroke-width="0.7"/>')

    s.append(txt(24, y + 50, "一、门开着，路也通着", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 120}" x2="330" y2="{gy + 120}" stroke="{INK}" stroke-width="1"/>')
    doorway(gy, True)
    # 门后的路：由门口往远处收窄（透视）
    s.append(f'<path d="M141,{gy + 120} L196,{gy + 120} L300,{gy + 76} L268,{gy + 76} Z" fill="#F2EADA" stroke="{LINE}" stroke-width="0.9"/>')
    # 远处邻国：屋
    s.append(f'<path d="M272,{gy + 76} L284,{gy + 62} L296,{gy + 76}" fill="none" stroke="#B9A98F" stroke-width="1.1"/>')
    s.append(f'<rect x="274" y="{gy + 76}" width="20" height="14" fill="none" stroke="#B9A98F" stroke-width="1.1"/>')
    s.append(f'<circle cx="308" cy="{gy + 90}" r="2" fill="#B9A98F"/>')
    s.append(f'<circle cx="317" cy="{gy + 92}" r="1.6" fill="#B9A98F"/>')
    s.append(txt(290, gy + 100, "邻国在望", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy + 148, "门是开的：挡路的从来不是门", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、脚停在门槛前", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 120}" x2="330" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1"/>')
    doorway(gy2, False)
    # 双足，立在门前（两只脚并立，脚尖朝门）
    s.append(f'<ellipse cx="74" cy="{gy2 + 112}" rx="9" ry="5" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="92" cy="{gy2 + 112}" rx="9" ry="5" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<circle cx="{78 + i * 4}" cy="{gy2 + 109}" r="0.9" fill="{INK}"/>')
        s.append(f'<circle cx="{96 + i * 4}" cy="{gy2 + 109}" r="0.9" fill="{INK}"/>')
    # 想去而不过去的虚线，停在门柱前
    s.append(f'<path d="M104,{gy2 + 112} L124,{gy2 + 112}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="124" y1="{gy2 + 102}" x2="124" y2="{gy2 + 122}" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(txt(120, gy2 + 96, "就到这里", 4.2, SEAL, "end"))
    # 鸡犬之声：门里传出来的两声
    s.append(f'<path d="M206,{gy2 + 82} q16,-8 32,0" fill="none" stroke="#B9A98F" stroke-width="0.8"/>')
    s.append(f'<path d="M214,{gy2 + 74} q14,-10 28,0" fill="none" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(222, gy2 + 96, "鸡犬之声相闻", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 148, "非不能往，是不必往", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "门开着，路通着，声音听得见：三样都在，三样都不动。", 4.8, INK))
    s.append(txt(24, a + 16, "没有走过去，不是因为走不过去，是因为没有非走不可的事。", 4.8, INK))
    s.append(txt(24, a + 34, "至老死不相往来者，非不能往，是不必往。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "邻国相望，鸡犬之声相闻，民至老死不相往来。", 4.5, INK, "middle"))
    s.append(txt(190, c + 36, "望得见，闻得见，脚不过去。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch80c"))
    s.append('</svg>')
    return "\n".join(s)


def ch81a_yi_kou_cang():
    W, H = 380, 728
    body, y = head(W, H, "它越大，主人越不敢出门",
                   "第 八 十 一 章 · 仓", "一口仓", "圣人不积，既以为人，己愈有。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "仓有四壁，有门，有锁：它能装，能算，能守着。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "仓是存量：越取越少；守得越紧，人越不敢走开。", 4.5, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、有壁有锁：装得下", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 128}" x2="330" y2="{gy + 128}" stroke="{INK}" stroke-width="1"/>')
    # 仓：屋形，四壁，门在中间
    s.append(f'<path d="M96,{gy + 128} L96,{gy + 52} L190,{gy + 34} L284,{gy + 52} L284,{gy + 128}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M96,{gy + 52} L190,{gy + 34} L284,{gy + 52}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<rect x="172" y="{gy + 84}" width="36" height="44" fill="#FBF6EC" stroke="{INK}" stroke-width="1.2"/>')
    # 锁
    s.append(f'<rect x="184" y="{gy + 102}" width="12" height="10" fill="{SEAL}" stroke="none"/>')
    s.append(f'<path d="M186,{gy + 102} q4,-6 8,0" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    # 仓里的谷堆（透过门看不去，改在檐下画谷）

    s.append(txt(190, gy + 144, "装得下：四壁、门、锁", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 168, "存量：一斗一斗数得清", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、越大，越不敢出门", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 128}" x2="330" y2="{gy2 + 128}" stroke="{INK}" stroke-width="1"/>')
    # 更大的仓
    s.append(f'<path d="M60,{gy2 + 128} L60,{gy2 + 48} L190,{gy2 + 28} L320,{gy2 + 48} L320,{gy2 + 128}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M60,{gy2 + 48} L190,{gy2 + 28} L320,{gy2 + 48}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<rect x="172" y="{gy2 + 84}" width="36" height="44" fill="#B9A98F" stroke="{INK}" stroke-width="1.2"/>')
    # 锁已锁上（赭色）
    s.append(f'<rect x="183" y="{gy2 + 102}" width="14" height="11" fill="{SEAL}" stroke="none"/>')
    s.append(f'<path d="M186,{gy2 + 102} q4,-7 8,0" fill="none" stroke="{SEAL}" stroke-width="1.3"/>')
    # 主人站在门外，手里握着一串钥匙
    s.append(f'<circle cx="120" cy="{gy2 + 100}" r="5" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M120,{gy2 + 105} L120,{gy2 + 128}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M113,{gy2 + 128} L120,{gy2 + 118} L127,{gy2 + 128}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M124,{gy2 + 110} l8,6" stroke="{INK}" stroke-width="1"/>')
    for i in range(3):
        s.append(f'<circle cx="{132 + i * 3}" cy="{gy2 + 117 + i * 1}" r="1.4" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
    s.append(txt(120, gy2 + 144, "主人守在门外", 4.4, SEAL, "middle"))
    s.append(txt(232, gy2 + 108, "仓越大，", 4.3, "#6E6459"))
    s.append(txt(232, gy2 + 120, "越不敢走。", 4.3, "#6E6459"))
    s.append(txt(190, gy2 + 168, "仓会空，泉不会：不积，是换一种算法", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "仓是存量：有壁、有门、有锁，越取越少。", 4.8, INK))
    s.append(txt(24, a + 16, "守得越紧，人越走不开——它越大，主人越不敢出门。", 4.8, INK))
    s.append(txt(24, a + 34, "圣人不积：不是不要仓，是知道仓算不出泉。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "圣人不积，既以为人，己愈有。", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "仓会空，泉不会。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch81a"))
    s.append('</svg>')
    return "\n".join(s)


def ch81b_yi_yan_quan():
    W, H = 380, 728
    body, y = head(W, H, "它不装，只是涌；越涌，周围越湿",
                   "第 八 十 一 章 · 泉", "一眼泉", "既以与人，己愈多。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "泉没有四壁，没有门，没有锁：它不装，只是涌。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "泉是流量：越取越多；周围越湿，它越涌。", 4.5, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、无壁无锁：只是个眼", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 120}" x2="330" y2="{gy + 120}" stroke="{INK}" stroke-width="1"/>')
    # 泉眼：地上一圈石（开口），水从中间涌起
    s.append(f'<ellipse cx="190" cy="{gy + 120}" rx="52" ry="10" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="190" cy="{gy + 120}" rx="34" ry="6" fill="#4A5C55" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M190,{gy + 116} q-12,-22 0,-34 q12,12 0,34" fill="none" stroke="#4A5C55" stroke-width="1.2"/>')
    s.append(f'<path d="M176,{gy + 116} q-8,-10 -2,-18" fill="none" stroke="#4A5C55" stroke-width="0.8"/>')
    s.append(f'<path d="M204,{gy + 116} q8,-10 2,-18" fill="none" stroke="#4A5C55" stroke-width="0.8"/>')
    # 周围湿：一圈淡灰的湿痕
    s.append(f'<ellipse cx="190" cy="{gy + 121}" rx="96" ry="16" fill="none" stroke="#DED2B8" stroke-width="1"/>')
    s.append(f'<ellipse cx="190" cy="{gy + 122}" rx="120" ry="20" fill="none" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(txt(190, gy + 146, "不装，只是涌", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 168, "流量：没有底，也没有顶", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、取走一瓢，还在涌", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 120}" x2="330" y2="{gy2 + 120}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="150" cy="{gy2 + 120}" rx="52" ry="10" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="150" cy="{gy2 + 120}" rx="34" ry="6" fill="#4A5C55" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M150,{gy2 + 116} q-12,-24 0,-36 q12,12 0,36" fill="none" stroke="#4A5C55" stroke-width="1.4"/>')
    s.append(f'<ellipse cx="150" cy="{gy2 + 121}" rx="96" ry="16" fill="none" stroke="#DED2B8" stroke-width="1"/>')
    # 一只瓢，舀起一瓢水，往外递
    # 瓢：斜握，瓢中盛着水
    s.append(f'<path d="M212,{gy2 + 108} q14,16 28,2" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M216,{gy2 + 110} q10,9 20,1" fill="#4A5C55" stroke="none" opacity="0.85"/>')
    s.append(f'<line x1="238" y1="{gy2 + 108}" x2="252" y2="{gy2 + 92}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<circle cx="253" cy="{gy2 + 91}" r="3" fill="none" stroke="{INK}" stroke-width="1"/>')
    # 水面浮出的一层（仍在涌）
    s.append(f'<path d="M196,{gy2 + 112} q10,-6 18,-2" fill="none" stroke="#4A5C55" stroke-width="0.9"/>')
    s.append(txt(252, gy2 + 140, "舀走一瓢", 4.2, SEAL, "middle"))
    s.append(txt(150, gy2 + 146, "取走，仍在涌", 4.4, SEAL, "middle"))
    s.append(txt(190, gy2 + 168, "既以与人，己愈多", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "泉是流量：不装，只涌；越取越多。", 4.8, INK))
    s.append(txt(24, a + 16, "舀走一瓢，泉不记得，周围的地记得——它更湿了。", 4.8, INK))
    s.append(txt(24, a + 34, "既以与人，己愈多：给人，是让泉眼更旺。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "既以与人，己愈多。", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "越取越多：泉不会空。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch81b"))
    s.append('</svg>')
    return "\n".join(s)


def ch81c_yi_ba_dao():
    W, H = 380, 728
    body, y = head(W, H, "顺着走，禾就下来；逆着走，刀就卡",
                   "第 八 十 一 章 · 刀", "一把刀", "天之道，利而不害；圣人之道，为而不争。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "它不砍，只是顺着禾走：顺着走，禾就下来。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "刀是「不害」的做法：利者，顺也，不是加力。", 4.5, "#6E6459", "middle"))

    s.append(txt(24, y + 50, "一、顺着走：禾下来", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy + 126}" x2="330" y2="{gy + 126}" stroke="{INK}" stroke-width="1"/>')
    # 禾：三根秆，穗下垂
    s.append(f'<line x1="110" y1="{gy + 126}" x2="110" y2="{gy + 66}" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<line x1="150" y1="{gy + 126}" x2="150" y2="{gy + 52}" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<line x1="190" y1="{gy + 126}" x2="190" y2="{gy + 72}" stroke="{GREEN}" stroke-width="1.4"/>')
    for cx, ty in [(110, 66), (150, 52), (190, 72)]:
        hy = gy + ty
        s.append(f'<path d="M{cx},{hy + 2} q7,9 1,17" fill="none" stroke="{GREEN}" stroke-width="1"/>')
        for k in range(3):
            s.append(f'<circle cx="{cx - 3}" cy="{hy + 7 + k * 4}" r="1.4" fill="{GREEN}"/>')
    # 刀：顺着秆斜切，刀身与秆同向
    s.append(f'<path d="M228,{gy + 44} L282,{gy + 96}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M282,{gy + 96} L288,{gy + 92} L284,{gy + 100} Z" fill="{INK}" stroke="none"/>')
    s.append(f'<line x1="228" y1="{gy + 44}" x2="222" y2="{gy + 38}" stroke="{SEAL}" stroke-width="2"/>')
    # 顺向的细虚线（不叠在刀上，放在刀外侧）
    s.append(f'<path d="M244,{gy + 48} L286,{gy + 82}" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="3 3"/>')
    s.append(f'<path d="M281,{gy + 76} l7,5 l-8,1" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(252, gy + 36, "顺", 4.6, SEAL, "middle"))
    s.append(txt(190, gy + 148, "刀顺着禾走，禾就下来", 4.6, GREEN, "middle"))

    s.append(txt(24, gy + 192, "二、逆着走：刀卡住", 4.8, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="34" y1="{gy2 + 126}" x2="330" y2="{gy2 + 126}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="110" y1="{gy2 + 126}" x2="110" y2="{gy2 + 58}" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<line x1="150" y1="{gy2 + 126}" x2="150" y2="{gy2 + 58}" stroke="{GREEN}" stroke-width="1.4"/>')
    s.append(f'<line x1="190" y1="{gy2 + 126}" x2="190" y2="{gy2 + 58}" stroke="{GREEN}" stroke-width="1.4"/>')
    # 刀逆着禾横切（刀身横在秆中央），被秆夹住
    s.append(f'<path d="M124,{gy2 + 96} L182,{gy2 + 96}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<line x1="124" y1="{gy2 + 96}" x2="116" y2="{gy2 + 96}" stroke="{SEAL}" stroke-width="2"/>')
    # 卡住：刀身处三道赭短线
    s.append(f'<line x1="140" y1="{gy2 + 90}" x2="140" y2="{gy2 + 102}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="164" y1="{gy2 + 90}" x2="164" y2="{gy2 + 102}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<path d="M186,{gy2 + 96} L200,{gy2 + 96}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="200" y1="{gy2 + 89}" x2="200" y2="{gy2 + 103}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(txt(196, gy2 + 82, "卡住", 4.4, SEAL, "middle"))
    s.append(txt(190, gy2 + 148, "逆着走，刀就卡：力加在刃上，不在禾上", 4.6, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "刀不砍，只是顺着禾走：顺是「不害」的做法。", 4.8, INK))
    s.append(txt(24, a + 16, "逆着走，禾没下来，刀先卡住——力用在自己身上了。", 4.8, INK))
    s.append(txt(24, a + 34, "天之道，利而不害；圣人之道，为而不争。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 23, "天之道，利而不害；圣人之道，为而不争。", 4.8, INK, "middle"))
    s.append(txt(190, c + 36, "刀顺着禾走，禾才下来。", 4.7, GREEN, "middle"))
    s.append(gold(c + 64, "ch81c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第二章 · 标杆 ============
def ch02b_yi_gen_biao_gan():
    W, H = 380, 999
    body, y = head(W, H, "一根标杆立起来，两侧的影子同时落地：丑不是先有的，是立美那一刻才有的",
                   "第 二 章 · 标", "一根标杆", "天下皆知美之为美，斯恶已。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「美」不是东西的性质，是一句评语；评语要有刻度，刻度先要立一根杆。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "杆一立，量得到的叫美，量不到的当场成了恶——恶是被这一杆造出来的，不是原来就有。", 5.0, "#6E6459", "middle"))

    # 一、未立标
    s.append(txt(24, y + 52, "一、未立标：地上只有东西", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="132" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy + 96
    s.append(f'<line x1="40" y1="{base}" x2="330" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    for bx, bw, bh in [(78, 26, 20), (150, 34, 14), (226, 22, 26)]:
        s.append(box(bx, base - bh, bw, bh, fill="#EFE6D4", stroke="#B9A98F", width=0.8))
    for bx in (60, 118, 196, 262, 306):
        s.append(f'<line x1="{bx}" y1="{base}" x2="{bx - 3}" y2="{base - 7}" stroke="#B9A98F" stroke-width="0.7"/>')
        s.append(f'<line x1="{bx}" y1="{base}" x2="{bx + 3}" y2="{base - 6}" stroke="#B9A98F" stroke-width="0.7"/>')
    s.append(txt(190, gy + 116, "东西都在，只是没人给它排位：没有「美」，也就没有「恶」", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 128, "空地一片", 4.3, "#8A7C69", "middle"))

    # 二、立标
    s.append(txt(24, gy + 150, "二、立标：一杆落地，两侧同时有了名字", 5.2, SEAL))
    gy2 = gy + 162
    s.append(f'<rect x="26" y="{gy2}" width="328" height="170" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base2 = gy2 + 116
    s.append(f'<line x1="40" y1="{base2}" x2="330" y2="{base2}" stroke="{INK}" stroke-width="1"/>')
    pole = 190
    s.append(f'<line x1="{pole}" y1="{base2}" x2="{pole}" y2="{base2 - 92}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(box(pole - 13, base2 - 104, 26, 12, fill=INK, stroke=INK, width=0.8))
    for k in range(1, 5):
        s.append(f'<line x1="{pole}" y1="{base2 - 92 + k * 2}" x2="{pole}" y2="{base2 - 92 + k * 2}" stroke="{INK}" stroke-width="0.4"/>')
    for k in range(5):
        yy = base2 - 84 + k * 18
        s.append(f'<line x1="{pole}" y1="{yy}" x2="{pole + 7}" y2="{yy - 9}" stroke="#B9A98F" stroke-width="0.5"/>')
    # 左右两片影子：贴地、平铺、中间留一道缝，不合成一顶
    for dx, col, hatch in [(-1, "#E8DCC2", "#CDBA97"), (1, "#D8CBAC", "#BFA77F")]:
        x_in = pole + dx * 12
        x_out = pole + dx * 114
        s.append(f'<path d="M{x_in},{base2} L{x_out},{base2} L{x_out - dx * 8},{base2 - 14} L{x_in},{base2 - 22} z" fill="{col}" stroke="none"/>')
        for k in range(5):
            hx = pole + dx * (20 + k * 20)
            s.append(f'<line x1="{hx}" y1="{base2 - 3}" x2="{hx}" y2="{base2 - 12}" stroke="{hatch}" stroke-width="0.5"/>')
    s.append(txt(pole - 62, base2 - 30, "美", 8.0, SEAL, "middle"))
    s.append(txt(pole - 62, base2 + 14, "量得到的", 4.4, SEAL, "middle"))
    s.append(txt(pole + 62, base2 - 30, "恶", 8.0, "#6E6459", "middle"))
    s.append(txt(pole + 62, base2 + 14, "量不到的", 4.4, "#6E6459", "middle"))
    s.append(txt(190, gy2 + 168, "两侧的影子同时落地：杆立之前，一片影子也没有", 4.5, GREEN, "middle"))
    s.append(txt(190, gy2 + 182, "影子不是原本就有的", 4.3, "#8A7C69", "middle"))

    a = gy2 + 194
    s.append(txt(24, a, "标尺一立，另一半就被判了罪——罪的来处，是那把尺，不是那个人。", 5.4, INK))
    s.append(txt(24, a + 16, "所以「斯恶已」不是骂人，是记账：这一杆立下去，账上同时记了一笔善、一笔恶。", 5.4, INK))
    s.append(txt(24, a + 34, "要收的不是恶人，是那一杆——杆收了，账才平。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "不是先有丑，再立美；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "是立美那一刻，丑才成立。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch02b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第二章 · 两只管子 ============
def ch02c_liang_zhi_guan():
    W, H = 380, 999
    body, y = head(W, H, "和是两套管各自守节、一唱一应；合是把两套并成一套，只留一个声音",
                   "第 二 章 · 和", "两只管子", "音声相和，前后相随。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「龢」从龠从禾，龠是编管——和这个字本来就说的是吹管之事，不是抹平。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "两管长短不同，各发各的声；一吹一应，声在中间才成了第三样东西。", 5.0, "#6E6459", "middle"))

    # 一、和
    s.append(txt(24, y + 52, "一、和：两管各守其节，应答生第三物", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="176" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')

    def guan(cx, top, h, w, lab, color=INK):
        s.append(f'<path d="M{cx - w / 2},{top} L{cx - w / 2},{top + h} q{w / 2},8 {w},0 L{cx + w / 2},{top} z" fill="#EFE6D4" stroke="{color}" stroke-width="1.1"/>')
        s.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w / 2}" ry="3.4" fill="none" stroke="{color}" stroke-width="0.9"/>')
        s.append(txt(cx, top - 8, lab, 4.4, color, "middle"))

    gb = gy + 132
    guan(112, gb - 92, 92, 16, "长管")
    guan(196, gb - 62, 62, 16, "短管")
    # 一唱、一应：各自的声纹
    for k in range(3):
        r = 24 + k * 8
        s.append(f'<path d="M{104},{gb - 76} q-{r / 2},-{r} -{r},0" fill="none" stroke="{SEAL}" stroke-width="0.7" opacity="0.5"/>')
    s.append(txt(44, gb - 84, "一唱", 4.4, SEAL))
    for k in range(3):
        r = 22 + k * 8
        s.append(f'<path d="M{214},{gb - 48} q{r / 2},-{r} {r},0" fill="none" stroke="{GREEN}" stroke-width="0.7" opacity="0.5"/>')
    s.append(txt(266, gb - 56, "一应", 4.4, GREEN))
    # 第三样东西：两管之间浮起
    for k in range(3):
        s.append(f'<path d="M136,{gb - 96 - k * 6} q14,-6 28,0" fill="none" stroke="#8A7C69" stroke-width="0.6" opacity="0.55"/>')
    s.append(txt(150, gb - 120, "第三样：和声", 4.4, "#6E6459", "middle"))
    s.append(f'<line x1="40" y1="{gb}" x2="330" y2="{gb}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 150, "两管互不吞并，各守边界——和的前提是不同", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 164, "和：一唱一应，各自成声", 4.3, "#8A7C69", "middle"))

    # 二、合
    s.append(txt(24, gy + 194, "二、合：两管并成一根，只剩一个声音", 5.2, SEAL))
    gy2 = gy + 206
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    gb2 = gy2 + 112
    s.append(f'<path d="M172,{gb2 - 96} L172,{gb2} q18,8 36,0 L208,{gb2 - 96} z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="190" cy="{gb2 - 96}" rx="18" ry="3.6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="40" y1="{gb2}" x2="330" y2="{gb2}" stroke="{INK}" stroke-width="1"/>')
    for k in range(3):
        r = 40 + k * 8
        s.append(f'<path d="M198,{gb2 - 80} q{r / 2},-{r} {r},0" fill="none" stroke="#6E6459" stroke-width="0.7" opacity="0.45"/>')
    s.append(txt(216, gb2 - 34, "只剩一个声音", 4.4, "#6E6459"))
    s.append(txt(190, gy2 + 128, "第二管不见了，第一管也没有变得更响——是少了一个声音，不是多了一个", 4.5, GREEN, "middle"))
    s.append(txt(190, gy2 + 142, "合：抹平边界，只留一套", 4.3, "#8A7C69", "middle"))

    a = gy2 + 172
    s.append(txt(24, a, "和不是「没有分歧」，恰是「有分歧而各自站得住」。", 5.4, INK))
    s.append(txt(24, a + 16, "老子要护的就是这一处：不把两套并成一套，才生得出第三样东西。", 5.4, INK))
    s.append(txt(24, a + 34, "合是把差异抹掉换来的安静；和是差异还在，却已经应上了。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "和是听得见的第三声，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "合是只剩一个声音的安静。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch02c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第三章 · 一块价牌 ============
def ch03b_yi_kuai_jia_pai():
    body, y = head(380, 999, "三个「不」是一个动作：不主动起标。价牌一挂，力气都朝牌子去",
                   "第 三 章 · 价 牌", "一块价牌", "不尚贤，使民不争；不贵难得之货，使民不为盗。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「尚」是把东西抬到上面去，「贵」是给它标个高价，「见」是把它摆到明处。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "三个字，三种抬举；三个「不」，是同一个动作：不主动起标。", 5.0, "#6E6459", "middle"))

    goods = [(92, 30, 26), (168, 36, 20), (244, 26, 30)]

    # 一、挂牌
    s.append(txt(24, y + 52, "一、挂牌：三块牌挂出来，力气全朝牌子去", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    shelf = gy + 46
    s.append(f'<line x1="40" y1="{shelf}" x2="330" y2="{shelf}" stroke="{INK}" stroke-width="1"/>')
    for gx, gw, gh in goods:
        s.append(box(gx, shelf, gw, gh, fill="#EFE6D4", stroke="#B9A98F", width=0.8))
        s.append(f'<line x1="{gx + gw / 2}" y1="{shelf + gh}" x2="{gx + gw / 2}" y2="{shelf + gh + 12}" stroke="#B9A98F" stroke-width="0.6"/>')
        s.append(box(gx + gw / 2 - 12, shelf + gh + 12, 24, 13, fill="#EBD9CE", stroke=SEAL, width=0.9))
        s.append(txt(gx + gw / 2, shelf + gh + 21, "价", 4.2, SEAL, "middle"))
    mid = 168 + 18
    ptxt = shelf + 20
    for hx in (92, mid, 266):
        s.append(f'<circle cx="{hx}" cy="{gy + 170}" r="3.2" fill="none" stroke="#B9A98F" stroke-width="0.7"/>')
    s.append(arrow(92, gy + 168, mid - 30, ptxt, SEAL, 1.0, None, "arrS"))
    s.append(arrow(mid, gy + 168, mid, ptxt + 2, SEAL, 1.0, None, "arrS"))
    s.append(arrow(266, gy + 168, mid + 30, ptxt, SEAL, 1.0, None, "arrS"))
    s.append(txt(304, shelf + 44, "争", 8.4, SEAL, "middle"))
    s.append(txt(190, gy + 200, "争的不是货，是牌子上的名次", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 236, "挂牌：三样货，三块价牌，三处力气都朝牌子去", 4.4, "#8A7C69", "middle"))

    # 二、撤牌
    s.append(txt(24, gy + 264, "二、撤牌：牌子摘了，货还在，力气各回各处", 5.2, SEAL))
    gy2 = gy + 276
    s.append(f'<rect x="26" y="{gy2}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    shelf2 = gy2 + 46
    s.append(f'<line x1="40" y1="{shelf2}" x2="330" y2="{shelf2}" stroke="{INK}" stroke-width="1"/>')
    for gx, gw, gh in goods:
        s.append(box(gx, shelf2, gw, gh, fill="#EFE6D4", stroke="#B9A98F", width=0.8))
        s.append(f'<line x1="{gx + gw / 2}" y1="{shelf2 + gh}" x2="{gx + gw / 2}" y2="{shelf2 + gh + 8}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="2 2"/>')
        s.append(box(gx + gw / 2 - 12, shelf2 + gh + 8, 24, 13, fill="none", stroke=LINE2, dash="3 3", width=0.7))
        s.append(txt(gx + gw / 2, shelf2 + gh + 17, "空", 4.1, "#B9A98F", "middle"))
    s.append(txt(322, shelf2 - 6, "牌子撤了", 4.2, GREEN, "end"))
    for hx in (92, 186, 272):
        s.append(f'<circle cx="{hx}" cy="{gy2 + 174}" r="3.2" fill="none" stroke="#B9A98F" stroke-width="0.7"/>')
    s.append(arrow(92, gy2 + 170, 104, shelf2 + 30, GREEN, 0.9, None, "arr2"))
    s.append(arrow(186, gy2 + 174, 184, shelf2 + 24, GREEN, 0.9, None, "arr2"))
    s.append(arrow(272, gy2 + 170, 256, shelf2 + 30, GREEN, 0.9, None, "arr2"))
    s.append(txt(190, gy2 + 200, "各取各自要的：本然之欲还在，攀缘之欲没了根", 4.5, GREEN, "middle"))
    s.append(txt(190, gy2 + 236, "撤牌：三块空位还在，只是不再挂东西", 4.4, "#8A7C69", "middle"))

    a = gy2 + 264
    s.append(txt(24, a, "老子不否贤，不否货，也不否欲——他否的是那把尺。", 5.4, INK))
    s.append(txt(24, a + 16, "尺一收，争、盗、乱三样一起没了根：不是压住了，是没处长出来。", 5.4, INK))
    s.append(txt(24, a + 34, "所以三句话不是三道禁令，是一个动作：不主动起标。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "不尚，不是不用贤；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "是不把贤摆成一把尺。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch03b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第三章 · 一棵树 ============
def ch03c_yi_ke_shu():
    body, y = head(380, 999, "虚其心是干里留空，实其腹是干壁加厚；一根往上争高的树，风一来就折",
                   "第 三 章 · 树", "一棵树", "虚其心，实其腹；弱其志，强其骨。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "四句不是四个动作，是一棵树的上下两头：上头不争高，下头扎得住，中间壁厚而心空。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "「虚」不是把念头掏空，是把干心留成中空；空在，壁才用得起来。", 5.0, "#6E6459", "middle"))

    # 一、争高
    s.append(txt(24, y + 52, "一、争高：枝往上抢，风一来断一根", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy + 140
    s.append(f'<line x1="40" y1="{base}" x2="330" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    trunk = 196
    s.append(f'<line x1="{trunk}" y1="{base}" x2="{trunk}" y2="{base - 96}" stroke="{INK}" stroke-width="1.7"/>')
    for h1, out, h2 in [(-24, -52, 34), (-44, 44, 36), (-62, -40, 30)]:
        s.append(f'<line x1="{trunk}" y1="{base + h1}" x2="{trunk + out}" y2="{base + h1 - h2}" stroke="{INK}" stroke-width="0.8"/>')
    # 折断：右侧一根，干上留短桩，断掉的那截躺在地上
    s.append(f'<line x1="{trunk}" y1="{base - 22}" x2="{trunk + 44}" y2="{base - 56}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{trunk + 44}" y1="{base - 56}" x2="{trunk + 54}" y2="{base - 62}" stroke="{INK}" stroke-width="0.9" stroke-dasharray="3 2"/>')
    s.append(f'<line x1="{trunk + 30}" y1="{base - 44}" x2="{trunk + 38}" y2="{base - 54}" stroke="{SEAL}" stroke-width="1.0"/>')
    s.append(f'<line x1="{trunk + 42}" y1="{base - 64}" x2="{trunk + 50}" y2="{base - 56}" stroke="{SEAL}" stroke-width="1.0"/>')
    s.append(f'<line x1="{trunk + 66}" y1="{base - 3}" x2="{trunk + 132}" y2="{base - 14}" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<line x1="{trunk + 104}" y1="{base - 9}" x2="{trunk + 116}" y2="{base - 22}" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(txt(trunk + 70, base - 76, "折了", 4.4, SEAL))
    for k in range(3):
        s.append(f'<path d="M48,{base - 104 + k * 9} q30,-8 58,0" fill="none" stroke="#B9A98F" stroke-width="0.6"/>')
    s.append(txt(52, base - 114, "风", 4.4, "#8A7C69"))
    s.append(txt(190, gy + 196, "志者，往上去的那股劲：劲全使在争高上，根就浅了", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 212, "争高的树：枝细而尖，断口留在干上，断枝落在地上", 4.4, "#8A7C69", "middle"))

    # 二、实腹虚心
    s.append(txt(24, gy + 240, "二、实腹虚心：干厚、心空、根深、枝低", 5.2, SEAL))
    gy2 = gy + 252
    s.append(f'<rect x="26" y="{gy2}" width="328" height="196" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base2 = gy2 + 116
    s.append(f'<line x1="40" y1="{base2}" x2="330" y2="{base2}" stroke="{INK}" stroke-width="1"/>')
    # 根：自干底散开，不聚成一把
    for x0, x1, d in [(172, 148, 40), (180, 168, 50), (190, 190, 54), (200, 214, 50), (208, 236, 40)]:
        s.append(f'<path d="M{x0},{base2} q{(x1 - x0) / 2},20 {x1 - x0},{d}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # 干：外壁实、内心空
    s.append(f'<rect x="168" y="{base2 - 88}" width="46" height="88" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="179" y="{base2 - 80}" width="24" height="80" fill="{PAPER}" stroke="{GREEN}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    for k in range(7):
        yy = base2 - 76 + k * 11
        s.append(f'<line x1="169" y1="{yy}" x2="178" y2="{yy}" stroke="#B9A98F" stroke-width="0.5"/>')
        s.append(f'<line x1="204" y1="{yy}" x2="213" y2="{yy}" stroke="#B9A98F" stroke-width="0.5"/>')
    s.append(txt(191, base2 - 40, "空", 4.6, GREEN, "middle"))
    # 枝：自外壁出，低而横
    for y0, dx, dy in [(-78, 46, 12), (-56, 34, 8)]:
        s.append(f'<line x1="214" y1="{base2 + y0}" x2="{214 + dx}" y2="{base2 + y0 - dy}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{214 + dx}" y1="{base2 + y0 - dy}" x2="{214 + dx + 8}" y2="{base2 + y0 - dy - 6}" stroke="{GREEN}" stroke-width="0.6"/>')
        s.append(f'<line x1="168" y1="{base2 + y0}" x2="{168 - dx}" y2="{base2 + y0 - dy}" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{168 - dx}" y1="{base2 + y0 - dy}" x2="{168 - dx - 8}" y2="{base2 + y0 - dy - 6}" stroke="{GREEN}" stroke-width="0.6"/>')
    # 标注：贴在图外，短引线指向壁、根、枝
    s.append(txt(30, base2 - 64, "实其腹＝壁厚", 4.3, INK))
    s.append(f'<line x1="100" y1="{base2 - 62}" x2="166" y2="{base2 - 62}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(30, base2 + 40, "强其骨＝根深", 4.3, INK))
    s.append(f'<line x1="100" y1="{base2 + 38}" x2="144" y2="{base2 + 32}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(350, base2 - 96, "弱其志＝枝低", 4.3, INK, "end"))
    s.append(f'<line x1="348" y1="{base2 - 94}" x2="266" y2="{base2 - 96}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(190, gy2 + 208, "壁厚；虚线处是干心，留着空", 4.5, GREEN, "middle"))
    s.append(txt(190, gy2 + 224, "实腹＝壁厚，虚心＝干心留空，强骨＝根深，弱志＝枝低", 4.4, "#8A7C69", "middle"))

    a = gy2 + 252
    s.append(txt(24, a, "「实其腹」不是吃饱，是把壁留厚；「虚其心」不是清空念头，是把干心留成中空。", 5.4, INK))
    s.append(txt(24, a + 16, "壁一厚，空就能用起来；若反把壁掏薄、把空填实，看着结实，一敲就碎。", 5.4, INK))
    s.append(txt(24, a + 34, "这是第十一章「有之以为利，无之以为用」在治身上的落地。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "虚心不是空掉念头，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "是把壁留厚、把空留住。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch03c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第四章 · 一只礼器 ============
def ch04b_yi_zhi_li_qi():
    body, y = head(380, 999, "器之所以为器，正在那处铸出来的空：实心一勺即满，空腔百勺不见底",
                   "第 四 章 · 礼 器", "一只礼器", "道冲，而用之或不盈。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "《说文》「盅，器虚也」——冲就是盅，就是那只被铸出来的空。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "青铜再贵、纹饰再繁，内里若是实的，就盛不下一勺黍稷。", 5.0, "#6E6459", "middle"))

    # 一、实心
    s.append(txt(24, y + 52, "一、实心：一勺下去就满，再一勺就溢", 5.2, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy + 152
    s.append(f'<line x1="40" y1="{base}" x2="330" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    yb = base - 80
    bd = f'M138,{yb} L150,{base - 12} Q190,{base - 4} 230,{base - 12} L242,{yb} Z'
    s.append(f'<path d="{bd}" fill="#D8CBAC" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<ellipse cx="190" cy="{yb}" rx="52" ry="7.5" fill="#D8CBAC" stroke="{INK}" stroke-width="1"/>')
    for k in range(3):
        s.append(f'<path d="M{160 + k * 4},{yb} q10,-6 22,0" fill="none" stroke="#B39A72" stroke-width="0.6"/>')

    s.append(f'<line x1="160" y1="{base - 12}" x2="156" y2="{base}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="220" y1="{base - 12}" x2="224" y2="{base}" stroke="{INK}" stroke-width="1.1"/>')
    # 溢：自口沿顺壁往下淌
    s.append(f'<path d="M240,{yb + 2} q12,22 7,42 q-2,12 5,16" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="253" cy="{yb + 64}" rx="2.6" ry="4" fill="{SEAL}" opacity="0.8"/>')
    s.append(f'<path d="M140,{yb + 2} q-12,20 -7,36 q2,10 -4,14" fill="none" stroke="{SEAL}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="128" cy="{yb + 56}" rx="2.6" ry="4" fill="{SEAL}" opacity="0.8"/>')
    s.append(txt(266, yb + 26, "溢了", 4.4, SEAL))
    s.append(txt(114, yb + 22, "溢了", 4.4, SEAL, "end"))
    # 勺
    s.append(f'<path d="M178,{gy + 46} q-14,10 0,14 q14,-4 0,-14 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="178" y1="{gy + 46}" x2="198" y2="{gy + 30}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(arrow(182, gy + 62, 188, yb - 6, SEAL, 0.8, None, "arr"))
    s.append(txt(190, gy + 172, "装满即止：器满则不受，用到这里就断了", 4.5, GREEN, "middle"))

    # 二、空腹
    s.append(txt(24, gy + 200, "二、空腹：一勺下去不见底，再来一勺还是不见底", 5.2, SEAL))
    gy2 = gy + 212
    s.append(f'<rect x="26" y="{gy2}" width="328" height="180" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base2 = gy2 + 152
    s.append(f'<line x1="40" y1="{base2}" x2="330" y2="{base2}" stroke="{INK}" stroke-width="1"/>')
    yb2 = base2 - 80
    bd2 = f'M138,{yb2} L150,{base2 - 12} Q190,{base2 - 4} 230,{base2 - 12} L242,{yb2} Z'
    s.append(f'<path d="{bd2}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M146,{yb2 + 7} L158,{base2 - 16} Q190,{base2 - 10} 222,{base2 - 16} L234,{yb2 + 7} Z" '
             f'fill="{PAPER}" stroke="{GREEN}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(f'<ellipse cx="190" cy="{yb2}" rx="52" ry="7.5" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="190" cy="{yb2}" rx="44" ry="4.6" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="160" y1="{base2 - 12}" x2="156" y2="{base2}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="220" y1="{base2 - 12}" x2="224" y2="{base2}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(txt(190, base2 - 44, "空", 5.0, GREEN, "middle"))
    s.append(txt(260, base2 - 56, "不见底", 4.3, GREEN))
    s.append(f'<line x1="258" y1="{base2 - 58}" x2="232" y2="{base2 - 58}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(txt(260, base2 - 42, "从来不满", 4.3, GREEN))
    s.append(f'<line x1="258" y1="{base2 - 44}" x2="230" y2="{base2 - 36}" stroke="{LINE2}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s.append(f'<path d="M178,{gy2 + 46} q-14,10 0,14 q14,-4 0,-14 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="178" y1="{gy2 + 46}" x2="198" y2="{gy2 + 30}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(arrow(182, gy2 + 62, 188, yb2 - 6, GREEN, 0.8, None, "arr2"))
    s.append(txt(190, gy2 + 172, "从来不满，所以用不完：不溢不是缺点，是它一直能用的缘故", 4.5, GREEN, "middle"))

    a = gy2 + 200
    s.append(txt(24, a, "道的体就是一个空，不是一个物：问它「是什么」，它答不上来，只能答「能盛」。", 5.4, INK))
    s.append(txt(24, a + 16, "「或不盈」是现象，「有弗盈」是本性——帛书那句多写一个字，说的是它从来不满。", 5.4, INK))
    s.append(txt(24, a + 34, "所以它用得久：一满就止，不满不止。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "它从来不满，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "所以从来用不完。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch04b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


# ============ 第四章 · 四步 ============
def ch04c_si_bu():
    import math
    W, H = 380, 999
    body, y = head(W, H, "挫锐、解纷、和光、同尘：四步不是四德，是同一个动作落在四处",
                   "第 四 章 · 四 步", "四步", "挫其锐，解其纷，和其光，同其尘。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "四句都从「其」字起——「其」指的不是别人，是自己身上那四处。", 5.0, INK, "middle"))
    s.append(txt(190, y + 28, "四步排下来是一条路：先卸锋，再理结，再罩光，最后落到与尘同色。", 5.0, "#6E6459", "middle"))

    def cell(x, y0, lab, sub):
        s.append(f'<rect x="{x}" y="{y0}" width="158" height="170" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
        s.append(txt(x + 79, y0 + 18, lab, 5.4, SEAL, "middle"))
        s.append(txt(x + 79, y0 + 32, sub, 4.2, "#8A7C69", "middle"))

    gx1, gx2 = 22, 200
    gy1, gy2 = y + 56, y + 240

    # 一 挫其锐
    cell(gx1, gy1, "挫其锐", "磨去那句非要说赢的话")
    cx, cy = gx1 + 79, gy1 + 96
    # 磨石在下面，刀身斜搭上去
    s.append(f'<path d="M{cx - 46},{cy + 26} L{cx + 40},{cy + 26} L{cx + 34},{cy + 38} L{cx - 40},{cy + 38} z" fill="#E4D8BF" stroke="{INK}" stroke-width="0.9"/>')
    # 刀：背直、刃在下一侧，锋端已被磨圆
    s.append(f'<path d="M{cx - 40},{cy + 20} L{cx + 26},{cy - 34} L{cx + 34},{cy - 26} L{cx - 32},{cy + 28} z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx + 26},{cy - 34} q9,3 8,12" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<path d="M{cx - 30},{cy + 22} q14,-10 28,-18" fill="none" stroke="{GREEN}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    s.append(txt(cx + 4, cy + 52, "刀背还在，锋没了", 4.2, GREEN, "middle"))

    # 二 解其纷
    cell(gx2, gy1, "解其纷", "一团乱线，理出三根")
    cx, cy = gx2 + 79, gy1 + 96
    for d in [(0, 1), (1, -1), (2, 2)]:
        s.append(f'<path d="M{cx - 34},{cy - 22 + d[0] * 8} q20,{14 * d[1]} 42,{2 * d[0]} q14,-10 26,{4 * d[1]}" fill="none" stroke="{INK}" stroke-width="0.7" opacity="0.8"/>')
    for k in range(3):
        s.append(arrow(cx - 30, cy + 24 + k * 9, cx + 30, cy + 24 + k * 9, GREEN, 0.7, None, "arr2"))
    s.append(txt(cx, cy + 62, "不剪断，只理顺", 4.2, GREEN, "middle"))

    # 三 和其光
    cell(gx1, gy2, "和其光", "灯还亮，只是不刺眼")
    cx, cy = gx1 + 79, gy2 + 100
    s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for k in range(6):
        a = k * 60
        r1, r2 = 13, 20
        s.append(f'<line x1="{cx + r1 * math.cos(math.radians(a))}" y1="{cy + r1 * math.sin(math.radians(a))}" x2="{cx + r2 * math.cos(math.radians(a))}" y2="{cy + r2 * math.sin(math.radians(a))}" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<path d="M{cx - 26},{cy + 26} L{cx + 26},{cy + 26} L{cx + 18},{cy - 30} L{cx - 18},{cy - 30} z" fill="none" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="5 3"/>')
    s.append(txt(cx, cy + 42, "罩上去，光还在里面", 4.2, GREEN, "middle"))

    # 四 同其尘
    cell(gx2, gy2, "同其尘", "不躲尘，也不让尘显出来")
    cx, cy = gx2 + 79, gy2 + 100
    s.append(f'<path d="M{cx - 24},{cy - 22} q24,10 48,0 L{cx + 30},{cy + 30} L{cx - 30},{cy + 30} z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    for k in range(12):
        px = cx - 26 + (k * 11) % 54
        py = cy - 16 + (k * 7) % 42
        s.append(f'<circle cx="{px}" cy="{py}" r="1.1" fill="#B9A98F"/>')
    s.append(txt(cx, cy + 44, "衣与尘一色，才不显", 4.2, GREEN, "middle"))

    a = gy2 + 186
    s.append(txt(24, a, "四步落在一处：把「我」的锋、结、光、色，一样一样收回到与万物同的程度。", 5.4, INK))
    s.append(txt(24, a + 16, "收不是抹掉——刀背还在，线还在，灯还在，衣还在；只是不再靠它们站到人前去。", 5.4, INK))
    s.append(txt(24, a + 34, "「同其尘」最难：不是自甘低下，是不必再让人看见自己干净。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "磨的不是刀，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "是那句非要说赢的话。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch04c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


GOLD = {
    "ch07b": ["天地所以能长且久者，以其不自生，故能长生。", "为己者，取而入，入而塞；不为己者，生而出，出而复——差别不在善恶，在闭环。"],
    "ch07c": ["是以圣人后其身而身先，外其身而身存。", "先不是争来的，是人心自归的；退不是姿态，是把手松开。"],
    "ch08b": ["处众人之所恶，故几于道。", "低处不是惩罚，是不必守的位置。"],
    "ch08c": ["居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。", "七善是一条链，不是七条戒律。"],
    "ch09b": ["持而盈之，不如其已；揣而锐之，不可长保。", "持满则溢，不如早止。"],
    "ch09c": ["金玉满堂，莫之能守；富贵而骄，自遗其咎。", "退的不是事，是恋；收的不是手，是心。"],
    "ch10b": ["载营魄抱一，能无离乎？", "身在此时，心也回到此时。"],
    "ch10c": ["生而不有，为而不恃，长而不宰，是谓玄德。", "做得多，占得少。"],
    "ch11b": ["三十辐共一毂，当其无，有车之用。", "有给你抓手，无给你生机。"],
    "ch11c": ["凿户牖以为室，当其无，有室之用。", "封死填满，就只是一座土堆。"],
    "ch12b": ["五色令人目盲；五音令人耳聋；五味令人口爽。", "门照开，权收回：五样都进来，人就成了货架。"],
    "ch12c": ["是以圣人为腹不为目，故去彼取此。", "为腹者，以物养己；为目者，以物役己。"],
    "ch13b": ["宠为下，得之若惊，失之若惊。", "钉子一拔，风还在吹，壁不晃了。"],
    "ch13c": ["故贵以身为天下，若可寄天下；爱以身为天下，若可托天下。", "养身如养器，护壁不据壁。"],
    "ch14b": ["视之不见名曰夷，听之不闻名曰希，搏之不得名曰微。", "探不到的地方不是空的，是探针够不着。"],
    "ch14c": ["执古之道，以御今之有；能知古始，是谓道纪。", "古不是过去，是本始：一根不被风向吹弯的准绳。"],
    "ch15b": ["豫兮若冬涉川，犹兮若畏四邻。", "善为道者，走路像过冬河：每一步都自带敬意。"],
    "ch15c": ["夫唯不盈，故能蔽而新成。", "留一处不满，旧物就还在生长。"],
    "ch16b": ["致虚极，守静笃；万物并作，吾以观复。", "静不是把人按住，是把那只搅动的手放下。"],
    "ch16c": ["夫物芸芸，各复归其根。", "复归其根，是把今年长出来的、重新变成明年的底。"],
    "ch17b": ["太上，下知有之；其次亲而誉之；其次畏之；其次侮之。", "贵言：不是不说，是不拿话去替代事。"],
    "ch17c": ["功成事遂，百姓皆谓我自然。", "从中间退到边上，让事自己站着。"],
    "ch18b": ["大道废，有仁义；智慧出，有大伪。", "补丁越响，破处越深。"],
    "ch18c": ["六亲不和，有孝慈；国家昏乱，有忠臣。", "补丁可以救命，却不能代替布。"],
    "ch19b": ["见素抱朴，少私寡欲。", "素不是简陋，是不必再靠外加的东西来证明自己。"],
    "ch19c": ["绝圣弃智，民利百倍；绝巧弃利，盗贼无有。", "绝弃是减法：减到够用，事就成了。"],
    "ch20b": ["众人熙熙，如享太牢；我独泊兮其未兆。", "不必挤的那一处，站定了，人就轻了。"],
    "ch20c": ["众人皆有余，而我独若遗。", "空着的那只袋，看上去是缺，其实是余地。"],
    "ch21b": ["孔德之容，惟道是从。", "德之所以能容，正因它不占地方。"],
    "ch21c": ["自今及古，其名不去，以阅众甫。", "不是知道得多，是站对了地方。"],
    "ch22b": ["曲则全，枉则直，洼则盈，敝则新。", "弯的能受，所以能全；低的能聚，所以能盈。"],
    "ch22c": ["圣人抱一，为天下式。", "抱一，不是统一别人，是不让自己裂开。"],
    "ch23b": ["希言自然。飘风不终朝，骤雨不终日。", "天地做不出一场长雨，人也做不出一段长言。"],
    "ch23c": ["同于道者，道亦乐得之。", "你把自己放进什么里，就被什么收下。"],
    "ch06b": ["谷神不死，是谓玄牝。", "谷者，两山间之空也；能受故能生，生而不有故不竭——生机不在满处，在空处。"],
    "ch06c": ["玄牝之门，是谓天地根。", "门在开合处，不在门板上；一着手去推，它就成了一堵墙。"],
    "ch05b": ["天地不仁，以万物为刍狗。", "刍者，束草也；刍狗有位而无主——用毕回草堆，不是被弃，是位次用完了。"],
    "ch05c": ["多言数穷，不如守中。", "穷者，路走到头也；锁在 0、锁在 1、锁在自以为稳的中间——枢不动，机就死。"],
    "ch02b": ["天下皆知美之为美，斯恶已。", "立美那一刻，丑才成立——不是先有丑，再立美。"],
    "ch02c": ["音声相和，前后相随。", "和者，《说文》「相应也」；龢从龠从禾，训「调」——一唱一应，各自成声。"],
    "ch03b": ["不尚贤，使民不争；不贵难得之货，使民不为盗。", "尚者，抬之使高也；贵者，标之使重也——三个「不」，是一个动作：不主动起标。"],
    "ch03c": ["虚其心，实其腹；弱其志，强其骨。", "虚者，器中之空也；实者，壁之厚也——空在，壁才用得起来。"],
    "ch04b": ["道冲，而用之或不盈。", "冲者，虚也；《说文》「盅，器虚也」——器之所以为器，正在那处铸出来的空。"],
    "ch04c": ["挫其锐，解其纷，和其光，同其尘。", "锐者，锋也；锉者，磨也——磨的不是刀，是那句非要说赢的话。"],
    "ch74a": ["常有司杀者杀。", "司者，《说文》曰「臣司事于外者，从反后」；"],
    "ch74b": ["夫代司杀者杀，是谓代大匠斫。", "斫者，《说文》曰「击也」，从斤——一下而断，不可复也。"],
    "ch74c": ["夫代大匠斫者，希有不伤其手矣。", "希者，稀也，稀者疏也；"],
    "ch75a": ["民之饥，以其上食税之多，是以饥。", "飢者，《说文》曰「饿也」，腹空也；饑者，「谷不熟」也。"],
    "ch75b": ["民之难治，以其上之有为，是以难治。", "治者，《说文》曰「治，水，出东莱曲城阳丘山，南入海」——本为水名。"],
    "ch75c": ["夫唯无以生为者，是贤于贵生。", "贤者，《说文》曰「多才也」，从贝——本与财相关。"],
    "ch76a": ["人之生也柔弱，其死也坚强。", "柔者，《说文》曰「木曲直也」——曲者可直，直者可曲。"],
    "ch76b": ["故坚强者死之徒，柔弱者生之徒。", "徒者，《说文》曰「步行也」，从辵从土——其字本在走。"],
    "ch76c": ["是以兵强则灭，木强则折。", "折者，《说文》曰「断也，从斤断艸」——斧落于草。"],
    "ch77a": ["天之道，其犹张弓与？", "张者，《说文》曰「施弓弦也」——非拉弓也，上弦也。"],
    "ch77b": ["有余者损之，不足者补之。", "补者，《说文》曰「完衣也」——缝也，非给也。"],
    "ch77c": ["人之道则不然，损不足以奉有余。", "奉者，《说文》曰「承也」，从手从廾——两手捧而献之。"],
    "ch78a": ["天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。", "易者，《说文》曰「蜥蜴」，一说象两器倾水之形。"],
    "ch78b": ["受国之垢，是谓社稷主。", "垢者，《说文》曰「浊也」，从土——垢即土也。"],
    "ch78c": ["受国不祥，是为天下王。", "社者，《说文》曰「地主也」，从示土——土神也。"],
    "ch79a": ["是以圣人执左契，而不责于人。", "契者，刻木为信，一剖两半；左契在债权人手，右契在负债者手。"],
    "ch79b": ["有德司契，无德司彻。", "彻者，通也；司彻者，通篇算之，故其数日新。"],
    "ch79c": ["天道无亲，常与善人。", "亲者，近也；无亲者，不偏向也。"],
    "ch80a": ["使民复结绳而用之。", "结绳者，大事大结，小事小结；只有数，无字。"],
    "ch80b": ["虽有舟舆，无所乘之。", "舟者，能行之物；不乘者，有而不启动。"],
    "ch80c": ["邻国相望，鸡犬之声相闻，民至老死不相往来。", "不相往来者，非不能往，是不必往。"],
    "ch81a": ["圣人不积，既以为人，己愈有。", "积者，存也；不积者，不把天下往怀里拐。"],
    "ch81b": ["既以与人，己愈多。", "与人者，予之也；愈多者，泉不因取竭。"],
    "ch81c": ["天之道，利而不害；圣人之道，为而不争。", "利者，顺也；不害者，不逆也。"],
    "ch73a": ["勇于敢则杀，勇于不敢则活。", "气无方向，向由敢定；"],
    "ch73b": ["繟者，《说文》曰「带缓也」，从糸——带系之松也。", "人之谋也系紧，紧则勒，勒处即崩处；"],
    "ch73c": ["天网恢恢，疏而不失。", "疏者，《说文》曰「通也」，非稀也；"],
    "ch72a": ["威从女从戌，戌者斧也；《说文》曰「姑也」——姑者，妇之尊长。", "斧备而不用，用则威亡；用斧者为人所还，还则堂不能安。"],
    "ch72b": ["无狎其所居，无厌其所生。", "狎者，犬可习也，熟而贴人；非屋之窄，乃无距也。"],
    "ch72c": ["自知不自见，自爱不自贵。", "故去彼取此。"],
    "ch71a": ["知不知，尚矣；不知知，病也。", "知从矢从口：箭出而中，报之于口。"],
    "ch71b": ["知不知，尚矣；不知知，病也。", "知者，命中之事，非胸中之有。"],
    "ch71c": ["《说文》曰：病，疾加也。", "病者，目中见靶外之箭，胸中箭犹在靶。"],
    "ch70a": ["吾言甚易知，甚易行；天下莫能知，莫能行。", "易者，非浅也，直也；无仪式，无秘传，无门槛——而无人走，故难不在道。"],
    "ch70b": ["吾言甚易知，甚易行；天下莫能知，莫能行。", "易者，非浅也，直也；无仪式，无秘传，无门槛——而无人走，故难不在道。"],
    "ch70c": ["吾言甚易知，甚易行；天下莫能知，莫能行。", "易者，非浅也，直也；无仪式，无秘传，无门槛——而无人走，故难不在道。"],
    "ch69a": ["主者，灯中一火，众物绕之；客者，寄也，宿于人家之屋。", "不敢为主者，非不能战，乃不敢使此战归我所有。"],
    "ch69b": ["斗伯比一眼而知其败：举趾高，心不固矣。", "轻敌先长在脚上，脚一抬，三宝先落。"],
    "ch69c": ["哀者，闵也；闵者，吊者在门。", "哀不是憋着一口气，是不忍：看见门里还有人活着。"],
    "ch68a": ["武从止从戈，止者足也；非扔其戈，乃停其足。", "定功戢兵——功先定，刀后收；胜而不收者，犹未胜也。"],
    "ch68b": ["与者党与，四手抬一物；争者两手引一物，皆须有对。", "不与：不给对手，就没有争；不跟敌人配对，却跟天配上了。"],
    "ch68c": ["力者，筋也；筋不使劲，筋是连。", "善用人者为之下：站低一处，众人的劲才连成一根筋。"],
    "ch67a": ["慈从心兹，兹者草木多益；心中自有草长，不问其落于何处。", "爱护一棵，慈护一片：护的时候不拼命，反而极稳。"],
    "ch67b": ["俭者约也，约者绳缠束；收十处为一束，一束可推千里。", "俭不是怕花钱，是怕散：散在十处，十处都不深。"],
    "ch67c": ["衛从行从帀，帀者周也；慈是围墙不是盾牌，盾挡一面，墙围一圈。", "天将救之，以慈卫之：不是外面拉一把，是自己被围住，伤不着。"],
    "ch66a": ["谷不是山的凹，是水的路；不是谷招水，是水自己往低处走。", "王是天下所归往：往者自至，非呼而来；海以纳百川名，不以大名。"],
    "ch66b": ["重者，人背一囊；害者，旗下取物。", "处上而民不重：不是不上，是上了让人不觉得沉。"],
    "ch66c": ["厭从厂从猒，饱兽压崖；非嫌其人也，乃觉其沉。", "天下乐推而不厌：送上去，不觉得沉。"],
    "ch65a": ["明是打光，不是自己亮；灯照路，不照人。", "明民是打光：光一打，位置就显出来；看得清，就生比较。"],
    "ch65b": ["愚从心从禺：禺是猴，猴不蠢，是停不住；心跟着猴跑，才是那个愚字。", "收心是把猴从肩上放下来：放下来它还在，只是不再拽着心跑。"],
    "ch65c": ["稽式是木工弹的那道线：它不评价，只显出来；常知稽式，是谓玄德。", "线一响，歪的木头自己就显出来了。"],
    "ch64a": ["兆是烧出来的那道裂纹；还没烧，就还读不出来——也还来得及。", "未兆不是征兆还小，是还没裂；趁它没裂，才来得及决定它裂成什么样。"],
    "ch64b": ["九层之台，起于累土；台有多高，等于抬过多少筐。", "千里之行，始于足下：远不是一步跨过去的，是一步一步攒出来的。"],
    "ch64c": ["牙自己长，骨头只托；辅万物之自然，就是托住，不去捏。", "托得好，牙正；托得歪，牙斜；骨头一动，满口都疼。"],
    "ch63a": ["图是「画计难」：先把难画出来，才有得打算；趁它还小，笔才落得下去。", "味是尝还没熟的，图是先把难画出来——都在事情还没长成的时候动手。"],
    "ch63b": ["细从糸，微也：一根一根，不断；大事是一束，可它只能一根一根抽出来。", "天下大事，必作于细：不是先有大石，是先有一根一根的线。"],
    "ch63c": ["易本是蜥蜴：会变色，会断尾；看得容易，是没看见它会变。", "轻诺必寡信，多易必多难；圣人犹难之，故终无难。"],
    "ch62a": ["奥是那个不见光的西南角；坐进，是坐着往上走。", "奥是最尊又最暗的那个角；尊，是没人敢坐；暗，是光进不去。"],
    "ch62b": ["宝是自己收着的，保是背着孩子的；一个揣在怀里，一个驮在背上。", "收留是给个地方，背着是驮在身上——走到哪儿带到哪儿。"],
    "ch62c": ["坐是停，进是登；这条路上的「进」，脚一步也不用迈。", "拱是两手收起来往前献，坐是手放开往下停；一个送一次，一个待一辈子。"],
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
    "ch61a": ["下游不是被推下去的，它本来就在那儿；不往上争的水，上游非来不可。"],
    "ch61b": ["「胜」是担得起，不是打得赢；母畜担得起，因为后面那一群都是它生的。"],
    "ch61c": ["取本义带刀；加一个「下」，刀就翻成了手——不是去割，是去接。"],
    "ch60a": ["烹小鲜的诀是不翻；这一章不教人怎么把事做成，教人做成了之后别再去动它。"],
    "ch60b": ["莅是草长到那个位置，不是人坐上去发令；一个到，一个管。"],
    "ch60c": ["交是两条腿交叉，不是两股绳拧成一股；各让一条腿，才各回各家。"],
    "ch59a": ["啬不是舍不得给，是把收下来的拢回仓里；这一章不是讲节俭，是讲收成。"],
    "ch59b": ["克是肩，不是刀；「无不克」不是打遍天下，是天下事都担得起。"],
    "ch59c": ["根是横着铺的，柢是竖着扎的；铺满一层挡不住风，扎死一根才挡得住。"],
    "ch58a": ["闷是把心关在门里，察是盖过来翻着看；一个是关，一个是翻。"],
    "ch58b": ["祸不是等在福后面，是靠在福身上；它们一直贴着，所以换的时候不用通知。"],
    "ch58c": ["方是两条船并着；并着不动刀，一动刀就成了界。"],
    "ch57a": ["正，是脚站定；一个政策最大的德，是明年还是它。"],
    "ch57b": ["奇是落单的一手；会用，但不能落单成习惯。"],
    "ch57c": ["彰是画上去的花；条文画得越花，能踩的线就越多。"],
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
def ch23b_zhou_yu():
    body, y = head(380, 999, "飘风不终朝，骤雨不终日：天地的力气也撑不久",
                   "第 二 十 三 章 · 一 场 骤 雨", "一场骤雨", "孰为此者？天地。天地尚不能久，而况于人乎？", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「希言自然」：话少，才合乎自然的走法；多言即用力，用力必不久。", 4.7, INK, "middle"))
    s.append(txt(190, y + 27, "先把「不久」这件事，交给天地自己演一遍。", 4.7, "#6E6459"))

    # 一、骤雨
    s.append(txt(24, y + 52, "一、骤雨：来得猛，走得也快；旁边的更漏只走了一小格", 5.1, SEAL))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="140" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    for k in range(14):
        x = 44 + k * 13
        s.append(f'<line x1="{x}" y1="{gy + 16}" x2="{x - 9}" y2="{gy + 62}" stroke="#8A7C69" stroke-width="0.8" opacity="0.75"/>')
    s.append(f'<ellipse cx="150" cy="{gy + 14}" rx="112" ry="14" fill="#EFE6D4" opacity="0.75" stroke="none"/>')
    s.append(f'<ellipse cx="96" cy="{gy + 12}" rx="52" ry="11" fill="#EFE6D4" opacity="0.6" stroke="none"/>')
    s.append(f'<ellipse cx="206" cy="{gy + 12}" rx="46" ry="10" fill="#EFE6D4" opacity="0.6" stroke="none"/>')
    s.append(f'<path d="M36,{gy + 68} q40,8 84,2 q46,-6 92,2 q44,8 86,-1" fill="none" stroke="{LINE2}" stroke-width="1.0"/>')
    s.append(txt(70, gy + 84, "一阵就过", 4.0, "#8A7C69"))
    # 更漏
    s.append(f'<path d="M232,{gy + 30} L268,{gy + 30} L262,{gy + 46} L252,{gy + 78} L248,{gy + 78} L238,{gy + 46} Z" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="232" y1="{gy + 30}" x2="268" y2="{gy + 30}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M238,{gy + 52} L262,{gy + 52} L256,{gy + 74} L244,{gy + 74} Z" fill="#EFE6D4" stroke="none"/>')
    for yy in [gy + 40, gy + 46, gy + 52]:
        s.append(f'<line x1="236" y1="{yy}" x2="240" y2="{yy}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(292, gy + 44, "只走一格", 3.9, SEAL))
    s.append(f'<line x1="286" y1="{gy + 48}" x2="256" y2="{gy + 48}" stroke="{LINE}" stroke-width="0.5"/>')
    s.append(f'<path d="M232,{gy + 100} L272,{gy + 100}" stroke="none"/>')
    s.append(txt(250, gy + 104, "更漏：量时之物，此处只量到一小段", 3.8, "#8A7C69", "middle"))
    s.append(txt(150, gy + 124, "飘风不终朝，骤雨不终日：连天地也做不出一场长雨", 4.2, SEAL, "middle"))

    # 二、多言
    s.append(txt(24, gy + 164, "二、多言即用力：一口气喊出去，声圈越散越淡", 5.1, GREEN))
    gy2 = gy + 176
    s.append(f'<rect x="26" y="{gy2}" width="328" height="150" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    px, py = 104, gy2 + 54
    s.append(f'<circle cx="{px}" cy="{py}" r="6.4" fill="none" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{px}" y1="{py + 7}" x2="{px}" y2="{py + 44}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="{px}" y1="{py + 44}" x2="{px - 8}" y2="{py + 62}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px}" y1="{py + 44}" x2="{px + 8}" y2="{py + 62}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px}" y1="{py + 20}" x2="{px + 16}" y2="{py + 12}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="{px}" y1="{py + 22}" x2="{px - 14}" y2="{py + 30}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M{px + 12},{py - 2} q10,6 0,12" fill="none" stroke="{SEAL}" stroke-width="0.8"/>')
    for k, (rx, ry, op) in enumerate([(16, 10, 0.9), (30, 18, 0.6), (44, 26, 0.35), (58, 34, 0.2)]):
        s.append(f'<ellipse cx="{px + 26 + k * 6}" cy="{py + 4}" rx="{rx}" ry="{ry}" fill="none" stroke="{SEAL}" stroke-width="0.8" opacity="{op}"/>')
    s.append(txt(px + 96, py - 22, "越散越淡", 4.0, SEAL))
    for k in range(3):
        s.append(f'<line x1="{286 + k * 14}" y1="{gy2 + 34}" x2="{300 + k * 14}" y2="{gy2 + 34}" stroke="#DCCFBB" stroke-width="0.6"/>')
    s.append(txt(300, gy2 + 26, "风已经停了", 3.8, "#8A7C69", "middle"))
    s.append(txt(190, gy2 + 132, "话一多，就得一直用力把它撑着；一停，就不见了", 4.2, GREEN, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "天地做不出一场长雨，人也做不出一段长言：这不是悲观，是把力的限度先量清。", 4.8, INK))
    s.append(txt(24, a + 16, "「希言」不是不说话，是不拿话去替代那件要长久的事。", 4.8, INK))
    s.append(txt(24, a + 34, "飘风骤雨之后，地还是干的；话说尽之后，事还是没动。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "希言自然。飘风不终朝，骤雨不终日。", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "天地尚不能久，而况于人乎？", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch23b"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


def ch23c_yan_ru_shui():
    body, y = head(380, 999, "同于道者，道亦乐得之：你把自己放进什么里，就被什么收下",
                   "第 二 十 三 章 · 一 撮 盐", "一撮盐", "同于道者，道亦乐得之；同于失者，失亦乐得之。", 999)
    s = [body]

    s.append(box(20, y + 2, 340, 34, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「从事于道者，同于道」：你实行什么，就与什么同类。", 4.8, INK, "middle"))
    s.append(txt(190, y + 27, "同类的东西互相收留，不必去求它收。", 4.8, "#6E6459"))

    # 一、盐入水
    s.append(txt(24, y + 52, "一、盐入水：化开，看不见了——水把它收下", 5.1, GREEN))
    gy = y + 64
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    bx, by, bw, bh = 96, gy + 34, 130, 78
    s.append(f'<path d="M{bx},{by} L{bx + 8},{by + bh} L{bx + bw - 8},{by + bh} L{bx + bw},{by} Z" fill="#E9F0E6" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<ellipse cx="{bx + bw / 2}" cy="{by}" rx="{bw / 2}" ry="7" fill="{PAPER}" stroke="{INK}" stroke-width="1.0"/>')
    s.append(f'<line x1="{bx + 6}" y1="{by + 18}" x2="{bx + bw - 6}" y2="{by + 18}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    s.append(txt(bx + bw / 2, by + 14, "水面", 3.7, GREEN, "middle"))
    s.append(f'<path d="M{bx + 30},{by + 44} q22,-8 44,2 q22,10 46,0" fill="none" stroke="{GREEN}" stroke-width="0.6" opacity="0.6"/>')
    s.append(f'<path d="M{bx + 26},{by + 58} q24,-8 48,2 q22,10 44,-1" fill="none" stroke="{GREEN}" stroke-width="0.6" opacity="0.4"/>')
    s.append(txt(bx + bw / 2, by + 70, "盐已化尽，颗粒不在", 3.8, GREEN, "middle"))
    s.append(f'<line x1="{bx + 34}" y1="{by - 22}" x2="{bx + 30}" y2="{by - 6}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M{bx + 26},{by - 4} q6,5 12,0" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(bx + 20, by - 28, "一撮盐", 3.9, INK))
    s.append(txt(190, gy + 132, "化在水里：不是消失，是归到同类那儿去了", 4.2, GREEN, "middle"))

    # 二、盐上石
    s.append(txt(24, gy + 178, "二、盐上石：不进，就堆在面上；风一过，也留不住", 5.1, SEAL))
    gy2 = gy + 190
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<path d="M66,{gy2 + 116} Q78,{gy2 + 62} 128,{gy2 + 46} Q186,{gy2 + 30} 214,{gy2 + 62} Q232,{gy2 + 88} 244,{gy2 + 116} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M96,{gy2 + 104} Q120,{gy2 + 66} 150,{gy2 + 56} M140,{gy2 + 110} Q170,{gy2 + 76} 196,{gy2 + 70}" fill="none" stroke="{LINE2}" stroke-width="0.7"/>')
    for k in range(6):
        s.append(f'<circle cx="{152 + (k % 3) * 9}" cy="{gy2 + 40 - (k // 3) * 5}" r="1.6" fill="#8A7C69"/>')
    s.append(txt(182, gy2 + 30, "盐堆在石面上，进不去", 3.9, SEAL))
    for k in range(3):
        s.append(f'<line x1="{92 + k * 9}" y1="{gy2 + 20}" x2="{168 + k * 9}" y2="{gy2 + 20}" stroke="#B7A99A" stroke-width="0.7"/>')
    s.append(arrow(196, gy2 + 20, 224, gy2 + 20, "#B7A99A", 0.7, None, "arr2"))
    s.append(txt(228, gy2 + 15, "风过，盐散", 3.8, "#8A7C69"))
    for k in range(4):
        s.append(f'<circle cx="{226 + k * 8}" cy="{gy2 + 32 + (k % 2) * 5}" r="1.2" fill="#8A7C69" opacity="{0.6 - k * 0.12}"/>')
    s.append(txt(190, gy2 + 132, "「信不足焉，有不信焉」：没进到那一处，就谈不上信", 4.2, SEAL, "middle"))

    a = gy2 + 174
    s.append(txt(24, a, "盐入水则化，入石则堆：同一撮盐，收不收在它落的地方。", 4.8, INK))
    s.append(txt(24, a + 16, "「同于失者，失亦乐得之」：不是惩罚，是你站在哪儿，哪儿就把你计入。", 4.8, INK))
    s.append(txt(24, a + 34, "所以要紧的不是求它收，是先看清自己落在哪一层。", 4.8, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "同于道者，道亦乐得之。", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "信不足焉，有不信焉。", 5.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch23c"))
    s.append('</svg>')
    out = "\n".join(s)
    ys = [float(v) for v in re.findall(r'y="([0-9.]+)"', out)]
    return out.replace("999", str(int(max(ys) + 26)))


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
    W, H = 380, 700
    body, y = head(W, H, "常心是一把自己打的尺：尺一横在人头顶，人就只剩一个读数",
                   "第 四 十 九 章 · 尺", "一把尺", "圣人无常心，以百姓心为心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「常」这个字最骗人：它听着像天理，其实是你自己的习惯。", 5.2, INK, "middle"))
    s.append(txt(190, y + 27, "一把尺在手，万物皆有长短；放下尺，不是没有标准，是不再拿它钉人。", 5.0, "#6E6459", "middle"))

    def person(cx, base, hh):
        top = base - hh
        s.append(f'<circle cx="{cx}" cy="{top + 6}" r="5.6" fill="none" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{cx}" y1="{top + 12}" x2="{cx}" y2="{base - 18}" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<line x1="{cx}" y1="{top + 22}" x2="{cx - 7}" y2="{top + 32}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{cx}" y1="{top + 22}" x2="{cx + 7}" y2="{top + 32}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<line x1="{cx}" y1="{base - 18}" x2="{cx - 6}" y2="{base}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{cx}" y1="{base - 18}" x2="{cx + 6}" y2="{base}" stroke="{INK}" stroke-width="1"/>')
        return top

    # 一、有常心：一把尺压在头顶
    s.append(txt(24, y + 50, "一、有常心：一把尺压在头顶", 5.2, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base = gy + 128
    s.append(f'<line x1="40" y1="{base}" x2="330" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    ruler_y = gy + 22
    s.append(box(44, ruler_y, 244, 9, fill="#EFE6D4", stroke=INK, width=1))
    for k in range(9):
        s.append(f'<line x1="{58 + k * 27}" y1="{ruler_y}" x2="{58 + k * 27}" y2="{ruler_y + 3.2}" stroke="{INK}" stroke-width="0.5"/>')
    s.append(f'<line x1="44" y1="{ruler_y + 9}" x2="288" y2="{ruler_y + 9}" stroke="{SEAL}" stroke-width="1.1" stroke-dasharray="6 3"/>')
    s.append(txt(296, ruler_y + 8, "合格线", 4.4, SEAL))
    for cx, hh, lab, pass_it in [(86, 96, "甲", True), (148, 72, "乙", False), (210, 48, "丙", False)]:
        top = person(cx, base, hh)
        if pass_it:
            s.append(f'<line x1="{cx}" y1="{top + 0.4}" x2="{cx}" y2="{ruler_y + 9}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 2"/>')
            s.append(txt(cx, base + 14, "甲：够得到", 4.3, GREEN, "middle"))
        else:
            s.append(f'<line x1="{cx}" y1="{top + 0.4}" x2="{cx}" y2="{top - 20}" stroke="{SEAL}" stroke-width="0.6" stroke-dasharray="3 2"/>')
            s.append(txt(cx, base + 14, lab + ("：差一截" if hh == 72 else "：差两截"), 4.3, SEAL, "middle"))
    s.append(txt(190, gy + 156, "尺一压下来，人就成了刻度上的一个读数", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 184, "尺一伸出去，话就跟着出去；尺压在头顶，人就被钉住", 4.6, GREEN, "middle"))

    # 二、无常心：尺插回腰间
    s.append(txt(24, gy + 208, "二、无常心：尺收回腰间，人还是三个人", 5.2, GREEN))
    gy2 = gy + 220
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    base2 = gy2 + 128
    s.append(f'<line x1="40" y1="{base2}" x2="330" y2="{base2}" stroke="{INK}" stroke-width="1"/>')
    for cx, hh, lab in [(86, 96, "甲"), (148, 72, "乙"), (210, 48, "丙")]:
        top = person(cx, base2, hh)
        s.append(txt(cx, base2 + 14, lab, 4.5, "#6E6459", "middle"))
    # 甲的腰间一道带，尺斜插在里面，露出半截
    s.append(f'<path d="M79,{base2 - 44} q7,3 14,0" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="92" y1="{base2 - 42}" x2="124" y2="{base2 - 54}" stroke="#EFE6D4" stroke-width="3.4"/>')
    s.append(f'<line x1="92" y1="{base2 - 42}" x2="124" y2="{base2 - 54}" stroke="{GREEN}" stroke-width="1.4"/>')
    for k in range(3):
        s.append(f'<line x1="{100 + k * 8}" y1="{base2 - 44 - k * 3}" x2="{100 + k * 8}" y2="{base2 - 40 - k * 3}" stroke="{INK}" stroke-width="0.5"/>')
    s.append(txt(238, gy2 + 44, "尺插回腰间：还在，", 4.4, GREEN))
    s.append(txt(238, gy2 + 56, "不横在人头顶", 4.4, GREEN))
    s.append(txt(190, gy2 + 184, "头顶那道虚线没有了：不把人划到哪一栏里去", 4.6, GREEN, "middle"))

    a = gy2 + 208
    s.append(txt(24, a, "尺量长短，是它本分；尺压在头顶，它就把人钉住了。", 5.4, INK))
    s.append(txt(24, a + 16, "「以百姓心为心」不是照他们说的做，是不把他们划到哪一栏里去。", 5.4, INK))
    s.append(txt(24, a + 34, "这一章不是教人宽容，是教人把自己那把尺认出来，然后松开手。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "一把尺能定长短，", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "也能把人钉在短的那一格里。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch49a"))
    s.append('</svg>')
    return "\n".join(s)


def ch49b_yi_tiao_qu():
    W, H = 380, 690
    body, y = head(W, H, "百姓把耳目当灌渠往外灌，圣人把渠口收一寸",
                   "第 四 十 九 章 · 渠", "一条渠", "歙歙焉，为天下浑其心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「注」，《说文》「灌也」——水往一处灌；「歙」，「缩鼻也」——鼻子往里一缩。", 5.0, INK, "middle"))
    s.append(txt(190, y + 27, "全章的对位就在这一出一入：往外灌的是耳目，往里收的是那口气。", 5.0, "#6E6459", "middle"))

    def head_at(cx, cy, lab):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="19" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<circle cx="{cx - 6.5}" cy="{cy - 4}" r="1.6" fill="{INK}"/>')
        s.append(f'<circle cx="{cx + 6.5}" cy="{cy - 4}" r="1.6" fill="{INK}"/>')
        s.append(txt(cx, cy - 27, lab, 4.6, "#6E6459", "middle"))

    def ditch(x0, y0, x1, water_dir, gate=False):
        """一条渠的剖面：两道岸、渠底、渠里的水。"""
        s.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<line x1="{x0}" y1="{y0 + 22}" x2="{x1}" y2="{y0 + 22}" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<rect x="{x0 + 3}" y="{y0 + 12}" width="{x1 - x0 - 6}" height="7" fill="{GREEN}" opacity="0.35"/>')
        # 水纹
        s.append(f'<path d="M{x0 + 6},{y0 + 12} h{x1 - x0 - 12}" stroke="{GREEN}" stroke-width="0.8"/>')
        if water_dir > 0:
            for k in range(4):
                xx = x0 + 30 + k * 44
                s.append(arrow(xx, y0 + 15, xx + 26, y0 + 15, SEAL, 0.7, head="arrS"))
        else:
            for k in range(3):
                xx = x1 - 40 - k * 46
                s.append(arrow(xx, y0 + 15, xx - 26, y0 + 15, GREEN, 0.7, head="arr2"))
        if gate:
            s.append(f'<line x1="{x1}" y1="{y0 - 2}" x2="{x1}" y2="{y0 + 24}" stroke="{SEAL}" stroke-width="1.6"/>')
            s.append(f'<line x1="{x1 - 8}" y1="{y0}" x2="{x1 - 8}" y2="{y0 + 22}" stroke="{SEAL}" stroke-width="1"/>')

    # 一、注：两条渠，口都朝外
    s.append(txt(24, y + 50, "一、注：耳目两条渠，口都朝外", 5.2, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy + 130}" x2="330" y2="{gy + 130}" stroke="{INK}" stroke-width="1"/>')
    head_at(74, gy + 66, "百姓")
    ditch(96, gy + 44, 300, +1)
    ditch(96, gy + 88, 300, +1)
    # 渠口断了岸，水淌出去
    for k in range(3):
        s.append(f'<circle cx="{306 + k * 6}" cy="{gy + 78 + k * 7}" r="1.9" fill="{SEAL}" opacity="0.5"/>')
    s.append(txt(150, gy + 36, "眼睛一条渠", 4.2, "#6E6459"))
    s.append(txt(150, gy + 126, "耳朵一条渠", 4.2, "#6E6459"))
    s.append(txt(302, gy + 40, "口朝外", 4.2, SEAL))
    s.append(txt(190, gy + 156, "看见什么、听见什么，心就在哪儿：水一开就关不上", 4.5, GREEN, "middle"))
    s.append(txt(190, gy + 184, "百姓把耳目当灌渠，往外灌", 4.6, GREEN, "middle"))

    # 二、歙：把口收一寸
    s.append(txt(24, gy + 208, "二、歙：把口收一寸，不堵死", 5.2, GREEN))
    gy2 = gy + 220
    s.append(f'<rect x="26" y="{gy2}" width="328" height="168" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    s.append(f'<line x1="40" y1="{gy2 + 130}" x2="330" y2="{gy2 + 130}" stroke="{INK}" stroke-width="1"/>')
    head_at(74, gy2 + 66, "圣人")
    ditch(96, gy2 + 44, 292, -1, gate=True)
    ditch(96, gy2 + 88, 292, -1, gate=True)
    s.append(txt(296, gy2 + 36, "口收窄", 4.2, SEAL))
    s.append(txt(190, gy2 + 156, "收住不是堵死：堵死是「防民之口」，收住是自己不往外灌", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 184, "圣人做的事，是把灌口往回收一寸", 4.6, GREEN, "middle"))

    a = gy2 + 208
    s.append(txt(24, a, "大家都往外灌，就没人吸；没人吸，那个场就干了。", 5.4, INK))
    s.append(txt(24, a + 16, "注是结构，不是罪状：眼睛看什么，心就在哪儿。", 5.4, INK))
    s.append(txt(24, a + 34, "所以圣人第一件事不是多说，是把灌口往回收一寸。", 5.2, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「歙」是吸，「注」是灌；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "一个往里收，一个往外倒。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch49b"))
    s.append('</svg>')
    return "\n".join(s)


def ch49c_hun_shui_sheng():
    W, H = 380, 660
    body, y = head(W, H, "浑是水混着流的声音：水还在流，只是不再一格一格地流",
                   "第 四 十 九 章 · 浑", "浑，是水声", "为天下浑其心。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 32, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「浑」，《说文》「混流声也」——水混着流的声音。", 5.2, INK, "middle"))
    s.append(txt(190, y + 27, "不是糊涂，不是把人弄傻：是让被切碎的心重新连成一片。", 5.0, "#6E6459", "middle"))

    # 一、一格一格：五格死水
    s.append(txt(24, y + 50, "一、一格一格：每滴都在自己的格子里", 5.2, SEAL))
    gy = y + 62
    s.append(f'<rect x="26" y="{gy}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ty, by = gy + 46, gy + 118
    for xv in (40, 104, 168, 232, 296, 330):
        s.append(f'<line x1="{xv}" y1="{ty}" x2="{xv}" y2="{by}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="40" y1="{ty}" x2="330" y2="{ty}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(f'<line x1="40" y1="{by}" x2="330" y2="{by}" stroke="{INK}" stroke-width="1"/>')
    for (xa, xb) in [(40, 104), (104, 168), (168, 232), (232, 296), (296, 330)]:
        wy = by - 26
        s.append(f'<line x1="{xa + 6}" y1="{wy}" x2="{xb - 6}" y2="{wy}" stroke="{GREEN}" stroke-width="0.9"/>')
    s.append(txt(190, gy + 136, "五格，五潭死水：一格不流到另一格", 4.5, SEAL, "middle"))
    s.append(txt(190, gy + 174, "墙一道一道立着：好坏、得失、敌我，每一刀都切得很准", 4.5, GREEN, "middle"))

    # 二、浑：墙软下来，水连成一片，并出声
    s.append(txt(24, gy + 192, "二、浑：墙软下来，水连成一片，也出了声", 5.2, GREEN))
    gy2 = gy + 204
    s.append(f'<rect x="26" y="{gy2}" width="328" height="152" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    ty2, by2 = gy2 + 46, gy2 + 118
    s.append(f'<line x1="40" y1="{by2}" x2="330" y2="{by2}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="40" y1="{ty2}" x2="330" y2="{ty2}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="4 3"/>')
    for xv in (40, 330):
        s.append(f'<line x1="{xv}" y1="{ty2}" x2="{xv}" y2="{by2}" stroke="{INK}" stroke-width="1"/>')
    for xv in (104, 168, 232, 296):
        s.append(f'<line x1="{xv}" y1="{ty2}" x2="{xv}" y2="{by2}" stroke="{LINE2}" stroke-width="0.5" stroke-dasharray="3 3"/>')
    s.append(f'<path d="M44,{by2 - 26} q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0 q16,-9 32,0 q16,9 32,0 q14,-7 28,-1" '
             f'fill="none" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(arrow(60, ty2 + 12, 168, ty2 + 12, GREEN, 0.7, head="arr2"))
    s.append(txt(174, ty2 + 14, "还是有流向", 4.5, GREEN))
    # 水声：从水面升起的三道弧
    for k, (cx, ry, op) in enumerate([(222, 9, 0.85), (246, 7, 0.6), (270, 5, 0.4)]):
        s.append(f'<path d="M{cx},{by2 - 56} q8,-{ry} 16,0" fill="none" stroke="{GREEN}" stroke-width="0.9" opacity="{op}"/>')
    s.append(txt(246, by2 - 66, "混流声也", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 136, "格子软了，水重新连成一片", 4.5, GREEN, "middle"))
    s.append(txt(190, gy2 + 174, "不是没有分别，是不再一格一格站着", 4.5, GREEN, "middle"))

    a = gy2 + 192
    s.append(txt(24, a, "一个时代的心被切碎，不是切得不准，是切得太准。", 5.4, INK))
    s.append(txt(24, a + 16, "每一刀都对，可每个人都站进了一个很小的格子。", 5.4, INK))
    s.append(txt(24, a + 34, "浑，是把格子的墙软下来——水才又能流到别人那儿去，也才重新有声。", 5.2, GREEN))

    c = a + 52
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


# ============ 第五十七章 · 一只脚 ============
def ch57a_yi_zhi_jiao():
    W, H = 380, 604
    body, y = head(W, H, "以正治国：正从止，是一只脚停在它该在的地方",
                   "第 五 十 七 章 · 正", "一只脚", "以正治国，以奇用兵，以无事取天下。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「正」从止——止就是脚趾，正的本义是「一只脚停在它该在的地方」。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以正不是「对」，是不动：脚不乱换地方，那个地方才立得住。", 5.2, "#6E6459", "middle"))

    def foot(cx, cy, col, dash=0, fill=None):
        o = []
        d = f' stroke-dasharray="{dash}"' if dash else ''
        fl = f' fill="{fill}"' if fill else ' fill="none"'
        o.append(f'<path d="M{cx-9},{cy-12} C{cx-11},{cy-2} {cx-10},{cy+9} {cx-4},{cy+14} C{cx+2},{cy+18} {cx+8},{cy+10} {cx+9},{cy-2} C{cx+10},{cy-11} {cx+6},{cy-17} {cx-1},{cy-17} C{cx-6},{cy-17} {cx-8},{cy-16} {cx-9},{cy-12} Z" stroke="{col}" stroke-width="1"{d}{fl}/>')
        o.append(f'<circle cx="{cx-6}" cy="{cy-20}" r="2.3" stroke="{col}" stroke-width="0.8"{d}{fl}/>')
        o.append(f'<circle cx="{cx-1.5}" cy="{cy-23}" r="2.0" stroke="{col}" stroke-width="0.8"{d}{fl}/>')
        o.append(f'<circle cx="{cx+2.5}" cy="{cy-22}" r="1.7" stroke="{col}" stroke-width="0.8"{d}{fl}/>')
        o.append(f'<circle cx="{cx+6}" cy="{cy-19}" r="1.5" stroke="{col}" stroke-width="0.8"{d}{fl}/>')
        return o

    # 一、脚乱换地方
    t1 = y + 46
    s.append(txt(24, t1, "一、脚乱换地方：换个地方，就换一套说法", 5.4, SEAL))
    gy1 = t1 + 116
    s.append(f'<line x1="24" y1="{gy1}" x2="246" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    for cx in (66, 124, 182):
        s += foot(cx, gy1 - 20, SEAL, dash="4 3")
    s.append(arrow(58, gy1 - 62, 118, gy1 - 62, SEAL, 0.7, head="arrS"))
    s.append(arrow(120, gy1 - 56, 176, gy1 - 56, SEAL, 0.7, head="arrS"))
    s.append(txt(140, gy1 - 72, "年年换新法", 4.8, SEAL, "middle"))
    s.append(txt(66, gy1 + 14, "三个规矩，三只脚，哪一只都不常", 4.6, "#6E6459"))

    # 二、脚站定
    t2 = gy1 + 40
    s.append(txt(24, t2, "二、脚站定：同一个地方，明年还是它", 5.4, GREEN))
    gy2 = t2 + 116
    s.append(f'<line x1="24" y1="{gy2}" x2="246" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s += foot(112, gy2 - 20, GREEN, fill="#EFE6D4")
    s.append(txt(150, gy2 - 26, "同一只脚，同一个地方", 4.8, GREEN))
    s.append(txt(150, gy2 - 14, "一笔不动，百姓才敢照着过日子", 4.4, "#6E6459"))
    # 年轴：四个年份都落在这一处（先有年头，脚才落得下）
    ty = gy2 - 62
    s.append(f'<line x1="52" y1="{ty}" x2="212" y2="{ty}" stroke="{LINE}" stroke-width="0.9"/>')
    for k, lab in enumerate(["去", "今", "明", "后"]):
        x = 64 + k * 44
        s.append(f'<line x1="{x}" y1="{ty-4}" x2="{x}" y2="{ty+4}" stroke="{INK}" stroke-width="0.9"/>')
        s.append(txt(x, ty - 9, lab, 4.2, "#6E6459", "middle"))
    s.append(f'<line x1="112" y1="{ty+8}" x2="112" y2="{gy2-44}" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    s.append(txt(220, ty + 2, "年年都落这一处", 4.6, GREEN))
    s.append(txt(112, gy2 + 16, "四个年头，都落在这一处", 4.6, "#6E6459", "middle"))

    b = gy2 + 44
    s.append(txt(24, b, "「正」从止，止是脚趾：一只脚停在它该在的地方。", 5.2, INK))
    s.append(txt(24, b + 16, "所以正不是「对」，是不动；一个政策最大的德，是明年还是它。", 5.2, INK))
    s.append(txt(24, b + 32, "朝令夕改的地方，不是百姓不听话，是脚没有地方可落。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "正，是脚站定；奇，是落单的一手；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "无事，是不给自己加职分。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch57a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十七章 · 一双手套 ============
def ch57b_yi_shuang_shou_tao():
    W, H = 380, 634
    body, y = head(W, H, "以奇用兵：奇，《说文》「不耦」——落单的一手",
                   "第 五 十 七 章 · 奇", "一双手套", "奇是落单的一手，会用，不能落单成习惯。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「奇」，《说文》「异也，一曰不耦」——不耦，就是落单：没有配对的。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "一双手套，平时是两只；出手的时候，只戴一只。", 5.2, "#6E6459", "middle"))

    def glove(cx, cy, col, dash=None, fill=None):
        o = []
        d = f' stroke-dasharray="{dash}"' if dash else ''
        fl = f' fill="{fill}"' if fill else ' fill="none"'
        o.append(f'<rect x="{cx-7}" y="{cy-12}" width="14" height="24" rx="5" stroke="{col}" stroke-width="1"{d}{fl}/>')
        for dx in (-3.5, 0, 3.5):
            o.append(f'<line x1="{cx+dx}" y1="{cy-11}" x2="{cx+dx}" y2="{cy-4}" stroke="{col}" stroke-width="0.5" stroke-dasharray="2 2"/>')
        o.append(f'<ellipse cx="{cx-9.5}" cy="{cy+3}" rx="3" ry="4.6" stroke="{col}" stroke-width="1"{d}{fl}/>')
        return o

    def boxwith(x, y0, labels, solid_slots):
        o = [box(x, y0, 64, 34, fill="#EFE6D4", stroke=INK, width=0.8)]
        for k, (gx, is_solid) in enumerate(solid_slots):
            o += glove(gx, y0 - 4 if False else y0 + 20, LINE if is_solid else LINE, dash=None if is_solid else "4 3")
        return o

    # 一、出手：取一只
    t1 = y + 46
    s.append(txt(24, t1, "一、出手：取一只，用一下", 5.4, SEAL))
    cy1 = t1 + 84
    s.append(box(40, cy1 + 6, 62, 36, fill="#EFE6D4", stroke=INK, width=0.8))
    s += glove(58, cy1 + 24, LINE, fill="#FBF6EC")
    s += glove(86, cy1 + 24, LINE, dash="4 3")
    s.append(txt(71, cy1 + 50, "盒里还剩一只", 4.2, "#8A8078", "middle"))
    s += glove(150, cy1 - 8, SEAL, fill="#FBF6EC")
    s.append(arrow(96, cy1 + 4, 138, cy1 - 12, SEAL, 0.7, head="arrS"))
    s.append(txt(170, cy1 - 20, "取出去：只戴一只", 4.8, SEAL))
    s.append(txt(170, cy1 - 8, "打完了，手要还回来", 4.4, "#6E6459"))
    s.append(txt(190, cy1 + 50, "兵是迫不得已的那一手", 4.6, "#6E6459", "middle"))

    # 二、成常：两只都取走
    t2 = cy1 + 76
    s.append(txt(24, t2, "二、成常：两只都取走，盒子就空了", 5.4, GREEN))
    cy2 = t2 + 78
    s.append(box(40, cy2 + 6, 62, 36, fill="#F2EADA", stroke=INK, width=0.8))
    s += glove(58, cy2 + 24, LINE, dash="4 3")
    s += glove(86, cy2 + 24, LINE, dash="4 3")
    s.append(txt(71, cy2 + 50, "盒里一只也没有", 4.2, "#8A8078", "middle"))
    s += glove(146, cy2 - 10, SEAL, fill="#FBF6EC")
    s += glove(172, cy2 - 10, SEAL, fill="#FBF6EC")
    s.append(txt(159, cy2 + 20, "两只都戴出去", 4.6, SEAL, "middle"))
    s.append(txt(159, cy2 + 32, "＝把奇当常", 4.6, SEAL, "middle"))
    s.append(txt(159, cy2 + 44, "＝以兵治国", 4.6, GREEN, "middle"))
    s.append(txt(190, cy2 + 66, "会用，但不能落单成习惯——习惯就成常了", 4.6, "#6E6459", "middle"))

    b = cy2 + 80
    s.append(txt(24, b, "「奇」是不耦，是落单：没有配对的。", 5.2, INK))
    s.append(txt(24, b + 16, "兵戈起于对立，是二元激化之后的应急，属于不得已的那一手。", 5.0, INK))
    s.append(txt(24, b + 32, "知雄守雌：知道那一手怎么用，绝不把它当日子过。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "奇是落单的一手；会用，但不能落单成习惯。", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "无事是宗旨，正是常轨，奇只是兜底。", 5.4, GREEN, "middle"))
    s.append(gold(c + 62, "ch57b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十七章 · 一块被画花的木牌 ============
def ch57c_yi_kuai_hua_pai():
    W, H = 380, 628
    body, y = head(W, H, "法令滋彰：彰从彡，是三撇毛，是画上去的花纹",
                   "第 五 十 七 章 · 彰", "一块木牌", "法令滋彰，盗贼多有。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「彰」从彡——彡是三撇毛，是画上去的花纹；不是「法令很多」，是「条文越画越花」。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "花是画在木牌上的；木牌本来只有一条线，是给人踩的。", 5.2, "#6E6459", "middle"))

    def board(cx, gy):
        o = [box(cx - 40, gy - 74, 80, 58, fill="#EFE6D4", stroke=INK, width=1)]
        o.append(f'<line x1="{cx-22}" y1="{gy-16}" x2="{cx-22}" y2="{gy}" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<line x1="{cx+22}" y1="{gy-16}" x2="{cx+22}" y2="{gy}" stroke="{INK}" stroke-width="2"/>')
        return o

    def sanpie(cx, cy, col, n=3, ln=11, gap=4.6):
        o = []
        for k in range(n):
            x = cx + k * gap
            o.append(f'<line x1="{x:.1f}" y1="{cy}" x2="{x+4.5:.1f}" y2="{cy-ln}" stroke="{col}" stroke-width="1"/>')
        return o

    def foot(cx, cy, col, fl=None, k=1.3):
        o = []
        fill = f' fill="{fl}"' if fl else ' fill="none"'
        def X(v): return cx + v * k
        def Y(v): return cy + v * k
        o.append(f'<path d="M{X(-6.5)},{Y(-9)} C{X(-8)},{Y(-1)} {X(-7.5)},{Y(7)} {X(-3)},{Y(11)} C{X(2)},{Y(14)} {X(6)},{Y(8)} {X(7)},{Y(-1)} C{X(8)},{Y(-9)} {X(5)},{Y(-14)} {X(-1)},{Y(-14)} C{X(-4.5)},{Y(-14)} {X(-5.5)},{Y(-13)} {X(-6.5)},{Y(-9)} Z" stroke="{col}" stroke-width="0.9"{fill}/>')
        o.append(f'<circle cx="{X(-5)}" cy="{Y(-16.5)}" r="{1.9*k}" stroke="{col}" stroke-width="0.7"{fill}/>')
        o.append(f'<circle cx="{X(-1.2)}" cy="{Y(-18.5)}" r="{1.6*k}" stroke="{col}" stroke-width="0.7"{fill}/>')
        o.append(f'<circle cx="{X(2)}" cy="{Y(-17)}" r="{1.4*k}" stroke="{col}" stroke-width="0.7"{fill}/>')
        o.append(f'<circle cx="{X(4.6)}" cy="{Y(-14.6)}" r="{1.2*k}" stroke="{col}" stroke-width="0.7"{fill}/>')
        return o

    # 一、素牌
    t1 = y + 46
    s.append(txt(24, t1, "一、素牌：一条刻线，脚踩得着", 5.4, GREEN))
    gy1 = t1 + 106
    s.append(f'<line x1="24" y1="{gy1}" x2="250" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s += board(78, gy1)
    s.append(f'<line x1="78" y1="{gy1-68}" x2="78" y2="{gy1-22}" stroke="{INK}" stroke-width="1.6"/>')
    s += foot(178, gy1 - 15, GREEN, "#EFE6D4")
    s.append(txt(196, gy1 - 44, "一条线：", 4.8, GREEN))
    s.append(txt(196, gy1 - 32, "踩得着，看得懂", 4.4, "#6E6459"))
    s.append(txt(100, gy1 + 14, "禁什么、许什么，一站就知道", 4.4, "#6E6459", "middle"))

    # 二、花牌
    t2 = gy1 + 40
    s.append(txt(24, t2, "二、花牌：条文越画越花，人只剩绕", 5.4, SEAL))
    gy2 = t2 + 106
    s += board(78, gy2)
    for r in range(4):
        for cc in range(4):
            s += sanpie(50 + cc * 19, gy2 - 24 - r * 12, SEAL)
    s.append(f'<line x1="78" y1="{gy2-68}" x2="78" y2="{gy2-22}" stroke="{LINE}" stroke-width="0.4" stroke-dasharray="2 3"/>')
    s.append(f'<line x1="24" y1="{gy2}" x2="250" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    for k in range(11):
        x0 = 28 + k * 21
        s.append(f'<line x1="{x0}" y1="{gy2}" x2="{x0+11}" y2="{gy2-16}" stroke="{SEAL}" stroke-width="0.5"/>')
    s += foot(178, gy2 - 34, INK, "#F8F3E6")
    s.append(f'<line x1="178" y1="{gy2-18}" x2="178" y2="{gy2-6}" stroke="{SEAL}" stroke-width="0.5" stroke-dasharray="2 2"/>')
    s.append(txt(200, gy2 - 52, "线多了：", 4.8, SEAL))
    s.append(txt(200, gy2 - 40, "一条都不敢踩", 4.4, "#6E6459"))
    s.append(txt(100, gy2 + 14, "绕着走：绕到最后，就是铤而走险", 4.4, SEAL, "middle"))

    b = gy2 + 40
    s.append(txt(24, b, "「彰」从彡：三撇毛，是画上去的花。", 5.2, INK))
    s.append(txt(24, b + 16, "木牌上本来只有一条线，那条线是给人踩的；画满了花，就没有一条清楚的线可踩。", 4.8, INK))
    s.append(txt(24, b + 32, "人不是不怕法，是踩不到那条线；踩不到，就只剩下绕——绕到最后，就是铤而走险。", 4.6, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "彰是画上去的花；", 6.0, INK, "middle"))
    s.append(txt(190, c + 36, "条文画得越花，能踩的线就越多。", 5.4, GREEN, "middle"))
    s.append(gold(c + 62, "ch57c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十八章 · 一扇门 ============
def ch58a_yi_shan_men():
    W, H = 380, 664
    body, y = head(W, H, "其政闷闷：闷从心从门，是心关在门里，不往外放",
                   "第 五 十 八 章 · 闷", "一扇门", "其政闷闷，其民淳淳。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「闷」，《说文》「懑也」，从心、从门——心关在门里。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "「察」，《说文》「覆也」，从宀、从祭——屋顶底下，把东西盖过来再审。", 5.2, "#6E6459", "middle"))

    def jar(cx, gy, level=None, col=INK, fill="#EFE6D4"):
        o = [f'<ellipse cx="{cx}" cy="{gy-24}" rx="15" ry="17" fill="{fill}" stroke="{col}" stroke-width="1"/>']
        o.append(f'<rect x="{cx-7}" y="{gy-46}" width="14" height="9" rx="2" fill="{fill}" stroke="{col}" stroke-width="1"/>')
        o.append(f'<line x1="{cx-15}" y1="{gy-42}" x2="{cx+15}" y2="{gy-42}" stroke="{col}" stroke-width="0.8"/>')
        if level is not None:
            o.append(f'<line x1="{cx-14}" y1="{level}" x2="{cx+14}" y2="{level}" stroke="{SEAL}" stroke-width="1"/>')
        return o

    # 一、门关着
    t1 = y + 46
    s.append(txt(24, t1, "一、门关着：心在门里，酒没兑水", 5.4, GREEN))
    gy1 = t1 + 108
    s.append(f'<line x1="24" y1="{gy1}" x2="240" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s.append(box(56, gy1 - 92, 60, 92, fill="#EFE6D4", stroke=INK, width=1.2))
    s.append(f'<line x1="86" y1="{gy1-92}" x2="86" y2="{gy1}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="74" y1="{gy1-42}" x2="74" y2="{gy1-34}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<circle cx="74" cy="{gy1-38}" r="2" fill="{INK}"/>')
    for k in range(4):
        s.append(f'<line x1="88" y1="{gy1-86+k*20}" x2="110" y2="{gy1-86+k*20}" stroke="{LINE}" stroke-width="0.5"/>')
    s += jar(150, gy1, None)
    s.append(txt(150, gy1 + 14, "淳：酒没兑水", 4.6, GREEN, "middle"))
    s.append(txt(176, gy1 - 66, "心关在门里", 4.8, GREEN))
    s.append(txt(176, gy1 - 54, "懂了不往外放", 4.4, "#6E6459"))

    # 二、屋顶盖下来，一遍遍翻
    t2 = gy1 + 36
    s.append(txt(24, t2, "二、盖过来审：翻一遍，割一道", 5.4, SEAL))
    gy2 = t2 + 134
    s.append(f'<line x1="24" y1="{gy2}" x2="240" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M40,{gy2-88} L110,{gy2-118} L180,{gy2-88}" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<line x1="40" y1="{gy2-88}" x2="180" y2="{gy2-88}" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="34" y1="{gy2-86}" x2="34" y2="{gy2}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<line x1="186" y1="{gy2-86}" x2="186" y2="{gy2}" stroke="{LINE}" stroke-width="1"/>')
    s.append(box(62, gy2 - 40, 76, 40, fill="#F2EADA", stroke=INK, width=0.9))
    for k in range(3):
        x = 70 + k * 24
        s.append(f'<line x1="{x}" y1="{gy2-14}" x2="{x+16}" y2="{gy2-36}" stroke="{INK}" stroke-width="0.7"/>')
        s.append(f'<line x1="{x+4}" y1="{gy2-12}" x2="{x+20}" y2="{gy2-34}" stroke="{INK}" stroke-width="0.7"/>')
    s.append(arrow(112, gy2 - 56, 112, gy2 - 46, SEAL, 0.7, head="arrS"))
    s += jar(208, gy2, gy2 - 22)
    s.append(txt(208, gy2 + 14, "缺：被割出来的", 4.6, SEAL, "middle"))
    s.append(txt(198, gy2 - 88, "一遍一遍翻着看", 4.8, SEAL, "start"))

    b = gy2 + 40
    s.append(txt(24, b, "「闷」从心从门：心关在门里，懂了不往外放。", 5.2, INK))
    s.append(txt(24, b + 16, "「察」训「覆」：屋顶底下，把东西盖过来一遍遍翻着审；越审越割。", 4.8, INK))
    s.append(txt(24, b + 32, "淳通醇，是酒没兑水；上面不兑，下面才是原味。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "闷是把心关在门里，察是盖过来翻着看；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "一个是关，一个是翻。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch58a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十八章 · 一张折纸 ============
def ch58b_yi_zhang_zhe_zhi():
    W, H = 380, 568
    body, y = head(W, H, "祸兮福之所倚：倚是靠着，伏是藏着——它们不是排队，是背贴背",
                   "第 五 十 八 章 · 倚伏", "一张折纸", "祸兮，福之所倚；福兮，祸之所伏。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「倚」是靠、是贴；「伏」是藏、是底下那面——一张纸的两面，本来就是同一张。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "所以不是祸完了才轮到福，是福在身上就一直贴着祸。", 5.2, "#6E6459", "middle"))

    cx, cy = 178, y + 146
    s.append(f'<rect x="{cx-64}" y="{cy-54}" width="64" height="108" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{cx},{cy-54} L{cx+64},{cy-54} L{cx+64},{cy+26} L{cx+38},{cy+54} L{cx},{cy+54} Z" fill="#F2EADA" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{cx}" y1="{cy-54}" x2="{cx}" y2="{cy+54}" stroke="{LINE2}" stroke-width="0.8"/>')
    s.append(f'<text x="{cx-32}" y="{cy+10}" font-size="22" fill="{INK}" text-anchor="middle">福</text>')
    s.append(f'<text x="{cx+34}" y="{cy+14}" font-size="18" fill="{SEAL}" text-anchor="middle">祸</text>')
    s.append(txt(cx - 32, cy - 66, "上面这面", 4.6, INK, "middle"))
    s.append(txt(cx + 34, cy - 66, "底下那面", 4.6, SEAL, "middle"))
    s.append(arrow(cx + 78, cy + 46, cx + 60, cy + 30, SEAL, 0.8, head="arrS"))
    s.append(txt(cx + 82, cy + 52, "翻过来：", 4.6, SEAL))
    s.append(txt(cx + 82, cy + 63, "不用通知", 4.6, SEAL))
    s.append(txt(cx, cy + 78, "折线不是界限：同一张纸，只是折了一下", 4.6, "#6E6459", "middle"))

    b = cy + 106
    s.append(txt(24, b, "「祸兮福之所倚」：倚不是「等着」，是靠、是贴——祸来的时候，福已经在它背后靠着。", 4.8, INK))
    s.append(txt(24, b + 16, "「福兮祸之所伏」：伏不是「埋伏」，是藏在底下那一面，翻手就到。", 4.8, INK))
    s.append(txt(24, b + 32, "所以换的时候不用通知：不是排队，是同一张纸的两面。", 5.0, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "祸不是等在福后面，是靠在福身上；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "它们一直贴着，所以换的时候不用通知。", 5.4, GREEN, "middle"))
    s.append(gold(c + 62, "ch58b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十八章 · 两条船 ============
def ch58c_liang_tiao_chuan():
    W, H = 380, 736
    body, y = head(W, H, "方而不割：方，《说文》「併船也」——两条船并在一起",
                   "第 五 十 八 章 · 方", "两条船", "方而不割，廉而不刿，直而不肆，光而不耀。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「方」，《说文》「併船也」——两条船并在一起；所以方不是「棱角」，是「并着」。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "并着不动刀；一动刀，并就成了界。", 5.2, "#6E6459", "middle"))

    def boat(cx, cy_, col, flip=1):
        o = []
        RX, RY = 17, 52
        o.append(f'<path d="M{cx},{cy_-RY} C{cx+RX},{cy_-RY+18} {cx+RX},{cy_+RY-18} {cx},{cy_+RY} C{cx-RX},{cy_+RY-18} {cx-RX},{cy_-RY+18} {cx},{cy_-RY} Z" fill="#EFE6D4" stroke="{col}" stroke-width="1.1"/>')
        o.append(f'<line x1="{cx}" y1="{cy_-32}" x2="{cx}" y2="{cy_+32}" stroke="{col}" stroke-width="0.4" stroke-dasharray="3 3"/>')
        for dy in (-34, 0, 34):
            o.append(f'<path d="M{cx-24},{cy_+dy} C{cx-30},{cy_+dy+7} {cx-30},{cy_+dy+14} {cx-24},{cy_+dy+18}" fill="none" stroke="{LINE2}" stroke-width="0.45"/>')
        ox = cx + flip * (RX - 3)
        o.append(f'<line x1="{ox}" y1="{cy_-6}" x2="{cx + flip*(RX+16)}" y2="{cy_+18}" stroke="{col}" stroke-width="1"/>')
        o.append(f'<line x1="{cx-4}" y1="{cy_+20}" x2="{cx+4}" y2="{cy_+20}" stroke="{col}" stroke-width="0.5"/>')
        return o

    # 一、并着
    t1 = y + 46
    s.append(txt(24, t1, "一、两条船并着：中间不留刀口", 5.4, GREEN))
    wy = t1 + 96
    s += boat(124, wy, INK, -1)
    s += boat(158, wy, INK, 1)
    s.append(txt(143, wy - 74, "并着：船帮贴船帮，中间没有刀口", 4.8, GREEN, "middle"))
    s.append(txt(124, wy + 76, "方：两条船并在一起", 4.6, "#6E6459"))

    # 二、动了刀
    t2 = wy + 84
    s.append(txt(24, t2, "二、一动刀：并就成了界", 5.4, SEAL))
    wy2 = t2 + 84
    s += boat(124, wy2, INK, -1)
    s += boat(158, wy2, INK, 1)
    s.append(f'<line x1="141" y1="{wy2-64}" x2="141" y2="{wy2+64}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(txt(150, wy2 - 46, "割", 4.8, SEAL, "start"))
    s.append(txt(196, wy2 + 32, "界：船还是两条", 4.8, SEAL, "start"))
    s.append(txt(196, wy2 + 46, "路只剩一边", 4.6, "#6E6459", "start"))
    s.append(txt(124, wy2 + 76, "一动刀，并就成了界", 4.6, SEAL))

    # 三、四句 = 四个方向的留一点
    t3 = wy2 + 84
    s.append(f'<line x1="24" y1="{t3}" x2="338" y2="{t3}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(24, t3 + 18, "四句，是四个方向上的「留一点」：", 5.2, INK))
    quads = [("方而不割", "并着，不收刀"), ("廉而不刿", "边立着，不利手"),
             ("直而不肆", "话说着，不说尽"), ("光而不耀", "灯亮着，不刺眼")]
    for k, (a, bb) in enumerate(quads):
        col = 26 + (k % 2) * 166
        row = t3 + 38 + (k // 2) * 19
        s.append(txt(col, row, a, 4.8, SEAL))
        s.append(txt(col + 50, row, "——" + bb, 4.6, "#6E6459"))

    b = t3 + 88
    s.append(txt(24, b, "方是两条船并着：并着不动刀，一动刀就成了界。", 5.2, INK))
    s.append(txt(24, b + 16, "廉是堂屋那条侧边，不是刀口：边要立着，可不能划手。", 5.0, INK))
    s.append(txt(24, b + 32, "直是话说着不说尽，光是灯亮着不刺眼——这一章的功夫，都在「留一点」上。", 4.6, GREEN))

    c = b + 48
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "方是两条船并着；并着不动刀，一动刀就成了界。", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "光在，耀不在；一刺眼，照就变成了压。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch58c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十九章 · 一口囤 ============
def ch59a_yi_kou_dun():
    W, H = 380, 640
    body, y = head(W, H, "治人事天，莫若啬：啬从來从回，是收庄稼入仓",
                   "第 五 十 九 章 · 啬", "一口囤", "治人事天，莫若啬。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「啬」，《说文》「爱濇也」，从「來」（麦子）、从「回」（围着囤转一圈收进去）。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "所以啬的本义不是「省」，是「收庄稼入仓」。", 5.2, "#6E6459", "middle"))

    def wheat(cx, gy, hgt=54):
        o = [f'<line x1="{cx}" y1="{gy}" x2="{cx}" y2="{gy-hgt}" stroke="{GREEN}" stroke-width="1.1"/>']
        o.append(f'<ellipse cx="{cx}" cy="{gy-hgt-6}" rx="3" ry="6" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
        for d in (-4, 0, 4):
            o.append(f'<line x1="{cx}" y1="{gy-hgt-10}" x2="{cx+d}" y2="{gy-hgt-18}" stroke="{SEAL}" stroke-width="0.6"/>')
        o.append(f'<line x1="{cx}" y1="{gy-hgt+10}" x2="{cx-7}" y2="{gy-hgt+2}" stroke="{GREEN}" stroke-width="0.6"/>')
        return o

    def dun(cx, gy, h=64, filled=False):
        w = 46
        o = [f'<rect x="{cx-w/2}" y="{gy-h}" width="{w}" height="{h}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>']
        o.append(f'<path d="M{cx-w/2},{gy-h} C{cx-w/2+8},{gy-h-12} {cx+w/2-8},{gy-h-12} {cx+w/2},{gy-h}" fill="none" stroke="{INK}" stroke-width="1"/>')
        for k in range(4):
            yy = gy - 18 - k * 15
            o.append(f'<line x1="{cx-w/2}" y1="{yy}" x2="{cx+w/2}" y2="{yy}" stroke="{LINE}" stroke-width="0.4"/>')
        if filled:
            o.append(f'<path d="M{cx-w/2+4},{gy-h+9} C{cx-8},{gy-h+3} {cx+8},{gy-h+3} {cx+w/2-4},{gy-h+9}" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
            for k in range(4):
                o.append(f'<circle cx="{cx-w/4+k*w/8}" cy="{gy-h+11}" r="1.6" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
        return o

    # 一、收
    t1 = y + 46
    s.append(txt(24, t1, "一、收：围着麦地转一圈，拢回仓里", 5.4, GREEN))
    gy1 = t1 + 122
    s.append(f'<line x1="24" y1="{gy1}" x2="240" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    for cx in (52, 74, 96):
        s += wheat(cx, gy1)
    s += dun(178, gy1, filled=True)
    s.append(f'<path d="M104,{gy1-56} C132,{gy1-86} 168,{gy1-86} 176,{gy1-58}" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(f'<path d="M172,{gy1-62} L176,{gy1-56} L181,{gy1-63}" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(110, gy1 - 92, "收进去", 4.6, GREEN))
    s.append(txt(178, gy1 + 14, "仓：满了才叫啬", 4.6, GREEN, "middle"))

    # 二、不是撒
    t2 = gy1 + 40
    s.append(txt(24, t2, "二、不是舍不得给：是往回拢，不是往外撒", 5.0, SEAL))
    gy2 = t2 + 118
    s.append(f'<line x1="24" y1="{gy2}" x2="240" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M96,{gy2-40} L136,{gy2-40} L128,{gy2} L104,{gy2} Z" fill="#EFE6D4" stroke="{SEAL}" stroke-width="1" stroke-dasharray="4 3"/>')
    for k in range(3):
        s.append(f'<circle cx="{106+k*10}" cy="{gy2-52-k*8}" r="2" fill="none" stroke="{SEAL}" stroke-width="0.7" stroke-dasharray="2 2"/>')
    s.append(txt(124, gy2 - 62, "往外撒：那是给，不是啬", 4.6, SEAL))
    s.append(txt(124, gy2 - 50, "撒完了，仓是空的", 4.4, "#6E6459"))
    s += dun(222, gy2, filled=True)
    s.append(txt(222, gy2 + 14, "拢回来：仓是实的", 4.4, GREEN, "middle"))

    b = gy2 + 40
    s.append(txt(24, b, "「啬」从來、从回：來是麦子，回是围着囤转一圈，把麦子赶进仓。", 4.8, INK))
    s.append(txt(24, b + 16, "所以啬不是舍不得给，是先把该收的收回来；一个动作，两种人做出来是两回事。", 4.8, INK))
    s.append(txt(24, b + 32, "这一章不是讲节俭，是讲收成。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "啬不是舍不得给，是把收下来的拢回仓里；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "这一章不是讲节俭，是讲收成。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch59a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十九章 · 一根扁担 ============
def ch59b_yi_gen_bian_dan():
    W, H = 380, 648
    body, y = head(W, H, "重积德则无不克：克训「肩」，是担得起，不是打遍天下",
                   "第 五 十 九 章 · 克", "一根扁担", "重积德则无不克。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「积」从禾，是一袋一袋码起来；「克」训「肩」，是扛得起。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以「无不克」不是打遍天下，是天下事都担得起。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "一根扁担两头沉：担得起，才走得远", 5.4, GREEN))
    gy1 = t1 + 132
    s.append(f'<line x1="24" y1="{gy1}" x2="250" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    # 人
    s.append(f'<circle cx="114" cy="{gy1-72}" r="6" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<line x1="114" y1="{gy1-66}" x2="114" y2="{gy1-30}" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="100" y1="{gy1-58}" x2="128" y2="{gy1-58}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="114" y1="{gy1-30}" x2="102" y2="{gy1}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="114" y1="{gy1-30}" x2="126" y2="{gy1}" stroke="{INK}" stroke-width="1.2"/>')
    # 扁担 + 两筐
    s.append(f'<line x1="56" y1="{gy1-58}" x2="172" y2="{gy1-58}" stroke="{INK}" stroke-width="2"/>')
    for bx in (56, 172):
        s.append(f'<line x1="{bx}" y1="{gy1-58}" x2="{bx}" y2="{gy1-52}" stroke="{INK}" stroke-width="0.5"/>')
        s.append(f'<path d="M{bx-16},{gy1-52} L{bx+16},{gy1-52} L{bx+11},{gy1-2} L{bx-11},{gy1-2} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
        for k in range(3):
            s.append(f'<line x1="{bx-10}" y1="{gy1-44+k*10}" x2="{bx+10}" y2="{gy1-44+k*10}" stroke="{LINE}" stroke-width="0.4"/>')
    s.append(txt(56, gy1 + 14, "一头：担子", 4.4, "#6E6459", "middle"))
    s.append(txt(172, gy1 + 14, "另一头：也担着", 4.4, "#6E6459", "middle"))
    s.append(txt(196, gy1 - 78, "克是肩：", 4.8, GREEN))
    s.append(txt(196, gy1 - 66, "担得起，不是打得过", 4.4, "#6E6459"))

    t2 = gy1 + 40
    s.append(txt(24, t2, "积是码货：一袋一袋往上堆，才堆得高", 5.4, SEAL))
    gy2 = t2 + 116
    s.append(f'<line x1="24" y1="{gy2}" x2="250" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    for k in range(5):
        w = 30 + k * 4
        s.append(f'<rect x="{116-w/2}" y="{gy2-(k+1)*18}" width="{w}" height="16" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
        s.append(f'<line x1="{116-w/2+6}" y1="{gy2-(k+1)*18+11}" x2="{116+w/2-6}" y2="{gy2-(k+1)*18+11}" stroke="{LINE}" stroke-width="0.4"/>')
    s.append(txt(150, gy2 - 40, "积：从禾，是码货", 4.8, SEAL))
    s.append(txt(150, gy2 - 28, "德是堆出来的，堆的前提是先收", 4.4, "#6E6459"))
    s.append(txt(116, gy2 + 14, "底下一袋是「啬」收回来的", 4.6, "#6E6459", "middle"))

    b = gy2 + 40
    s.append(txt(24, b, "积德是码货，不是做好事：德是堆出来的，堆的前提是先收。", 5.0, INK))
    s.append(txt(24, b + 16, "克是肩，不是刀：「无不克」不是打遍天下，是天下事都担得起。", 5.0, INK))
    s.append(txt(24, b + 32, "担子两头都沉，人才走得稳；只挑轻的那头，走两步就歪。", 4.8, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "克是肩，不是刀；「无不克」不是打遍天下，", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "是天下事都担得起。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch59b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第五十九章 · 一棵树 ============
def ch59c_yi_ke_shu():
    W, H = 380, 718
    body, y = head(W, H, "深根固柢：根是横着铺的，柢是竖着扎的",
                   "第 五 十 九 章 · 根柢", "一棵树", "是谓深根固柢，长生久视之道。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「根」是横着铺开的那一层须；「柢」，《说文》「木根也」，是那根往下扎死的主根。", 4.8, INK, "middle"))
    s.append(txt(190, y + 26, "铺满一层挡不住风；扎死一根，才挡得住。", 5.2, "#6E6459", "middle"))

    def trunk(cx, gy, tilt=0):
        o = [f'<line x1="{cx}" y1="{gy}" x2="{cx+tilt}" y2="{gy-70}" stroke="{INK}" stroke-width="2.6"/>']
        o.append(f'<line x1="{cx+tilt*0.6}" y1="{gy-44}" x2="{cx+tilt*0.6-22}" y2="{gy-66}" stroke="{INK}" stroke-width="1.2"/>')
        o.append(f'<line x1="{cx+tilt*0.8}" y1="{gy-56}" x2="{cx+tilt*0.8+20}" y2="{gy-76}" stroke="{INK}" stroke-width="1.2"/>')
        o.append(f'<circle cx="{cx+tilt*0.5-24}" cy="{gy-70}" r="12" fill="none" stroke="{GREEN}" stroke-width="0.5"/>')
        o.append(f'<circle cx="{cx+tilt*0.8+22}" cy="{gy-80}" r="13" fill="none" stroke="{GREEN}" stroke-width="0.5"/>')
        return o

    # 一、只有根
    t1 = y + 46
    s.append(txt(24, t1, "一、只有根：横着铺一层，风一来就歪", 5.4, SEAL))
    gy1 = t1 + 120
    s.append(f'<line x1="24" y1="{gy1}" x2="240" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s += trunk(150, gy1, tilt=8)
    for d in (-56, -42, -28, 28, 42, 56):
        s.append(f'<path d="M150,{gy1+2} C{150+d*0.4},{gy1+14} {150+d*0.8},{gy1+16} {150+d},{gy1+22}" fill="none" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(f'<line x1="150" y1="{gy1}" x2="158" y2="{gy1-70}" stroke="{LINE}" stroke-width="0.4" stroke-dasharray="3 3"/>')
    s.append(arrow(196, gy1 - 46, 176, gy1 - 44, SEAL, 0.8, head="arrS"))
    s.append(txt(198, gy1 - 52, "风", 4.8, SEAL))
    s.append(txt(150, gy1 + 34, "根浅、铺得广：一层皮毛，挡不住风", 4.6, SEAL, "middle"))

    # 二、柢扎下去
    t2 = gy1 + 70
    s.append(txt(24, t2, "二、有柢：一根扎死，风还在，树不动", 5.4, GREEN))
    gy2 = t2 + 132
    s.append(f'<line x1="24" y1="{gy2}" x2="240" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s += trunk(150, gy2, tilt=0)
    for d in (-40, -22, 22, 40):
        s.append(f'<path d="M150,{gy2+2} C{150+d*0.4},{gy2+10} {150+d*0.8},{gy2+12} {150+d},{gy2+16}" fill="none" stroke="{SEAL}" stroke-width="0.6"/>')
    s.append(f'<line x1="150" y1="{gy2}" x2="150" y2="{gy2+50}" stroke="{SEAL}" stroke-width="2.4"/>')
    s.append(f'<line x1="150" y1="{gy2+26}" x2="138" y2="{gy2+40}" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(f'<line x1="150" y1="{gy2+34}" x2="162" y2="{gy2+48}" stroke="{SEAL}" stroke-width="0.8"/>')
    s.append(arrow(196, gy2 - 46, 176, gy2 - 44, SEAL, 0.8, head="arrS"))
    s.append(txt(198, gy2 - 52, "风还在", 4.8, SEAL))
    s.append(txt(196, gy2 + 10, "柢：竖着扎死一根", 4.8, GREEN))
    s.append(txt(150, gy2 + 68, "长生久视：久不是远，是扎得住", 4.6, GREEN, "middle"))

    b = gy2 + 84
    s.append(txt(24, b, "往外长的都有屋脊：树有顶，屋有顶，到顶就开始老。", 4.9, INK))
    s.append(txt(24, b + 16, "往里蓄的没有顶：仓越满越稳，柢越扎越深，都不长「顶」。", 4.9, INK))
    s.append(txt(24, b + 32, "「久视」是看得久，不是看得远；「长生」在这本书里，从不指肉身不坏。", 4.7, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "根是横着铺的，柢是竖着扎的；铺满一层挡不住风，", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "扎死一根才挡得住。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch59c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十章 · 一口锅 ============
def ch60a_yi_kou_guo():
    W, H = 380, 700
    body, y = head(W, H, "治大国若烹小鲜：鲜是新杀之鱼，最嫩，也最经不起翻",
                   "第 六 十 章 · 烹", "一口锅", "治大国，若烹小鲜。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「鲜」，《说文》「鱼名」；先秦用「鲜」多取「新」义——新杀之鱼。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以「小鲜」不是小鱼干，是刚下锅的那条；它最嫩，最经不起翻。", 5.0, "#6E6459", "middle"))

    def pot(cx, gy, w=96):
        o = []
        o.append(f'<path d="M{cx-w/2},{gy-40} L{cx+w/2},{gy-40} L{cx+w/2-10},{gy} L{cx-w/2+10},{gy} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
        o.append(f'<path d="M{cx-w/2},{gy-40} C{cx-12},{gy-46} {cx+12},{gy-46} {cx+w/2},{gy-40}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        o.append(f'<path d="M{cx-w/2-14},{gy-32} C{cx-w/2-20},{gy-24} {cx-w/2-8},{gy-18} {cx-w/2},{gy-20}" fill="none" stroke="{INK}" stroke-width="1"/>')
        o.append(f'<path d="M{cx+w/2+14},{gy-32} C{cx+w/2+20},{gy-24} {cx+w/2+8},{gy-18} {cx+w/2},{gy-20}" fill="none" stroke="{INK}" stroke-width="1"/>')
        for dx in (-22, 0, 22):
            o.append(f'<path d="M{cx+dx},{gy+2} C{cx+dx-7},{gy+10} {cx+dx-2},{gy+18} {cx+dx},{gy+22} C{cx+dx+4},{gy+14} {cx+dx+6},{gy+8} {cx+dx},{gy+2} Z" fill="none" stroke="{SEAL}" stroke-width="0.9"/>')
        return o

    def fish(cx, cy, col, split=0):
        o = []
        o.append(f'<path d="M{cx-16},{cy} C{cx-8},{cy-7} {cx+10},{cy-7} {cx+18},{cy} C{cx+10},{cy+7} {cx-8},{cy+7} {cx-16},{cy} Z" fill="#FBF6EC" stroke="{col}" stroke-width="1"/>')
        o.append(f'<path d="M{cx-16},{cy} L{cx-24},{cy-6} L{cx-24},{cy+6} Z" fill="none" stroke="{col}" stroke-width="0.9"/>')
        o.append(f'<circle cx="{cx+10}" cy="{cy-1}" r="1.2" fill="{col}"/>')
        if split:
            o.append(f'<line x1="{cx-2}" y1="{cy-8}" x2="{cx-2}" y2="{cy+8}" stroke="{col}" stroke-width="0.5" stroke-dasharray="2 2"/>')
        return o

    # 一、翻
    t1 = y + 46
    s.append(txt(24, t1, "一、翻：铲子一搅，鱼断成两截", 5.4, SEAL))
    gy1 = t1 + 128
    s += pot(112, gy1)
    s += fish(108, gy1 - 32, SEAL, split=1)
    s.append(f'<line x1="150" y1="{gy1-64}" x2="126" y2="{gy1-30}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<rect x="140" y="{gy1-70}" width="16" height="9" fill="#EFE6D4" stroke="{INK}" stroke-width="0.8"/>')
    s.append(txt(178, gy1 - 72, "铲子在锅里搅", 4.8, SEAL))
    s.append(txt(178, gy1 - 60, "翻一遍，断一处", 4.4, "#6E6459"))
    s.append(txt(112, gy1 + 40, "锅是敞的：谁都想伸一铲子", 4.6, "#6E6459", "middle"))

    # 二、不翻
    t2 = gy1 + 62
    s.append(txt(24, t2, "二、不翻：盖子盖着，火自己稳", 5.4, GREEN))
    gy2 = t2 + 118
    s += pot(112, gy2)
    s.append(f'<path d="M{112-52},{gy2-44} C{112-20},{gy2-62} {112+20},{gy2-62} {112+52},{gy2-44}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<circle cx="112" cy="{gy2-60}" r="4" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(txt(196, gy2 - 64, "盖着：看不见，也别揭", 4.8, GREEN))
    s.append(txt(196, gy2 - 52, "鱼在里头熟，不用管", 4.4, "#6E6459"))
    s.append(txt(112, gy2 + 40, "火候够了，自己就熟", 4.6, "#6E6459", "middle"))

    b = gy2 + 62
    s.append(txt(24, b, "烹小鲜的诀是不翻：新鱼最嫩，翻一遍就断一处。", 5.0, INK))
    s.append(txt(24, b + 16, "大国万民的生机也一样：政令反复，就是锅里的铲子。", 5.0, INK))
    s.append(txt(24, b + 32, "上一章攒得住，这一章才敢不动；仓里有粮的人，才熬得住不揭锅盖。", 4.8, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "治大国，若烹小鲜：", 6.2, INK, "middle"))
    s.append(txt(190, c + 36, "诀只有一个字——不翻。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch60a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十章 · 一片草 ============
def ch60b_yi_pian_cao():
    W, H = 380, 672
    body, y = head(W, H, "以道莅天下：莅从艸从位，是草长到那个位置",
                   "第 六 十 章 · 莅", "一片草", "以道莅天下，其鬼不神。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「莅」，《说文》「临也」，从艸、从位——是草长到那个位置上去了。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以莅是「到」，不是「坐上去发令」；一个到，一个管。", 5.2, "#6E6459", "middle"))

    def blade(cx, gy, hgt, col=GREEN, lean=0):
        o = [f'<path d="M{cx},{gy} C{cx+lean*0.3},{gy-hgt*0.5} {cx+lean},{gy-hgt*0.8} {cx+lean*1.2},{gy-hgt}" fill="none" stroke="{col}" stroke-width="1.1"/>']
        return o

    # 一、压着长
    t1 = y + 46
    s.append(txt(24, t1, "一、压着长：草被压到那个位置", 5.4, SEAL))
    gy1 = t1 + 124
    s.append(f'<line x1="24" y1="{gy1}" x2="250" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="30" y1="{gy1-88}" x2="240" y2="{gy1-88}" stroke="{LINE}" stroke-width="0.6" stroke-dasharray="5 3"/>')
    for k, cx in enumerate((58, 74, 90, 106, 122)):
        s += blade(cx, gy1, 74 + k % 2 * 6, SEAL, lean=-30)
    s.append(box(150, gy1 - 118, 44, 26, fill="#EFE6D4", stroke=INK, width=0.9))
    s.append(txt(172, gy1 - 100, "令", 4.8, INK, "middle"))
    s.append(arrow(172, gy1 - 90, 172, gy1 - 74, SEAL, 0.9, head="arrS"))
    s.append(txt(196, gy1 - 60, "压到这么高", 4.6, SEAL))
    s.append(txt(58, gy1 + 14, "草被压弯：长不到它自己的高度", 4.6, "#6E6459"))

    # 二、自然长
    t2 = gy1 + 36
    s.append(txt(24, t2, "二、自己长：长到那位置，就不动了", 5.4, GREEN))
    gy2 = t2 + 124
    s.append(f'<line x1="24" y1="{gy2}" x2="250" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="30" y1="{gy2-94}" x2="240" y2="{gy2-94}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="5 3"/>')
    for k, cx in enumerate((58, 74, 90, 106, 122)):
        s += blade(cx, gy2, 86 - k % 2 * 5, GREEN, lean=2)
    for k, cx in enumerate((58, 74, 90, 106, 122)):
        s.append(f'<ellipse cx="{cx+1}" cy="{gy2-86-k%2*5}" rx="2" ry="3.4" fill="none" stroke="{GREEN}" stroke-width="0.7"/>')
    s.append(txt(160, gy2 - 102, "就长到这儿，不再往上", 4.6, GREEN))
    s.append(txt(58, gy2 + 14, "莅：草到了它该到的位置", 4.6, "#6E6459"))

    b = gy2 + 40
    s.append(txt(24, b, "「莅」从艸从位：是草长到那个位置上，不是人坐上去发令。", 4.9, INK))
    s.append(txt(24, b + 16, "压着长的草，长不到自己的高度；长到位的草，不再往上争。", 5.0, INK))
    s.append(txt(24, b + 32, "一个「到」，一个「管」：到了，就不用管了。", 5.2, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "莅是草长到那个位置，不是人坐上去发令；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "一个到，一个管。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch60b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十章 · 两条腿 ============
def ch60c_liang_tiao_tui():
    W, H = 380, 650
    body, y = head(W, H, "夫两不相伤，故德交归焉：交从交胫，是两条腿交叉",
                   "第 六 十 章 · 交", "两条腿", "夫两不相伤，故德交归焉。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「交」，《说文》「交胫也」——两条腿交叉；「归」，「女嫁也」，各回各家。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "所以「德交归」不是把德交上去，是两边各让一条腿，各自回家。", 5.0, "#6E6459", "middle"))

    def leg(x0, y0, x1, y1, col=INK, dashed=False):
        d = ' stroke-dasharray="4 3"' if dashed else ''
        return f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{col}" stroke-width="3"{d}/>'


    def footplan(cx, cy, col, dirn=1):
        return (f'<path d="M{cx},{cy-9} C{cx-dirn*6},{cy-4} {cx-dirn*6},{cy+5} {cx-dirn*2},{cy+9} C{cx+dirn*3},{cy+12} {cx+dirn*6},{cy+6} {cx+dirn*5},{cy-1} C{cx+dirn*5},{cy-8} {cx+dirn*2},{cy-12} {cx},{cy-9} Z" fill="#EFE6D4" stroke="{col}" stroke-width="0.9"/>')

    # 交叉处
    cx, cy = 150, y + 168
    s.append(leg(78, cy - 70, 200, cy + 28))
    s.append(leg(222, cy - 70, 100, cy + 28))
    s.append(footplan(206, cy + 34, INK, 1))
    s.append(footplan(94, cy + 34, INK, -1))
    s.append(txt(150, cy - 88, "两条腿交叉，各让一条", 5.0, SEAL, "middle"))
    s.append(arrow(96, cy + 56, 52, cy + 56, GREEN, 0.9, head="arrL"))
    s.append(arrow(204, cy + 56, 248, cy + 56, GREEN, 0.9, head="arr2"))
    s.append(txt(96, cy + 72, "各回各家", 4.8, GREEN))
    s.append(txt(212, cy + 72, "各回各家", 4.8, GREEN, "start"))

    # 反例：拧成一股
    t2 = cy + 84
    s.append(f'<line x1="24" y1="{t2}" x2="338" y2="{t2}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(txt(24, t2 + 18, "不是拧成一股：拧起来，谁都走不了", 5.4, SEAL))
    cy2 = t2 + 72
    s.append(f'<line x1="56" y1="{cy2-34}" x2="244" y2="{cy2-34}" stroke="{SEAL}" stroke-width="3"/>')
    s.append(f'<line x1="56" y1="{cy2-24}" x2="244" y2="{cy2-24}" stroke="{SEAL}" stroke-width="3"/>')
    for k in range(6):
        x = 62 + k * 30
        s.append(f'<line x1="{x}" y1="{cy2-38}" x2="{x+14}" y2="{cy2-20}" stroke="{SEAL}" stroke-width="0.7"/>')
    s.append(txt(190, cy2 - 48, "两股拧成一根绳：拆不开了", 4.6, SEAL, "middle"))

    b = cy2 + 24
    s.append(txt(24, b, "「交」是交胫：两条腿交叉，各让一条；「归」是女嫁，各回各家。", 4.9, INK))
    s.append(txt(24, b + 16, "拧成一股，成了绳，谁都走不了；交叉一下，两边都回得去。", 4.9, INK))
    s.append(txt(24, b + 32, "太平是没有声音，交归是各有各的地方；前者靠压，后者靠让。", 4.7, GREEN))

    c = b + 50
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "交是两条腿交叉，不是两股绳拧成一股；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "各让一条腿，才各回各家。", 5.6, GREEN, "middle"))
    s.append(gold(c + 62, "ch60c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十一章 · 一条河 ============
def ch61a_yi_tiao_he():
    W, H = 380, 664
    body, y = head(W, H, "大国者下流：下流不是品行低下，是水走到底的那一段",
                   "第 六 十 一 章 · 下流", "一条河", "大国者下流，天下之牝，天下之交也。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「流」，《说文》「水行也」——水在走；「下流」是水走到底的那一段。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "江河的下游，是所有上游都往那儿去的地方。", 5.2, "#6E6459", "middle"))

    t1 = y + 46
    s.append(txt(24, t1, "上游都往下走，走到低处汇成一处", 5.4, GREEN))
    ty = t1 + 66

    # 上游支流
    for x0 in (52, 104):
        s.append(f'<path d="M{x0},{ty} C{x0+16},{ty+40} {x0+34},{ty+62} {150},{ty+80}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
        s.append(arrow(x0 + 6, ty + 8, x0 + 20, ty + 32, GREEN, 0.7, head="arr2"))
    for x0 in (196, 248):
        s.append(f'<path d="M{x0},{ty} C{x0-16},{ty+40} {x0-34},{ty+62} {150},{ty+80}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
        s.append(arrow(x0 - 6, ty + 8, x0 - 20, ty + 32, GREEN, 0.7, head="arr2"))
    s.append(txt(150, ty - 12, "上游：水从高处来", 4.6, "#6E6459", "middle"))

    # 主河道 + 下游水潭
    s.append(f'<path d="M138,{ty+76} C132,{ty+110} 128,{ty+140} 122,{ty+168}" fill="none" stroke="{GREEN}" stroke-width="1.2"/>')
    s.append(f'<path d="M162,{ty+76} C168,{ty+110} 172,{ty+140} 178,{ty+168}" fill="none" stroke="{GREEN}" stroke-width="1.2"/>')
    s.append(arrow(150, ty + 100, 150, ty + 130, GREEN, 0.8, head="arr2"))
    s.append(f'<ellipse cx="150" cy="{ty+194}" rx="74" ry="26" fill="#EFE6D4" stroke="{GREEN}" stroke-width="1"/>')
    for k in range(3):
        s.append(f'<path d="M{96+k*8},{ty+186+k*6} C{126},{ty+180+k*6} {174},{ty+180+k*6} {204-k*8},{ty+186+k*6}" fill="none" stroke="{LINE2}" stroke-width="0.5"/>')
    s.append(txt(150, ty + 232, "下游：所有水都到这儿", 4.8, GREEN, "middle"))
    s.append(txt(150, ty + 246, "不是被推下去的，它本来就在那儿", 4.8, "#6E6459", "middle"))

    b = ty + 272
    s.append(txt(24, b, "「下流」是水走到底的那一段，不是品行低下。", 5.2, INK))
    s.append(txt(24, b + 16, "不往上争的水，上游非来不可——它不用抢，位置就在那里。", 5.0, INK))
    s.append(txt(24, b + 32, "大国把自己放在那一段上，天下的水自己就往这儿流。", 4.9, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "下游不是被推下去的，它本来就在那儿；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "不往上争的水，上游非来不可。", 5.6, GREEN, "middle"))
    s.append(gold(c + 62, "ch61a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十一章 · 一只母畜 ============
def ch61b_yi_zhi_mu_chu():
    W, H = 380, 620
    body, y = head(W, H, "牝常以静胜牡：胜是担得起，不是打得赢",
                   "第 六 十 一 章 · 牝", "一只母鸡", "牝常以静胜牡，以静为下。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「牝」是雌，「牡」是雄；「胜」训「肩」——是担得起，不是打得赢。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "母鸡不争，可脚边那一群，都是它孵出来的。", 5.2, "#6E6459", "middle"))

    def bird(cx, gy, col, scale=1.0, male=False, lying=False):
        o = []
        bw, bh = 26 * scale, 17 * scale
        cy_ = gy - (9 * scale if lying else 20 * scale)
        o.append(f'<ellipse cx="{cx}" cy="{cy_}" rx="{bw}" ry="{bh}" fill="#EFE6D4" stroke="{col}" stroke-width="1"/>')
        hx, hy = cx + bw - 2 * scale, cy_ - (14 * scale if male else 9 * scale)
        o.append(f'<line x1="{cx+bw-6*scale}" y1="{cy_-4*scale}" x2="{hx}" y2="{hy}" stroke="{col}" stroke-width="1.2"/>')
        o.append(f'<circle cx="{hx+3*scale}" cy="{hy-3*scale}" r="{5*scale}" fill="none" stroke="{col}" stroke-width="1"/>')
        for k in range(3):
            o.append(f'<path d="M{hx+1*scale+k*2.4*scale},{hy-8*scale} C{hx+1*scale+k*2.4*scale},{hy-12*scale} {hx+3*scale+k*2.4*scale},{hy-12*scale} {hx+3*scale+k*2.4*scale},{hy-9*scale}" fill="none" stroke="{col}" stroke-width="0.8"/>')
        o.append(f'<path d="M{hx+8*scale},{hy-3*scale} L{hx+13*scale},{hy-1*scale} L{hx+8*scale},{hy+1*scale} Z" fill="none" stroke="{col}" stroke-width="0.7"/>')
        for d in (-6, -2):
            o.append(f'<line x1="{cx-bw-2*scale}" y1="{cy_-6*scale+d*2}" x2="{cx-bw-14*scale}" y2="{cy_-14*scale+d*2}" stroke="{col}" stroke-width="0.8"/>')
        if lying:
            o.append(f'<line x1="{cx-8*scale}" y1="{gy}" x2="{cx+12*scale}" y2="{gy}" stroke="{col}" stroke-width="0.9"/>')
        else:
            for dx in (-8 * scale, 10 * scale):
                o.append(f'<line x1="{cx+dx}" y1="{cy_+bh-2}" x2="{cx+dx}" y2="{gy}" stroke="{col}" stroke-width="1"/>')
        return o

    def chick(cx, gy, col):
        o = [f'<circle cx="{cx}" cy="{gy-9}" r="7" fill="#EFE6D4" stroke="{col}" stroke-width="0.9"/>']
        o.append(f'<circle cx="{cx+6}" cy="{gy-15}" r="4" fill="none" stroke="{col}" stroke-width="0.9"/>')
        o.append(f'<path d="M{cx+10},{gy-16} L{cx+14},{gy-15} L{cx+10},{gy-14} Z" fill="none" stroke="{col}" stroke-width="0.6"/>')
        o.append(f'<line x1="{cx-2}" y1="{gy-2}" x2="{cx-2}" y2="{gy}" stroke="{col}" stroke-width="0.8"/>')
        o.append(f'<line x1="{cx+3}" y1="{gy-2}" x2="{cx+3}" y2="{gy}" stroke="{col}" stroke-width="0.8"/>')
        return o

    # 一、牡
    t1 = y + 46
    s.append(txt(24, t1, "一、牡：昂着头，争那一步", 5.4, SEAL))
    gy1 = t1 + 112
    s.append(f'<line x1="24" y1="{gy1}" x2="240" y2="{gy1}" stroke="{INK}" stroke-width="1"/>')
    s += bird(86, gy1, SEAL, 1.15, male=True)
    s.append(txt(160, gy1 - 52, "一只，站着", 4.8, SEAL))
    s.append(txt(160, gy1 - 40, "冠最高，脚边没有别的", 4.4, "#6E6459"))
    s.append(txt(86, gy1 + 14, "牡：以力相争", 4.6, SEAL, "middle"))

    # 二、牝
    t2 = gy1 + 34
    s.append(txt(24, t2, "二、牝：静着卧下，脚边一群", 5.4, GREEN))
    gy2 = t2 + 118
    s.append(f'<line x1="24" y1="{gy2}" x2="240" y2="{gy2}" stroke="{INK}" stroke-width="1"/>')
    s += bird(70, gy2, GREEN, 1.1, male=False, lying=True)
    for dx in (120, 152, 184):
        s += chick(dx, gy2, GREEN)
    s.append(txt(70, gy2 + 14, "牝：静着，不动", 4.6, GREEN, "middle"))
    s.append(txt(168, gy2 + 14, "跟着的那群，都是它孵的", 4.4, "#6E6459", "middle"))

    b = gy2 + 40
    s.append(txt(24, b, "「胜」是担得起，不是打得赢：母鸡不争，脚边那一群都是它的。", 4.8, INK))
    s.append(txt(24, b + 16, "静不是不动，是不必动；下不是低人一等，是让水自己流过来。", 4.9, INK))
    s.append(txt(24, b + 32, "以静为下：静到那个位置，就有人来。", 5.1, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "「胜」是担得起，不是打得赢；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "母畜担得起，因为后面那一群都是它生的。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch61b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十一章 · 一只手 ============
def ch61c_yi_zhi_shou():
    W, H = 380, 656
    body, y = head(W, H, "或下以取：取本义带刀，加一个「下」，刀就翻成了手",
                   "第 六 十 一 章 · 取", "一只手", "故或下以取，或下而取。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「取」从又从耳：杀敌之后割左耳计功——本义带刀。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "前面加一个「下」，刀就翻成了手：不是去割，是去接。", 5.0, "#6E6459", "middle"))

    def ear(cx, cy, col):
        o = [f'<path d="M{cx},{cy+12} C{cx+9},{cy+8} {cx+11},{cy-4} {cx+4},{cy-10} C{cx-2},{cy-15} {cx-9},{cy-10} {cx-6},{cy-2} C{cx-3},{cy+5} {cx+2},{cy+6} {cx+3},{cy}" fill="none" stroke="{col}" stroke-width="1.1"/>']
        o.append(f'<path d="M{cx+1},{cy+2} C{cx+4},{cy-2} {cx+2},{cy-6} {cx-1},{cy-7}" fill="none" stroke="{col}" stroke-width="0.6"/>')
        return o

    def knife(x, y, col):
        o = [f'<rect x="{x-3}" y="{y}" width="6" height="16" rx="2" fill="none" stroke="{col}" stroke-width="0.8"/>']
        o.append(f'<path d="M{x-2},{y} L{x-2},{y-34} C{x+10},{y-30} {x+14},{y-20} {x+12},{y-6} L{x+2},{y}" fill="#EFE6D4" stroke="{col}" stroke-width="1"/>')
        return o

    def hand(cx, cy, col):
        o = [f'<rect x="{cx-19}" y="{cy-8}" width="38" height="22" rx="8" fill="#EFE6D4" stroke="{col}" stroke-width="1.1"/>']
        for k in range(4):
            o.append(f'<rect x="{cx-17+k*9}" y="{cy-24+k*0.9}" width="6" height="16" rx="3" fill="#EFE6D4" stroke="{col}" stroke-width="0.9"/>')
        o.append(f'<rect x="{cx-27}" y="{cy-2}" width="12" height="6" rx="3" fill="#EFE6D4" stroke="{col}" stroke-width="0.9"/>')
        return o

    # 一、刀
    t1 = y + 46
    s.append(txt(24, t1, "一、带刀：取本义，是割", 5.4, SEAL))
    cy1 = t1 + 116
    s.append(f'<line x1="118" y1="{cy1-88}" x2="118" y2="{cy1-72}" stroke="{LINE}" stroke-width="0.7"/>')
    s += ear(118, cy1 - 60, INK)
    s += knife(168, cy1 - 40, SEAL)
    s.append(arrow(186, cy1 - 82, 162, cy1 - 62, SEAL, 0.8, head="arrS"))
    s.append(txt(118, cy1 - 84, "一只耳，挂在这儿", 4.4, INK, "middle"))
    s.append(txt(118, cy1 + 8, "割下来计功：这是「取」的老底子", 4.6, SEAL, "middle"))
    s.append(txt(196, cy1 - 34, "刀落下去：割", 4.6, SEAL))

    # 二、手
    t2 = cy1 + 76
    s.append(txt(24, t2, "二、加一个「下」：掌心翻上来，去接", 5.2, GREEN))
    cy2 = t2 + 106
    s += hand(120, cy2, GREEN)
    s.append(f'<line x1="146" y1="{cy2-34}" x2="158" y2="{cy2-22}" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    s += ear(160, cy2 - 14, GREEN)
    s.append(arrow(168, cy2 - 44, 160, cy2 - 26, GREEN, 0.7, head="arr2"))
    s.append(txt(196, cy2 - 40, "来归的，落下来", 4.6, GREEN))
    s.append(txt(196, cy2 - 28, "手在下面接着", 4.4, "#6E6459"))
    s.append(txt(120, cy2 + 34, "刀口还在，只是翻过去了", 4.6, GREEN, "middle"))

    b = cy2 + 52
    s.append(txt(24, b, "「取」从又从耳，本义带刀：割左耳计功。", 4.9, INK))
    s.append(txt(24, b + 16, "前面加一个「下」，刀就翻成了手——不是去割，是去接。", 4.9, INK))
    s.append(txt(24, b + 32, "刀口还在，只是翻过去了；翻过去的刀，就成了接的手。", 4.9, GREEN))

    c = b + 50
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "取本义带刀；加一个「下」，刀就翻成了手——", 5.2, INK, "middle"))
    s.append(txt(190, c + 36, "不是去割，是去接。", 6.0, GREEN, "middle"))
    s.append(gold(c + 62, "ch61c"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十二章 · 一个墙角 ============
def ch62a_yi_ge_qiang_jiao():
    W, H = 380, 706
    body, y = head(W, H, "奥是室之西南隅：最尊，也最暗；不是深奥，是那个角",
                   "第 六 十 二 章 · 奥", "一个墙角", "道者，万物之奥。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「奥」，《说文》「宛也，室之西南隅」——就是屋里西南那个角。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "那个角，古人祭神、尊长坐；也最暗——「不见户明」。", 5.0, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、屋里那个角：最尊，也最暗", 4.8, SEAL))

    gy = y + 66
    rx0, rx1 = 56, 322
    ry0, ry1 = gy, gy + 176

    # 地板
    s.append(f'<rect x="{rx0}" y="{ry0}" width="{rx1 - rx0}" height="{ry1 - ry0}" fill="#FBF6EC" stroke="none"/>')
    # 光楔：门在南墙右段，光往里走一程就停
    s.append(f'<polygon points="242,{ry1 - 4} 276,{ry1 - 4} 300,{ry0 + 48} 160,{ry0 + 26}" '
             f'fill="#EADFC2" opacity="0.6" stroke="none"/>')
    s.append(f'<path d="M160,{ry0 + 26} Q230,{ry0 + 32} 300,{ry0 + 48}" fill="none" stroke="{SEAL}" '
             f'stroke-width="1" stroke-dasharray="4 3"/>')
    # 西南角：暗（加点竖纹，显出暗）
    s.append(f'<rect x="{rx0 + 4}" y="{ry1 - 48}" width="54" height="44" fill="#DBCFB7" stroke="none"/>')
    for k in range(5):
        s.append(f'<line x1="{rx0 + 10 + k * 10}" y1="{ry1 - 46}" x2="{rx0 + 10 + k * 10}" y2="{ry1 - 6}" '
                 f'stroke="#C6B79B" stroke-width="0.6"/>')
    # 席
    s.append(f'<rect x="{rx0 + 18}" y="{ry1 - 38}" width="26" height="25" fill="none" stroke="{INK}" stroke-width="1"/>')
    for k in range(3):
        s.append(f'<line x1="{rx0 + 18}" y1="{ry1 - 30 + k * 8}" x2="{rx0 + 44}" y2="{ry1 - 30 + k * 8}" '
                 f'stroke="{LINE}" stroke-width="0.5"/>')
    # 四壁
    s.append(f'<rect x="{rx0}" y="{ry0 - 5}" width="{rx1 - rx0}" height="5" fill="#E6DCC6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{rx0 - 5}" y="{ry0 - 5}" width="5" height="{ry1 - ry0 + 10}" fill="#E6DCC6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{rx1}" y="{ry0 - 5}" width="5" height="{ry1 - ry0 + 10}" fill="#E6DCC6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="{rx0 - 5}" y="{ry1}" width="247 - {rx0}" height="5" fill="#E6DCC6" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<rect x="276" y="{ry1}" width="{rx1 + 5 - 276}" height="5" fill="#E6DCC6" stroke="{INK}" stroke-width="0.8"/>')
    # 门扇弧
    s.append(f'<path d="M242,{ry1} A36,36 0 0 1 278,{ry1 - 36}" fill="none" stroke="{LINE}" '
             f'stroke-width="0.8" stroke-dasharray="2 2"/>')

    s.append(txt(259, ry1 + 18, "门：光从这儿进来", 4.6, SEAL, "middle"))
    s.append(txt(296, ry0 + 62, "光只到这儿", 4.4, SEAL, "end"))
    s.append(txt(120, ry1 - 34, "西南角：最尊", 4.8, INK))
    s.append(txt(120, ry1 - 20, "也最暗——光进不去", 4.6, "#6E6459"))

    s.append(txt(190, ry1 + 38, "万物归到这儿：不是归到光亮的台上被审判，", 4.6, SEAL, "middle"))
    s.append(txt(190, ry1 + 52, "是归到一个连光都进不去的角里，被收着。", 4.6, SEAL, "middle"))

    s.append(txt(24, ry1 + 74, "二、帛书作「注」：水往一处流", 4.8, GREEN))
    gy2 = ry1 + 92
    s.append(arrow(96, gy2 + 2, 178, gy2 + 38, GREEN, 1, head="arr2"))
    s.append(arrow(190, gy2 - 14, 190, gy2 + 44, GREEN, 1, head="arr2"))
    s.append(arrow(284, gy2 + 2, 202, gy2 + 38, GREEN, 1, head="arr2"))
    s.append(f'<ellipse cx="190" cy="{gy2 + 54}" rx="30" ry="9" fill="#EFE6D4" stroke="{GREEN}" stroke-width="1"/>')
    s.append(txt(190, gy2 + 56, "一处", 4.2, GREEN, "middle"))
    s.append(txt(190, gy2 + 80, "注：水往一处流——奥讲屋，注讲水，讲的是同一件事", 4.6, "#6E6459", "middle"))

    a = gy2 + 98
    s.append(txt(24, a, "「注」是水往一处流，「奥」是屋里的那个角：一个讲水，一个讲屋，", 4.8, INK))
    s.append(txt(24, a + 16, "讲的却是同一件事——有个地方，东西都往那儿去。", 4.9, INK))
    s.append(txt(24, a + 34, "尊，是因为没人敢坐；暗，是因为光进不去——暗，才是它能容的原因。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "奥是最尊又最暗的那个角；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "不是归到光亮的台上，是归到一个角落被收着。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch62a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十二章 · 一副背带 ============
def ch62b_yi_fu_bei_dai():
    W, H = 380, 700
    body, y = head(W, H, "保是从人从孚：不是给个地方，是驮在身上走",
                   "第 六 十 二 章 · 保", "一副背带", "善人之宝，不善人之所保。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「保」，《说文》「养也」，从人从孚——孚，是一只被抱住的孩子。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "本义是背着孩子：驮在背上，两只手还要腾出来干活。", 5.0, "#6E6459", "middle"))

    def child(cx, gy, col, k=1.0):
        o = []
        o.append(f'<circle cx="{cx}" cy="{gy - 34 * k}" r="{5 * k}" fill="none" stroke="{col}" stroke-width="1"/>')
        o.append(f'<rect x="{cx - 6 * k}" y="{gy - 28 * k}" width="{12 * k}" height="{16 * k}" rx="2" '
                 f'fill="#EFE6D4" stroke="{col}" stroke-width="1"/>')
        o.append(f'<line x1="{cx - 3 * k}" y1="{gy - 12 * k}" x2="{cx - 4 * k}" y2="{gy}" stroke="{col}" stroke-width="1"/>')
        o.append(f'<line x1="{cx + 3 * k}" y1="{gy - 12 * k}" x2="{cx + 4 * k}" y2="{gy}" stroke="{col}" stroke-width="1"/>')
        return o

    s.append(txt(24, y + 48, "一、收留：给一个地方", 4.8, "#6E6459"))
    gy1 = y + 172
    # 门框
    s.append(f'<rect x="126" y="{gy1 - 64}" width="6" height="64" fill="#E6DCC6" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<rect x="208" y="{gy1 - 64}" width="6" height="64" fill="#E6DCC6" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M126,{gy1 - 64} Q170,{gy1 - 82} 214,{gy1 - 64}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # 给的那块地方
    s.append(f'<rect x="152" y="{gy1}" width="36" height="7" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s += child(170, gy1, INK)
    s.append(txt(190, gy1 + 26, "收留：给一个地方", 4.8, "#6E6459", "middle"))
    s.append(txt(190, gy1 + 40, "地方是死的，人在地方里", 4.4, "#6E6459", "middle"))

    s.append(txt(24, gy1 + 66, "二、背着：驮在身上，走到哪儿带到哪儿", 4.8, SEAL))
    gy2 = gy1 + 190
    # 背上驮着的包袱：孩子的小脑袋从包袱口露出来
    s.append(f'<path d="M174,{gy2 - 48} Q174,{gy2 - 56} 182,{gy2 - 56} L190,{gy2 - 56} Q196,{gy2 - 56} 196,{gy2 - 47} '
             f'L196,{gy2 - 26} L174,{gy2 - 26} Z" fill="#F6EFE0" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<circle cx="185" cy="{gy2 - 60}" r="5" fill="#F6EFE0" stroke="{SEAL}" stroke-width="1"/>')
    s.append(f'<line x1="182" y1="{gy2 - 66}" x2="188" y2="{gy2 - 66}" stroke="{SEAL}" stroke-width="0.8"/>')
    # 大人：侧身，背朝左
    s.append(f'<line x1="200" y1="{gy2 - 26}" x2="197" y2="{gy2}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="213" y1="{gy2 - 26}" x2="216" y2="{gy2}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="194" y="{gy2 - 54}" width="22" height="28" rx="3" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="208" cy="{gy2 - 64}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="194" y1="{gy2 - 52}" x2="209" y2="{gy2 - 34}" stroke="{SEAL}" stroke-width="1" stroke-dasharray="2.4 1.8"/>')
    # 前手与篮
    s.append(f'<line x1="216" y1="{gy2 - 48}" x2="232" y2="{gy2 - 30}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M224,{gy2 - 26} A10,8 0 0 0 244,{gy2 - 26}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<path d="M223,{gy2 - 26} L225,{gy2 - 8} L243,{gy2 - 8} L245,{gy2 - 26}" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(252, gy2 - 32, "手还空着", 4.2, "#6E6459"))
    s.append(txt(190, gy2 + 26, "背着：驮在背上，手还腾着提篮", 4.8, SEAL, "middle"))
    s.append(txt(190, gy2 + 40, "人走到哪儿，孩子就到哪儿", 4.4, "#6E6459", "middle"))

    a = gy2 + 62
    s.append(txt(24, a, "宝是自己收着的，保是背着孩子的：一个揣在怀里，一个驮在背上。", 4.8, INK))
    s.append(txt(24, a + 16, "收留是给个地方，人得待在那儿；背着是带在身上，走到哪儿带到哪儿。", 4.9, INK))
    s.append(txt(24, a + 34, "「太保」做的就是这件事；道对不善之人做的事，就是太保做的事。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "宝是自己收着的，保是背着孩子的；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "一个揣在怀里，一个驮在背上。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch62b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十二章 · 一个坐姿 ============
def ch62c_yi_ge_zuo_zi():
    W, H = 380, 686
    body, y = head(W, H, "坐训止，进训登：停住，却往上走——这条路上不用脚",
                   "第 六 十 二 章 · 坐", "一个坐姿", "虽有拱璧以先驷马，不如坐进此道。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「坐」，《说文》「止也」——停下来；「进」，《说文》「登也」——往上走。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "两个字摆在一起，是一对矛盾：停住，却往上走。", 5.0, "#6E6459", "middle"))

    def tread(cx, cy, col, sc=0.78):
        inner = [f'<path d="M-9,-12 C-11,-2 -10,9 -4,14 C2,18 8,10 9,-2 C10,-11 6,-17 -1,-17 C-6,-17 -8,-16 -9,-12 Z" '
                 f'fill="none" stroke="{col}" stroke-width="1.3"/>',
                 f'<circle cx="-6" cy="-20" r="2.3" fill="none" stroke="{col}" stroke-width="1"/>',
                 f'<circle cx="-1.5" cy="-23" r="2.0" fill="none" stroke="{col}" stroke-width="1"/>',
                 f'<circle cx="2.5" cy="-22" r="1.7" fill="none" stroke="{col}" stroke-width="1"/>',
                 f'<circle cx="6" cy="-19" r="1.5" fill="none" stroke="{col}" stroke-width="1"/>']
        return [f'<g transform="translate({cx},{cy}) scale({sc})">' + "".join(inner) + '</g>']

    s.append(txt(24, y + 48, "一、用脚：一步一阶", 4.8, "#6E6459"))
    gy1 = y + 196
    # 俯看的台阶：一级一级往上收
    for k in range(7):
        ty = gy1 - 14 - k * 14
        col = "#EFE6D4" if k % 2 == 0 else "#F6EFE0"
        s.append(f'<rect x="132" y="{ty}" width="112" height="14" fill="{col}" stroke="{INK}" stroke-width="0.8"/>')
    s += tread(170, gy1 - 36, INK, 0.66)
    s += tread(206, gy1 - 78, INK, 0.66)
    s.append(arrow(124, gy1 - 4, 124, gy1 - 104, "#6E6459", 1, dash="3 2"))
    s.append(txt(124, gy1 - 110, "往上", 4.2, "#6E6459", "middle"))
    s.append(txt(190, gy1 + 24, "用脚：一步一阶，两个脚印隔着一阶", 4.8, "#6E6459", "middle"))

    s.append(txt(24, gy1 + 52, "二、不用脚：坐在这儿，就往上走", 4.8, SEAL))
    gy2 = gy1 + 150
    # 盘坐
    s.append(f'<line x1="120" y1="{gy2}" x2="262" y2="{gy2}" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="176" y1="{gy2 - 26}" x2="158" y2="{gy2 - 8}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="204" y1="{gy2 - 26}" x2="222" y2="{gy2 - 8}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="158" y1="{gy2 - 8}" x2="198" y2="{gy2 - 2}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="222" y1="{gy2 - 8}" x2="182" y2="{gy2 - 2}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M178,{gy2 - 54} L202,{gy2 - 54} L206,{gy2 - 24} L174,{gy2 - 24} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="190" cy="{gy2 - 64}" r="7.5" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="180" y1="{gy2 - 50} " x2="164" y2="{gy2 - 16}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="200" y1="{gy2 - 50}" x2="216" y2="{gy2 - 16}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="163" cy="{gy2 - 14}" rx="4" ry="3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<ellipse cx="217" cy="{gy2 - 14}" rx="4" ry="3" fill="#EFE6D4" stroke="{INK}" stroke-width="0.9"/>')
    # 止：压地的那条线
    s.append(f'<line x1="146" y1="{gy2 + 8}" x2="234" y2="{gy2 + 8}" stroke="{LINE}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(arrow(190, gy2 - 80, 190, gy2 - 120, GREEN, 1.2, dash="3 2", head="arr2"))
    s.append(txt(200, gy2 - 110, "进：往上走", 4.6, GREEN))
    s.append(txt(146, gy2 + 26, "坐：停住，脚不用迈", 4.6, SEAL))

    a = gy2 + 50
    s.append(txt(24, a, "第一条路上，「进」是脚的事；这一条路上，「进」是坐的事。", 4.8, INK))
    s.append(txt(24, a + 16, "往外走要开路，往里走只要坐下：停了，才升得起来。", 4.9, INK))
    s.append(txt(24, a + 34, "帛书作「坐而进此」——多一个「而」字：先停，再进。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "坐是停，进是登；", 5.8, INK, "middle"))
    s.append(txt(190, c + 36, "这条路上的「进」，脚一步也不用迈。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch62c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十三章 · 一支笔 ============
def ch63a_yi_zhi_bi():
    W, H = 380, 606
    body, y = head(W, H, "图训画计难：先把那个难画出来，才有得打算",
                   "第 六 十 三 章 · 图", "一支笔", "图难于其易，为大于其细。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「图」，《说文》「画计难也」——先把难处画出来，再打算。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以「图难于其易」，不是趁容易时解决难，是趁它还容易，先把难画出来。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、木牍上那道山：先画，还没发生", 4.8, SEAL))
    gy = y + 58
    # 木牍
    s.append(f'<rect x="100" y="{gy}" width="150" height="196" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<rect x="104" y="{gy + 4}" width="142" height="188" fill="none" stroke="{LINE}" stroke-width="0.6"/>')
    # 山形：一道还没长成的难
    s.append(f'<path d="M116,{gy + 172} L140,{gy + 96} L158,{gy + 128} L182,{gy + 72} L206,{gy + 120} L230,{gy + 172}" '
             f'fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<path d="M116,{gy + 172} L230,{gy + 172}" stroke="{LINE}" stroke-width="0.8"/>')
    # 山脚那株苗
    s.append(f'<line x1="214" y1="{gy + 172}" x2="214" y2="{gy + 150}" stroke="{GREEN}" stroke-width="1.3"/>')
    s.append(f'<line x1="214" y1="{gy + 158}" x2="204" y2="{gy + 147}" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<line x1="214" y1="{gy + 153}" x2="224" y2="{gy + 142}" stroke="{GREEN}" stroke-width="1.1"/>')
    s.append(f'<path d="M204,{gy + 147} l-3,-1" stroke="{GREEN}" stroke-width="1"/>')
    s.append(f'<path d="M224,{gy + 142} l3,-1" stroke="{GREEN}" stroke-width="1"/>')
    # 笔：杆长，笔尖点在苗边
    s.append(f'<line x1="308" y1="{gy + 26}" x2="236" y2="{gy + 150}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<line x1="308" y1="{gy + 18}" x2="308" y2="{gy + 28}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M236,{gy + 148} L244,{gy + 162} L226,{gy + 158} Z" fill="{SEAL}" stroke="{SEAL}" stroke-width="0.8"/>')

    s.append(txt(190, gy + 214, "牍上先画：山是难，山脚那株苗，是它现在的样子", 4.6, "#6E6459", "middle"))

    a = gy + 236
    s.append(txt(24, a, "「图」是「画计难」：难还没来时，先把它画在牍上，才知道往哪儿下手。", 4.8, INK))
    s.append(txt(24, a + 16, "等它长成一座山，就只剩对着山叹气；趁它还是那株苗，才画得动。", 4.9, INK))
    s.append(txt(24, a + 34, "为大于其细：大不是从大处做起的，是从那一笔点得下去的地方做起的。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "图是「画计难」：先把难画出来，才有得打算；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "趁它还小，笔才落得下去。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch63a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十三章 · 一根丝 ============
def ch63b_yi_gen_si():
    W, H = 380, 592
    body, y = head(W, H, "细从糸：一根一根，不断；大事是一束，细是那一根",
                   "第 六 十 三 章 · 细", "一根丝", "天下大事，必作于细。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「细」，《说文》「微也」，从糸——糸是丝，一根一根。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "大事不是一块石头，是一束线：它只能一根一根抽出来。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、一束，还是一根", 4.8, SEAL))
    gy = y + 62
    # 挂线的那根杆
    s.append(f'<line x1="112" y1="{gy}" x2="252" y2="{gy}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="112" y1="{gy - 6}" x2="112" y2="{gy + 6}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<line x1="252" y1="{gy - 6}" x2="252" y2="{gy + 6}" stroke="{INK}" stroke-width="1"/>')
    # 一束：十几根垂着的丝
    for i in range(13):
        x0 = 120 + i * 9.5
        end = gy + 84 + (6 if i % 3 == 0 else 0) + (3 if i % 4 == 1 else 0)
        s.append(f'<line x1="{x0}" y1="{gy + 2}" x2="{x0 - 1}" y2="{end}" stroke="#B9AA95" stroke-width="0.9"/>')
    # 从束里抽出来的一根，往右一直延出去
    s.append(f'<path d="M230,{gy + 6} C252,{gy + 22} 268,{gy + 38} 316,{gy + 32}" fill="none" stroke="{GREEN}" stroke-width="1.6"/>')
    s.append(txt(186, gy + 112, "一束：看着是一件事", 4.5, "#6E6459", "middle"))
    s.append(txt(266, gy + 8, "抽这一根出来，一直不断", 4.4, GREEN, "middle"))

    a = gy + 136
    s.append(txt(24, a, "「细」从糸：丝是一根一根的，抽不断，才织得成整幅。", 4.8, INK))
    s.append(txt(24, a + 16, "天下大事，必作于细——不是先有大石，是先有一根一根的线。", 4.9, INK))
    s.append(txt(24, a + 34, "一束看着是一件事，可它只能一根一根地往下抽。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "细从糸，微也：一根一根，不断；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "大事是一束，可它只能一根一根抽出来。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch63b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十三章 · 一条尾巴 ============
def ch63c_yi_tiao_wei_ba():
    W, H = 380, 604
    body, y = head(W, H, "易本是蜥蜴：会变色，会断尾——看得容易，是没看见它会变",
                   "第 六 十 三 章 · 易", "一条尾巴", "夫轻诺必寡信，多易必多难。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「易」本义是蜥蜴：会变色，会断尾——不是「容易」那个易。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "你看它趴着不动，就当它不会变；一拉，尾巴先没了。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、会变色、会断尾的那条尾巴", 4.8, SEAL))
    gy = y + 196
    # 地
    s.append(f'<line x1="76" y1="{gy + 18}" x2="318" y2="{gy + 18}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    # 身子：半青半赭，显出会变色
    s.append(f'<ellipse cx="184" cy="{gy - 34}" rx="44" ry="16" fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M184,{gy - 50} A44,16 0 0 0 184,{gy - 18} L184,{gy - 18} Z" fill="#CFD8CD" stroke="none"/>')
    s.append(f'<path d="M184,{gy - 50} A44,16 0 0 1 228,{gy - 34} L184,{gy - 34} Z" fill="#E3D2C6" stroke="none"/>')
    s.append(f'<ellipse cx="184" cy="{gy - 34}" rx="44" ry="16" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # 头与口
    s.append(f'<path d="M146,{gy - 44} C132,{gy - 42} 112,{gy - 38} 102,{gy - 34} C112,{gy - 29} 132,{gy - 24} 146,{gy - 22}" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<circle cx="126" cy="{gy - 34}" r="1.7" fill="{INK}"/>')
    s.append(f'<path d="M102,{gy - 34} L116,{gy - 32}" stroke="{INK}" stroke-width="0.8"/>')
    # 四足：折一下，带趾
    for (ax, ay, bx2, by2, tx, ty) in ((156, gy - 20, 150, gy - 4, 146, gy + 16),
                                       (176, gy - 18, 174, gy - 2, 172, gy + 16),
                                       (204, gy - 18, 208, gy - 2, 212, gy + 16),
                                       (220, gy - 22, 226, gy - 6, 232, gy + 14)):
        s.append(f'<path d="M{ax},{ay} L{bx2},{by2} L{tx},{ty}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<line x1="{tx}" y1="{ty}" x2="{tx - 4}" y2="{ty}" stroke="{INK}" stroke-width="0.7"/>')
    # 尾：连着的这一段，断口在这儿
    s.append(f'<path d="M226,{gy - 40} C248,{gy - 42} 264,{gy - 30} 270,{gy - 18}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="272" y1="{gy - 22}" x2="278" y2="{gy - 16}" stroke="{SEAL}" stroke-width="1.6"/>')
    s.append(f'<line x1="268" y1="{gy - 18}" x2="274" y2="{gy - 12}" stroke="{SEAL}" stroke-width="1.6"/>')
    # 断下来的那一截，落在地上
    s.append(f'<path d="M278,{gy - 8} C292,{gy + 2} 302,{gy + 8} 310,{gy + 16}" fill="none" stroke="{INK}" '
             f'stroke-width="1.2" stroke-dasharray="2 1.6"/>')
    s.append(txt(300, gy + 34, "断了的那一截", 4.2, SEAL, "middle"))
    s.append(txt(120, gy + 34, "半青半赭：它会变色", 4.4, "#6E6459", "middle"))

    a = gy + 58
    s.append(txt(24, a, "「易」本是蜥蜴的名字：会变色，尾巴一拉就断，断了自己再长。", 4.8, INK))
    s.append(txt(24, a + 16, "轻诺、多易，错在把趴着不动的当成了不会动的。", 4.9, INK))
    s.append(txt(24, a + 34, "圣人犹难之：连看得容易的，也先当它会变，所以终无难。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "易本是蜥蜴：会变色，会断尾；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "看得容易，是没看见它会变。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch63c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十四章 · 一片龟甲 ============
def ch64a_yi_pian_gui_jia():
    W, H = 380, 620
    body, y = head(W, H, "兆是烧出来的那道裂纹：还没烧，就还读不出来",
                   "第 六 十 四 章 · 兆", "一片龟甲", "其安易持，其未兆易谋。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「兆」，《说文》「灼龟坼也」——烧龟甲，烧出来的那道裂纹。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "所以「未兆」不是还没有征兆，是还没烧、还没裂、还读不出来。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、这片甲：钻了孔，还没点火", 4.8, SEAL))
    gy = y + 62
    # 龟腹甲
    s.append(f'<path d="M170,{gy + 26} C118,{gy + 26} 92,{gy + 56} 92,{gy + 84} C92,{gy + 116} 124,{gy + 138} 170,{gy + 138} '
             f'C216,{gy + 138} 248,{gy + 116} 248,{gy + 84} C248,{gy + 56} 222,{gy + 26} 170,{gy + 26} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1.4"/>')
    s.append(f'<line x1="170" y1="{gy + 30}" x2="170" y2="{gy + 134}" stroke="{LINE}" stroke-width="0.9"/>')
    for (yy, x0, x1) in ((gy + 56, 122, 218), (gy + 82, 104, 236), (gy + 108, 118, 222)):
        s.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{LINE}" stroke-width="0.7"/>')
    # 钻孔
    s.append(f'<circle cx="170" cy="{gy + 44}" r="5" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<circle cx="170" cy="{gy + 44}" r="1.6" fill="{INK}"/>')
    # 还没裂出来的那道纹：虚线
    s.append(f'<path d="M170,{gy + 48} L160,{gy + 76} L168,{gy + 96}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(f'<path d="M170,{gy + 48} L182,{gy + 78} L176,{gy + 100}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 3"/>')
    # 底下的火：还没点
    s.append(f'<line x1="140" y1="{gy + 170}" x2="200" y2="{gy + 170}" stroke="{INK}" stroke-width="1.4"/>')
    for (fx, fh) in ((152, 12), (166, 18), (180, 12)):
        s.append(f'<path d="M{fx},{gy + 169} C{fx - 4},{gy + 169 - fh} {fx},{gy + 161 - fh} {fx + 3},{gy + 157 - fh} '
                 f'C{fx + 7},{gy + 163 - fh} {fx + 6},{gy + 169} {fx + 4},{gy + 169} Z" '
                 f'fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="2 2"/>')
    s.append(txt(200, gy + 164, "火还没点", 4.2, SEAL))

    s.append(txt(258, gy + 74, "钻了孔，", 4.6, INK))
    s.append(txt(258, gy + 88, "还没点火", 4.6, INK))
    s.append(txt(190, gy + 194, "火还没点，纹还没裂——所以现在，什么都还不是", 4.6, SEAL, "middle"))

    a = gy + 216
    s.append(txt(24, a, "「兆」是烧出来的那道裂：兆出来了，吉凶才读得出来。", 4.8, INK))
    s.append(txt(24, a + 16, "「未兆」不是征兆还小，是还没裂——连它自己都还不知道往哪儿走。", 4.9, INK))
    s.append(txt(24, a + 34, "其未兆易谋：趁它还没裂，还来得及决定它裂成什么样。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "兆是烧出来的那道裂纹；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "还没烧，就还读不出来——也还来得及。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch64a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十四章 · 一筐土 ============
def ch64b_yi_kuang_tu():
    W, H = 380, 620
    body, y = head(W, H, "九层之台，起于累土：台有多高，等于抬过多少筐",
                   "第 六 十 四 章 · 累", "一筐土", "九层之台，起于累土。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "台不是一次垒成的：一筐一筐抬上去，抬过多少筐，就有多少高。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "「累」，《说文》「增也」——一层一层往上加。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、一筐，就是一层", 4.8, SEAL))
    gy = y + 196
    # 台：一层比一层窄
    for k in range(6):
        wy = 150 - k * 12
        ty = gy - 22 * (k + 1)
        s.append(f'<rect x="{180 - wy / 2}" y="{ty}" width="{wy}" height="22" fill="{"#EFE6D4" if k % 2 == 0 else "#F6EFE0"}" '
                 f'stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{180 - wy / 2 + 8}" y1="{ty + 11}" x2="{180 + wy / 2 - 8}" y2="{ty + 11}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(f'<line x1="88" y1="{gy}" x2="332" y2="{gy}" stroke="{INK}" stroke-width="1.4"/>')
    # 地上那筐土
    s.append(f'<path d="M292,{gy - 2} L297,{gy + 20} L319,{gy + 20} L324,{gy - 2}" fill="#EFE6D4" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M297,{gy - 2} C303,{gy - 10} 313,{gy - 10} 319,{gy - 2}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<ellipse cx="308" cy="{gy}" rx="13" ry="4" fill="#DBCFB7" stroke="{INK}" stroke-width="0.8"/>')
    # 抬上去的那一路
    s.append(arrow(286, gy - 22, 236, gy - 126, GREEN, 1.2, dash="3 2", head="arr2"))
    s.append(txt(308, gy + 34, "一筐土", 4.4, "#6E6459", "middle"))
    s.append(txt(246, gy - 142, "抬到顶上，", 4.3, GREEN))
    s.append(txt(246, gy - 130, "就多一层", 4.3, GREEN))

    a = gy + 44
    s.append(txt(24, a, "九层之台，起于累土：每一筐都要走那段坡，都要对齐。", 4.8, INK))
    s.append(txt(24, a + 16, "台的高度，等于抬过的次数——不是等于想过多高。", 4.9, INK))
    s.append(txt(24, a + 34, "千里之行，始于足下：远不是一步跨过去的，是一步一步攒出来的。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "九层之台，起于累土；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "台有多高，等于抬过多少筐。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch64b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十四章 · 一块骨头 ============
def ch64c_yi_kuai_gu_tou():
    W, H = 380, 610
    body, y = head(W, H, "辅是颊车：牙自己长，骨头只托——托住，别去捏",
                   "第 六 十 四 章 · 辅", "一块骨头", "以辅万物之自然而不敢为。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「辅」，《说文》「人颊车也」——脸颊里那块牙床骨。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "牙不是牙床长出来的：牙自己长，骨头只给它一个位置，托住。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、牙床托着的那排牙", 4.8, SEAL))
    gy = y + 196
    # 牙床
    s.append(f'<path d="M112,{gy} C124,{gy - 66} 250,{gy - 66} 264,{gy}" fill="none" stroke="{INK}" stroke-width="3.4"/>')
    s.append(f'<path d="M118,{gy - 4} C130,{gy - 58} 246,{gy - 58} 258,{gy - 4}" fill="none" stroke="{LINE}" stroke-width="0.8"/>')
    # 一排牙：各按牙床的弧线站
    for (tx, ty) in ((132, gy - 34), (152, gy - 50), (172, gy - 58), (192, gy - 60), (212, gy - 54), (232, gy - 40)):
        s.append(f'<rect x="{tx - 6}" y="{ty - 22}" width="12" height="24" rx="3" fill="#FBF6EC" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{tx - 3}" y1="{ty - 18}" x2="{tx - 3}" y2="{ty - 2}" stroke="{LINE}" stroke-width="0.6"/>')
    # 牙自己往上长：虚线上长的箭头
    s.append(arrow(182, gy - 96, 182, gy - 128, GREEN, 1.1, dash="3 2", head="arr2"))
    s.append(arrow(158, gy - 84, 158, gy - 104, GREEN, 1, dash="3 2", head="arr2"))
    s.append(arrow(208, gy - 84, 208, gy - 104, GREEN, 1, dash="3 2", head="arr2"))
    s.append(txt(192, gy - 132, "牙自己长", 4.5, GREEN))
    s.append(txt(258, gy - 38, "骨头只托", 4.5, INK))
    s.append(txt(120, gy + 22, "托得好，牙正；托得歪，牙斜；骨头一动，满口都疼", 4.6, "#6E6459"))

    a = gy + 48
    s.append(txt(24, a, "「辅」是颊车，就是牙床骨：它不造牙，只给牙一个位置。", 4.8, INK))
    s.append(txt(24, a + 16, "以辅万物之自然而不敢为：托住，不捏——捏，就是替它长。", 4.9, INK))
    s.append(txt(24, a + 34, "《左传》「辅车相依，唇亡齿寒」：辅与车是两块互相靠着的骨头。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "牙自己长，骨头只托；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "辅万物之自然，就是托住，不去捏。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch64c"))
    s.append('</svg>')
    return "\n".join(s)



# ============ 第六十五章 · 一盏灯 ============
def ch65a_yi_zhan_deng():
    W, H = 380, 690
    body, y = head(W, H, "明是月光从窗格照进屋：照，是打光，不是自己亮",
                   "第 六 十 五 章 · 明", "一盏灯", "非以明民，将以愚之。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「明」，《说文》「照也」，从月、从囧——囧是窗格。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "明民就是打光：把光打到人身上，人彼此就看得清长短了。", 5.0, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、灯挂在屋子正中：影子都落在脚下", 4.8, SEAL))
    gy = y + 62
    s.append(f'<rect x="96" y="{gy}" width="188" height="156" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 灯：一根绳吊在正中
    s.append(f'<line x1="190" y1="{gy}" x2="190" y2="{gy + 22}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M180,{gy + 32} L200,{gy + 32} L196,{gy + 22} L184,{gy + 22} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<polygon points="182,{gy + 42} 198,{gy + 42} 272,{gy + 142} 108,{gy + 142}" fill="#EADFC2" opacity="0.5" stroke="none"/>')
    s.append(f'<circle cx="190" cy="{gy + 38}" r="4.2" fill="{SEAL}" stroke="{SEAL}" stroke-width="0.8"/>')
    # 三个人，影子长短不一
    for (px, sl, dirn) in ((132, 24, -1), (190, 7, 1), (250, 34, 1)):
        s.append(f'<path d="M{px},{gy + 138} L{px + dirn * sl},{gy + 144} L{px + dirn * sl},{gy + 149} '
                 f'L{px},{gy + 142} Z" fill="#CFC3A8" stroke="none"/>')
        s.append(f'<circle cx="{px}" cy="{gy + 104}" r="5" fill="none" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<rect x="{px - 5}" y="{gy + 110}" width="10" height="16" rx="2" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{px - 3}" y1="{gy + 126}" x2="{px - 4}" y2="{gy + 138}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<line x1="{px + 3}" y1="{gy + 126}" x2="{px + 4}" y2="{gy + 138}" stroke="{INK}" stroke-width="1"/>')
    s.append(txt(190, gy + 172, "灯在当中：影子有长有短，谁都在看谁的影子", 4.6, SEAL, "middle"))

    s.append(txt(24, y + 250, "二、灯挪到门边：光只照路", 4.8, GREEN))
    gy2 = y + 260
    s.append(f'<rect x="96" y="{gy2}" width="188" height="118" fill="#FBF6EC" stroke="{LINE}" stroke-width="0.8"/>')
    # 门在左墙
    s.append(f'<line x1="104" y1="{gy2 + 90}" x2="104" y2="{gy2 + 20}" stroke="{INK}" stroke-width="2.4" opacity="0.6"/>')
    # 灯挂在门边
    s.append(f'<line x1="118" y1="{gy2 + 40}" x2="118" y2="{gy2 + 20}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<path d="M110,{gy2 + 20} L126,{gy2 + 20} L124,{gy2 + 10} L112,{gy2 + 10} Z" fill="#EFE6D4" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<circle cx="118" cy="{gy2 + 24}" r="3.4" fill="{GREEN}" stroke="{GREEN}" stroke-width="0.8"/>')
    # 路：一条横带
    s.append(f'<rect x="110" y="{gy2 + 84}" width="164" height="26" fill="#F0E7D5" stroke="none"/>')
    s.append(f'<line x1="110" y1="{gy2 + 84}" x2="274" y2="{gy2 + 84}" stroke="{LINE}" stroke-width="0.7"/>')
    s.append(f'<line x1="110" y1="{gy2 + 110}" x2="274" y2="{gy2 + 110}" stroke="{LINE}" stroke-width="0.7"/>')
    # 光落在路上的一段
    s.append(f'<ellipse cx="162" cy="{gy2 + 97}" rx="46" ry="13" fill="#EADFC2" opacity="0.9" stroke="none"/>')
    s.append(txt(250, gy2 + 100, "路", 4.4, "#6E6459", "middle"))
    s.append(txt(152, gy2 + 74, "照亮的是路", 4.4, GREEN, "middle"))
    s.append(txt(190, gy2 + 134, "灯靠门：照亮路，不照亮人——不吹灯，是把灯挪开", 4.6, GREEN, "middle"))

    a = gy2 + 154
    s.append(txt(24, a, "明民，是打光：光一打，位置就看得清；看得清，就生比较。", 4.8, INK))
    s.append(txt(24, a + 16, "这一照亮，给的是路还是靶子？老子问的是这一句。", 4.9, INK))
    s.append(txt(24, a + 34, "他说的不是吹灯，是不把灯挂到人头顶上。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "明是打光，不是自己亮；", 5.6, INK, "middle"))
    s.append(txt(190, c + 36, "灯照路，不照人。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch65a"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十五章 · 一只猴 ============
def ch65b_yi_zhi_hou():
    W, H = 380, 690
    body, y = head(W, H, "愚从心从禺：禺是猴，猴不蠢，是停不住",
                   "第 六 十 五 章 · 愚", "一只猴", "民之难治，以其智多。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「愚」，《说文》「戆也」，从心从禺——禺是猴，兽之愚者。", 5.2, INK, "middle"))
    s.append(txt(190, y + 26, "猴不蠢，猴是躁：一刻不停，见什么抓什么。愚，是心跟着猴跑。", 4.8, "#6E6459", "middle"))

    def monkey(cx, cy, col, k=1.0):
        o = []
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{9 * k}" ry="{12 * k}" fill="#EFE6D4" stroke="{col}" stroke-width="1"/>')
        o.append(f'<circle cx="{cx}" cy="{cy - 18 * k}" r="{7 * k}" fill="#EFE6D4" stroke="{col}" stroke-width="1"/>')
        o.append(f'<circle cx="{cx - 6.6 * k}" cy="{cy - 22 * k}" r="{2.4 * k}" fill="none" stroke="{col}" stroke-width="0.9"/>')
        o.append(f'<circle cx="{cx + 6.6 * k}" cy="{cy - 22 * k}" r="{2.4 * k}" fill="none" stroke="{col}" stroke-width="0.9"/>')
        o.append(f'<circle cx="{cx - 1.6 * k}" cy="{cy - 19 * k}" r="{0.8 * k}" fill="{col}"/>')
        o.append(f'<circle cx="{cx + 1.6 * k}" cy="{cy - 19 * k}" r="{0.8 * k}" fill="{col}"/>')
        o.append(f'<line x1="{cx}" y1="{cy - 15 * k}" x2="{cx}" y2="{cy - 12 * k}" stroke="{col}" stroke-width="0.7"/>')
        o.append(f'<path d="M{cx - 8 * k},{cy + 4 * k} C{cx - 18 * k},{cy + 8 * k} {cx - 20 * k},{cy - 4 * k} {cx - 13 * k},{cy - 9 * k}" '
                 f'fill="none" stroke="{col}" stroke-width="1"/>')
        o.append(f'<path d="M{cx + 8 * k},{cy + 4 * k} C{cx + 18 * k},{cy + 9 * k} {cx + 23 * k},{cy + 1 * k} {cx + 18 * k},{cy - 7 * k}" '
                 f'fill="none" stroke="{col}" stroke-width="1"/>')
        return o

    def person(cx, gy, col):
        o = []
        o.append(f'<line x1="{cx - 6}" y1="{gy - 16}" x2="{cx - 9}" y2="{gy}" stroke="{col}" stroke-width="1.2"/>')
        o.append(f'<line x1="{cx + 6}" y1="{gy - 16}" x2="{cx + 9}" y2="{gy}" stroke="{col}" stroke-width="1.2"/>')
        o.append(f'<rect x="{cx - 12}" y="{gy - 46}" width="24" height="30" rx="3" fill="#EFE6D4" stroke="{col}" stroke-width="1.2"/>')
        o.append(f'<circle cx="{cx}" cy="{gy - 56}" r="8" fill="none" stroke="{col}" stroke-width="1.2"/>')
        return o

    s.append(txt(24, y + 48, "一、猴在肩上：心跟着猴跑", 4.8, SEAL))
    gy = y + 180
    s += person(182, gy, INK)
    s += monkey(206, gy - 62, SEAL, 0.78)
    s.append(f'<path d="M170,{gy - 44} C160,{gy - 54} 152,{gy - 66} 156,{gy - 74}" fill="none" stroke="{SEAL}" stroke-width="1" stroke-dasharray="3 2"/>')
    s.append(f'<circle cx="158" cy="{gy - 80}" r="6" fill="none" stroke="{SEAL}" stroke-width="1"/>')
    s.append(txt(158, gy - 94, "心", 4.4, SEAL, "middle"))
    s.append(txt(216, gy - 30, "猴", 4.4, SEAL, "middle"))
    s.append(txt(190, gy + 24, "心跟着猴跑：一刻不停，见什么抓什么", 4.6, SEAL, "middle"))

    s.append(txt(24, gy + 52, "二、把猴放下来：它蹲在地上，心才落回身上", 4.8, GREEN))
    gy2 = gy + 120
    s += person(182, gy2, INK)
    s.append(f'<circle cx="182" cy="{gy2 - 34}" r="5.5" fill="none" stroke="{GREEN}" stroke-width="1.2"/>')
    s.append(txt(196, gy2 - 36, "心落回身上", 4.4, GREEN))
    s += monkey(240, gy2 - 16, SEAL, 0.66)
    s.append(f'<line x1="240" y1="{gy2 - 2}" x2="240" y2="{gy2}" stroke="{SEAL}" stroke-width="0.8" stroke-dasharray="2 2"/>')
    s.append(txt(240, gy2 + 16, "猴放着，不打它", 4.4, SEAL, "middle"))

    a = gy2 + 40
    s.append(txt(24, a, "愚不是蠢：禺是猴，心跟着猴跑，才叫愚。", 4.8, INK))
    s.append(txt(24, a + 16, "民之难治，以其智多——多的不是本事，是这份停不住。", 4.9, INK))
    s.append(txt(24, a + 34, "收心，是把猴从肩上放下来；放下来它还在，只是不再拽着心跑。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "愚从心从禺：禺是猴，猴不蠢，是停不住；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "心跟着猴跑，才是那个愚字。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch65b"))
    s.append('</svg>')
    return "\n".join(s)


# ============ 第六十五章 · 一道墨线 ============
def ch65c_yi_dao_mo_xian():
    W, H = 380, 586
    body, y = head(W, H, "稽式是木工弹的那道线：它不评价木头，只让木头看见自己",
                   "第 六 十 五 章 · 稽", "一道墨线", "知此两者亦稽式。", H)
    s = [body]

    s.append(box(20, y + 2, 340, 30, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, y + 14, "「稽」，《说文》「留止也」，又有「考」义：稽式，是拿来校量的那个样式。", 5.0, INK, "middle"))
    s.append(txt(190, y + 26, "木工弹墨线：线一响，歪的木头自己就显出来了。", 4.9, "#6E6459", "middle"))

    s.append(txt(24, y + 48, "一、木上一道线，木头自己看见自己", 4.8, SEAL))
    gy = y + 150
    # 木板：上缘歪，下面厚
    s.append(f'<path d="M120,{gy} L160,{gy - 6} L200,{gy + 4} L240,{gy - 6} L252,{gy} L252,{gy + 32} L120,{gy + 32} Z" '
             f'fill="#EFE6D4" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<line x1="116" y1="{gy + 32}" x2="256" y2="{gy + 32}" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(3):
        yy = gy + 12 + k * 7
        s.append(f'<line x1="128" y1="{yy}" x2="244" y2="{yy}" stroke="{LINE}" stroke-width="0.5"/>')
    # 弹出来的那道直墨线
    s.append(f'<line x1="106" y1="{gy - 22}" x2="266" y2="{gy - 22}" stroke="{INK}" stroke-width="1.6"/>')
    # 两端的墨斗
    s.append(f'<rect x="98" y="{gy - 28}" width="14" height="12" fill="#F6EFE0" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<rect x="260" y="{gy - 28}" width="14" height="12" fill="#F6EFE0" stroke="{INK}" stroke-width="1"/>')
    # 线到木之间的距离，用虚线标出两处
    s.append(f'<line x1="160" y1="{gy - 22}" x2="160" y2="{gy - 6}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="2 2"/>')
    s.append(f'<line x1="240" y1="{gy - 22}" x2="240" y2="{gy - 6}" stroke="{SEAL}" stroke-width="0.9" stroke-dasharray="2 2"/>')
    s.append(txt(186, gy - 34, "线是直的，木是歪的——差多少，一眼看见", 4.6, SEAL, "middle"))
    s.append(txt(186, gy + 50, "线不评价这块木头，它只把差处显出来", 4.6, "#6E6459", "middle"))

    a = gy + 72
    s.append(txt(24, a, "稽式不是尺子上的刻度，是弹出来的那一道线：留在木上，木头自己就看见了。", 4.8, INK))
    s.append(txt(24, a + 16, "知此两者亦稽式——「以智治国」与「不以智治国」，就是这一道线。", 4.9, INK))
    s.append(txt(24, a + 34, "常知稽式，是谓玄德：常拿它量自己，不拿它去量别人。", 5.0, GREEN))

    c = a + 52
    s.append(f'<line x1="24" y1="{c}" x2="338" y2="{c}" stroke="{LINE}" stroke-width="0.6"/>')
    s.append(box(20, c + 8, 340, 40, fill="#F2EADA", stroke="#C9B79A"))
    s.append(txt(190, c + 24, "稽式是木工弹的那道线：它不评价，只显出来；", 5.4, INK, "middle"))
    s.append(txt(190, c + 36, "常知稽式，是谓玄德。", 5.2, GREEN, "middle"))
    s.append(gold(c + 62, "ch65c"))
    s.append('</svg>')
    return "\n".join(s)



FIGS = {
    "ch01-wu-you": ("第一章", "无有同出", ch01_wu_you),
    "ch01-zhi-yue": ("第一章", "指月三境", ch01_zhi_yue),
    "ch01-miao-jiao": ("第一章", "观妙观徼", ch01_miao_jiao),
    "ch02b-yi-gen-biao-gan": ("第二章", "一根标杆", ch02b_yi_gen_biao_gan),
    "ch02c-liang-zhi-guan": ("第二章", "两只管子", ch02c_liang_zhi_guan),
    "ch03b-yi-kuai-jia-pai": ("第三章", "一块价牌", ch03b_yi_kuai_jia_pai),
    "ch03c-yi-ke-shu": ("第三章", "一棵树", ch03c_yi_ke_shu),
    "ch04b-yi-zhi-li-qi": ("第四章", "一只礼器", ch04b_yi_zhi_li_qi),
    "ch04c-si-bu": ("第四章", "四步", ch04c_si_bu),
    "ch02-liu-zu": ("第二章", "六组对偶", ch02_liu_zu),
    "ch11-li-yong": ("第十一章", "利与用", ch11_li_yong),
    "ch11b-san-shi-fu-yi-gu": ("第十一章", "三十辐共一毂", ch11b_san_shi_fu_yi_gu),
    "ch11c-zao-hu-you": ("第十一章", "凿户牖", ch11c_zao_hu_you),
    "ch12b-tian-men-wu-lu": ("第十二章", "五路进门", ch12b_tian_men_wu_lu),
    "ch12c-wei-fu-bu-wei-mu": ("第十二章", "为腹不为目", ch12c_wei_fu_bu_wei_mu),
    "ch13b-ding-zai-bi-shang": ("第十三章", "一枚钉", ch13b_ding_zai_bi_shang),
    "ch13c-bao-yu-tuo": ("第十三章", "抱与托", ch13c_bao_yu_tuo),
    "ch14b-san-zhi-tan-zhen": ("第十四章", "三支探针", ch14b_san_zhi_tan_zhen),
    "ch14c-gu-sheng-yu-jin": ("第十四章", "一根准绳", ch14c_gu_sheng_yu_jin),
    "ch15b-dong-chuan": ("第十五章", "冬涉川", ch15b_dong_chuan),
    "ch15c-bu-yu-ying": ("第十五章", "旧罐", ch15c_bu_yu_ying),
    "ch16b-yi-gang-shui": ("第十六章", "一缸浊水", ch16b_yi_gang_shui),
    "ch16c-luo-ye-gui-gen": ("第十六章", "落叶归根", ch16c_luo_ye_gui_gen),
    "ch17b-si-shan-men": ("第十七章", "四扇门", ch17b_si_shan_men),
    "ch17c-gong-cheng": ("第十七章", "功成之后", ch17c_gong_cheng),
    "ch18b-yi-kuai-bu": ("第十八章", "一块补丁", ch18b_yi_kuai_bu),
    "ch18c-san-kuai-bu-ding": ("第十八章", "三处破", ch18c_san_kuai_bu_ding),
    "ch19b-yi-ju-qi-qi": ("第十九章", "一具漆器", ch19b_yi_ju_qi_qi),
    "ch19c-ban-chu-qu": ("第十九章", "搬出去", ch19c_ban_chu_qu),
    "ch20b-shi-ji-yu-jiao-luo": ("第二十章", "市集与角落", ch20b_shi_ji_yu_jiao_luo),
    "ch20c-kong-dai": ("第二十章", "一只空袋", ch20c_kong_dai),
    "ch21b-kong-de-zhi-rong": ("第二十一章", "一枚带孔的璧", ch21b_kong_de_zhi_rong),
    "ch21c-men-nei-dian-shu": ("第二十一章", "门内点数", ch21c_men_nei_dian_shu),
    "ch22b-qu-mu-cao": ("第二十二章", "一只曲木槽", ch22b_qu_mu_cao),
    "ch22c-bao-yi": ("第二十二章", "抱一与五牌", ch22c_bao_yi),
    "ch23b-zhou-yu": ("第二十三章", "一场骤雨", ch23b_zhou_yu),
    "ch23c-yan-ru-shui": ("第二十三章", "一撮盐", ch23c_yan_ru_shui),
    "ch24-qi-zhe-bu-li": ("第二十四章", "企者不立", ch24_qi_zhe_bu_li),
    "ch23-xi-yan-zi-ran": ("第二十三章", "希言自然", ch23_xi_yan_zi_ran),
    "ch22-qu-ze-quan": ("第二十二章", "曲则全", ch22_qu_ze_quan),
    "ch26-zhong-wei-qing-gen": ("第二十六章", "重为轻根", ch26_zhong_wei_qing_gen),
    "ch27-shan-xing-wu-zhe-ji": ("第二十七章", "善行无辙迹", ch27_shan_xing_wu_zhe_ji),
    "ch25-dao-fa": ("第二十五章", "道法自然", ch25_dao_fa),
    # ── 已撤旧稿（用户否决／被三图取代）：ch38-wu-ji（滑落版）、ch51-sheng-bu-you、
    #    ch67-san-bao、ch77-zhang-gong、ch81-bu-ji。件存 book/义理图/old/，仅供追溯；
    #    全量重生成会把它们写回 book/义理图/，务必删净后再嵌阅读版。
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
    "ch49b-yi-tiao-qu": ("第四十九章", "一条渠", ch49b_yi_tiao_qu),
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
    "ch57a-yi-zhi-jiao": ("第五十七章", "一只脚", ch57a_yi_zhi_jiao),
    "ch57b-yi-shuang-shou-tao": ("第五十七章", "一双手套", ch57b_yi_shuang_shou_tao),
    "ch57c-yi-kuai-hua-pai": ("第五十七章", "一块木牌", ch57c_yi_kuai_hua_pai),
    "ch58a-yi-shan-men": ("第五十八章", "一扇门", ch58a_yi_shan_men),
    "ch58b-yi-zhang-zhe-zhi": ("第五十八章", "一张折纸", ch58b_yi_zhang_zhe_zhi),
    "ch58c-liang-tiao-chuan": ("第五十八章", "两条船", ch58c_liang_tiao_chuan),
    "ch59a-yi-kou-dun": ("第五十九章", "一口囤", ch59a_yi_kou_dun),
    "ch59b-yi-gen-bian-dan": ("第五十九章", "一根扁担", ch59b_yi_gen_bian_dan),
    "ch59c-yi-ke-shu": ("第五十九章", "一棵树", ch59c_yi_ke_shu),
    "ch60a-yi-kou-guo": ("第六十章", "一口锅", ch60a_yi_kou_guo),
    "ch60b-yi-pian-cao": ("第六十章", "一片草", ch60b_yi_pian_cao),
    "ch60c-liang-tiao-tui": ("第六十章", "两条腿", ch60c_liang_tiao_tui),
    "ch61a-yi-tiao-he": ("第六十一章", "一条河", ch61a_yi_tiao_he),
    "ch61b-yi-zhi-mu-chu": ("第六十一章", "一只母畜", ch61b_yi_zhi_mu_chu),
    "ch61c-yi-zhi-shou": ("第六十一章", "一只手", ch61c_yi_zhi_shou),
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
    "ch05b-yi-zhi-chu-gou": ("第五章", "一只刍狗", ch05b_yi_zhi_chu_gou),
    "ch05c-yi-ba-suo": ("第五章", "一把锁", ch05c_yi_ba_suo),
    "ch05-tuo-yue": ("第五章", "中不是点，是枢", ch05_tuo_yue),
    "ch06b-yi-kou-gu": ("第六章", "一口谷", ch06b_yi_kou_gu),
    "ch06c-yi-shan-men-zhou": ("第六章", "一扇门轴", ch06c_yi_shan_men_zhou),
    "ch06-gu-shen": ("第六章", "谷神不死", ch06_gu_shen),
    "ch07b-yi-ge-huan": ("第七章", "一个环", ch07b_yi_ge_huan),
    "ch07c-yi-shan-zhai-men": ("第七章", "一扇窄门", ch07c_yi_shan_zhai_men),
    "ch07-bu-zi-sheng": ("第七章", "不自生", ch07_bu_zi_sheng),
    "ch08-shang-shan": ("第八章", "上善若水", ch08_shang_shan),
    "ch08b-yi-chu-di-chu": ("第八章", "一处低处", ch08b_yi_chu_di_chu),
    "ch08c-qi-jie-tong-guan": ("第八章", "一根七节管", ch08c_qi_jie_tong_guan),
    "ch09-ying-man": ("第九章", "持而盈之", ch09_ying_man),
    "ch09b-yi-zhi-qi-qi": ("第九章", "一只欹器", ch09b_yi_zhi_qi_qi),
    "ch09c-zan-yu-song": ("第九章", "攥与松", ch09c_zan_yu_song),
    "ch10-bao-yi": ("第十章", "载营魄抱一", ch10_bao_yi),
    "ch10b-liang-lun-yi-zhou": ("第十章", "两轮一轴", ch10b_liang_lun_yi_zhou),
    "ch10c-yi-jian-jie-zhu-de-wu": ("第十章", "一间借住的屋", ch10c_yi_jian_jie_zhu_de_wu),
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
    "ch62a-yi-ge-qiang-jiao": ("第六十二章", "一个墙角", ch62a_yi_ge_qiang_jiao),
    "ch62b-yi-fu-bei-dai": ("第六十二章", "一副背带", ch62b_yi_fu_bei_dai),
    "ch62c-yi-ge-zuo-zi": ("第六十二章", "一个坐姿", ch62c_yi_ge_zuo_zi),
    "ch63a-yi-zhi-bi": ("第六十三章", "一支笔", ch63a_yi_zhi_bi),
    "ch63b-yi-gen-si": ("第六十三章", "一根丝", ch63b_yi_gen_si),
    "ch63c-yi-tiao-wei-ba": ("第六十三章", "一条尾巴", ch63c_yi_tiao_wei_ba),
    "ch64a-yi-pian-gui-jia": ("第六十四章", "一片龟甲", ch64a_yi_pian_gui_jia),
    "ch64b-yi-kuang-tu": ("第六十四章", "一筐土", ch64b_yi_kuang_tu),
    "ch64c-yi-kuai-gu-tou": ("第六十四章", "一块骨头", ch64c_yi_kuai_gu_tou),
    "ch65a-yi-zhan-deng": ("第六十五章", "一盏灯", ch65a_yi_zhan_deng),
    "ch65b-yi-zhi-hou": ("第六十五章", "一只猴", ch65b_yi_zhi_hou),
    "ch65c-yi-dao-mo-xian": ("第六十五章", "一道墨线", ch65c_yi_dao_mo_xian),
    "ch66a-yi-tiao-shui-lu": ("第六十六章", "一条水路", ch66a_yi_tiao_shui_lu),
    "ch66b-yi-zhi-kou-dai": ("第六十六章", "一只口袋", ch66b_yi_zhi_kou_dai),
    "ch66c-yi-kou-qi": ("第六十六章", "一口气", ch66c_yi_kou_qi),
    "ch67a-yi-cong-cao": ("第六十七章", "一丛草", ch67a_yi_cong_cao),
    "ch67b-yi-shu-sheng": ("第六十七章", "一束绳", ch67b_yi_shu_sheng),
    "ch67c-yi-quan-qiang": ("第六十七章", "一圈墙", ch67c_yi_quan_qiang),
    "ch68a-yi-zhi-jiao": ("第六十八章", "一只脚", ch68a_yi_zhi_jiao),
    "ch68b-yi-dao-feng": ("第六十八章", "一道缝", ch68b_yi_dao_feng),
    "ch68c-yi-gen-jin": ("第六十八章", "一根筋", ch68c_yi_gen_jin),
    "ch69a-yi-zhan-deng": ("第六十九章", "一盏灯", ch69a_yi_zhan_deng),
    "ch69b-yi-shuang-jiao": ("第六十九章", "一双抬高的脚", ch69b_yi_shuang_jiao),
    "ch69c-yi-shan-men": ("第六十九章", "一扇门", ch69c_yi_shan_men),
    "ch70a-yi-dao-ke-xian": ("第七十章", "一道刻线", ch70a_yi_dao_ke_xian),
    "ch70b-yi-jian-ma-yi": ("第七十章", "一件麻衣", ch70b_yi_jian_ma_yi),
    "ch70c-yi-kuai-hui-yu": ("第七十章", "一块揣着的玉", ch70c_yi_kuai_hui_yu),
    "ch71a-yi-zhi-jian": ("第七十一章", "一支箭", ch71a_yi_zhi_jian),
    "ch71b-yi-zhang-ba": ("第七十一章", "一张靶", ch71b_yi_zhang_ba),
    "ch71c-yi-bao-ba": ("第七十一章", "一个报靶的人", ch71c_yi_bao_ba),
    "ch72a-yi-wei-po-po": ("第七十二章", "一位坐堂的婆婆", ch72a_yi_wei_po_po),
    "ch72b-yi-wo-gou": ("第七十二章", "一窝挤着的狗", ch72b_yi_wo_gou),
    "ch72c-yi-gan-cheng": ("第七十二章", "一杆秤", ch72c_yi_gan_cheng),
    "ch73a-yi-gu-qi": ("第七十三章", "一股气", ch73a_yi_gu_qi),
    "ch73b-yi-gen-dai-zi": ("第七十三章", "一根松带子", ch73b_yi_gen_dai_zi),
    "ch73c-yi-zhang-wang": ("第七十三章", "一张通着的网", ch73c_yi_zhang_wang),
    "ch74a-yi-ge-fan-zi": ("第七十四章", "一个翻过来的字", ch74a_yi_ge_fan_zi),
    "ch74b-yi-ba-fu": ("第七十四章", "一把斧", ch74b_yi_ba_fu),
    "ch74c-yi-zhi-shou": ("第七十四章", "一只被斫的手", ch74c_yi_zhi_shou),
    "ch75a-yi-zhi-kong-wan": ("第七十五章", "一只空碗", ch75a_yi_zhi_kong_wan),
    "ch75b-yi-tiao-he": ("第七十五章", "一条河", ch75b_yi_tiao_he),
    "ch75c-yi-gan-cheng": ("第七十五章", "一杆秤", ch75c_yi_gan_cheng),
    "ch76a-yi-gen-zhi-tiao": ("第七十六章", "一根枝条", ch76a_yi_gen_zhi_tiao),
    "ch76b-yi-zhang-gong": ("第七十六章", "一张弓", ch76b_yi_zhang_gong),
    "ch76c-yi-ba-fu": ("第七十六章", "一把斧", ch76c_yi_ba_fu),
    "ch77a-yi-zhang-xian": ("第七十七章", "一张弦", ch77a_yi_zhang_xian),
    "ch77b-yi-jian-po-yi": ("第七十七章", "一件破衣", ch77b_yi_jian_po_yi),
    "ch77c-liang-zhi-shou": ("第七十七章", "两只捧起的手", ch77c_liang_zhi_shou),
    "ch78a-yi-zhi-qi": ("第七十八章", "一只器", ch78a_yi_zhi_qi),
    "ch78b-yi-peng-tu": ("第七十八章", "一捧土", ch78b_yi_peng_tu),
    "ch78c-yi-kuai-pai-wei": ("第七十八章", "一块牌位", ch78c_yi_kuai_pai_wei),
    "ch79a-ban-pian-mu": ("第七十九章", "半片木", ch79a_ban_pian_mu),
    "ch79b-yi-zhang-zhang": ("第七十九章", "一张账", ch79b_yi_zhang_zhang),
    "ch79c-yi-gan-cheng": ("第七十九章", "一杆秤", ch79c_yi_gan_cheng),
    "ch80a-yi-gen-sheng": ("第八十章", "一根打了结的绳", ch80a_yi_gen_sheng),
    "ch80b-yi-tiao-chuan": ("第八十章", "一条停在岸上的船", ch80b_yi_tiao_chuan),
    "ch80c-yi-shan-men": ("第八十章", "一扇开着的门", ch80c_yi_shan_men),
    "ch81a-yi-kou-cang": ("第八十一章", "一口仓", ch81a_yi_kou_cang),
    "ch81b-yi-yan-quan": ("第八十一章", "一眼泉", ch81b_yi_yan_quan),
    "ch81c-yi-ba-dao": ("第八十一章", "一把刀", ch81c_yi_ba_dao),
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
