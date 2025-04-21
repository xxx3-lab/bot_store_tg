import os
import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# Initialize the bot with your token

bot = telebot.TeleBot('7343784880:AAHQYQ6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q6Q')

# Команда страт первый запуск бота и приветствие + вывод меню инлайн с категориями товаров
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в наш магазин!")
    show_categories(message)
    bot.send_message(message.chat.id, "Выберите категорию товаров:")
   # Вывод меню инлайн с категориями товаров
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Категория 1", callback_data="category_1"))



# Категории товаров и их подкатегории (пример) 

categories = {
    "category_1": {"subcategory_1": ["item_1", "item_2"], "subcategory_2": ["item_3", "item_4"]},
    "category_2": {"subcategory_3": ["item_5", "item_6"], "subcategory_4": ["item_7", "item_8"]},
}
# Обработчик нажатия на кнопку категории 1

@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))

def handle_category(call):
    category = call.data  # Получаем выбранную категорию 1
    subcategories = categories[category]  # Получаем подкатегории для выбранной категории 1
    # Вывод меню инлайн с подкатегориями товаров 1
    markup = InlineKeyboardMarkup()
    for subcategory in subcategories:  # Перебираем подкатегории 1
        markup.add(InlineKeyboardButton(subcategory, callback_data=f"{category}_{subcategory}"))  # Добавляем кнопку для каждой подкатегории 1
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите подкатегорию:", reply_markup=markup)
        # Обработчик нажатия на кнопку подкатегории 1
        @bot.callback_query_handler(func=lambda call: call.data.startswith(f"{category}_"))  # Обработчик для подкатегорий 1
        def handle_subcategory(call):  # Обработчик для подкатегорий 1
            subcategory = call.data.split("_")[1]  # Получаем выбранную подкатегорию 1
            products = subcategories[subcategory]  # Получаем товары для выбранной подкатегории 1
            # Вывод меню инлайн с товарами 1
            markup = InlineKeyboardMarkup()  # Создаем новую клавиатуру 1
            for product in products:  # Перебираем товары 1
                markup.add(InlineKeyboardButton(product, callback_data=f"{category}_{subcategory}_{product}"))  # Добавляем кнопку для каждого товара 1
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите товар:", reply_markup=markup)
                # Обработчик нажатия на кнопку товара 1
                @bot.callback_query_handler(func=lambda call: call.data.startswith(f"{category}_{subcategory}_"))  # Обработчик для товаров 1
                def handle_product(call):  # Обработчик для товаров 1
                    product = call.data.split("_")[2]  # Получаем выбранный товар 1
                    # Вывод информации о товаре 1
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы выбрали {product}. Цена: {prices[product]}")
                    # Возврат в главное меню 1
                    bot.send_message(call.message.chat.id, "Возврат в главное меню", reply_markup=main_menu())
                    bot.answer_callback_query(call.id)  # Подтверждение нажатия 1
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  # Удаление сообщения с выбором товара 1
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id + 1)  # Удаление сообщения с возвратом в главное меню 1