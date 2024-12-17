from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_schedule_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text = '⬅️',
            callback_data = 'get_prev_schedule' 
        ),
        InlineKeyboardButton(
            text = '➡️',
            callback_data = 'get_next_schedule'
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def create_teacher_schedule_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text = '⬅️',
            callback_data = 'get_prev_teacherschedule' 
        ),
        InlineKeyboardButton(
            text = '➡️',
            callback_data = 'get_next_teacherschedule'
        )
    )
    builder.adjust(2)
    return builder.as_markup()
