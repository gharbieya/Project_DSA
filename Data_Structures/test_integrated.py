from root_tree import RootBST
from hash_table import PatternHashTable
import time
import os

OUTPUT_PATH = "Data_Structures/output.txt"
ROOTS_PATH = "Data/roots.txt"
PATTERNS_PATH = "Data/patterns.txt"


def write_line(text: str) -> None:
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def reset_output() -> None:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("=== EXTREME INTEGRATION TEST (RootBST + HashTable) ===\n")


def load_roots_from_file(file_path: str):
    roots = []
    if not os.path.exists(file_path):
        return roots
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if raw:
                roots.append(raw)
    return roots


def collect_patterns_from_table(table: PatternHashTable):
    patterns = []
    for chain in table._buckets:
        current = chain.head
        while current:
            patterns.append(current.pattern)
            current = current.next
    return patterns


def test_integration_extreme():
    reset_output()

    # Load roots
    tree = RootBST()
    roots_loaded = tree.load_roots_from_file(ROOTS_PATH)
    write_line(f"Loaded roots into BST: {roots_loaded}")

    # Load patterns
    table = PatternHashTable()
    patterns_loaded = table.load_patterns_from_file(PATTERNS_PATH)
    write_line(f"Loaded patterns into hash table: {patterns_loaded}")

    # Collect raw lists
    roots_list = load_roots_from_file(ROOTS_PATH)
    patterns_list = collect_patterns_from_table(table)

    write_line(f"Roots in file: {len(roots_list)}")
    write_line(f"Patterns in table: {len(patterns_list)}")

    # ---------------------------------------------------------------------
    # 1) Existing root + valid patterns
    # ---------------------------------------------------------------------
    write_line("\n[1] Existing Root + Valid Patterns")
    root = "ك-ت-ب"
    root_exists = tree.search(root) is not None
    write_line(f"Root '{root}' exists? {root_exists}")

    test_patterns = ["فاعل", "مفعول", "تفعيل", "استفعال"]
    for p in test_patterns:
        derived = table.derive(root, p)
        write_line(f"{root} + {p} = {derived}")

    # ---------------------------------------------------------------------
    # 2) Missing pattern
    # ---------------------------------------------------------------------
    write_line("\n[2] Missing Patterns (should return None)")
    missing_patterns = ["فعّول", "مفاعيلة", "تفعيول"]
    for p in missing_patterns:
        derived = table.derive(root, p)
        write_line(f"{root} + {p} = {derived}")

    # ---------------------------------------------------------------------
    # 3) Invalid root formats (should return None)
    # ---------------------------------------------------------------------
    write_line("\n[3] Invalid Root Formats")
    invalid_roots = ["كتب", "ك-ت", "ك-ت-ب-د", "k-t-b", "ك--ت-ب", "-ك-ت-ب"]
    for r in invalid_roots:
        derived = table.derive(r, "فاعل")
        write_line(f"{r} + فاعل = {derived}")

    # ---------------------------------------------------------------------
    # 4) Missing root in BST (skip derivation)
    # ---------------------------------------------------------------------
    write_line("\n[4] Root Not in BST (skip derivation)")
    missing_root = "ز-ز-ز"
    exists = tree.search(missing_root) is not None
    write_line(f"Root '{missing_root}' exists? {exists}")
    if exists:
        write_line(f"{missing_root} + فاعل = {table.derive(missing_root, 'فاعل')}")
    else:
        write_line("Derivation skipped (root not in BST)")

    # ---------------------------------------------------------------------
    # 5) Normalization check (diacritics)
    # ---------------------------------------------------------------------
    write_line("\n[5] Normalization Check (Diacritics)")
    diacritic_pattern = "فَاعِل"
    derived = table.derive(root, diacritic_pattern)
    write_line(f"{root} + {diacritic_pattern} = {derived}")

    # ---------------------------------------------------------------------
    # 6) Stress derivation with dataset
    # ---------------------------------------------------------------------
    write_line("\n[6] Stress Derivation (Dataset x Patterns)")
    sample_roots = roots_list[:20] if len(roots_list) > 20 else roots_list
    sample_patterns = patterns_list[:20] if len(patterns_list) > 20 else patterns_list

    start = time.time()
    total = 0
    produced = 0
    for r in sample_roots:
        if tree.search(r) is None:
            continue
        for p in sample_patterns:
            total += 1
            if table.derive(r, p) is not None:
                produced += 1
    elapsed = time.time() - start

    write_line(f"Stress roots used: {len(sample_roots)}")
    write_line(f"Stress patterns used: {len(sample_patterns)}")
    write_line(f"Total derivations attempted: {total}")
    write_line(f"Derivations produced: {produced}")
    write_line(f"Time: {elapsed:.4f} seconds")

    write_line("\n✅ Extreme integration test completed")


if __name__ == "__main__":
    test_integration_extreme()