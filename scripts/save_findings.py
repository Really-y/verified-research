#!/usr/bin/env python3
"""findings.json-u iş qovluğundakı data/research.db-yə yazır və CSV ixrac edir.

İstifadə: save_findings.py reports/<ad>.findings.json [--question "sual"] [--sector "sektor"]
"""
import argparse
import csv
import json
import sqlite3
from datetime import date
from pathlib import Path

COLS = ["tarix", "sual", "sektor", "gosterici", "deyer", "vahid", "dovr", "menbe_url",
        "sitat", "baxis_tarixi", "etibarliliq", "nov", "qeyd"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings")
    ap.add_argument("--question", default="")
    ap.add_argument("--sector", default="")
    ap.add_argument("--db", default="data/research.db")
    a = ap.parse_args()
    src = Path(a.findings)
    items = json.loads(src.read_text(encoding="utf-8"))
    Path(a.db).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(a.db)
    con.execute("CREATE TABLE IF NOT EXISTS findings (id INTEGER PRIMARY KEY AUTOINCREMENT, %s)"
                % ", ".join(c + " TEXT" for c in COLS))
    rows = []
    for f in items:
        note = f.get("note", "")
        if f.get("type") == "estimate":
            note = ("düstur: %s; girişlər: %s. %s" % (f.get("formula", ""), f.get("inputs", ""), note)).strip()
        rows.append([date.today().isoformat(), a.question, a.sector, f.get("indicator", ""),
                     str(f.get("value", "")), f.get("unit", ""), str(f.get("period", "")),
                     f.get("source_url", ""), f.get("quote", ""), f.get("accessed", ""),
                     f.get("confidence", ""), f.get("type", "fact"), note])
    con.executemany("INSERT INTO findings (%s) VALUES (%s)" % (", ".join(COLS), ", ".join("?" * len(COLS))), rows)
    con.commit()
    con.close()
    out = src.with_name(src.name.replace(".findings.json", ".csv"))
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(rows)
    print("%d tapıntı yazıldı: %s; CSV: %s" % (len(rows), a.db, out))


if __name__ == "__main__":
    main()
