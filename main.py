import asyncio
import logging

from aiogram import Bot, Dispatcher, types, executor

import os

logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)
USER_NAME = ''
LEVELS = {
    'Beginner': range(0, 9),
    'Elementary': range(9, 15),
    'Pre-intermediate': range(15, 23),
    'Intermediate': range(23, 31),
    'Upper-intermediate': range(31, 36),
    'Advanced': range(36, 40)
}
TEST = {
    'Выберите наиболее подходящий ответ! “What does your husband do?“': ['He is feeding the dog.',
                                                                        'He is a doctor.',
                                                                        'Yes, he does.',
                                                                        'Yes, he is.'],
    'Что такое альтернативный вопрос в английском языке?': [
        'Вопрос, требующий ответа «Да» или «Нет».',
        'Специальный вопрос к любому члену предложения.',
        'Вопрос, предполагающий выбор между двумя качествами, предметами или действиями.',
        'Вопрос, являющийся уточнением какого-либо утверждения.'],
    'Yesterday I ................. a bird': ['saw', 'sawed', 'see', 'seed'],
    'Найдите неправильный глагол: to play, to smile, to laugh, to see': ['to play', 'to smile',
                                                                         'to laugh', 'to see'],
    'При помощи какого суффикса может образовываться наречие в английском языке? От какой части речи?': [
        'При помощи суффикса «-ly» от глаголов.', 'При помощи суффикса «-ly» от прилагательных.',
        'При помощи суффикса «-ed» от существительных.',
        'При помощи суффикса «-ing» от прилагательных.'],
    'Укажите существительное, имеющее неправильную форму множественного числа.': ['lady',
                                                                                 'gentleman', 'son',
                                                                                 'daughter'],
    'Найдите ошибку в трёх формах глагола.': ['teach – taught – taught', 'catch – caught – caught',
                                             'bring – braught – braught', 'seek – sought – sought'],
    'Выберите наиболее подходящий ответ! “What is she doing?“': ['She is playing with the bunny.',
                                                                'She is a manager.',
                                                                'She cleans the house every day.',
                                                                'She is clean the carpet.'],
    'Как совершается действие, выраженное глаголом в Present Continuous?': [
        'Действие, выраженное глаголом в Present Continuous, во всех случаях совершается постоянно или регулярно в настоящем времени.',
        'Действие совершается всегда в будущем времени.',
        'Действие совершается в данный момент, или момент речи в настоящем времени.',
        'Действие уже совершено, и в предложении подчеркивается результат такого действия.'],
    'Karina never minds ................. the movie again.': ['to watch', 'to be watched', 'watch',
                                                              'watching'],
    'I couldn’t help ................. .': ['for laughing', 'and laughed', 'laughing',
                                            'to laughed'],
    'Можно мне взять Ваш карандаш?': ['Can I take your pencil?', 'Must I take your pencil?',
                                      'Should I take your pencil?', 'May I take your pencil?'],
    'Марта никогда не слышала, как он говорит по-английски': [
        'Martha never heard him spoke English.', 'Martha never heard him to speak English.',
        'Martha has never heard him speak English.', 'Martha never heard how he speaks English.'],
    'Я знаю его четыре года.': ['I know him four years.', 'I have been knowing him for four years.',
                                'I know him for four years.', 'I have known him for four years.'],
    'В каком из представленных ниже слов звук, который передаётся буквой «a», отличается от остальных?': [
        'map', 'tape', 'age', 'make'],
    'I have ................. butter, please, buy some.': ['little', 'many', 'few', 'a few'],
    'The taxi ................. by 7 o’clock yesterday.': ['has arrived', 'had arrived', 'arrived',
                                                           'is arrived'],
    'Должно быть, он продал свою машину.': ['It must be that he has sold his car.',
                                            'He must sold his car.',
                                            'He should have solden his car.',
                                            'He must have sold his car.'],
    'Я хочу, чтобы погода была хорошая.': ['I want that the weather will be fine.',
                                           'I want the weather to be fine.',
                                           'I want the weather be fine.',
                                           'I want the weather being fine.'],
    'Какой же он умный мальчик!': ['What an intelligent boy is he!',
                                   'What the intelligent boy is he!',
                                   'What an intelligent boy he is!',
                                   'What the intelligent boy he is!'],
    'Find the incorrect sentence.': [
        'Though it was nine o’clock in the evening, there were not many people in the bar.',
        'Although it is nine o’clock in the evening, there are not many people in the restaurant.',
        'It was only nine o’clock in the morning, and there were too many people in the café.',
        'Through it was eight o’clock in the morning, there weren’t many people in the pub.'],
    'Какое из перечисленных ниже предложений нельзя перевести на русский язык как «Я читаю»?': [
        'I read magazines every day.', 'I am reading a book.',
        'I have been reading the magazine for two hours.', 'Все варианты подходят.'],
    'When Kate ................. at Pier 90, it was crowded with football fans.': ['achieved',
                                                                                   'arrived',
                                                                                   'entered',
                                                                                   'reached'],
    'There was no one to cheer him ................. .': ['on', 'in', 'up', 'over'],
    'Could you possibly give me ................. ?' : ['a advice', 'an advice', 'some advices',
                                                       'a piece of advice'],
    'Marvin asked me ................. .': ['what was my favourite vegetable',
                                            'what my favourite vegetable was',
                                            'what is my favourite vegetable',
                                            'what about my favourite vegetable'],
    'The accident happened ................. our way home.': ['in', 'on', 'for', 'about'],
    'If he were not so absent-minded, he ................. you for your sister (yesterday)': [
        'would not mistake', 'would not have mistaken', 'would not have been mistaken',
        'did not mistake'],
    'If Mike lived in the country house, he ................. happier.': ['was', 'is', 'will be',
                                                                          'would be'],
    '................. that weird man sitting over there?': ['Which', 'Whose', "Who's", 'Who'],
    'How long ................. his house?': ['has Mr Johnson had', 'does Mr Johnson have',
                                              'had Mr Johnson had', 'has Mr Johnson been having'],
    'Ron has made up his ................. to become a teacher.': ['brains', 'decision', 'head',
                                                                   'mind'],
    "If Deborah ................. to dinner tomorrow, I'll be happy.": ['will come', 'comes',
                                                                        'came', 'was coming'],
    'Ask somebody for ................. occupation.': ['his', 'her', 'their', 'its'],
    "Kids shouldn't take those pills, and ................. .": ['neither should she',
                                                                 'neither she should',
                                                                 'she did either',
                                                                 "either shouldn't she"],
    'The doctor ................. me that there would be no pain.': ['sured', 'insured',
                                                                     'reassured', 'ensured'],
    'I am looking for an ................. method of heating.': ['economics', 'economy', 'economic',
                                                                 'economical'],
    'We try to be ................. to the needs of the customer.': ['responsible', 'responsive',
                                                                     'respondent', 'response'],
    'An obstetrician/gynecologist at the pre-conception clinic suggests we ................. some further tests.': [
        'doing', 'to do', 'are doing', 'should do'],
    'This particular college has a very selective ................. policy.': ['acceptance',
                                                                               'entrance',
                                                                               'admissions',
                                                                               'admittance']}
QUESTIONS = [quest for quest in TEST.keys()]
LEVEL = ''
RIGHT_ANS = [2, 3, 1, 4, 2, 2, 3, 1, 3, 4, 3, 4, 3, 4, 1, 1, 2, 4, 2, 3, 4, 4, 2, 3, 4, 2, 2, 2, 4,
             3, 1, 4, 2, 3, 1, 3, 4, 2, 4, 3]
RA = 0


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    global LEVEL, QUESTIONS, TEST, LEVELS
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я бот, который поможет тебе выучить английский язык.")
    await message.answer(
        'Тебе нужно пройти тест, чтобы я понял какие задания тебе нужны. На каждый вопрос дается полминуты. Готов?')
    await asyncio.sleep(3)
    for quest, anss in TEST.items():
        keyboard = types.InlineKeyboardMarkup()
        for ans in anss:
            keyboard.add(types.InlineKeyboardButton(ans,
                                                    callback_data=f'ans_{QUESTIONS.index(quest)}_{anss.index(ans) + 1}'))
        msg = await message.answer(f'{quest}', reply_markup=keyboard)
        await asyncio.sleep(30)
        await msg.edit_text('Время вышло. Идем дальше.', reply_markup=None)
    print(RA)
    for level, range in LEVELS.items():
        if RA in range:
            LEVEL = level
            break
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
    await bot.send_message(callback_query.from_user.id, 'Хорошо, начнем с грамматики.', reply_markup=None)


@dp.callback_query_handler(lambda c: c.data == 'practice')
async def choose1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Хорошо, начнем с практики.', reply_markup=None)


@dp.callback_query_handler(text_contains='ans_')
async def test(call: types.CallbackQuery):
    global RA, RIGHT_ANS
    if call.data and call.data.startswith('ans_'):
        call = call['data']
        call = call.split('_')
        if RIGHT_ANS[int(call[1])] == int(call[2]):
            RA += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
