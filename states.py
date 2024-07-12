from aiogram.fsm.state import StatesGroup, State

class Parse(StatesGroup):
    ssn_prompt = State()