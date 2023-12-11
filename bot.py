from dotenv import load_dotenv
import telebot
import os
import functions

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 'Send me the name of the city to find out the weather')


@bot.message_handler()
def main(message):
    city = message.text
    try:
        datetime, status, temperature, humidity, wind = functions.get_weather(
            city)
        functions.values_to_image(
            datetime, city, temperature, status, humidity, wind)
        functions.get_image()
        photo = open("index.jpg", "rb")
        bot.send_photo(message.chat.id, photo)
        photo.close()
    except Exception:
        bot.send_message(message.chat.id, "The specified city was not found")


bot.polling(none_stop=True)
