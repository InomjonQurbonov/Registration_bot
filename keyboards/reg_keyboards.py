from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



kb_register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ro'yhatdan o'tish")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Iltimos <<Ro'yhatdan o'tish>> tugmasini bosing",
    one_time_keyboard=True
)

kb_request_contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=" 📞Telefon raqamni yuborish📞 ",
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Iltimos <<📞Telefon raqamni yuborish📞>> tugmasini bosing",
    one_time_keyboard=True
)
