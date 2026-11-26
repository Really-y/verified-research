#!/usr/bin/env bash
# Yoxlama skriptinin və hook-un sınağı. Lokal veb server saxta "mənbə" rolunu oynayır.
# İstifadə: bash tests/run_tests.sh   (çıxış kodu 0 = bütün sınaqlar gözlənilən nəticəni verdi)
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
W="$(mktemp -d)"; mkdir -p "$W/site" "$W/reports"; cd "$W"
PORT=8765; B="http://127.0.0.1:$PORT"
export VERIFY_TODAY=2026-11-26
python3 - << 'EOF'
import json
dims = ["market_size", "growth", "segments", "customers", "competitors", "pricing",
        "channels", "regulation", "trade", "entry_barriers", "trends", "risks"]
json.dump({"type": "market", "items": {d: {"status": "found"} for d in dims}}, open("default.coverage.json", "w"))
json.dump({
    "author": "critic",
    "assumptions": [{"text": "Tələb növbəti üç ildə indiki tempdə artacaq", "weakest": True},
                    {"text": "Tənzimləmə dəyişməyəcək"}],
    "counter_case": "Bazar artıq doymuş ola bilər: artım yalnız qiymət artımından gəlir, həcm sabitdir.",
    "objections": [
        {"text": "Güclü rəqib artıq bazardadır və qiyməti aşağı sala bilər", "severity": "high",
         "response": "rejected", "response_note": "Rəqibin payı kiçikdir və başqa seqmentdə işləyir"},
        {"text": "Bazar həcmi tək media mənbəyinə söykənir", "severity": "medium",
         "response": "accepted", "response_note": "Rəsmi mənbə ilə təsdiq əlavə olundu, hər iki rəqəm göstərilir"},
        {"text": "Mövsümilik nəzərə alınmayıb", "severity": "low",
         "response": "partially", "response_note": "Boşluqlar bölməsinə qeyd əlavə olundu, data tapılmadı"}]},
    open("default.critique.json", "w", encoding="utf-8"), ensure_ascii=False)
EOF
cat > site/stat.html << 'EOF'
<html><head><meta charset="utf-8"><style>p{color:red}</style><script>var x=99999;</script></head><body>
<h1>Pərakəndə ticarət</h1>
<p>2023-cü ildə pərakəndə ticarət dövriyyəsi <b>57,4</b> milyard manat təşkil etmişdir.</p>
<p>Ölkə əhalisinin sayı 10&nbsp;180,8 min nəfər olmuşdur.</p>
</body></html>
EOF
(cd site && exec python3 -m http.server $PORT >/dev/null 2>&1) & SRV=$!
trap 'kill $SRV 2>/dev/null; [ -n "${KEEP:-}" ] || rm -rf "$W"' EXIT
sleep 1
cat > reports/good.findings.json << EOF
[
 {"indicator":"Pərakəndə ticarət dövriyyəsi","value":"57,4","unit":"mlrd manat","period":"2023","source_url":"$B/stat.html","quote":"2023-cü ildə pərakəndə ticarət dövriyyəsi 57,4 milyard manat təşkil etmişdir.","accessed":"2026-11-25","confidence":"yüksək","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Əhali","value":"10 180,8","unit":"min nəfər","period":"2023","source_url":"$B/stat.html","quote":"Ölkə əhalisinin sayı 10 180,8 min nəfər olmuşdur.","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Adambaşına dövriyyə","value":"5 638","unit":"manat","type":"estimate","formula":"57,4 mlrd / 10 180,8 min","inputs":["57,4","10 180,8"]}
]
EOF
cat > reports/good.md << EOF
# Pərakəndə ticarət

Tarix: 2026-11-25

## Xülasə
2023-cü ildə dövriyyə 57,4 mlrd manat olub. Adambaşına TƏXMİN 5 638 manat.

## Əsas rəqəmlər
| Göstərici | Dəyər | Dövr | Mənbə | Etibarlılıq |
|---|---|---|---|---|
| Dövriyyə | 57,4 mlrd manat | 2023 | [DSK]($B/stat.html) | yüksək |
| Əhali | 10 180,8 min | 2023 | [DSK]($B/stat.html) | yüksək |
| Adambaşına dövriyyə (TƏXMİN) | 5 638 manat | 2023 | hesablama | orta |
EOF
# uydurma: agent həm rəqəmi, həm sitatı uydurur (mənbədə 57,4)
sed 's/57,4/62,1/g' reports/good.findings.json > reports/fabricated.findings.json
sed 's/57,4/62,1/g' reports/good.md > reports/fabricated.md
# ölü link
sed 's#stat.html#yoxdur.html#g' reports/good.findings.json > reports/deadlink.findings.json
sed 's#stat.html#yoxdur.html#g' reports/good.md > reports/deadlink.md
# mətndə mənbəsiz rəqəmlər + linksiz cədvəl sətri
cp reports/good.findings.json reports/unsourced.findings.json
sed 's/^## Əsas rəqəmlər/Bazar ildə 12,5% böyüyür və 340 min müştəri var.\n\n## Əsas rəqəmlər/; s#\[DSK\]([^)]*) | yüksək |$#DSK | yüksək |#' reports/good.md > reports/unsourced.md
# sitat düzdür, amma yazılan dəyər fərqlidir
sed '0,/"value":"57,4"/s//"value":"59,9"/' reports/good.findings.json > reports/mismatch.findings.json
sed 's/57,4 mlrd/59,9 mlrd/g' reports/good.md > reports/mismatch.md
# təxmin düstursuz
sed 's/,"formula":"[^"]*","inputs":\[[^]]*\]//' reports/good.findings.json > reports/badestimate.findings.json
cp reports/good.md reports/badestimate.md
# tapıntı faylı yoxdur
cp reports/good.md reports/nofindings.md

FAIL=0
check() { # ad, gözlənilən kod, gözlənilən mətn
  [ -f "reports/$1.coverage.json" ] || [ "$1" = nocoverage ] || cp default.coverage.json "reports/$1.coverage.json"
  [ -f "reports/$1.critique.json" ] || [ "$1" = nocritique ] || cp default.critique.json "reports/$1.critique.json"
  if [ -f "reports/$1.md" ] && [ "$1" != noheading ] && ! grep -q "^## Tənqid və əks mövqe" "reports/$1.md"; then
    printf '\n## Tənqid və əks mövqe\nƏn zəif fərziyyə tələbin növbəti üç ildə indiki tempdə artacağıdır. Əks mövqe: bazar artıq doymuş ola bilər, artım yalnız qiymət artımından gəlir, həcm isə sabitdir. Əsas etirazlar: güclü rəqib qiyməti aşağı sala bilər (rədd edildi, rəqibin payı kiçikdir), bazar həcmi tək media mənbəyinə söykənir (qəbul edildi, rəsmi mənbə əlavə olundu), mövsümilik nəzərə alınmayıb (qismən).\n' >> "reports/$1.md"
  fi
  [ -f "reports/$1.md" ] && [ "$1" != stalecrit ] && touch "reports/$1.md"
  out="$(python3 "$ROOT/scripts/verify_report.py" "reports/$1.md" --delay 0 2>&1)"; rc=$?
  if [ $rc -eq $2 ] && grep -q "$3" <<< "$out"; then echo "KEÇDİ   $1 (kod $rc, \"$3\")"
  else echo "UĞURSUZ $1 (kod $rc, gözlənilən $2 və \"$3\")"; echo "$out" | sed 's/^/    /'; FAIL=1; fi
}
echo "--- verify_report.py"
check good        0 "YOXLAMA KEÇDİ"
check fabricated  1 "SİTAT TAPILMADI"
check deadlink    1 "LİNK İŞLƏMİR"
check unsourced   1 "MƏNBƏSİZ RƏQƏM"
check unsourced   1 "CƏDVƏL SƏTRİNDƏ MƏNBƏ LİNKİ YOXDUR"
check mismatch    1 "RƏQƏM SİTATDA YOXDUR"
check badestimate 1 "TƏXMİN ƏSASSIZDIR"
check nofindings  1 "TAPINTI FAYLI YOXDUR"

echo "--- hook_verify.py"
hook() { echo "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$1\"}}" | python3 "$ROOT/scripts/hook_verify.py" 2>"$W/err"; echo $?; }
exp() { if [ "$2" = "$3" ]; then echo "KEÇDİ   $1 (kod $2)"; else echo "UĞURSUZ $1 (kod $2, gözlənilən $3)"; FAIL=1; fi; }
exp "düzgün hesabat"            "$(hook "$W/reports/good.md")" 0
exp "hesabat olmayan fayl"      "$(hook "$W/site/stat.html")" 0
exp "reports xaricində .md"     "$(hook "$W/notes.md")" 0
exp "uydurma hesabat, cəhd 1"   "$(hook "$W/reports/fabricated.md")" 2
grep -q "SİTAT TAPILMADI" "$W/err" && echo "KEÇDİ   stderr-də səbəb göstərilir" || { echo "UĞURSUZ stderr boşdur"; FAIL=1; }
hook "$W/reports/fabricated.md" >/dev/null
exp "uydurma hesabat, cəhd 3"   "$(hook "$W/reports/fabricated.md")" 2
grep -q "LİMİT" "$W/err" && echo "KEÇDİ   3-cü cəhddə dayanma təlimatı verilir" || { echo "UĞURSUZ limit mesajı yoxdur"; FAIL=1; }

# real sınaqda tapıldı (biznes): tənqiddən əvvəlki qaralamalar cəhd limitini doldururdu
cp reports/good.md reports/draft.md; cp reports/good.findings.json reports/draft.findings.json; cp default.coverage.json reports/draft.coverage.json
for i in 1 2 3 4; do r=$(hook "$W/reports/draft.md"); done
exp "tənqidsiz qaralama, 4-cü yazılış" "$r" 2
grep -q "cəhd sayılmadı" "$W/err" && ! grep -q "LİMİT" "$W/err" && [ ! -f reports/.draft.attempts ] \
  && echo "KEÇDİ   yalnız tənqid mərhələsi qalan qaralama cəhd limitini xərcləmir" || { echo "UĞURSUZ qaralama cəhd sayıldı"; FAIL=1; }
sed 's/57,4/62,1/g' reports/draft.md > reports/draft2.md; sed 's/57,4/62,1/g' reports/draft.findings.json > reports/draft2.findings.json; cp default.coverage.json reports/draft2.coverage.json
hook "$W/reports/draft2.md" >/dev/null
grep -q "cəhd 1/3" "$W/err" && echo "KEÇDİ   tənqidsiz qaralamada uydurma rəqəm yenə cəhd sayılır" || { echo "UĞURSUZ uydurma qaralama cəhd sayılmadı"; FAIL=1; }

# real sınaqda tapıldı (şirkət): problemləri azaldan agent limitə çatıb tənqiddən əvvəl dayanırdı
sed 's/57,4/62,1/g; s/10 180,8/10 999,9/g' reports/good.md > reports/prog.md
sed 's/57,4/62,1/g; s/10 180,8/10 999,9/g' reports/good.findings.json > reports/prog.findings.json; cp default.coverage.json reports/prog.coverage.json; cp default.critique.json reports/prog.critique.json
hook "$W/reports/prog.md" >/dev/null; hook "$W/reports/prog.md" >/dev/null
sed 's/10 999,9/10 180,8/g' reports/prog.md > reports/p.tmp && mv reports/p.tmp reports/prog.md
sed 's/10 999,9/10 180,8/g' reports/prog.findings.json > reports/p.tmp && mv reports/p.tmp reports/prog.findings.json
hook "$W/reports/prog.md" >/dev/null
grep -q "irəliləyiş var" "$W/err" && grep -q "cəhd 2/3" "$W/err" && echo "KEÇDİ   problem sayı azalanda cəhd sayılmır" || { echo "UĞURSUZ irəliləyiş cəhd sayıldı"; cat "$W/err" | head -3; FAIL=1; }
hook "$W/reports/prog.md" >/dev/null
grep -q "cəhd 3/3" "$W/err" && grep -q "LİMİT" "$W/err" && echo "KEÇDİ   irəliləyiş olmayanda limit yenə işləyir" || { echo "UĞURSUZ limit işləmədi"; FAIL=1; }

echo "--- save_findings.py"
python3 "$ROOT/scripts/save_findings.py" reports/good.findings.json --question "test" --sector "pərakəndə" >/dev/null
n=$(python3 -c "import sqlite3;print(sqlite3.connect('data/research.db').execute('select count(*) from findings').fetchone()[0])")
exp "bazaya 3 sətir yazıldı" "$n" 3
[ -s reports/good.csv ] && echo "KEÇDİ   CSV ixrac olundu" || { echo "UĞURSUZ CSV yoxdur"; FAIL=1; }
echo "--- ədəd tanıma"
python3 "$ROOT/tests/test_numbers.py" || FAIL=1

echo "--- PDF mənbə (DSK-nın 2023 press-relizinin real mətni)"
if python3 -c "import pypdf, reportlab" 2>/dev/null; then
  python3 "$ROOT/tests/make_pdf.py" "$ROOT/tests/fixtures/dsk_2023_retail.txt" site/dsk.pdf
  U="$B/dsk.pdf"
  mk() {
    cat > "reports/$1.findings.json" << EOF
[
 {"indicator":"Pərakəndə ticarət dövriyyəsi","value":"$2","unit":"mln manat","period":"2023","source_url":"$U","quote":"Pərakəndə ticarət dövriyyəsi $2 103,7","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Real artım","value":"3,7","unit":"faiz","period":"2023","source_url":"$U","quote":"2022-ci illə müqayisədə pərakəndə ticarət dövriyyəsi real ifadədə 3,7 faiz","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Adambaşına aylıq xərc","value":"484,2","unit":"manat","period":"2023","source_url":"$U","quote":"əhalinin bir nəfəri orta hesabla ayda 484,2 manatlıq","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true}
]
EOF
    cat > "reports/$1.md" << EOF
# Pərakəndə ticarət, 2023

## Xülasə
Dövriyyə $2 mln manat olub, real artım 3,7 faiz. Bir nəfər ayda orta hesabla 484,2 manat xərcləyib.

## Əsas rəqəmlər
| Göstərici | Dəyər | Dövr | Mənbə |
|---|---|---|---|
| Dövriyyə | $2 mln manat | 2023 | [DSK]($U) |
| Real artım | 3,7 faiz | 2023 | [DSK]($U) |
| Adambaşına aylıq xərc | 484,2 manat | 2023 | [DSK]($U) |
EOF
  }
  mk pdfreal "58 997,7"; mk pdfwrong "61 200,0"
  check pdfreal  0 "3/3 fakt təsdiqləndi"
  check pdfwrong 1 "SİTAT TAPILMADI"
else
  echo "ÖTÜRÜLDÜ pypdf və reportlab quraşdırılmayıb (pip install pypdf reportlab)"
fi

echo "--- başqa dil və ədəd formatı (ingilis, alman)"
cat > site/acme.html << 'EOF'
<html><body><h1>ACME Annual Report 2024</h1>
<p>Revenue was $1,234,567.89 in 2024, up 12.5% year over year.</p>
<p>Der Umsatz betrug 1.234.567,89 Euro im Jahr 2024.</p>
<p>The company employed 3,400 people at year end.</p></body></html>
EOF
mken() { # ad, gəlir dəyəri
  cat > "reports/$1.findings.json" << EOF
[
 {"indicator":"Revenue","value":"$2","unit":"USD","country":"US","period":"2024","source_url":"$B/acme.html","quote":"Revenue was \$$2 in 2024, up 12.5% year over year.","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Revenue growth","value":"12.5","unit":"%","period":"2024","source_url":"$B/acme.html","quote":"Revenue was \$1,234,567.89 in 2024, up 12.5% year over year.","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Umsatz","value":"1.234.567,89","unit":"EUR","period":"2024","source_url":"$B/acme.html","quote":"Der Umsatz betrug 1.234.567,89 Euro im Jahr 2024.","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Employees","value":"3,400","period":"2024","source_url":"$B/acme.html","quote":"The company employed 3,400 people at year end.","type":"fact","source_tier":1,"tier_reason":"sınaq mənbəyi","stale_note":"sınaq","key":true},
 {"indicator":"Revenue per employee","value":"363","unit":"USD","type":"estimate","formula":"1,234,567.89 / 3,400","inputs":["1,234,567.89","3,400"]}
]
EOF
  cat > "reports/$1.md" << EOF
# ACME, 2024

Date: 2026-11-25

## Summary
Revenue was \$$2, up 12.5%. In euro terms the report states 1.234.567,89. Headcount was 3,400. ESTIMATE: revenue per employee is about 363 USD.

## Key figures
| Indicator | Value | Period | Source |
|---|---|---|---|
| Revenue | \$$2 | 2024 | [ACME]($B/acme.html) |
| Growth | 12.5% | 2024 | [ACME]($B/acme.html) |
| Employees | 3,400 | 2024 | [ACME]($B/acme.html) |
| Revenue per employee (ESTIMATE) | 363 USD | 2024 | calculation |
EOF
}
mken en "1,234,567.89"; mken enwrong "1,934,567.89"
check en      0 "4/4 fakt təsdiqləndi"
check enwrong 1 "SİTAT TAPILMADI"
# başlıq tanınmayan dildə: skript bunu bildirməlidir
sed 's/^## Key figures/## Chiffres clés/' reports/en.md > reports/badheading.md; cp reports/en.findings.json reports/badheading.findings.json
check badheading 1 "Əsas rəqəmlər bölməsi yoxdur"

echo "--- mənbə keyfiyyəti, çarpaz təsdiq, köhnəlik, əhatə"
# iki "müstəqil" mənbə: 127.0.0.1 və localhost fərqli host sayılır
cat > site/media.html << 'EOF'
<html><body><p>Ekspertlərin fikrincə bazarın həcmi 480 milyon manatdır.</p></body></html>
EOF
cat > site/agency.html << 'EOF'
<html><body><p>Rəsmi məlumata görə bazarın həcmi 495 milyon manat olmuşdur.</p>
<p>Digər hesablamaya görə bazarın həcmi 910 milyon manatdır.</p></body></html>
EOF
L="http://localhost:$PORT"
q() { # ad, findings JSON
  printf '%s\n' "$2" > "reports/$1.findings.json"
  cat > "reports/$1.md" << EOF
# Bazar

## Xülasə
Bazarın həcmi 480 milyon manatdır.

## Əsas rəqəmlər
| Göstərici | Dəyər | Dövr | Mənbə |
|---|---|---|---|
| Bazar həcmi | 480 mln manat | 2025 | [mənbə]($B/media.html) |
EOF
}
P='"indicator":"Bazar həcmi","value":"480","value_num":480000000,"unit":"mln manat","period":"2025","source_url":"'$B'/media.html","quote":"bazarın həcmi 480 milyon manatdır","type":"fact","key":true'
C_OK='{"source_url":"'$L'/agency.html","quote":"bazarın həcmi 495 milyon manat olmuşdur","value":"495","value_num":495000000,"source_tier":1,"tier_reason":"sınaq: rəsmi qurum"}'
C_FAR='{"source_url":"'$L'/agency.html","quote":"bazarın həcmi 910 milyon manatdır","value":"910","value_num":910000000,"source_tier":1,"tier_reason":"sınaq: rəsmi qurum"}'
C_SAME='{"source_url":"'$B'/agency.html","quote":"bazarın həcmi 495 milyon manat olmuşdur","value":"495","value_num":495000000,"source_tier":1,"tier_reason":"sınaq"}'
C_WEAK='{"source_url":"'$L'/agency.html","quote":"bazarın həcmi 495 milyon manat olmuşdur","value":"495","value_num":495000000,"source_tier":5}'
C_BADNUM='{"source_url":"'$L'/agency.html","quote":"bazarın həcmi 495 milyon manat olmuşdur","value":"495","value_num":480000000,"source_tier":1,"tier_reason":"sınaq"}'

q notier      "[{$P}]"
q unjustified "[{$P,\"source_tier\":1}]"
q singleweak  "[{$P,\"source_tier\":5}]"
q corrok      "[{$P,\"source_tier\":5,\"corroboration\":[$C_OK]}]"
q weakweak    "[{$P,\"source_tier\":5,\"corroboration\":[$C_WEAK]}]"
q samedomain  "[{$P,\"source_tier\":5,\"corroboration\":[$C_SAME]}]"
q conflict    "[{$P,\"source_tier\":5,\"corroboration\":[$C_FAR]}]"
q conflictok  "[{$P,\"source_tier\":5,\"discrepancy_note\":\"ikinci mənbə topdansatışı da daxil edir\",\"corroboration\":[$C_FAR,$C_OK]}]"
q fakenum     "[{$P,\"source_tier\":5,\"corroboration\":[$C_BADNUM]}]"
q nokey       "[{$(sed 's/,"key":true//' <<< "$P"),\"source_tier\":5}]"
q stale       "[{$(sed 's/"period":"2025"/"period":"2021"/' <<< "$P"),\"source_tier\":5,\"corroboration\":[$C_OK]}]"

q garbage     '["abc", 5, {"indicator":"x","value":"480","corroboration":"yox"}]'
check garbage     1 "TAPINTI OBYEKT DEYİL"
check notier      1 "MƏNBƏ SƏVİYYƏSİ YOXDUR"
check unjustified 1 "SƏVİYYƏ ƏSASLANDIRILMAYIB"
check singleweak  1 "ƏSAS RƏQƏM TƏK MƏNBƏYƏ SÖYKƏNİR"
check corrok      0 "+1 müstəqil mənbə"
check weakweak    1 "ƏSAS RƏQƏM ZƏİF MƏNBƏLƏRƏ SÖYKƏNİR"
check samedomain  1 "MÜSTƏQİL DEYİL"
check conflict    1 "ZİDDİYYƏT"
check conflictok  0 "YOXLAMA KEÇDİ"
check fakenum     1 "value_num DƏYƏRLƏ UYĞUN DEYİL"
check nokey       1 "ƏSAS RƏQƏM SEÇİLMƏYİB"
check stale       1 "KÖHNƏ DATA İŞARƏLƏNMƏYİB"

# tanınmış domen siyahısı: səviyyəni şişirtmək olmaz
python3 - "$ROOT/scripts" << 'EOF' && echo "KEÇDİ   domen səviyyələri (9 yoxlama)" || FAIL=1
import sys
sys.path.insert(0, sys.argv[1])
from verify_report import known_tier, load_trusted, registrable, sig_digits
t = load_trusted()
assert known_tier("www.stat.gov.az", t) == 1 and known_tier("data.worldbank.org", t) == 2
assert known_tier("www.tuik.gov.tr", t) == 1 and known_tier("example-blog.com", t) is None
assert known_tier("www.statistics.gov.uk", t) == 1 and known_tier("govexample.com", t) is None
assert registrable("www.stat.gov.az") == "stat.gov.az" and registrable("news.bbc.co.uk") == "bbc.co.uk"
assert sig_digits("58 997,7") == sig_digits(58997700000) and sig_digits("59,0") == sig_digits(59000000000)
EOF

# əhatə
cp reports/corrok.md reports/nocoverage.md; cp reports/corrok.findings.json reports/nocoverage.findings.json
check nocoverage 1 "ƏHATƏ FAYLI YOXDUR"
for t in covmissing covnosearch; do cp reports/corrok.md reports/$t.md; cp reports/corrok.findings.json reports/$t.findings.json; done
python3 - << 'EOF'
import json
d = json.load(open("default.coverage.json", encoding="utf-8"))
a = json.loads(json.dumps(d)); del a["items"]["regulation"]; del a["items"]["pricing"]
json.dump(a, open("reports/covmissing.coverage.json", "w", encoding="utf-8"), ensure_ascii=False)
b = json.loads(json.dumps(d)); b["items"]["pricing"] = {"status": "not_found", "searched": ["bir yer"]}
json.dump(b, open("reports/covnosearch.coverage.json", "w", encoding="utf-8"), ensure_ascii=False)
EOF
check covmissing  1 "ƏHATƏ NATAMAM"
check covnosearch 1 "AXTARIŞ YERİ GÖSTƏRİLMƏYİB"
# hər araşdırma növünün öz məcburi bölmələri var (şirkət, elmi, hüquq, texniki, siyasət, yoxlama, biznes, hədəf bazar)
echo "--- araşdırma növləri üzrə əhatə"
for t in company academic legal technical policy due_diligence business target_markets mixed badtype other2 otherok; do
  cp reports/corrok.md reports/cov_$t.md; cp reports/corrok.findings.json reports/cov_$t.findings.json; done
python3 - "$ROOT" << 'EOF2'
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from verify_report import TYPE_DIMENSIONS as T
def w(name, typ, items):
    json.dump({"type": typ, "items": items}, open("reports/cov_%s.coverage.json" % name, "w", encoding="utf-8"), ensure_ascii=False)
for t in ["company", "academic", "legal", "technical", "policy", "due_diligence", "business", "target_markets"]:
    full = {d: {"status": "found"} for d in T[t]}
    w(t, t, full)                                     # tam: keçir
    del full[T[t][-1]]; w(t + "_miss", t, full)       # sonuncu bölmə çatmır: rədd
both = {d: {"status": "found"} for d in T["market"] + T["legal"]}
w("mixed", ["market", "legal"], both)
both.pop("penalties"); w("mixed_miss", ["market", "legal"], both)
w("badtype", "markt", {"a": {"status": "found"}, "b": {"status": "found"}, "c": {"status": "found"}})
w("other2", "other", {"a": {"status": "found"}, "b": {"status": "found"}})
w("otherok", "other", {"a": {"status": "found"}, "b": {"status": "found"}, "c": {"status": "found"}})
EOF2
for t in company academic legal technical policy due_diligence business target_markets mixed; do
  check cov_$t 0 "YOXLAMA KEÇDİ"
  cp reports/corrok.md reports/cov_${t}_miss.md; cp reports/corrok.findings.json reports/cov_${t}_miss.findings.json
  check cov_${t}_miss 1 "ƏHATƏ NATAMAM"
done
check cov_badtype 1 "ARAŞDIRMA NÖVÜ TANINMIR"
check cov_other2  1 "ən azı 3 alt sual"
check cov_otherok 0 "YOXLAMA KEÇDİ"
grep -q "Araşdırma növü: market + legal" reports/cov_mixed.quality.md && echo "KEÇDİ   qarışıq növ keyfiyyət xülasəsində göstərilir" || { echo "UĞURSUZ qarışıq növ xülasədə yoxdur"; FAIL=1; }

[ -s reports/corrok.quality.md ] && grep -q "müstəqil mənbə ilə təsdiqlənib: 1" reports/corrok.quality.md \
  && grep -q "İnsan baxmalıdır" reports/corrok.quality.md && grep -q "sınaq: rəsmi qurum" reports/corrok.quality.md \
  && echo "KEÇDİ   keyfiyyət xülasəsi faylı yaradılır və əsaslandırılmış mənbələri insana göstərir" || { echo "UĞURSUZ keyfiyyət xülasəsi"; FAIL=1; }

echo "--- tənqid və əks mövqe"
crit() { # ad, python ifadəsi: d (default tənqid) üzərində dəyişiklik
  cp reports/corrok.md "reports/$1.md"; cp reports/corrok.findings.json "reports/$1.findings.json"
  python3 - "$1" "$2" << 'EOF'
import json, sys
d = json.load(open("default.critique.json", encoding="utf-8"))
exec(sys.argv[2])
json.dump(d, open("reports/%s.critique.json" % sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
EOF
}
cp reports/corrok.md reports/nocritique.md; cp reports/corrok.findings.json reports/nocritique.findings.json
crit fewobj     'd["objections"] = d["objections"][:1]'
crit unanswered 'd["objections"][0]["response"] = ""'
crit nonote     'd["objections"][1]["response_note"] = "ok"'
crit nocounter  'd["counter_case"] = ""'
crit noweakest  'd["assumptions"][0].pop("weakest")'
crit nosev      'd["objections"][2]["severity"] = "çox"'
crit rejected   'pass'
cp reports/corrok.md reports/noheading.md; cp reports/corrok.findings.json reports/noheading.findings.json
sed -i '/^## Tənqid və əks mövqe/,$d' reports/noheading.md

check nocritique 1 "TƏNQİD FAYLI YOXDUR"
check fewobj     1 "TƏNQİD NATAMAM"
check unanswered 1 "ETİRAZ CAVABSIZDIR"
check nonote     1 "ETİRAZIN CAVABI İZAHSIZDIR"
check nocounter  1 "ƏKS MÖVQE YOXDUR"
check noweakest  1 "ƏN ZƏİF FƏRZİYYƏ GÖSTƏRİLMƏYİB"
check nosev      1 "ETİRAZIN CİDDİLİYİ YANLIŞDIR"
check noheading  1 "Tənqid bölməsi yoxdur"
check rejected   0 "tənqid: 3 etiraz"
grep -q "Rədd edilmiş ciddi etirazlar" reports/rejected.quality.md && grep -q "rəqib artıq bazardadır" reports/rejected.quality.md \
  && echo "KEÇDİ   rədd edilmiş ciddi etiraz keyfiyyət xülasəsində insana göstərilir" || { echo "UĞURSUZ rədd edilmiş etiraz göstərilmir"; FAIL=1; }

# şirkət real sınağında tapıldı: model tənqidi özü yazdı; mətn faktı (sahiblər) rədd edilirdi
crit selfcrit 'd["author"] = "self"'
check selfcrit 1 "TƏNQİD MÜSTƏQİL DEYİL"
crit noauthor 'del d["author"]'
check noauthor 0 "YOXLAMA KEÇDİ"
grep -q "tənqidin müəllifi göstərilməyib" reports/noauthor.quality.md && echo "KEÇDİ   müəllifsiz tənqid insana göstərilir" || { echo "UĞURSUZ müəllifsiz tənqid xülasədə yoxdur"; FAIL=1; }
cat > site/owner.html << 'EOF2'
<html><body><p>PASHA Holding is owned by the Aliyev and Pashayev families in Azerbaijan.</p></body></html>
EOF2
for t in textok textbad; do cp reports/good.md reports/$t.md; done
python3 - "$B" << 'EOF2'
import json, sys
B = sys.argv[1]
g = json.load(open("reports/good.findings.json", encoding="utf-8"))
f = {"indicator": "Sahiblər", "value": "Aliyev and Pashayev families", "source_url": B + "/owner.html",
     "quote": "PASHA Holding is owned by the Aliyev and Pashayev families in Azerbaijan.", "type": "fact", "source_tier": 3, "tier_reason": "sınaq"}
json.dump(g + [f], open("reports/textok.findings.json", "w", encoding="utf-8"), ensure_ascii=False)
f2 = dict(f, value="Smith family")
json.dump(g + [f2], open("reports/textbad.findings.json", "w", encoding="utf-8"), ensure_ascii=False)
EOF2
check textok  0 "YOXLAMA KEÇDİ"
check textbad 1 "DƏYƏR SİTATDA YOXDUR"

# due diligence real sınağından: tənqid bölməsi yer tutucu qalmış, hesabat tənqiddən sonra yenilənməmişdi
sed '/^## Tənqid və əks mövqe/,$d' reports/corrok.md > reports/placeholder.md; cp reports/corrok.findings.json reports/placeholder.findings.json
printf '\n## Tənqid və əks mövqe\n(critic subagentinin nəticəsi gözlənilir)\n' >> reports/placeholder.md
check placeholder 1 "TƏNQİD BÖLMƏSİ BOŞDUR"
sed '/^## Tənqid və əks mövqe/,$d' reports/corrok.md > reports/stalecrit.md; cp reports/corrok.findings.json reports/stalecrit.findings.json
cp default.coverage.json reports/stalecrit.coverage.json
printf '\n## Tənqid və əks mövqe\nƏn zəif fərziyyə tələbin növbəti üç ildə indiki tempdə artacağıdır. Əks mövqe: bazar artıq doymuş ola bilər, artım yalnız qiymət artımından gəlir, həcm isə sabitdir. Əsas etirazlar: güclü rəqib qiyməti aşağı sala bilər, bazar həcmi tək media mənbəyinə söykənir, mövsümilik nəzərə alınmayıb; hamısına cavab verilib.\n' >> reports/stalecrit.md
touch -d "2 minutes ago" reports/stalecrit.md; cp default.critique.json reports/stalecrit.critique.json
check stalecrit 1 "HESABAT TƏNQİDDƏN SONRA YENİLƏNMƏYİB"

echo "--- zəif yerlər (GOAL şərt 9)"
python3 "$ROOT/tests/test_weaknesses.py" || FAIL=1
# köçürülmüş sitat: fərqli domen, amma eyni mətn
cat > site/copy.html << 'EOF'
<html><body><p>Xəbər: Ekspertlərin fikrincə bazarın həcmi 480 milyon manatdır.</p></body></html>
EOF
C_COPY='{"source_url":"'$L'/copy.html","quote":"bazarın həcmi 480 milyon manatdır","value":"480","value_num":480000000,"source_tier":1,"tier_reason":"sınaq"}'
q copied "[{$P,\"source_tier\":5,\"corroboration\":[$C_COPY]}]"
check copied 1 "köçürmə əlaməti"
# JavaScript səhifəsi: məzmun skriptdə, görünən mətn yoxdur
cat > site/spa.html << 'EOF'
<html><head><script src="/app.js"></script></head><body><div id="root"></div><noscript>Enable JavaScript</noscript></body></html>
EOF
cat > site/next.html << 'EOF'
<html><body><div id="__next"></div><script id="__NEXT_DATA__" type="application/json">{"props":{"t":"Ekspertlərin fikrincə bazarın həcmi 480 milyon manatdır."}}</script></body></html>
EOF
q spa  "[{$(sed 's#/media.html#/spa.html#' <<< "$P"),\"source_tier\":1,\"tier_reason\":\"sınaq\"}]"
q next "[{$(sed 's#/media.html#/next.html#' <<< "$P"),\"source_tier\":1,\"tier_reason\":\"sınaq\"}]"
check spa  1 "SƏHİFƏ JAVASCRIPT İLƏ YÜKLƏNİR"
check next 0 "skript datasında tapıldı"
# minlik ayırıcısız dəyər (mənbədə 1,234,567.89) və dil-neytral başlıq işarəsi
mken nosep "1,234,567.89"; sed -i 's/"value":"1,234,567.89"/"value":"1234567.89"/' reports/nosep.findings.json
check nosep 0 "4/4 fakt təsdiqləndi"
sed 's/^## Key figures/## Chiffres clés <!-- key-figures -->/' reports/en.md > reports/frmark.md; cp reports/en.findings.json reports/frmark.findings.json
check frmark 0 "YOXLAMA KEÇDİ"
# ardıcıl tam ədədlər: dəyər yalnız bir hissədir, insan baxmalıdır
cat > site/pop.html << 'EOF'
<html><body><p>Əhalinin sayı 10 180 812 nəfər olmuşdur.</p></body></html>
EOF
cat > reports/seq.findings.json << EOF
[{"indicator":"Əhali","value":"10 180","value_num":10180,"unit":"min","period":"2025","source_url":"$B/pop.html","quote":"Əhalinin sayı 10 180 812 nəfər olmuşdur.","type":"fact","source_tier":1,"tier_reason":"sınaq","key":true}]
EOF
printf '# Əhali\n\n## Xülasə\nƏhali 10 180 min.\n\n## Əsas rəqəmlər\n| G | D | M |\n|---|---|---|\n| Əhali | 10 180 | [m](%s/pop.html) |\n' "$B" > reports/seq.md
check seq 0 "YOXLAMA KEÇDİ"
grep -q "ardıcıl tam ədədlərin bir hissəsidir" reports/seq.quality.md && echo "KEÇDİ   ardıcıl tam ədədlər keyfiyyət xülasəsində insana göstərilir" || { echo "UĞURSUZ ardıcıl tam ədəd qeydi yoxdur"; FAIL=1; }

# real sınaqda tapıldı (Gürcüstan): xəritəsi olmayan ölkə üçün mənbə faylı yaradılmırdı
sed 's/"key":true}/"key":true,"country":"GE"}/' reports/good.findings.json > reports/nomap.findings.json; cp reports/good.md reports/nomap.md
check nomap 1 "ÖLKƏ MƏNBƏ FAYLI YOXDUR"
mkdir -p research-data/sources; printf '# Gürcüstan (GE)\n| Qurum | URL |\n|---|---|\n| Geostat | https://www.geostat.ge |\n' > research-data/sources/GE.md
check nomap 0 "YOXLAMA KEÇDİ"
sed 's/"key":true}/"key":true,"country":"AZ"}/' reports/good.findings.json > reports/azmap.findings.json; cp reports/good.md reports/azmap.md
check azmap 0 "YOXLAMA KEÇDİ"

echo; [ $FAIL -eq 0 ] && echo "BÜTÜN SINAQLAR KEÇDİ" || echo "UĞURSUZ SINAQ VAR"
exit $FAIL
