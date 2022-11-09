from cryptography.fernet import Fernet

"""ТУТ ВСЕ ФУНКЦИИ ШИФРОВЩИКА/РАСШИФРОВЩИКА
   И ФУНКЦИИ ЗАГРУЗКИ И ВЫГРУЗКИ ТЕКСТОВЫХ ФАЙЛОВ"""

#ШИФРОВЩИК ИЗ МОДУЛЯ CRYPTHOGRAPHY
KEY = b'geHMZFo9UgzPEjYCTA63Q-XRihhq7whkQsn9RZvJrT4='
CIPHER = Fernet(KEY)


#ТОЛЬКО ВЫГРУЖАЕТ ДАННЫЕ ИЗ ФАЙЛА
def unloader(file_title: str) -> list:
	with open(file_title, encoding="utf-8") as file:
		data = file.readlines()
	return data
	

#ТОЛЬКО ЗАГРУЖАЕТ ДАННЫЕ В ФАЙЛ В ОПРЕДЕЛЁННОМ РЕЖИМЕ
def loader(data: list, file_title: str, mod_load: str='w') -> None:
	with open(file_title, mod_load, encoding="utf-8") as file:
		file.writelines(data)
	

#ТОЛЬКО ШИФРУЕТ ДАННЫЕ И ВОЗВРАЩАЕТ ИХ
def encrypto(data: list) -> list:
	return [str(CIPHER.encrypt(item.encode())) + '|' for item in data]


#ТОЛЬКО РАСШИФРОВЫВАЕТ ДАННЫЕ И ВОЗВРАЩАЕТ ИХ
def decrypto(data: str) -> list:
	result = list()
	#ОЧИСТКА ШИФРА ОТ НЕКОТОРЫХ ЭЛЕМЕНТОВ(С НИМИ НЕ РАСШИФРОВАТЬ)
	for item in data.split('|'):
		if item != '\n' and item != '\n\n':
			item = item[2:len(item)-1]
			if item != '':
				result.append(item) 
	return [(CIPHER.decrypt(item.encode())).decode("utf-8") for item in result]
