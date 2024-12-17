import asyncio

from database import Database
from client.fetcher import Fetcher
from client.parser import Parser1
from client.get_static import get_static
from models.context import Context
from telegram.bot import bot, dispatcher
from telegram.router import router


async def main():
    database = Database()
    fetcher = Fetcher()
    parser1 = Parser1()

    async with database:
        await database.create_faculties_table()
        await database.create_users_table()

        static = await get_static(database, fetcher, parser1)

        context = Context(database, fetcher, parser1, static)

        dispatcher.include_router(router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot, context=context)

if __name__ == "__main__":
    asyncio.run(main())