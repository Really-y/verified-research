"""GOAL.md şərt 9: skriptin bilinən zəif yerləri üçün sınaqlar (şəbəkəsiz).

Hər blok bir zəif yeri göstərir. Əvvəlcə uğursuz olduqları görülüb, sonra skript düzəldilib.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import verify_report as V  # noqa: E402

n = 0


def ok(cond, msg):
    global n
    assert cond, msg
    n += 1


# 1. Minlik ayırıcısız dəyər ayırıcılı yazılışla uyğun gəlməli, mənası dəyişməməlidir
e = "Revenue was $1,234,567.89 in 2024."
ok(V.value_in("1234567.89", e), "1234567.89 ilə 1,234,567.89 eyni ədəddir")
ok(V.value_in("1234567,89", "Umsatz 1.234.567,89 Euro"), "alman yazılışı")
ok(V.value_in("58997,7", "dövriyyəsi 58 997,7 103,7"), "boşluqlu minlik")
ok(not V.value_in("1234.56789", e), "fərqli ədəd uyğun gəlməməlidir")
ok(not V.value_in("1234", "price 1,234.5 USD"), "kəsr hissəsi atılmamalıdır")
# birmənalı olmayan '1,234': 1234 (ingilis) və ya 1,234 (alman) ola bilər; ayırıcısız dəyər qəbul edilmir
ok(not V.value_in("1234", "ratio 1,234 units"), "birmənalı olmayan yazılış ayırıcısız dəyərlə uyğunlaşmamalıdır")
ok(V.value_in("1,234", "ratio 1,234 units"), "eyni yazılış həmişə uyğundur")

# 2. Ərəb, fars və hind rəqəmləri, sağdan-sola işarələri
ar = "‏بلغ حجم السوق ١٬٢٣٤٫٥ مليون دينار في عام ٢٠٢٤"
ok(V.value_in("1,234.5", ar), "ərəb rəqəmləri və ərəb ayırıcıları")
ok(V.value_in("١٬٢٣٤٫٥", ar), "dəyər ərəb rəqəmləri ilə yazılıb")
ok(not V.value_in("1,234.6", ar), "fərqli ərəb ədədi")
fa = "حجم بازار ۴۵٫۷ درصد رشد کرد"
ok(V.value_in("45.7", fa), "fars rəqəmləri")
hi = "बाजार का आकार ३४५ करोड़ रुपये"
ok(V.value_in("345", hi), "devanaqari rəqəmləri")
ok(V.norm_text("‏نص‎ عربي") == V.norm_text("نص عربي"), "istiqamət işarələri sitat müqayisəsinə təsir etmir")

# 3. registrable(): mürəkkəb domen sonluqları və paylaşılan hostinq
R = V.registrable
ok(R("www.abs.gov.au") == "abs.gov.au", "gov.au")
ok(R("news.yahoo.co.jp") == "yahoo.co.jp", "co.jp")
ok(R("www.example.or.jp") == "example.or.jp", "or.jp")
ok(R("www.ox.ac.uk") == "ox.ac.uk", "ac.uk")
ok(R("www.hurriyet.com.tr") == "hurriyet.com.tr", "com.tr")
ok(R("www.tuik.gov.tr") == "tuik.gov.tr", "gov.tr")
ok(R("blog1.blogspot.com") != R("blog2.blogspot.com"), "fərqli blogspot bloqları fərqli sahiblərdir")
ok(R("a.github.io") != R("b.github.io"), "github.io")
ok(R("x.substack.com") != R("y.substack.com"), "substack")
ok(R("www.stat.gov.az") == "stat.gov.az" and R("news.bbc.co.uk") == "bbc.co.uk", "köhnə davranış qalır")
ok(R("www.destatis.de") == "destatis.de" and R("ec.europa.eu") == R("eur-lex.europa.eu"), "adi domenlər")

# 4. Başlıq dil-neytral işarə ilə tanınır
md = "# R\n\n## Chiffres clés <!-- key-figures -->\n| a | b |\n|---|---|\n| x | [s](http://s) |\n"
ok(V.key_table_rows(md) is not None, "dil-neytral işarəli başlıq")
ok(V.key_table_rows("## Chiffres clés\n| a |\n|---|\n| x |\n") is None, "işarəsiz naməlum başlıq rədd edilir")
ok(V.has_crit_heading("## Critique et contre-argument <!-- critique -->\n"), "tənqid başlığı işarə ilə")

# 5. Ardıcıl tam ədədlər: alt-hissə ilə uyğunluq qeyri-müəyyən sayılır
ok(V.ambiguous_match("30439", "əhali 30 439 102 nəfər"), "30439 alt-hissədir, qeyri-müəyyən")
ok(not V.ambiguous_match("30 439 102", "əhali 30 439 102 nəfər"), "tam ədəd birmənalıdır")
ok(not V.ambiguous_match("58 997,7", "dövriyyəsi 58 997,7 103,7"), "kəsrli ədəd birmənalıdır")

# 6. Müstəqillik: eyni sitat başqa domendə köçürmədir
ok(V.copied_quote("Bazarın həcmi 480 milyon manatdır.", "bazarın həcmi 480 milyon manatdır"), "eyni sitat")
ok(not V.copied_quote("bazarın həcmi 480 milyon manatdır", "rəsmi məlumata görə bazarın həcmi 495 milyon manat olmuşdur"), "fərqli sitat")

# 7. JavaScript səhifəsi aşkarlanır
js = '<html><head><script src="/app.js"></script></head><body><div id="__next"></div><noscript>Enable JavaScript</noscript></body></html>'
ok(V.looks_js_only(js, V.html_to_text(js)), "boş SPA səhifəsi")
static = "<html><body>" + "<p>Pərakəndə ticarət dövriyyəsi 57,4 milyard manat.</p>" * 20 + "</body></html>"
ok(not V.looks_js_only(static, V.html_to_text(static)), "statik səhifə")
# sınaq zamanı tapılan yanlış rədd: az mətnli statik səhifədə adi <script> teqi JavaScript səhifəsi sayılırdı
small = '<html><head><script>var x=1;</script></head><body><p>Dövriyyə 57,4 milyard manat.</p></body></html>'
ok(not V.looks_js_only(small, V.html_to_text(small)), "kiçik statik səhifə skript teqi ilə")
# Next.js səhifəsində data skriptin içindədir: sitat oradan tapılmalıdır
nx = ('<html><body><div id="__next"></div><script id="__NEXT_DATA__" type="application/json">'
      '{"props":{"text":"Bazar\\u0131n h\\u0259cmi 480 milyon manatd\\u0131r"}}</script></body></html>')
ok(V.quote_in_scripts("bazarın həcmi 480 milyon manatdır", nx), "sitat Next.js datasında")
ok(not V.quote_in_scripts("bazarın həcmi 999 milyon manatdır", nx), "uydurma sitat skript datasında da yoxdur")

# 8. Real sınaqda tapıldı (critic, DSK PDF): PDF mətnində sözlərin içinə boşluq düşür
#    ('real ifad ədə 3,7 faiz', 'pə rakəndə'); düzgün sitat rədd edilməməlidir
pdf = "dəyəri əvvəlki ill ə müqayisədə real ifad ədə 3,7 faiz artaraq ümumi pə rakəndə ticarət"
ok(V.quote_in_text("real ifadədə 3,7 faiz artaraq ümumi pərakəndə ticarət", pdf), "PDF-də sözün içində boşluq")
ok(not V.quote_in_text("real ifadədə 3,9 faiz artaraq", pdf), "fərqli rəqəm yenə rədd edilir")
ok(not V.quote_in_text("real ifadədə 13,7 faiz", pdf), "boşluqsuz müqayisə rəqəm sərhədini pozmamalıdır")

# 9. Real sınaqda tapıldı: pozuq URL skripti çökdürürdü (fetch ValueError)
st, txt, note, raw = V.fetch("example.com/yoxdur")
ok(st == 0 and note, "pozuq URL problem kimi qaytarılır, çökmür")

print("KEÇDİ   zəif yerlər (%d yoxlama)" % n)
