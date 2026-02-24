from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class DerivedWordNode:
    word: str
    count: int = 1
    next: Optional["DerivedWordNode"] = None


class DerivedWordList:
    """
    Linked list to store derived words for a root.
    Ensures uniqueness and tracks frequency.
    """

    def __init__(self) -> None:
        self.head: Optional[DerivedWordNode] = None
        self._size: int = 0

    def add(self, word: str) -> bool:
        current = self.head
        while current:
            if current.word == word:
                current.count += 1
                return False
            current = current.next

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

    def to_items(self) -> List[Tuple[str, int]]:
        items: List[Tuple[str, int]] = []
        current = self.head
        while current:
            items.append((current.word, current.count))
            current = current.next
        return items

    def __len__(self) -> int:
        return self._size