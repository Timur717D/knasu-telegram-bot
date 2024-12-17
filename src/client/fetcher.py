import os

from aiohttp import ClientSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Fetcher:
    def __init__(self):
        self._cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'cache')
        self._schedule_page_path = os.path.join(self._cache_path, 'schedule.html')
        self._rpd_page_path = os.path.join(self._cache_path, 'rpd.html')
    
    async def get_schedule_page(self):
        if os.path.exists(self._schedule_page_path):
            with open(self._schedule_page_path, 'r', encoding='utf-8') as file:
                return file.read()

        async with ClientSession() as session:
            async with session.get('https://knastu.ru/students/schedule') as response:
                schedule_page = await response.text()
                with open(self._schedule_page_path, 'w', encoding='utf-8') as file:
                    file.write(schedule_page)
                return schedule_page
            
    async def get_rpd_page(self):
        if os.path.exists(self._rpd_page_path):
            with open(self._rpd_page_path, 'r', encoding='utf-8') as file:
                return file.read()

        async with ClientSession() as session:
            async with session.get('https://knastu.ru/sveden/education') as response:
                rpd_page = await response.text()
                with open(self._rpd_page_path, 'w', encoding='utf-8') as file:
                    file.write(rpd_page)
                return rpd_page
            
    async def get_rpd_direction_page(self, filename: str):
        rpd_page_direction_path = os.path.join(self._cache_path, f'rpd_direction{'_'.join(filename.split('/'))}.html')
        if os.path.exists(rpd_page_direction_path):
            with open(rpd_page_direction_path, 'r', encoding='utf-8') as file:
                return file.read()

        async with ClientSession() as session:
            async with session.get(f'https://knastu.ru{filename}') as response:
                rpd_page_direction = await response.text()

                with open(rpd_page_direction_path, 'w', encoding='utf-8') as file:
                    file.write(rpd_page_direction)
                return rpd_page_direction
            
    async def get_rpd_direction_end_page(self, filename: str):
        rpd_page_direction_end_path = os.path.join(self._cache_path, f'rpd_direction_end_{'_'.join(filename.split('/'))}.html')
        rpd_page_direction_end_path = rpd_page_direction_end_path.replace('?', '_')
        if os.path.exists(rpd_page_direction_end_path):
            with open(rpd_page_direction_end_path, 'r', encoding='utf-8') as file:
                return file.read()

        async with ClientSession() as session:
            async with session.get(f'https://knastu.ru/sveden/education/{filename}') as response:
                rpd_page_direction_end = await response.text()

                with open(rpd_page_direction_end_path, 'w', encoding='utf-8') as file:
                    file.write(rpd_page_direction_end)
                return rpd_page_direction_end
    
    def take_schedule_screenshot(self, link: str, date: str):
        full_link = f'https://knastu.ru{link}?day={date}'
        print('link', full_link)
        filename = f'{link.split('/')[-1]}_{date.replace('.', '_')}.png'
        schedule_screenshot_path = os.path.join(self._cache_path, filename)
        if not os.path.exists(schedule_screenshot_path):
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Firefox(options=options)
            driver.get(full_link)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cookie_notification > div > button'))).click()
            element = driver.find_element(By.CSS_SELECTOR, '#cb-content > section > div > div > div > table')
            element.screenshot(schedule_screenshot_path)
            driver.quit()
        return schedule_screenshot_path
