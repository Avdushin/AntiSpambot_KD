from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
bot = Bot(token=config.get("TOKEN"))
pay_token= config.get("PAY_TOKEN")

user = config.get("user")
password= config.get("password")
host= config.get("host")
port= config.get("port")
database= config.get("database")

dp = Dispatcher(bot, storage=MemoryStorage())