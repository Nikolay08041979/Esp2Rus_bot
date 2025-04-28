# bot/states/__init__.py
from aiogram.fsm.state import State, StatesGroup

class QuizState(StatesGroup):
    CategorySelected = State()
    LevelSelected = State()
    AwaitingWordCount = State()
    in_quiz = State()
