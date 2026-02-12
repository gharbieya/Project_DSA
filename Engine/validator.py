from __future__ import annotations
from typing import Dict, Optional, Iterable

from Data_Structures.root_tree import RootBST
from Data_Structures.hash_table import PatternHashTable
from Data_Structures.normalization import normalize_common
from Engine.generator import MorphologicalGenerator


def _iter_patterns(table: PatternHashTable) -> Iterable[str]:
    for chain in table._buckets:
        current = chain.head
        while current:
            yield current.pattern
            current = current.next


class MorphologicalValidator:
    """
    Validates whether a word belongs to a root.
    MUST reuse MorphologicalGenerator.
    """

    def __init__(
        self,
        generator: MorphologicalGenerator,
        root_tree: RootBST,
        pattern_table: PatternHashTable,
    ) -> None:
        self._generator = generator
        self._roots = root_tree
        self._patterns = pattern_table

    def validate(self, raw_root: str, raw_word: str) -> Dict[str, Optional[str]]:
        if self._roots.search(raw_root) is None:
            return {"result": "NON", "pattern": None}

        normalized_word = normalize_common(raw_word)

        for pattern in _iter_patterns(self._patterns):
            gen = self._generator.generate_one(raw_root, pattern)
            if gen["ok"] and gen["word"] is not None:
                if normalize_common(gen["word"]) == normalized_word:
                    return {"result": "OUI", "pattern": pattern}

        return {"result": "NON", "pattern": None}