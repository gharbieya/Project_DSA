from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Generator, Dict

from linked_list import DerivedWordList
from normalization import normalize_root, normalize_common


def is_arabic_letter(ch: str) -> bool:
    """
    Arabic letters are mainly in: \u0621 - \u064A
    Includes Alef Maksura (ى = \u0649).
    """
    return "\u0621" <= ch <= "\u064A"


def validate_dashed_root_with_reason(raw_root: str) -> Optional[str]:
    normalized = normalize_common(raw_root)

    letters_only = normalized.replace("-", "")
    if not letters_only:
        return "Root must contain letters."
    if not all(is_arabic_letter(ch) for ch in letters_only):
        return "Only Arabic letters are allowed."
    if len(letters_only) != 3:
        return "Root must have exactly 3 letters."

    if normalized.count("-") != 2:
        return "Root must contain exactly two dashes (example: ك-ت-ب)."

    parts = normalized.split("-")
    if not all(parts):
        return "Missing letter between dashes."
    if not all(len(part) == 1 for part in parts):
        return "Each part must be a single letter."

    return None


def validate_dashed_root(raw_root: str) -> bool:
    return validate_dashed_root_with_reason(raw_root) is None


def to_compact_root(raw_root: str) -> str:
    """
    Convert a dashed root to compact form: ك-ت-ب -> كتب
    """
    compact = normalize_root(raw_root)
    if len(compact) != 3:
        raise ValueError(f"Expected 3 letters, got {len(compact)}")
    return compact


def format_dashed(compact_root: str) -> str:
    """
    Convert compact root to dashed form: كتب -> ك-ت-ب
    """
    if len(compact_root) != 3:
        raise ValueError(f"Root must be exactly 3 letters, got {len(compact_root)}")
    if not all(is_arabic_letter(ch) for ch in compact_root):
        raise ValueError("Root must contain only Arabic letters.")
    return "-".join(compact_root)


# ---------------------------
# BST Node
# ---------------------------

@dataclass
class RootNode:
    root: str  # compact root: كتب
    derived: DerivedWordList
    left: Optional["RootNode"] = None
    right: Optional["RootNode"] = None


# ---------------------------
# BST for Roots
# ---------------------------

class RootBST:
    """
    Binary Search Tree storing Arabic roots in compact form.
    Unicode ordering is used by Python string comparison.
    """

    def __init__(self) -> None:
        self.root: Optional[RootNode] = None
        self._size: int = 0

    # ---------- Core Operations ----------

    def insert(self, raw_root: str) -> RootNode:
        error = validate_dashed_root_with_reason(raw_root)
        if error:
            raise ValueError(error)

        compact = to_compact_root(raw_root)

        if self.root is None:
            self.root = RootNode(root=compact, derived=DerivedWordList())
            self._size += 1
            return self.root

        current = self.root
        while True:
            if compact == current.root:
                return current
            elif compact < current.root:
                if current.left is None:
                    current.left = RootNode(root=compact, derived=DerivedWordList())
                    self._size += 1
                    return current.left
                current = current.left
            else:
                if current.right is None:
                    current.right = RootNode(root=compact, derived=DerivedWordList())
                    self._size += 1
                    return current.right
                current = current.right

    def search(self, raw_root: str) -> Optional[RootNode]:
        if not validate_dashed_root(raw_root):
            return None

        compact = to_compact_root(raw_root)
        current = self.root
        while current:
            if compact == current.root:
                return current
            elif compact < current.root:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, raw_root: str) -> bool:
        error = validate_dashed_root_with_reason(raw_root)
        if error:
            return False

        compact = to_compact_root(raw_root)
        self.root, deleted = self._delete_recursive(self.root, compact)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_recursive(self, node: Optional[RootNode], compact: str):
        if node is None:
            return None, False

        if compact < node.root:
            node.left, deleted = self._delete_recursive(node.left, compact)
            return node, deleted
        elif compact > node.root:
            node.right, deleted = self._delete_recursive(node.right, compact)
            return node, deleted
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            successor = self._min_node(node.right)
            node.root = successor.root
            node.derived = successor.derived
            node.right, _ = self._delete_recursive(node.right, successor.root)
            return node, True

    def _min_node(self, node: RootNode) -> RootNode:
        current = node
        while current.left:
            current = current.left
        return current

    def add_derived_word(self, raw_root: str, derived_word: str) -> bool:
        node = self.search(raw_root)
        if node is None:
            return False
        return node.derived.add(derived_word)

    # ---------- Input Helpers ----------

    def add_root_from_user_input(self, user_input: str) -> bool:
        """
        Explicit user insertion (dynamic insertion allowed by spec).
        """
        size_before = self._size
        self.insert(user_input)
        return self._size > size_before

    def load_roots_from_file(self, file_path: str) -> int:
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                size_before = self._size
                try:
                    self.insert(raw)
                    if self._size > size_before:
                        count += 1
                except ValueError:
                    continue
        return count

    # ---------- Batch Operations ----------

    def get_all_derivatives(self) -> Dict[str, List[str]]:
        result = {}

        def _collect(node: Optional[RootNode]):
            if node is None:
                return
            _collect(node.left)
            result[format_dashed(node.root)] = node.derived.to_list()
            _collect(node.right)

        _collect(self.root)
        return result

    def count_total_derivatives(self) -> int:
        total = 0

        def _count(node: Optional[RootNode]):
            nonlocal total
            if node is None:
                return
            total += len(node.derived)
            _count(node.left)
            _count(node.right)

        _count(self.root)
        return total

    # ---------- Traversal / Utility ----------

    def inorder(self) -> Generator[str, None, None]:
        def _inorder(node: Optional[RootNode]):
            if node is None:
                return
            yield from _inorder(node.left)
            yield node.root
            yield from _inorder(node.right)

        yield from _inorder(self.root)

    def list_roots(self, dashed: bool = True) -> List[str]:
        roots = list(self.inorder())
        if dashed:
            return [format_dashed(r) for r in roots]
        return roots

    def size(self) -> int:
        return self._size

    def height(self) -> int:
        def _height(node: Optional[RootNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)