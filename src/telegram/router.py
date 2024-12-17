from datetime import date, datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from bs4 import BeautifulSoup

from models.context import Context
from telegram.keyboards.create_faculty_keyboard import create_faculty_keyboard
from telegram.keyboards.create_year_keyboard import create_year_keyboard
from telegram.keyboards.create_study_group_keyboard import create_study_group_keyboard
from telegram.keyboards.create_schedule_keyboard import create_schedule_keyboard, create_teacher_schedule_keyboard
from telegram.keyboards.create_start_keyboard import create_start_keyboard
from telegram.keyboards.create_semester_keyboard import create_semester_keyboard
from telegram.keyboards.create_semester_fos_keyboard import create_semester_fos_keyboard
from telegram.keyboards.create_discipline_keyboard import create_discipline_keyboard
from telegram.keyboards.create_discipline_fos_keyboard import create_discipline_fos_keyboard
from telegram.keyboards.create_teacher_keyboard import choice_letter, choice_teacher

from client.schedule_teachers import get_block_data, get_href_teacher, get_html_content, get_letters, get_teacher

router = Router()

#=====================================================================================================
@router.message(F.text == '📋 РПД')
async def get_rpd_link(message: Message, context: Context, state: FSMContext):
    await state.clear()
    id = message.chat.id
    user = await context.database.get_user(id)
    result = {}
    soup = BeautifulSoup(await context.fetcher.get_rpd_page(), 'lxml')
    directions = soup.find_all('div', class_ = 'w-100')
    for direction in directions[1:-1]:
        direction_name = direction.find('div', class_ = 'direction-name')
        if direction_name.text.strip() == (context.schedule_tree[user.faculty][str(user.year)][user.study_group])[-2]:
            direction_level = (direction.find('div', class_ = 'direction-level')).get('title')
            if direction_level == (context.schedule_tree[user.faculty][str(user.year)][user.study_group][-1]):
                direction_href = (direction.find('a', {'href': True})).get('href')
                result[user.study_group] = direction_href

    soup = BeautifulSoup(await context.fetcher.get_rpd_direction_page(result[user.study_group]), 'lxml')
    block_specialities = soup.find('table', class_ = 'table')
    info_speciality = block_specialities.find_all('a', attrs={'href': True, 'target':'_blank'})
    for href in info_speciality:
        if 'РПД' in href.text:
            href = href.get('href')
            soup2 = BeautifulSoup(await context.fetcher.get_rpd_direction_end_page(href), 'lxml')
            name_group = soup2.find('h3', class_ = 'align-right main_head').text
            if user.study_group in name_group:
                #
                disciplines = soup2.find_all('tr', attrs={'data-type':'dis', 'data-sms-number': True})
                semester_and_discipline = {}
                for discipline in disciplines:
                    if 'РПД' in discipline.text:
                        hrefs = discipline.find_all('a', {'href': True})
                        for href in hrefs:
                            if 'РПД' in href.text:
                                href = href.get('href')
                                discipline_name = discipline.find('td').text
                                semester = discipline.get('data-sms-number')
                                if len(discipline_name) > 28:
                                    semester_and_discipline[(semester, discipline_name[:28])] = href
                                else: 
                                    semester_and_discipline[(semester, discipline_name)] = href
    await state.update_data(semester_and_discipline)
    await message.answer(
        context.messages['choice_semester'],
        reply_markup=create_semester_keyboard(semester_and_discipline))

@router.callback_query(F.data.startswith('semester_'))
async def get_rpd_discipline(call: CallbackQuery, context: Context, state: FSMContext):
    semester_and_discipline = await state.get_data()
    semester = int(call.data.split('_')[-1])
    await call.message.edit_text(
        context.messages['choice_discipline'],
        reply_markup=create_discipline_keyboard(semester, semester_and_discipline))
    
@router.callback_query(F.data.startswith('dis='))
async def get_file_rpd_discipline(call: CallbackQuery, context: Context, state: FSMContext):
    semester_and_discipline = await state.get_data()
    discipline = call.data.split('=')[1]
    semester = call.data.split('=')[-1]
    href = semester_and_discipline[(semester, discipline)]
    href = '%20'.join(href.split(' '))
    await call.message.delete()
    await call.message.answer_document(
        f'https://knastu.ru{href}', caption=context.messages['rpd_given'])
    await state.clear()
#===============================================================================================

#===============================================================================================
@router.message(F.text == '📑 Материалы для экз.')
async def get_exam_link(message: Message, context: Context, state: FSMContext):
    await state.clear()
    id = message.chat.id
    user = await context.database.get_user(id)
    result = {}
    soup = BeautifulSoup(await context.fetcher.get_rpd_page(), 'lxml')
    directions = soup.find_all('div', class_ = 'w-100')
    for direction in directions[1:-1]:
        direction_name = direction.find('div', class_ = 'direction-name')
        if direction_name.text.strip() == (context.schedule_tree[user.faculty][str(user.year)][user.study_group])[-2]:
            direction_level = (direction.find('div', class_ = 'direction-level')).get('title')
            if direction_level == (context.schedule_tree[user.faculty][str(user.year)][user.study_group][-1]):
                direction_href = (direction.find('a', {'href': True})).get('href')
                result[user.study_group] = direction_href

    soup = BeautifulSoup(await context.fetcher.get_rpd_direction_page(result[user.study_group]), 'lxml')
    block_specialities = soup.find('table', class_ = 'table')
    info_speciality = block_specialities.find_all('a', attrs={'href': True, 'target':'_blank'})
    for href in info_speciality:
        if 'РПД' in href.text:
            href = href.get('href')
            soup2 = BeautifulSoup(await context.fetcher.get_rpd_direction_end_page(href), 'lxml')
            name_group = soup2.find('h3', class_ = 'align-right main_head').text
            if user.study_group in name_group:
                #
                disciplines = soup2.find_all('tr', attrs={'data-type':'dis', 'data-sms-number': True})
                semester_and_discipline = {}
                for discipline in disciplines:
                    fos = discipline.find_all('td', {'style':'width: 0'})[-1]
                    if 'ФОС' in fos.text:
                        href = fos.find('a', {'href': True})
                        href = href.get('href')
                        discipline_name = discipline.find('td').text
                        semester = discipline.get('data-sms-number')
                        if len(discipline_name) > 28:
                            semester_and_discipline[(semester, discipline_name[:28])] = href
                        else: 
                            semester_and_discipline[(semester, discipline_name)] = href
    await state.update_data(semester_and_discipline)
    if semester_and_discipline:
        await message.answer(
            context.messages['choice_semester'],
            reply_markup=create_semester_fos_keyboard(semester_and_discipline))
    else:
        await message.answer(
            context.messages['exam_null'],
            reply_markup=None)
    
@router.callback_query(F.data.startswith('semester2_'))
async def get_exam_discipline(call: CallbackQuery, context: Context, state: FSMContext):
    semester_and_discipline = await state.get_data()
    semester = int(call.data.split('_')[-1])
    await call.message.edit_text(
        context.messages['choice_discipline'],
        reply_markup=create_discipline_fos_keyboard(semester, semester_and_discipline))
    
@router.callback_query(F.data.startswith('dis2='))
async def get_file_exam_discipline(call: CallbackQuery, context: Context, state: FSMContext):
    semester_and_discipline = await state.get_data()
    discipline = call.data.split('=')[1]
    semester = call.data.split('=')[-1]
    href = semester_and_discipline[(semester, discipline)]
    href = '%20'.join(href.split(' '))
    await call.message.delete()
    await call.message.answer_document(
        f'https://knastu.ru{href}', caption=context.messages['exam_given'])
    await state.clear()
    
#===============================================================================================
#===============================================================================================
@router.message(F.text == '🗓 КУГ')
async def get_kyg_link(message: Message, context: Context, state: FSMContext):
    await state.clear()
    id = message.chat.id
    user = await context.database.get_user(id)
    result = {}
    soup = BeautifulSoup(await context.fetcher.get_rpd_page(), 'lxml')
    directions = soup.find_all('div', class_ = 'w-100')
    for direction in directions[1:-1]:
        direction_name = direction.find('div', class_ = 'direction-name')
        if direction_name.text.strip() == (context.schedule_tree[user.faculty][str(user.year)][user.study_group])[-2]:
            direction_level = (direction.find('div', class_ = 'direction-level')).get('title')
            if direction_level == (context.schedule_tree[user.faculty][str(user.year)][user.study_group][-1]):
                direction_href = (direction.find('a', {'href': True})).get('href')
                result[user.study_group] = direction_href

    soup = BeautifulSoup(await context.fetcher.get_rpd_direction_page(result[user.study_group]), 'lxml')
    block_specialities = soup.find('table', class_ = 'table')
    info_speciality = block_specialities.find_all('a', attrs={'href': True, 'target':'_blank'})
    for href in info_speciality:
        href = href.get('href')
        if 'КУГ' in href:
            if user.study_group in href:
                break

    href = '%20'.join(href.split(' '))
    await message.answer_document(f'https://knastu.ru{href}',
        caption=context.messages['kyg_given']
        )
#====================================================================================================
@router.message(CommandStart())
async def start(message: Message, state: FSMContext, context: Context):
    id = message.chat.id
    user = await context.database.get_user(id)
    if not user:
        await first_registration(message, state, context)
    else:
        await main_menu(message, state, context)

async def first_registration(message: Message, state: FSMContext, context: Context):
    await message.answer(
        context.messages['first_registration'],
        reply_markup=create_faculty_keyboard(context.schedule_tree)
    )

@router.message(F.text == "Изменить данные")
async def enter_faculty(message: Message, state: FSMContext, context: Context):
    await message.answer(
        context.messages['enter_faculty'],
        reply_markup=create_faculty_keyboard(context.schedule_tree)
    )

@router.callback_query(F.data.startswith('faculty'))
async def enter_year(call: CallbackQuery, state: FSMContext, context: Context):
    faculty = call.data.split('_')[-1]
    await state.update_data(faculty=faculty)
    await call.message.edit_text(
        context.messages['enter_year'],
        reply_markup=create_year_keyboard(context.schedule_tree, faculty)
    )

@router.callback_query(F.data.startswith('year'))
async def enter_study_group(call: CallbackQuery, state: FSMContext, context: Context):
    data = await state.get_data()
    year = call.data.split('_')[-1]
    await state.update_data(year=year)
    await call.message.edit_text(
        context.messages['enter_study_group'],
        reply_markup=create_study_group_keyboard(context.schedule_tree, data['faculty'], year)
    )

@router.callback_query(F.data.startswith('study_group'))
async def successful_registraion(call: CallbackQuery, state: FSMContext, context: Context):
    data = await state.get_data()
    study_group = call.data.split('_')[-1]
    await state.update_data(study_group=study_group)
    await context.database.add_user(
        call.message.chat.id,
        data['faculty'],
        data['year'],
        study_group     
    )
    await call.answer(context.messages['successful_registration'], show_alert=True)
    await call.message.delete()
    await call.message.answer(
        context.messages['main_menu'],
        reply_markup=create_start_keyboard()
    )

@router.callback_query(F.data == 'show_main_menu')
async def show_main_menu(call: CallbackQuery, state: FSMContext, context: Context):
    await state.clear()
    await call.message.delete()
    await main_menu(call.message, state, context)

async def main_menu(message: Message, state: FSMContext, context: Context):
    await message.answer(
        context.messages['main_menu'],
        reply_markup=create_start_keyboard()
    )

@router.message(F.text == "Расписание группы")
async def get_schedule(message: Message, state: FSMContext, context: Context):
    try:
        if not isinstance(message, Message):
            message = message.message
        data = await state.get_data()
        if 'date' not in data:
            await state.update_data(date=date.today().strftime('%d.%m.%Y'))
            data = await state.get_data()
        user = await context.database.get_user(message.chat.id)
        link = context.schedule_tree[user.faculty][str(user.year)][user.study_group]
        schedule_screenshot_path = context.fetcher.take_schedule_screenshot(link[0], data['date'])
        if message.content_type == ContentType.TEXT:
            await message.answer_photo(
                FSInputFile(path=schedule_screenshot_path),
                reply_markup=create_schedule_keyboard()
            )
        else:
            await message.edit_media(
                InputMediaPhoto(media=FSInputFile(path=schedule_screenshot_path)),
                reply_markup=create_schedule_keyboard()
            )
    except Exception:
        await message.answer('Нет расписания у данного преподавателя на текущую неделю.')

@router.message(F.text == "Расписание преподавателя")
async def get_inline_btn_link22(message: Message, state: FSMContext):
    await message.answer(f'Выберите букву фамилии преподавателя:', 
                         reply_markup=await choice_letter())

@router.callback_query(lambda call: call.data.startswith('letter'))
async def get_inline_btn_link23(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Выберите преподавателя:', 
                         reply_markup=await choice_teacher(call.data))

@router.callback_query(lambda call: call.data.startswith('teacher'))
async def get_teacher_schedule(call: CallbackQuery, state: FSMContext, context: Context):
    try:
        value = None
        if 'teacher_' in call.data:
            value = call.data
            await state.update_data(teacher_key=call.data)
        else:
            data = await state.get_data()
            value = data['teacher_key']
        link = await get_href_teacher(value)
        data = await state.get_data()
        if 'teacher_date' not in data:
            await state.update_data(teacher_date=date.today().strftime('%d.%m.%Y'))
            data = await state.get_data()
        schedule_screenshot_path = context.fetcher.take_schedule_screenshot(link[17:], data['teacher_date'])
        if call.message.content_type == ContentType.TEXT:
            await call.message.delete()
            await call.message.answer_photo(
                FSInputFile(path=schedule_screenshot_path),
                reply_markup=create_teacher_schedule_keyboard()
            )
        else:
            await call.message.edit_media(
                InputMediaPhoto(media=FSInputFile(path=schedule_screenshot_path)),
                reply_markup=create_teacher_schedule_keyboard()
            )
    except Exception:
        await call.message.answer('Нет расписания у данного преподавателя на текущую неделю.')
    
@router.callback_query(F.data == 'get_prev_teacherschedule')
@router.callback_query(F.data == 'get_next_teacherschedule')
async def get_prev_schedule(call: CallbackQuery, state: FSMContext, context: Context):
    data = await state.get_data()
    delta = -7 if call.data == 'get_prev_teacherschedule' else 7
    new_date = (datetime.strptime(data['teacher_date'], '%d.%m.%Y') + timedelta(days=delta)).strftime('%d.%m.%Y')
    await state.update_data(teacher_date=new_date)
    await get_teacher_schedule(call, state, context)

@router.callback_query(F.data == 'get_prev_schedule')
@router.callback_query(F.data == 'get_next_schedule')
async def get_prev_schedule(call: CallbackQuery, state: FSMContext, context: Context):
    data = await state.get_data()
    delta = -7 if call.data == 'get_prev_schedule' else 7
    new_date = (datetime.strptime(data['date'], '%d.%m.%Y') + timedelta(days=delta)).strftime('%d.%m.%Y')
    await state.update_data(date=new_date)
    await get_schedule(call, state, context)
