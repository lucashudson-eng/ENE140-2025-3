from telegram.ext import ApplicationBuilder
import zipfile
import requests
import cv2
import matplotlib.pyplot as plt
import glob
import random
import os
import time
from ultralytics import YOLO

class BotTelegram:
    def __init__(self, token, mensagem):
        self.__token = token
        self.mensagem = mensagem

    token = '7812768588:AAFyWirqLGt_B-cdMip7sWMp8n_bVBYvzyo'

    builder = ApplicationBuilder().token(token).build()
    
    #criar função de interpretação de mensagem, se é audio ou imagem


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
