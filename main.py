import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


stat = {
    "🍔Чизбургер|3H": 0,
    "🍔Классика|4H": 0,
    "🍔Двойной|5H": 0,
    "🍟Соль|1H": 0,
    "🍟Сметана и зелень|1H": 0,
    "🍗Тушенка|2H" : 0,
    "🥤Кола|1H": 0,
    "🥤Липтон|1H": 0,
    "🥤Яблочный сок|1H": 0,
    "price" : 0
}

orders = {}
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
    orders[message.chat.id] = {"order": [], "price": 0, "delivery": ""} 
    
    markup = types.ReplyKeyboardMarkup()
    
    store_make_order = types.KeyboardButton("🛒Касса")
    delivery_make_order = types.KeyboardButton("🚚Доставка")

    markup.row(store_make_order, delivery_make_order)
    bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)

@bot.message_handler(commands=["stat"])
def statistics(message):
    print(stat)

@bot.message_handler(commands=["clearstatdata"])
def clear(message):
    global stat
    stat = {
        "🍔Чизбургер|3H": 0,
        "🍔Классика|4H": 0,
        "🍔Двойной|5H": 0,
        "🍟Соль|1H": 0,
        "🍟Сметана и зелень|1H": 0,
        "🍗Тушенка|2H" : 0,
        "🥤Кола|1H": 0,
        "🥤Липтон|1H": 0,
        "🥤Яблочный сок|1H": 0,
        "price" : 0
    }
    bot.send_message(message.chat.id, "Статистика очищена")


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
        
        orders[message.chat.id]["delivery"] = False
        
        bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Готово'", reply_markup=markup)

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
        
        orders[message.chat.id]["delivery"] = True

        bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Готово'", reply_markup=markup)    

    if message.text in menu:
        orders[message.chat.id]["order"].append(message.text)
        orders[message.chat.id]["price"] += prices[message.text]
        print(orders)

    if message.text == "✅Готово":
        bot.send_message(message.chat.id, 'Напишите имя')
        bot.register_next_step_handler(message, get_name)

    if message.text == "❌Отменить заказ":
        orders[message.chat.id] = {"order": [], "price": 0, "delivery": ""}

        markup = types.ReplyKeyboardMarkup()

        store_make_order = types.KeyboardButton("🛒Касса")
        delivery_make_order = types.KeyboardButton("🚚Доставка")

        markup.row(store_make_order, delivery_make_order)
        bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)

    if message.text == '✅Подтвердить заказ' :
        global stat

        markup = types.InlineKeyboardMarkup()

        btn1 = types.InlineKeyboardButton('Заказ готов', callback_data="ready")
        
        markup.add(btn1)

        for item in orders[message.chat.id]["order"]:
            stat[item] += 1

        stat["price"] += orders[message.chat.id]["price"]
        
        if orders[message.chat.id]["delivery"] == False:
            bot.send_message("-4729706765", f"Имя: {orders[message.chat.id]["name"]}\nВаш заказ:\n{orders[message.chat.id]["order"]}\n\nСумма заказа: {orders[message.chat.id]["price"]}H\n\nЗаказ на кассу", reply_markup=markup)

        else:
            bot.send_message("-4729706765", f'Имя: {orders[message.chat.id]["name"]}\nНомер стола: {orders[message.chat.id]["table_number"]}\nТелефон: {orders[message.chat.id]["phone"]}\nНазвание старт-апа: {orders[message.chat.id]["table_name"]}\n\nВаш заказ: \n{orders[message.chat.id]["order"]}\n\nСумма заказа: {orders[message.chat.id]["price"]}H + 1H(за доставку)\nИтого: {orders[message.chat.id]["price"] + 1}H\n\nЗаказ на доставку', reply_markup=markup)

        markup = types.ReplyKeyboardMarkup()

        orders[message.chat.id] = {"order": [], "price": 0, "delivery": ""}

        store_make_order = types.KeyboardButton("🛒Касса")
        delivery_make_order = types.KeyboardButton("🚚Доставка")

        markup.row(store_make_order, delivery_make_order)
        bot.send_message(message.chat.id, "Выбери способ заказа", reply_markup=markup)
        
       
@bot.message_handler()
def get_name(message):
    orders[message.chat.id]["name"] = message.text
    
    if orders[message.chat.id]["delivery"] == True:

        bot.send_message(message.chat.id, "Напишите номер стола")
        bot.register_next_step_handler(message, get_table_number)
        
    else:
        markup = types.ReplyKeyboardMarkup()

        send = types.KeyboardButton("✅Подтвердить заказ")
        cancel = types.KeyboardButton("❌Отменить заказ")
        
        markup.row(send, cancel)
        
        bot.send_message(message.chat.id, f'Имя: {orders[message.chat.id]["name"]}\n\nВаш заказ: \n{orders[message.chat.id]["order"]}\n\nСумма заказа: {orders[message.chat.id]["price"]}H\n\nЗаказ на кассу')
        bot.send_message(message.chat.id, "Проверьте ваш заказ и нажмите '✅Подтвердить заказ', если вы допустили ошибку, нажмите '❌Отменить заказ'", reply_markup=markup)
        
def get_table_number(message):
    orders[message.chat.id]["table_number"] = message.text
    bot.send_message(message.chat.id, "Напишите свой номер телефона.")
    bot.register_next_step_handler(message, get_number)

def get_number(message):
    orders[message.chat.id]["phone"] = message.text
    bot.send_message(message.chat.id, "Напишите название стартапа")
    bot.register_next_step_handler(message, get_table_name)

def get_table_name(message):

    orders[message.chat.id]["table_name"] = message.text
    
    markup = types.ReplyKeyboardMarkup()

    send = types.KeyboardButton("✅Подтвердить заказ")
    cancel = types.KeyboardButton("❌Отменить заказ")

    markup.row(send, cancel)
    
    bot.send_message(message.chat.id, f'Имя: {orders[message.chat.id]["name"]}\nНомер стола: {orders[message.chat.id]["table_number"]}\nТелефон: {orders[message.chat.id]["phone"]}\nНазвание старт-апа: {orders[message.chat.id]["table_name"]}\n\nВаш заказ: \n{orders[message.chat.id]["order"]}\n\nСумма заказа: {orders[message.chat.id]["price"]}H + 1H(за доставку)\nИтого: {orders[message.chat.id]["price"] + 1}H\n\nЗаказ на доставку')
    bot.send_message(message.chat.id, "Проверьте ваш заказ и нажмите '✅Подтвердить заказ', если вы допустили ошибку, нажмите '❌Отменить заказ'", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "ready":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Отнес заказ на точку", callback_data="delivered")

        markup.row(btn1)

        bot.send_message("-4649840888", callback.message.text, reply_markup=markup)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    if callback.data == "delivered":
        bot.edit_message_text(callback.message.chat.id, callback.message.message_id, text="✅Заказ доставлен")


bot.infinity_polling()