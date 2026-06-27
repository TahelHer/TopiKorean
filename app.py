from flask import Flask, render_template
from pathlib import Path
import json


app = Flask(__name__, template_folder="templates")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

def load_vocab(filename):
    file_path = OUTPUT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


topik1_data = load_vocab("topik1_vocabulary.json")
topik2_data = load_vocab("topik2_vocabulary.json")

def clean(data):
    return [
        {
            "Korean": w.get("Korean", ""),
            "English": w.get("English", ""),
            "Part_Of_Speech": w.get("Part_Of_Speech", "")
        }
        for w in data
    ]


# HOME
@app.route("/")
def home():
    return render_template(
        "topik.html",
        topik1=topik1_data,
        topik2=topik2_data
    )

# TOPIK 1
@app.route("/topik1")
def topik1():
    return render_template(
        "topik.html",
        vocab_data=clean(topik1_data),
        level="TOPIK 1"
    )


# TOPIK 2
@app.route("/topik2")
def topik2():
    return render_template(
        "topik.html",
        vocab_data=clean(topik2_data),
        level="TOPIK 2"
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
