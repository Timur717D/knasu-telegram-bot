import json
import os

from client.fetcher import Fetcher
from client.parser import Parser1
from database import Database

async def get_static(database: Database, fetcher: Fetcher, parser1: Parser1):
    schedule_page = await fetcher.get_schedule_page()

    faculties = await database.get_faculties()

    schedule_tree = parser1.parse_schedule_page(schedule_page, faculties)


    messages_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'messages.json')
    with open(messages_path, 'r', encoding='utf-8') as file:
        messages = json.loads(file.read())
        return schedule_tree, messages