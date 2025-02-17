from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
bot = Bot(token=TG_TOKEN)