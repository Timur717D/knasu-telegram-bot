from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from client.schedule_teachers import get_letters, get_teacher
import asyncio

async def choice_letter() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    letter = await get_letters()
    for letter_key, letter_value in letter.items():
        builder.row(
            InlineKeyboardButton(
                text = letter_value,
                callback_data = letter_key
            )
        )
    builder.adjust(8)
    return builder.as_markup()
async def choice_teacher(data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    teachers = await get_teacher(data)
    for teacher_key, teacher_value in teachers.items():
        builder.row(
            InlineKeyboardButton(
                text = teacher_value,
                callback_data = teacher_key
            )
        )
    builder.adjust(1)
    return builder.as_markup()