from aiogram import types, F, Router, flags
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from parser import parse
from states import Parse



import keyboards
import text
router  = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(text.greet.format(name = message.from_user.full_name), reply_markup=keyboards.menu)

@router.message(F.text == 'Меню')
@router.message(F.text == 'Выйти в меню')
async def mennu(message: Message):
    await message.answer(text.menu, reply_markup=keyboards.menu)

@router.callback_query(F.data == 'parse_data')
async def input_ssn_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Parse.ssn_prompt)
    await callback.message.edit_text(text.ssn_text)
    await callback.message.answer(text.parse_exit, reply_markup=keyboards.exit_kb)

@router.message(Parse.ssn_prompt)
@flags.chat_action('typing')
async def parse_ssn(message: Message, state: FSMContext):
    ssn = message.text
    mesg = await message.answer('Please wait...')
    res = parse(ssn)
    if not res:
        return await mesg.edit_text('Error', reply_markup=keyboards.exit_kb)
    text_result = ''
    for item in res:
        text_result += (f'{item['program_name']}\n'
                        f'Место в рейтинге: {item['start_position']}-{item['end_position']}\n'
                        f'Бюджетные места: {item['free_places']}\nКоммерческие места: {item['commercial_places']}\n'
                        f'Всего мест: {item['commercial_places']+item['free_places']}\n'
                        f'Ваша заявка: {item['student_program_types']}\n'
                        f'Ваш балл: {item['student_points']}\n\n')
    await mesg.edit_text(text_result)
