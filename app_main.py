from aiogram import executor
from regular_commands import commands
import logging
from config import dp
import DataBase
import os


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    DataBase.start()

commands(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup, timeout=2)
