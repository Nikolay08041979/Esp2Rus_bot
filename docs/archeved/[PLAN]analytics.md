# 📊 План–Факт по аналитике Esp2Rus_bot v2 (обновлён 10.05.2025)

## Этап 1. Подготовка структуры данных — ✅ Выполнено
- [x] Созданы все таблицы (13 шт.) и VIEW (5 шт.)
- [x] Используется `run_install.py` + `install_config.py`
- [x] Загружены справочники `dictionary`, `study_levels`, `word_category`, `study_level`
- [x] Архивирована папка `/install/` и зафиксирована структура `db/`

---

## Этап 2. Интеграция аналитики в Telegram-бот — ✅ Выполнено
- [x] Интеграция `log_client_activity()` через `analytics.py`
- [x] Реализован расчёт `quiz_weight`, `client_rating`, `level_id_word`
- [x] Автообновление `client_info`, `client_activity_log`, `client_analytics`
- [x] Привязка слов к сессии через `client_activity_words`
- [x] Логирование в `logs/analytics_debug/`

---

## Этап 3. Расчёт производных метрик — ✅ Выполнено
- [x] `client_rating` через `calculate_client_rating.py`
- [x] Переписан `save_client_analytics.py`
- [x] `quiz_weight` рассчитывается только при `score_quiz == 1.0`
- [x] Логика `level_id_word` на основе `get_level_id_word.py`
- [x] Защита от некорректных данных

---

## Этап 4. Мониторинг и откат — ✅ Выполнено
- [x] Логирование расчётов по cron
- [x] `rollback_analytics.py`
- [x] Таблица `cron_events` + логгирование задач

---

## Этап 5. Админ-интерфейс и отчёты — 🔄 В процессе
- [ ] `/admin_clients` — панель активности и статистики
- [ ] `/report @username` — выгрузка отчёта
- [ ] Экспорт CSV в `reports/`

---

## Этап 6. Автоматическая отчётность — 🔄 Запланировано
- [ ] Еженедельный отчёт (CSV + Telegram)
- [ ] Сравнение с предыдущей неделей
- [ ] Рассылка админам

---

## Этап 7. Тестирование и валидация — 🔄 В процессе
- [x] Юнит-тесты: `quiz_weight`, `client_rating`, `level_id_word`
- [ ] Проверка `learned_words` и `level_id_current`

---

## Этап 8. Персонализация — 🔄 В приоритете
- [x] Составлено финальное ТЗ (learned_words, user_word_stats, user_progress_by_theme)
- [ ] `client_level_matrix` — логика CEFR-присвоения
- [ ] Выдача слов по персонализированному списку
- [ ] `LANGUAGE_TARGET` и `LEARN_THRESHOLD` выведены в `.env` / `config.py`

---

## Этап 9. Миграция на прод — 🔄 После валидации
- [ ] Подготовка `README_Prod_Migration.md`, `CONTRIBUTING.md`
- [ ] Бэкап прод-таблиц
- [ ] Переключение ENV_MODE + деплой