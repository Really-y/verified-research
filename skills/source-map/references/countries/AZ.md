# Azərbaycan (AZ)

Yoxlanılıb: 2026-11-26, `verified-research/0.4` User-Agent-i ilə; `robots.txt` hər birində oxunub (heç biri istifadə olunan yolları qadağan etmir).

| Qurum | URL | Hansı data | Səviyyə | Status |
|---|---|---|---|---|
| Dövlət Statistika Komitəsi | https://www.stat.gov.az | əhali, gəlir, ticarət, sektorlar | 1 | işləyir (2026-11-26, PDF və HTML): aylıq press-relizlər PDF-dir, `/news/source/DT_PRESS_AA_İİİİ.pdf` və `PRESS_İİİİ_AA_dt.pdf`; `verify_report.py` PDF-i birbaşa yükləyib mətnini çıxarır (sınanıb: `DT_PRESS_12_2023.pdf`). Bölmələr üzrə illik cədvəllər: `/source/<bölmə>/` (məsələn `/source/trade/`) |
| Mərkəzi Bank | https://www.cbar.az | kredit, depozit, ödəniş, məzənnə | 1 | işləyir (HTML; rəsmi məzənnə XML: `https://www.cbar.az/currencies/GG.AA.İİİİ.xml`) |
| Dövlət Gömrük Komitəsi | https://customs.gov.az | idxal, ixrac | 1 | işləyir (HTML): `https://customs.gov.az/az/faydali/gomruk-statistikasi/xarici-ticaretin-veziyyeti-haqqinda` |
| İqtisadiyyat Nazirliyi | https://economy.gov.az/az | siyasət, sektor proqramları | 1 | işləyir (HTML) |
| KOBİA | https://smb.gov.az/az | kiçik və orta biznes | 1 | işləyir (HTML) |
| AZPROMO | https://azpromo.az/az/ | ixrac, investisiya | 1 | işləyir (HTML) |
| Qanunvericilik bazası | https://e-qanun.az | qanunlar, qərarlar | 1 | qismən: sayt JavaScript tətbiqidir, sənəd səhifəsində (`/framework/<id>`) qanunun mətni statik HTML-də yoxdur, yəni `verify_report.py` sitatı tapa bilmir. Qanun mətnini sitat kimi istifadə etmək üçün rəsmi nəşrin PDF-ini və ya Milli Məclisin saytındakı mətni axtar |
| Vergi orqanı | https://www.taxes.gov.az/az | vergi, kommersiya reyestri | 1 | işləyir (HTML) |
| tap.az | https://tap.az | qiymət, təklif həcmi | 6 | işləyir (HTML; `robots.txt` elan səhifələrinə icazə verir) |
| boss.az | https://boss.az | iş elanları, maaşlar | 6 | işləyir (HTML) |
| lalafo.az | https://lalafo.az | qiymət, təklif həcmi | 6 | işləyir (HTML, server tərəfində render olunur; `robots.txt` `/ajax/` və `/api/` yollarını qadağan edir) |
