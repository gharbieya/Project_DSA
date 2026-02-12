from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

from normalization import normalize_pattern, extract_root_letters, validate_dashed_root


@dataclass
class PatternRuleNode:
    pattern: str
    rule: str
    next: Optional["PatternRuleNode"] = None


class PatternRuleChain:
    def __init__(self) -> None:
        self.head: Optional[PatternRuleNode] = None

    def insert(self, pattern: str, rule: str) -> bool:
        current = self.head
        while current:
            if current.pattern == pattern:
                return False
            current = current.next
        node = PatternRuleNode(pattern, rule)
        node.next = self.head
        self.head = node
        return True

    def find_node(self, pattern: str) -> Optional[PatternRuleNode]:
        current = self.head
        while current:
            if current.pattern == pattern:
                return current
            current = current.next
        return None

    def find(self, pattern: str) -> bool:
        return self.find_node(pattern) is not None

    def update(self, pattern: str, rule: str) -> bool:
        node = self.find_node(pattern)
        if node is None:
            return False
        node.rule = rule
        return True

    def remove(self, pattern: str) -> bool:
        prev = None
        current = self.head
        while current:
            if current.pattern == pattern:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False


class PatternHashTable:
    """
    Hash table for patterns (pattern + rule).
    Chaining with linked lists.
    Fixed table size (37).
    """

    def __init__(self) -> None:
        self._capacity = 37
        self._size = 0
        self._buckets: List[PatternRuleChain] = [
            PatternRuleChain() for _ in range(self._capacity)
        ]

    def _normalize_and_validate(self, pattern: object) -> Optional[str]:
        if not isinstance(pattern, str):
            return None
        normalized = normalize_pattern(pattern)
        if not normalized:
            return None
        if len(normalized) < 3:
            return None
        if "ف" not in normalized or "ع" not in normalized or "ل" not in normalized:
            return None
        return normalized

    def _hash(self, key: str) -> int:
        base = 131
        mod = self._capacity
        value = 0
        for ch in key:
            value = (value * base + ord(ch)) % mod
        return value

    def insert(self, pattern: object, rule: Optional[str] = None) -> bool:
        normalized = self._normalize_and_validate(pattern)
        if normalized is None:
            return False

        normalized_rule = self._normalize_and_validate(rule or normalized)
        if normalized_rule is None:
            return False

        idx = self._hash(normalized)
        inserted = self._buckets[idx].insert(normalized, normalized_rule)
        if inserted:
            self._size += 1
        return inserted

    def contains(self, pattern: object) -> bool:
        normalized = self._normalize_and_validate(pattern)
        if normalized is None:
            return False
        idx = self._hash(normalized)
        return self._buckets[idx].find(normalized)

    def update(self, pattern: object, new_rule: str) -> bool:
        normalized = self._normalize_and_validate(pattern)
        normalized_rule = self._normalize_and_validate(new_rule)
        if normalized is None or normalized_rule is None:
            return False
        idx = self._hash(normalized)
        return self._buckets[idx].update(normalized, normalized_rule)

    def remove(self, pattern: object) -> bool:
        normalized = self._normalize_and_validate(pattern)
        if normalized is None:
            return False
        idx = self._hash(normalized)
        removed = self._buckets[idx].remove(normalized)
        if removed:
            self._size -= 1
        return removed

    def get_rule(self, pattern: object) -> Optional[str]:
        normalized = self._normalize_and_validate(pattern)
        if normalized is None:
            return None
        idx = self._hash(normalized)
        node = self._buckets[idx].find_node(normalized)
        return None if node is None else node.rule

    def iter_patterns(self):
        for chain in self._buckets:
            current = chain.head
            while current:
                yield current.pattern
                current = current.next

    def size(self) -> int:
        return self._size

    def load_patterns_from_file(self, file_path: str) -> int:
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                if self.insert(raw):
                    count += 1
        return count

    def derive(self, raw_root: str, pattern: object) -> Optional[str]:
        rule = self.get_rule(pattern)
        if rule is None:
            return None
        return derive_from_normalized_pattern(raw_root, rule)


def derive_from_normalized_pattern(raw_root: str, normalized_pattern: str) -> Optional[str]:
    if not validate_dashed_root(raw_root):
        return None

    letters = extract_root_letters(raw_root)
    if letters is None:
        return None
    f, a, l = letters

    result = []
    for ch in normalized_pattern:
        if ch == "ف":
            result.append(f)
        elif ch == "ع":
            result.append(a)
        elif ch == "ل":
            result.append(l)
        else:
            result.append(ch)
    return "".join(result)