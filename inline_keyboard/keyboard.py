from aiogram import types

# Основная клавиатура
inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
inline_keyboard.add(types.InlineKeyboardButton(text='Меню', callback_data='menu'), 
                    types.InlineKeyboardButton(text='Создать бота', callback_data='create_bot'), 
                    types.InlineKeyboardButton(text='Информация', callback_data='info'))

# Клавиатура наззад
back_keyboard = types.InlineKeyboardMarkup() 
back_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

# Клавиатура назад в меню
back_menu_keyboard = types.InlineKeyboardMarkup()
back_menu_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='menu_back'))

# Клавиатура с ссылкой
url_keyboard3 = types.InlineKeyboardMarkup(row_width=2)
url_keyboard3.add(types.InlineKeyboardButton(text="как узанть chat_id", url="https://lumpics.ru/how-find-out-chat-id-in-telegram/"), 
                  types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))

#Клавиатура выбора
choice_keyboard = types.InlineKeyboardMarkup() 
choice_keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes'),
                    types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))

#Клавиатура выбора
choice_keyboard1 = types.InlineKeyboardMarkup() 
choice_keyboard1.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))

# Клавиатура отмены
cancel_keyboard = types.InlineKeyboardMarkup()
cancel_keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))

#Клавиатура меню
menu_keyboard = types.InlineKeyboardMarkup(row_width=2) 
menu_keyboard.add(types.InlineKeyboardButton(text='Мои боты', callback_data='my_bot'),
                  types.InlineKeyboardButton(text='Продлить\nподписку всех ботов', callback_data='extend_all_bot'),
                  types.InlineKeyboardButton(text='Назад', callback_data='back'))
