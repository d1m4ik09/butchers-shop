import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Переслать', callback_data="send")

    markup.add(btn1)

    bot.send_message(message.chat.id, "Какашки", reply_markup=markup)


@bot.message_handler(commands=['id'])
def id(message):
    bot.send_message(message.chat.id, message.chat.id)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "send":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Подтвердить заказ', callback_data="accept")
        btn2 = types.InlineKeyboardButton('Отменить заказ', callback_data="cancel")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message("-1002166064543", callback.message.message_id, reply_markup=markup)

    if callback.data == "accept":
        bot.send_message("-1002166064543", "ебенет")

bot.infinity_polling()