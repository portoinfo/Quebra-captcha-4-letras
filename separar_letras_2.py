import cv2
import os
import glob

def separar(pasta_origem, qtde_letras = 5):
	arquivos = glob.glob(f'{pasta_origem}/*')
	for arquivo in arquivos:
		print(f'Arquivo: {arquivo}')
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
			#if area >= 40.0:
			#	print(f'Area: {area}, Largura: {largura}, Altura: {altura}')
			if area >= 40:
				regiao_letras.append((x, y, largura, altura))
		print(f'Regiões encontradas: {len(regiao_letras)}')
		if len(regiao_letras) != qtde_letras:
			pass#continue
		# desenhar os contornos e separar as letras em arquivos individuais
		imagem_final = cv2.merge([imagem] * 3)

		i = 0
		for retangulo in regiao_letras:
			x, y, largura, altura = retangulo
			imagem_letra = imagem[y-2:y+altura+2, x-2:x+largura+2]
			i += 1
			nome_arquivo = os.path.basename(arquivo).replace(".jpeg", f"letra{i}.jpeg")
			cv2.imwrite(f'letras/{nome_arquivo}', imagem_letra)
			cv2.rectangle(imagem_final, (x-2, y-2), (x+largura+2, y+altura+2), (0, 255, 0), 1)
		nome_arquivo = os.path.basename(arquivo)
		cv2.imwrite(f"identificado/{nome_arquivo}", imagem_final)

if __name__ == "__main__":
	separar('ajeitado', 4)
	print("Letras separadas com sucesso!")	