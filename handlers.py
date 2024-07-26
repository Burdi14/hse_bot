from aiogram import types, F, Router, flags
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import parser
from states import Parse
import os


import keyboards
import text
router  = Router()

ssn = ''
@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(text.greet.format(name = message.from_user.full_name), reply_markup=keyboards.menu)

@router.callback_query(F.data == 'parse_data')
async def input_ssn_prompt(callback: CallbackQuery, state: FSMContext):
    if callback.message.text == text.greet.format(name = callback.from_user.full_name):
        await callback.message.answer(text.ssn_text, reply_markup=keyboards.exit_kb)
    else:
        await callback.message.edit_text(text.ssn_text, reply_markup=keyboards.exit_kb)
    await state.set_state(Parse.ssn_prompt)

@router.callback_query(Parse.ssn_prompt)
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_menu':
        await callback.message.edit_text(text.menu, reply_markup=keyboards.menu)

    await state.clear()

@router.message(Parse.ssn_prompt)
@flags.chat_action('typing')
async def parse_ssn(message: Message, state: FSMContext):
    ssn = message.text
    mesg_wait = await message.answer('Please wait...')

    dict_res= []
    programs_links = parser.get_programs()
    list_size, cur = len(programs_links), 1
    for link in programs_links:
        parse_res = parser.parse_program(link, ssn)
        if parse_res:
            dict_res.append(parse_res)
        await mesg_wait.edit_text(f'Please wait...\n{cur/list_size*100:.2f}% scanned')
        cur+=1
    os.system('rm main_page.html cur.xlsx')
    if dict_res:
        text_result = ''
        for item in dict_res:
            text_result += (f'{item['program_name']}\n'
                            f'Место в рейтинге: {item['start_position']}-{item['end_position']}\n'
                            f'Место среди подавших оригинал аттестата: {item['start_position_docs']}-{item['end_position_docs']}\n'
                            f'Бюджетные места: {item['free_places']}\nКоммерческие места: {item['commercial_places']}\n'
                            f'Всего мест: {item['commercial_places'] + item['free_places']}\n'
                            f'Ваша заявка: {item['student_program_types']}\n'
                            f'Ваш балл: {item['student_points']}\n\n')
        await mesg_wait.edit_text(text_result, reply_markup=keyboards.menu)
    if not dict_res:
        await mesg_wait.edit_text('Error', reply_markup=keyboards.menu)

    state.clear()