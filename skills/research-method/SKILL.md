---
name: research-method
description: Use FIRST for any question that asks for facts or figures from external sources (for example "how big is the X market in Baku?", "how has Y changed?"), in any country, language or field (market, business, academic, regulatory, technical, financial, policy). Also use when the user wants "just a quick number" or says no source is needed: never give a statistic from memory, find it in a source first. Requires a source and a verbatim quote for every figure and machine-verifies the report.
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_text.py" *), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verify_report.py" *), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/save_findings.py" *)
---

# Araşdırma metodu

İstənilən ölkə, dil və mövzu üçün. Hesabatı istifadəçinin sual verdiyi dildə yaz.

## Tez rəqəm istəyəndə
İstifadəçi "tez bir rəqəm de, mənbə lazım deyil" desə də, rəqəmi yaddaşdan vermə. Qısa yol: bir-iki ilkin mənbədə rəqəmi tap, `fetch_text.py` ilə sitatı yoxla və cavabı bir-iki cümlə ilə ver, mənbə linki ilə. Tam hesabat, tənqid və əhatə faylı lazım deyil. Rəqəm tapılmırsa, "tapılmadı" de və ən yaxın mənbəli göstəricini göstər; təxmin verirsənsə, onu açıq "TƏXMİN" kimi, düsturu və mənbəli girişləri ilə ver.

## Addımlar
1. Araşdırma növünü müəyyən et (`research-types` skill-ini çağır) və sualı alt suallara böl. Coğrafiyanı və dövrü dəqiqləşdir. **Əhatə siyahısını yaz** (`reports/<ad>.coverage.json`): `"type"` növün adıdır (`market`, `business`, `target_markets`, `company`, `academic`, `legal`, `technical`, `policy`, `due_diligence`, `other`) və ya qarışıq sualda siyahısı (`["market", "legal"]`); `items`-də həmin növün `research-types`-dakı bütün məcburi bölmələri olmalıdır (bazar üçün `market-research`-dəki on iki). `other` üçün ən azı üç alt sual.
2. **Ölkə mənbə xəritəsi (məcburi).** Sual bir və ya bir neçə ölkəyə aiddirsə, hər ölkə üçün ISO2 kodunu müəyyən et və xəritəni oxu: əvvəlcə `${CLAUDE_PLUGIN_ROOT}/skills/source-map/references/countries/<ISO2>.md`, sonra iş qovluğunda `research-data/sources/<ISO2>.md`. **İkisi də yoxdursa, araşdırmadan əvvəl `research-data/sources/<ISO2>.md` faylını yarat**: `source-map` skill-indəki 8 bəndlik siyahı üzrə (statistika qurumu, mərkəzi bank, gömrük, reyestr, qanunvericilik bazası, vergi və tənzimləyicilər, birja, elan saytları), hər biri üçün rəsmi URL, data formatı (HTML/PDF/API) və status. Hər fakt tapıntısına `"country": "<ISO2>"` yaz; yoxlama skripti xəritəsi olmayan ölkəni rədd edir. Sonra hər alt sual üçün əvvəlcə xəritədəki və `${CLAUDE_PLUGIN_ROOT}/skills/source-map/references/global.md`-dəki ilkin mənbələrə bax, sonra ümumi veb axtarış. Alət seçimi üçün `research-tools`.
3. Yerli mənbələri yerli dildə axtar (məsələn, Türkiyə üçün türkcə, Almaniya üçün almanca). İngiliscə xülasələr çox vaxt natamam və gecikmiş olur.
4. Hər mənbəni `source-quality` ilə qiymətləndir. Hər rəqəm üçün tapıntı qeyd et: göstərici, dəyər, vahid, valyuta, dövr, ölkə, mənbə URL-i, **mənbədəki hərfi sitat**, baxış tarixi.
5. Nəticənin söykəndiyi rəqəmlərə `"key": true` yaz. Əsas rəqəm 1–2 səviyyəli mənbədən deyilsə, başqa domendə müstəqil ikinci mənbə tap (`corroboration`). Fərq 10%-dən çoxdursa, səbəbini tap (fərqli tərif, dövr, valyuta, metod), `discrepancy_note` yaz və hər iki rəqəmi göstər.
6. Etibarlılıq: yüksək (ilkin rəsmi mənbə və ya resenziyalı nəşr), orta (beynəlxalq təşkilat, iki uyğun ikinci dərəcəli mənbə), aşağı (tək ikinci dərəcəli mənbə, media, təxmini alətlər).
7. Data yoxdursa "tapılmadı" yaz və harada axtardığını göstər. **Rəqəm uydurma.**
8. Hesablama və ya təxmin varsa, tapıntıda `"type": "estimate"` yaz, düsturu və giriş rəqəmlərini göstər. Hesablamanı kodla apar.
9. Ölkələr arası müqayisədə valyutanı, ili və tərifi eyniləşdir; çevirmə məzənnəsinin mənbəyini və tarixini tapıntı kimi qeyd et.
10. Hesabatı yazmazdan əvvəl `verified-research:fact-checker` subagentinə bütün əsas tapıntıları yoxlat; `düzəliş lazımdır` və `rədd` hökmlərini həll et.
11. Qaralama hazır olanda `critical-review` skill-ini izlə: `verified-research:critic` nəticəni sındırmağa çalışır, sən hər etiraza yazılı cavab verirsən (`reports/<ad>.critique.json`).
12. Böyük və ya qarışıq suallarda alt sualları subagentlərə **paralel** ver (bir mesajda bir neçə `Agent` çağırışı), növə uyğun: `verified-research:market-researcher`, `competitor-researcher`, `customer-researcher` (bazar, biznes), `literature-researcher` (elmi), `regulatory-researcher` (hüquq), `company-researcher` (şirkət, due diligence), `technical-researcher` (texniki), `policy-researcher` (siyasət). Hər subagentə ölkəni, dövrü, alt sualı və `research-types`-dakı həmin bölmələri ver. Yekunu `verified-research:report-editor` yığır.
13. Hesabatın "Təhlil" bölməsini `research-types`-dakı növə uyğun təhlil üsulu ilə yaz; faktlar, təhlil və tövsiyələr ayrı bölmələrdə.

## Alətlər və icazələr
- Skriptləri **tək, sadə əmr** kimi çağır, tam yolla: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_text.py" "<URL>" --grep "<söz>"`. `cd`, `;`, `&&`, boru (`|`) və `for` dövrləri ilə birləşdirmə: məhdud icazəli sessiyalarda belə əmrlər rədd edilir, sadə əmr isə icazə siyahısına düşür.
- Bir Bash əmri rədd edilsə, Bash-ın tamamilə bağlı olduğunu fərz etmə: eyni skripti sadə formada yenidən çağır.
- Skriptlər işləməsə belə `findings.json`, `coverage.json` və hesabatı **yenə yaz** (Write aləti ayrıdır) və hesabatda yoxlamanın işləmədiyini açıq qeyd et. Faylsız cavab vermə.
- Mənbə avtomatik girişi bloklayırsa (403, robots.txt), bloku keçməyə çalışma (User-Agent, Referer dəyişmək və s.). Həmin sənədin başqa **rəsmi** nüsxəsini tap: tənzimləyicinin saytı (mərkəzi bankın bank hesabatları), birjanın açıqlama sistemi, rəsmi reyestr, rəsmi qəzet. Tapılmırsa, faktı `not_found` və ya "avtomatik yoxlanmayıb" kimi göstər.

## Mənbə keyfiyyəti sıralaması
Eyni fakt üçün həmişə ən yuxarı səviyyəni seç:
1. İlkin rəsmi mənbə: statistika qurumu, mərkəzi bank, gömrük, tənzimləyici, qanun mətni, məhkəmə qərarı, şirkətin rəsmi hesabatı (illik hesabat, birja bəyanatı)
2. Beynəlxalq təşkilat (Dünya Bankı, IMF, OECD, BMT qurumları) və resenziyalı elmi nəşr
3. Şirkətin öz açıqlaması (sayt, press-reliz, qiymət siyahısı)
4. Tanınmış araşdırma şirkəti, preprint, sahə assosiasiyası
5. Nüfuzlu media
6. Bloq, forum, sosial media (yalnız rəy kimi, rəqəm mənbəyi kimi yox)

2 ildən köhnə rəqəmi "köhnə" kimi işarələ. Mənbəsi göstərilməyən rəqəmi istifadə etmə, ilkin mənbəni tap.

## Çıxış faylları
İş qovluğunda (plugin qovluğunda yox):
- `reports/<tarix>-<mövzu>.md`: hesabat, `report-template` skill-inə uyğun.
- `reports/<tarix>-<mövzu>.coverage.json`: əhatə siyahısı (`market-research`).
- `reports/<tarix>-<mövzu>.critique.json`: tənqid və cavablar (`critical-review`).
- `reports/<tarix>-<mövzu>.findings.json`: tapıntılar. Format:

```json
[
  {"indicator": "Pərakəndə ticarət dövriyyəsi", "value": "58 997,7", "value_num": 58997700000,
   "unit": "mln manat", "country": "AZ", "period": "2023", "key": true,
   "source_url": "https://www.stat.gov.az/news/source/DT_PRESS_12_2023.pdf",
   "quote": "Pərakəndə ticarət dövriyyəsi 58 997,7 103,7",
   "source_tier": 1, "accessed": "2026-11-26", "confidence": "yüksək", "type": "fact",
   "stale_note": "2024 və 2025 illik rəqəmləri də götürülüb; bu sətir müqayisə ili üçündür"},
  {"indicator": "Onlayn satışın payı", "value": "7", "value_num": 7, "unit": "%", "period": "2025",
   "key": true, "source_url": "https://example-research.com/report", "quote": "...",
   "source_tier": 4, "type": "fact",
   "corroboration": [
     {"source_url": "https://example-agency.gov.xx/stat", "quote": "...", "value": "6,8",
      "value_num": 6.8, "source_tier": 1}
   ]},
  {"indicator": "Adambaşına illik xərc", "value": "5 810", "unit": "manat",
   "type": "estimate", "formula": "484,2 × 12", "inputs": ["484,2", "12"]}
]
```

Sahələr: `source_tier` hər fakt üçün məcburidir; `key` nəticənin söykəndiyi rəqəmlər üçün; `value_num` əsas rəqəmlər və təsdiq mənbələri üçün (eyni vahidə çevrilmiş ədəd); `tier_reason`, `stale_note`, `discrepancy_note` skript tələb edəndə. Ətraflı: `source-quality`.

**Əvvəlcə findings.json, sonra hesabatı yaz.**

Sitat qaydaları:
- Sitatı mənbədən **köçür**, yaddaşdan yazma və tərcümə etmə. Yoxlama skripti onu səhifədə hərfi axtarır, ona görə sitat mənbənin dilində qalır.
- Sitatı `WebFetch`-in xülasəsindən götürmə. Mətni yoxlama skriptinin gördüyü kimi al:
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_text.py" "<URL>" --grep "<açar söz>"` (HTML, PDF və JSON üçün).
- `value` sahəsini **mənbədə yazıldığı kimi** yaz: `1,234,567.89` (ingilis), `1.234.567,89` (alman, türk), `58 997,7` (Azərbaycan, rus). Hesabat mətnində də eyni yazılışı işlət.
- Rəqəm sitatın içində olmalıdır. Cədvəl sətri də sitat ola bilər.
- PDF-dən sitat götürəndə çıxarılmış mətndən götür: sətir sonu defisləri itə bilər.
- JavaScript ilə yüklənən səhifədə sitat tapılmaya bilər; statik səhifə, PDF və ya API variantını axtar.

## Yoxlama
Hesabatı yazdıqdan sonra işə sal:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/verify_report.py" reports/<fayl>.md
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/save_findings.py" reports/<fayl>.findings.json
```

Skript `reports/<fayl>.quality.md` yaradır: mənbə səviyyələri, təsdiqlənmiş əsas rəqəmlər, əhatə, insanın baxmalı olduğu yerlər. Hesabatın sonunda ona keçid ver; məzmununu özün yazma və dəyişmə.

Yoxlama keçməyən rəqəmi düzəlt və ya hesabatdan çıxar. Eyni hesabat 3 dəfə uğursuz olsa, dayan və uğursuz rəqəmləri istifadəçiyə göstər.
