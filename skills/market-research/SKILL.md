---
name: market-research
description: Use for any full market study of a product, sector or country market. Enforces a twelve-part coverage checklist so no part of the market is silently skipped. Always used together with research-method.
---

# Tam bazar araşdırması

> **Əvvəlcə `research-method`.** Bu skill təkbaşına işləmir: tapıntı formatı, hərfi sitat qaydası, fayl adları və avtomatik yoxlama `verified-research:research-method`-dadır. O, bu sessiyada hələ yüklənməyibsə, indi `Skill` aləti ilə onu çağır, sonra buraya qayıt.

Bazar araşdırması on iki bölmənin hamısını əhatə etməlidir. Araşdırmadan **əvvəl** `reports/<ad>.coverage.json` yarat, işlədikcə yenilə. Skript on iki açarın hamısını tələb edir.

| Açar | Suallar | Əsas mənbələr |
|---|---|---|
| `market_size` | Bazarın həcmi (dəyər və miqdar). İki üsulla: yuxarıdan-aşağı və aşağıdan-yuxarı | statistika, ticarət datası, şirkət hesabatları |
| `growth` | Son 3–5 ilin dinamikası, proqnoz və kimin proqnozu | statistika, beynəlxalq təşkilatlar |
| `segments` | Məhsul, qiymət, region, kanal üzrə seqmentlər və payları | sahə assosiasiyaları, statistika |
| `customers` | Kim alır, niyə, nə qədər, necə qərar verir | sorğular, rəylər, axtarış trendləri |
| `competitors` | Əsas oyunçular, payları, mövqeləri, əvəzedicilər | `competitor-watch` |
| `pricing` | Qiymət səviyyələri, marja, qiymət dinamikası | rəqib saytları, elan saytları, statistika |
| `channels` | Satış və paylama kanalları, onlayn payı, əsas vasitəçilər | şirkət saytları, e-ticarət statistikası |
| `regulation` | Lisenziya, sertifikat, standart, vergi, etiketləmə | rəsmi qanunvericilik, tənzimləyici |
| `trade` | İdxal, ixrac, əsas təchizatçı ölkələr, tariflər | UN Comtrade, gömrük, WTO |
| `entry_barriers` | Kapital, icazələr, miqyas, brend, paylama şəbəkəsinə giriş | yuxarıdakıların sintezi |
| `trends` | Texnologiya, istehlak vərdişləri, tənzimləmə dəyişiklikləri | sahə nəşrləri, elmi ədəbiyyat |
| `risks` | Valyuta, siyasi, təchizat, tələb, tənzimləmə riskləri | mərkəzi bank, IMF, sanksiya siyahıları |

## coverage.json formatı
```json
{"type": "market",
 "items": {
   "market_size": {"status": "found"},
   "pricing": {"status": "partial", "searched": ["rəqib saytları (5-dən 3-ü qiymət göstərir)", "elan saytları"]},
   "segments": {"status": "not_found", "searched": ["milli statistika: seqment bölgüsü yoxdur", "sahə assosiasiyası: hesabat pulludur"]}
 }}
```

## Qaydalar
- `found`: bölmədə ən azı bir təsdiqlənmiş tapıntı var. `partial`: bəzi suallar cavabsızdır. `not_found`: mənbəli cavab yoxdur.
- `partial` və `not_found` üçün `searched`-də ən azı iki konkret axtarış yeri və nəticəsi yaz. "Axtardım, tapmadım" yetərli deyil.
- Tapılmayan bölməni təxminlə doldurma. Hesabatın boşluqlar bölməsində yaz və onu doldurmaq üçün nə lazım olduğunu göstər (ödənişli hesabat, sorğu, müsahibə, yerli ekspert).
- Heç bir bölməni "uyğun deyil" deyə atma; uyğun deyilsə, `not_found` yaz və səbəbini `searched`-də izah et.
- Bölmələri subagentlərə paylaya bilərsən; yekunda `fact-checker` hər əsas rəqəmi yenidən yoxlayır.

Başqa növlərin (`business`, `company`, `academic`, `legal`, `technical`, `policy`, `due_diligence`, `target_markets`) məcburi bölmələri `research-types`-dadır. Qarışıq sualda `"type": ["market", "legal"]` yaz; skript hər iki siyahını tələb edir. Heç biri uyğun deyilsə (`"type": "other"`), `items` sənin alt suallarındır, ən azı üç.

Başqa bölmələr: çərçivələr üçün `business-analysis`, ölkə seçimi üçün `target-markets`, mənbə qiymətləndirməsi üçün `source-quality`.
