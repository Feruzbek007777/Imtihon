from telebot import TeleBot
from database import Database

TOKEN = "8206840872:AAE_BHHXZCXIfA4-LWu-yJpqhyCp0D61RHw"

bot = TeleBot(TOKEN)
db = Database("main.db")
