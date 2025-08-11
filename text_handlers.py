from loader import bot, db
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from admin_buttons import admin_menu

ADMIN_ID = 7657284302

@bot.message_handler(commands=["start"])
def start(message: Message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"Salom admin {message.from_user.full_name}!", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, f"Assalomu aleykum {message.from_user.full_name}, botimizga xush kelibsiz!")
        show_books_buttons(message.chat.id)

def show_books_buttons(chat_id):
    books = db.select_books()
    if not books:
        bot.send_message(chat_id, "Hozircha kitoblar yo‘q.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(KeyboardButton(book[1]))

    bot.send_message(chat_id, "Mavjud kitoblar:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.from_user.id != ADMIN_ID)
def user_select_book(message: Message):
    books = db.select_books()
    selected = next((b for b in books if b[1] == message.text), None)

    if not selected:
        bot.send_message(message.chat.id, "Bunday kitob topilmadi.")
        return

    infos = db.select_books_info(selected[0])
    if not infos:
        bot.send_message(message.chat.id, "Bu kitob haqida ma'lumot yo‘q.")
    else:
        for info in infos:
            bot.send_message(message.chat.id, info[1])


# Ustoz tan olaman admin panelda updatega qiynaldim va suniy intelekt yordam berdi  qolgan hammasi ozimni kodim ustoz 100 talik
# Batafsil telegramdan ovozli xabar qilganman ustoz