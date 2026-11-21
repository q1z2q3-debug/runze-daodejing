# 用法：在仓库根执行  python3 tools/refs/refs_ziqian_ladder.py
import cairosvg
INK,SEAL,GREEN,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#E6D8C2","#F8F3E6"
RED="#B5462F"; BLUE="#2E7C8F"; GREY="#8A7C69"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
W,H=1000,640
AX,AY=90,470
LV=["量子","元素","原子","无机小分子","有机大分子","蛋白质","细胞","组织","器官","五脏六腑","人体",
    "家庭","团体·企业","国家","文明","生态圈","地球","星系","宇宙"]
def x_of(i): return 90+i*(870/18)
CROSS=x_of(10)  # 人体
def build(visible=False):
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="从量子到宇宙的涌现阶梯，妙徼两曲线" font-family="{SERIF}">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
       f'<text x="24" y="26" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">子 虔 版 骨 架 · 补 全 涌 现 阶 梯</text>',
       f'<text x="24" y="54" font-size="17" fill="{INK}">从量子到宇宙：十九级涌现，两条曲线</text>',
       f'<text x="24" y="74" font-size="10" fill="#6E6459">横轴：复杂性（小→大）；纵轴：精确度（低→高）。交叉处落在「人体」——人恰在交会点。</text>']
    # 色面（先画，压在轴下）
    if visible:
        bands=[(3,7,BLUE,"须知仪器"),(8,14,RED,"肉眼与身体可及"),(15,18,GREY,"可见而不可及")]
        for a,b,c,lab in bands:
            x1,x2=x_of(a)-22,x_of(b)+22
            s.append(f'<rect x="{x1}" y="{150}" width="{x2-x1}" height="{AY-150}" fill="{c}" opacity="0.06"/>')
            s.append(f'<line x1="{x1}" y1="150" x2="{x1}" y2="{AY}" stroke="{c}" stroke-width="0.7" stroke-dasharray="5 4"/>')
            s.append(f'<line x1="{x2}" y1="150" x2="{x2}" y2="{AY}" stroke="{c}" stroke-width="0.7" stroke-dasharray="5 4"/>')
            s.append(f'<text x="{(x1+x2)/2}" y="168" font-size="9.6" fill="{c}" text-anchor="middle" letter-spacing="1">{lab}</text>')
    # 轴
    s.append(f'<path d="M{AX},{AY} L{AX},150" stroke="{INK}" stroke-width="1.1"/><path d="M{AX-5},161 L{AX},147 L{AX+5},161" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<path d="M{AX},{AY} L975,{AY}" stroke="{INK}" stroke-width="1.1"/><path d="M964,{AY-5} L978,{AY} L964,{AY+5}" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<text x="{AX-18}" y="300" font-size="10.5" fill="{INK}" transform="rotate(-90 {AX-18} 300)" text-anchor="middle">精 确 度</text>')
    s.append(f'<text x="975" y="{AY-26}" font-size="10.5" fill="{INK}" text-anchor="end" letter-spacing="1">复 杂 性</text>')
    # 刻度与标签（交错两行）
    for i,name in enumerate(LV):
        x=x_of(i)
        s.append(f'<line x1="{x}" y1="{AY-4}" x2="{x}" y2="{AY+4}" stroke="#C9B79A" stroke-width="0.5"/>')
        ty = AY+26 if i%2==0 else AY+44
        s.append(f'<line x1="{x}" y1="{AY+5}" x2="{x}" y2="{ty-9}" stroke="#DCCBB0" stroke-width="0.4"/>')
        s.append(f'<text x="{x}" y="{ty}" font-size="8.6" fill="#6E6459" text-anchor="middle">{name}</text>')
    # 两曲线
    s.append(f'<path d="M{AX+4},182 C 300,270 {CROSS-90},322 {CROSS},330 C {CROSS+120},340 800,395 960,422" fill="none" stroke="{RED}" stroke-width="1.9"/>')
    s.append(f'<path d="M{AX+4},422 C 300,342 {CROSS-90},338 {CROSS},330 C {CROSS+120},322 800,258 960,182" fill="none" stroke="{BLUE}" stroke-width="1.9"/>')
    # 交叉点
    s.append(f'<circle cx="{CROSS}" cy="330" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(f'<text x="{CROSS}" y="312" font-size="10" fill="{INK}" text-anchor="middle">玄</text>')
    s.append(f'<text x="{CROSS}" y="352" font-size="9.2" fill="#6E6459" text-anchor="middle">人在这里</text>')
    # 顶部
    s.append(f'<text x="{AX+10}" y="146" font-size="10.5" fill="{RED}">恒 有 欲</text>')
    s.append(f'<text x="940" y="146" font-size="10.5" fill="{BLUE}" text-anchor="end">恒 无 欲</text>')
    s.append(f'<text x="{W/2-32}" y="126" font-size="21" fill="{BLUE}" text-anchor="end">大 而 无 外</text>')
    s.append(f'<text x="{W/2+32}" y="126" font-size="21" fill="{RED}">小 而 无 内</text>')
    s.append(f'<circle cx="{W/2}" cy="118" r="13" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{W/2},105 A13,13 0 0 1 {W/2},131 A6.5,6.5 0 0 1 {W/2},118 A6.5,6.5 0 0 0 {W/2},105" fill="{INK}"/>')
    s.append(f'<circle cx="{W/2}" cy="111.5" r="2" fill="{PAPER}"/>')
    # 底
    s.append(f'<text x="{W/2}" y="562" font-size="16" fill="{INK}" text-anchor="middle" letter-spacing="4" font-family="{SANS}">I  KNOW  THAT  I  KNOW  NOTHING</text>')
    s.append(f'<text x="{W/2}" y="596" font-size="10.5" fill="{SEAL}" text-anchor="middle" letter-spacing="2">太玄之门：玄之又玄　众妙之门</text>')
    s.append('</svg>')
    return "\n".join(s)
for name,vis in (('ziqian-ladder',False),('ziqian-ladder-visible',True)):
    svg=build(vis)
    open(f'book/义理图/_refs/{name}.svg','w',encoding='utf8').write(svg)
    cairosvg.svg2png(url=f'book/义理图/_refs/{name}.svg',write_to=f'book/义理图/_refs/{name}.png',scale=2)
print('ok')
