#!/usr/bin/env python3
"""Mənbə səhifəsinin mətnini yoxlama skriptinin gördüyü kimi çap edir (HTML, PDF, JSON).

Hərfi sitatı buradan köçür: verify_report.py sitatı eyni mətndə axtarır. WebFetch səhifəni
xülasə edir, ona görə ondan götürülən sitat çox vaxt yoxlamadan keçmir.

İstifadə: fetch_text.py URL [--grep söz] [--context 200]
Heç nə yazmır. Çıxış kodu: 0 uğurlu, 1 səhifə açılmadı.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from verify_report import fetch, looks_js_only  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--grep", help="yalnız bu sözün ətrafını göstər (registrsiz)")
    ap.add_argument("--context", type=int, default=200)
    ap.add_argument("--max", type=int, default=20000, help="maksimum simvol")
    a = ap.parse_args()
    status, text, note, raw = fetch(a.url)
    if status != 200 or note:
        print("AÇILMADI: %s %s" % (status, note))
        return 1
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip()
    if looks_js_only(raw, text):
        print("XƏBƏRDARLIQ: səhifə JavaScript ilə yüklənir; sitat yoxlanılmaya bilər. Statik səhifə, PDF və ya API axtar.")
    if a.grep:
        hits = [m.start() for m in re.finditer(re.escape(a.grep), text, re.I)]
        print("%d uyğunluq: %s" % (len(hits), a.grep))
        for h in hits[:20]:
            print("…" + text[max(0, h - a.context):h + a.context].replace("\n", " ") + "…\n")
        return 0
    print(text[:a.max])
    if len(text) > a.max:
        print("\n[... %d simvoldan %d göstərildi; --grep işlət]" % (len(text), a.max))
    return 0


if __name__ == "__main__":
    sys.exit(main())
