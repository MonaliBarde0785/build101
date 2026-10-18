import json
from datetime import date

from app.agents.commercial_dates import DATA_PATH, commercial_dates_between


def names(start: date, end: date) -> list[str]:
    return [item.name for item in commercial_dates_between(start, end)]


def test_one_off_date_inside_the_window() -> None:
    assert names(date(2026, 11, 23), date(2026, 11, 29)) == ["Black Friday"]


def test_yearly_date_repeats_in_later_years() -> None:
    assert names(date(2027, 12, 20), date(2027, 12, 26)) == ["Navidad"]
    assert names(date(2027, 6, 15), date(2027, 6, 21)) == ["Día de los Abuelos"]


def test_window_across_new_year_is_sorted() -> None:
    assert names(date(2026, 12, 22), date(2027, 1, 7)) == [
        "Feria Ideas+",
        "Navidad",
        "Día de Reyes",
    ]


def test_range_overlapping_only_its_tail_still_counts() -> None:
    found = commercial_dates_between(date(2026, 12, 24), date(2026, 12, 24))
    assert [item.name for item in found] == ["Feria Ideas+"]


def test_one_off_date_does_not_repeat() -> None:
    assert names(date(2027, 5, 1), date(2027, 5, 31)) == []


def test_label_shows_single_day_and_range() -> None:
    found = commercial_dates_between(date(2026, 11, 20), date(2026, 12, 5))
    assert [item.label() for item in found] == [
        "Black Friday (2026-11-27)",
        "Feria Ideas+ (2026-12-01 to 2026-12-24)",
    ]


def test_every_entry_cites_a_source() -> None:
    entries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert all(entry["source"].startswith("https://") for entry in entries)
