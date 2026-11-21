#!/usr/bin/env python3
"""改图前快照：把现行 SVG 复制进 book/义理图/_versions/chNN/<图名>.v<版本>.svg

用法：
  python3 tools/snapshot.py 2      # 第二章三幅
  python3 tools/snapshot.py all    # 正册全部
幂等：同图同版本已存在则跳过，绝不覆盖、绝不删除。
"""
import sys, pathlib, shutil, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "book/义理图"
VER = (ROOT / "VERSION").read_text().strip()

def main(arg):
    targets = None if arg == "all" else int(arg)
    made = skipped = 0
    for f in sorted(FIG.glob("*.svg")):
        m = re.match(r"ch(\d{2})", f.name)
        if not m:
            continue
        n = int(m.group(1))
        if targets is not None and n != targets:
            continue
        dest_dir = FIG / "_versions" / f"ch{n:02d}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{f.stem}.v{VER}.svg"
        if dest.exists():
            skipped += 1
            continue
        shutil.copy2(f, dest)
        made += 1
    scope = "正册全部" if targets is None else f"第{targets}章"
    print(f"快照 {scope} · v{VER}：新增 {made} 幅，已存在跳过 {skipped} 幅")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
