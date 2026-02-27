# Arabic Morphological Search Engine and Derivation Generator

A data-structures–focused Arabic morphological engine that:
- Stores Arabic roots in a Binary Search Tree (BST)
- Stores morphological patterns in a hash table with chaining
- Generates derived forms using the pattern (wazn) rules
- Validates whether a word can be derived from a given root

## Features
- **BST for roots** (compact roots like `كتب`)
- **Hash table for patterns** (fixed size, chaining)
- **Linked lists** for derived words and collision handling
- **Normalization** for Arabic diacritics and letter variants
- **Generation** and **validation** of derived words

## Project Structure
```
Data_Structures/
  root_tree.py        # BST for roots
  hash_table.py       # Hash table for patterns
  linked_list.py      # Linked list for derived words
  normalization.py    # Arabic normalization & validation
Data/
  roots.txt           # Root dataset
  patterns.txt        # Pattern dataset
```

## Requirements
- Python 3.x
- (Optional) XeLaTeX if you compile the report

## How It Works
1. Roots are loaded from `roots.txt` into the BST.
2. Patterns are loaded from `patterns.txt` into a hash table.
3. Generation replaces **ف/ع/ل** in a pattern with the root letters.
4. Validation regenerates candidates from all patterns and compares.

## Complexity (Overview)
- BST search/insert: **O(log n)** average, **O(n)** worst
- Hash lookup: **O(1)** average, **O(P)** worst
- Validation: **O(log n + P)** average

## Example (Concept)
- Root: ك-ت-ب  
- Pattern: مفعول  
- Result: مكتوب

## License
Specify your license here (e.g., MIT, GPL, or “All Rights Reserved”).
