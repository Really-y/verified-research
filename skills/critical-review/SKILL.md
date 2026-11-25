---
name: critical-review
description: Use before finalising any report that draws conclusions or makes recommendations, and whenever the user asks for critique, a devil's advocate view, risks, weaknesses or a second opinion on an idea or plan.
---

# Tənqidi baxış

Hesabatı yazan özünü tənqid edə bilmir. Buna görə tənqidi ayrı subagent aparır və hər etiraza yazılı cavab verilir.

## Addımlar
1. Hesabatın qaralaması, `findings.json` və `coverage.json` hazır olanda `verified-research:critic` subagentini çağır. Ona öz nəticəni müdafiə edən izahat vermə; yalnız faylları ver.
2. Onun cavabını `reports/<ad>.critique.json` kimi saxla.
3. Hər etiraza cavab ver:
   - `accepted`: etiraz haqlıdır. Hesabatı dəyiş (nəticəni yumşalt, rəqəmi çıxar, ssenari əlavə et) və `response_note`-da nə dəyişdiyini yaz.
   - `partially`: qismən haqlıdır. Nəyi qəbul etdiyini və nəyi yox, yaz.
   - `rejected`: haqsızdır. Hansı sübuta görə, yaz. "Razı deyiləm" yetərli deyil.
4. `high` ciddilikli etiraz qəbul olunubsa, nəticə və tövsiyələr bölməsi dəyişməlidir. Dəyişmirsə, bu `accepted` deyil.
5. Hesabata `## Tənqid və əks mövqe` bölməsi əlavə et: ən zəif fərziyyə, əks mövqe, əsas etirazlar və cavabların. Rədd etdiyin etirazları da göstər ki, oxucu özü qərar versin.
6. Tənqiddən sonra əminlik səviyyəni yenidən yaz: yüksək / orta / aşağı və niyə.

## critique.json formatı
```json
{"assumptions": [
   {"text": "Tələb növbəti üç ildə indiki tempdə artacaq", "weakest": true},
   {"text": "İdxal rüsumu dəyişməyəcək"}],
 "counter_case": "Bazar artıq doymuş ola bilər: artım qiymət artımından gəlir, həcm sabitdir.",
 "failure_cases": [{"text": "...", "source_url": "https://..."}],
 "objections": [
   {"text": "Bazar həcmi tək media mənbəyinə söykənir", "severity": "high",
    "response": "accepted", "response_note": "Rəsmi mənbə ilə təsdiq əlavə olundu, hər iki rəqəm göstərilir"}]}
```

## Skript nəyi məcbur edir
- tənqid faylı var; ən azı 3 etiraz; hər birində ciddilik, cavab və izahat;
- əks mövqe yazılıb; ən zəif fərziyyə işarələnib;
- hesabatda tənqid bölməsi var (başlıq: `## Tənqid və əks mövqe`, `## Critique and counter-case`, `## Критика и контраргументы` və ya `## Eleştiri ve karşı görüş`);
- rədd edilmiş `high` etirazlar `quality.md`-də "insan baxmalıdır" bölməsində göstərilir.

Skript etirazın və ya cavabın **haqlı** olduğunu yoxlamır; bunu istifadəçi qərar verir.

## İstifadəçi fikir və ya plan təqdim edəndə
İstifadəçi öz ideyasını qiymətləndirməyi istəyirsə, onu razı salmağa çalışma. Güclü tərəfləri qısa, zəif tərəfləri konkret yaz. İdeya zəifdirsə, bunu açıq de və nəyin onu gücləndirəcəyini göstər.
