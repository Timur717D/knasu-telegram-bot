import os

import aiosqlite

from models.user import User

class Database:
    def __init__(self):
        self._db = None
        self._filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        self._filename = os.path.join(self._filepath, 'database.db')

    async def __aenter__(self):
        self._db = await aiosqlite.connect(self._filename)

    async def __aexit__(self, exc_type, exc, tb):
        await self._db.close()

    async def create_users_table(self):
        await self._db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                faculty TEXT NOT NULL,
                year INTEGER NOT NULL,
                study_group TEXT NOT NULL
            )
        ''')
        await self._db.commit()

    async def get_user(self, id: int) -> User | None:
        response = await self._db.execute('''
            SELECT * FROM users WHERE id = ?
        ''', (id,))
        user_tuple = await response.fetchone()
        return None if user_tuple == None else User(*user_tuple)
    
    async def add_user(self, id: int, faculty: str, year: int, study_group: str):
        await self._db.execute('''
            INSERT OR REPLACE INTO users (id, faculty, year, study_group)
                VALUES (?, ?, ?, ?)
        ''', (id, faculty, year, study_group))
        await self._db.commit()
    
    async def remove_user(self, id: int):
        await self._db.execute('''
            DELETE FROM users WHERE id = ?
        ''', (id,))
        await self._db.commit()

    async def create_faculties_table(self):
        await self._db.execute('''
            CREATE TABLE IF NOT EXISTS faculties (
                name TEXT PRIMARY KEY
            )
        ''')
        await self._db.execute('''
            INSERT OR REPLACE INTO faculties (name)
                VALUES ('СГФ'), ('ФАМТ'), ('ФКС'), ('ФКТ'), ('ФМХТ'), ('ФЭУ') 
        ''')
        await self._db.commit()
    
    async def get_faculties(self):
        response = await self._db.execute('''
            SELECT * FROM faculties
        ''')
        faculty_names = list(map(lambda faculty: faculty[0], await response.fetchall()))
        return faculty_names
