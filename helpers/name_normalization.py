"""
Name normalization helpers for CT Process ETL.

Purpose:
- Correct obvious casing defects from source exports.
- Preserve common name particles and apostrophes/hyphens.
- Add practical handling for Mc/Mac-style names without pretending this is a perfect genealogy/name parser.

Recommended application fields:
- FirstName
- MidName
- LastName
- NickName
- AliasName / AliasName_2 ... AliasName_n

Do NOT apply to addresses, organizations, locations, email addresses, or free-text notes.
"""

from __future__ import annotations
import re

LOWERCASE_PARTICLES = {
    "da", "de", "del", "der", "di", "du", "la", "le", "van", "von", "of", "the"
}

# Known exceptions can be expanded as discovered in real data.
EXACT_EXCEPTIONS = {
    "mcdonald": "McDonald",
    "mcdougal": "McDougal",
    "mcdougall": "McDougall",
    "mcintyre": "McIntyre",
    "mckenzie": "McKenzie",
    "mckinney": "McKinney",
    "mclaughlin": "McLaughlin",
    "mcmillan": "McMillan",
    "mcnamara": "McNamara",
    "macdonald": "MacDonald",
}


def normalize_name(value: str) -> str:
    """Normalize a personal-name value while preserving blank values."""
    if value is None:
        return ""

    text = str(value).strip()
    if not text:
        return ""

    # Preserve all-uppercase short initials like "J" but normalize words.
    tokens = re.split(r"(\s+)", text)
    return "".join(_normalize_space_token(tok) if not tok.isspace() else tok for tok in tokens)


def _normalize_space_token(token: str) -> str:
    # A token may contain hyphens and apostrophes.
    hyphen_parts = token.split("-")
    return "-".join(_normalize_apostrophe_part(part) for part in hyphen_parts)


def _normalize_apostrophe_part(part: str) -> str:
    apostrophe_parts = re.split(r"([’'])", part)
    normalized = []
    capitalize_next = True

    for sub in apostrophe_parts:
        if sub in {"'", "’"}:
            normalized.append(sub)
            capitalize_next = True
            continue
        if not sub:
            continue
        normalized.append(_normalize_word(sub, force_capitalize=capitalize_next))
        capitalize_next = False

    return "".join(normalized)


def _normalize_word(word: str, force_capitalize: bool = True) -> str:
    raw = word.strip()
    if not raw:
        return ""

    lower = raw.lower()
    if lower in EXACT_EXCEPTIONS:
        return EXACT_EXCEPTIONS[lower]

    if lower in LOWERCASE_PARTICLES and not force_capitalize:
        return lower

    # Initials, e.g. "J" or "J."
    if re.fullmatch(r"[A-Za-z]\.?", raw):
        return raw.upper()

    # Mc + letter: McDonald, McDougal, McArthur, etc.
    if lower.startswith("mc") and len(lower) > 2 and lower[2].isalpha():
        return "Mc" + lower[2].upper() + lower[3:]

    # Conservative Mac + letter rule. This may not fit every name, but catches common Camel-case issues.
    if lower.startswith("mac") and len(lower) > 3 and lower[3].isalpha():
        return "Mac" + lower[3].upper() + lower[4:]

    return lower[:1].upper() + lower[1:]
