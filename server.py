from flask import Flask, request, jsonify, send_from_directory
import os

# Use the correct class names from your project
from Data_Structures.root_tree import RootBST, format_dashed
from Data_Structures.hash_table import PatternHashTable
from Engine.generator import MorphologicalGenerator
from Engine.validator import MorphologicalValidator

app = Flask(__name__, static_folder='UI', static_url_path='')

# ===== Load data once =====
root_tree = RootBST()
pattern_table = PatternHashTable()

ROOTS_PATH = os.path.join("Data", "roots.txt")
PATTERNS_PATH = os.path.join("Data", "patterns.txt")

root_tree.load_roots_from_file(ROOTS_PATH)
pattern_table.load_patterns_from_file(PATTERNS_PATH)

# Initialize generator and validator
generator = MorphologicalGenerator(root_tree, pattern_table)
validator = MorphologicalValidator(generator, root_tree, pattern_table)


# ===== Serve UI =====
@app.route("/")
def index():
    return send_from_directory("UI", "Interface.html")


# ===== Generate word =====
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    raw_root = data.get("root")
    pattern = data.get("pattern")

    result = generator.generate_one(raw_root, pattern)
    return jsonify(result)


# ===== Generate full family =====
@app.route("/generate_family", methods=["POST"])
def generate_family():
    data = request.json
    raw_root = data.get("root")

    results = generator.generate_family(raw_root)
    return jsonify(results)


# ===== Validate word =====
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    raw_root = data.get("root")
    raw_word = data.get("word")

    result = validator.validate(raw_root, raw_word)
    return jsonify(result)


# ===== Add root =====
@app.route("/add_root", methods=["POST"])
def add_root():
    data = request.json
    raw_root = data.get("root")
    try:
        canonical = root_tree.insert(raw_root)
        return jsonify({"status": "ok", "root": format_dashed(canonical.root)})
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)})


# ===== Add pattern =====
@app.route("/add_pattern", methods=["POST"])
def add_pattern():
    data = request.json
    pattern = data.get("pattern")
    try:
        pattern_table.insert(pattern)
        return jsonify({"status": "ok", "pattern": pattern})
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)})


# ===== List all roots =====
@app.route("/api/roots", methods=["GET"])
def list_roots():
    all_roots = [format_dashed(r) for r in root_tree.inorder()]
    return jsonify(all_roots)


# ===== List all patterns =====
@app.route("/api/patterns", methods=["GET"])
def list_patterns():
    all_patterns = [p for p in pattern_table.iter_patterns()]
    return jsonify(all_patterns)


if __name__ == "__main__":
    app.run(debug=True)