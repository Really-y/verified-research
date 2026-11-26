---
name: research-types
description: Use at the start of every research task to classify it (market, business, target markets, company or financial, academic literature, legal or regulatory, technical or product, policy or socioeconomic, due diligence, or a mix) and pick the matching coverage checklist, evidence standard, analysis method and specialist subagents. Always used together with research-method.
---

# Araşdırma növləri

> **Əvvəlcə `research-method`.** Bu skill təkbaşına işləmir: tapıntı formatı, hərfi sitat qaydası, fayl adları və avtomatik yoxlama `verified-research:research-method`-dadır. O, bu sessiyada hələ yüklənməyibsə, indi `Skill` aləti ilə onu çağır, sonra buraya qayıt.

## 1. Növü müəyyən et
Sualı aşağıdakı növlərdən birinə və ya bir neçəsinə aid et. Qarışıq sualda (məsələn, "Gürcüstanda su bazarı nə qədərdir və hansı icazələr lazımdır?") **hər iki növü** götür: `"type": ["market", "legal"]`. Skript bütün növlərin bölmələrini birlikdə tələb edir.

| `type` | Nə vaxt | Əlavə skill | Subagentlər |
|---|---|---|---|
| `market` | bazar həcmi, sektor, tələb, ticarət | `market-research` | market-, competitor-, customer-researcher |
| `business` | ideyanın qiymətləndirilməsi, TAM/SAM/SOM, zərərsizlik, unit economics | `business-analysis` | market-, competitor-researcher |
| `target_markets` | ölkə və region seçimi, ixrac istiqaməti | `target-markets` | market-, regulatory-researcher |
| `company` | konkret şirkət: maliyyə, sahiblik, mövqe | `competitor-watch` (rəqib izləmə) | company-researcher |
| `academic` | "sübut nə deyir?", elmi ədəbiyyat, effekt | | literature-researcher |
| `legal` | qanun, icazə, lisenziya, standart, idxal tələbləri | | regulatory-researcher |
| `technical` | texnologiya, məhsul, versiya, standart, müqayisə | | technical-researcher |
| `policy` | sosial-iqtisadi göstərici, siyasət effekti, ölkə müqayisəsi | | policy-researcher |
| `due_diligence` | təşkilat haqqında yoxlama: qeydiyyat, məhkəmə, sanksiya | | company-researcher |
| `other` | heç biri uyğun deyil | | uyğun olan |

## 2. Əhatə siyahısı (`coverage.json`, skript məcbur edir)
`market` üçün 12 bölmə `market-research`-dədir. Digər növlərin bölmələri:

| `type` | Məcburi açarlar və onların sualı |
|---|---|
| `business` | `market_size` (TAM/SAM/SOM iki üsulla), `competition`, `pricing`, `costs` (başlanğıc və aylıq), `unit_economics` (orta çek, marja, CAC/LTV əgər tətbiq olunursa), `break_even`, `scenarios` (pessimist, baza, optimist), `risks` |
| `target_markets` | `candidates` (geniş siyahı və seçim səbəbi), `criteria_weights`, `comparable_data` (eyni il, valyuta, tərif), `scoring` (kodla), `shortlist_deep_dive`, `sensitivity` (çəki dəyişəndə sıralama) |
| `company` | `identity` (rəsmi ad, qeydiyyat nömrəsi, ölkə), `ownership` (səhmdarlar, benefisiar, əgər açıqdırsa), `financials` (gəlir, mənfəət, valyuta, maliyyə ili, audit), `business_model`, `market_position` (pay, rəqiblər), `management`, `legal_issues` (məhkəmə, cərimə, tənzimləyici qərarlar), `risks` |
| `academic` | `search_strategy` (bazalar, axtarış ifadələri, tarix aralığı), `evidence_base` (tədqiqatların sayı, növü, nümunə ölçüsü), `main_findings` (effektin istiqaməti və ölçüsü), `study_quality` (dizayn, qərəz riski, resenziya, geri çağırma yoxlaması), `conflicting_evidence`, `gaps` |
| `legal` | `applicable_law` (akt adı, nömrəsi), `requirements` (maddə-maddə), `current_version` (qüvvədə olan redaksiyanın tarixi), `authority` (səlahiyyətli qurum), `procedure` (müraciət, müddət, rüsum), `penalties`, `upcoming_changes` (qəbul edilmiş, amma qüvvəyə minməmiş dəyişikliklər) |
| `technical` | `versions` (versiya və buraxılış tarixi), `specifications`, `standards`, `alternatives`, `known_issues` (məlum xətalar, təhlükəsizlik bildirişləri), `performance` (ölçmə üsulu ilə), `cost_licensing` |
| `policy` | `definitions` (göstəricinin rəsmi tərifi), `data_trend`, `comparison` (eyni tərifli ölkə və ya qrup), `methodology` (nümunə, sorğu, düzəlişlər), `stakeholders` (mövqelər mənbəsi ilə), `evidence_of_effects` (səbəb-nəticə sübutu, korrelyasiya deyil), `limitations` |
| `due_diligence` | `registration`, `ownership`, `financials`, `litigation`, `sanctions` (OFAC, AB, BMT, Böyük Britaniya siyahıları), `licenses`, `media` (iddia ilə sübut ayrı), `claims_vs_evidence` (təşkilatın öz iddiaları və onları təsdiq edən sənəd) |
| `other` | sənin alt sualların, ən azı üç |

Bölmə uyğun deyilsə (məsələn, xidmət şirkətində `trade`), onu atma: `not_found` yaz və `searched`-də iki yer göstər. Növ adını səhv yazsan, skript rədd edir.

## 3. Sübut standartı

| Növ | Əsas mənbələr | Sübut standartı | Tipik səhv |
|---|---|---|---|
| Bazar və sektor | statistika qurumları, gömrük, sahə assosiasiyaları, şirkət hesabatları | rəqəm üçün ilkin mənbə; bazar həcmi iki üsulla | araşdırma şirkətlərinin pulsuz xülasələrindəki rəqəmi mənbəsiz götürmək |
| Biznes təhlili | yuxarıdakılar + rəqib qiymət siyahıları, icarə elanları, əmək haqqı statistikası | hər giriş rəqəmi tapıntıdır; hesablama kodla; üç ssenari | bir optimist fərziyyəni bütün modelə yaymaq |
| Hədəf bazar | UN Comtrade, Dünya Bankı, WTO/WITS, milli statistika | bütün ölkələr üçün eyni il, valyuta, tərif; bal və xam rəqəm ayrı | fərqli illərin rəqəmlərini bir cədvəldə müqayisə etmək |
| Şirkət və maliyyə | illik hesabatlar, birja bəyanatları (SEC EDGAR, Companies House və s.), şirkət reyestrləri | rəqəm rəsmi hesabatdan; valyuta və maliyyə ili göstərilir | media xəbərindəki rəqəmi hesabatla yoxlamamaq; seqment rəqəmini şirkətin ümumi rəqəmi kimi götürmək |
| Elmi ədəbiyyat | OpenAlex, Crossref, PubMed, Cochrane, arXiv, jurnal səhifələri | resenziyalı nəşr preprintdən, sistematik icmal tək tədqiqatdan üstündür; nümunə ölçüsü və tədqiqat növü qeyd olunur | abstraktı oxumadan başlıqdan nəticə çıxarmaq; geri çağırılmış məqaləyə istinad; nəşr qərəzini nəzərə almamaq |
| Hüquq və tənzimləmə | rəsmi qanunvericilik bazaları (EUR-Lex, e-qanun.az və s.), tənzimləyici qurumlar, rəsmi qəzetlər | yalnız rəsmi mətn, maddə nömrəsi və qüvvədə olan redaksiya tarixi ilə | köhnə redaksiyaya və ya hüquq firmasının bloquna əsaslanmaq |
| Texniki və məhsul | rəsmi sənədlər, standartlar (ISO, IETF RFC, W3C), patent bazaları, buraxılış qeydləri, CVE/NVD | versiya və tarix göstərilir; benchmark-ın şərtləri yazılır | köhnə versiyanın sənədinə istinad; satıcının marketinq benchmark-ını müstəqil ölçmə kimi təqdim etmək |
| Siyasət və sosial-iqtisadi | beynəlxalq təşkilatlar, milli statistika, sorğu təşkilatları, qiymətləndirmə tədqiqatları | metodologiya və nümunə göstərilir; səbəb iddiası üçün kvazi-eksperimental və ya RCT sübutu | fərqli təriflərlə ölçülmüş göstəriciləri müqayisə etmək; korrelyasiyanı effekt kimi təqdim etmək |
| Təşkilat haqqında yoxlama | reyestrlər, məhkəmə bazaları, sanksiya siyahıları, rəsmi sayt | yalnız açıq rəsmi mənbələr; iddia ilə sübutu ayır | təsdiqlənməmiş ittihamı fakt kimi yazmaq; adaşı ilə qarışdırmaq (qeydiyyat nömrəsi ilə yoxla) |

## 4. Təhlil üsulu (hesabatın "Təhlil" bölməsi)
Faktlar toplananda iş bitmir. Növə görə təhlil:

- **market:** iki üsulla həcm və fərqin izahı; artımın real (inflyasiyasız) və nominal hissəsi; seqment və kanal üzrə harada pul var.
- **business:** düsturlar kodla; zərərsizlik nöqtəsi üç ssenaridə; ən həssas giriş (±20% dəyişəndə nəticəni ən çox dəyişən); "bu nə vaxt yanlış olar?".
- **target_markets:** bal cədvəli kodla; çəki həssaslığı; qısa siyahıdakı hər ölkə üçün əsas maneə.
- **company:** 3–5 illik dinamika, marjalar, rəqiblərlə eyni metrikada müqayisə; qırmızı bayraqlar (audit rəyi, gecikmiş hesabat, tez-tez rəhbər dəyişməsi).
- **academic:** sübut cədvəli (tədqiqat, dizayn, n, nəticə, qərəz riski); sübutun ümumi gücü (güclü / orta / zəif / ziddiyyətli) və niyə; nəticənin kimə ümumiləşdirilə bilməyəcəyi.
- **legal:** tələblər yoxlama siyahısı kimi (maddə, nə tələb olunur, kim yoxlayır, sənəd); qeyri-müəyyən yerlər; "yekun söz hüquqşünasındır".
- **technical:** eyni meyarlarla müqayisə cədvəli; hansı halda hansı variant; versiya riskləri.
- **policy:** trend və müqayisə eyni tərifdə; effekt iddiaları sübut səviyyəsi ilə; əsas mövqelər ayrı-ayrı, birini seçmədən.
- **due_diligence:** tapıntı və iddia cədvəli (təsdiqləndi / təsdiqlənmədi / ziddiyyətli); risk səviyyəsi səbəbi ilə; açıq suallar.

## Hədlər
- **Fiziki şəxslər:** yalnız ictimai rolu olan şəxslərin ictimai fəaliyyəti. Şəxsi məlumat (ünvan, ailə, sağlamlıq, şəxsi hesablar) toplama.
- **Tibb, hüquq, vergi, investisiya:** araşdırma mənbələri və faktları verir, qərar mütəxəssisindir. Hesabatda bunu qeyd et.
- **Tibbi mövzular:** klinik təlimatları və sistematik icmalları tək tədqiqatlardan üstün tut.
- Mübahisəli mövzularda əsas mövqeləri mənbələri ilə ayrı-ayrı göstər, birini seçmə.

Biznes çərçivələri üçün `business-analysis`, ölkə seçimi üçün `target-markets`.
