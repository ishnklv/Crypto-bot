import config
import logging

from http_module import fetch_crypto

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

# Buttons
page = 0


def render(limit, skip):
    return fetch_crypto(limit=limit, skip=skip)


@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    crypto_btn = types.InlineKeyboardButton(text='cryptos', callback_data='cryptos')
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(crypto_btn)
    await msg.answer('Welcome to crypto stats', reply_markup=kb)


@dp.message_handler(commands=['cryptos'])
async def get_crypto(msg: types.Message):
    cryptos = render(limit=10, skip=0)
    pg_kb = types.InlineKeyboardMarkup(row_width=2)
    for crypto in cryptos:
        btn = types.InlineKeyboardButton(
            f"rank: {crypto['r']}, name: {crypto['n']}, p24: {crypto['p24']}%",
            url=f"https://coinstats.app/coins/{crypto['i']}/",
        )
        pg_kb.add(btn)

    prev_btn = types.InlineKeyboardButton('⬅️', callback_data='prev')
    next_btn = types.InlineKeyboardButton('➡️', callback_data='next')
    pg_kb.add(prev_btn, next_btn)
    await msg.answer('All Cryptos',
                     reply_markup=pg_kb)


@dp.callback_query_handler(lambda c: c.data == 'next')
async def next_pagination(callback: types.CallbackQuery):
    global page
    page += 1
    skip = page * 10
    cryptos = render(limit=10, skip=skip)
    pg_kb = types.InlineKeyboardMarkup(row_width=2)
    for crypto in cryptos:
        btn = types.InlineKeyboardButton(
            f"rank: {crypto['r']}, name: {crypto['n']}, p24: {crypto['p24']}%",
            url=f"https://coinstats.app/coins/{crypto['i']}/")
        pg_kb.add(btn)

    prev_btn = types.InlineKeyboardButton('⬅️', callback_data='prev')
    next_btn = types.InlineKeyboardButton('➡️', callback_data='next')
    pg_kb.add(prev_btn, next_btn)
    try:
        await bot.edit_message_text(
            'All cryptos',
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=pg_kb
        )
    except BaseException:
        print('error')


@dp.callback_query_handler(lambda c: c.data == 'prev')
async def prev_pagination(callback: types.CallbackQuery):
    global page
    page -= 1
    if page < 0:
        return await callback.answer('limit exceeded')
    skip = page * 10
    cryptos = render(limit=10, skip=skip)
    pg_kb = types.InlineKeyboardMarkup(row_width=5)
    for crypto in cryptos:
        btn = types.InlineKeyboardButton(
            f"rank: {crypto['r']}, name: {crypto['n']}, p24: {crypto['p24']}%",
            url=f"https://coinstats.app/coins/{crypto['i']}/"
        )
        pg_kb.add(btn)

    prev_btn = types.InlineKeyboardButton('⬅️', callback_data='prev')
    next_btn = types.InlineKeyboardButton('➡️', callback_data='next')
    pg_kb.add(prev_btn, next_btn)
    try:
        await bot.edit_message_text(
            'All cryptos',
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=pg_kb
        )
    except BaseException:
        print('error')


async def set_bot_commands(_):
    bot_commands = [
        types.BotCommand(command='/start', description='for using service'),
        types.BotCommand(command='/cryptos', description='get all crypto')
    ]

    await bot.set_my_commands(bot_commands)

# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_bot_commands)
