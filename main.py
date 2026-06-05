import asyncio
import re
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
    await message.answer("Здравствуйте 👋\nВыберите класс:", reply_markup=classes_keyboard())
    await state.set_state(Register.class_select)

# СВЯЗЬ С ПРЕПОДАВАТЕЛЕМ
@dp.message(F.text == "Связь с преподавателем")
async def teacher(message: Message):
    await message.answer(f"Напишите преподавателю:\n{TEACHER}")

@dp.message(Register.class_select)
async def choose_class(message: Message, state: FSMContext):
    user_class = message.text.strip()
    await state.update_data(class_user=user_class)
    
    if user_class in ["5", "6", "7", "8"]:
        await message.answer("Выберите предмет:", reply_markup=subjects_middle())
    elif user_class == "9":
        await message.answer("Выберите предмет:", reply_markup=subject_9())
    elif user_class == "10":
        await message.answer("Выберите предмет:", reply_markup=subject_10())
    elif user_class == "11":
        await message.answer("Выберите предмет:", reply_markup=subject_11())
    await state.set_state(Register.subject_select)

@dp.message(Register.subject_select)
async def choose_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text.strip())
    await message.answer("Выберите формат занятия", reply_markup=format_keyboard())
    await state.set_state(Register.format_select)

@dp.message(Register.format_select)
async def choose_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text.strip())
    await message.answer("Выберите дату:", reply_markup=create_calendar())
    await state.set_state(Register.date_select)

@dp.callback_query(F.data.startswith("date_"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer() 
    await state.update_data(date=callback.data.split("_")[1])
    await callback.message.answer("Выберите время:", reply_markup=time_keyboard(TIMES))
    await state.set_state(Register.time_select)

@dp.callback_query(F.data.startswith("time_"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer() 
    await state.update_data(time=callback.data.split("_")[1])
    await callback.message.answer("Введите ФИО ученика (три слова):")
    await state.set_state(Register.name)

@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    fio = message.text.strip()
    fio_pattern = r"^[А-Яа-яёЁA-Za-z\-]+(\s+[А-Яа-яёЁA-Za-z\-]+){2}$"
    if not re.match(fio_pattern, fio):
        await message.answer("❌ Неверный формат ФИО. Введите Фамилию, Имя и Отчество (три слова):")
        return
    
    await state.update_data(name=fio)
    await message.answer(f"ФИО <b>{fio}</b> успешно сохранено!🤍", parse_mode="HTML")
    await message.answer("Введите номер телефона:")
    await state.set_state(Register.phone)

@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    clean_phone = re.sub(r"\D", "", message.text)
    if len(clean_phone) == 11 and clean_phone[0] in '78':
        clean_phone = '7' + clean_phone[1:]
    elif len(clean_phone) == 10:
        clean_phone = '7' + clean_phone
    else:
        await message.answer("❌ Некорректный формат телефона. Введите номер телефона в формате: 89001234567")
        return


    await state.update_data(phone=clean_phone)
    await message.answer(f"Номер {clean_phone} успешно сохранен!🤍")
    await message.answer("Введите Telegram (@username):")
    await state.set_state(Register.telegram)


@dp.message(Register.telegram)
async def finish(message: Message, state: FSMContext):
    tg_username = message.text.strip().lstrip("@")
    tg_pattern = r"^[A-Za-z][A-Za-z0-9_]{4,31}$"
    if not re.match(tg_pattern, tg_username):
        await message.answer("❌ Некорректный юзернейм. Попробуйте еще раз:")
        return
    await message.answer(f"Ваш юзернейм <b>@{tg_username}</b> сохранен!🤍", parse_mode="HTML")

    data = await state.get_data()
    format_lesson = data["format"]
    
    # ЛОГИКА ОПРЕДЕЛЕНИЯ ДАННЫХ
    if "Онлайн" in format_lesson:
        extra_info = f"💻 Ссылка на конференцию: {LINK_ONLINE}"
    else:
        extra_info = f"📍 Адрес занятия: {ADDRESS_OFFICE}"

    # Сохранение в Excel
    add_student([data["name"], data["phone"], f"@{tg_username}", data["class_user"], 
                 data["subject"], data["date"], data["time"], format_lesson])

    # Текст для админа
    admin_text = (f"Новая запись:\n👤 {data['name']}\n📅 {data['date']} в {data['time']}\n"
                  f"📍 {format_lesson}\n📞 {data['phone']}\n💬 @{tg_username}")
    await bot.send_message(GROUP_CHAT_ID, admin_text)

    # Текст для ученика
    user_text = (f"🤍Вы успешно записаны!🤍\n\n"
                 f"📅 Дата: {data['date']}\n"
                 f"⏰ Время: {data['time']}\n"
                 f"📍 Формат: {format_lesson}\n\n"
                 f"{extra_info}")
    await message.answer("Хорошего Вам дня!💐")
    await message.answer(user_text)
    await state.clear()

@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("Админ панель", reply_markup=admin_keyboard())

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
