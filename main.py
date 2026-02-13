from __future__ import annotations

import os

from Data_Structures.root_tree import RootBST, format_dashed
from Data_Structures.hash_table import PatternHashTable
from Engine.generator import MorphologicalGenerator
from Engine.validator import MorphologicalValidator


def _list_patterns(table: PatternHashTable):
    return list(table.iter_patterns())


def _print_patterns(table: PatternHashTable):
    patterns = _list_patterns(table)
    if not patterns:
        print("No patterns loaded.")
        return
    for i, p in enumerate(patterns, start=1):
        print(f"{i}. {p}")


def _select_pattern(table: PatternHashTable) -> str | None:
    patterns = _list_patterns(table)
    if not patterns:
        print("No patterns available.")
        return None

    print("\nAvailable patterns:")
    _print_patterns(table)
    choice = input("Select pattern by index or type pattern exactly: ").strip()

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(patterns):
            return patterns[idx - 1]
        print("Invalid index.")
        return None

    if table.contains(choice):
        return choice

    print("Pattern not found.")
    return None


def _load_data(root_tree: RootBST, pattern_table: PatternHashTable):
    base_dir = os.path.dirname(__file__)
    roots_path = os.path.join(base_dir, "Data", "roots.txt")
    patterns_path = os.path.join(base_dir, "Data", "patterns.txt")

    roots_loaded = root_tree.load_roots_from_file(roots_path)
    patterns_loaded = pattern_table.load_patterns_from_file(patterns_path)

    print(f"Loaded roots: {roots_loaded}")
    print(f"Loaded patterns: {patterns_loaded}")


def _show_validated_derivatives(root_tree: RootBST):
    raw_root = input("Enter root (dashed form): ").strip()
    node = root_tree.search(raw_root)
    if node is None:
        print("Root not found.")
        return

    if hasattr(node.derived, "to_items"):
        items = node.derived.to_items()
        if not items:
            print("No validated derivatives for this root.")
            return
        print(f"Validated derivatives for {raw_root}:")
        for word, count in items:
            print(f"- {word} (freq: {count})")
        return

    words = node.derived.to_list()
    if not words:
        print("No validated derivatives for this root.")
        return
    print(f"Validated derivatives for {raw_root}:")
    for word in words:
        print(f"- {word}")


def main():
    root_tree = RootBST()
    pattern_table = PatternHashTable()
    _load_data(root_tree, pattern_table)

    generator = MorphologicalGenerator(root_tree, pattern_table)
    validator = MorphologicalValidator(generator, root_tree, pattern_table)

    while True:
        print("\n--- Morphological Engine CLI ---")
        print("1) Add root")
        print("2) Search root")
        print("3) Display all roots")
        print("4) Add pattern")
        print("5) Modify pattern")
        print("6) Delete pattern")
        print("7) Generate word")
        print("8) Generate family")
        print("9) Validate word")
        print("10) Show validated derivatives")
        print("0) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            raw_root = input("Enter root (dashed form): ").strip()
            try:
                inserted = root_tree.insert(raw_root)
                print(f"Root inserted: {format_dashed(inserted.root)}")
            except ValueError as exc:
                print(str(exc))

        elif choice == "2":
            raw_root = input("Enter root (dashed form): ").strip()
            node = root_tree.search(raw_root)
            if node:
                print(f"Root found: {format_dashed(node.root)}")
            else:
                print("Root not found.")

        elif choice == "3":
            roots = root_tree.list_roots(dashed=True)
            if not roots:
                print("No roots in tree.")
            else:
                print("Roots in BST (in-order):")
                for r in roots:
                    print(f"- {r}")

        elif choice == "4":
            pattern = input("Enter new pattern: ").strip()
            try:
                pattern_table.insert(pattern)
                print("Pattern added.")
            except ValueError as exc:
                print(str(exc))

        elif choice == "5":
            pattern = input("Enter pattern to modify: ").strip()
            new_rule = input("Enter new rule (pattern form): ").strip()
            try:
                pattern_table.update(pattern, new_rule)
                print("Pattern updated.")
            except ValueError as exc:
                print(str(exc))

        elif choice == "6":
            pattern = input("Enter pattern to delete: ").strip()
            try:
                pattern_table.remove(pattern)
                print("Pattern removed.")
            except ValueError as exc:
                print(str(exc))

        elif choice == "7":
            raw_root = input("Enter root (dashed form): ").strip()
            selected_pattern = _select_pattern(pattern_table)
            if selected_pattern is None:
                continue
            result = generator.generate_one(raw_root, selected_pattern)
            if result["ok"]:
                print(f"Root: {result['root']}")
                print(f"Pattern: {result['pattern']}")
                print(f"Word: {result['word']}")
            else:
                print(f"Generation error: {result['error']}")

        elif choice == "8":
            raw_root = input("Enter root (dashed form): ").strip()
            results = generator.generate_family(raw_root)
            if results and not results[0]["ok"] and results[0]["error"] == "ROOT_NOT_FOUND":
                print("Root not found.")
                continue
            print(f"Family generated for root {raw_root}:")
            for res in results:
                if res["ok"]:
                    print(f"{res['root']} + {res['pattern']} = {res['word']}")
                else:
                    print(f"{res['root']} + {res['pattern']} = None ({res['error']})")

        elif choice == "9":
            raw_root = input("Enter root (dashed form): ").strip()
            raw_word = input("Enter word: ").strip()
            result = validator.validate(raw_root, raw_word)
            if result["result"] == "OUI":
                print(f"OUI — pattern recognized: {result['pattern']}")
            else:
                print("NON")

        elif choice == "10":
            _show_validated_derivatives(root_tree)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()