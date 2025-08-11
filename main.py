from loader import bot, db
import text_handlers
import admin

if __name__ == "__main__":
    db.create_table_books()
    db.create_table_info()
    bot.infinity_polling()
