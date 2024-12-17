from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
from datetime import timedelta, date, datetime
from playwright.async_api import async_playwright
async def get_html_content(url):
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            html = await response.text()
            return html
        
async def get_block_data():
    url = 'https://knastu.ru/teachers/schedule' 
    html = await get_html_content(url)
    soup = BeautifulSoup(html, 'lxml')
    block = soup.find('div', class_ = 'col-md-12')
    return block
async def get_letters():
    letters = await get_block_data()
    letters = letters.find_all('a', attrs={'title': 'Перейти к букве', 'class': 'btn btn-default btn-small'})
    letter_dict = {}
    for index, letter in enumerate(letters):
        letter_dict[f'letter_{index}'] = letter.text
    return letter_dict
async def get_teacher(letter_key):
    global teachers
    l = await get_letters()
    teachers = await get_block_data()
    letters = teachers.find_all('a', attrs={'name': True})
    for letter in letters:
        if letter.get('name') == l.get(letter_key):
            teachers = teachers.find_all('div', attrs={'style':'display:block', 'class':'col-md-12'})
            for index, teacher in enumerate(teachers):
                if teacher.text.strip()[0] == letter.get('name'):
                    teachers = teachers[index].find_all('div', class_='col-md-4')
                    break
    global dict_teachers
    dict_teachers = {}
    for index, teach in enumerate(teachers):
        dict_teachers[f'teacher_{index}'] = ' '.join(teach.text.split('\xa0')).strip()
    return dict_teachers
async def get_href_teacher(teacher_key):
    for href in teachers:
        href = href.find('a', href=True)
        if dict_teachers.get(teacher_key) == ' '.join(href.text.split('\xa0')).strip(): 
            href = href.get('href')
            break
    link_teacher = f'https://knastu.ru{href}'
    return link_teacher