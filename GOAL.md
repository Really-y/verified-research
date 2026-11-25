# MƏQSƏD: verified-research pluginini tamamla və real şəraitdə sübut et

Plugin qlobaldır: istənilən ölkə, dil və araşdırma növü (bazar, biznes, hədəf bazar, şirkət və maliyyə, elmi ədəbiyyat, hüquq və tənzimləmə, texniki, siyasət).

Bu qovluq işlək skeletdir. `tests/RESULTS.md` nəyin artıq sübut olunduğunu və nəyin olunmadığını göstərir. Sənin işin "Hələ yoxlanılmayıb" siyahısını bağlamaqdır. Mövcud sınaqları sındırma: hər dəyişiklikdən sonra aşağıdakı iki əmr keçməlidir.

```bash
claude plugin validate . --strict
bash tests/run_tests.sh
```

Müstəqil işlə. Yalnız bu hallarda dayan və soruş: pul xərcləyən addım, sistemə qlobal quraşdırma, API açarı çatışmazlığı.

## Bilinən faktlar (2026-11-25, Claude Code 2.1.332-də sınanıb və ya sənəddən oxunub)

- Yalnız `plugin.json` `.claude-plugin/` içində olur; qalan hər şey plugin kökündədir.
- Yüklənmə statusu: `claude --plugin-dir . plugin list` (bayraq `plugin` sözündən **əvvəl** gəlir; sonra yazanda "unknown option" xətası verir).
- Komponent siyahısı və token xərci: `claude --plugin-dir . plugin details verified-research`.
- Sessiyada: `/reload-plugins`, `/plugin` (Installed və Errors tabları), `/hooks`.
- `PostToolUse` hook-unda yalnız **2** çıxış kodu stderr-i Claude-a göstərir; 1 kodu bloklamır və yalnız istifadəçiyə görünür. `scripts/hook_verify.py` buna görə 2 qaytarır.
- Hook faylın yolunu stdin-dən JSON kimi alır: `.tool_input.file_path`.
- Eval halları: `evals/**/case.yaml` və ya `prompt.md` + `graders/*.md`. Sxemi `claude plugin eval --help` və code.claude.com/docs/en/plugin-evals-dən oxu.
- stat.gov.az-ın aylıq press-relizləri PDF-dir və mətni çıxarılır. Cədvəllərdə ədədlər yanaşı durur (`58 997,7 103,7`).
- Sənəd indeksi: https://code.claude.com/docs/llms.txt

## Bitmə şərti

0. **Yoxlayıcını yoxla.** Doqquz sınaqdan sonra ən azı 20 əsas tapıntı seç və hər birini özün mənbədən yoxla: rəqəm düzdürmü, sitat həmin göstəriciyə aiddirmi, daha yaxşı mənbə varmı. Skriptin və `fact-checker`-in keçirdiyi, amma əslində yanlış olan halları say. Nəticəni (`20-dən neçəsi düz`) `tests/RESULTS.md`-ə yaz. Bu, pluginin real dəqiqlik ölçüsüdür.

0a. **Tənqidçini yoxla.** Bilərəkdən zəif bir nəticəsi olan hesabat qaralaması hazırla (məsələn, tək mənbəyə söykənən bazar həcmi, nəzərə alınmamış güclü rəqib, optimist təxmin) və `critic`-ə ver. Üç qüsurdan neçəsini tapdığını `tests/RESULTS.md`-ə yaz. Sonra möhkəm bir hesabat ver: uydurma etiraz yazırmı? Etirazlar formal və ümumidirsə, `agents/critic.md`-i sərtləşdir və yenidən sına.
1. **Real sessiya.** `sandbox/` qovluğu yarat, orada `claude --plugin-dir ..` ilə sessiya aç. `/plugin` Errors tabı boşdur. "Bakıda X bazarı nə qədərdir?" kimi adi sualda Claude `research-method`-u özü seçir.
2. **Hook real işləyir.** `sandbox/reports/`-a bilərəkdən uydurma rəqəmli hesabat yazdır. Debug log-da hook-un 2 kodu ilə çıxdığı və Claude-un səbəbi aldığı görünür. Sübutu `tests/RESULTS.md`-ə yaz.
3. **`${CLAUDE_PLUGIN_ROOT}`.** `research-method` skill-indəki bash əmrləri bu dəyişəndən istifadə edir. Skill-dən çağırılan əmrdə əlçatan olduğunu yoxla. Deyilsə, sənəddəki düzgün üsulla əvəz et.
4. **Mənbələr və alətlər.** `skills/source-map/references/global.md`, `countries/AZ.md` və `skills/research-tools/references/tools.md`-də hər "yoxlanılmayıb" sətrini aç və statusu yenilə: `işləyir` (data formatı ilə: HTML, PDF, API) / `qeydiyyat lazımdır` / `əlçatmaz`. İşləməyən URL-i düzəlt və ya sil. `robots.txt`-ə əməl et.
5. **Doqquz araşdırma sınağı** `sandbox/`-da (`evals/README.md`-dəki hallar), hesabatlar `sandbox/reports/`-da. Bunlar birlikdə yoxlayır: yerli bazar, xəritəsi olmayan ölkə (GE faylı yaranmalıdır), hədəf bazar müqayisəsi, biznes təhlili, ingiliscə elmi ədəbiyyat, tənzimləmə, data olmayan sual, mənbəsiz rəqəm tələsi, şəxsi məlumat həddi. Rəqəm olan hər hesabatda `verify_report.py` 0 qaytarır.
6. **Əl ilə müqayisə.** Birinci sınağın rəqəmlərini stat.gov.az press-relizlərində özün tap və hesabatla tutuşdur. Uyğun gələn, gəlməyən və səbəbi `tests/RESULTS.md`-ə yaz.
7. **Eval.** `evals/README.md`-dəki doqquz halı real formatda yaz, `claude plugin eval .` işlət. Pluginlə və pluginsiz bal fərqini `tests/RESULTS.md`-ə yaz.
8. **Subagentlər.** Subagents sənədini oxu; hər agentə yalnız lazım olan alətləri ver (araşdırmaçılara yazma icazəsi lazım deyil).
9. **Skriptin zəif yerləri.** Sınaqlarda rast gəldiyin hər yanlış rədd və ya yanlış təsdiq üçün `tests/`-ə yeni hal əlavə et, sonra düzəlt. Bilinən hallar: müstəqillik yalnız domen fərqi ilə ölçülür (iki sayt eyni ilkin mənbədən köçürə bilər); `registrable()` sadələşdirilib, mürəkkəb domen sonluqlarında səhv edə bilər; `trusted_domains.txt` qısadır, sınaqlarda rast gəldiyin rəsmi qurumları **təklif kimi** `tests/RESULTS.md`-ə yaz, siyahını özün dəyişmə; JavaScript ilə yüklənən səhifələr; dəyər mənbədəki yazılışla eyni olmalıdır (`1234567.89` ilə `1,234,567.89` uyğun gəlmir); başlıq yalnız dörd dildə tanınır; sağdan-sola və rəqəmləri fərqli yazılan dillər (ərəb, fars, hind rəqəmləri) sınanmayıb; ardıcıl tam ədədlər (`30 439 102`) qeyri-müəyyəndir; sitat düz, amma başqa göstəriciyə aid ola bilər (skript bunu tutmur, `report-editor` yoxlamalıdır).
10. **Dövri monitorinq.** Sənəddə Claude Code üçün cədvəlli işə salma üsulunu tap (daxili imkan və ya sistem cron-u ilə başsız rejim) və README-də həftəlik rəqib izləməni necə qurmağı yaz.
11. **README.** Komanda ilə paylaşma yolları, Looker Studio-ya CSV qoşmaq, məhdudiyyətlər.

## Qaydalar

- Açarlar yalnız iş qovluğundakı `.env`-də; plugin içində açar olmamalıdır.
- Skriptlər Python standart kitabxanası və `pypdf` ilə qalsın.
- Hər bitmə şərtindən sonra commit.
- Bir şey işləmirsə, saxta "keçdi" yazma. `tests/RESULTS.md`-də nəyin işləmədiyini və səbəbini yaz.

## Sonda

Qısa yekun: 11 şərtdən hansı bağlandı, hansı yox və niyə; yoxlama skripti neçə rəqəmi təsdiqlədi və neçəsini rədd etdi; eval fərqi; əlçatmaz mənbələr; növbəti 3 təkmilləşdirmə.
