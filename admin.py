from loader import bot, db
from telebot.types import Message
from admin_buttons import admin_menu

ADMIN_ID = 7657284302

@bot.message_handler(commands=["admin"])
def admin_start(message: Message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Admin panelga xush kelibsiz!", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "Siz admin emassiz!")

@bot.message_handler(func=lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "➕ Kitob qo'shish")
def add_book(message: Message):
    bot.send_message(message.chat.id, "Kitob nomini kiriting:")
    bot.register_next_step_handler(message, save_book)

def save_book(message: Message):
    db.insert_books(message.text)
    bot.send_message(message.chat.id, "Kitob qo'shildi ✅")

@bot.message_handler(func=lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "📚 Kitoblar")
def list_books(message: Message):
    books = db.select_books()
    if books:
        text = "\n".join([f"{b[0]}. {b[1]}" for b in books])
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Hozircha kitoblar yo‘q.")

@bot.message_handler(func=lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "ℹ️ Kitobga ma'lumot qo'shish")
def add_info(message: Message):
    books = db.select_books()
    if not books:
        bot.send_message(message.chat.id, "Avval kitob qo‘shing.")
        return

    text = "Ma'lumot qo‘shmoqchi bo'lgan kitob raqamini kiriting:\n"
    text += "\n".join([f"{b[0]}. {b[1]}" for b in books])
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, get_book_id_for_info)

def get_book_id_for_info(message: Message):
    try:
        book_id = int(message.text)
        bot.send_message(message.chat.id, "Kitob haqida ma'lumot kiriting:")
        bot.register_next_step_handler(message, save_book_info, book_id)
    except:
        bot.send_message(message.chat.id, "Raqam kiriting!")

def save_book_info(message: Message, book_id):
    db.insert_book_info(book_id, message.text)
    bot.send_message(message.chat.id, "Kitob haqida ma'lumot qo‘shildi ✅")

# ✏️ Ma'lumotni yangilash
@bot.message_handler(func=lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "✏️ Ma'lumotni yangilash")
def update_info_start(message: Message):
    books = db.select_books()
    if not books:
        bot.send_message(message.chat.id, "Kitoblar yo‘q.")
        return
    text = "Qaysi kitob ma'lumotini yangilaysiz?\n"
    for b in books:
        infos = db.select_books_info(b[0])
        for info in infos:
            text += f"{info[0]}. {b[1]} — {info[1]}\n"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "Yangilash uchun ma'lumot ID sini kiriting:")
    bot.register_next_step_handler(message, get_info_id_for_update)

def get_info_id_for_update(message: Message):
    try:
        info_id = int(message.text)
        bot.send_message(message.chat.id, "Yangi ma'lumotni kiriting:")
        bot.register_next_step_handler(message, save_updated_info, info_id)
    except:
        bot.send_message(message.chat.id, "Raqam kiriting!")

def save_updated_info(message: Message, info_id):
    db.update_book_info(info_id, message.text)
    bot.send_message(message.chat.id, "Ma'lumot yangilandi ✅")

# 🗑 Ma'lumotni o‘chirish
@bot.message_handler(func=lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "🗑 Ma'lumotni o'chirish")
def delete_info_start(message: Message):
    books = db.select_books()
    if not books:
        bot.send_message(message.chat.id, "Kitoblar yo‘q.")
        return
    text = "Qaysi kitob ma'lumotini o'chirasiz?\n"
    for b in books:
        infos = db.select_books_info(b[0])
        for info in infos:
            text += f"{info[0]}. {b[1]} — {info[1]}\n"
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "O'chirish uchun ma'lumot ID sini kiriting:")
    bot.register_next_step_handler(message, delete_info_confirm)

def delete_info_confirm(message: Message):
    try:
        info_id = int(message.text)
        db.delete_book_info(info_id)
        bot.send_message(message.chat.id, "Ma'lumot o‘chirildi ✅")
    except:
        bot.send_message(message.chat.id, "Raqam kiriting!")
