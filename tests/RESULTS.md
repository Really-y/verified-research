# Sınaq nəticələri

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
