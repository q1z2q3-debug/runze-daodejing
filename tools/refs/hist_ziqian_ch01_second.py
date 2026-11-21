# 用法：在仓库根执行  python3 tools/refs/hist_ziqian_ch01_second.py
import cairosvg
INK,SEAL,GREEN,LINE,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#DCCBB0","#E6D8C2","#F8F3E6"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
RED="#B5462F"; BLUE="#2E7C8F"
W,H=760,530
def frame(extra_title=True):
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="子虔版观妙图仿画" font-family="{SERIF}">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
       f'<text x="20" y="24" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">子 虔 版 原 图 · 仿 画</text>',
       f'<text x="20" y="50" font-size="16" fill="{INK}">复杂性—精确度：两条曲线，一张太极</text>',
       f'<text x="20" y="70" font-size="10" fill="#6E6459">横轴：复杂性（小→大）；纵轴：精确度（低→高）。原图见《道德经解（子虔版）》第 23 页。</text>']
    return s
def axes(s):
    ax,ay=110,432
    s.append(f'<path d="M{ax},{ay} L{ax},150" stroke="{INK}" stroke-width="1.1"/><path d="M{ax-5},160 L{ax},146 L{ax+5},160" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M{ax},{ay} L700,{ay}" stroke="{INK}" stroke-width="1.1"/><path d="M690,{ay-5} L704,{ay} L690,{ay+5}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<text x="86" y="300" font-size="10.5" fill="{INK}" transform="rotate(-90 86 300)">精 确 度</text>')
    s.append(f'<text x="596" y="454" font-size="10.5" fill="{INK}" letter-spacing="1">复 杂 性</text>')
def curves(s):
    s.append(f'<path d="M150,152 C 260,214 340,300 470,362 C 550,396 630,406 690,408" fill="none" stroke="{RED}" stroke-width="1.9"/>')
    s.append(f'<path d="M150,428 C 270,398 390,326 470,278 C 560,224 640,186 700,150" fill="none" stroke="{BLUE}" stroke-width="1.9"/>')
    for x,y,t in ((168,154,"量子"),(256,216,"元素"),(330,274,"原子"),(386,306,"分子"),(448,354,"物质")):
        s.append(f'<text x="{x}" y="{y}" font-size="9.6" fill="{INK}">{t}</text>')
    for x,y,t in ((492,320,"生物大分子"),(552,270,"生命"),(614,224,"超智能体"),(666,186,"生态"),(700,160,"宇宙")):
        s.append(f'<text x="{x}" y="{y}" font-size="9.6" fill="{INK}">{t}</text>')
def top_bottom(s):
    s.append(f'<text x="150" y="122" font-size="10.5" fill="{RED}">恒 有 欲</text>')
    s.append(f'<text x="662" y="122" font-size="10.5" fill="{BLUE}">恒 无 欲</text>')
    s.append(f'<text x="228" y="196" font-size="25" fill="{BLUE}">大 而 无 外</text>')
    s.append(f'<text x="418" y="196" font-size="25" fill="{RED}">小 而 无 内</text>')
    s.append(f'<circle cx="380" cy="188" r="15" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M380,173 A15,15 0 0 1 380,203 A7.5,7.5 0 0 1 380,188 A7.5,7.5 0 0 0 380,173" fill="{INK}"/>')
    s.append(f'<circle cx="380" cy="181" r="2.4" fill="{PAPER}" stroke="none"/>')
    s.append(f'<text x="380" y="484" font-size="17" fill="{INK}" text-anchor="middle" letter-spacing="4" font-family="{SANS}">I  KNOW  THAT  I  KNOW  NOTHING</text>')
    s.append(f'<text x="380" y="508" font-size="10.5" fill="{SEAL}" text-anchor="middle" letter-spacing="2">太玄之门：玄之又玄　众妙之门</text>')
    s.append('</svg>')

# 1) 纯仿画
s=frame(); axes(s); curves(s); top_bottom(s)
open('book/义理图/_refs/ziqian-ch01.svg','w',encoding='utf8').write("\n".join(s))
cairosvg.svg2png(url='book/义理图/_refs/ziqian-ch01.svg',write_to='book/义理图/_refs/ziqian-ch01.png',scale=2)
print('redraw ok')
