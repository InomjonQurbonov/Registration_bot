from aiogram.fsm.state import StatesGroup,State

class RegisterStates(StatesGroup):
    regName = State()
    regEmail = State()
    #regSpec = State()
    #regWork = State()
    regPhone = State()
    regBithyear = State()