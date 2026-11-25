---
name: source-quality
description: Use whenever a source is about to be relied on - to rate its quality, decide whether a figure needs a second independent source, and resolve disagreements between sources.
---

# Mənbə keyfiyyəti

Hər mənbəni istifadə etməzdən əvvəl qiymətləndir. Nəticəni tapıntıya `source_tier` (1–6) kimi yaz.

## Beş sual
1. **Kimdir?** Datanı özü toplayan qurumdur (ilkin), yoxsa başqasından köçürən (ikinci dərəcəli)? Köçürəndirsə, ilkin mənbəyə get.
2. **Necə ölçüb?** Metodologiya, nümunə ölçüsü, tərif açıqlanıb? Açıqlanmayıbsa, səviyyə ən yaxşı halda 4-dür.
3. **Nə vaxt?** Data hansı dövrə aiddir və nə vaxt dərc olunub? Daha yeni buraxılış varmı?
4. **Marağı nədir?** Rəqəmi dərc edənin onu şişirtməkdə və ya azaltmaqda marağı varmı (satıcı, lobbi, reklam)? Varsa, müstəqil təsdiq məcburidir.
5. **Başqaları nə deyir?** Müstəqil mənbə eyni şeyi göstərirmi?

## Səviyyələr
| Səviyyə | Nədir | Təkbaşına əsas rəqəm üçün yetərlidir? |
|---|---|---|
| 1 | İlkin rəsmi mənbə: statistika qurumu, mərkəzi bank, tənzimləyici, qanun mətni, auditdən keçmiş şirkət hesabatı | bəli |
| 2 | Beynəlxalq təşkilat, resenziyalı elmi nəşr | bəli |
| 3 | Şirkətin öz açıqlaması (sayt, press-reliz) | yox, ikinci mənbə lazımdır |
| 4 | Araşdırma şirkəti, sahə assosiasiyası, preprint | yox, ikinci mənbə lazımdır |
| 5 | Media | yox, 1–3 səviyyəli mənbə ilə təsdiq lazımdır |
| 6 | Bloq, forum, sosial media, elan saytı | yox, 1–3 səviyyəli mənbə ilə təsdiq lazımdır |

## Skript nəyi məcbur edir
- `source_tier` hər fakt üçün yazılmalıdır.
- Tanınmış domenlərin səviyyəsi `scripts/trusted_domains.txt`-dən gəlir və şişirdilə bilməz. Dövlət domenləri avtomatik 1 sayılır.
- Siyahıda olmayan mənbəyə 1–3 səviyyə verirsənsə, `tier_reason` yaz: bu qurum kimdir və niyə ilkin mənbədir. Bu mənbələr keyfiyyət xülasəsində "insan baxmalıdır" bölməsində göstərilir. Siyahını özün dəyişmə.
- Nəticənin söykəndiyi tapıntılara `"key": true` yaz. Əsas rəqəm ya 1–2 səviyyəli mənbədən olmalı, ya da başqa domendəki müstəqil mənbə ilə təsdiqlənməlidir (`corroboration`).
- Müqayisə üçün hər iki mənbədə `value_num` yaz: eyni vahidə çevrilmiş ədəd (məsələn, `58 997,7 mln` və `59,0 mlrd` üçün 58997700000 və 59000000000).
- Mənbələr 10%-dən çox fərqlənirsə, səbəbi tap (fərqli tərif, dövr, valyuta, əhatə), `discrepancy_note` yaz və hesabatda hər iki rəqəmi göstər. Səbəbi tapmasan, bunu yaz; rəqəmlərdən birini səssizcə seçmə.
- 2 ildən köhnə data üçün əvvəlcə yenisini axtar. Yoxdursa `stale_note` yaz: harada axtardın və niyə yenisi yoxdur.

## Müstəqillik
İki mənbə eyni ilkin mənbədən köçürübsə, bu bir mənbədir. Müstəqil təsdiq fərqli üsulla və ya fərqli qurum tərəfindən əldə edilmiş rəqəm deməkdir (məsələn, milli statistika və güzgü ticarət datası; şirkət hesabatı və tənzimləyicinin statistikası). Skript yalnız domenin fərqli olduğunu yoxlayır; həqiqi müstəqilliyi sən və `fact-checker` yoxlayırsınız.
