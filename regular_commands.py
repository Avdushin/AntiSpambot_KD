from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from inline_keyboard import keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, dp, pay_token
import DataBase
from datetime import datetime, timedelta

class FSM(StatesGroup):
    get_chat_id = State()
    payment_data = State()

#Команда старт
async def start_cmd(message: types.Message):
    await bot.send_message(message.chat.id, "Я бот администратор сервиса!!Не будем томить давай ты нажмешь информация и я раскажу о себе не много ", reply_markup=keyboard.inline_keyboard)


#Команда отмены
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.answer()
    message = callback_query.message
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите действие: ",
        reply_markup=keyboard.inline_keyboard
    )

#Команда назад в меню
async def menu_back(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите действие: ", 
        reply_markup=keyboard.menu_keyboard)

# Команда назад
async def back(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Выберите действие: ", 
        reply_markup=keyboard.inline_keyboard)



#команда с информацией
async def info_cmd(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Ответ на callback query без отправки нового сообщения
    message = callback_query.message
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Информация об использовании:\n"
             "1. Бот является платным сервисом и его использование требует оплаты.\n"
             "2. Возможны технические работы, в результате которых бот может временно отключаться.\n"
             "3. Оплата взимается за каждый чат отдельно.\n"
             "4. Перемещение бота на другие чаты невозможно.\n"
             "5. При создании бота вы автоматически соглашаетесь с правилами.",
        reply_markup=keyboard.cancel_keyboard
    )
#Меню
async def menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id,
                                text='Выберите нужный пункт',
                                reply_markup=keyboard.menu_keyboard)

# Мои боты
async def my_bot(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    if DataBase.get_data(id=message.chat.id) != None:
        rez = DataBase.get_data(id=message.chat.id)
        # Создаем клавиатуру с ботами пользователя
        bot_keyboard = InlineKeyboardMarkup(row_width=2)
        for i in range(len(rez)):
            bot_num = rez[i][3]
            button = InlineKeyboardButton(text=f'Бот №{bot_num} ({rez[i][1]})', callback_data=f'bot_info_{bot_num}')
            bot_keyboard.add(button)

        back_button = InlineKeyboardButton(text='Назад', callback_data='menu_back')
        bot_keyboard.add(back_button)

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"Ваши боты:",
            reply_markup=bot_keyboard)
        
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"У вас пока нет ботов",
            reply_markup=keyboard.back_menu_keyboard
        )

    # Назад к ботам
    async def back_my_bot(callback_query: types.CallbackQuery):
        await callback_query.answer()
        message = callback_query.message
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Ваши боты: ", 
            reply_markup=bot_keyboard)
    dp.register_callback_query_handler(back_my_bot, lambda c: c.data == 'back_my_bot')

# Информация о боте
async def bot_info_(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    bot_num = int(callback_query.data.split('_')[2])  
    bot_data = DataBase.get_data(id=message.chat.id)  
    if bot_data:
        user_id, chat_id, subscription_start, bot_num = bot_data[int(bot_num)-1]
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f'''Информация о боте №{bot_num}:
                ID пользователя: {user_id}
                Chat ID: {chat_id}
                Дата подписки: {(datetime.strptime(subscription_start, r'%Y-%m-%d') - timedelta(days=30)).strftime(r'%Y-%m-%d')}
                Дата окончания подписки: {subscription_start}''',
                reply_markup=keyboard.back_keyboard)
        await bot.send_invoice(chat_id=callback_query.message.chat.id,
                           title="Подписка анти спам",
                           description=f"Продление подписки бота №{bot_num} ({chat_id})",
                           provider_token= pay_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[{
                               "label" : "Руб",
                               "amount": 30000
                               }],
                               start_parameter="donation_to_charity",
                               payload=f"{user_id},{chat_id}")
    else:
        await bot.send_message(message.chat.id, "Информация о боте не найдена.")

#Продлить подписку всех ботов
async def extend_all_bot(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = callback_query.message
    if DataBase.get_data(id=message.chat.id) != None:
        rez = DataBase.get_data(id=message.chat.id)
        await bot.send_invoice(chat_id=callback_query.message.chat.id,
                           title="Подписка анти спам",
                           description=f"Продление всех имеющихся ботов)",
                           provider_token= pay_token,
                           currency="rub",
                           is_flexible=False,
                           prices=[{
                               "label" : "Руб",
                               "amount": 30000 * len(rez)
                               }],
                               start_parameter="donation_to_charity",
                               payload=f"{message.chat.id}")
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"У вас пока нет ботов",
            reply_markup=keyboard.back_menu_keyboard)

#Создать бота
async def create_bot(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Ответ на callback query без отправки нового сообщения
    message = callback_query.message
    await FSM.get_chat_id.set()
    await bot.send_message(callback_query.from_user.id, 
                           "Отправте Chat ID где будет бот ", 
                           reply_markup=keyboard.url_keyboard3)

async def get_chat_id(message: types.Message, state: FSMContext):
    try:
        if isinstance(int(message.text), int):
            async with state.proxy() as data:
                data['get_chat_id'] = message.text
            await FSM.next()
            await bot.send_message(chat_id=message.chat.id, 
                                   text="Проверте правильно ли вы забисали chat_id если всё верно отпрате да ", 
                                   reply_markup=keyboard.choice_keyboard)
        else:
            await  bot.send_message(chat_id=message.chat.id, 
                                    text="Попробуйте ввести ещё раз но но верно", 
                                    reply_markup=keyboard.choice_keyboard1)
    except:
        await  bot.send_message(chat_id=message.chat.id, 
                                text="Попробуйте ввести ещё раз но но верно ", 
                                reply_markup=keyboard.choice_keyboard1)


async def payment_data(callback_query: types.CallbackQuery, state: FSMContext ):
    async with state.proxy() as data:
        if callback_query.data == "yes":
            data["payment_data"] = None
            now = datetime.now()
            now = now + timedelta(days=30)
            await bot.send_invoice(chat_id=callback_query.message.chat.id,
                                    title="Подписка анти спам",
                                    description=f"Оплата подписки пользователь {callback_query.message.chat.id}",
                                    provider_token= pay_token,
                                    currency="rub",
                                    is_flexible=False,
                                    prices=[{
                                        "label" : "Руб",
                                        "amount": 30000
                                    }],
                                    start_parameter="donation_to_charity",
                                    payload=f"{callback_query.message.chat.id, data['get_chat_id']}")
            await state.finish()
        else:
            await bot.send_message(callback_query.message.chat.id, "Отказ был принят")
            await state.finish()

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    pmnt = message.successful_payment.to_python()
    a = pmnt['invoice_payload']
    a = a.replace(")", "").replace("(", "").replace("'", "")
    a = a.split(',')
    print(len(a))
    print(pmnt['invoice_payload'])
    if len(a) == 2:
        DataBase.insert_data(data = [a[0], a[1], (datetime.now() + timedelta(days=30)).strftime(r'%Y-%m-%d')])
    elif len(a) == 3:
        DataBase.insert_update(data= [a[0], a[1], a[2],(datetime.now() + timedelta(days=30)).strftime(r'%Y-%m-%d')])
    elif len(a) == 1:
        DataBase.update_all(data=[a[0],(datetime.now() + timedelta(days=30)).strftime(r'%Y-%m-%d') ])
    await bot.send_message(chat_id=message.chat.id, text="оплата прошла успешно! добавте его в группу https://t.me/nospam_no_bot и назначте администратором")
    

    

def commands(dp: Dispatcher, ):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_callback_query_handler(cancel, lambda c: c.data == 'cancel', state='*')
    dp.register_callback_query_handler(menu_back, lambda c: c.data == 'menu_back')
    dp.register_callback_query_handler(back, lambda c: c.data == 'back')
    dp.register_callback_query_handler(info_cmd, lambda c: c.data == 'info')
    dp.register_callback_query_handler(create_bot, lambda c: c.data == 'create_bot', state=None)
    dp.register_callback_query_handler(menu, lambda c: c.data == "menu" )
    dp.register_callback_query_handler(my_bot, lambda c: c.data == "my_bot" )
    dp.register_message_handler(get_chat_id, state=FSM.get_chat_id )
    dp.register_callback_query_handler(bot_info_, lambda c: c.data.startswith('bot_info_'))
    dp.register_callback_query_handler(extend_all_bot, lambda c: c.data == 'extend_all_bot')
    dp.register_callback_query_handler(payment_data, lambda c: c.data == 'yes', state=FSM.payment_data)