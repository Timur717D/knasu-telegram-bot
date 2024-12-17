from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_choice_schedule() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text = '👤 Расписание группы',
            callback_data = 'get_student_schedule'
        ),
        InlineKeyboardButton(
            text = '👩‍🏫 Расписание преподавателя',
            callback_data = 'teacher_schedule'
        )
    )
    builder.adjust(1, repeat=True)
    return builder.as_markup()