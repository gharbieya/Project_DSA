# from hash_table import PatternHashTable, derive_from_pattern

# OUTPUT_PATH = "Data_Structures/output.txt"
# PATTERNS_PATH = "Data/patterns.txt"


# def write_line(text: str) -> None:
#     with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
#         f.write(text + "\n")


# def reset_output() -> None:
#     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
#         f.write("=== Hash Table Test ===\n")


# def test_hash_table():
#     reset_output()

#     table = PatternHashTable()
#     count = table.load_patterns_from_file(PATTERNS_PATH)
#     write_line(f"Loaded patterns: {count}")

#     # ✅ Correct example
#     root = "ك-ت-ب"
#     pattern = "فاعل"
#     exists = table.contains(pattern)
#     derived = derive_from_pattern(root, pattern) if exists else None
#     write_line(f"Root: {root} | Pattern: {pattern} -> {derived}")

#     # ✅ Shadda preserved (pattern with harakat input)
#     pattern_with_shakl = "فَعّال"
#     exists2 = table.contains(pattern_with_shakl)
#     derived2 = derive_from_pattern(root, pattern_with_shakl) if exists2 else None
#     write_line(f"Pattern with harakat: {pattern_with_shakl} -> {derived2}")

#     # ❌ Unknown pattern
#     unknown_pattern = "فعّول"
#     exists3 = table.contains(unknown_pattern)
#     write_line(f"Unknown pattern '{unknown_pattern}' found? {exists3}")

#     # ❌ Invalid root
#     invalid_root = "ك-ب"
#     derived_invalid = derive_from_pattern(invalid_root, "فاعل")
#     write_line(f"Invalid root '{invalid_root}' -> {derived_invalid}")


# if __name__ == "__main__":
#     test_hash_table()

from hash_table import PatternHashTable
import time
import os

OUTPUT_PATH = "Data_Structures/output.txt"
PATTERNS_PATH = "Data/patterns.txt"


def ensure_output_directory():
    output_dir = os.path.dirname(OUTPUT_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)


def write_line(text: str) -> None:
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def write_section(title: str) -> None:
    separator = "=" * 60
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n{separator}\n")
        f.write(f"{title}\n")
        f.write(f"{separator}\n")


def reset_output() -> None:
    ensure_output_directory()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("╔" + "═" * 58 + "╗\n")
        f.write("║" + " " * 15 + "HASH TABLE SYSTEM TEST" + " " * 15 + "║\n")
        f.write("╚" + "═" * 58 + "╝\n")


# ============================================================================
# TEST 1: Load Patterns Dataset
# ============================================================================

def test_load_patterns():
    write_section("TEST 1: LOAD PATTERNS DATASET")

    table = PatternHashTable()

    if not os.path.exists(PATTERNS_PATH):
        write_line(f"❌ File not found: {PATTERNS_PATH}")
        return

    count = table.load_patterns_from_file(PATTERNS_PATH)
    write_line(f"✅ Loaded patterns: {count}")
    write_line(f"Table size: {table.size()}")
    write_line(f"Capacity: {table._capacity}")
    write_line(f"Load factor: {table.size() / table._capacity:.2%}")

    expected_patterns = [
        "فاعل", "مفعول", "فعّال", "تفعيل", "استفعال",
        "افتعال", "فعيل", "تفاعل", "انفعال", "مستفعل"
    ]
    missing = []
    for p in expected_patterns:
        if not table.contains(p):
            missing.append(p)

    if not missing:
        write_line("✅ All expected patterns found")
    else:
        write_line(f"❌ Missing patterns: {missing}")


# ============================================================================
# TEST 3: Derivation (System Patterns)
# ============================================================================

def test_derivation():
    write_section("TEST 3: WORD DERIVATION")

    table = PatternHashTable()
    table.load_patterns_from_file(PATTERNS_PATH)

    test_cases = [
        ("ك-ت-ب", "فاعل", "كاتب"),
        ("ك-ت-ب", "مفعول", "مكتوب"),
        ("د-ر-س", "فاعل", "دارس"),
        ("د-ر-س", "مفعول", "مدروس"),
        ("ع-ل-م", "فاعل", "عالم"),
        ("ك-ت-ب", "فعّال", "كتّاب"),
        ("ك-ت-ب", "مفعل", "مكتب"),
    ]

    for root, pattern, expected in test_cases:
        if not table.contains(pattern):
            write_line(f"❌ Pattern not found in table: {pattern}")
            continue
        result = table.derive(root, pattern)
        status = "✅" if result == expected else "⚠️"
        write_line(f"{status} {root} + {pattern} = {result} (expected {expected})")


# ============================================================================
# TEST 4: Performance (System Scale)
# ============================================================================

def test_performance():
    write_section("TEST 4: PERFORMANCE")

    table = PatternHashTable()
    table.load_patterns_from_file(PATTERNS_PATH)

    start = time.time()
    for _ in range(1000):
        for p in ["فاعل", "مفعول", "تفعيل", "استفعال"]:
            table.contains(p)
    elapsed = time.time() - start

    write_line(f"1000 lookups x 4 patterns: {elapsed:.4f} seconds")


# ============================================================================
# MAIN
# ============================================================================

def run_all_tests():
    reset_output()

    tests = [
        test_load_patterns,
        test_derivation,
        test_performance,
    ]

    for test in tests:
        test()

    write_section("TEST SUMMARY")
    write_line("✅ All system-level tests completed")


if __name__ == "__main__":
    run_all_tests()