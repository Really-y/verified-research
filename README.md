# verified-research

Claude Code üçün qlobal araşdırma plugini: istənilən ölkə və mövzu (bazar, biznes, hədəf bazar seçimi, şirkət və maliyyə, elmi ədəbiyyat, hüquq və tənzimləmə, texniki, siyasət). Hər rəqəm üçün mənbə və hərfi sitat tələb edir, hesabat yazılanda rəqəmləri mənbə səhifələri ilə avtomatik tutuşdurur.

## İşə salmaq

```bash
claude --plugin-dir /yol/verified-research
```

Sualı istənilən dildə yazın ("Almaniyada üzvi qida bazarı nə qədərdir?", "Which three Gulf countries are the best export targets for hazelnuts?") və ya skill-i birbaşa çağırın: `/verified-research:research-method`. Hesabat sualın dilində yazılır.

## Tərkibi

- Skill-lər: `research-method`, `research-types`, `source-quality`, `market-research`, `critical-review`, `source-map`, `research-tools`, `business-analysis`, `target-markets`, `competitor-watch`, `report-template`
- Subagentlər: `market-researcher`, `competitor-researcher`, `customer-researcher`, `literature-researcher`, `regulatory-researcher`, `fact-checker`, `critic`, `report-editor`
- Hook: `reports/*.md` yazılanda `scripts/verify_report.py` işə düşür; uğursuzluq Claude-a qaytarılır
- Skriptlər: `verify_report.py` (yoxlama), `save_findings.py` (SQLite və CSV)

İş datası (`reports/`, `data/research.db`, `research-data/sources/`, `.env`) plugin qovluğunda deyil, işlədiyiniz qovluqda saxlanılır.

## Keyfiyyət yoxlaması

Hər hesabat üçün skript bunları məcbur edir və `reports/<ad>.quality.md` yaradır:

- hər rəqəm mənbə səhifəsində hərfi keçir;
- hər mənbənin səviyyəsi (1–6) yazılıb; tanınmış domenlərin səviyyəsi `scripts/trusted_domains.txt`-dən gəlir və şişirdilə bilməz;
- nəticənin söykəndiyi əsas rəqəmlər ya rəsmi ilkin və ya beynəlxalq mənbədəndir, ya da başqa domendəki ikinci mənbə ilə təsdiqlənib;
- mənbələr 10%-dən çox fərqlənirsə, səbəb yazılıb və hər iki rəqəm göstərilib;
- 2 ildən köhnə data işarələnib;
- bazar araşdırmasında on iki bölmənin hamısı əhatə siyahısındadır; tapılmayan hər bölmə üçün ən azı iki axtarış yeri göstərilib.

- ayrı `critic` subagenti nəticəni sındırmağa çalışıb: ən azı üç etiraz, əks mövqe, ən zəif fərziyyə; hər etiraza yazılı cavab verilib. Rədd edilmiş ciddi etirazlar keyfiyyət xülasəsində sizə göstərilir.

`trusted_domains.txt` faylını yalnız siz dəyişirsiniz. Öz bazarınızın rəsmi qurumlarını ora əlavə edin.

## Ölkələr

Beynəlxalq mənbələr `skills/source-map/references/global.md`-dədir. Hazır ölkə faylı yalnız Azərbaycan üçündür (`countries/AZ.md`). Başqa ölkə üzrə ilk sualda agent həmin ölkənin ilkin mənbələrini (statistika qurumu, mərkəzi bank, gömrük, reyestr, qanunvericilik bazası) tapır və iş qovluğunda `research-data/sources/<ISO2>.md` faylına yazır; sonrakı araşdırmalar onu istifadə edir.

## Tələblər

Python 3.9+ və `pip install pypdf` (bir çox statistika qurumu datanı PDF kimi yayır). Sınaqlar üçün əlavə olaraq `pip install reportlab`.

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
