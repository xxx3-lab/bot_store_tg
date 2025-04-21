# Телеграмм бот для предложения услуг из портфолио ── Telegram bot, Sql Date, Data Visualization, UI/UX Design а именно Ahiteo Tech
import telebot
import os
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('№') # Токен бота

# обработчик каманды /start где будет написанно Ahiteo Tech и мои виды услгу + будет выход инлайн клавиатуры с кнопкой Заказать услугу
@bot.message_handler(commands=['start']) # Обработчик команды /start
def start(message):
    bot.send_message(message.chat.id, 'Ahiteo Tech ваш помощник в мире IT, предлагаем услуги по разработке сайтов, ботов, программного обеспечения и многое другое.', reply_markup=keyboard) # Отправка сообщения с текстом Ahiteo Tech
    # инлайн клавиатура с кнопкой Заказать услугу
    keyboard = InlineKeyboardMarkup() # Создание инлайн клавиатуры
    keyboard.add(InlineKeyboardButton('Заказать услугу', callback_data='order')) # Добавление кнопки Заказать услугу
