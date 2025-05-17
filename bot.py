import asyncio
from aiogram import Bot, Dispatcher, types, F, filters
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from db import (
    init_models, init_kargos, show_zakaz,
    delete_zakaz, open_connection, close_connection
)

TOKEN = "7955520574:AAFnwODOcjoz4tavTWvwN3_RNzPIwUpe_yA"  

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Zakaz(StatesGroup):
    kod_id = State()
    vazn = State()
    adress = State()
    user_id = State()
    deleted_id = State()

class User(StatesGroup):
    phone_number = State()
    ind_id = State()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Заказ равон кардан")],
        [KeyboardButton(text="🏢 Филиалхои мо"), KeyboardButton(text="ℹ️ Оиди карго")],
        [KeyboardButton(text="📋 Дидани заказхо"), KeyboardButton(text="❌ Отмена заказ")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Хуш омадед ба Somon Cargo!", reply_markup=main_menu)
    con = open_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,))
    user = cur.fetchone()
    if not user:
        await message.answer("📞 Рақами телефони худро ворид кунед:")
        await state.set_state(User.phone_number)
    else:
        await message.answer("📌 Аз меню интихоб кунед:")
    close_connection(con, cur)

@dp.message(User.phone_number)
async def get_phone(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Илтимос, танҳо рақам ворид кунед.")
        return
    await state.update_data(phone_number=message.text)
    await message.answer("📮 Индекси почтаро ворид кунед:")
    await state.set_state(User.ind_id)

@dp.message(User.ind_id)
async def get_ind(message: Message, state: FSMContext):
    data = await state.get_data()
    con = open_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users(telegram_id, username, phone_number, ind_id) VALUES (?, ?, ?, ?)",
        (message.from_user.id, message.from_user.full_name, data["phone_number"], message.text)
    )
    con.commit()
    close_connection(con, cur)
    await state.clear()
    await message.answer("🎉 Шумо бомуваффақият сабт шудед!", reply_markup=main_menu)

@dp.message(F.text == "📦 Заказ равон кардан")
async def zakaz_start(message: Message, state: FSMContext):
    await state.set_state(Zakaz.kod_id)
    await message.answer("🔢 Код ID-и борро ворид кунед:")

@dp.message(Zakaz.kod_id)
async def zakaz_vazn(message: Message, state: FSMContext):
    await state.update_data(kod_id=message.text)
    await state.set_state(Zakaz.vazn)
    await message.answer("⚖️ Вазни борро ворид кунед (кг):")

@dp.message(Zakaz.vazn)
async def zakaz_adress(message: Message, state: FSMContext):
    if not message.text.replace(".", "").isdigit():
        await message.answer("❗ Лутфан, вазнро бо рақам нависед!")
        return
    await state.update_data(vazn=message.text)
    await state.set_state(Zakaz.adress)
    await message.answer("📍 Адреси пурраро ворид кунед:")

@dp.message(Zakaz.adress)
async def zakaz_finish(message: Message, state: FSMContext):
    await state.update_data(adress=message.text, user_id=message.from_user.id)
    data = await state.get_data()
    init_kargos({
        "kod": data["kod_id"],
        "vazn": data["vazn"],
        "adress": data["adress"],
        "user_id": data["user_id"]
    })
    await message.answer("✅ Закази шумо қабул шуд. Дар 15–25 рӯз мерасад.")
    await state.clear()

@dp.message(F.text == "📋 Дидани заказхо")
async def show_my_orders(message: Message):
    zakazho = show_zakaz()
    if not zakazho:
        await message.answer("⛔ Шумо ягон заказ надоред.")
        return
    response = "📦 Заказҳои шумо:\n\n"
    for zakaz in zakazho:
        response += (
            f"🔢 Код: {zakaz[1]}\n"
            f"⚖️ Вазн: {zakaz[2]} кг\n"
            f"📍 Адрес: {zakaz[3]}\n\n"
        )
    await message.answer(response)

@dp.message(F.text == "❌ Отмена заказ")
async def delete_order_prompt(message: Message, state: FSMContext):
    await state.set_state(Zakaz.deleted_id)
    await message.answer("🗑 Код ID-и заказро нависед барои бекор кардан:")

@dp.message(Zakaz.deleted_id)
async def delete_order_confirm(message: Message, state: FSMContext):
    deleted = delete_zakaz(message.text)
    if deleted:
        await message.answer("✅ Закази шумо бекор шуд.")
    
    await state.clear()

@dp.message(F.text == "ℹ️ Оиди карго")
async def about_info(message: Message):
    await message.answer(
        "🚚 Somon Cargo — каргои бехатар ва зуд!\n"
        "⏱ Мӯҳлати расондан: 15-25 рӯз\n"
        "💰 Нарх: 2$–3$, дар Душанбе — ройгон!\n"
        "📦 Мо кафолат медиҳем, ки бори шумо саривақт мерасад."
    )

@dp.message(F.text == "🏢 Филиалхои мо")
async def show_branches(message: Message):
    await message.answer(
        "🏢 Филиалҳои мо дар Тоҷикистон:\n\n"
        "1️⃣ Ширин (назди фабрика)\n"
        "2️⃣ Саховат (пушти бозор)\n"
        "3️⃣ 9 км (назди Шарк Транс)"
    )

async def main():
    init_models()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
