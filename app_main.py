from aiogram import Bot, Dispatcher, executor
from regular_commands import commands
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from config import dp
import DataBase
import os


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    DataBase.start()

commands(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
