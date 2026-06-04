from aiogram.fsm.state import State, StatesGroup

# FSM состояния
class Register(StatesGroup):
    class_select = State()  # Выбор класса
    subject_select = State()  # Выбор предмета
    format_select = State()  # Выбор формата
    date_select = State()  # Выбор даты
    time_select = State()  # Выбор времени
    name = State()  # ФИО
    phone = State()  # Телефон
    telegram = State()  # Telegram