import asyncio
from aiogram import Bot, Dispatcher, types, F,filters
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from db import init_models, init_obj,init_kargos,show_zakaz,delete_zakaz,update_kargo_full,open_connection,close_connection

TOKEN = '8144030905:AAEYkyyWUJEq9YZ7IgLLHlHpO_-8pVwbBK0'

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Zakaz(StatesGroup):
    kod_id=State()
    vazn=State()
    adress=State()
    user_id=State()
zakaz=[]

class EditZakaz(StatesGroup):
    zakaz_id = State()
    field = State()
    new_value = State()


class User(StatesGroup):
    phone_number = State()
    ind_id = State()
    telegram_id=State()
markub=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заказ равон кардан"),KeyboardButton(text="update zakaz")],
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
        await message.answer('viberite knopki:', reply_markup=markub)

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
    await state.clear()

@dp.message(F.text=="Заказ равон кардан")
async def zakaz_hundler(message:Message,state:FSMContext):
    await state.set_state(Zakaz.kod_id)
    await message.answer("Код id борро равон кунед: ")

# 3. Гирифтани kod_id ва гузаштан ба вазн
@dp.message(Zakaz.kod_id)
async def kod_id_hundler(message: Message, state: FSMContext):
    await state.update_data(kod_id=message.text)
    await state.set_state(Zakaz.vazn)
    await message.answer("Бори шумо чанд кг аст?")

@dp.message(Zakaz.vazn)
async def vazn_hundler(message: Message, state: FSMContext):
    await state.update_data(vazn=message.text)
    await state.set_state(Zakaz.user_id)
    await message.answer("Лутфан, инчоро клик  кунед /sendaddress.")

@dp.message(Zakaz.user_id)
async def get_user(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(Zakaz.adress)
    await message.answer("Ҳозир адреси пурраи худро ворид кунед:")

GROUP_ID = -1002525875441
@dp.message(Zakaz.adress)
async def adress_hundler(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    data = await state.get_data()

    init_kargos({
        "kod": data["kod_id"],
        "vazn": data["vazn"],
        "adress": data["adress"],
        "user_id": data["user_id"]
    })

    await message.answer(
        "Шумо бомуваффақият фармоиши худро равон кардед. Дар муддати 15–25 рӯз даставка мекунем."
    )
    await bot.send_message(
        GROUP_ID,
        f" ot {message.from_user.full_name}:\n\n{data['kod_id']}\n {data['adress']} \n {data['adress']}"
    )
    await state.clear()


@dp.message(F.text == 'update zakaz')
async def edit_zakaz_start(message: Message, state: FSMContext):
    await message.answer("Ид заказа, который хотите изменить:")
    await state.set_state(EditZakaz.zakaz_id)
@dp.message(EditZakaz.zakaz_id)
async def get_zakaz_id(message: Message, state: FSMContext):
    await state.update_data(zakaz_id=message.text)
    await message.answer("Что хотите изменить? Напишите: `kod`, `vazn`, или `adress`.")
    await state.set_state(EditZakaz.field)
@dp.message(EditZakaz.field)
async def get_field(message: Message, state: FSMContext):
    field = message.text
    if field not in ["kod", "vazn", "adress"]:
        await message.answer("Только: `kod`, `vazn`, или `adress`.")
        return
    await state.update_data(field=field)
    await message.answer("Напишите новое значение:")
    await state.set_state(EditZakaz.new_value)
@dp.message(EditZakaz.new_value)
async def apply_update(message: Message, state: FSMContext):
    data = await state.get_data()
    zakaz_id = int(data["zakaz_id"])
    field = data["field"]
    new_value = message.text

    # Вызов функции
    if field == "kod":
        update_kargo_full(zakaz_id, new_kod=new_value)
    elif field == "vazn":
        update_kargo_full(zakaz_id, new_vazn=new_value)
    elif field == "adress":
        update_kargo_full(zakaz_id, new_adres=new_value)

    await message.answer(f"Заказ {zakaz_id} обновлен: поле `{field}` теперь «{new_value}».")
    await state.clear()




@dp.message(F.text == 'Оиди карго')
async def a_baout(messege:Message):
    await messege.answer(
        """ Мо Somon Cargo карго барои бехатар ва 
            зуд дар вакти муайян бурда расонидани борхои 
            шумо . Мо борхо шуморо метавонем дар муддати 
            15-25 руз оварда мерасонем . Нархи хизматрасонии 
            мо аз 2$ то 3$ мебошад ва хато дар дохили шахри
            Душанбе доставкаи ройгон дорем. мо ба хизматрасони 
            худ кафолат медихем ки борхои шуморо дар вакти
            муайян ва бе мушкили мерасонем.
        """)
    
    
@dp.message(F.text == 'Филиалхои мо')
async def a_filial(messege:Message):
    await messege.answer(
    """
        Мо дар Чумхурии Точикистон 3 то филиали худро дорем:\n
        1. Фабрикаи "Ширин" -  дар назди фабрика
        2. "Саховат" - пушти бозори Саховат
        3. "9 km" - дар наздики "Шарк Транс"
    """
    )






async def main():
    init_models()
    print('ok')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
