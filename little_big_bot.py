from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os
import aiofiles

number = 100
count_of_attempts = 1

bot = Bot('...')
dp = Dispatcher(bot)

users = dict()


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    global count_of_attempts

    if str(message.from_user.id) not in users.keys():
        users[str(message.from_user.id)] = message.from_user.full_name

        async with aiofiles.open('users_data.txt', 'w+') as users_data:
            for ID, username in users.items():
                await users_data.write(f'ID: {ID} | Username: {username}')

    if count_of_attempts == 1:
        await message.answer(f'Привет, я загадал число, попробуй его угадать')
    else:
        await message.answer(f'Введите число: ')


@dp.message_handler()
async def info(message: types.Message):
    global number, count_of_attempts

    try:
        if int(message.text) == number:
            await message.answer(f'Вы угадали!\nКоличество попыток: {count_of_attempts}.')



        elif int(message.text) < number:
            await message.answer(f'Введенное число меньше загаданного.')
            count_of_attempts += 1
            await start_message(message)

        else:
            await message.answer(f'Введенное число больше загаданного.')
            count_of_attempts += 1
            await start_message(message)

    except ValueError:
        print(f'\n[ERROR] Данные должны иметь числовой тип.')
        await start_message(message)


if __name__ == '__main__':
    print('bot polling started')
    executor.start_polling(dp, skip_updates=True)



