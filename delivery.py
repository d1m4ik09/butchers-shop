import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

order_user = []
phone_user = ""
table_name_user = ""
table_num_user = ""
name_user = ""

del_orders = {}
prices = {
    "🍔Чизбургер|3H": 3,
    "🍔Классика|4H": 4,
    "🍔Двойной|5H": 5,
    "🍟Соль|1H": 1,
    "🍟Сметана и зелень|1H": 1,
    "🍗Тушенка|2H" : 2,
    "🥤Кола|1H": 1,
    "🥤Липтон|1H": 1,
    "🥤Яблочный сок|1H": 1
}
menu = ["🍔Чизбургер|3H", "🍔Классика|4H", "🍔Двойной|5H", "🍟Соль|1H", "🍟Сметана и зелень|1H", "🍗Тушенка|2H", "🥤Кола|1H", "🥤Липтон|1H", "🥤Яблочный сок|1H"]


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()

    delivery_make_order = types.KeyboardButton("🚚Доставка")

    markup.row(delivery_make_order)

    bot.send_message(message.chat.id, "нажми доставка чтобы начать", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=["clear"])
def clear(message):
    global order_user, phone_user, table_name_user, table_num_user, name_user

    order_user = []
    phone_user = ""
    table_name_user = ""
    table_num_user = ""
    name_user = ""

@bot.message_handler()
def on_click(message):
    if message.text == "🚚Доставка":
        markup = types.ReplyKeyboardMarkup()

        cheese = types.KeyboardButton(menu[0])
        classic = types.KeyboardButton(menu[1])
        double = types.KeyboardButton(menu[2])
        
        snack1 = types.KeyboardButton(menu[3])
        snack2 = types.KeyboardButton(menu[4])
        snack3 = types.KeyboardButton(menu[5])
        
        drink1 = types.KeyboardButton(menu[6])
        drink2 = types.KeyboardButton(menu[7])
        drink3 = types.KeyboardButton(menu[8])

        ready_order = types.KeyboardButton("✅Готово")

        markup.row(cheese, classic, double)
        markup.row(drink1, drink2, drink3)
        markup.row(snack1, snack2, snack3)
        markup.row(ready_order)

        bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Готово'", reply_markup=markup)
    
    if message.text in menu:
        global order_user
        order_user.append(f'{message.text} ')

    if message.text == "✅Готово":
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(message.chat.id, "Напишите номер телевона", reply_markup=markup)
        bot.register_next_step_handler(message, phone_num)



@bot.message_handler()
def phone_num(message):
    global phone_user
    phone_user = message.text
    bot.send_message(message.chat.id, "Напишите название стола")
    bot.register_next_step_handler(message, table_name)


def table_name(message):
    global table_name_user
    table_name_user = [message.text]
    bot.send_message(message.chat.id, "Напишите номер стола")
    bot.register_next_step_handler(message, table_num)

def table_num(message):
    global table_num_user
    table_num_user = message.text
    bot.send_message(message.chat.id, "Напишите ваше имя")
    bot.register_next_step_handler(message, name)

def name(message):
    global del_orders, order_user, phone_user, table_name_user, table_num_user, name_user

    del_orders[phone_user] = {"phone" : phone_user,
                              "table_name" : table_name_user,
                              "table_num" : table_name_user,
                              "order" : order_user}
    
    final = []
    for i in del_orders:
        final.append(i)


    bot.send_message("-1002166064543", final)

    order_user = []
    phone_user = ""
    table_name_user = ""
    table_num_user = ""
    name_user = ""
    



bot.infinity_polling()