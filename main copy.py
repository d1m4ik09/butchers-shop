import telebot
from telebot import types
from dotenv import load_dotenv
import os
import random

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

orders = {}
del_orders = {}
stat = {
    "🍔Чизбургер|3H": 0,
    "🍔Классика|4H": 0,
    "🍔Двойной|5H": 0,
    "🍟Соль|1H": 0,
    "🍟Сметана и зелень|1H": 0,
    "🍗Тушенка|2H" : 0,
    "🥤Кола|1H": 0,
    "🥤Липтон|1H": 0,
    "🥤Яблочный сок|1H": 0
}
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


@bot.message_handler(commands=['start'])
def start(message):
    # user_form[message.chat.id] = {"skills": ""}
    orders[message.chat.id] = {"order": "", "price": 0}
    
    markup = types.ReplyKeyboardMarkup()
    
    store_make_order = types.KeyboardButton("🛒Касса")
    delivery_make_order = types.KeyboardButton("🚚Доставка")

    markup.row(store_make_order, delivery_make_order)
    bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(content_types=['text'])
def on_click(message):
    if message.text == "🛒Касса":
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
        
        bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Я сделал заказ'", reply_markup=markup)

    if message.text == "🚚Доставка":
        bot.send_message(message.chat.id, "Напишите номер телефона")
        bot.register_next_step_handler(delivery_fun, message)

    if message.text in menu:
        if message.chat.id == '':
            pass
            
        orders[message.chat.id]["order"] += f"{message.text} "
        orders[message.chat.id]["price"] += prices[message.text]
        print(orders)

    if message.text == "✅Я сделал заказ":
        print(orders)
        markup = types.ReplyKeyboardMarkup()
        send = types.KeyboardButton("✅Подтвердить заказ")
        cancel = types.KeyboardButton("❌Отменить заказ")
        markup.row(send, cancel)

        bot.send_message(message.chat.id, f'Ваш заказ: \n{orders[message.chat.id]["order"].split()}\n\nСумма заказа: {orders[message.chat.id]["price"]}H')
        
        bot.send_message(message.chat.id, "Проверьте ваш заказ и нажмите '✅Подтвердить заказ', если вы допустили ошибку, нажмите '❌Отменить заказ'", reply_markup=markup)
        


    if message.text == "❌Отменить заказ":
        orders[message.chat.id] = {}

        markup = types.ReplyKeyboardMarkup()

        make_an_order = types.KeyboardButton("🛒Сделать заказ")

        markup.row(make_an_order)
        print(orders)

    if message.text == '✅Подтвердить заказ':    
        markup = types.ReplyKeyboardMarkup()
        # rdy_btn = types.KeyboardButton("✅Готово")
        
        bot.send_message(message.chat.id, "Для отправки заказа на кухню, напишите своё имя.")
       
        bot.register_next_step_handler(message, get_name)

@bot.message_handler()
def get_name(message):
    global orders
    orders[message.chat.id]["name"] = message.text
    bot.send_message(message.chat.id, "Напишите номер стола, к которому мы отнесем ваш заказ.")
    bot.register_next_step_handler(message, get_table_number)
    
def delivery_fun(message):
    global del_orders 
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
    
    bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Я сделал заказ'", reply_markup=markup)
    
    del_orders[message.text] = {}
    bot

def get_table_number(message):
    global orders
    orders[message.chat.id]["table_number"] = message.text
    bot.send_message(message.chat.id, "Последний этап. Напишите свой номер телефона для связки с вами при получении заказа.")
    bot.register_next_step_handler(message, get_number)

def get_number(message):
    global orders
    orders[message.chat.id]["number"] = message.text
    bot.send_message(message.chat.id, "Ваш заказ отправлен на обработку. В ближайшее время отправим вам статус заказа.")


@bot.message_handler()
def send_order(message):
    count = 0

    for item in orders[message.chat.id]:
        count += prices[item]
    
    # пересылка в канал с inline


bot.infinity_polling()