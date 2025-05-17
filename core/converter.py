import csv
import json

def convert_csv_to_json(csv_path: str, json_path: str):
    """Конвертация CSV-файла в JSON"""
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        words = []
        for row in reader:
            word = {
                "word_src": row["word_src"].strip().lower(),
                "word_rus": row["word_rus"].strip().lower(),
                "category": row["category"].strip().lower(),
                "level": row["level"].strip().lower() if "level" in row and row["level"] else None,
            }
            # Обработка дополнительных переводов
            if "other_rus" in row and row["other_rus"]:
                others = [o.strip().lower() for o in row["other_rus"].split(",") if o.strip()]
                word["other_rus1"] = others[0] if len(others) > 0 else None
                word["other_rus2"] = others[1] if len(others) > 1 else None
                word["other_rus3"] = others[2] if len(others) > 2 else None
            else:
                word["other_rus1"] = None
                word["other_rus2"] = None
                word["other_rus3"] = None

            words.append(word)

    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(words, jsonfile, ensure_ascii=False, indent=4)
