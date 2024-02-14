from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import re
from config import DB_NAME
from keyboards.reg_keyboards import kb_request_contact
from states.reg_states import RegisterStates
from utils.database import Database

reg_router = Router()
db = Database(DB_NAME)

@reg_router.message(F.text == "Ro'yhatdan o'tish")
async def register_start(message: Message, state=FSMContext):
    users = db.get_users(message.from_user.id)
    if users[6] and users[7]:
        await message.reply(
            f"Hurmatli {users[5]}, siz deyarli ro'yxatdan o'tdingiz",
            reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(
            "Ro'yxatdan o'tish jarayonini boshlaymiz \n"
            "Iltimos to'liq ism famillyangizni kiriting",
            reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterStates.regName)

@reg_router.message(RegisterStates.regName)
async def register_name(message: Message, state=FSMContext):
    await state.update_data(reg_name=message.text)
    await message.answer(
        "Iltimos telefon raqamingizni yuboring",
        reply_markup=kb_request_contact
    )
    await state.set_state(RegisterStates.regPhone)
    
@reg_router.message(RegisterStates.regPhone)
async def register_phone(message: Message, state=FSMContext):
    try:
        await state.update_data(reg_phone=message.contact.phone_number)
        reg_data = await state.get_data()
        reg_name = reg_data.get('reg_name')
        reg_phone = reg_data.get('reg_phone')
        await message.answer(
            f"Hurmatli {reg_name} siz deyarli ro'yxatdan o'tdingiz",
            reply_markup=ReplyKeyboardRemove())
        db.update_user(message.from_user.id, reg_name, reg_phone)
        await message.answer(
            "Iltimos email manzilingizni yuboring"
            )
        await state.set_state(RegisterStates.regEmail)
    except Exception as e:
        print(e)
        await message.answer(
            f"Iltimos telefon raqamingizni yuboring",
            reply_markup=kb_request_contact
        )
        
@reg_router.message(RegisterStates.regBithyear)
async def register_year_of_birth(message: Message, state=FSMContext):
    try:
        year_of_birth = int(message.text)
        await state.update_data(reg_year_of_birth=year_of_birth)
        reg_data = await state.get_data()
        reg_year_of_birth = reg_data.get('reg_year_of_birth')
        await message.answer(
            f"Sizning tug'ilgan yilingiz muvaffaqiyatli saqlandi: {reg_year_of_birth}",
            reply_markup=ReplyKeyboardRemove()
        )
        db.update_user_birt_year(message.from_user.id, reg_year_of_birth)
        await state.clear()
    except ValueError:
        await message.answer("Noto'g'ri yil formati. Iltimos, to'g'ri yilni yuboring.")
        

def is_valid_email(email):
    """
    Validate if the provided string is a valid email address.
    """
    email_regex = r'^\S+@\S+\.\S+$'
    return re.match(email_regex, email) is not None

@reg_router.message(RegisterStates.regEmail)
async def register_email(message: Message, state=FSMContext):
    try:
        user_input = message.text.strip()

        if is_valid_email(user_input):
            await state.update_data(reg_email=user_input)
            reg_data = await state.get_data()
            reg_email = reg_data.get('reg_email')
            await message.answer(
                f"Sizning email manzilingiz muvaffaqiyatli saqlandi: {reg_email}",
                reply_markup=ReplyKeyboardRemove())
            db.update_user_email(message.from_user.id, reg_email)
            await message.answer("Iltimos, tug'ilgan yilingizni yuboring")
            await state.set_state(RegisterStates.regBithyear)
        else:
            await message.answer("Noto'g'ri email formati. Iltimos, to'g'ri email manzilni yuboring.")
    except Exception as e:
        print(e)
        await message.answer("Noto'g'ri email formati. Iltimos, to'g'ri email manzilni yuboring.")