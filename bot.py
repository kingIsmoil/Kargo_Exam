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


class Zakaz(StatesGroup):
    kod_id=State()
    vazn=State()
    adress=State()
zakaz=[]

class User(StatesGroup):
    phone_number = State()
    ind_id = State()

# Канопкахо
markub=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Номнавис кардан"),KeyboardButton(text="Заказ равон кардан")],
        [KeyboardButton(text="Филиалхои мо"),KeyboardButton(text="Оиди карго")]
    ],
    resize_keyboard=True
)





@dp.message(filters.Command("start"))
async def start_pol(message:Message,state:FSMContext):
    await message.answer("Ба Каргои Сомон мо хуш омадед барои хамкори ташаккур",reply_markup=markub)
    con = open_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,))
    user = cur.fetchone()
    if not user:
        await message.answer('vvedite nomer telephona')
        await state.set_state(User.phone_number)
    else:
        await message.answer('viuje zaregistrirovani')
        await message.answer('viberite knopki:', reply_markup=markub())

@dp.message(User.phone_number)
async def get_phone(message:Message,state:FSMContext):
    await state.update_data(phone_number = message.text)
    await message.answer('wwedite index')
    await state.set_state(User.ind_id)

@dp.message(User.ind_id)
async def get_ind(message:Message, state:FSMContext):
    await state.update_data(ind_id = message.text)
    data = await state.get_data()
    con = open_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO users(telegram_id, username, phone_number, ind_id) VALUES (?, ? , ?, ?)", 
            (message.from_user.id, message.from_user.full_name, data['phone_number'], data['ind_id']))
    con.commit()
    close_connection(con,cur)
    await message.answer('vi zaregistrirovani')

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
    zakaz= await state.update_data(adress=message.text)
    await message.answer("Шумо бомувафакият закази худро равон кардед. Дар муддати 15 то 25 руз даставка мекунем")




async def main():
    init_models()
    print('ok')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
