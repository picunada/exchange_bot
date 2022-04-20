from aiogram.dispatcher.filters.state import StatesGroup, State


class Exchange(StatesGroup):
    amount = State()  # Will be represented in storage as 'Exchange:amount'
    card_num = State()  # Will be represented in storage as 'Exchange:card'
