from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text='📊 Узнать место в рейтинге ВШЭ', callback_data='parse_data')],
    [InlineKeyboardButton(text='👹 Посмотреть меме', callback_data='show_meme')]
    ]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_meme_kb = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='◀️ Выйти в меню')], [KeyboardButton(text='👹 Еще меме')]], resize_keyboard=True)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)

