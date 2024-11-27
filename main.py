import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

menu = ['qwe -3h', 'rty - 4h']
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()

    cheese = types.KeyboardButton("🍔Чизбургер")
    classic = types.KeyboardButton("🍔Классика")
    double = types.KeyboardButton("🍔Двойной")


    snack1 = types.KeyboardButton("🍟Соль")
    snack2 = types.KeyboardButton("🍟Сметана и зелень")

    drink1 = types.KeyboardButton("🥤Кола")
    drink2 = types.KeyboardButton("🥤Липтон")
    drink3 = types.KeyboardButton("🥤Яблочный сок")

    ready_order = types.KeyboardButton("Готово")

    
    markup.row(cheese, classic, double)
    markup.row(snack1, snack2)
    markup.row(drink1, drink2, drink3)
    markup.row(ready_order)
    markup.row()













bot.infinity_polling()