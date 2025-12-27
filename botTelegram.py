from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import zipfile
import requests
import cv2
import matplotlib.pyplot as plt
import glob
import random
import os
import time
from ultralytics import YOLO
from telegram import Update

class BotTelegram:
    def __init__(self, token):
        self.__token = token
        self.app = Application.builder().token(token).build()
            #commands
        self.app.add_handler(CommandHandler('start', self.start_command))
        self.app.add_handler(CommandHandler('help', self.help_command))

            #messages
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        
            #deal with errors
        self.app.add_error_handler(self.error)

            #imagem e audio
        self.app.add_handler(MessageHandler(filters.PHOTO, self.router_imagem))
        self.app.add_handler(MessageHandler(filters.VOICE, self.router_audio))

    #comandos
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("bot iniciado")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("envie uma imagem para que o bot descreva os objetos contidos nela ou um áudio para que o bot o transcreva em forma de texto")
    
    #se o usuário enviar uma mensagem
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("mensagens de texto não são compreendidas pelo bot. por favor envie apenas audios ou imagens")
    
    #em caso de erro
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')

    #identificar se a mensagem é um áudio ou imagem
    async def router_imagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot_imagem = BotImagem(update.message, self.model)

    async def router_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Áudio recebido! Processando...")

    #iniciar leitura de mensgaens
    def iniciar_bot(self):
        self.app.run_polling(poll_interval=3)

if __name__ == "__main__":
    token = '8578762728:AAGHWPWoP9qlkCgY8BikH8kpvivhR9_CJlI'
    bot = BotTelegram(token)
    bot.iniciar_bot()

class BotImagem(BotTelegram):
    def __init__(self, token, mensagem):
        super().__init__(token, mensagem)


    model = YOLO("yolov8n.pt")

    # Função para executar a parte do yolo, sendo "image_path" a imagem que quer-se ler
    def aval_img_yolo(self, image_path, model):

        # Está lendo a iamgem que é enviada ao yolo
        image = cv2.imread(image_path)

        if image is None:
                return "Erro ao carregar a imagem."

        # Está executando o yolo
        result = model(image)

        if len(result[0].boxes) == 0:
                return "Nenhum objeto detectado." # Fundamental compreender que  o yolo pré treinado possui limitações

        # Nomes das classes já presentes no yolo
        name_class = result[0].names

        final = "Avaliação da imagem:\n"

        # Esse loop passa por cada parte do yolo já treinasdo e mostra o resultado da análise
        for box in result[0].boxes:
            class_id = int(box.cls)
            confidence = float(box.conf) * 100


            # Desenvolvendo o comportamento da bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])   # bounding box

            # desenha a bounding box (vermelha)
            cv2.rectangle(
            image,
                (x1, y1),
                (x2, y2),
                (0, 0, 255), # vermelho (BGR)
                2
            )

            # Desenha o texto na imagem
            cv2.putText(
            image,
                f"{name_class[class_id]} {confidence:.1f}%",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # Imprime no prompt
            print(
                f"Classe: {name_class[class_id]} | "
                f"Confiança: {confidence:.2f}% | "
                f"Box: ({x1}, {y1}, {x2}, {y2})"
            )

        # Mostra a imagem com bounding boxes
            cv2.imshow("Resultado", image)
        
        cv2.waitKey(0) #apertar qualquer tecla para sair
        
        cv2.destroyAllWindows()

        return final

class BotAudio(BotTelegram):
    def __init__(self, token, mensagem):
        super().__init__(token, mensagem)

    #interpretar a mensagem como um audio


