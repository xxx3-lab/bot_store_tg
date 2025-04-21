import telebot
from telebot import types
import os

# Токен вашего бота
bot = telebot.TeleBot('7717396942:AAHHTTG5Bx9UsExbsCVMxMRGhJg70_ZahNU')

# Ваш ID для получения уведомлений
YOUR_TELEGRAM_ID = 123456789  # Замените на ваш Telegram ID

# Словарь для хранения услуг и их цен
services = {
    'website': {'name': 'Разработка сайтов', 'price': 500},
    'bot': {'name': 'Разработка ботов', 'price': 300},
    'software': {'name': 'Разработка программного обеспечения', 'price': 1000},
    'consultation': {'name': 'Консультация', 'price': 100}
}

# Словарь для отслеживания состояния пользователей
user_states = {}

# Приветственное сообщение и инлайн клавиатура
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_states[user_id] = {'username': username, 'state': 'awaiting_service'}

    bot.send_message(
        message.chat.id,
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Ahiteo Tech — ваш помощник в мире IT.\n"
        "Мы предлагаем следующие услуги:\n"
        "- Разработка сайтов\n"
        "- Разработка ботов\n"
        "- Разработка программного обеспечения\n"
        "- Консультация\n\n"
        "Чтобы сделать заказ, нажмите кнопку ниже.",
        reply_markup=get_services_keyboard()
    )


# Клавиатура с услугами
def get_services_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for service_key, service_data in services.items():
        keyboard.add(InlineKeyboardButton(service_data['name'], callback_data=f"service_{service_key}"))
    return keyboard


# Обработчик выбора услуги
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def handle_service_selection(call):
    service_key = call.data.split('_')[1]
    service = services.get(service_key)

    if service:
        user_states[call.from_user.id]['selected_service'] = service_key
        bot.send_message(
            call.message.chat.id,
            f"Вы выбрали услугу: *{service['name']}*\n"
            f"Стоимость: ${service['price']}\n\n"
            "Выберите действие:",
            reply_markup=get_payment_or_contact_keyboard(),
            parse_mode='Markdown'
        )


# Клавиатура для оплаты или связи
def get_payment_or_contact_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💳 Оплатить", callback_data="pay"),
        InlineKeyboardButton("📞 Связаться со мной", callback_data="contact")
    )
    return keyboard


# Обработчик оплаты
@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def handle_payment(call):
    service_key = user_states[call.from_user.id].get('selected_service')
    service = services.get(service_key)

    if service:
        bot.send_message(
            call.message.chat.id,
            f"Оплата услуги *{service['name']}* (${service['price']})\n"
            "Для оплаты перейдите по ссылке: [Оплатить](https://example.com/pay)\n\n"
            "После оплаты свяжитесь со мной для подтверждения.",
            parse_mode='Markdown'
        )


# Обработчик связи с вами
@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def handle_contact(call):
    user_id = call.from_user.id
    username = call.from_user.username
    chat_id = call.message.chat.id

    # Отправка уведомления вам
    notification_text = (
        f"🔔 Новый запрос на связь!\n"
        f"ID пользователя: {user_id}\n"
        f"Username: @{username}\n"
        f"Чат ID: {chat_id}"
    )
    bot.send_message(YOUR_TELEGRAM_ID, notification_text)

    # Ответ пользователю
    if username:
        bot.send_message(
            chat_id,
            "Спасибо за обращение! Я свяжусь с вами в течение 24 часов в личных сообщениях."
        )
    else:
        bot.send_message(
            chat_id,
            "У вас нет username. Для связи через бота нажмите кнопку ниже.",
            reply_markup=get_start_chat_keyboard()
        )


# Клавиатура для начала диалога через бота
def get_start_chat_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Начать диалог через бота", callback_data="start_chat"))
    return keyboard


# Обработчик начала диалога через бота
@bot.callback_query_handler(func=lambda call: call.data == 'start_chat')
def handle_start_chat(call):
    user_id = call.from_user.id
    user_states[user_id]['state'] = 'chatting'

    bot.send_message(
        call.message.chat.id,
        "Введите ваше сообщение, и я передам его владельцу бота."
    )


# Обработчик текстовых сообщений в режиме диалога
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'chatting')
def handle_chat_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text

    # Пересылка сообщения вам
    forwarded_message = (
        f"💬 Сообщение от пользователя:\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Текст: {text}"
    )
    bot.send_message(YOUR_TELEGRAM_ID, forwarded_message)

    # Ответ пользователю
    bot.send_message(
        message.chat.id,
        "Ваше сообщение успешно отправлено! Ждите ответа."
    )


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)