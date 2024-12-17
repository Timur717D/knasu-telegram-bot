from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_study_group_keyboard(schedule_tree: dict, faculty: str, year: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for study_group in schedule_tree[faculty][year]:
        builder.row(
            InlineKeyboardButton(
                text = study_group,
                callback_data = f'study_group_{study_group}'
            )
        )
    builder.adjust(3)
    return builder.as_markup()
