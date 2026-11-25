# Sınaq nəticələri

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
