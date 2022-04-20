from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


exchange_button = KeyboardButton("Exchange")
cancel = KeyboardButton("Cancel")
menu = ReplyKeyboardMarkup().add(exchange_button)
active_menu = ReplyKeyboardMarkup().add(cancel)

