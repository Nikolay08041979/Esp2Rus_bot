import csv
import json
import os

def convert_csv_to_json(csv_path: str, json_path: str) -> dict:
    result = {"converted": 0, "errors": []}
    entries = []

    with open(csv_path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        required_fields = {"word_esp", "word_rus", "other_rus", "category", "level"}

        if not required_fields.issubset(reader.fieldnames):
            result["errors"].append("❌ В CSV-файле отсутствуют необходимые столбцы.")
            return result

        for row in reader:
            try:
                # Валидация other_rus
                other_parts = row["other_rus"].split(",")
                if len(other_parts) != 3:
                    raise ValueError("Поле other_rus должно содержать 3 слова через запятую")

                entries.append({
                    "word_esp": row["word_esp"].strip(),
                    "word_rus": row["word_rus"].strip(),
                    "other_rus": ",".join([w.strip() for w in other_parts]),
                    "category": row["category"].strip(),
                    "level": row["level"].strip()
                })
                result["converted"] += 1
            except Exception as e:
                result["errors"].append(f"{row.get('word_esp', '?')}: {str(e)}")

    # Запись в JSON
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=2)

    return result