import config
from aiogram import Bot, Dispatcher, types
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot
import re
from bot import BotDB
from get_data import Get_Data

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)  # в копейках (руб)

@dp.message_handler(commands='start')
async def start(message: types.message):
    start_buttons = ['📈 Сигналы','🚨 Инфо', 'Купить подписку']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*start_buttons)

    await message.answer('Привет, чего желаешь?', reply_markup = keyboard)


@dp.message_handler(Text(equals='📈 Сигналы'))
async def send_signals(message: types.message):
    if(BotDB.user_exists(message.from_user.id)):
        await message.answer(Get_Data.get_data())
        
    

                
@dp.message_handler(Text(equals='🚨 Инфо'))
async def send_info(message: types.message):
    await message.answer('pass')



# buy
@dp.message_handler(Text(equals='Купить подписку'))
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                        title="Подписка на бота",
                        description="Активация подписки на бота на 1 месяц",
                        provider_token=config.PAYMENTS_TOKEN,
                        currency="rub",
                        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload")
    
    
# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
        
    
# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await bot.send_message(message.chat.id,
                        f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")