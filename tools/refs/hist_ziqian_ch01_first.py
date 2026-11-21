# 用法：在仓库根执行  python3 tools/refs/hist_ziqian_ch01_first.py
import cairosvg
INK,SEAL,GREEN,LINE,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#DCCBB0","#E6D8C2","#F8F3E6"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
RED="#B5462F"; BLUE="#2E7C8F"
W,H=760,440
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="子虔版观妙图仿画：复杂性—精确度双曲线" font-family="{SERIF}">',
   f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
   f'<text x="20" y="26" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">子 虔 版 原 图 · 仿 画</text>',
   f'<text x="20" y="52" font-size="16" fill="{INK}">复杂性—精确度：两条曲线，一张太极</text>',
   f'<text x="20" y="72" font-size="10.5" fill="#6E6459">横轴：复杂性（小→大）；纵轴：精确度（低→高）。原图为第 23 页「太和思维」。</text>']
# 轴
ax, ay = 96, 356
s.append(f'<path d="M{ax},{ay} L{ax},60" stroke="{INK}" stroke-width="1.2"/><path d="M{ax-5},70 L{ax},56 L{ax+5},70" fill="none" stroke="{INK}" stroke-width="1.2"/>')
s.append(f'<path d="M{ax},{ay} L{700},{ay}" stroke="{INK}" stroke-width="1.2"/><path d="M690,{ay-5} L702,{ay} L690,{ay+5}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
s.append(f'<text x="74" y="200" font-size="10.5" fill="{INK}" transform="rotate(-90 74 200)">精 确 度</text>')
s.append(f'<text x="600" y="378" font-size="10.5" fill="{INK}" letter-spacing="1">复 杂 性</text>')
# 两条曲线
s.append(f'<path d="M150,74 C 250,140 330,240 470,300 C 540,326 620,336 690,340" fill="none" stroke="{RED}" stroke-width="2"/>')
s.append(f'<path d="M150,340 C 260,318 380,250 470,200 C 560,150 640,110 700,66" fill="none" stroke="{BLUE}" stroke-width="2"/>')
# 左段层级（贴红线）
for x,y,t in ((168,96,"量子"),(258,166,"元素"),(330,220,"原子"),(398,258,"分子"),(452,282,"物质")):
    s.append(f'<text x="{x}" y="{y}" font-size="10" fill="{INK}">{t}</text>')
# 右段层级（贴蓝线）
for x,y,t in ((500,262,"生物大分子"),(548,222,"生命"),(618,178,"超智能体"),(660,138,"生态"),(706,86,"宇宙")):
    s.append(f'<text x="{x}" y="{y}" font-size="10" fill="{INK}">{t}</text>')
# 顶部两端
s.append(f'<text x="168" y="46" font-size="11" fill="{RED}">恒 有 欲</text>')
s.append(f'<text x="660" y="46" font-size="11" fill="{BLUE}">恒 无 欲</text>')
# 中央八字 + 太极
s.append(f'<text x="238" y="126" font-size="26" fill="{BLUE}">大 而 无 外</text>')
s.append(f'<circle cx="380" cy="118" r="14" fill="none" stroke="{INK}" stroke-width="1"/>')
s.append(f'<path d="M380,104 A7,7 0 0 1 380,118 A7,7 0 0 1 380,132" fill="none" stroke="{INK}" stroke-width="0.9"/>')
s.append(f'<path d="M380,104 A7,7 0 0 0 380,118 A7,7 0 0 0 380,132" fill="{INK}" opacity="0.35"/>')
s.append(f'<text x="414" y="126" font-size="26" fill="{RED}">小 而 无 内</text>')
# 底部
s.append(f'<text x="380" y="398" font-size="18" fill="{INK}" text-anchor="middle" letter-spacing="4" font-family="{SANS}">I  KNOW  THAT  I  KNOW  NOTHING</text>')
s.append(f'<text x="380" y="422" font-size="11" fill="{SEAL}" text-anchor="middle" letter-spacing="2">太玄之门：玄之又玄　众妙之门</text>')
s.append('</svg>')
open('book/义理图/_refs/ziqian-ch01.svg','w',encoding='utf8').write("\n".join(s))
cairosvg.svg2png(url='book/义理图/_refs/ziqian-ch01.svg',write_to='book/义理图/_refs/ziqian-ch01.png',scale=2)
print('ok')
