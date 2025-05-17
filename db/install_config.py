
from collections import OrderedDict

INSTALL_SCHEMA = {
    "tables": OrderedDict([
        ("word_category", 1),
        ("study_level", 1),
        ("study_levels", 1),
        ("dictionary", 2),
        ("client_info", 3),
        ("client_activity_log", 4),
        ("client_analytics", 5),
        ("learned_words", 6),
        ("user_word_stats", 6),
        ("user_progress_by_theme", 6),
        ("cron_events", 7),
        ("client_activity_words", 7),
    ]),
    "views": OrderedDict([
        ("study_level_mapped", 8),
        ("level_matrix", 9),
        ("quiz_weight_by_group", 10),
        ("word_weight", 10),
        ("user_progress_by_theme", 10),
        ("personalized_words", 10),
        ("word_success_count", 10),
        ("client_level_progress", 11)
    ])
}

'''✅ Блок tables (по порядку создания)
Основные справочники:
"word_category" — тематики
"study_level" — внутренние уровни (начальный, средний...)
"study_levels" — CEFR-уровни (A1–C2)

Словарь:
"dictionary" — основная таблица слов

Пользовательская информация:
"client_info" — данные пользователей

Активности:
"client_activity_log" — логи викторин

Агрегаты:
"client_analytics" — агрегированные метрики

Личная статистика:
"learned_words" — выученные слова
"user_word_stats" — по каждому слову
"user_progress_by_theme" — прогресс по темам

Служебные:
"cron_events" — фоновые задачи
"client_activity_words" — слова в викторине
"table_study_level_mapped" — привязка уровней

Матрица переходов:
"level_matrix" — определение уровня клиента

✅ Блок views (по порядку установки)
"study_level_mapped" — прежний VIEW, остаётся для совместимости

Метрики и персонализация:

"quiz_weight_by_group"

"word_weight"

"user_progress_by_theme" — агрегация

"personalized_words"

"word_success_count"

"client_level_progress" — для расчёта уровня клиента'''