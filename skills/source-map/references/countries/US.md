# Amerika Birləşmiş Ştatları (US)

Yoxlanılıb: 2026-11-26, `verified-research/0.5` User-Agent-i ilə. Bir neçə federal sayt avtomatik sorğulara 403 qaytarır; onlar üçün işləyən API və ya güzgü mənbə göstərilib.

| Qurum | URL | Hansı data | Səviyyə | Status |
|---|---|---|---|---|
| Census Bureau | https://www.census.gov , https://api.census.gov | əhali, pərakəndə satış, xarici ticarət | 1 | əlçatmaz avtomatik (sayt və API 403; API pulsuz açar istəyir). Eyni seriyalar FRED və BEA-da var |
| Bureau of Labor Statistics | https://api.bls.gov/publicAPI/v2/timeseries/data/<seriya> | məşğulluq, maaş, CPI | 1 | API işləyir (JSON, açarsız gündə 25 sorğu); `www.bls.gov` 403 qaytarır |
| Bureau of Economic Analysis | https://www.bea.gov , https://apps.bea.gov/iTable/ | ÜDM, gəlir, xərc | 1 | işləyir (HTML; API pulsuz açar istəyir) |
| Federal Reserve | https://www.federalreserve.gov | faiz, kredit, ödəniş | 1 | işləyir (HTML) |
| FRED (St. Louis Fed) | https://fred.stlouisfed.org | makro seriyalar | 1 | əlçatmaz bu yoxlamada (bağlantı vaxtı bitdi); API pulsuz açar istəyir |
| SEC EDGAR | https://data.sec.gov/submissions/CIK##########.json | şirkət hesabatları | 1 | işləyir (API JSON); `www.sec.gov` səhifələri əlaqəsiz User-Agent-ə 403 |
| eCFR (federal qaydalar) | https://www.ecfr.gov , https://www.ecfr.gov/api/versioner/v1/ | qüvvədə olan federal qaydalar | 1 | işləyir (HTML, API JSON) |
| Federal Register | https://www.federalregister.gov/api/v1/documents.json | yeni qaydalar, bildirişlər | 1 | işləyir (API JSON) |
| USITC DataWeb | https://dataweb.usitc.gov | idxal, ixrac, tariflər | 1 | işləyir (HTML, qeydiyyatla yükləmə); `www.usitc.gov` 403 |
| IRS | https://www.irs.gov | vergi | 1 | işləyir (HTML) |
| Ştat şirkət reyestrləri | hər ştatın Secretary of State saytı | şirkət qeydiyyatı | 1 | yoxlanılmayıb |
