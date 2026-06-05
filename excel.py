import openpyxl
import os
from datetime import datetime, timedelta, timezone

FILE = "students.xlsx"


def get_book():
    if not os.path.exists(FILE):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append([
            "ФИО", "Телефон", "Telegram",
            "Класс", "Предмет", "Дата",
            "Время", "Формат"
        ])
        wb.save(FILE)
    return openpyxl.load_workbook(FILE)


def add_student(data):
    wb = get_book()
    sheet = wb.active
    
    # [ДОБАВЛЕНО] Проверка на дубликат: если такая запись уже есть, не добавляем её снова
    # data[2] — это Telegram-юзернейм, data[5] — дата, data[6] — время
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[2] == data[2] and row[5] == data[5] and row[6] == data[6]:
            return False  # Сигнализируем боту, что запись уже существует
            
    sheet.append(data)
    wb.save(FILE)
    return True


def get_all():
    wb = get_book()
    sheet = wb.active
    return list(sheet.iter_rows(min_row=2, values_only=True))


def clear():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append([
        "ФИО", "Телефон", "Telegram",
        "Класс", "Предмет", "Дата",
        "Время", "Формат"
    ])
    wb.save(FILE)


def get_today():
    # [ИСПРАВЛЕНО] Явно задаем часовой пояс (например, МСК — UTC+3), 
    # чтобы код внутри Docker-контейнера не выдавал британское время
    tz_moscow = timezone(timedelta(hours=3))
    today = datetime.now(tz_moscow).strftime("%d.%m")

    rows = get_all()
    # Фильтруем строки, у которых Дата (индекс 5) совпадает с сегодняшней, 
    # и сортируем их по Времени (индекс 6), чтобы расписание шло по порядку
    today_lessons = [r for r in rows if r[5] == today]
    return sorted(today_lessons, key=lambda x: x[6] if x[6] else "")
