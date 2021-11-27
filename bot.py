import key
import telebot

api_token = key.API_TOKEN

bot = telebot.TeleBot(api_token,parse_mode=None)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if(message.text=="start"):
	    bot.reply_to(message, "Send me a picture in PNG or JPEG format")
    else:
        bot.reply_to(message, "To use me, send an image that you would like to be made as a sticker (in PNG or JPEG format) and i will return the formatted image")
        
bot.infinity_polling()