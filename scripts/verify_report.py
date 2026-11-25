#!/usr/bin/env python3
"""Hesabatı mənbələrlə tutuşdurur və keyfiyyətini ölçür. Modeldən asılı deyil.

Yoxlayır: (1) hər rəqəm mənbə səhifəsində hərfi keçir; (2) mənbə səviyyəsi göstərilib və
əsaslandırılıb; (3) əsas rəqəmlər ilkin mənbəyə və ya müstəqil ikinci mənbəyə söykənir və
mənbələr bir-biri ilə uzlaşır; (4) köhnə data işarələnib; (5) əhatə siyahısı tamdır; (6) tənqid aparılıb və hər etiraza cavab verilib.

İstifadə: verify_report.py reports/<ad>.md [--delay saniyə]
Yanaşı fayllar: <ad>.findings.json, <ad>.coverage.json, <ad>.critique.json. Nəticə: <ad>.quality.md
Çıxış kodu: 0 hamısı keçdi, 1 ən azı bir problem.
"""
import argparse
import datetime
import html
import io
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "verified-research/0.4 (+report verification)"
SPACES = "\u00a0\u2009\u202f\u2007"
KEY_HEADINGS = ["Əsas rəqəmlər", "Key figures", "Ключевые показатели", "Temel rakamlar"]
EST_MARKS = ["TƏXMİN", "ESTIMATE", "ОЦЕНКА", "TAHMİN"]
CRIT_HEADINGS = ["Tənqid və əks mövqe", "Critique and counter-case", "Критика и контраргументы", "Eleştiri ve karşı görüş"]
SEVERITIES = {"high", "medium", "low"}
RESPONSES = {"accepted", "partially", "rejected"}
MIN_OBJECTIONS = 3
MIN_NOTE = 15  # cavab izahının minimum uzunluğu (simvol)
AGREE_TOLERANCE = 0.10   # iki mənbə arasında icazəli nisbi fərq
STALE_YEARS = 2          # bundan köhnə data işarələnməlidir
MARKET_DIMENSIONS = ["market_size", "growth", "segments", "customers", "competitors", "pricing",
                     "channels", "regulation", "trade", "entry_barriers", "trends", "risks"]
STATUSES = {"found", "partial", "not_found"}
OFFICIAL_RE = re.compile(r"(^|\.)(gov|gob|gouv|govt|go|gc|mil)(\.[a-z]{2})?$")
SECOND_LEVEL = {"co", "com", "gov", "org", "net", "edu", "ac", "gob", "gouv", "go"}


# ---------- mətn və ədəd ----------
def norm_text(s):
    s = unicodedata.normalize("NFKC", s)
    for q in "“”„«»":
        s = s.replace(q, '"')
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def norm_num(s):
    s = unicodedata.normalize("NFKC", str(s))
    for ch in SPACES + " ":
        s = s.replace(ch, "")
    return s.replace(",", ".").strip(".")


SP = "[ %s]" % SPACES
NUM_RE = re.compile(r"\d{1,3}(?:%s\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)*" % SP)


def raw_numbers(text):
    """Ədədləri yazıldığı kimi qaytarır. Boşluq yalnız minlik ayırıcı kimi qəbul olunur."""
    return [m.group() for m in NUM_RE.finditer(unicodedata.normalize("NFKC", text))]


def numbers_in(text):
    return [norm_num(n) for n in raw_numbers(text)]


def value_in(value, text):
    """Dəyər mətndə ayrıca ədəd kimi keçirmi. '58 997,7 103,7' iki ədəddir."""
    v = norm_num(value)
    if not v:
        return False
    for raw in raw_numbers(text):
        if norm_num(raw) == v:
            return True
        toks = re.split(SP, raw)
        if len(toks) > 2 and not re.search(r"[.,]", raw):
            for i in range(len(toks)):
                for j in range(i + 1, len(toks) + 1):
                    if norm_num("".join(toks[i:j])) == v:
                        return True
    return False


def splits_into(raw, allowed):
    toks = re.split(SP, raw)

    def rec(i):
        if i == len(toks):
            return True
        for j in range(i + 1, len(toks) + 1):
            n = norm_num("".join(toks[i:j]))
            if (n in allowed or trivial(n)) and rec(j):
                return True
        return False
    return len(toks) > 1 and rec(0)


def trivial(n):
    """İllər və tək rəqəmli tam ədədlər mənbə tələb etmir."""
    return bool(re.fullmatch(r"\d", n) or re.fullmatch(r"(19|20)\d{2}", n))


def sig_digits(x):
    """Əhəmiyyətli rəqəmlər: '58 997,7' və 58997700000 eyni nəticəni verir."""
    if isinstance(x, (int, float)):
        x = ("%.10f" % x).rstrip("0").rstrip(".")
    return re.sub(r"\D", "", str(x)).strip("0")


# ---------- şəbəkə ----------
def html_to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return html.unescape(raw)


def fetch(url, timeout=25):
    """(status, text, qeyd) qaytarır."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = r.status
            ctype = (r.headers.get("Content-Type") or "").lower()
            body = r.read(15_000_000)
    except urllib.error.HTTPError as e:
        return e.code, "", "HTTP %s" % e.code
    except Exception as e:
        return 0, "", "%s: %s" % (type(e).__name__, e)
    if "pdf" in ctype or url.lower().split("?")[0].endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError:
            return status, "", "PDF oxunmadı (pip install pypdf)"
        try:
            pages = PdfReader(io.BytesIO(body)).pages
            return status, " ".join((p.extract_text() or "") for p in pages), ""
        except Exception as e:
            return status, "", "PDF oxunmadı: %s" % e
    m = re.search(r"charset=([\w-]+)", ctype)
    try:
        text = body.decode(m.group(1) if m else "utf-8", errors="replace")
    except LookupError:
        text = body.decode("utf-8", errors="replace")
    return status, (text if "json" in ctype else html_to_text(text)), ""


# ---------- mənbə keyfiyyəti ----------
def host_of(url):
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def registrable(host):
    """Müstəqillik müqayisəsi üçün əsas domen (sadələşdirilmiş)."""
    if not host or re.fullmatch(r"[\d.]+", host) or "." not in host:
        return host
    p = host.split(".")
    if len(p) >= 3 and len(p[-1]) == 2 and p[-2] in SECOND_LEVEL:
        return ".".join(p[-3:])
    return ".".join(p[-2:])


def load_trusted():
    out = {}
    f = Path(__file__).with_name("trusted_domains.txt")
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].split()
            if len(line) >= 2 and line[1].isdigit():
                out[line[0].lower()] = int(line[1])
    return out


def known_tier(host, trusted):
    """Domenin siyahıdakı səviyyəsi; rəsmi dövlət domeni üçün 1; tanınmırsa None."""
    best = None
    for dom, tier in trusted.items():
        if host == dom or host.endswith("." + dom):
            best = tier if best is None else min(best, tier)
    if best is None and OFFICIAL_RE.search(host):
        best = 1
    return best


def strip_for_scan(md):
    md = re.sub(r"(?s)```.*?```", " ", md)
    md = re.sub(r"`[^`]*`", " ", md)
    md = re.sub(r"\]\([^)]*\)", "]", md)
    md = re.sub(r"https?://\S+", " ", md)
    md = re.sub(r"(?m)^(Tarix|Date|Дата|Tarih):.*$", " ", md)
    md = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", md)
    md = re.sub(r"(?m)^\s*\d+[.)]\s", " ", md)
    return md


def key_table_rows(md):
    pat = r"(?ms)^##\s*(?:%s)\s*$(.*?)(?=^##\s|\Z)" % "|".join(map(re.escape, KEY_HEADINGS))
    m = re.search(pat, md)
    if not m:
        return None
    rows = [l for l in m.group(1).splitlines() if l.strip().startswith("|")]
    return [r for r in rows[2:] if r.strip("| -")]


def today():
    return datetime.date.fromisoformat(os.environ.get("VERIFY_TODAY", datetime.date.today().isoformat()))


class Run:
    def __init__(self, delay):
        self.delay, self.cache, self.problems, self.lines = delay, {}, [], []
        self.trusted = load_trusted()

    def bad(self, msg):
        self.problems.append(msg)
        self.lines.append("  ✘ " + msg)

    def ok(self, msg):
        self.lines.append("  ✔ " + msg)

    def page(self, url):
        if url not in self.cache:
            if self.cache:
                time.sleep(self.delay)
            self.cache[url] = fetch(url)
        return self.cache[url]

    def check_source(self, label, value, url, quote):
        """Rəqəm sitatda, sitat səhifədə. True/False."""
        if not url or not quote:
            self.bad("MƏNBƏSİZ (source_url və quote lazımdır): %s" % label)
            return False
        if not value_in(value, quote):
            self.bad("RƏQƏM SİTATDA YOXDUR: %s = %s, sitat: \"%s\"" % (label, value, quote[:120]))
            return False
        status, text, note = self.page(url)
        if status != 200:
            self.bad("LİNK İŞLƏMİR (%s): %s" % (note or status, url))
            return False
        if note:
            self.bad("%s: %s" % (note, url))
            return False
        if norm_text(quote) not in norm_text(text):
            self.bad("SİTAT TAPILMADI mənbə səhifəsində: %s \"%s\"" % (url, quote[:120]))
            return False
        return True

    def check_tier(self, label, item):
        """Səviyyəni yoxlayır; (səviyyə, 'siyahı'|'əsaslandırma') və ya (None, None)."""
        t = item.get("source_tier")
        if not isinstance(t, int) or not 1 <= t <= 6:
            self.bad("MƏNBƏ SƏVİYYƏSİ YOXDUR (source_tier 1–6 lazımdır): %s" % label)
            return None, None
        host = host_of(item.get("source_url", ""))
        k = known_tier(host, self.trusted)
        if k is not None:
            if t < k:
                self.bad("SƏVİYYƏ ŞİŞİRDİLİB: %s, %s siyahıda %d səviyyədir, %d yazılıb" % (label, host, k, t))
                return None, None
            return t, "siyahı"
        if t <= 3 and not str(item.get("tier_reason", "")).strip():
            self.bad("SƏVİYYƏ ƏSASLANDIRILMAYIB: %s, %s tanınmış siyahıda yoxdur; tier_reason yaz "
                     "(niyə rəsmi və ya ilkin mənbədir) və ya səviyyəni 4–6 et" % (label, host))
            return None, None
        return t, ("əsaslandırma" if t <= 3 else "siyahı")


def verify(report_path, delay=1.0, out=sys.stdout):
    report_path = Path(report_path)
    stem = report_path.with_suffix("")
    findings_path = Path(str(stem) + ".findings.json")
    coverage_path = Path(str(stem) + ".coverage.json")
    if not report_path.exists():
        print("Hesabat tapılmadı: %s" % report_path, file=out)
        return 1
    md = report_path.read_text(encoding="utf-8")
    if not findings_path.exists():
        print("✘ TAPINTI FAYLI YOXDUR: %s\nƏvvəlcə findings.json, sonra hesabatı yaz." % findings_path, file=out)
        return 1
    try:
        findings = json.loads(findings_path.read_text(encoding="utf-8"))
        assert isinstance(findings, list)
    except Exception as e:
        print("✘ findings.json oxunmadı: %s" % e, file=out)
        return 1

    R = Run(delay)
    scan = strip_for_scan(md)
    allowed = set()
    st = {"facts": 0, "verified": 0, "estimates": 0, "tiers": {}, "manual_tier": [], "key": 0,
          "key_primary": 0, "key_corroborated": 0, "stale": [], "discrepancies": []}

    for i, f in enumerate(findings, 1):
        if not isinstance(f, dict):
            R.lines.append("[%d]" % i)
            R.bad("TAPINTI OBYEKT DEYİL: #%d" % i)
            continue
        name = f.get("indicator", "#%d" % i)
        val = norm_num(f.get("value", ""))
        R.lines.append("[%d] %s = %s%s" % (i, name, f.get("value", "?"), "  (əsas)" if f.get("key") else ""))
        if not val:
            R.bad("DƏYƏR YOXDUR: %s" % name)
            continue
        allowed.add(val)
        allowed.update(numbers_in(str(f.get("period", ""))))

        if f.get("type") == "estimate":
            st["estimates"] += 1
            if not f.get("formula") or not f.get("inputs"):
                R.bad("TƏXMİN ƏSASSIZDIR (formula və inputs lazımdır): %s" % name)
            elif not any(k in md for k in EST_MARKS):
                R.bad("TƏXMİN İŞARƏLƏNMƏYİB (hesabatda %s sözlərindən biri yoxdur): %s" % (" / ".join(EST_MARKS), name))
            else:
                R.ok("təxmin: düstur və girişlər var")
            allowed.update(numbers_in(" ".join(map(str, f.get("inputs", []))) + " " + str(f.get("formula", ""))))
            continue

        st["facts"] += 1
        if not value_in(val, scan):
            R.lines.append("  · qeyd: bu dəyər hesabat mətnində istifadə olunmayıb")
        n0 = len(R.problems)
        src_ok = R.check_source(name, f.get("value"), f.get("source_url", ""), f.get("quote", ""))
        tier, how = R.check_tier(name, f)
        if tier:
            st["tiers"][tier] = st["tiers"].get(tier, 0) + 1
            if how == "əsaslandırma":
                st["manual_tier"].append("%s: %s (%s)" % (name, host_of(f["source_url"]), f.get("tier_reason")))

        # köhnəlik
        years = [int(y) for y in re.findall(r"(?:19|20)\d{2}", str(f.get("period", "")))]
        if years and max(years) < today().year - STALE_YEARS:
            if not str(f.get("stale_note", "")).strip():
                R.bad("KÖHNƏ DATA İŞARƏLƏNMƏYİB: %s, dövr %s. Daha yenisini axtar; yoxdursa stale_note yaz "
                      "(harada axtardın və niyə yenisi yoxdur)" % (name, f.get("period")))
            else:
                st["stale"].append("%s (%s): %s" % (name, f.get("period"), f.get("stale_note")))

        # çarpaz təsdiq
        good_corr, corr_tiers = 0, []
        base = registrable(host_of(f.get("source_url", "")))
        corr = f.get("corroboration") or []
        for j, c in enumerate(corr if isinstance(corr, list) else [], 1):
            lab = "%s, təsdiq mənbəyi %d" % (name, j)
            if not isinstance(c, dict):
                R.bad("TƏSDİQ MƏNBƏYİ OBYEKT DEYİL: %s" % lab)
                continue
            allowed.add(norm_num(c.get("value", "")))
            if registrable(host_of(c.get("source_url", ""))) == base:
                R.bad("MÜSTƏQİL DEYİL: %s əsas mənbə ilə eyni domendədir (%s)" % (lab, base))
                continue
            c_ok = R.check_source(lab, c.get("value"), c.get("source_url", ""), c.get("quote", ""))
            c_tier, c_how = R.check_tier(lab, c)
            if c_tier and c_how == "əsaslandırma":
                st["manual_tier"].append("%s: %s (%s)" % (lab, host_of(c.get("source_url", "")), c.get("tier_reason")))
            if not (c_ok and c_tier):
                continue
            a, b = f.get("value_num"), c.get("value_num")
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                R.bad("MÜQAYİSƏ MÜMKÜN DEYİL: %s, hər iki mənbədə value_num (eyni vahiddə ədəd) lazımdır" % lab)
                continue
            if sig_digits(b) != sig_digits(c.get("value")):
                R.bad("value_num DƏYƏRLƏ UYĞUN DEYİL: %s (%s və %s)" % (lab, c.get("value"), b))
                continue
            diff = abs(a - b) / abs(a) if a else 1.0
            if diff > AGREE_TOLERANCE:
                note = str(f.get("discrepancy_note", "")).strip()
                if not note:
                    R.bad("ZİDDİYYƏT: %s, mənbələr %.0f%% fərqlənir (%s və %s). Səbəbi araşdır və "
                          "discrepancy_note yaz, hesabatda hər iki rəqəmi göstər" % (lab, diff * 100, f.get("value"), c.get("value")))
                else:
                    st["discrepancies"].append("%s: %s və %s (%.0f%%). %s" % (name, f.get("value"), c.get("value"), diff * 100, note))
                continue
            good_corr += 1
            corr_tiers.append(c_tier)
        if isinstance(f.get("value_num"), (int, float)) and sig_digits(f["value_num"]) != sig_digits(f.get("value")):
            R.bad("value_num DƏYƏRLƏ UYĞUN DEYİL: %s (%s və %s)" % (name, f.get("value"), f["value_num"]))

        # əsas rəqəm qaydası
        if f.get("key"):
            st["key"] += 1
            if tier and tier <= 2:
                st["key_primary"] += 1
                if good_corr:
                    st["key_corroborated"] += 1
            elif tier and good_corr and (tier <= 4 or min(corr_tiers) <= 3):
                st["key_corroborated"] += 1
            elif tier and tier >= 5 and good_corr:
                R.bad("ƏSAS RƏQƏM ZƏİF MƏNBƏLƏRƏ SÖYKƏNİR: %s, %d səviyyəli mənbə yalnız 1–3 səviyyəli "
                      "mənbə ilə təsdiqlənə bilər" % (name, tier))
            elif tier:
                R.bad("ƏSAS RƏQƏM TƏK MƏNBƏYƏ SÖYKƏNİR: %s (%d səviyyə). İlkin rəsmi mənbə tap və ya "
                      "müstəqil ikinci mənbə ilə təsdiqlə (corroboration)" % (name, tier))
        if src_ok and len(R.problems) == n0:
            st["verified"] += 1
            R.ok("TƏSDİQLƏNDİ" + (" (+%d müstəqil mənbə)" % good_corr if good_corr else ""))

    # hesabat mətni
    R.lines.append("[hesabat mətni]")
    stray = sorted({norm_num(r) for r in set(raw_numbers(scan))
                    if norm_num(r) not in allowed and not trivial(norm_num(r)) and not splits_into(r, allowed)})
    for n in stray:
        R.bad("MƏNBƏSİZ RƏQƏM hesabatda (findings.json-da yoxdur): %s" % n)
    rows = key_table_rows(md)
    if rows is None:
        R.bad("Əsas rəqəmlər bölməsi yoxdur (başlıq bunlardan biri olmalıdır: %s)" % ", ".join("## " + h for h in KEY_HEADINGS))
    else:
        for r in rows:
            if "](http" not in r and not any(k in r for k in EST_MARKS):
                R.bad("CƏDVƏL SƏTRİNDƏ MƏNBƏ LİNKİ YOXDUR: %s" % r.strip()[:100])
    if st["facts"] and not st["key"]:
        R.bad("ƏSAS RƏQƏM SEÇİLMƏYİB: nəticənin söykəndiyi tapıntılara \"key\": true yaz")
    if not stray and rows:
        R.ok("mənbəsiz rəqəm yoxdur, cədvəl sətirlərində link var")

    # əhatə
    R.lines.append("[əhatə]")
    cov = {"found": 0, "partial": 0, "not_found": 0, "gaps": []}
    if not coverage_path.exists():
        R.bad("ƏHATƏ FAYLI YOXDUR: %s. Araşdırmadan əvvəl yoxlama siyahısını yaz" % coverage_path.name)
    else:
        try:
            cv = json.loads(coverage_path.read_text(encoding="utf-8"))
            items = cv["items"]
            assert isinstance(items, dict)
        except Exception as e:
            R.bad("coverage.json oxunmadı: %s" % e)
            items, cv = {}, {}
        if cv.get("type") == "market":
            missing = [d for d in MARKET_DIMENSIONS if d not in items]
            if missing:
                R.bad("ƏHATƏ NATAMAM: bazar araşdırmasında bu bölmələr yoxdur: %s" % ", ".join(missing))
        elif items and len(items) < 3:
            R.bad("ƏHATƏ NATAMAM: ən azı 3 alt sual lazımdır")
        for k, v in items.items():
            s = (v or {}).get("status")
            if s not in STATUSES:
                R.bad("ƏHATƏ STATUSU YANLIŞDIR: %s (found / partial / not_found olmalıdır)" % k)
                continue
            cov[s] += 1
            if s != "found":
                searched = [x for x in (v.get("searched") or []) if str(x).strip()]
                if len(searched) < 2:
                    R.bad("AXTARIŞ YERİ GÖSTƏRİLMƏYİB: %s tapılmayıb və ya natamamdır; ən azı 2 axtarış yeri yaz (searched)" % k)
                else:
                    cov["gaps"].append("%s (%s): axtarılıb: %s" % (k, s, "; ".join(map(str, searched))))
        if items and not any("ƏHATƏ" in p or "AXTARIŞ" in p for p in R.problems):
            R.ok("əhatə siyahısı tamdır: %d tapıldı, %d qismən, %d tapılmadı" % (cov["found"], cov["partial"], cov["not_found"]))

    # tənqid
    R.lines.append("[tənqid]")
    critique_path = Path(str(stem) + ".critique.json")
    crit = {"n": 0, "accepted": 0, "partially": 0, "rejected": 0, "rejected_high": [], "weakest": "", "counter": ""}
    if not critique_path.exists():
        R.bad("TƏNQİD FAYLI YOXDUR: %s. Hesabatı critic subagentinə ver" % critique_path.name)
    else:
        n0 = len(R.problems)
        try:
            cr = json.loads(critique_path.read_text(encoding="utf-8"))
            assert isinstance(cr, dict)
        except Exception as e:
            R.bad("critique.json oxunmadı: %s" % e)
            cr = {}
        objs = [o for o in (cr.get("objections") or []) if isinstance(o, dict)]
        if len(objs) < MIN_OBJECTIONS:
            R.bad("TƏNQİD NATAMAM: ən azı %d etiraz lazımdır, %d var" % (MIN_OBJECTIONS, len(objs)))
        for k, o in enumerate(objs, 1):
            text = str(o.get("text", "")).strip()
            lab = "etiraz %d (%s)" % (k, text[:60])
            if len(text) < MIN_NOTE:
                R.bad("ETİRAZ BOŞDUR: etiraz %d" % k)
                continue
            if o.get("severity") not in SEVERITIES:
                R.bad("ETİRAZIN CİDDİLİYİ YANLIŞDIR: %s (high / medium / low olmalıdır)" % lab)
                continue
            if o.get("response") not in RESPONSES:
                R.bad("ETİRAZ CAVABSIZDIR: %s (response: accepted / partially / rejected)" % lab)
                continue
            note = str(o.get("response_note", "")).strip()
            if len(note) < MIN_NOTE:
                R.bad("ETİRAZIN CAVABI İZAHSIZDIR: %s. response_note yaz: hesabatda nə dəyişdi və ya niyə dəyişmədi" % lab)
                continue
            crit["n"] += 1
            crit[o["response"]] += 1
            if o["response"] == "rejected" and o["severity"] == "high":
                crit["rejected_high"].append("%s. Rədd səbəbi: %s" % (text, note))
        crit["counter"] = str(cr.get("counter_case", "")).strip()
        if len(crit["counter"]) < MIN_NOTE:
            R.bad("ƏKS MÖVQE YOXDUR: counter_case yaz (nəticənin əksini müdafiə edən ən güclü arqument)")
        weak = [a for a in (cr.get("assumptions") or []) if isinstance(a, dict) and a.get("weakest") and str(a.get("text", "")).strip()]
        if not weak:
            R.bad("ƏN ZƏİF FƏRZİYYƏ GÖSTƏRİLMƏYİB: assumptions siyahısında birinə \"weakest\": true yaz")
        else:
            crit["weakest"] = str(weak[0]["text"]).strip()
        if not re.search(r"(?m)^##\s*(?:%s)\s*$" % "|".join(map(re.escape, CRIT_HEADINGS)), md):
            R.bad("Tənqid bölməsi yoxdur (başlıq bunlardan biri olmalıdır: %s)" % ", ".join("## " + h for h in CRIT_HEADINGS))
        if len(R.problems) == n0:
            R.ok("tənqid: %d etiraz (%d qəbul, %d qismən, %d rədd), əks mövqe və ən zəif fərziyyə var"
                 % (crit["n"], crit["accepted"], crit["partially"], crit["rejected"]))

    # keyfiyyət xülasəsi
    q = ["# Keyfiyyət xülasəsi: %s" % report_path.name, "",
         "Bu fayl yoxlama skripti tərəfindən yaradılıb, model tərəfindən yox.", "",
         "- Yoxlama: %s (%d problem)" % ("KEÇDİ" if not R.problems else "UĞURSUZ", len(R.problems)),
         "- Fakt tapıntıları: %d, mənbədə təsdiqləndi: %d; təxminlər: %d" % (st["facts"], st["verified"], st["estimates"]),
         "- Mənbə səviyyələri (1 ən yaxşı): " + (", ".join("%d-ci: %d" % (t, n) for t, n in sorted(st["tiers"].items())) or "yoxdur"),
         "- Əsas rəqəmlər: %d; ilkin və ya beynəlxalq rəsmi mənbədən: %d; müstəqil mənbə ilə təsdiqlənib: %d" % (st["key"], st["key_primary"], st["key_corroborated"]),
         "- Əhatə: %d tapıldı, %d qismən, %d tapılmadı" % (cov["found"], cov["partial"], cov["not_found"]),
         "- Tənqid: %d etiraz; %d qəbul, %d qismən, %d rədd" % (crit["n"], crit["accepted"], crit["partially"], crit["rejected"]), ""]
    if crit["weakest"]:
        q += ["## Ən zəif fərziyyə", crit["weakest"], ""]
    if crit["counter"]:
        q += ["## Əks mövqe", crit["counter"], ""]
    for title, arr in (("İnsan baxmalıdır: səviyyəsi siyahı ilə yox, əsaslandırma ilə qəbul edilən mənbələr", st["manual_tier"]),
                       ("İnsan baxmalıdır: Rədd edilmiş ciddi etirazlar", crit["rejected_high"]),
                       ("Köhnə data", st["stale"]), ("Mənbələr arası fərqlər", st["discrepancies"]),
                       ("Boşluqlar", cov["gaps"]), ("Problemlər", R.problems)):
        if arr:
            q += ["## " + title] + ["- " + a for a in arr] + [""]
    q += ["## Skript nəyi yoxlamır",
          "- Mənbənin özünün düzgünlüyünü", "- Sitatın həqiqətən həmin göstəriciyə, ölkəyə və tərifə aid olduğunu",
          "- Daha yaxşı mənbənin mövcud olub-olmadığını", "- Təhlil və tövsiyələrin əsaslılığını",
          "- Etirazların və onlara verilən cavabların haqlı olub-olmadığını (yalnız mövcudluğunu yoxlayır)", ""]
    try:
        Path(str(stem) + ".quality.md").write_text("\n".join(q), encoding="utf-8")
    except OSError:
        pass

    print("\n".join(R.lines), file=out)
    print("\nNəticə: %d/%d fakt təsdiqləndi, %d problem. Keyfiyyət xülasəsi: %s.quality.md"
          % (st["verified"], st["facts"], len(R.problems), stem.name), file=out)
    print("YOXLAMA KEÇDİ" if not R.problems else "YOXLAMA UĞURSUZ", file=out)
    return 0 if not R.problems else 1


def main():
    ap = argparse.ArgumentParser(description="Hesabatı mənbələrlə tutuşdurur və keyfiyyətini ölçür.")
    ap.add_argument("report")
    ap.add_argument("--delay", type=float, default=1.0, help="sorğular arası fasilə (san.)")
    a = ap.parse_args()
    sys.exit(verify(a.report, a.delay))


if __name__ == "__main__":
    main()
