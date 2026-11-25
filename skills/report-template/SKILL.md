---
name: report-template
description: Use when writing the final research or analysis report. Gives the standard structure and the sourcing rules the verification script checks.
---

# Hesabat şablonu

Şablon: [templates/report.md](templates/report.md). Hesabatı istifadəçinin dilində yaz.

Yoxlama skripti iki şeyi mətndə axtarır, ona görə bunları dəqiq işlət:
- **Əsas rəqəmlər bölməsinin başlığı** bunlardan biri olmalıdır: `## Əsas rəqəmlər`, `## Key figures`, `## Ключевые показатели`, `## Temel rakamlar`. Başqa dildə yazırsansa, `## Key figures` işlət.
- **Təxmin işarəsi:** `TƏXMİN`, `ESTIMATE`, `ОЦЕНКА` və ya `TAHMİN` (böyük hərflərlə).

- **Tənqid bölməsinin başlığı:** `## Tənqid və əks mövqe`, `## Critique and counter-case`, `## Критика и контраргументы` və ya `## Eleştiri ve karşı görüş`.

Qaydalar:
- Hesabatdakı hər rəqəm `findings.json`-dakı bir tapıntıya uyğun gəlməlidir (eyni yazılışla).
- Əsas rəqəmlər cədvəlində hər sətirdə mənbə linki olmalıdır.
- Faktları, təhlili və tövsiyələri ayrı bölmələrdə saxla.
- Tapılmayan data boşluqlar bölməsində yazılır; `coverage.json`-dakı hər `partial` və `not_found` bölmə orada görünməlidir.
- Əsas rəqəm iki mənbədə fərqlidirsə, hər ikisini göstər.
- Hesabatın sonunda skriptin yaratdığı `<ad>.quality.md` faylına keçid ver.
