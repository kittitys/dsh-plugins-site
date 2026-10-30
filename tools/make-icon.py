# -*- coding: utf-8 -*-
"""
生成 dsh-mem0-memory 插件图标（2026-10-30）
- 512/256/128 PNG（圆角方形、渐变底、深色 DS 字），另出 SVG
- 配色取自站点 assets/site.css：--accent #4c8dff → --accent-2 #7ee0c0，字色 #0b1020
用法： python make-icon.py <输出目录>
"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

ACCENT = (76, 141, 255)     # #4c8dff
ACCENT2 = (126, 224, 192)   # #7ee0c0
INK = (11, 16, 32)          # #0b1020

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\msyhbd.ttc",
]


def pick_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("no bold font found")


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_icon(size, out_png, font_path, radius_ratio=0.22):
    ss = 4  # 超采样，抗锯齿更干净
    S = size * ss
    # 渐变底：左上 → 右下
    grad = Image.new("RGB", (S, S))
    px = grad.load()
    for y in range(S):
        for x in range(S):
            t = (x / (S - 1) * 0.55) + (y / (S - 1) * 0.45)
            px[x, y] = lerp(ACCENT, ACCENT2, min(1.0, max(0.0, t)))

    # 圆角遮罩
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius_ratio), fill=255)

    icon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    icon.paste(grad, (0, 0), mask)

    # DS 字：先画到透明层，按 alpha 包围盒裁切后居中粘贴（避免字体度量误差）
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(font_path, int(S * 0.46))
    text = "DS"
    spacing = int(S * 0.015)
    widths = [ldraw.textlength(ch, font=font) for ch in text]
    x = 0
    for ch in text:
        ldraw.text((x, 0), ch, font=font, fill=INK + (255,))
        x += ldraw.textlength(ch, font=font) + spacing
    glyph = layer.crop(layer.getbbox())

    # 缩放到目标尺寸：宽度占 62%，高度不超过 40%
    max_w, max_h = int(S * 0.62), int(S * 0.42)
    scale = min(max_w / glyph.width, max_h / glyph.height)
    glyph = glyph.resize((max(1, round(glyph.width * scale)), max(1, round(glyph.height * scale))), Image.LANCZOS)

    icon.paste(glyph, ((S - glyph.width) // 2, (S - glyph.height) // 2 - int(S * 0.01)), glyph)

    icon = icon.resize((size, size), Image.LANCZOS)
    icon.save(out_png, "PNG")
    return out_png


def make_svg(out_svg):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="dsh-mem0-memory">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4c8dff"/>
      <stop offset="1" stop-color="#7ee0c0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="512" height="512" rx="112" ry="112" fill="url(#g)"/>
  <text x="256" y="256" text-anchor="middle" dominant-baseline="central"
        font-family="Segoe UI, Arial, sans-serif" font-weight="700" font-size="225"
        letter-spacing="8" fill="#0b1020">DS</text>
</svg>
"""
    with open(out_svg, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return out_svg


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    font = pick_font()
    made = []
    for size in (512, 256, 128):
        name = f"dsh-mem0-memory-icon-{size}.png"
        made.append(make_icon(size, os.path.join(out_dir, name), font))
    made.append(make_svg(os.path.join(out_dir, "dsh-mem0-memory-icon.svg")))
    for p in made:
        print(f"{os.path.basename(p)}\t{os.path.getsize(p)} bytes")


if __name__ == "__main__":
    main()
