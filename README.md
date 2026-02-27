# Arabic Morphological Search Engine and Derivation Generator

A data-structures–focused Arabic morphological engine that:
- Stores Arabic roots in a Binary Search Tree (BST)
- Stores morphological patterns in a hash table with chaining
- Generates derived forms using the pattern derivation rules
- Validates whether a word can be derived from a given root

## Features
- **Binary Search Tree for roots** 
- **Hash table for patterns** (fixed size, chaining)
- **Linked lists** for derived words and collision handling
- **Normalization** for Arabic normalization & validation
- **Generation** and **Validation** of derived words

## Project Structure
```
Data_Structures/
  root_tree.py        # BST 
  hash_table.py       # Hash table 
  linked_list.py      # Linked list
  normalization.py    
Data/
  roots.txt           # Root dataset
  patterns.txt        # Pattern dataset
```

## Requirements
- Python 3.x

## How It Works
1. Roots are loaded from `roots.txt` into the BST.
2. Patterns are loaded from `patterns.txt` into a hash table.
3. Generation replaces **ف/ع/ل** in a pattern with the root letters.
4. Validation regenerates candidates from all patterns and compares.

## Complexity (Overview)
- BST search/insert: **O(log n)** average, **O(n)** worst
- Hash lookup: **O(1)** average, **O(P)** worst
- Validation: **O(log n + P)** average
