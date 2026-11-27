# Shared brief for research sub-agents (read fully before starting)

Repo: /home/user/verified-research (a research plugin). Its method is mandatory:
- Read `skills/research-method/SKILL.md` (sections "Çıxış faylları", sitat qaydaları) and `skills/source-quality/SKILL.md`.
- Every factual claim (tuition number, deadline, admission rule, legal article text) must be a FINDING with a
  VERBATIM quote copied from the text that `python3 /home/user/verified-research/scripts/fetch_text.py "<URL>" --grep "<word>"`
  prints. Never quote from WebFetch summaries, never translate quotes, never quote from memory. The number in
  `value` must appear in the quote exactly as written on the source (e.g. "3,000", "1.500", "6 000").
- Call scripts as ONE simple command each (no cd, &&, pipes, loops).
- Prefer official university / ministry / accreditation-agency pages and PDFs. Agencies/aggregators (studyportals,
  mastersportal, agency blogs) are tier 6 and may only be used to discover URLs, never as evidence.
- If a page is JS-only or blocked (403/robots), don't bypass it; find an official PDF or other official page, else record "Not verified".
- NEVER invent fees, deadlines, admission criteria or attendance rules. If not verifiable: say "Not verified".
- Do not recommend fake enrollment, fictitious attendance or misrepresenting study mode.

## Student profile
Azerbaijani citizen; Azerbaijani secondary school certificate (attestat, average 4/5) or a sub-bachelor (college,
"subbakalavr") diploma; English B1 self-assessed, NO IELTS/TOEFL; budget USD 800–2,000/year tuition;
Bachelor's, preferably IT/Computer Science/Software Engineering or Business; intake autumn 2027.
Wants a genuine full-time Bachelor's and, legally, as little physical presence abroad as the rules allow
(hybrid/online parts only where officially permitted).

## Output (write these files; do not edit anything else in the repo)
1. `reports/parts/<your-slug>.findings.json` — list of findings in the plugin format:
   {"indicator": "...", "value": "<as on source>", "value_num": <number or omit for text>, "unit": "EUR/year" ,
    "country": "<ISO2>", "period": "2026/27", "key": true/false, "source_url": "...", "quote": "<verbatim>",
    "source_tier": 1-6, "tier_reason": "<required if domain not gov and tier<=3: e.g. official site of public university X>",
    "accessed": "2026-11-27", "confidence": "yüksək|orta|aşağı", "type": "fact"}
   For text facts (e.g. "programme taught in English"), `value` must be a short string occurring verbatim in the quote.
   University official sites = tier 3 by default for their own fees/admissions (tier 1 only if it is a legally binding
   regulation/rector's order/senate resolution PDF — then give tier_reason). Government/ministry/accreditation agency = 1.
   If fees found are for 2025/26 or 2026/27 (2027/28 not yet published), say so in "period" and add "stale_note" if older than 2024.
2. `reports/parts/<your-slug>.notes.md` — per university, a block with ALL of these fields (write "Not verified" where
   you could not verify): Official name | Country/city | Accreditation authority (+ registry link) | Programme name &
   language | Exact annual tuition for non-EU/international (currency as published, year of schedule) | Mandatory other
   university fees (application, registration, enrollment) | Admission: is an Azerbaijani attestat accepted? sub-bachelor
   diploma? recognition/nostrification steps | Minimum grades | English requirement (IELTS/TOEFL, or internal test /
   interview / B1 accepted?) | Attendance rules (mandatory attendance %, exam presence) | Online/hybrid components
   officially permitted for full-time students (quote the rule) | Application URL | 2027 intake deadline (or latest known
   deadline + year) | Your verdict on budget fit | Source URLs with publication/access dates.
   Mark every statement VERIFIED (with finding) or ASSUMPTION/Not verified.
3. Final reply to the orchestrator: a compact summary (≤ 600 words): which universities fit the USD 800–2,000 budget,
   which accept B1/internal English test, which have official hybrid/online elements, biggest uncertainties.

Exchange rate: do not convert yourself in findings; the orchestrator will convert with an official rate.
Date today: 2026-11-27. Budget ~ 60–90 minutes of work; aim for depth on the 4–6 best candidates in your region
rather than shallow coverage of many.
