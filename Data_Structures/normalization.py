from __future__ import annotations

DIACRITICS = set([
    "\u064b", "\u064c", "\u064d", "\u064e",
    "\u064f", "\u0650", "\u0651", "\u0652",
    "\u0670"
])

ALEF_VARIANTS = {
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
}

TATWEEL = "\u0640"


def normalize_common(text: str) -> str:
    """Shared normalization for Arabic text."""
    if not text:
        return ""
    text = text.replace(" ", "").replace("\t", "").replace("\n", "")
    text = text.replace(TATWEEL, "")
    text = "".join(ALEF_VARIANTS.get(ch, ch) for ch in text)
    text = "".join(ch for ch in text if ch not in DIACRITICS)
    return text


def normalize_root(raw_root: str) -> str:
    """Normalize and remove dashes."""
    normalized = normalize_common(raw_root)
    return "".join(ch for ch in normalized if ch != "-")


def normalize_pattern(pattern: str) -> str:
    """Normalize pattern (no dashes)."""
    return normalize_common(pattern)


def extract_root_letters(raw_root: str):
    """Return the 3 root letters as a tuple, or None if invalid."""
    normalized = normalize_root(raw_root)
    if len(normalized) != 3:
        return None
    return normalized[0], normalized[1], normalized[2]