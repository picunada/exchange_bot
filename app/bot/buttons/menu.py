from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

exchange_button = KeyboardButton("Начать обмен 💰💰💰")
help_button = KeyboardButton("Инструкция ℹ️")
get_status_button = KeyboardButton("/get_order_status")
ready_button = KeyboardButton("Все верно, готов оплатить! ✅")
cancel = KeyboardButton("Что-то пошло не так, отменяем ❌")
paid = KeyboardButton("Пользователь оплатил✅")
transaction_end = KeyboardButton("Перевод завершен")
menu = ReplyKeyboardMarkup(resize_keyboard=True).add(exchange_button).add(help_button)
active_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)
check_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(ready_button).add(cancel)
paid_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(paid).add(cancel)
transaction_completed = ReplyKeyboardMarkup(resize_keyboard=True).add(transaction_end)
