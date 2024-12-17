from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_discipline_fos_keyboard(semester: int, semester_and_discipline: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for discipline in semester_and_discipline.keys():
        sem = int(discipline[0])
        discipline = discipline[1]
        if sem == semester:
            builder.row(
                InlineKeyboardButton(
                    text = discipline,
                    callback_data = f'dis2={discipline}={semester}'
                )
            )
    builder.adjust(1)
    return builder.as_markup()
