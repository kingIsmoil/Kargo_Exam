import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from db import open_connection, init_models, close_connection

TOKEN = '8144030905:AAEYkyyWUJEq9YZ7IgLLHlHpO_-8pVwbBK0'

bot = Bot(token=TOKEN)
dp = Dispatcher()











async def main():
    init_models()
    print('ok')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
