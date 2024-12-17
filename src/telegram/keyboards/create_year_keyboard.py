from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_year_keyboard(schedule_tree: dict, faculty: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for year in schedule_tree[faculty].keys():
        builder.row(
            InlineKeyboardButton(
                text = year,
                callback_data = f'year_{year}'
            )
        )
    builder.adjust(3)
    return builder.as_markup()
