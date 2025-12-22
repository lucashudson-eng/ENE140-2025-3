
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('8235945672:AAEvnPJIiQO5zDzxsbUQ5--9rOUIBNAg7Ko')

@bot.message_handler(commands=['start', 'help']) # Adicionado 'commands='
def start(msg: telebot.types.Message):
    bot.reply_to(msg, 'Olá! Selecione uma das funções:')

# ESTA LINHA É ESSENCIAL: ela faz o bot ficar "ouvindo" o Telegram
print("Bot rodando...")
bot.polling()