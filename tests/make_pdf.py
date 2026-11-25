"""Sınaq üçün mətn faylından PDF düzəldir. İstifadə: make_pdf.py giriş.txt çıxış.pdf"""
import glob
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

fonts = (glob.glob("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
         + glob.glob("/usr/share/fonts/**/*Sans*.ttf", recursive=True)
         + glob.glob("/Library/Fonts/Arial Unicode.ttf")
         + glob.glob("C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("F", fonts[0]))
c = canvas.Canvas(sys.argv[2])
c.setFont("F", 10)
y = 800
for line in open(sys.argv[1], encoding="utf-8"):
    c.drawString(40, y, line.rstrip("\n"))
    y -= 16
c.save()
