from __future__ import annotations
from typing import List, Optional, Iterable, TypedDict

from Data_Structures.root_tree import RootBST
from Data_Structures.hash_table import PatternHashTable


def _iter_patterns(table: PatternHashTable) -> Iterable[str]:
    for chain in table._buckets:
        current = chain.head
        while current:
            yield current.pattern
            current = current.next


class GenerationResult(TypedDict):
    ok: bool
    root: str
    pattern: Optional[str]
    word: Optional[str]
    error: Optional[str]


class MorphologicalGenerator:
    """
    Generates derived words from (root, pattern).
    ONLY component allowed to derive.
    """

    def __init__(self, root_tree: RootBST, pattern_table: PatternHashTable) -> None:
        self._roots = root_tree
        self._patterns = pattern_table

    def generate_one(
        self,
        raw_root: str,
        raw_pattern: str,
        store: bool = True,
    ) -> GenerationResult:
        if self._roots.search(raw_root) is None:
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "ROOT_NOT_FOUND",
            }

        if not self._patterns.contains(raw_pattern):
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "PATTERN_NOT_FOUND",
            }

        derived = self._patterns.derive(raw_root, raw_pattern)
        if derived is None:
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "DERIVATION_FAILED",
            }

        if store:
            self._roots.add_derived_word(raw_root, derived)

        return {
            "ok": True,
            "root": raw_root,
            "pattern": raw_pattern,
            "word": derived,
            "error": None,
        }

    def generate_family(self, raw_root: str) -> List[GenerationResult]:
        if self._roots.search(raw_root) is None:
            return [{
                "ok": False,
                "root": raw_root,
                "pattern": None,
                "word": None,
                "error": "ROOT_NOT_FOUND",
            }]

        results: List[GenerationResult] = []
        for pattern in _iter_patterns(self._patterns):
            results.append(self.generate_one(raw_root, pattern, store=True))
        return results