#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""义理图版式审计：画布与内容底 / 横向溢出 / 字号档 / 文字压线。
只读，不改图。用法： python3 tools/audit_layout.py [--list]
"""
import glob, os, re, sys
import xml.etree.ElementTree as ET

NS = '{http://www.w3.org/2000/svg}'
TIERS = [(3.5, 4.6, '注'), (4.7, 5.2, '正文'), (5.6, 6.0, '收口'),
         (7.4, 7.4, '标签'), (8.0, 8.4, '金句栏'), (10.5, 10.5, '副题'),
         (11, 11, '题签'), (21, 21, '主标'), (6.2, 40.0, '图形字')]


def tier_of(size):
    for lo, hi, name in TIERS:
        if lo - 0.001 <= size <= hi + 0.001:
            return name
    return None


def fnum(v, d=0.0):
    try:
        return float(v)
    except Exception:
        return d


def band_bottom(el):
    """元素底边 y（近似）"""
    tag = el.tag.replace(NS, '')
    a = el.attrib
    try:
        if tag == 'rect':
            return fnum(a.get('y')) + fnum(a.get('height'))
        if tag == 'circle':
            return fnum(a.get('cy')) + fnum(a.get('r'))
        if tag == 'ellipse':
            return fnum(a.get('cy')) + fnum(a.get('ry'))
        if tag == 'line':
            return max(fnum(a.get('y1')), fnum(a.get('y2')))
        if tag == 'polygon' or tag == 'polyline':
            pts = re.findall(r'-?\d+(?:\.\d+)?', a.get('points', ''))
            ys = [float(x) for i, x in enumerate(pts) if i % 2 == 1]
            return max(ys) if ys else None
        if tag == 'path':
            d = a.get('d', '')
            ys = []
            for m in re.finditer(r'[-+]?\d*\.?\d+', d):
                ys.append(float(m.group()))
            # 成对取 y：粗略
            return max(ys[1::2]) if len(ys) > 1 else None
    except Exception:
        return None
    return None


def text_geom(el):
    a = el.attrib
    y = fnum(a.get('y'))
    size = fnum(a.get('font-size'), 5.2)
    anchor = a.get('text-anchor', 'start')
    txt = ''.join(el.itertext())
    w = 0.0
    for ch in txt:
        w += size if ord(ch) > 0x2E7F else size * 0.55
    x = fnum(a.get('x'))
    if anchor == 'middle':
        x0, x1 = x - w / 2, x + w / 2
    elif anchor == 'end':
        x0, x1 = x - w, x
    else:
        x0, x1 = x, x + w
    return dict(x0=x0, x1=x1, y=y, size=size, txt=txt, anchor=anchor)


def audit(path):
    r = dict(name=os.path.basename(path)[:-4], issues=[])
    try:
        tree = ET.parse(path)
    except Exception as e:
        r['issues'].append(('parse', str(e)[:50]))
        return r
    root = tree.getroot()
    vb = [fnum(v) for v in re.split(r'[ ,]+', root.attrib.get('viewBox', '').strip())]
    W = vb[2] if len(vb) == 4 else 380
    H = vb[3] if len(vb) == 4 else 0
    if len(vb) != 4 or H <= 0:
        r['issues'].append(('viewBox', root.attrib.get('viewBox', '')))
        return r

    texts, bottoms = [], []
    for el in root.iter():
        tag = el.tag.replace(NS, '')
        if tag == 'text':
            g = text_geom(el)
            texts.append(g)
            bottoms.append(g['y'] + g['size'] * 0.25)
        elif tag in ('rect', 'circle', 'ellipse', 'line', 'path', 'polygon', 'polyline'):
            b = band_bottom(el)
            if b is not None:
                bottoms.append(b)

    text_bottoms = [g['y'] + g['size'] * 0.25 for g in texts]
    maxy = max(bottoms) if bottoms else 0
    tmaxy = max(text_bottoms) if text_bottoms else 0
    # 1 底部裁切：内容越过画布
    if maxy > H:
        r['issues'].append(('cut_bottom', f'内容底 {maxy:.0f} > 画布 {H:.0f}，越 {maxy-H:.0f}px'))
    if tmaxy > H:
        r['issues'].append(('cut_text', f'文字底 {tmaxy:.0f} > 画布 {H:.0f}，越 {tmaxy-H:.0f}px'))
    elif tmaxy > H - 4:
        r['issues'].append(('tight_text', f'文字底 {tmaxy:.0f} / 画布 {H:.0f}，余 {H-tmaxy:.0f}px'))

    # 2 横向溢出
    for g in texts:
        if g['x1'] > W - 6:
            r['issues'].append(('over_right', f'右溢 {g["x1"]-W:+.0f}px 「{g["txt"][:14]}」'))
        if g['x0'] < 6:
            r['issues'].append(('over_left', f'左溢 {6-g["x0"]:.0f}px 「{g["txt"][:14]}」'))

    # 3 字号档
    gaps = {}
    for g in texts:
        if not g['txt'].strip():
            continue
        if tier_of(g['size']) is None:
            gaps.setdefault(round(g['size'], 1), 0)
            gaps[round(g['size'], 1)] += 1
    if gaps:
        r['issues'].append(('font_gap', '空档字号 ' + '、'.join(f'{k}({v})' for k, v in sorted(gaps.items()))))

    # 4 文字压线：同一条水平带上两段文字横向重叠且 y 近
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i], texts[j]
            if abs(a['y'] - b['y']) < (a['size'] + b['size']) / 2 * 0.8:
                if a['x0'] < b['x1'] - 2 and b['x0'] < a['x1'] - 2:
                    r['issues'].append(('text_clash', f'「{a["txt"][:10]}」×「{b["txt"][:10]}」'))
                    break
    return r


def main():
    files = sorted(glob.glob('book/义理图/*.svg'))
    res = [audit(f) for f in files]
    kinds = {}
    for r in res:
        for k, _ in r['issues']:
            kinds.setdefault(k, []).append(r['name'])
    print(f'审计 {len(files)} 幅\n')
    order = ['parse', 'viewBox', 'cut_bottom', 'tight_bottom', 'over_right',
             'over_left', 'text_clash', 'font_gap']
    for k in order:
        if k in kinds:
            print(f'{k:12s} {len(kinds[k]):3d} 幅  {", ".join(kinds[k][:8])}{" …" if len(kinds[k])>8 else ""}')
    clean = [r['name'] for r in res if not r['issues']]
    print(f'\n无问题 {len(clean)} 幅')
    if '--list' in sys.argv:
        print('\n明细：')
        for r in res:
            if r['issues']:
                print(r['name'])
                for k, m in r['issues'][:6]:
                    print('   ', k, m)


if __name__ == '__main__':
    main()
