# verified-research

[English](README.md) · **Azərbaycanca**

Claude Code üçün qlobal araşdırma plugini: istənilən ölkə və mövzu (bazar, biznes, hədəf bazar seçimi, şirkət və maliyyə, elmi ədəbiyyat, hüquq və tənzimləmə, texniki, siyasət). Hər rəqəm üçün mənbə və hərfi sitat tələb edir, hesabat yazılanda rəqəmləri mənbə səhifələri ilə avtomatik tutuşdurur.

## Quraşdırma

Marketplace kimi (GitHub-dan):

```
/plugin marketplace add Really-y/verified-research
/plugin install verified-research@verified-research
```

Və ya yerli qovluqdan, yalnız bu sessiya üçün:

```bash
claude --plugin-dir /yol/verified-research
```

Sualı istənilən dildə yazın ("Almaniyada üzvi qida bazarı nə qədərdir?", "Which three Gulf countries are the best export targets for hazelnuts?") və ya skill-i birbaşa çağırın: `/verified-research:research-method`. Hesabat sualın dilində yazılır.

## Tərkibi

- Skill-lər: `research-method`, `research-types`, `source-quality`, `market-research`, `critical-review`, `source-map`, `research-tools`, `business-analysis`, `target-markets`, `competitor-watch`, `report-template`
- Subagentlər: `market-researcher`, `competitor-researcher`, `customer-researcher`, `literature-researcher`, `regulatory-researcher`, `company-researcher`, `technical-researcher`, `policy-researcher`, `fact-checker`, `critic`, `report-editor`
- Hook: `reports/*.md` yazılanda `scripts/verify_report.py` işə düşür; uğursuzluq Claude-a qaytarılır
- Skriptlər: `verify_report.py` (yoxlama), `fetch_text.py` (mənbə mətnini yoxlamanın gördüyü kimi göstərir, hərfi sitat üçün), `save_findings.py` (SQLite və CSV)

İş datası (`reports/`, `data/research.db`, `research-data/sources/`, `.env`) plugin qovluğunda deyil, işlədiyiniz qovluqda saxlanılır. **Claude-u plugin qovluğunun içindən yox, ayrıca iş qovluğundan işə salın:** Claude Code `--plugin-dir` qovluğunun içinə yazmağı həssas fayl dəyişikliyi sayır və başsız rejimdə (`claude -p`) bloklayır.

## Keyfiyyət yoxlaması

Hər hesabat üçün skript bunları məcbur edir və `reports/<ad>.quality.md` yaradır:

- hər rəqəm mənbə səhifəsində hərfi keçir;
- hər mənbənin səviyyəsi (1–6) yazılıb; tanınmış domenlərin səviyyəsi `scripts/trusted_domains.txt`-dən gəlir və şişirdilə bilməz;
- nəticənin söykəndiyi əsas rəqəmlər ya rəsmi ilkin və ya beynəlxalq mənbədəndir, ya da başqa domendəki ikinci mənbə ilə təsdiqlənib;
- mənbələr 10%-dən çox fərqlənirsə, səbəb yazılıb və hər iki rəqəm göstərilib;
- 2 ildən köhnə data işarələnib;
- hər araşdırma növünün öz məcburi əhatə siyahısı var (`market` 12 bölmə; `business`, `target_markets`, `company`, `academic`, `legal`, `technical`, `policy`, `due_diligence` 6–8 bölmə; qarışıq sualda `["market", "legal"]` kimi birlikdə); tapılmayan hər bölmə üçün ən azı iki axtarış yeri göstərilib.

- ayrı `critic` subagenti nəticəni sındırmağa çalışıb: ən azı üç etiraz, əks mövqe, ən zəif fərziyyə; hər etiraza yazılı cavab verilib. Rədd edilmiş ciddi etirazlar keyfiyyət xülasəsində sizə göstərilir.

`trusted_domains.txt` faylını yalnız siz dəyişirsiniz. Öz bazarınızın rəsmi qurumlarını ora əlavə edin.

## Ölkələr

Beynəlxalq mənbələr `skills/source-map/references/global.md`-dədir. Hazır ölkə faylı yalnız Azərbaycan üçündür (`countries/AZ.md`). Başqa ölkə üzrə ilk sualda agent həmin ölkənin ilkin mənbələrini (statistika qurumu, mərkəzi bank, gömrük, reyestr, qanunvericilik bazası) tapır və iş qovluğunda `research-data/sources/<ISO2>.md` faylına yazır; sonrakı araşdırmalar onu istifadə edir.

## Tələblər

Python 3.9+ və `pypdf` (bir çox statistika qurumu datanı PDF kimi yayır). Sınaqlar üçün əlavə olaraq `reportlab`. Sistem Python-una quraşdırmaq istəmirsinizsə, virtual mühit yaradın və Claude Code-u həmin mühit aktiv olanda işə salın (hook `python3`-ü `PATH`-dən götürür):

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf reportlab
PATH="$PWD/.venv/bin:$PATH" claude --plugin-dir /yol/verified-research
```

## Komanda ilə paylaşma

1. **Git repo + marketplace (tövsiyə olunur).** Repoda `.claude-plugin/marketplace.json` var. Komanda üzvləri `/plugin marketplace add Really-y/verified-research` və `/plugin install verified-research@verified-research` yazır; yeniləmələr `/plugin marketplace update` ilə gəlir.
2. **Layihəyə bağlamaq.** Layihənin `.claude/settings.json` faylına marketplace-i və plugin-i əlavə edin ki, repo-nu açan hər kəsə avtomatik təklif olunsun:
   ```json
   {"extraKnownMarketplaces": {"verified-research": {"source": {"source": "github", "repo": "Really-y/verified-research"}}},
    "enabledPlugins": {"verified-research@verified-research": true}}
   ```
3. **Arxiv.** `claude --plugin-dir verified-research.zip` da işləyir; qapalı mühitlər üçün qovluğu zip kimi paylaşın.
4. **Nəticələri paylaşmaq.** `reports/*.md` + `*.quality.md` + `*.findings.json` birlikdə paylaşılır: oxucu hər rəqəmin mənbəsini və skriptin hökmünü görür. `data/research.db` komandanın ortaq tarixçəsidir; onu ortaq qovluqda saxlayın və ya hər araşdırmadan sonra CSV-ni ixrac edin.

## Looker Studio-ya CSV qoşmaq

`save_findings.py` hər araşdırmadan sonra `reports/<ad>.csv` yaradır (UTF-8 BOM ilə, sütunlar: `tarix, sual, sektor, gosterici, deyer, vahid, dovr, menbe_url, sitat, baxis_tarixi, etibarliliq, nov, qeyd`).

1. Bütün CSV-ləri bir fayla yığın: `python3 -c "import sqlite3,csv,sys; c=sqlite3.connect('data/research.db'); r=c.execute('select * from findings'); w=csv.writer(open('findings_all.csv','w',newline='',encoding='utf-8')); w.writerow([d[0] for d in r.description]); w.writerows(r)"`
2. Faylı Google Sheets-ə yükləyin (Fayl → İdxal) və ya Google Drive-a qoyun. Mütəmadi yeniləmə üçün eyni Sheet-in üzərinə idxal edin ("Cari vərəqi əvəz et").
3. Looker Studio → Yarat → Data mənbəyi → **Google Sheets** konnektoru → həmin vərəq. (Birbaşa **Fayl yükləmə** konnektoru da CSV qəbul edir, amma avtomatik yenilənmir.)
4. Sahə tiplərini yoxlayın: `deyer` mətndir (mənbədəki yazılışla saxlanılır: `58 997,7`). Qrafik üçün hesablanmış sahə yaradın: `CAST(REPLACE(REPLACE(deyer, " ", ""), ",", ".") AS NUMBER)`; ingiliscə yazılışlarda (`1,234.5`) əvvəlcə vergülü silin.
5. `etibarliliq` və `nov` (fact/estimate) sahələrini filtr kimi əlavə edin ki, təxminlər faktlarla qarışmasın; `menbe_url`-u cədvəldə link kimi göstərin.

## Dövri monitorinq (həftəlik rəqib izləmə)

Claude Code-da üç yol var (sənəd: code.claude.com/docs/en/scheduled-tasks, /en/routines, /en/headless):

| Yol | Harada işləyir | Nə vaxt seçmək |
|---|---|---|
| `/schedule` (bulud planlı tapşırıqları) | Anthropic buludunda, kompüter sönülü olanda da | plugin GitHub repo-dadırsa; Pro/Max/Team/Enterprise planları |
| Desktop tətbiqində planlı tapşırıq | yerli maşın, tətbiq açıq olanda | Desktop istifadəçiləri |
| Sistem `cron` + başsız rejim (`claude -p`) | yerli maşın və ya server | tam nəzarət, yerli `data/research.db` ilə |

`/loop` və `CronCreate` yalnız açıq sessiya müddətində işləyir (planlı tapşırıqlar 30 gündən sonra silinir), ona görə həftəlik izləmə üçün uyğun deyil.

**Sistem cron ilə nümunə** (hər bazar ertəsi 08:00). İş qovluğunda `watch.sh`:

```bash
#!/usr/bin/env bash
cd /yol/is-qovlugu                       # reports/, data/research.db burada
export PATH="/yol/is-qovlugu/.venv/bin:$PATH"
claude -p "$(cat watch-prompt.txt)" \
  --plugin-dir /yol/verified-research \
  --permission-mode acceptEdits --permission-prompts none \
  --allowedTools "WebSearch" "WebFetch" "Read" "Write" "Edit" "Glob" "Grep" "Skill" "Agent" \
    "Bash(python3 *verified-research/scripts/*)" \
  --max-turns 150 --output-format json > "logs/watch-$(date +%F).json" 2>&1
```

`watch-prompt.txt`:

```
competitor-watch skill-i ilə bu rəqibləri yoxla: <rəqib 1 saytı>, <rəqib 2 saytı>, <rəqib 3 saytı>.
Bazar: <ölkə, sektor>. Əvvəlki nəticəni data/research.db-dən oxu və yalnız dəyişiklikləri yaz
(qiymət, yeni məhsul, aktiv reklam, iş elanı, rəy reytinqi). Hesabatı reports/<tarix>-reqib-izleme.md kimi yaz,
yoxlamadan keçir və save_findings.py ilə bazaya əlavə et.
```

`crontab -e`:

```
0 8 * * 1  /yol/is-qovlugu/watch.sh
```

Qeydlər: `--permission-prompts none` icazə sorğularını avtomatik rədd edir (cavab verən yoxdur), ona görə lazım olan alətləri `--allowedTools`-da açıq yazın. `--bare` rejimində quraşdırılmış plugin-lər avtomatik yüklənmir; `--plugin-dir` mütləqdir. Cron mühitində `PATH` qısadır, `claude`-un tam yolunu yazın (`which claude`). Giriş: `claude` hesaba daxil olmuş istifadəçinin adından işləyir; serverdə `ANTHROPIC_API_KEY` iş qovluğundakı `.env`-dən oxuna bilər (plugin qovluğunda açar saxlamayın).

**Bulud variantı:** `/schedule` yazın, tapşırığa yuxarıdakı mətni verin və repo kimi plugin-in GitHub repo-sunu seçin. Bulud tapşırığı yerli `data/research.db`-ni görmür; tarixçəni repo-da saxlayın (məsələn, `reports/` qovluğunu commit edin).

## Sınaq

```bash
claude plugin validate . --strict
bash tests/run_tests.sh
```

## Məhdudiyyətlər

- Yoxlama rəqəmin mənbə səhifəsində olduğunu təsdiqləyir. Mənbənin özünün düzgünlüyünü və sitatın suala uyğunluğunu yoxlamır.
- Tapıntıdakı dəyər mənbədəki yazılışla eyni olmalıdır (`1,234,567.89`, `1.234.567,89`, `58 997,7`).
- Hesabatın əsas rəqəmlər başlığı dörd dildən birində olmalıdır (Azərbaycan, ingilis, rus, türk); başqa dillərdə `## Key figures` işlədilir.
- JavaScript ilə yüklənən səhifələrdə sitat tapılmaya bilər.
- `global.md`, `countries/AZ.md` və `tools.md` sətirlərinin çoxu "yoxlanılmayıb" statusundadır; ilk istifadədə təsdiqlənməlidir.
- Təhlil, bal cədvəlləri və tövsiyələr mühakimədir, avtomatik yoxlanılmır.
- Skript tənqidin aparıldığını və cavablandığını yoxlayır, etirazların haqlı olub-olmadığını yox. Tənqidçi də yanıla bilər; hansı tərəfin haqlı olduğuna siz qərar verirsiniz.
- Fiziki şəxslər haqqında şəxsi məlumat toplanmır. Tibb, hüquq, vergi və investisiya qərarlarında yekun söz mütəxəssisindir.
