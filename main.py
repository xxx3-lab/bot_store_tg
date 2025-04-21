import telebot
from telebot import types
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
bot = telebot.TeleBot('7717396942:AAHHTTG5Bx9UsExbsCVMxMRGhJg70_ZahNU')

# Ваш ID для получения уведомлений
YOUR_TELEGRAM_ID = 5744368771  # Замените на ваш Telegram ID

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
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for service_key, service_data in services.items():
        keyboard.add(types.InlineKeyboardButton(service_data['name'], callback_data=f"service_{service_key}"))
    return keyboard


# Обработчик выбора услуги
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def handle_service_selection(call):
    try:
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
    except Exception as e:
        logger.error(f"Error in handle_service_selection: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


# Клавиатура для оплаты или связи
def get_payment_or_contact_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("💳 Оплатить", callback_data="pay"),
        types.InlineKeyboardButton("📞 Связаться со мной", callback_data="contact"),
        types.InlineKeyboardButton("📝 Создать чат для ТЗ", callback_data="create_chat")
    )
    return keyboard


# Обработчик создания чата для ТЗ
@bot.callback_query_handler(func=lambda call: call.data == 'create_chat')
def handle_create_chat(call):
    try:
        user_id = call.from_user.id
        username = call.from_user.username
        chat_id = call.message.chat.id

        # Формируем текст уведомления
        notification_text = (
            f"🔔 Новый запрос на создание чата для ТЗ!\n"
            f"ID пользователя: {user_id}\n"
            f"Username: @{username}\n"
            f"Чат ID: {chat_id}"
        )

        # Отправляем уведомление администратору
        bot.send_message(YOUR_TELEGRAM_ID, notification_text)

        # Ответ пользователю
        bot.send_message(
            chat_id,
            "Чат для ТЗ создан! Я свяжусь с вами в ближайшее время."
        )
    except Exception as e:
        logger.error(f"Error in handle_create_chat: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


# Обработчик оплаты
@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def handle_payment(call):
    try:
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
    except Exception as e:
        logger.error(f"Error in handle_payment: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


# Обработчик связи с вами
@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def handle_contact(call):
    try:
        user_id = call.from_user.id
        username = call.from_user.username
        chat_id = call.message.chat.id

        # Формируем текст уведомления
        notification_text = (
            f"🔔 Новый запрос на связь!\n"
            f"ID пользователя: {user_id}\n"
            f"Username: @{username}\n"
            f"Чат ID: {chat_id}"
        )

        # Отправляем уведомление администратору
        bot.send_message(YOUR_TELEGRAM_ID, notification_text)

        # Ответ пользователю
        bot.send_message(
            chat_id,
            "Спасибо за обращение! Я свяжусь с вами в течение 24 часов."
        )
    except Exception as e:
        logger.error(f"Error in handle_contact: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


# Запуск бота
if __name__ == '__main__':
    while True:
        try:
            logger.info("Бот запущен...")
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(f"Critical error: {e}")
            logger.info("Перезапуск бота через 5 секунд...")
            time.sleep(5)