from db.importer import import_words_from_json
from core.config import DB  # <-- импорт безопасных данных

json_path = "../data/words.json"

result = import_words_from_json(json_path, DB)

print("✅ Успешно добавлено:", result["added"])
print("⏭ Пропущено (дубликаты):", len(result["duplicates"]))
if result["errors"]:
    print("⚠️ Ошибки:")
    for err in result["errors"]:
        print("-", err)
else:
    print("🎉 Импорт прошёл без ошибок.")
