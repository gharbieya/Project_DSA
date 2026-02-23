from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class DerivedWordNode:
    word: str  #the derived word
    count: int = 1
    next: Optional["DerivedWordNode"] = None


#Linked list to store derived words for a root in BST
class DerivedWordList:
 
    def __init__(self) -> None:
        self.head: Optional[DerivedWordNode] = None
        self._size: int = 0  #number of distinct derived words

    #add a new derived word
    def add(self, word: str) -> bool:
        """
        If word already exists:
            - Increase its frequency not size
            - Return False
        If word is new:
            - Insert at head
            - Increase size
            - Return True
        """
                
        current = self.head
        #Search if word already exists
        while current:
            if current.word == word:
                current.count += 1
                return False
            current = current.next

        #insert new word at the beginning
        node = DerivedWordNode(word)
        node.next = self.head
        self.head = node
        self._size += 1
        return True

    #Check if word exists
    def contains(self, word: str) -> bool:
        current = self.head
        while current:
            if current.word == word:
                return True
            current = current.next
        return False
    
    #return list of derived words
    def to_list(self) -> List[str]:
        words: List[str] = []
        current = self.head
        while current:
            words.append(current.word)
            current = current.next
        return words

    #return list of derived words with frequency
    def to_items(self) -> List[Tuple[str, int]]:
        items: List[Tuple[str, int]] = []
        current = self.head
        while current:
            items.append((current.word, current.count))
            current = current.next
        return items

    #return number of distinct derived words
    def __len__(self) -> int:
        return self._size