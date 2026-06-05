from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def classes_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="5"), KeyboardButton(text="6")],
            [KeyboardButton(text="7"), KeyboardButton(text="8")],
            [KeyboardButton(text="9"), KeyboardButton(text="10")],
            [KeyboardButton(text="11")],
            [KeyboardButton(text="Связь с преподавателем")]
        ],
        resize_keyboard=True
    )


def subjects_middle():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Информатика")],
            [KeyboardButton(text="Математика")],
            [KeyboardButton(text="Связь с преподавателем")]
        ],
        resize_keyboard=True
    )


def subject_9():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ОГЭ информатика")],
            [KeyboardButton(text="ОГЭ математика")],
            [KeyboardButton(text="Подтянуть знания по математике")],
            [KeyboardButton(text="Подтянуть знания по информатике")],
            [KeyboardButton(text="Связь с преподавателем")]
        resize_keyboard=True
    )


def subject_10():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Математика ЕГЭ")],
            [KeyboardButton(text="Подтянуть знания по информатике")],
            [KeyboardButton(text="Подтянуть знания по математике")],
            [KeyboardButton(text="Связь с преподавателем")]
        ],
        resize_keyboard=True
    )


def subject_11():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ЕГЭ математика")],
            [KeyboardButton(text="Подтянуть знания по математике")],
            [KeyboardButton(text="Подтянуть знания по информатике")],
            [KeyboardButton(text="Связь с преподавателем")]
        ],
        resize_keyboard=True
    )


def format_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Онлайн")],
            [KeyboardButton(text="Очный")],
            [KeyboardButton(text="Связь с преподавателем")]
        ],
        resize_keyboard=True
    )


def time_keyboard(times):

    buttons = []

    for t in times:

        buttons.append(
            [InlineKeyboardButton(text=t, callback_data=f"time_{t}")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Все записи")],
            [KeyboardButton(text="📅 Сегодня")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="❌ Удалить запись")],
            [KeyboardButton(text="🗑 Очистить базу")]
        ],
        resize_keyboard=True
    )
