# Beynəlxalq və mövzu mənbələri

Status: `işləyir` / `qeydiyyat lazımdır` / `əlçatmaz` / `yoxlanılmayıb`. Format: data hansı şəkildə gəlir (HTML, PDF, API JSON/XML/CSV).

**Yoxlanılıb: 2026-11-26**, `curl` ilə, `verified-research/0.4` User-Agent-i ilə (yoxlama skriptinin göndərdiyi). Brauzer User-Agent-i ilə də sınanıb; "əlçatmaz" yazılan saytlar ikisində də 403 qaytarır. `robots.txt` hər birində oxunub; qadağan olunan yol istifadə edilmir.

**Vacib:** "əlçatmaz" o deməkdir ki, `verify_report.py` həmin domendəki səhifədən sitat yoxlaya bilmir. Rəqəmi oradan götürürsənsə, eyni rəqəmi işləyən API-dən və ya güzgü mənbədən (məsələn, IMF WEO rəqəmi Dünya Bankı API-dən) götür; yoxsa tapıntı yoxlamadan keçmir.

| Mövzu | Mənbə | URL (işləyən giriş nöqtəsi) | Səviyyə | Status |
|---|---|---|---|---|
| Makroiqtisadiyyat | Dünya Bankı API | https://api.worldbank.org/v2/country/AZ/indicator/NY.GDP.MKTP.CD?format=json | 2 | işləyir (API JSON). Veb sayt `data.worldbank.org` botlara 403 qaytarır, sitat üçün API URL-i işlət |
| Makroiqtisadiyyat | IMF Data, WEO, DataMapper API | https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH/AZE | 2 | əlçatmaz (bütün `imf.org` və `data.imf.org` avtomatik sorğulara 403, `robots.txt` də bağlıdır). Rəqəmi Dünya Bankı API-dən və ya milli mənbədən götür |
| Makro, sosial | OECD Data Explorer, SDMX API | https://sdmx.oecd.org/public/rest/ , https://data-explorer.oecd.org | 2 | işləyir (API SDMX-XML/CSV; Data Explorer HTML). Köhnə `data.oecd.org` 403 qaytarır |
| Ümumi statistika | UNdata | https://data.un.org/Data.aspx , https://data.un.org/ws/rest/ | 2 | işləyir (HTML cədvəl; SDMX API) |
| Avropa | Eurostat API | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?geo=DE&unit=CP_MEUR&na_item=B1GQ&time=2023 | 1 | işləyir (API JSON-stat; sayt HTML) |
| Ticarət | UN Comtrade (public preview API) | https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=31&period=2023&partnerCode=0&cmdCode=080222&flowCode=X | 2 | işləyir (API JSON, açarsız; 500 sətir limiti). Tam API üçün pulsuz qeydiyyat və açar lazımdır |
| Ticarət, tariflər | WITS | https://wits.worldbank.org | 2 | işləyir (HTML). API URL sxemi sınaqda 400/405 qaytardı; HTML səhifələrini işlət |
| Tariflər | WTO Tariff & Trade Data | https://ttd.wto.org/en | 2 | işləyir (HTML) |
| Əmək | ILOSTAT (rplumber API) | https://rplumber.ilo.org/data/indicator/?id=UNE_DEAP_SEX_AGE_RT_A&ref_area=AZE&format=.csv | 2 | işləyir (API CSV). Veb sayt `ilostat.ilo.org` Cloudflare yoxlaması ilə bağlıdır (403) |
| Kənd təsərrüfatı, ərzaq | FAOSTAT | https://bulks-faostat.fao.org/production/ | 2 | qismən: toplu ZIP/CSV yükləmə işləyir; veb interfeys JavaScript-dir, API (`faostatservices.fao.org`) 401 qaytarır, yəni qeydiyyat lazımdır. ZIP-dən götürülən rəqəmi skript yoxlaya bilmir |
| Səhiyyə | WHO GHO OData API | https://ghoapi.azureedge.net/api/WHOSIS_000001 | 2 | işləyir (API JSON; sayt HTML) |
| Enerji | IEA, US EIA | https://www.iea.org , https://www.eia.gov , https://api.eia.gov/v2/ | 2 | IEA: işləyir (HTML; datanın çoxu pulludur). EIA: sayt işləyir (HTML), API pulsuz qeydiyyat və açar istəyir |
| Telekom, rəqəmsal | ITU DataHub | https://datahub.itu.int | 2 | əlçatmaz (sayt və API avtomatik sorğulara 403/202 yoxlama). ITU göstəriciləri Dünya Bankı API-də də var (məsələn, `IT.NET.USER.ZS`) |
| Əhali | UN World Population Prospects | https://population.un.org/wpp | 2 | sayt işləyir (HTML, CSV yükləmə); Data Portal API data sorğusu 401 qaytarır, yəni token lazımdır |
| Elmi ədəbiyyat | OpenAlex API | https://api.openalex.org/works?search=... | 2 | işləyir (API JSON, açarsız) |
| Elmi ədəbiyyat | Crossref API | https://api.crossref.org/works?query=... | 2 | işləyir (API JSON, açarsız) |
| Tibb | PubMed, E-utilities | https://pubmed.ncbi.nlm.nih.gov , https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ | 2 | işləyir (HTML; API JSON/XML) |
| Preprintlər | arXiv API | https://export.arxiv.org/api/query?search_query=... | 4 | işləyir (HTML; API Atom XML) |
| Patentlər | WIPO Patentscope | https://patentscope.wipo.int/search/en/search.jsf | 1 | işləyir (HTML, nəticələr qismən JavaScript-lə yüklənir) |
| Patentlər | Espacenet, EPO OPS | https://worldwide.espacenet.com , https://ops.epo.org | 1 | əlçatmaz avtomatik sorğu ilə (403); OPS API pulsuz qeydiyyat istəyir |
| Şirkətlər (ABŞ) | SEC EDGAR | https://data.sec.gov/submissions/CIK0000320193.json , https://efts.sec.gov/LATEST/search-index?q=... | 1 | işləyir (API JSON). `www.sec.gov` səhifələri əlaqə məlumatı olmayan User-Agent-ə 403 qaytarır (SEC qaydası) |
| Şirkətlər (BK) | Companies House | https://find-and-update.company-information.service.gov.uk/search/companies?q=... | 1 | işləyir (HTML); API pulsuz açar istəyir |
| Şirkətlər (qlobal) | OpenCorporates | https://opencorporates.com | 4 | qeydiyyat lazımdır: `robots.txt` `/search` və `/companies?q=` axtarışını qadağan edir, API açar istəyir (401). Avtomatik istifadə etmə |
| AB hüququ | EUR-Lex | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32001L0110 | 1 | işləyir (HTML). Ana səhifə bot yoxlaması verir (202), sənəd URL-ləri birbaşa açılır; `Crawl-delay: 10` |
| Əqli mülkiyyət hüququ | WIPO Lex | https://www.wipo.int/en/web/wipolex | 2 | işləyir (HTML) |
| Sanksiyalar | BMT, AB, OFAC siyahıları | rəsmi saytlar | 1 | yoxlanılmayıb |
| Axtarış tələbi | Google Trends | https://trends.google.com | 4 | əlçatmaz avtomatik: `robots.txt` `/trends/explore?` yolunu qadağan edir, data JavaScript-lə gəlir. İnsan brauzerdə açıb CSV ixrac edə bilər |
| Reklamlar | Meta Ad Library | https://www.facebook.com/ads/library | 3 | əlçatmaz avtomatik (403, `robots.txt` bağlıdır). API üçün Meta tərtibatçı hesabı və təsdiq lazımdır |
| Sayt reytinqi | Tranco | https://tranco-list.eu/api/ranks/domain/example.com | 4 | işləyir (API JSON) |
| Sayt reytinqi | Cloudflare Radar | https://radar.cloudflare.com | 4 | qeydiyyat lazımdır: sayt 403, API pulsuz token istəyir |
