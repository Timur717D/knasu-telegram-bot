from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_semester_keyboard(semester_and_discipline: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    semesters = sorted(set([int(i[0]) for i in semester_and_discipline.keys()]))
    for semester in semesters:
        builder.row(
            InlineKeyboardButton(
                text = str(semester),
                callback_data = f'semester_{semester}'
            )
        )
    builder.adjust(4)
    return builder.as_markup()
