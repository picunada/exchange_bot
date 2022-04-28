from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State


class Exchange(StatesGroup):
    amount = State()  # Will be represented in storage as 'Exchange:amount'
    card_num = State()  # Will be represented in storage as 'Exchange:card'
    check = State()  # Will be represented in storage as 'Exchange:check'
    admin_link = State()
    admin_check = State()
    payment_process = State()
    transaction_end = State()
