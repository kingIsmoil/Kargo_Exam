import asyncio
from aiogram import Bot, Dispatcher, types, F,filters
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


# Класи заказ равон кардан
class Zakaz(StatesGroup):
    kod_id=State()
    vazn=State()
    adress=State()
# Листи заказ
zakaz=[]


# Канопкахо
markub=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Номнавис кардан"),KeyboardButton(text="Заказ равон кардан")],
        [KeyboardButton(text="Филиалхои мо"),KeyboardButton(text="Оиди карго")]
    ],
    resize_keyboard=True
)




@dp.message(filters.Command("start"))
async def start_pol(message:Message):
    await message.answer("Ба Каргои Сомон мо хуш омадед барои хамкори ташаккур",reply_markup=markub)



@dp.message(F.text=="Заказ равон кардан")

async def zakaz_hundler(message:Message,state:FSMContext):
    await state.set_state(Zakaz.kod_id)
    await message.answer("Код id борро равон кунед: ")

@dp.message(Zakaz.kod_id)
async def kod_id_hundler(message:Message,state:FSMContext):
    await state.update_data(kod_id=message.text)
    await state.set_state(Zakaz.vazn)
    await message.answer("Бори шумо чанд кг аст :")

@dp.message(Zakaz.vazn)
async def vazn_hundler(message:Message,state:FSMContext):
    await state.update_data(vazn=message.text)
    await state.set_state(Zakaz.adress)
    await message.answer("Лутфан аддреси худро пурра равон кунед :")


@dp.message(Zakaz.adress)

async def adrez_hundler(message:Message,state:FSMContext):
    zakaz= await state.update_data(addres=message.text)
    await message.answer("Шумо бомувафакият закази худро равон кардед. Дар муддати 15 то 25 руз даставка мекунем")




@dp.message(F.text == 'Оиди карго')
async def a_baout(messege:Message):
    await messege.answer(
        """Cargo refers to the goods
           or merchandise that is transported from one
           location to another, typically by ship, aircraft,
           train, or truck. It encompasses a wide range of items, 
           including unfinished goods, finished products, machinery, 
           vehicles, and consumer goods. In essence, cargo is the 
           material being moved within shipping and logistics operations. 
           
           Our cargo will deliver your cargo safely, quickly and on time.
           """)
    
@dp.message(F.text == 'Филиалхои мо')
async def a_filial(messege:Message):
    await messege.answer(
        """
        We have 3 branches in the Republic of Tajikistan:\n
        1. "Ширин"factory, next to the factory 
        2. "Саховат" in front of the Саховат market
        3. "9 km", next to the "Шарк Транс"
        """
    )





async def main():
    init_models()
    print('ok')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
