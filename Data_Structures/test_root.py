from root_tree import RootBST

tree = RootBST()
lines = []

# 1) Manual insertions (valid)
lines.append(str(tree.insert_from_user_input("ك-ت-ب")))  # True
lines.append(str(tree.insert_from_user_input("ق-ر-أ")))  # True
lines.append(str(tree.insert_from_user_input("ك-ت-ب")))  # False (duplicate)

# 2) Add derived words
lines.append(str(tree.add_derived_word("ك-ت-ب", "كاتب")))   # True
lines.append(str(tree.add_derived_word("ك-ت-ب", "كاتب")))   # False (duplicate)
lines.append(str(tree.add_derived_word("ق-ر-أ", "قارئ")))   # True

# 3) Check stored roots (dashed output)
lines.append(str(tree.list_roots(dashed=True)))

# 4) Invalid input format test
try:
    tree.insert("كتب")
except ValueError as e:
    lines.append(f"Invalid format caught: {e}")

# 5) File loading test
count = tree.load_roots_from_file("../Data/roots.txt")
lines.append(f"Loaded from file: {count}")
lines.append(str(tree.list_roots(dashed=True)))

# 6) Additional invalid roots
invalid_roots = [
    "ك-ت-ب-ا",
    "a-b-c",
    "كتابة",
    "كتب",
    "ك--ت-ب",
    "ك-ت",
    "ك ت ب",
    "invalid"
]

for r in invalid_roots:
    try:
        tree.insert(r)
        lines.append(f"Unexpected قبول: {r}")
    except ValueError as e:
        lines.append(f"Rejected {r}: {e}")

# Print to terminal
for line in lines:
    print(line)

# Save same output to file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))