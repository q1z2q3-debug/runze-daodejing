# 用法：在仓库根执行  python3 tools/refs/refs_two_gaze.py
import cairosvg
INK,SEAL,GREEN,LINE,LINE2,PAPER="#2F2A24","#A2503B","#4A5C55","#DCCBB0","#E6D8C2","#F8F3E6"
RED="#B5462F"; BLUE="#2E7C8F"; GREY="#8A7C69"
SERIF="'Noto Serif CJK SC','Noto Serif SC','Songti SC',serif"
SANS="'Noto Sans CJK SC','Noto Sans SC',sans-serif"
W,H=1000,1000
TOP=170; BOT=854; AX=290
ROWS=["量子|「无可再分」，它没有里面|一切精确性的底",
      "元素|同一元素，千万种样子|同一种料，到处可用",
      "原子|空轨道：价住在空处|能成键，才有万物",
      "无机小分子|晶格之间的间隙|能溶、能渗",
      "有机大分子|链与链之间的折叠空间|能存信息、能自组装",
      "蛋白质|活性口袋：口袋空了才装下底物|能催化，成为酶",
      "细胞|膜围出的「内」——第一次有里面|能代谢、能自持",
      "组织|细胞之间的缝|能输送、能连接",
      "器官|腔与管：胃腔、血管腔、心腔|能收纳、能流通",
      "五脏六腑|系统之间的循环回路|能生化、能平衡",
      "人体|意识：心里那个空，装得下万物|能观、能知",
      "家庭|成员之间的位份：人不在，位还空着|能承继、能相处",
      "团体·企业|岗位：职位是空位，人填进去|能分工、能协作",
      "国家|制度：一个空框，人处其中|能治、能序",
      "文明|生死之间的传递：人没了，话还在|能积累、能超越个体",
      "生态圈|物质循环的回路|能自养、能再生",
      "地球|圈层界面：地壳与大气之间|能承载",
      "星系|引力势阱：看不见的坑，星在其中|能聚、能成形",
      "宇宙|大而无外：连「外」也没有|能容一切"]
N=len(ROWS)
def y_of(i): return BOT-i*((BOT-TOP)/(N-1))
def build():
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="以有观无与以无观有：十九级的空与用" font-family="{SERIF}">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
       f'<text x="110" y="30" font-size="11" fill="{SEAL}" font-family="{SANS}" letter-spacing="3">义 理 图 · 有 无 双 观</text>',
       f'<text x="110" y="66" font-size="18" fill="{INK}">以有观无，一路上到宇宙；以无观有，一路下到量子</text>',
       f'<text x="110" y="92" font-size="10.4" fill="#6E6459">每一级都先造出一个「空」，新的性质就住在那个空里 —— 有之以为利，无之以为用。</text>']
    # 列头
    s.append(f'<text x="{AX-20}" y="112" font-size="8.6" fill="{GREY}" text-anchor="end" font-family="{SANS}" letter-spacing="2">级</text>')
    s.append(f'<text x="{AX+32}" y="112" font-size="8.6" fill="{RED}" font-family="{SANS}" letter-spacing="2">它造出的「无」（空）</text>')
    s.append(f'<text x="950" y="112" font-size="8.6" fill="{GREEN}" text-anchor="end" font-family="{SANS}" letter-spacing="2">因此之「用」</text>')
    # 轴：上箭头 / 下箭头
    s.append(f'<path d="M{AX},{BOT+2} L{AX},{TOP-2}" stroke="{LINE}" stroke-width="0.9"/>')
    s.append(f'<path d="M{AX-5},{TOP-14} L{AX},{TOP-52} L{AX+5},{TOP-14}" fill="none" stroke="{RED}" stroke-width="1.3"/>')
    s.append(f'<text x="{AX-16}" y="{TOP-46}" font-size="9" fill="{RED}" letter-spacing="1" text-anchor="end">以有观无 · 涌现在上</text>')
    s.append(f'<path d="M{AX-5},{BOT+14} L{AX},{BOT+52} L{AX+5},{BOT+14}" fill="none" stroke="{BLUE}" stroke-width="1.3"/>')
    s.append(f'<text x="{AX-16}" y="{BOT+48}" font-size="9" fill="{BLUE}" letter-spacing="1" text-anchor="end">以无观有 · 还原在下</text>')
    for i,row in enumerate(ROWS):
        lv,void,use=row.split("|")
        y=y_of(i)
        s.append(f'<line x1="{AX-10}" y1="{y-4}" x2="{AX+10}" y2="{y-4}" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<text x="{AX-24}" y="{y}" font-size="10" fill="{INK}" font-weight="600" text-anchor="end">{lv}</text>')
        s.append(f'<text x="{AX+30}" y="{y}" font-size="9" fill="{SEAL}">{void}</text>')
        s.append(f'<text x="950" y="{y}" font-size="9" fill="{GREEN}" text-anchor="end">{use}</text>')
    s.append(f'<text x="{W/2}" y="932" font-size="11" fill="{INK}" text-anchor="middle">此两者同出而异名，同谓之玄 —— 不是两条路，是同一实相的两面。</text>')
    s.append(f'<text x="{W/2}" y="960" font-size="9.6" fill="#6E6459" text-anchor="middle">向上看得越远，看见的是更大的空；向下看得越深，看见的是更细的实。</text>')
    s.append(f'<text x="{W/2}" y="984" font-size="9.6" fill="{SEAL}" text-anchor="middle">空不是没有，是被「有」围出来的那一处可用之处。</text>')
    s.append('</svg>')
    return "".join(s)
if __name__=="__main__":
    out=build()
    open("book/义理图/_refs/models/you-wu-two-gaze.svg","w",encoding="utf8").write(out)
    cairosvg.svg2png(bytestring=out.encode(),write_to="book/义理图/_refs/models/you-wu-two-gaze.png",scale=2,background_color=PAPER)
    print("ok")
