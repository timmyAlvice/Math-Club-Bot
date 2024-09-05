# from aiogram.utils import executor
from create_bot import bot, dp
# from handlers import 
import asyncio

# register_handlers(dp)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def on_startup(_):
    print('ALL UPDATES IS SUCSESSFULL\nBOT IS ONLINE')

if __name__ == "__main__":
    asyncio.run(main())