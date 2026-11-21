# 用法：在仓库根执行  python3 tools/refs/refs_emergence.py
import cairosvg
INK,SEAL,GREEN,LINE,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#DCCBB0","#E6D8C2","#F8F3E6"
RED="#B5462F"; BLUE="#2E7C8F"; GREY="#8A7C69"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
W,H=1000,822
BH=72; X0=110; SW_=100; RISE=56; BASE=700
ROWS=[("原子","化合价","化学键"),
      ("小分子","反应性","分子的形状"),
      ("有机大分子","长链稳定","自组织"),
      ("蛋白质","催化（酶）","构象 · 识别"),
      ("细胞","代谢 · 自我维持","复制 · 边界"),
      ("组织","分工","协同"),
      ("器官","功能","系统里的角色"),
      ("人体","意识","自省")]
def by(i): return BASE-BH-i*RISE
def build():
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="涌现判据：八级台阶与生命门槛" font-family="{SERIF}">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
       f'<text x="24" y="30" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">义 理 图 · 涌 现 判 据</text>',
       f'<text x="24" y="66" font-size="18" fill="{INK}">涌现不在某一点开始，它每一级都在发生</text>',
       f'<text x="24" y="92" font-size="10.4" fill="#6E6459">而「生命」这一属性，起点在细胞 —— 蛋白质是材料，不是命。</text>']
    for i,(name,p1,p2) in enumerate(ROWS):
        c = GREEN if i==3 else (SEAL if i>=4 else GREY)
        x=X0+i*SW_; y=by(i)
        s.append(f'<rect x="{x}" y="{y}" width="{SW_}" height="{BH}" fill="{c}" opacity="0.07"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{SW_}" height="{BH}" fill="none" stroke="{c}" stroke-width="0.9"/>')
        s.append(f'<path d="M{x},{y} H{x+SW_}" stroke="{c}" stroke-width="2"/>')
        s.append(f'<text x="{x+9}" y="{y+23}" font-size="9.6" fill="{INK}" font-weight="600">{name}</text>')
        s.append(f'<text x="{x+9}" y="{y+42}" font-size="7.9" fill="{c}">{p1}</text>')
        s.append(f'<text x="{x+9}" y="{y+57}" font-size="7.9" fill="{c}">{p2}</text>')
    # 生命门槛
    xm=X0+4*SW_
    s.append(f'<line x1="{xm}" y1="208" x2="{xm}" y2="712" stroke="{RED}" stroke-width="1" stroke-dasharray="6 5"/>')
    s.append(f'<text x="{xm-12}" y="200" font-size="9.2" fill="{GREY}" text-anchor="end">此前都是「物」</text>')
    s.append(f'<text x="{xm+12}" y="200" font-size="9.6" fill="{RED}" letter-spacing="0.6">生命门槛 · 越此线才叫「活」</text>')
    # 底部判据
    lines=[("判据","涌现 = 下层单独不具备、且无法由下层线性加总得出的性质。",INK),
           ("检验","把上层拆回下层，新性质随即消失；而在拆开的下层里，找不到它的影子。","#6E6459"),
           ("两向","蛋白质离体即失活、不复制；细胞拆散即不代谢 —— 两头都拆得住，故「生命」属于细胞，不属于蛋白质。",SEAL)]
    for k,(tag,txt,c) in enumerate(lines):
        y=748+k*26
        s.append(f'<text x="{X0}" y="{y}" font-size="8.4" fill="{c}" font-family="{SANS}" letter-spacing="2">{tag}</text>')
        s.append(f'<text x="{X0+40}" y="{y}" font-size="9.8" fill="{c}">{txt}</text>')
    s.append('</svg>')
    return "".join(s)
if __name__=="__main__":
    out=build()
    open("book/义理图/_refs/models/emergence-threshold.svg","w",encoding="utf8").write(out)
    cairosvg.svg2png(bytestring=out.encode(),write_to="book/义理图/_refs/models/emergence-threshold.png",scale=2,background_color=PAPER)
    print("ok")
