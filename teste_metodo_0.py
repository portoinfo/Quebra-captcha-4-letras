import cv2
import glob
from PIL import Image
metodos = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV,
]

imagem = cv2.imread("bdcaptcha_teste/pgCaptchaImage004.jpeg")

# transformar a imagem em escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

i = 0
for metodo in metodos:
    i += 1
    _, imagem_tratada = cv2.threshold(imagem_cinza, 147, 215, metodo or cv2.THRESH_OTSU)
    cv2.imwrite(f'testesmetodo/imagem_tratadax_{i}.jpeg', imagem_tratada)

arquivos = glob.glob("testesmetodo/imagem_tratadax_*")
for arquivo in arquivos:
	imagem = Image.open(arquivo)
	imagem = imagem.convert("L")
	imagem2 = Image.new("L", imagem.size, 255)
	idx = 0
	for x in range(imagem.size[1]):
		for y in range(imagem.size[0]):
			cor_pixel = imagem.getpixel((y, x))
	#        if  (int(cor_pixel) != 127 and idx < 100):
	#            print(f'A cor do pixel: {cor_pixel}\n')
	#            idx += 1
			if int(cor_pixel) < 120:
				imagem2.putpixel((y, x), 0)
	arquivo_final = arquivo.replace('.jpeg', '_final.jpeg')
	imagem2.save(arquivo_final)

