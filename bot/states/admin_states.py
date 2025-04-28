# --- Новый файл: bot/states/admin_states.py ---

from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    awaiting_new_category = State()
    awaiting_delete_category = State()
    awaiting_new_level = State()
    awaiting_delete_level = State()
