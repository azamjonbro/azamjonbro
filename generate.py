# Usage: python3 generate.py [orange|blue|green|purple] [photo.jpg]  ->  neofetch.png
from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT = "/System/Library/Fonts/Menlo.ttc"
BG      = (13, 17, 23)      # github dark
import sys
THEMES = {
    "orange": ((255, 166, 87), (200, 120, 50), (110, 70, 35)),
    "blue":   ((88, 166, 255), (60, 120, 200), (35, 65, 110)),
    "green":  ((63, 185, 80),  (46, 140, 60),  (25, 75, 35)),
    "purple": ((188, 140, 255), (140, 95, 210), (75, 50, 115)),
}
THEME = sys.argv[1] if len(sys.argv) > 1 else "blue"
ART_HI, ART_MID, ART_LO = THEMES[THEME]
LABEL = TITLE = ART_HI
VALUE   = (230, 237, 243)   # light

# ---------- ASCII art from avatar ----------
COLS, ROWS = 54, 24
img = Image.open(sys.argv[2] if len(sys.argv) > 2 else "photo.jpg").convert("L").crop((160, 100, 590, 530))
img = ImageOps.invert(img)
img = ImageOps.autocontrast(img, cutoff=1)
thr = 50
img = img.point(lambda v: 0 if v < thr else int((v - thr) * 255 / (255 - thr)))
img = img.resize((COLS, ROWS), Image.LANCZOS)
ramp = " .:-=+*#%@"
art = []
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        v = img.getpixel((x, y))
        row += ramp[int(v / 256 * len(ramp))]
    art.append(row)

# ---------- info block ----------
info = [
    ("azamjonbro@github", None),
    ("---", None),
    ("OS", "macOS, Linux"),
    ("Uptime", "22 yil"),
    ("Location", "Namangan, Uzbekistan"),
    ("Kernel", "Full-Stack Engineer"),
    ("IDE", "VS Code, Cursor"),
    ("", None),
    ("Languages.Scripts", "JavaScript, TypeScript"),
    ("Languages.Frontend", "Vue, Nuxt, React, Next.js"),
    ("Languages.Mobile", "React Native, Electron"),
    ("Languages.Backend", "Node.js, Express, NestJS"),
    ("Databases", "PostgreSQL, MongoDB"),
    ("DevOps", "Docker, Git, Linux, Nginx"),
    ("", None),
    ("Hobbies", "Open Source, Typing, Side Projects"),
    ("", None),
    ("Contact.Telegram", "@azamjonbro"),
    ("Contact.Website", "azamjonbro.uz"),
    ("Contact.Codewars", "azamjonbro (4 kyu)"),
    ("Contact.Monkeytype", "azamjonbro"),
    ("", None),
    ("GitHub Stats:", None),
    ("Repos: 58 | Followers: 128 | Contributions: 2,255", None),
]

# ---------- render ----------
FS = 22
font = ImageFont.truetype(FONT, FS)
cw = font.getlength("M")
lh = int(FS * 1.35)
pad = 40
gap = 40
art_w = int(COLS * cw)
info_w = 0
for k, v in info:
    s = k if v is None else f"{k}: {v}"
    info_w = max(info_w, font.getlength(s))
W = int(pad + art_w + gap + info_w + pad)
H = int(pad + max(len(art), len(info)) * lh + pad)

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

# art — brighter chars in orange, dim in brown
for y, row in enumerate(art):
    for x, ch in enumerate(row):
        if ch == " ":
            continue
        r = ramp.index(ch)
        c = ART_HI if r >= 7 else ART_MID if r >= 4 else ART_LO
        d.text((pad + x * cw, pad + y * lh), ch, font=font, fill=c)

ix = pad + art_w + gap
for i, (k, v) in enumerate(info):
    y = pad + i * lh
    if k == "---":
        d.line((ix, y + lh // 2, ix + font.getlength("azamjonbro@github"), y + lh // 2), fill=LABEL, width=2)
    elif v is None:
        d.text((ix, y), k, font=font, fill=TITLE if i == 0 else VALUE)
    else:
        d.text((ix, y), k + ":", font=font, fill=LABEL)
        d.text((ix + font.getlength(k + ": "), y), v, font=font, fill=VALUE)

im.save("neofetch.png")
print(W, H)
