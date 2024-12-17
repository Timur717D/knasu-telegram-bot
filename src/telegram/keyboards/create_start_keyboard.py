from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_start_keyboard():
    buttons = [
        [KeyboardButton(text="Расписание группы"), KeyboardButton(text="Расписание преподавателя")],
        [KeyboardButton(text="📋 РПД"), KeyboardButton(text="🗓 КУГ")], 
        [KeyboardButton(text="📑 Материалы для экз."), KeyboardButton(text="Изменить данные")]
    ]

    keyboard = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Воспользуйтесь меню:")
    
    return keyboard
