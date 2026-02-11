from __future__ import annotations

DIACRITICS = set([
    "\u064b",  # Tanwin Fath
    "\u064c",  # Tanwin Damm
    "\u064d",  # Tanwin Kasr
    "\u064e",  # Fatha
    "\u064f",  # Damma
    "\u0650",  # Kasra
    "\u0651",  # Shadda
    "\u0652",  # Sukun
    "\u0670",  # Superscript Alef
])

# All diacritics except Shadda
DIACRITICS_NO_SHADDA = DIACRITICS - {"\u0651"}

ALEF_VARIANTS = {
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
}

TATWEEL = "\u0640"


def _normalize_base(text: str) -> str:
    if not text:
        return ""
    text = text.replace(" ", "").replace("\t", "").replace("\n", "")
    text = text.replace(TATWEEL, "")
    text = "".join(ALEF_VARIANTS.get(ch, ch) for ch in text)
    return text


def normalize_common(text: str) -> str:
    """Normalize Arabic text and remove ALL diacritics (including shadda)."""
    text = _normalize_base(text)
    text = "".join(ch for ch in text if ch not in DIACRITICS)
    return text


def normalize_root(raw_root: str) -> str:
    """Normalize root and remove dashes."""
    normalized = normalize_common(raw_root)
    return "".join(ch for ch in normalized if ch != "-")


def normalize_pattern(pattern: str) -> str:
    """
    Normalize pattern:
    - remove harakat (diacritics) but KEEP shadda
    - normalize Alef variants
    """
    text = _normalize_base(pattern)
    text = "".join(ch for ch in text if ch not in DIACRITICS_NO_SHADDA)
    return text


def extract_root_letters(raw_root: str):
    normalized = normalize_root(raw_root)
    if len(normalized) != 3:
        return None
    return normalized[0], normalized[1], normalized[2]


def is_arabic_letter(ch: str) -> bool:
    return "\u0621" <= ch <= "\u064A"


def validate_dashed_root(raw_root: str) -> bool:
    if not isinstance(raw_root, str):
        return False

    normalized = normalize_common(raw_root)
    if normalized.count("-") != 2:
        return False

    parts = normalized.split("-")
    if len(parts) != 3 or not all(parts):
        return False

    letters = "".join(parts)
    if len(letters) != 3:
        return False

    if not all(is_arabic_letter(ch) for ch in letters):
        return False

    return True