import logging
import telebot
from dotenv import load_dotenv
import os
from libs import db
from libs import get_city

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)  # Исправлено

db_path = "storage/db.db"

# Загрузка переменных окружения
load_dotenv()
tg_token = os.getenv("telegram_token")
logging.info("Токен бота загружен.")

bot = telebot.TeleBot(tg_token)
logging.info("Бот загружен.")

@bot.message_handler(commands=["start", "Start"])
def start(message):
    logging.info(f"Сообщение старт для {message.from_user.id}")
    bot.send_message(message.chat.id, "Здравствуйте, я погодный бот. Я расскажу вам погоду в вашем городе прямо сейчас =)")
    bot.send_message(message.chat.id, "Чтобы начать, поставьте свой город командой /set_city или если вы уже настроили город, можете посмотреть погоду командой /weather.")

@bot.message_handler(commands=["help", "Help"])
def help_command(message):
    logging.info(f"Сообщение хелп для {message.from_user.id}")
    bot.send_message(message.chat.id, "Команды:\n/start - вывести стартовое приветствие.\n/set_city - Поставить свой город.\n/weather - Показать погоду в вашем городе.\n/help - Вывести это сообщение.")

@bot.message_handler(commands=["set_city"])
def set_city(message):
    # Исправлено: добавлена запятая для создания кортежа
    check = db.get_data(db_path, "SELECT tg_id FROM main WHERE tg_id = ?", (message.from_user.id,))  
    if check is None:
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Определить город.", callback_data="city_opredelation", request_location=True)
        keyboard.add(button)
        bot.send_message(message.chat.id, "Вы ещё не ставили город, нажмите на кнопку снизу, чтобы определить ваш город.", reply_markup=keyboard)
    else:
        # Здесь можно добавить логику для обработки случая, когда город уже установлен
        bot.send_message(message.chat.id, "Ваш город уже установлен!")

if __name__ == "__main__":  # Исправлено
    bot.polling()
