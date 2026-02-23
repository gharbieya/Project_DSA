from __future__ import annotations
from typing import Optional, Iterable, TypedDict, Literal

from Data_Structures.root_tree import RootBST
from Data_Structures.hash_table import PatternHashTable
from Data_Structures.normalization import normalize_common
from Engine.generator import MorphologicalGenerator

# Structured Result Type -----
class ValidationResult(TypedDict):
    """
    result  : "OUI" if word is valid for root, otherwise "NON"
    pattern : pattern that produced the word (if valid)
    """
    result: Literal["OUI", "NON"]
    pattern: Optional[str]

# Morphological Validator -------
class MorphologicalValidator:
    """
    Validates whether a word belongs to a given root
    Reuses MorphologicalGenerator
    """

    def __init__(
        self,
        generator: MorphologicalGenerator,
        root_tree: RootBST,
        pattern_table: PatternHashTable,
    ) -> None:
        
        """
        Constructor receives:
        - generator     : the derivation component
        - root_tree     : BST storing roots
        - pattern_table : hash table storing patterns
        """
        self._generator = generator
        self._roots = root_tree
        self._patterns = pattern_table

    def validate(self, raw_root: str, raw_word: str) -> ValidationResult:
        #Check root existence
        if self._roots.search(raw_root) is None:
            return {"result": "NON", "pattern": None}

        #Normalize input word
        normalized_word = normalize_common(raw_word)

        #Try all patterns (exhaustive validation)
        for pattern in self._patterns.iter_patterns():
            gen = self._generator.generate_one(raw_root, pattern, store=False)
            if gen["ok"] and gen["word"] is not None:
                if normalize_common(gen["word"]) == normalized_word:
                    self._roots.add_derived_word(raw_root, gen["word"])
                    return {"result": "OUI", "pattern": pattern}

        return {"result": "NON", "pattern": None}