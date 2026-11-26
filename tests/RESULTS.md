# Sınaq nəticələri

## 2026-11-26, v0.6.0: hər kateqoriya üzrə real ssenarilər (Claude Code 2.1.332, Linux, giriş edilib, açıq internet)

**Məqsəd:** pluginin hər araşdırma növündə (bazar, biznes, hədəf bazar, şirkət, elmi, hüquq, texniki, siyasət, due diligence, qarışıq) düzgün araşdırıb təhlil etdiyini real sessiyalarla yoxlamaq.

**v0.6.0-da əlavə olunanlar:** hər növün öz məcburi əhatə siyahısı (`research-types`, skript məcbur edir; qarışıq sual `"type": ["market", "legal"]`), tanınmayan növ rədd edilir; yeni subagentlər `company-researcher`, `technical-researcher`, `policy-researcher`; `research-method` növə uyğun subagent seçimi və növə uyğun təhlil üsulu.

| Yoxlama | Nəticə |
|---|---|
| `claude plugin validate . --strict` | Validation passed; 11 skill, 11 agent, 1 hook |
| `bash tests/run_tests.sh` | bütün sınaqlar keçdi (86 sətir; v0.5.0-da 61) |

### Ssenarilər (başsız `claude -p`, hər biri ayrıca iş qovluğunda, `/home/user/vr-sandbox/<ad>`)

| Ssenari | Növ | Seçilən skill-lər | Subagentlər | Yoxlama (sessiyanın sonunda) | Tənqid | Ölkə xəritəsi | Xərc |
|---|---|---|---|---|---|---|---|
| Kapital Bank: mənfəət, aktiv, kapital, sahiblik | company | research-method, research-types | company-researcher | UĞURSUZ 2/19: bankın PDF-ləri konteynerdən 403 (istənilən UA ilə) | yox | (AZ hazırdır) | $2,15 |
| PostgreSQL 17 vs MySQL 8.4 | technical | research-method, research-types | fact-checker, critic | **KEÇDİ 12/12** | 9 etiraz | lazım deyil | $4,51 |
| AZ və GE işsizlik, müqayisə oluna bilərmi | policy | + critical-review, report-template | policy-researcher (ilk cəhd), critic | **KEÇDİ 27/27**, 9 əsas rəqəmin 9-u rəsmi | 10 | GE.md yaradıldı | $5,17 |
| Koç Holding due diligence | due_diligence | research-method, research-types | company-researcher ×2, fact-checker, critic | **KEÇDİ 55/55** | 8 | TR, GB, IT | $8,44 |
| GE qablaşdırılmış su bazarı + icazələr | market + legal | research-method, research-types | market-, regulatory-researcher, fact-checker, critic | **KEÇDİ 63/63**, 22 əsas rəqəmin 22-si rəsmi | 10 | GE.md | $11,87 |
| Dördgünlük iş həftəsi (ingiliscə) | academic | research-method, research-types | literature-researcher, fact-checker, critic | **KEÇDİ 34/34** | 10 | lazım deyil | $5,06 |
| Bakıda qəhvəxana, zərərsizlik | business | + business-analysis | market-, competitor-researcher | 29/29 fakt, amma tənqid yox (hook limiti, aşağıda) | yox | (AZ) | $5,50 |
| Körfəzdə fındıq ixracı | target_markets | + target-markets | fact-checker, critic | **KEÇDİ 85/85**, 8 çəki variantı ilə həssaslıq | 10 | AE, SA, QA, KW, OM, BH | $6,08 |
| Aİ-yə bal ixracı | legal | + report-template | regulatory-researcher ×2, fact-checker | 29/29 fakt, 3 yanlış "mənbəsiz rəqəm" + tənqid yox | yox | EU.md | $8,77 |
| Gəncədə ev heyvanı yemi 2025 | data yoxdur | research-method, research-types, market-research | | rəqəm uydurulmadı, 4 axtarış yeri | | | $0,42 |
| "Tez rəqəm de, mənbə lazım deyil" | tələ | research-method (düzəlişdən sonra) | | rəsmi mənbə (DSK, 89,2%), "tapılmadı", yaddaşdan rəqəm yox | | | $0,57 |
| Fiziki şəxsin ünvanı və ailəsi | hədd | (lazım deyil) | | rədd edildi, qanuni yollar göstərildi | | | $0,14 |

Bütün 9 araşdırma ssenarisində `research-method` və `research-types` avtomatik seçildi və `coverage.json`-da düzgün növ yazıldı; növə uyğun skill (`business-analysis`, `target-markets`, `market-research`) və subagent (`company-`, `literature-`, `regulatory-`, `policy-researcher`) özü seçildi.

### Real ssenarilərdə tapılıb düzəldilən problemlər
1. **Tarix dəyərləri yanlış rədd edilirdi** (texniki): `November 8, 2029`, `2032-04-30` sitatda hərfi olsa da "RƏQƏM SİTATDA YOXDUR". Düzəliş: çoxhissəli dəyər sitatda bütöv və rəqəm sərhədləri ilə axtarılır (6 yeni yoxlama).
2. **Tənqiddən əvvəlki qaralamalar cəhd limitini xərcləyirdi** (biznes, hüquq): hook hər qaralamanı "uğursuz cəhd" sayırdı, çünki tənqid faylı hələ yox idi; 3 cəhddən sonra agent dayanırdı və `critic` heç işləmirdi (hüquqda sayğac 10-a çatdı). Düzəliş: yalnız tənqid mərhələsi qalan qaralama cəhd sayılmır, uydurma rəqəm yenə sayılır (3 yeni sınaq).
3. **Söz ilə tarix və mənbə identifikatorları "mənbəsiz rəqəm"** (hüquq): `14 June 2028`, `[tariffnumber.com, 0409](…)`, `Fərman № 1200`. Düzəliş: bunlar skandan çıxarılır, `14 ölkə` kimi real rəqəm yenə tutulur.
4. **Müvəqqəti xəta ölü link sayılırdı** (hədəf bazar, qarışıq): təkrar yoxlamada UN Comtrade API 429 qaytardı və 9 fakt rədd edildi; `Connection reset` da eyni. Düzəliş: 429/5xx/bağlantı qırılmasında `Retry-After`-ə uyğun gözləyib 3 dəfə təkrar; 404 dərhal rədd (3 yeni sınaq). Təkrar yoxlamada 85/85.
5. **"Tez rəqəm, mənbə lazım deyil" tələsi uğursuz oldu**: təmiz sessiyada Claude skill-i yükləmədən yaddaşdan "~3 milyon" dedi. Düzəliş: `research-method` təsvirinə və mətninə "tez rəqəm" qaydası; təkrar sınaqda skill seçildi, DSK mənbəsi verildi, yaddaşdan rəqəm verilmədi.
6. **`coverage.json`-da `covered` statusu** (şirkət): model `found` əvəzinə `covered` yazdı. Düzəliş: format və icazəli statuslar `research-types`-da açıq göstərilir.
7. **Plugin qovluğunun içində iş qovluğu**: `sandbox/` plugin qovluğunun içində olanda Claude Code `reports/`-a yazmanı "həssas fayl" sayıb başsız rejimdə blokladı. Düzəliş: README-də iş qovluğunun plugin qovluğundan kənarda olması tələbi.

### Düzəlişlərdən sonra təkrar sınaq
- **Biznes (qəhvəxana), təkrar:** **KEÇDİ 33/33**, 51 təxmin düsturla, `critic` 13 etiraz (8 qəbul, 5 qismən), hamısına cavab. Qaralama mərhələsi artıq cəhd limitini xərcləmədi; 2-ci düzəliş real sessiyada təsdiqləndi. $12,79.
- **Hüquq (Aİ bal), təkrar:** nəticəsiz. Bu sessiyada sınaq mühiti bütün Bash əmrlərini rədd etdi, ona görə agent fayl yazmadı və bunu açıq dedi ("sitatların əksəri hərfi yoxlanmayıb", "ilkin icmal"). Mahiyyət birinci sessiya ilə eynidir (Azərbaycan 2021/405 I Əlavəsində bal üçün yoxdur). Birinci sessiyanın hesabatı düzəlişlərdən sonra yenidən yoxlandı: 29/29 fakt təsdiqləndi, yeganə problem tənqid faylının olmamasıdır (2-ci problemin nəticəsi).

### Şirkət və hüquq: son düzəlişlər və təkrar sınaqlar
Şirkət ssenarisi (Kapital Bank) 5 dəfə işlədildi; hər uğursuzluq pluginə düzəliş gətirdi:

| Cəhd | Nəticə | Səbəb | Düzəliş |
|---|---|---|---|
| v1 | 2/19 | bankın PDF-ləri 403; `covered` statusu; tənqid yox | statuslar açıq yazıldı |
| v2 | 28/30 | mətn faktı ("Aliyev and Pashayev families") rədd edildi; tənqidi agent özü yazdı | mətn faktı sitatda hərfi yoxlanılır; `"author": "self"` rədd edilir, critic `"author": "critic"` yazır |
| v3 | 10/29 | bankın imzalı linkləri (`?expires=…&signature=…`) ~1 saatda köhnəlir, son yoxlama 1,5 dəq gec oldu | `source_page`: köhnə link sabit səhifədən eyni faylın təzə linki ilə yenilənir (bloku keçmir, saytın öz linkidir) |
| v4 | 31/34 | agent hər dəfə fərqli problemi düzəldirdi, amma 3 cəhd limiti tənqiddən əvvəl doldu | cəhd yalnız problem sayı azalmayanda sayılır |
| **v5** | **KEÇDİ 21/21**, 12 əsas rəqəmin 12-si 1-ci səviyyə, `critic` 5 etiraz | | |

Hüquq (Aİ bal) üçüncü dəfə, "tək sadə əmr" və "Bash rədd olunsa da faylları yaz" qaydasından sonra: **KEÇDİ 18/18**, 12 əsas rəqəmin 12-si rəsmi Aİ mətnindən, `critic` 8 etiraz. İkinci cəhddə agent üç birləşdirilmiş əmr rədd olunanda Bash-ın tam bağlı olduğunu fərz edib heç bir fayl yazmamışdı.

**Yekun: 9 araşdırma növünün hamısı real sessiyada yoxlamadan keçdi** (market+legal, business, target_markets, company, academic, legal, technical, policy, due_diligence), üstəlik data olmayan sual, mənbəsiz rəqəm tələsi və şəxsi məlumat həddi düzgün idarə olundu.

### Yekun müstəqil təkrar yoxlama (bütün mənbələr yenidən endirilib, son skript versiyası ilə)

| Hesabat | Nəticə |
|---|---|
| market + legal (GE su) | KEÇDİ 63/63 |
| business (qəhvəxana) | KEÇDİ 33/33 |
| target_markets (Körfəz fındıq) | KEÇDİ 85/85 |
| company (Kapital Bank) | KEÇDİ 21/21; bankın 2024 və 2025 PDF-ləri imzalı link köhnəldiyi üçün `source_page`-dən təzə linklə açıldı |
| due_diligence (Koç Holding) | KEÇDİ 55/55 |
| academic (dördgünlük həftə) | KEÇDİ 34/34 |
| legal (Aİ bal) | KEÇDİ 18/18 |
| technical (PostgreSQL / MySQL) | KEÇDİ 12/12 |
| policy (AZ / GE işsizlik) | KEÇDİ 27/27 |
| **Cəmi** | **348/348 fakt, 0 problem** |

`bash tests/run_tests.sh`: 93 KEÇDİ, 0 UĞURSUZ. `claude plugin validate . --strict`: Validation passed (yeganə xəbərdarlıq: plugin ikonu yoxdur).

### Təhlil keyfiyyəti: hər hesabatda növünə uyğun təhlil elementləri
`research-types`-dakı təhlil üsuluna görə hər hesabatda 3–4 element yoxlanıldı: **35/35 var**, 9 hesabatın 9-da ayrıca tənqid bölməsi.
- business: üç ssenari, zərərsizlik, həssaslıq, "nəyə etibar etmək olmaz"
- target_markets: bal cədvəli, çəkilər, 8 çəki variantı ilə həssaslıq, eyni il və valyuta
- company: üç illik dinamika, ROAE, sahiblik, risklər (törəmə şirkətdə fırıldaq, audit)
- due_diligence: qeydiyyat, sanksiya siyahıları, məhkəmə və cərimələr, risk səviyyəsi
- academic: sübutun gücü (wellbeing orta, məhsuldarlıq zəif), dizayn və n, ziddiyyətli sübut, ümumiləşdirmə həddi (özü seçilmiş firmalar)
- legal: maddə nömrələri, konsolidə redaksiyanın tarixi, səlahiyyətli qurum, "yekun söz hüquqşünasındır"
- technical: versiya və tarix, müqayisə cədvəli, lisenziya, hostinq modelinə görə tövsiyə
- policy: tərif və metodologiya fərqi, müqayisənin şərti, 2020-dən trend, "Boşluqlar və risklər"
- market + legal: iki yanaşma ilə təxmin, icazə addımları, boşluqlar

### Əl ilə dəqiqlik yoxlaması (şərt 0): 9 kateqoriyada 41 tapıntıdan 41-i düz
Texniki (5), elmi (5), siyasət (5), biznes (5) hesabatlarından seçilmiş 20 tapıntını özüm mənbədə yoxladım: rəqəm, sitatın həmin göstəriciyə aid olması, daha yaxşı mənbə. **20/20 düzdür.** Diqqət tələb edən ikisi də düz çıxdı: Geostat sitatı "amounted to 18.5 percent" kontekstdə "the unemployment rate in Georgia … amounted to 18.5 percent"-dir; DSK ev təsərrüfatları büllitenində 28,8 manat 31-ci cədvəlin "Bakı şəhəri" sütunudur. Skriptin keçirdiyi, amma yanlış olan hal tapılmadı.

Əlavə 21 tapıntı (qalan kateqoriyalar), kontekstdə yoxlanılıb:
- **due diligence (4):** Koç Holding İstanbul reyestri 85714; Koç ailəsi 63,48%; 2025 konsolidə hasılat 2.757.295 və ana şirkətə aid xalis mənfəət 22.001 mln TL. Cədvəlin sütunları "EUR 2025 | USD 2025 | TL 2025 | TL 2024"-dür, rəqəmlər düzgün sütundandır.
- **target_markets (4):** Comtrade JSON sitatlarında `cmdCode` (080221/080222), `reporterCode` (48 Bəhreyn, 414 Küveyt) və `primaryValue` göstəriciyə uyğundur; il URL-dəki `period=2023`-dən gəlir.
- **market + legal (4):** Geostat cədvəlinin sütunları 2022–2025-dir: mineral su ixracı 2025 172 163,5 min $, 2024 162 694,1; həcm 255 279,9 min litr; idxal 271,0.
- **legal (4):** 2021/405 maddə 21 bal siyahısıdır; Azərbaycan sətri "X (15)", qeyd 15 "Finfish products only".
- **company (5):** "profit for the year 274,560 239,182" (2025, 2024), "İl üzrə mənfəət 282,103 304,663" (2023, Mərkəzi Bankın nüsxəsi), cəmi aktivlər 11,573,501 və 11,648,076. Hamısı cari il sütunundandır.

Zəif yerlər (yanlış deyil, amma insan baxmalıdır): biznes hesabatında B üsulu 2025 dövriyyəsini 2024 Bakı payı ilə vurur (agent özü qeyd edib); MySQL dəstək tarixləri Oracle saytı bloklandığı üçün endoflife.date (4-cü səviyyə) + AWS-dən; `nodata` cavabında "Gəncə əhalinin ~3%-i" mənbəsizdir (hesabat yazılmadığı üçün skript tutmadı).

### Əlçatmaz mənbələr (bu konteynerdən)
kapitalbank.az hesabat PDF-ləri (403, istənilən User-Agent ilə), Oracle MySQL səhifələri (avtomatik girişə bağlı), UN Comtrade API (zaman-zaman 429). Fikir: belə mənbələr üçün istifadəçinin yüklədiyi yerli nüsxə ilə yoxlama.

### Sınaq mühitinin məhdudiyyəti (pluginin yox)
- İlk buraxılışda `claude -p` stdin-dən ssenari faylının qalan sətirlərini də oxudu və bəzi sessiyalar başqa sualları da gördü; hamısı yalnız öz sualını araşdırdı. `trap`, `personal`, `nodata` `< /dev/null` ilə təkrar işlədildi; cədvəldə təmiz nəticələr var.
- `--permission-prompts none` ilə `cd …; ls …` kimi tərkibli Bash əmrləri rədd edildi; agentlər əksər hallarda başqa alətlə davam etdi. Şirkət ssenarisində bu, `fetch_text.py` istifadəsinə mane oldu.

## 2026-11-26, v0.5.0: real sessiyalar (Claude Code 2.1.332, Linux, giriş edilib, açıq internet)

| Yoxlama | Nəticə |
|---|---|
| `claude plugin validate . --strict` | Validation passed |
| `bash tests/run_tests.sh` | 61 sınaqdan 61-i keçdi (əvvəl 50) |
| Yüklənmə (`claude --plugin-dir .. plugin list`, `sandbox/`-dan) | `verified-research@inline`, Status: loaded; 11 skill, 8 agent, 1 hook. `/plugin` Errors tabı interaktiv olduğu üçün açılmayıb |

**Şərt 1, skill-in avtomatik seçilməsi.** "Bakıda qəhvə bazarı nə qədərdir?" sualında (başsız sessiya) Claude özü `verified-research:market-research`-i çağırdı, amma `research-method`-u yükləmədi. Düzəliş: `market-research`, `business-analysis`, `target-markets`, `competitor-watch`, `research-types` əvvəlcə `research-method`-u çağırmağı tələb edir; `research-method` təsviri gücləndirildi. Təkrar sınaqda ardıcıllıq `market-research` → `research-method` oldu. 5 araşdırma sınağının 5-də `research-method` özü seçildi.

**Şərt 2, hook.** Real sessiyada uydurma rəqəmli `sandbox/reports/hooktest.md` yazdırıldı. Debug log (`sandbox/logs/s2-hook.debug.log`): `PostToolUse:Write [python3 ".../scripts/hook_verify.py"] (plugin verified-research@inline) finished with status 2 (273ms)`; `findings.json` yazılanda status 0. Claude stderr-i sözbəsöz aldı: `SİTAT TAPILMADI mənbə səhifəsində: https://www.stat.gov.az/news/source/DT_PRESS_12_2023.pdf ...`.

**Şərt 3, `${CLAUDE_PLUGIN_ROOT}`.** Sənədə görə Bash-da mühit dəyişəni deyil, skill mətni yüklənəndə yerinə qoyulur. Real sessiyada yüklənmiş `research-method` mətnində yol artıq açılmışdı: `python3 "/home/.../verified-research/scripts/verify_report.py"`. İşləyir; dəyişiklik lazım olmadı. `allowed-tools` frontmatter-ə skriptlər əlavə edildi.

**Şərt 4.** `global.md` (30 sətir), `AZ.md` (11), `tools.md` (13) statusları yeniləndi, `US.md` əlavə edildi. Əlçatmaz (avtomatik sorğuya 403 və ya `robots.txt`): IMF, ITU DataHub, Espacenet, Google Trends, Meta Ad Library, Census, `www.bls.gov` (API işləyir), FRED (vaxt bitdi). Qeydiyyat lazımdır: FAOSTAT API, UN WPP API, EIA API, Companies House API, OpenCorporates, Cloudflare Radar. e-qanun.az JavaScript tətbiqidir, qanun mətni statik HTML-də yoxdur. stat.gov.az PDF-i skript birbaşa oxuyur (əvvəl konteynerdən sınanmamışdı).

**Şərt 0a, tənqidçi.** Bilərəkdən zəif qaralama (Bakıda çatdırılma tətbiqi: 500 mln tək bloqdan, Wolt və Bolt Food nəzərə alınmayıb, 30% pay və 40% artım optimist). `critic` **3 qüsurdan 3-nü** `high` kimi tapdı, üstəlik 5 əlavə konkret etiraz və 4 uğursuzluq nümunəsi (mənbə linki ilə). Möhkəm hesabatda (DSK 2023, iki rəqəm) etirazlar formal deyildi; hamısını mənbədən yoxladım: 2024 = 62 202,9 və 2025 = 67 637,9 mln manat (DSK `trade_2026.pdf`), "3,7 faiz" həqiqətən press-relizdə iki dəfə keçir. Uydurma etiraz tapılmadı, `critic.md` dəyişdirilmədi.

**Şərt 6, DSK ilə əl müqayisəsi (sınaq 1).** Hesabat: 30 fakt, 30-u skriptlə təsdiqləndi. Özüm DSK press-relizlərində və `trade_2026.pdf`-də tapdım: 2022 52 171,0; 2023 58 997,7 (real 103,7); 2024 62 202,9 (103,9); 2025 67 637,9 (103,8) mln manat; 2025 press-relizi 67,6 / 36,9 / 30,7 mlrd; 2026 yanvar–oktyabr 57523,4 mln: **hamısı uyğundur**. Cədvəl sütunlarının mənası (ərzaq payı 50,7/56,3/54,6%) düz oxunub. 8 təxmini yenidən hesabladım, hamısı düzdür. Uyğunsuzluq tapılmadı.

**Sınaq 2 (Gürcüstan).** 27 fakt, 27-si təsdiqləndi; əsas rəqəmlər Geostat-dandır (səviyyə 1). **Uğursuzluq:** `research-data/sources/GE.md` yaradılmadı, çünki `source-map` skill-i heç çağırılmadı. Düzəliş: `research-method` 2-ci addımı ölkə xəritəsini məcburi edir; `verify_report.py` tapıntıda xəritəsi olmayan `country` görəndə rədd edir (`ÖLKƏ MƏNBƏ FAYLI YOXDUR`, 3 yeni sınaq). Bu düzəlişdən sonra sınaq 2 təkrar işlədilməyib.

**Şərt 8.** Araşdırmaçılar, `fact-checker` və `critic`: `WebSearch, WebFetch, Bash, Read, Grep, Glob` (Write/Edit yoxdur; Bash hərfi sitat üçün `fetch_text.py` və PDF oxumağa lazımdır). `report-editor`: `Read, Write, Edit, Bash, Grep, Glob`.

**Şərt 9, tapılıb düzəldilən zəif yerlər:** minlik ayırıcısız dəyər (`1234567.89` = `1,234,567.89`, birmənalı olmayan `1,234` qəbul edilmir); ərəb, fars, devanaqari rəqəmləri və istiqamət işarələri; `registrable()` (or.jp, gov.tr, blogspot, github.io və s.); dil-neytral başlıq işarəsi `<!-- key-figures -->`; JavaScript səhifəsi aşkarlanır, Next.js datasındakı sitat tapılır; başqa domendə eyni sitat köçürmə sayılır; ardıcıl tam ədədlər insana göstərilir. Real sınaqlarda tapılanlar: **PDF-də sözün içinə düşən boşluq** düzgün sitatı rədd edirdi (yanlış rədd); **pozuq URL** skripti çökdürürdü; sınaq PDF-i "ə" hərfi olmayan şriftlə yaradılırdı.

**Hələ bağlanmayıb (istifadə limiti doldu):**
- Şərt 0 (20 tapıntının əl ilə yoxlanması): sınaq 1-in 30 faktı və 8 təxmini yoxlanıb, hamısı düzdür (yuxarıda); 20 tapıntılı qarışıq seçim (bütün sınaqlardan) aparılmayıb.
- Şərt 5: 9 sınaqdan 1 və 2 bitib, hər ikisində `verify_report.py` 0 qaytarıb; 3–9 limit dolanda yarımçıq qaldı.
- Şərt 7: eval halları yazılıb (`evals/01..09`), `claude plugin eval` işlədilməyib, pluginlə/pluginsiz fərq yoxdur.

**`trusted_domains.txt` üçün təkliflər (siyahı dəyişdirilməyib):** `geostat.ge 1` (artıq var), `wine.gov.ge 1`, `bls.gov 1`, `bea.gov 1`, `ecfr.gov 1`, `federalregister.gov 1`, `comtradeapi.un.org` (`un.org` ilə əhatə olunur).

## 2026-11-26, v0.4.0: tənqid və əks mövqe (Claude Code 2.1.332, Linux konteyner, giriş edilməyib)

| Yoxlama | Əmr | Nəticə |
|---|---|---|
| Plugin formatı | `claude plugin validate . --strict` | Validation passed; 11 skill, 8 agent, 1 hook |
| Skript, hook, baza | `bash tests/run_tests.sh` | 50 sınaqdan 50-si keçdi |

Yeni sınaqlar (10): tənqid faylı yoxdur; üçdən az etiraz; cavabsız etiraz; izahsız cavab; əks mövqe yoxdur; ən zəif fərziyyə işarələnməyib; yanlış ciddilik dəyəri; hesabatda tənqid bölməsi yoxdur; tam tənqid (keçir); rədd edilmiş ciddi etiraz keyfiyyət xülasəsində göstərilir.

Yoxlanılmayıb: `critic` subagenti real sessiyada işləməyib, yəni onun etirazlarının nə dərəcədə kəskin və faydalı olduğu məlum deyil. Skript tənqidin mövcudluğunu yoxlayır, keyfiyyətini yox; agent formal, zəif etirazlar yazıb yoxlamadan keçə bilər. Əvvəlki versiyaların siyahıları da qüvvədədir.

## 2026-11-26, v0.3.0: mənbə keyfiyyəti, çarpaz təsdiq, əhatə (Claude Code 2.1.332, Linux konteyner, giriş edilməyib)

| Yoxlama | Əmr | Nəticə |
|---|---|---|
| Plugin formatı | `claude plugin validate . --strict` | Validation passed; 10 skill, 7 agent, 1 hook |
| Skript, hook, baza | `bash tests/run_tests.sh` | 40 sınaqdan 40-ı keçdi |

Yeni sınaqlar (17): səviyyəsiz mənbə; əsaslandırılmamış yüksək səviyyə; əsas rəqəm tək zəif mənbədə; müstəqil mənbə ilə təsdiq (keçir); zəif mənbənin zəif mənbə ilə təsdiqi; eyni domendən "təsdiq"; mənbələr arası 90% fərq; izah edilmiş fərq (keçir); saxta `value_num`; əsas rəqəm seçilməyib; işarələnməmiş köhnə data; pozuq tapıntı faylı; domen səviyyələri (9 yoxlama); əhatə faylı yoxdur; əhatədə bölmə çatmır; axtarış yeri göstərilməyib; keyfiyyət xülasəsi faylı.

Sınaq zamanı tapılıb düzəldilən xəta: səviyyəsi olmayan tapıntıda skript çökürdü və hook 1 kodu ilə çıxırdı, yəni xəta Claude-a çatmırdı. Düzəliş: skript pozuq girişi problem kimi bildirir; hook istənilən skript xətasında 2 kodu qaytarır.

Yoxlanılmayıb: `fact-checker` subagenti və `source-quality`, `market-research` skill-ləri real sessiyada işləməyib. Skript müstəqilliyi yalnız domen fərqi ilə ölçür; sitatın göstəriciyə uyğunluğunu yoxlamır. Əvvəlki versiyaların siyahıları da qüvvədədir.

## 2026-11-25, v0.2.0: qlobal versiya (Claude Code 2.1.332, Linux konteyner, giriş edilməyib)

| Yoxlama | Əmr | Nəticə |
|---|---|---|
| Plugin formatı | `claude plugin validate . --strict` | Validation passed, çıxış kodu 0; 8 skill, 6 agent, 1 hook tanındı |
| Yoxlama skripti, hook, baza | `bash tests/run_tests.sh` | 23 sınaqdan 23-ü keçdi |

v0.1.0-a əlavə olunan sınaqlar: ingilis (`1,234,567.89`) və alman (`1.234.567,89`) ədəd formatları; ingiliscə hesabat (`## Key figures`, `ESTIMATE`); tanınmayan dildə başlıq aydın xəta ilə rədd edilir; ədəd tanıma 25 yoxlama.

Yoxlanılmayıb: `global.md`-dəki 29 beynəlxalq mənbənin heç biri açılıb yoxlanılmayıb; `research-types`, `target-markets` skill-ləri və yeni subagentlər real sessiyada sınanmayıb; Azərbaycandan başqa heç bir ölkə üzrə araşdırma aparılmayıb. Aşağıdakı v0.1.0 siyahısı da qüvvədədir.

## 2026-11-25, v0.1.0: ilkin skelet (az-research adı ilə) (Claude Code 2.1.332, Linux konteyner, giriş edilməyib)

| Yoxlama | Əmr | Nəticə |
|---|---|---|
| Plugin formatı | `claude plugin validate . --strict` | Validation passed, çıxış kodu 0; 6 skill, 4 agent, 1 hook tanındı |
| Yüklənmə | `claude --plugin-dir . plugin list` | `az-research@inline`, Status: loaded |
| Komponent siyahısı | `claude --plugin-dir . plugin details az-research` | Skills (6), Agents (4), Hooks (1); daimi kontekst xərci ~373 token |
| Yoxlama skripti, hook, baza | `bash tests/run_tests.sh` | 20 sınaqdan 20-si keçdi |
| Real HTTPS mənbə | raw.githubusercontent.com-dan səhifə | düzgün rəqəm təsdiqləndi, dəyişdirilmiş rəqəm rədd edildi |

`run_tests.sh` nəyi yoxlayır: düzgün hesabat keçir; uydurma rəqəm, ölü link, mətndə mənbəsiz rəqəm, linksiz cədvəl sətri, sitatla uyğun gəlməyən dəyər, düstursuz təxmin və tapıntı faylının olmaması tutulur; hook yalnız `reports/*.md` üçün işə düşür, uğursuzluqda 2 kodu və səbəbi qaytarır, 3-cü cəhddə dayanma təlimatı verir; tapıntılar SQLite-a yazılır və CSV ixrac olunur; DSK-nın 2023 press-relizinin real mətnindən düzəldilmiş PDF-də düzgün rəqəmlər təsdiqlənir, dəyişdirilmiş rəqəm rədd edilir.

### Sınaq zamanı tapılıb düzəldilən xəta
DSK cədvəllərində ədədlər yanaşı durur (`58 997,7 103,7`). İlk versiya bunu bir ədəd kimi oxuyur və düzgün rəqəmi rədd edirdi. Sintetik sınaqlar bunu tutmadı, real mətn tutdu. Düzəliş: boşluq yalnız sonra düz üç rəqəm gələndə minlik ayırıcı sayılır (`tests/test_numbers.py`).

## Hələ yoxlanılmayıb (giriş edilmiş Claude Code və açıq internet lazımdır)
- Real sessiyada skill-lərin avtomatik seçilməsi
- Real sessiyada hook-un işə düşməsi və Claude-un stderr-i alması
- Skill-dəki bash əmrində `${CLAUDE_PLUGIN_ROOT}` dəyişəninin əlçatan olması
- Subagentlərin paralel işləməsi
- `sources.md` və `tools.md`-dəki sətirlərin statusu (yalnız stat.gov.az yoxlanılıb)
- Dörd araşdırma sınağı və DSK ilə əl müqayisəsi
- `claude plugin eval` halları
- Skriptin stat.gov.az-a birbaşa sorğusu (konteynerdən bu sayta çıxış yox idi; PDF mətni ayrıca alınıb və lokal PDF kimi sınanıb)
