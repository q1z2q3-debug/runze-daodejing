# 用法：在仓库根执行  python3 tools/refs/refs_sansheng.py
import cairosvg
INK,SEAL,GREEN,LINE,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#DCCBB0","#E6D8C2","#F8F3E6"
RED="#B5462F"; BLUE="#2E7C8F"; GREY="#8A7C69"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
W,H=1000,700
CY=286; R=54
NODES=[("无","道。未分化、无边界、本自寂静。\n不是空无一物，是还没有「物」。\n此处不可说，只能说「未」。", BLUE),
       ("一","第一次显。浑然一体，尚未分。\n此时「有」与「无」还抱在一起，\n叫它「有」，是因为它已经在了。", GREY),
       ("二","有与无相对，阴阳始分。\n**有无相生，从这里才成立** ——\n一个有了对面，才谈得上相生。", RED),
       ("三","二之间的那个「和」。\n不是第三个东西，是关系本身。\n冲气以为和 —— 和，才生得下万物。", GREEN),
       ("万","三的组合，层层涌现。\n从分子到细胞到人体到宇宙，\n十九级，每一级都再走一遍这个三。", SEAL)]
def cx(i): return 110+i*195
def build():
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="道生一、一生二、二生三、三生万物与反者道之动" font-family="{SERIF}">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
       f'<text x="24" y="30" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">义 理 图 · 生 成 之 序</text>',
       f'<text x="24" y="66" font-size="18" fill="{INK}">道生一，一生二，二生三，三生万物 —— 而「反」是它的引擎</text>',
       f'<text x="24" y="92" font-size="10.4" fill="#6E6459">关键在「三」：它不是第三个数，是二与二之间的那个和。数到三就错了，看到和才对。</text>']
    # 连线
    for i in range(4):
        x1,x2=cx(i)+R+4,cx(i+1)-R-4
        s.append(f'<line x1="{x1}" y1="{CY}" x2="{x2-8}" y2="{CY}" stroke="{LINE}" stroke-width="1"/>')
        s.append(f'<path d="M{x2-14},{CY-4} L{x2-4},{CY} L{x2-14},{CY+4}" fill="none" stroke="{LINE}" stroke-width="1.2"/>')
    # 节点
    for i,(ch,txt,c) in enumerate(NODES):
        x=cx(i)
        s.append(f'<circle cx="{x}" cy="{CY}" r="{R}" fill="{c}" opacity="0.08"/>')
        s.append(f'<circle cx="{x}" cy="{CY}" r="{R}" fill="none" stroke="{c}" stroke-width="1.2"/>')
        TAG={"无":"未","一":"初显","二":"分","三":"和","万":"成"}[ch]
        s.append(f'<text x="{x}" y="{CY-R-12}" font-size="9.2" fill="{c}" text-anchor="middle" letter-spacing="2">{TAG}</text>')
        s.append(f'<text x="{x}" y="{CY+13}" font-size="34" fill="{c}" text-anchor="middle">{ch}</text>')
        lines=txt.split("\n")
        for k,ln in enumerate(lines):
            bold = ln.startswith("**")
            t = ln.replace("**","")
            s.append(f'<text x="{x}" y="{CY+R+26+k*15}" font-size="8.5" fill="{SEAL if bold else "#5C5247"}" text-anchor="middle" font-weight="{"600" if bold else "400"}">{t}</text>')
    # 反者道之动 回环
    s.append(f'<path d="M890,{CY+R+72} L890,500 L110,500 L110,{CY+R+72}" fill="none" stroke="{SEAL}" stroke-width="1.1" stroke-dasharray="6 5"/>')
    s.append(f'<path d="M105,{CY+R+84} L110,{CY+R+68} L115,{CY+R+84}" fill="none" stroke="{SEAL}" stroke-width="1.2"/>')
    s.append(f'<text x="500" y="522" font-size="11" fill="{SEAL}" text-anchor="middle" letter-spacing="2">反 者 道 之 动 —— 生 而 不 居，返 而 后 生</text>')
    s.append(f'<text x="500" y="546" font-size="9" fill="#6E6459" text-anchor="middle">没有这一返，有就是死有，无就是死无，万物数到三就断了。</text>')
    s.append(f'<text x="500" y="606" font-size="9.6" fill="{INK}" text-anchor="middle">「无中生有」只能作理上的原点，不能作事上的先后 —— 否则又回到「先有一个无，再生出一个有」。</text>')
    s.append(f'<text x="500" y="630" font-size="9.6" fill="{INK}" text-anchor="middle">以化学作比：原子是「二」（实核与虚云），键是「三」（两原子之间的和），分子以上是「万物」。</text>')
    s.append(f'<text x="500" y="654" font-size="9" fill="{GREY}" text-anchor="middle">注家于「三」有数读（天地人／阴阳冲气／形气神），本书取「冲气以为和」一读，须在体例定谳。</text>')
    s.append('</svg>')
    return "".join(s)
if __name__=="__main__":
    out=build()
    open("book/义理图/_refs/models/dao-sheng-yi-er-san.svg","w",encoding="utf8").write(out)
    cairosvg.svg2png(bytestring=out.encode(),write_to="book/义理图/_refs/models/dao-sheng-yi-er-san.png",scale=2,background_color=PAPER)
    print("ok")
