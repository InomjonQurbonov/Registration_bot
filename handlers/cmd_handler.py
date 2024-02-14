from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, user
from aiogram.filters import CommandStart, Command

from keyboards.reg_keyboards import kb_register
from utils.database import Database
from config import DB_NAME

db = Database(DB_NAME)

cmd_router = Router()

@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    user = db.get_users(message.from_user.id)
    if not user:
        db.add_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                        message.from_user.last_name)
        await message.reply(text="Iltimos ro'yhatdan o'ting!", reply_markup=kb_register)
    elif not user[6]:
        await message.reply(text="Iltimos ro'yhatdan o'ting!", reply_markup=kb_register)
        if not user[7]:
            await message.reply(text="Iltimos ro'yhatdan o'ting!", reply_markup=kb_register)
    else:
        formatted_message = f"Hurmatli  @{user[4]}, qaytganingiz bilan"
        await message.reply(text=formatted_message, parse_mode=ParseMode.HTML)

@cmd_router.message(Command('help'))
async def cmd_code(message: Message):
    user = db.get_users(message.from_user.id)
    if user:
        s = f"Salom @{user[4]} men sizga yordam beraman"
        await message.reply(s)

@cmd_router.message(Command('code'))
async def cmd_code(message: Message):
    code_snippet = "```python\nprint('hello world')\n```"
    await message.answer(code_snippet, parse_mode=ParseMode.MARKDOWN_V2)
