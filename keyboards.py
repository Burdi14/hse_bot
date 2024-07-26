from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# menu = [
#     [InlineKeyboardButton(text='📊 Узнать место в рейтинге ВШЭ', callback_data='parse_data')],
#     [InlineKeyboardButton(text='👹 Посмотреть мем дня', callback_data='show_meme')]
#     ]


menu =  [[InlineKeyboardButton(text='📊 Узнать место в рейтинге ВШЭ', callback_data='parse_data')]]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️Выйти в меню", callback_data = 'back_to_menu')]])

