import cv2
import os
import glob
import numpy as np
from PIL import Image


def tratar_imagens(pasta_origem, pasta_temp, pasta_destino='ajeitado'):
    arquivos = glob.glob(f"{pasta_origem}/*")
    for arquivo in arquivos:
        nome_arquivo = os.path.basename(arquivo)
        imagem = cv2.imread(arquivo)

        # transformar a imagem em escala de cinza
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

        # Create a mask for blue color (tune if needed)
        hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 160, 0])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Inpaint to remove the blue line
        image_no_line = cv2.inpaint(imagem, blue_mask, 3, cv2.INPAINT_TELEA)
        nome_arquivo_1 = nome_arquivo.replace('.jpeg', '_no_line.jpeg')
        #cv2.imwrite(f'{pasta_temp}/{nome_arquivo_1}', image_no_line)

        # Define range for green color in HSV
        lower_green = np.array([40, 40, 40])   # You can fine-tune these values
        upper_green = np.array([80, 255, 255])

        # Create mask for green areas
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Inpaint to remove the green line
        image_no_line = cv2.inpaint(image_no_line, green_mask, 3, cv2.INPAINT_TELEA)

        # Define lower and upper bounds for red (2 ranges)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # Create two masks for red and combine
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Inpaint to remove the red line
        image_no_line = cv2.inpaint(image_no_line, red_mask, 3, cv2.INPAINT_TELEA)

        # Convert to grayscale again after line removal
        gray_no_line = cv2.cvtColor(image_no_line, cv2.COLOR_BGR2GRAY)
        nome_arquivo_2 = nome_arquivo.replace('.jpeg', '_gray.jpeg')
        #print(f'pasta_temp: {pasta_temp} e nome_arquivo_2: {nome_arquivo_2}')
        #cv2.imwrite(f'{pasta_temp}/{nome_arquivo_2}', gray_no_line)

        _, imagem_tratada = cv2.threshold(gray_no_line, 127, 255, cv2.THRESH_BINARY or cv2.THRESH_OTSU)
        
        # Optional: remove horizontal lines
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
        #imagem_tratada = cv2.morphologyEx(imagem_tratada, cv2.MORPH_OPEN, kernel, iterations=1)

        # Invert back if needed
        #imagem_tratada = cv2.bitwise_not(imagem_tratada)
        #imagem_tratada = cv2.medianBlur(imagem_tratada,3)

        cv2.imwrite(f'{pasta_temp}/{nome_arquivo}', imagem_tratada)

    arquivos = glob.glob(f"{pasta_temp}/*")
    for arquivo in arquivos:
        imagem = Image.open(arquivo)
        imagem = imagem.convert("L")
        #imagem.save(f'temp/{nome_arquivo}')
        imagem2 = Image.new("L", imagem.size, 255)

        for x in range(imagem.size[1]):
            for y in range(imagem.size[0]):
                cor_pixel = imagem.getpixel((y, x))
                #print(f'Cor do pixel: {cor_pixel}')
                if int(cor_pixel) < 127:
                    imagem2.putpixel((y, x), 0)
        nome_arquivo = os.path.basename(arquivo)
        imagem2.save(f'{pasta_destino}/{nome_arquivo}')


if __name__ == "__main__":
    tratar_imagens('bdcaptcha', 'temp_gray', 'ajeitado')
