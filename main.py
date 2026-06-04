import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import *
from states import Register
from keyboards import *
from excel import *
from calendar_keyboard import create_calendar


bot = Bot(TOKEN)
dp = Dispatcher()


TIMES = [
"10-11","12-13","13-14","14-15",
"15-16","16-17","17-18","18-19"
]


# START
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Здравствуйте 👋\nВыберите класс:",
        reply_markup=classes_keyboard()
    )

    await state.set_state(Register.class_select)


# СВЯЗЬ С ПРЕПОДАВАТЕЛЕМ
@dp.message(F.text == "Связь с преподавателем")
async def teacher(message: Message):

    await message.answer(
        f"Напишите преподавателю:\n{TEACHER}"
    )

@dp.message(Register.class_select)
async def choose_class(message: Message, state: FSMContext):
    user_class = message.text


    await state.update_data(class_user=user_class)

    if user_class in ["5","6","7","8"]:
        await message.answer(
            "Выберите предмет",
            reply_markup=subjects_middle()
        )
    elif user_class == "9":
        await message.answer(
            "Выберите направление",
            reply_markup=subject_9()
        )
    elif user_class == "10":
        await message.answer(
            "Выберите предмет",
            reply_markup=subject_10()
        )
    elif user_class == "11":
        await message.answer(
            "Выберите направление",
            reply_markup=subject_11()
        )

    await state.set_state(Register.subject_select)

@dp.message(Register.subject_select)
async def choose_subject(message: Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)

    await message.answer(
        "Выберите формат занятия",
        reply_markup=format_keyboard()
    )

    await state.set_state(Register.format_select)


# ВЫБОР ФОРМАТА
@dp.message(Register.format_select)
async def choose_format(message: Message, state: FSMContext):

    await state.update_data(format=message.text)

    await message.answer(
        "Выберите дату:",
        reply_markup=create_calendar()
    )

    await state.set_state(Register.date_select)


# ВЫБОР ДАТЫ
@dp.callback_query(F.data.startswith("date_"))
async def choose_date(callback: CallbackQuery, state: FSMContext):

    date = callback.data.split("_")[1]

    await state.update_data(date=date)

    await callback.message.answer(
        "Выберите время:",
        reply_markup=time_keyboard(TIMES)
    )

    await state.set_state(Register.time_select)


# ВЫБОР ВРЕМЕНИ
@dp.callback_query(F.data.startswith("time_"))
async def choose_time(callback: CallbackQuery, state: FSMContext):

    time = callback.data.split("_")[1]

    await state.update_data(time=time)

    await callback.message.answer("Введите ФИО ученика:")

    await state.set_state(Register.name)


# ФИО
@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer("Введите номер телефона:")

    await state.set_state(Register.phone)


# ТЕЛЕФОН
@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):

    await state.update_data(phone=message.text)

    await message.answer("Введите Telegram (@username):")

    await state.set_state(Register.telegram)


# TELEGRAM
@dp.message(Register.telegram)
async def finish(message: Message, state: FSMContext):

    data = await state.get_data()

    name = data["name"]
    phone = data["phone"]
    tg = message.text
    user_class = data["class"]
    subject = data["subject"]
    date = data["date"]
    time = data["time"]
    format = data["format"]

    add_student([
        name,
        phone,
        tg,
        user_class,
        subject,
        date,
        time,
        format
    ])

    text = (
        f"Новая запись:\n\n"
        f"👤 {name}\n"
        f"📚 {subject}\n"
        f"🏫 {user_class} класс\n"
        f"📅 {date}\n"
        f"⏰ {time}\n"
        f"📍 {format}\n"
        f"📞 {phone}\n"
        f"💬 {tg}"
    )

    await bot.send_message(GROUP_CHAT_ID, text)

    await message.answer(
        "✅ Вы успешно записаны!"
    )

    await state.clear()


# ADMIN
@dp.message(Command("admin"))
async def admin(message: Message):

    if message.from_user.id not in ADMINS:
        return

    await message.answer(
        "Админ панель",
        reply_markup=admin_keyboard()
    )


# ЗАПУСК
async def main():

    print("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())