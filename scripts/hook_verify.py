#!/usr/bin/env python3
"""PostToolUse hook: reports/*.md yazılanda verify_report.py işə salır.

Uğursuzluqda nəticəni stderr-ə yazır və 2 kodu ilə çıxır: Claude Code
PostToolUse hook-unda yalnız 2 kodu stderr-i Claude-a göstərir.
"""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from verify_report import verify  # noqa: E402

MAX_ATTEMPTS = 3


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    p = Path(fp)
    if p.suffix != ".md" or p.parent.name != "reports":
        return 0
    buf = io.StringIO()
    try:
        rc = verify(p, out=buf)
    except Exception as e:  # skript xətası yoxlamanı səssiz ötürməməlidir
        sys.stderr.write("verified-research yoxlaması işləmədi (%s: %s). Hesabat yoxlanılmamış sayılır; "
                         "bunu istifadəçiyə bildir.\n" % (type(e).__name__, e))
        return 2
    counter = p.with_name("." + p.stem + ".attempts")
    if rc == 0:
        counter.unlink(missing_ok=True)
        return 0
    n = int(counter.read_text()) + 1 if counter.exists() else 1
    counter.write_text(str(n))
    sys.stderr.write("verified-research yoxlaması (cəhd %d/%d): %s\n%s\n" % (n, MAX_ATTEMPTS, p.name, buf.getvalue()))
    if n >= MAX_ATTEMPTS:
        sys.stderr.write("LİMİT: %d uğursuz cəhd. Hesabatı daha dəyişmə. Dayan və yuxarıdakı "
                         "uğursuz rəqəmləri istifadəçiyə göstər.\n" % n)
    else:
        sys.stderr.write("Uğursuz rəqəmləri mənbədən düzəlt və ya hesabatdan və findings.json-dan çıxar. Rəqəm uydurma.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
