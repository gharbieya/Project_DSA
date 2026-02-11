from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DerivedWordNode:
    word: str
    next: Optional["DerivedWordNode"] = None


class DerivedWordList:
    """
    Linked list to store derived words for a root.
    Ensures uniqueness by linear search.
    """

    def __init__(self) -> None:
        self.head: Optional[DerivedWordNode] = None
        self._size: int = 0

    def add(self, word: str) -> bool:
        if self.contains(word):
            return False
        node = DerivedWordNode(word)
        node.next = self.head
        self.head = node
        self._size += 1
        return True

    def contains(self, word: str) -> bool:
        current = self.head
        while current:
            if current.word == word:
                return True
            current = current.next
        return False

    def to_list(self) -> List[str]:
        words: List[str] = []
        current = self.head
        while current:
            words.append(current.word)
            current = current.next
        return words

    def __len__(self) -> int:
        return self._size