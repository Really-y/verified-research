# Alətlər

Status yoxlanılıb: 2026-11-26 (Linux, Claude Code 2.1.332). Mənbələrin ətraflı statusu: `source-map/references/global.md`.

| Ehtiyac | Pulsuz yol | Pullu alternativ | Status |
|---|---|---|---|
| Veb axtarış və səhifə oxuma | Claude Code-un daxili `WebSearch` və `WebFetch` alətləri | - | işləyir (real sessiyada sınanıb, `tests/RESULTS.md`). `WebFetch` səhifəni modelə xülasə kimi verir; hərfi sitat üçün mənbəni `curl` və ya `verify_report.py` ilə yoxla |
| JavaScript səhifələri, scraping | Playwright (lokal, `npx playwright`) və ya Crawl4AI | Firecrawl (pulsuz plan: ayda 1 000 kredit), Apify | Playwright: bu maşında brauzerlər quraşdırılıb, amma plugin onu çağırmır. Crawl4AI, Firecrawl, Apify sınanmayıb (açar yoxdur). Qeyd: `verify_report.py` JavaScript icra etmir, ona görə belə səhifədən götürülən sitat yoxlamadan keçmir |
| Makro data | Dünya Bankı API, Eurostat API, OECD SDMX API | - | işləyir (API JSON/XML). IMF saytı və API-si avtomatik sorğulara 403 qaytarır |
| Elmi ədəbiyyat | OpenAlex və Crossref API, PubMed E-utilities, arXiv API | Scopus, Web of Science | işləyir (API JSON/XML, açarsız) |
| Şirkət məlumatı | milli reyestrlər, SEC EDGAR (`data.sec.gov`), Companies House (HTML) | Orbis, Crunchbase | EDGAR API və Companies House HTML işləyir. OpenCorporates: `robots.txt` axtarışı qadağan edir, API açar istəyir |
| Patentlər | WIPO Patentscope | Espacenet / EPO OPS (pulsuz qeydiyyat) | Patentscope işləyir (HTML, qismən JavaScript); Espacenet avtomatik sorğulara 403 |
| Ticarət datası | UN Comtrade public preview API, WITS (HTML), milli gömrük statistikası | ITC Trade Map, Comtrade tam API (pulsuz açar) | işləyir (API JSON, açarsız preview 500 sətirə qədər) |
| Sayt trafiki | Tranco API (aşağı etibarlılıq) | Similarweb API, Cloudflare Radar API (pulsuz token) | Tranco işləyir (API JSON); Similarweb və Radar sınanmayıb (açar yoxdur) |
| Açar söz və tələb | Google Trends (insan brauzerdə açıb CSV ixrac edir), axtarış təklifləri, rəqib sitemap-i | SEMrush, Ahrefs | Google Trends avtomatik əlçatmaz (`robots.txt`, JavaScript) |
| Brend izləmə | dövri veb axtarış (`competitor-watch`, README-də cədvəl), Google Maps rəyləri, açıq sosial səhifələr | Brand24, Mention | veb axtarış işləyir; pullu alətlər sınanmayıb |
| Rəqib reklamları | Meta Ad Library (insan brauzerdə açır) | Meta Ad Library API (tərtibatçı hesabı) | avtomatik əlçatmaz (403, `robots.txt` bağlıdır) |
| Sorğu | Google Forms, Tally (insan icra edir) | Typeform | - |
| Dashboard | CSV ixracı (`save_findings.py`), Google Sheets, Looker Studio | Power BI | CSV ixracı işləyir (`tests/run_tests.sh`); Looker Studio qoşulması README-də |
