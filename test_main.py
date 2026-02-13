from __future__ import annotations
import os
import time

from Data_Structures.root_tree import RootBST
from Data_Structures.hash_table import PatternHashTable
from Engine.generator import MorphologicalGenerator
from Engine.validator import MorphologicalValidator


OUTPUT_PATH = "test_main_output.txt"
ROOTS_PATH = "Data/roots.txt"
PATTERNS_PATH = "Data/patterns.txt"


def write_line(text: str):
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def reset_output():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("=== EXTREME SYSTEM TEST ===\n")


def main():
    reset_output()

    tree = RootBST()
    table = PatternHashTable()
    gen = MorphologicalGenerator(tree, table)
    val = MorphologicalValidator(gen, tree, table)

    roots_loaded = tree.load_roots_from_file(ROOTS_PATH)
    patterns_loaded = table.load_patterns_from_file(PATTERNS_PATH)
    write_line(f"Loaded roots: {roots_loaded}")
    write_line(f"Loaded patterns: {patterns_loaded}")

    write_line("\n[1] Root Insertion Tests")
    valid_roots = ["س-م-ع", "د-خ-ل", "غ-ف-ل"]
    invalid_roots = ["كتب", "ك-ت", "ك-ت-ب-د", "a-b-c", "ك--ت-ب"]

    for r in valid_roots:
        try:
            tree.insert(r)
            write_line(f"Inserted: {r}")
        except ValueError as e:
            write_line(f"{r} -> {e}")

    for r in invalid_roots:
        try:
            tree.insert(r)
            write_line(f"Inserted: {r}")
        except ValueError as e:
            write_line(f"{r} -> {e}")

    write_line("\n[2] Pattern CRUD Tests")
    try:
        table.insert("مفاعل")
        write_line("مفاعل -> added")
    except ValueError as e:
        write_line(f"مفاعل -> {e}")

    try:
        table.insert("مفاعل")
        write_line("مفاعل -> added (duplicate)")
    except ValueError as e:
        write_line(f"مفاعل -> {e}")

    try:
        table.update("مفاعل", "مفاعِل")
        write_line("مفاعل -> updated to مفاعِل")
    except ValueError as e:
        write_line(f"مفاعل -> {e}")

    try:
        table.remove("مفاعل")
        write_line("مفاعل -> removed")
    except ValueError as e:
        write_line(f"مفاعل -> {e}")

    write_line("\n[3] Invalid Pattern Tests")
    invalid_patterns = ["فاعلx", "فعل", "سسس", "كتابة", "مفا", "", "12", "ف", "عل", "مت"]
    for p in invalid_patterns:
        try:
            table.insert(p)
            write_line(f"{p} -> inserted (should fail)")
        except ValueError as e:
            write_line(f"{p} -> {e}")

    write_line("\n[4] Generation Tests")
    root = "ك-ت-ب"
    patterns = list(table.iter_patterns())
    for p in patterns[:5]:
        res = gen.generate_one(root, p)
        write_line(f"{root} + {p} = {res['word']}")

    write_line("\n[5] Family Generation (first 5)")
    family = gen.generate_family(root)
    for res in family[:5]:
        write_line(f"{res['root']} + {res['pattern']} = {res['word']}")

    write_line("\n[6] Validation Tests")
    if patterns:
        test_word = gen.generate_one(root, patterns[0])["word"]
        if test_word:
            result = val.validate(root, test_word)
            write_line(f"Validate {test_word} with {root} -> {result}")

    result = val.validate(root, "غير_موجود")
    write_line(f"Validate غير_موجود with {root} -> {result}")

    write_line("\n[7] Validated Derivatives")
    node = tree.search(root)
    if node and hasattr(node.derived, "to_items"):
        for word, count in node.derived.to_items():
            write_line(f"{word} (freq {count})")

    write_line("\n[8] Stress Test (20 roots x 20 patterns)")
    start = time.time()
    roots = tree.list_roots(dashed=True)[:20]
    patterns = list(table.iter_patterns())[:20]
    total = 0
    for r in roots:
        for p in patterns:
            res = gen.generate_one(r, p, store=False)
            if res["ok"]:
                total += 1
    elapsed = time.time() - start
    write_line(f"Generated: {total} in {elapsed:.4f} sec")


if __name__ == "__main__":
    main()