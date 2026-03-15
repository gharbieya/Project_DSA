# Arabic Morphological Search Engine and Derivation Generator

A data-structures Arabic morphological engine that:
- Stores Arabic roots in a Binary Search Tree (BST)
- Stores morphological patterns in a hash table with chaining
- Generates derived words using patterns derivation rules
- Generates morphological family using patterns derivation rules
- Validates whether a word can be derived from a given root

## Features
- **Binary Search Tree for roots** 
- **Hash table for patterns** (fixed size, chaining)
- **Linked lists** for derived words and collision handling
- **Normalization** for Arabic normalization & validation
- **Generation** and **Validation** of derived words
- **Root management** (insert, search, delete)
- **Pattern management** (insert, search, delete)

## Project Structure
```
server.py             # Flask server that serves the UI and API endpoints
main.py               # CLI entrypoint (terminal menu)
Data_Structures/
  root_tree.py        # Binary Search Tree 
  hash_table.py       # Hash table 
  linked_list.py      # Linked list
  normalization.py    
Data/
  roots.txt           # Root dataset
  patterns.txt        # Pattern dataset
Engine/
  generator.py       
  validator.py    
UI/
  Interface.html      # Web UI
```

## How It Works
1. Roots are loaded from `roots.txt` into the BST.
2. Patterns are loaded from `patterns.txt` into a hash table.
3. Generation replaces **ف/ع/ل** in a pattern with the root letters.
4. Validation regenerates candidates from all patterns and compares.

## Complexity Overview
- BST manipulation: **O(log n)** average, **O(n)** worst
- Hash manipulation: **O(1)** average, **O(P)** worst
- Generation (1 word): **O(log n)** average, **O(n)** worst
- Validation: **O(log n + P)** worst

**Where:**
- **n** = number of roots  
- **P** = number of patterns  

## Flask Server Installation and Run Guide

The web UI is served by `server.py` using Flask.

> Important: run the commands from the **project root** (the folder that contains `Data/`, `UI/`, and `server.py`) so relative paths resolve correctly.

### Prerequisites
- Python 3.10+ installed
- `pip` available

### Windows (PowerShell)
```powershell
cd path\to\DSA_Project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install flask
python server.py
```

Then open:
- `http://127.0.0.1:5000`

### Linux (bash)
```bash
cd /path/to/DSA_Project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
python server.py
```

Then open:
- `http://127.0.0.1:5000`

### Stop the server
- Press `Ctrl + C` in the terminal running Flask.

## CLI

You can also run the project as a command-line interface (CLI):

```bash
python main.py
```

This opens an interactive menu in the terminal for inserting/searching roots, managing patterns, and generating/validating words.

## API Endpoints (Flask)

Base URL (default): `http://127.0.0.1:5000`

### `POST /generate`
Generate one derived word from a root + pattern.

Example:
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"root":"ك-ت-ب","pattern":"فاعل"}'
```

### `POST /generate_family`
Generate a list of derived words across all patterns.

Example:
```bash
curl -X POST http://127.0.0.1:5000/generate_family \
  -H "Content-Type: application/json" \
  -d '{"root":"ك-ت-ب"}'
```

### `POST /validate`
Validate whether a word can be derived from the given root.

Example:
```bash
curl -X POST http://127.0.0.1:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"root":"ك-ت-ب","word":"كاتب"}'
```

### `POST /add_root`
Add a new root (dashed form).

Example:
```bash
curl -X POST http://127.0.0.1:5000/add_root \
  -H "Content-Type: application/json" \
  -d '{"root":"س-م-ع"}'
```

### `POST /add_pattern`
Add a new pattern.

Example:
```bash
curl -X POST http://127.0.0.1:5000/add_pattern \
  -H "Content-Type: application/json" \
  -d '{"pattern":"مفاعل"}'
```

### `GET /api/roots`
List all roots.

Example:
```bash
curl http://127.0.0.1:5000/api/roots
```

### `GET /api/patterns`
List all patterns.

Example:
```bash
curl http://127.0.0.1:5000/api/patterns
```

## Data Files Format

The application loads its datasets from:
- `Data/roots.txt`
- `Data/patterns.txt`

Both files are plain text (`UTF-8`), with **one entry per line**.

### Roots (`Data/roots.txt`)
- Format: dashed triliteral roots like `ك-ت-ب`
- One root per line

Example:
```
ك-ت-ب
د-خ-ل
س-م-ع
```

### Patterns (`Data/patterns.txt`)
- Format: Arabic pattern strings such as `فاعل`, `مفعول`, `تفعيل`, ...
- One pattern per line
- Diacritics may appear in some patterns; the engine normalizes input.

Example:
```
فاعل
مفعول
تفعيل
```

## License

This project is licensed under the MIT License. See `LICENSE`.