import asyncio
from aiogram import Bot, Dispatcher ,F
from aiogram.filters import CommandStart ,Command
from aiogram.types import Message

from handlers import router
dp = Dispatcher()

bot = Bot(token='YOUR_BOT_TOKEN')

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')