import calendar
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_calendar():

    now = datetime.now()

    year = now.year
    month = now.month

    markup = InlineKeyboardMarkup(inline_keyboard=[])

    cal = calendar.monthcalendar(year, month)

    for week in cal:

        row = []

        for day in week:

            if day == 0:

                row.append(
                    InlineKeyboardButton(text=" ", callback_data="ignore")
                )

            else:

                row.append(
                    InlineKeyboardButton(
                        text=str(day),
                        callback_data=f"date_{day}.{month}"
                    )
                )

        markup.inline_keyboard.append(row)

    return markup