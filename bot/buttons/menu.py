from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

exchange_button = KeyboardButton("/exchange")
get_status_button = KeyboardButton("/get_order_status")
cancel = KeyboardButton("/cancel")
menu = ReplyKeyboardMarkup().add(exchange_button)
active_menu = ReplyKeyboardMarkup().add(cancel)
