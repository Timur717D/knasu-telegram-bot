from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_faculty_keyboard(schedule_tree: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for faculty in schedule_tree.keys():
        builder.row(
            InlineKeyboardButton(
                text = faculty,
                callback_data = f'faculty_{faculty}'
            )
        )
    builder.adjust(3)
    return builder.as_markup()
