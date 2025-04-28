from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

# --- Reply Keyboards ---

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def category_keyboard(categories: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat, callback_data=f"cat:{cat}")] for cat in categories
        ]
    )


def level_keyboard(levels: list[str]) -> ReplyKeyboardMarkup:
    """
    Генерация клавиатуры уровней сложности.
    Используется после выбора категории, в состоянии QuizState.CategorySelected → LevelSelected.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=level)] for level in levels] + [[KeyboardButton(text="все уровни")]],
        resize_keyboard=True
    )



def quiz_options_keyboard(options: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in options] + [[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )

start_over_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")]
    ],
    resize_keyboard=True
)

def answer_keyboard(options: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in options],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# --- Inline Keyboards (если появятся) ---

def confirm_upload_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_upload")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_upload")]
        ]
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика по категориям", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📊 Статистика по уровням", callback_data="admin_stats_levels")],
        [InlineKeyboardButton(text="➕ Добавить категорию", callback_data="admin_add_category")],
        [InlineKeyboardButton(text="🗑 Удалить категорию", callback_data="admin_delete_category")],
        [InlineKeyboardButton(text="📘 Посмотреть уровни", callback_data="admin_list_levels")],
        [InlineKeyboardButton(text="➕ Добавить уровень", callback_data="admin_add_level")],
        [InlineKeyboardButton(text="🗑 Удалить уровень", callback_data="admin_delete_level")]
    ])