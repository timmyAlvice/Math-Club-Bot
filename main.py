# from aiogram.utils import executor
from create_bot import bot
from create_dispatcher import dp
import asyncio, logging

logging.basicConfig(level=logging.INFO)

async def main():
    # await bot.delete_webhook(drop_pending_updates=True)
    print("ALL UPDATES IS SUCSESSFULL\nBOT IS ONLINE")
    await dp.start_polling(bot)    

if __name__ == "__main__":
    asyncio.run(main())