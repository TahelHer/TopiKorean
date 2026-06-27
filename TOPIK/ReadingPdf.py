import re
import json
from pathlib import Path
from pypdf import PdfReader

def categorize_word(korean_word):

    # Verbs (כל מה שנגמר ב-다)
    if korean_word.endswith("다"):
        return "Verb"

    # ברירת מחדל
    return "Noun"


# תיקיות יחסיות (מתאים לאתר / שרת)
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

pattern = r'(\d+)\s+([가-힣]+)\s+([a-zA-Z\s,~]+)'

print("📚 מתחיל לקרוא קבצי TOPIK מתיקיית data...")

pdf_files = list(DATA_DIR.glob("*.pdf"))

if not pdf_files:
    print("⚠️ לא נמצאו קבצי PDF בתיקיית data")
else:
    for pdf_path in pdf_files:
        print(f"📄 מעבד: {pdf_path.name}")

        reader = PdfReader(str(pdf_path))
        raw_text = ""

        for page in reader.pages:
            raw_text += (page.extract_text() or "") + "\n"

        matches = re.findall(pattern, raw_text)

        vocabulary_list = []

        for match in matches:
            word_no = int(match[0])
            korean = match[1].strip()
            english = match[2].strip().replace('\n', ' ')

            vocabulary_list.append({
                "No": word_no,
                "Korean": korean,
                "English": english,
                "Part_Of_Speech": categorize_word(korean)
            })

        output_file = OUTPUT_DIR / f"{pdf_path.stem}_vocabulary.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(vocabulary_list, f, ensure_ascii=False, indent=4)

        print(f"✅ נשמר: {output_file.name} ({len(vocabulary_list)} מילים)")

print("🎉 סיום עיבוד כל הקבצים")