import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

orders = {}
prices = {
    "🍔Чизбургер|3H": 3,
    "🍔Классика|4H": 4,
    "🍔Двойной|5H": 5,
    "🍟Соль|1H": 1,
    "🍟Сметана и зелень|1H": 1,
    "🥤Кола|1H": 1,
    "🥤Липтон|1H": 1,
    "🥤Яблочный сок|1H": 1
}
menu = ["🍔Чизбургер|3H", "🍔Классика|4H", "🍔Двойной|5H", "🍟Соль|1H", "🍟Сметана и зелень|1H", "🥤Кола|1H", "🥤Липтон|1H", "🥤Яблочный сок|1H"]

@bot.message_handler(commands=['start'])
def start(message):
    # user_form[message.chat.id] = {"skills": ""}
    orders[message.chat.id] = {"order": "", "price": 0}
    
    markup = types.ReplyKeyboardMarkup()
    
    make_an_order = types.KeyboardButton("🛒Сделать заказ")
    
    markup.row(make_an_order)
    bot.send_message(message.chat.id, "Привет! Я бот для принятия заказов. Нажми на кнопку '🛒Сделать заказ', чтобы начать.", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)
    
@bot.message_handler(content_types=['text'])
def on_click(message):

    if message.text == '🛒Сделать заказ':
        markup = types.ReplyKeyboardMarkup()

        cheese = types.KeyboardButton(menu[0])
        classic = types.KeyboardButton(menu[1])
        double = types.KeyboardButton(menu[2])
        
        snack1 = types.KeyboardButton(menu[3])
        snack2 = types.KeyboardButton(menu[4])
        
        drink1 = types.KeyboardButton(menu[5])
        drink2 = types.KeyboardButton(menu[6])
        drink3 = types.KeyboardButton(menu[7])

        ready_order = types.KeyboardButton("✅Я сделал заказ")

        markup.row(cheese, classic, double)
        markup.row(drink1, drink2, drink3)
        markup.row(snack1, snack2)
        markup.row(ready_order)
        
        bot.send_message(message.chat.id, "Выберите позиции из кнопок и нажмите '✅Я сделал заказ'", reply_markup=markup)

    if message.text in menu:
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
        orders[message.chat.id] = {"order": "", "price": 0}

        markup = types.ReplyKeyboardMarkup()

        make_an_order = types.KeyboardButton("🛒Сделать заказ")

        markup.row(make_an_order)
        print(orders)

    if message.text == '✅Подтвердить заказ':    
        markup = types.ReplyKeyboardMarkup()
        # rdy_btn = types.KeyboardButton("✅Готово")
        
        
        bot.send_message(message.chat.id, "Для отправки заказа на кухню, напишите своё имя")
        
        bot.register_next_step_handler(message, get_name)

@bot.message_handler()
def get_name(message):
    global orders
    
    orders[message.chat.id]["name"] = message.text
    


@bot.message_handler()
def on_click2(message):
    pass
    

def check_order(message):
    pass
   

def send_order(message):
    count = 0

    for item in orders[message.chat.id]:
        count += prices[item]
    
    # пересылка в канал с inline


bot.infinity_polling()