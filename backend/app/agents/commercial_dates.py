"""Uruguayan commercial dates agents may mention, from a static list (the model never guesses)."""

import json
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "commercial_dates_uy.json"


@dataclass(frozen=True, slots=True)
class CommercialDate:
    name: str
    start: date
    end: date

    def label(self) -> str:
        """ "Black Friday (2026-11-27)" or "Feria Ideas+ (2026-12-01 to 2026-12-24)"."""
        if self.start == self.end:
            return f"{self.name} ({self.start.isoformat()})"
        return f"{self.name} ({self.start.isoformat()} to {self.end.isoformat()})"


@cache
def _entries() -> tuple[dict[str, str], ...]:
    return tuple(json.loads(DATA_PATH.read_text(encoding="utf-8")))


def _occurrences(entry: dict[str, str], year: int) -> list[CommercialDate]:
    """A `YYYY-MM-DD` entry is that date only; a `MM-DD` entry repeats every year."""
    if len(entry["date"]) == len("YYYY-MM-DD"):
        start = date.fromisoformat(entry["date"])
        end = date.fromisoformat(entry.get("end", entry["date"]))
        return [CommercialDate(entry["name"], start, end)] if start.year == year else []
    month, day = map(int, entry["date"].split("-"))
    start = date(year, month, day)
    return [CommercialDate(entry["name"], start, start)]


def commercial_dates_between(start: date, end: date) -> list[CommercialDate]:
    """Dates that overlap `start..end` (inclusive), earliest first."""
    found = [
        occurrence
        for year in range(start.year, end.year + 1)
        for entry in _entries()
        for occurrence in _occurrences(entry, year)
        if occurrence.start <= end and occurrence.end >= start
    ]
    return sorted(found, key=lambda item: (item.start, item.name))
