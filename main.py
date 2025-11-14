TOKEN = 'f9LHodD0cOJsUziEEEDzAS6kQLSFSxaE5ejYyGI7Z2SrIRrBNjT4C5759g0r7Eqdl2bBbFZzCfeVankzda2F'
VUZ_name = 'МГУ'


import asyncio
import logging

from maxapi import Bot, Dispatcher, F
from maxapi.types import *
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

import db

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN)
dp = Dispatcher()  

user = None
weeks = [3,4,5]
cur_week = 3


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Привет! Отправь мне /start'
    )


@dp.message_created(Command('stud'))
async def chg_srud(event: MessageCreated):
    global user
    user = {'digital_id':'12345',
        'first_name':event.message.sender.first_name,
        'last_name':event.message.sender.last_name,
        'category':'студент',
        'dormitory':None}
    await event.message.answer(f"Теперь вы студент. Напишите /start")

@dp.message_created(Command('prep'))
async def chg_prep(event: MessageCreated):
    global user
    user = {'digital_id':'12345',
        'first_name':event.message.sender.first_name,
        'last_name':event.message.sender.last_name,
        'category':'преподаватель',
        'dormitory':None}

    await event.message.answer(f"Теперь вы преподаватель. Напишите /start")

@dp.message_created(Command('abit'))
async def chg_none(event: MessageCreated):
    global user
    user = None
    await event.message.answer(f"Теперь вы абитуриент. Напишите /start")




@dp.message_created(Command('start'))
async def main_func(event: MessageCreated):

    #тут проверка

    global user

    if user:

        if user['category'] == 'студент':
            builder = InlineKeyboardBuilder()

            builder.row(CallbackButton(text="Распиание 🗒",payload='student_schedule'))
            builder.row(CallbackButton(text="Деканат",payload='student_decanat'))
            if user['dormitory']: builder.row(CallbackButton(text="Общежитие",payload='student_dormitory'))
            builder.row(CallbackButton(text="Оценки",payload='student_otsenki'))

            await event.message.answer(f"Привет, {user['first_name']}", attachments=[builder.as_markup()])


        elif user['category'] == 'преподаватель':
            builder = InlineKeyboardBuilder()

            builder.row(CallbackButton(text="Расписание 🗒",payload='teacher_schedule'))
            builder.row(CallbackButton(text="Кафедра",payload='teacher_kaf'))
            builder.row(CallbackButton(text="Деканат",payload='teacher_decanat'))

            await event.message.answer(f"Здравствуйте, {user['first_name']}", attachments=[builder.as_markup()])


    else:

        builder = InlineKeyboardBuilder()
        builder.row(LinkButton(text="Сайт университета", url="https://example.com"))
        builder.row(CallbackButton(text="Направления подготовки",payload='abiturient_directions'))
        builder.row(CallbackButton(text="Правила поступления",payload='abiturient_rules'))

        await event.message.answer(f"Вас приветсвует {VUZ_name}. \n\nСейчас вы абитуриент, чтобы сменть свою роль напишите /stud или /prep", attachments=[builder.as_markup()])
    
    


@dp.message_callback()
async def message_callback(callback: MessageCallback):
    
    data = callback.callback.payload
    user_id = callback.from_user.user_id

    # region СТУДЕНТЫ

    if data == 'student_schedule':
        builder = InlineKeyboardBuilder()

        for week in weeks:
            builder.row(CallbackButton(text=f"Неделя {week} {'🛎' if week == cur_week else ''}",payload=f'student_schedule_{week}'))

        await callback.message.answer('выберите неделю', attachments=[builder.as_markup()])

    elif data.startswith('student_schedule_'):
        
        week = data.split('_')[-1]

        pnd, vtr, srd, cht, ptn = db.get_student_schedule(week, '12345')
        
        msg=''

        msg+='\nПонедельник\n'
        for p in pnd:
            msg += f"{p['num']} {p['discipline']} {p['teacher']['last_name']} каб.{p['room']}\n"
        
        msg+='\nВтроник\n'
        for p in vtr:
            msg += f"{p['num']} {p['discipline']} {p['teacher']['last_name']} каб.{p['room']}\n"

        msg+='\nСреда\n'
        for p in srd:
            msg += f"{p['num']} {p['discipline']} {p['teacher']['last_name']} каб.{p['room']}\n"

        msg+='\nЧетверг\n'
        for p in cht:
            msg += f"{p['num']} {p['discipline']} {p['teacher']['last_name']} каб.{p['room']}\n"

        msg+='\nПятинца\n'
        for p in ptn:
            msg += f"{p['num']} {p['discipline']} {p['teacher']['last_name']} каб.{p['room']}\n"

        await callback.message.delete()
        await callback.message.answer(msg)



    elif data =='student_decanat':
        builder = InlineKeyboardBuilder()

        builder.row(CallbackButton(text="Заказать справку с места учёбы",payload='student_decanat_'))
        builder.row(CallbackButton(text="Запросить академ-отпуск",payload='student_decanat_'))
        builder.row(CallbackButton(text="Подать заявление на отчисление",payload='student_decanat_'))

        await callback.message.answer('Выберите', attachments=[builder.as_markup()])

    elif data.startswith('student_decanat_'):
        
        zapros = data.split('_')[-1]

        

        await callback.message.delete()
        await callback.message.answer('Ваш запрос отправлен!')


    elif data =='student_otsenki':

        discs = [{'id':1, 'name':'Математика'}]

        builder = InlineKeyboardBuilder()

        for disc in discs:
            builder.row(CallbackButton(text=f"{disc['name']}",payload=f'student_otsenki_{disc['id']}'))

        await callback.message.answer('выберите дисциплину', attachments=[builder.as_markup()])

    elif data.startswith('student_otsenki_'):
        
        disc_id = data.split('_')[-1]

        ots = db.get_otsenki('12345', disc_id)

        msg = 'Оценки\n'

        for o in ots:
            msg+=f"{o['para']['date']} {o['para']['discipline']} - {o['otsenka']}\n"

        await callback.message.delete()
        await callback.message.answer(msg)

    #endregion

    #region ПРЕПОДАВАТЕЛИ

    elif data == 'teacher_schedule':
        builder = InlineKeyboardBuilder()

        for week in weeks:
            builder.row(CallbackButton(text=f"Неделя {week} {'🛎' if week == cur_week else ''}",payload=f'teacher_schedule_{week}'))

        await callback.message.answer('Выберите неделю', attachments=[builder.as_markup()])

    elif data.startswith('teacher_schedule_'):
        
        week = data.split('_')[-1]

        pnd, vtr, srd, cht, ptn = db.get_teacher_schedule(week, '12345')
        
        msg=''

        msg+='\nПонедельник\n'
        for p in pnd:
            msg += f"{p['num']} {p['discipline']} {p['group']} каб. {p['room']}\n"
        
        msg+='\nВтроник\n'
        for p in vtr:
            msg += f"{p['num']} {p['discipline']} {p['group']} каб. {p['room']}\n"

        msg+='\nСреда\n'
        for p in srd:
            msg += f"{p['num']} {p['discipline']} {p['group']} каб. {p['room']}\n"

        msg+='\nЧетверг\n'
        for p in cht:
            msg += f"{p['num']} {p['discipline']} {p['group']} каб. {p['room']}\n"

        msg+='\nПятинца\n'
        for p in ptn:
            msg += f"{p['num']} {p['discipline']} {p['group']} каб. {p['room']}\n"

        await callback.message.delete()
        await callback.message.answer(msg)




    elif data =='teacher_decanat':
        builder = InlineKeyboardBuilder()

        builder.row(CallbackButton(text="Запросс",payload='teacher_decanat_'))

        await callback.message.answer('Выберите', attachments=[builder.as_markup()])

    elif data.startswith('teacher_decanat_'):
        
        zapros = data.split('_')[-1]

        

        await callback.message.delete()
        await callback.message.answer('Ваш запрос отправлен!')




    elif data == 'teacher_kaf':
        builder = InlineKeyboardBuilder()

        builder.row(CallbackButton(text="Получить справку с места работы",payload='teacher_kaf_'))
        builder.row(CallbackButton(text="Запросить отгул",payload='teacher_kaf_'))

        await callback.message.answer('Выберите', attachments=[builder.as_markup()])

    elif data.startswith('teacher_kaf_'):
        
        zapros = data.split('_')[-1]

        await callback.message.delete()
        await callback.message.answer('Ваш запрос отправлен!')

    #endregion


    elif data.startswith('abiturient_directions'):
        
        await callback.message.answer('*Отркрытие мини приложения с данной информацией*\nНаправление - проходной бал - стоимость обучения')

    elif data.startswith('abiturient_rules'):
        
        await callback.message.answer('*Отркрытие мини приложения с данной информацией*\nДля поступления ...')








async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())