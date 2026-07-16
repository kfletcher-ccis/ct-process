from __future__ import annotations
import re
from datetime import datetime
from typing import Iterable, List, Sequence
from config import NULL_VALUES

def normalize_lookup_id(value) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if value.endswith('.0') and value[:-2].isdigit():
        value = value[:-2]
    if not value:
        return ""
    return value.zfill(7) if len(value) < 7 else value

def clean_null_value(value) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if value.endswith('.0') and value[:-2].isdigit():
        value = value[:-2]
    return "" if value.upper() in {v.upper() for v in NULL_VALUES} else value

def split_pipe_values(value) -> List[str]:
    value = clean_null_value(value)
    if not value:
        return []
    return [clean_null_value(v) for v in str(value).split('||') if clean_null_value(v)]

def safe_get(values: Sequence[str], index: int) -> str:
    return values[index] if index < len(values) else ""

def parse_date(date_text: str):
    txt = clean_null_value(date_text)
    if not txt:
        return None
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(txt, fmt)
        except ValueError:
            pass
    return None

def date_sort_key(date_text: str, ascending=True):
    dt = parse_date(date_text)
    if dt is None:
        return datetime.min if ascending else datetime.max
    return dt

def year_from_date(date_text: str) -> str:
    dt = parse_date(date_text)
    return str(dt.year) if dt else ""

def yymmdd_from_date(date_text: str) -> str:
    dt = parse_date(date_text)
    return dt.strftime("%y%m%d") if dt else "000000"

def build_import_id(lookup_id: str, record_type: str, graduation_date: str, counter: int) -> str:
    return f"{normalize_lookup_id(lookup_id)}-{record_type}-{yymmdd_from_date(graduation_date)}{counter}"

def is_email(value: str) -> bool:
    return "@" in clean_null_value(value)

def normalize_duplicate_columns(columns: Iterable[str]) -> List[str]:
    counts = {}
    output = []
    for raw in columns:
        col = str(raw).strip()
        # Pandas may produce Header, Header.1, Header.2; normalize to Header, Header_2, Header_3.
        base = re.sub(r"\.\d+$", "", col)
        counts[base] = counts.get(base, 0) + 1
        output.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    return output

def repeated_values(row, base_name: str, max_count: int | None = None) -> List[str]:
    values=[]
    if max_count is None:
        max_count=50
    for i in range(1, max_count+1):
        field = base_name if i == 1 else f"{base_name}_{i}"
        if field not in row.index:
            if i == 1:
                continue
            # keep scanning lightly because some duplicate-normalized sets may skip in odd cases
            continue
        val = clean_null_value(row.get(field, ""))
        if val:
            values.append(val)
    return values

from datetime import date, timedelta


def is_within_last_days(
    date_text: str,
    days: int = 90,
    as_of_date=None
) -> bool:
    """
    Return True when date_text is within the last N days,
    inclusive of today.

    Expected source date format includes M/D/YYYY or MM/DD/YYYY.
    """

    dt = parse_date(date_text)

    if dt is None:
        return False

    if as_of_date is None:
        as_of_date = date.today()

    candidate = dt.date()

    start_date = as_of_date - timedelta(days=days)

    return start_date <= candidate <= as_of_date

def normalize_email(value):
    if value is None:
        return ""

    return str(value).strip().lower()