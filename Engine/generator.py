from __future__ import annotations
from typing import List, Optional, Iterable, TypedDict

from Data_Structures.root_tree import RootBST
from Data_Structures.hash_table import PatternHashTable

#Structured result type ----
class GenerationResult(TypedDict):
    """
    ok      : True if generation succeeded
    root    : input root
    pattern : input pattern
    word    : derived word if success
    error   : error code if failure
    """
    ok: bool
    root: str
    pattern: Optional[str]
    word: Optional[str]
    error: Optional[str]

# Morphological Generator ------
class MorphologicalGenerator:
    """
    Generates derived words from (root, pattern)
    ONLY component allowed to derive
    """

    def __init__(self, root_tree: RootBST, pattern_table: PatternHashTable) -> None:
        self._roots = root_tree
        self._patterns = pattern_table

    #Generate one derived word
    def generate_one(
        self,
        raw_root: str,
        raw_pattern: str,
        store: bool = True,
    ) -> GenerationResult:
        #Check root existence
        if self._roots.search(raw_root) is None:
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "ROOT_NOT_FOUND",
            }

        #Check pattern existence
        if not self._patterns.contains(raw_pattern):
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "PATTERN_NOT_FOUND",
            }

        #Derive word using hash table
        derived = self._patterns.derive(raw_root, raw_pattern)
        if derived is None:
            return {
                "ok": False,
                "root": raw_root,
                "pattern": raw_pattern,
                "word": None,
                "error": "DERIVATION_FAILED",
            }

        #Store derived word in BST linked list
        if store:
            self._roots.add_derived_word(raw_root, derived)

        return {
            "ok": True,
            "root": raw_root,
            "pattern": raw_pattern,
            "word": derived,
            "error": None,
        }

    #Generate full morphological family --------
    def generate_family(self, raw_root: str) -> List[GenerationResult]:
        """
        Generate all possible derived words for a given root
        using all patterns stored in the hash table
        """
                
        #Check root existance
        if self._roots.search(raw_root) is None:
            return [{
                "ok": False,
                "root": raw_root,
                "pattern": None,
                "word": None,
                "error": "ROOT_NOT_FOUND",
            }]

        results: List[GenerationResult] = []
        for pattern in self._patterns.iter_patterns():
            results.append(self.generate_one(raw_root, pattern, store=True))
        return results