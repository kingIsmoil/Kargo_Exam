import asyncio
from aiogram import Bot, Dispatcher, types, F,filters
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from db import init_models, init_obj,init_kargos,show_zakaz,delete_zakaz,update_zakaz

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
    await state.update_data(adress=message.text)
    data = await state.get_data()
    init_kargos({
        "kod": data["kod_id"],
        "vazn": data["vazn"],
        "adress": data["adress"]
    })
    await message.answer("Шумо бомуваффақият закази худро равон кардед. Дар муддати 15 то 25 рӯз даставка мекунем.")
    await state.clear()







async def main():
    init_models()
    print('ok')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
