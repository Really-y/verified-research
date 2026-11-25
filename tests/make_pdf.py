"""Sınaq üçün mətn faylından PDF düzəldir. İstifadə: make_pdf.py giriş.txt çıxış.pdf

Şrift mətndəki bütün hərfləri (ə, ş, ğ və s.) daşımalıdır; yoxsa PDF-dən çıxarılan mətndə
həmin hərflər itir və sınaq yanlış səbəbdən uğursuz olur. Ona görə ilk tapılan yox,
mətnin bütün simvollarını əhatə edən ilk şrift seçilir.
"""
import glob
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

text = open(sys.argv[1], encoding="utf-8").read()
need = {ord(c) for c in text if not c.isspace()}
candidates = (glob.glob("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
              + glob.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True)
              + glob.glob("/usr/share/fonts/**/*Sans*.ttf", recursive=True)
              + glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
              + glob.glob("/Library/Fonts/Arial Unicode.ttf")
              + glob.glob("C:/Windows/Fonts/arial.ttf"))
chosen = None
for path in candidates:
    try:
        font = TTFont("F", path)
    except Exception:
        continue
    if need <= set(font.face.charToGlyph):
        chosen = font
        break
if chosen is None:
    sys.exit("Mətnin bütün hərflərini daşıyan TTF şrift tapılmadı")
pdfmetrics.registerFont(chosen)
c = canvas.Canvas(sys.argv[2])
c.setFont("F", 10)
y = 800
for line in text.splitlines():
    c.drawString(40, y, line)
    y -= 16
c.save()
