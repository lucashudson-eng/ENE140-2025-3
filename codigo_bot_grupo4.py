#Bibliotecas necessárias
import os
from telegram import Update # Execute "pip install python-telegram-bot" para intalar esta biblioteca
from telegram.ext import (Application, CommandHandler, MessageHandler, ContextTypes, filters)
    
#Classe mãe com o bot
class BotTelegram:

    # Guarda as informações básicas e prepara o bot
    def __init__(self, token, nomedobot):
        self.__token = token
        self.nomedobot = nomedobot
        self.app = Application.builder().token(self.__token).build()

        # Comandos básicos
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))

        # Resposta para mensagens de texto
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

        #Inicia o bot
        print("Bot ligado.")
        self.app.run_polling()   

    # Responde ao comando /start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Olá! Encaminhe-me uma imagem ou uma mensagem de voz para que eu possa analisar.")

    # Responde ao comando /help
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Sou um bot que reconhece objetos em imagens e transcreve mensagens de voz. Por favor, encaminhe-me uma imagem ou uma mensagem de voz para que eu possa analisar.")

    # Resposta padrão para qualquer mensagem de texto do usuário
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Por favor, encaminhe-me uma imagem ou uma mensagem de voz.")

#Deixando o token não restrável com gitignore (token está como uma variável de ambiente)
token = os.getenv("BOT_TOKEN")
if not token:
    raise RuntimeError("BOT_TOKEN não definido. Defina a variável de ambiente BOT_TOKEN antes de executar o script.")

#Iniciado o bot
bot = BotTelegram(token, "@trabalho_telegram_bot")