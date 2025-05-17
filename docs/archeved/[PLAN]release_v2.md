## ✅ Финализированный статус (на 11 мая)

### Этапы 1–4: Архитектура и метрики — ✅ Завершены
- Структура db/, analytics/, metrics/
- Метрики: quiz_weight, client_rating, level_id_word
- Логика save_client_activity_log, save_client_analytics, update_learned_words
- Cron-логи, 
- флаги управления (USE_ANALYTICS_V2, # === Флаги ===
USE_ANALYTICS_V2 = os.getenv("USE_ANALYTICS_V2", "False").lower() == "true"
DELETE_INACTIVE_CLIENTS = False  # по умолчанию удаление клиентов отключено. Для включения режима удаления неактивных клиентов раз в сутки - True
LEVEL_CALCULATION_ONLINE = True  # По умолчанию включён online расчет - True. для переключения на offline-расчёт раз в сутки - False 
)

### Этап 5: Админ-интерфейс и отчёты — 🟡 В процессе
- /admin_clients — не реализован
- /report @user — не реализован
- Выгрузка CSV / отправка на email админам — не реализована

### Этап 6: Автоматическая отчётность — 🔜 Запланировано
- cron-скрипты
- auto-summary в Telegram

### Этап 7: Тесты и валидация — 🟡 Частично
- quiz_weight, client_rating, learned_words — ✅
- level_id_current, level_matrix — ✅ реализовано, требуется покрытие и тестирование

### Этап 8: Персонализация (v2) — ✅ Завершено
- learned_words — по 3 успешным попыткам (флаг)
- view_personalized_words — исключает выученные
- client_level_progress — создан
- level_id_current — считается после каждой викторины
- ONLINE/OFFLINE режим — в settings.py (config.py)

---

## 📌 To Do перед запуском в прод

### 🛠 Технические:
- [ ] Проверка run_install.py на staging
- [ ] README_Prod_Migration.md с шагами и rollback
- [ ] README_release_v2 (для публикации на github)
- [ ] Добавление USE_ANALYTICS_V2 в .env.prod (мы же договороились оставить в config.py и не итащить на прод)

### 📊 Функциональные:
- [ ] Реализация /admin_clients
- [ ] Реализация команды /report
- [ ] Автоотчёт по cron в Telegram
- [ ] Повторение выученных слов (опционально) - предлагаю перенести в roadmap на следующий релиз

---

## 📦 Для v2.1+
- Расширенная статистика по словам и категориям
- Интервальное повторение
- Поддержка мультиязычности
- "Режим повторения" выученных слов