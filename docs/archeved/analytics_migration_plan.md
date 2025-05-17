
# 📊 План миграции аналитики Esp2Rus_bot v2

## Этап 0. Подготовка
✅ Структура `analytics/metrics/` создана  
✅ `save_client_activity_log.py` — лог активности  
✅ `save_client_analytics.py` — агрегатор  
✅ `calculate_quiz_weight_with_fetch` — расчёт через view  

---

## Этап 1. Параллельное тестирование
🟡 Добавить флаг `USE_ANALYTICS_V2 = True`  
🟡 При флаге активировать новый стек  
🟡 Сравнение логов в `logs/analytics_debug/`  
🟡 Тестирование quiz_weight, client_rating, level_id_current  

---

## Этап 2. Активация нового стека (staging)
🔄 Включить `USE_ANALYTICS_V2 = True` в `@Test_Esp2Rus_bot`  
✅ Тест кейсы по всем метрикам  
✅ Визуальная проверка значений в client_analytics  

---

## Этап 3. Продакшн запуск
🟢 Подключить `save_client_activity_log` в боевом боте  
📦 Заархивировать старую аналитику в `analytics_old/`  
📝 Обновить `README.md`, `docs/`, schema_v4.png  

---

## Этап 4. Мониторинг и откат
🧾 Логирование расчётов и обновлений  
🛑 Готовность к откату через `.env`  
🔁 Скрипт `rollback_analytics.py` для возврата к старому стеку  
