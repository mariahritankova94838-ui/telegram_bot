import openpyxl
import os
from datetime import datetime

FILE = "students.xlsx"


def get_book():

    if not os.path.exists(FILE):

        wb = openpyxl.Workbook()

        sheet = wb.active

        sheet.append([
            "ФИО","Телефон","Telegram",
            "Класс","Предмет","Дата",
            "Время","Формат"
        ])

        wb.save(FILE)

    return openpyxl.load_workbook(FILE)


def add_student(data):

    wb = get_book()
    sheet = wb.active

    sheet.append(data)

    wb.save(FILE)


def get_all():

    wb = get_book()
    sheet = wb.active

    return list(sheet.iter_rows(min_row=2, values_only=True))


def clear():

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append([
        "ФИО","Телефон","Telegram",
        "Класс","Предмет","Дата",
        "Время","Формат"
    ])

    wb.save(FILE)


def get_today():

    today = datetime.now().strftime("%d.%m")

    rows = get_all()

    return [r for r in rows if r[5] == today]