"""Ədəd tanıma sınaqları. DSK cədvəllərində ədədlər yanaşı durur: '58 997,7 103,7'."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from verify_report import raw_numbers, value_in, splits_into

t = "Pərakəndə ticarət dövriyyəsi 58 997,7 103,7"
assert raw_numbers(t) == ["58 997,7", "103,7"]
assert value_in("58 997,7", t) and value_in("58997.7", t) and value_in("103,7", t)
assert not value_in("8 997,7", t) and not value_in("58 997", t)
assert not value_in("997,7", t) and not value_in("61 200,0", t)
assert value_in("3,7", "real ifadədə 3,7 faiz")
assert not value_in("3,7", "real ifadədə 13,7 faiz") and not value_in("3,7", "3,75 faiz")
assert value_in("51.6", "51,6%") and value_in("2023", "2023-cü ildə")
assert splits_into("30 439 102", {"30439", "102"}) and not splits_into("30 439 102", {"30439"})
assert value_in("102", "30 439 102") and not value_in("39", "30 439 102")
assert value_in("10 180,8", "sayı 10\u00a0180,8 min")
e = "Revenue was $1,234,567.89 in 2024, up 12.5% year over year."
assert raw_numbers(e) == ["1,234,567.89", "2024", "12.5"]
assert value_in("1,234,567.89", e) and value_in("12.5", e) and not value_in("234,567.89", e) and not value_in("2.5", e)
assert value_in("1.234.567,89", "Der Umsatz betrug 1.234.567,89 Euro") and not value_in("1.234.567", "betrug 1.234.567,89 Euro")
assert value_in("3,400", "employed 3,400 people") and not value_in("400", "employed 3,400 people")
# tarixlər və çoxhissəli dəyərlər (real sınaqda tapıldı: texniki araşdırmada tarixlər yanlış rədd edilirdi)
assert value_in("November 8, 2029", "17 17.12 Yes September 26, 2024 November 8, 2029")
assert value_in("2032-04-30", '"eol":"2032-04-30"') and value_in("8 noyabr 2029", "8 noyabr 2029-cu il")
assert not value_in("November 8, 2029", "November 18, 2029") and not value_in("2032-04-30", "2032-04-29")
assert not value_in("2032-04-30", "2032-04-301") and not value_in("8 noyabr 2029", "18 noyabr 2029")
print("KEÇDİ   ədəd tanıma (31 yoxlama)")
