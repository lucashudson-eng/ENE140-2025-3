import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('8235945672:AAEvnPJIiQO5zDzxsbUQ5--9rOUIBNAg7Ko')
@bot.message_handler(commands=['start', 'help'])
def start(msg):
    # Criando o teclado de opções
    markup = InlineKeyboardMarkup()

    # Criando os botões (text = o que aparece, callback_data = o "comando" secreto que o bot recebe)
    btn_audio = InlineKeyboardButton(
        text="🎙️ Transcrever Áudio", callback_data="opcao_audio")
    btn_imagem = InlineKeyboardButton(
        text="🖼️ Identificar Objeto", callback_data="opcao_imagem")

    # Adicionando os botões ao teclado
    markup.add(btn_audio, btn_imagem)

    bot.reply_to(msg, "Olá! O que você gostaria de fazer hoje?",
                 reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def callback_reposta(call):
    if call.data == "opcao_audio":
        bot.send_message(call.message.chat.id, "Perfeito! Me envie um áudio ou mensagem de voz para que eu possa transcrever.")
    
    elif call.data == "opcao_imagem":
        bot.send_message(call.message.chat.id, "Ótimo! Envie uma foto e eu direi o que estou vendo.")
