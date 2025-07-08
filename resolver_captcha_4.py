from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import cv2
import pickle
from tratar_captcha_1 import tratar_imagens

def quebrar_captcha():
    # importar o modelo que a gente treinou e importar o tradutor
    with open("rotulos_modelo.dat", "rb") as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    modelo = load_model("modelo_treinado.hdf5")

    # usar o modelo pra resolver os catpchas
    tratar_imagens("resolver", pasta_destino="resolver")
    # ler todos os arquivos da pasta "resolver"
    ######
    arquivos = list(paths.list_images("resolver"))
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        # em preto e branco
        _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

        # encontrar os contornos de cada letra
        contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regiao_letras = []

        # filtrar os contornos que são realmente de letras
        for contorno in contornos:
            (x, y, largura, altura) = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if area > 115:
                regiao_letras.append((x, y, largura, altura))

        regiao_letras = sorted(regiao_letras, key=lambda x: x[0])
        # desenhar os contornos e separar as letras em arquivos individuais
        imagem_final = cv2.merge([imagem] * 3)
        previsao = []

        for retangulo in regiao_letras:
            x, y, largura, altura = retangulo
            imagem_letra = imagem[y - 2:y + altura + 2, x - 2:x + largura + 2]

            # dar a letra pra inteligencia artificial descobrir que letra é essa
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

            # tratamento para o Keras funcionar
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append(letra_prevista)

        texto_previsao = "".join(previsao)
        print(f'Arquivo lido: {arquivo} e texto previsto: {texto_previsao}')
        #return texto_previsao


if __name__ == "__main__":
    quebrar_captcha()
