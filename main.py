import logging

from aiogram import Bot, Dispatcher, types, executor
from secret import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
USER_NAME = ''
LEVEL = ''


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name} ! Я бот, который поможет тебе выучить английский язык.")
    await message.answer('Тебе нужно пройти тест, чтобы я понял какие задания тебе нужны.')
    await message.answer('Тест будет позже :)')
    await message.answer(f'Твой уровень - {LEVEL}.')
    keyboard = types.InlineKeyboardMarkup()
    gr = types.InlineKeyboardButton('Грамматика', callback_data='grammar')
    keyboard.add(gr)
    pr = types.InlineKeyboardButton('Практика', callback_data='practice')
    keyboard.add(pr)
    await message.answer('Теперь выбирай, с чего начнем:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'grammar')
async def choose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Хорошо, начнем с грамматики.')


@dp.callback_query_handler(lambda c: c.data == 'practice')
async def choose1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Хорошо, начнем с практики.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
